"""Validate implemented transport against the catalog; generate or check OpenAPI/TS."""

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from zuno_edu.bootstrap.app import create_app
from zuno_edu.interfaces.api.identity import create_identity_router
from zuno_edu.modules.identity.application.service import AuthenticationService

ROOT = Path(__file__).resolve().parents[1]
OPENAPI = ROOT / "packages/contracts/openapi.json"
TYPES = ROOT / "packages/contracts/src/generated.ts"


def validate(document: dict[str, Any], root: Path = ROOT) -> None:
    catalog = json.loads(
        (root / "docs/architecture/backend-catalog.json").read_text(encoding="utf-8")
    )
    chunks = json.loads((root / "docs/planning/chunks.json").read_text(encoding="utf-8"))
    operations = {
        (item["route"], item["method"].lower()): item
        for item in catalog["operations"]
        if item["method"] != "WORKER"
    }
    actual = {
        (path, method)
        for path, methods in document["paths"].items()
        for method in methods
        if method in {"get", "post", "put", "patch", "delete"}
    }
    if ("/api/v1/health", "get") not in actual:
        raise ValueError("Missing implemented health route")
    for route in actual - {("/api/v1/health", "get")}:
        if route not in operations:
            raise ValueError("Undocumented HTTP operation")
    implemented = {chunk["id"] for chunk in chunks if chunk["status"] in {"PR_OPEN", "COMPLETE"}}
    for route, operation in operations.items():
        if operation["chunk"] in implemented and route not in actual:
            raise ValueError("Missing implemented catalog operation: " + operation["id"])
    schemas = document["components"]["schemas"]
    catalog_schemas = {item["name"]: item for item in catalog["schemas"]}
    for name, schema in schemas.items():
        if name == "HealthResponse":
            continue
        if name in {"Role", "AccountStatus"}:
            owner, field_name = (
                ("SessionView", "role") if name == "Role" else ("AccountView", "status")
            )
            expected_values = next(
                field["type"]
                for field in catalog_schemas[owner]["fields"]
                if field["name"] == field_name
            )[5:-1].split("|")
            if schema.get("type") != "string" or schema.get("enum") != expected_values:
                raise ValueError("Schema enum drift: " + name)
            continue
        if name not in catalog_schemas:
            raise ValueError("Undocumented transport schema: " + name)
        expected = catalog_schemas[name]
        header_fields = {
            field["name"] for field in expected["fields"] if field.get("location") == "header"
        }
        for route, catalog_operation in operations.items():
            if catalog_operation["request"] != name or route not in actual:
                continue
            parameters = document["paths"][route[0]][route[1]].get("parameters", [])
            for field in expected["fields"]:
                if field["name"] not in header_fields:
                    continue
                matches = [p for p in parameters if p.get("name") == field["name"]]
                if len(matches) != 1 or (
                    matches[0].get("in") != "header"
                    or matches[0].get("required", False) != field["required"]
                    or matches[0].get("schema", {}).get("type") != "string"
                    or matches[0].get("schema", {}).get("format") != field["type"]
                    or "anyOf" in matches[0].get("schema", {})
                ):
                    raise ValueError("Schema fields/header drift: " + name)
        fields = {field["name"] for field in expected["fields"]} - header_fields
        required = {
            field["name"] for field in expected["fields"] if field["required"]
        } - header_fields
        if (
            set(schema.get("properties", {})) != fields
            or set(schema.get("required", [])) != required
            or schema.get("additionalProperties") is not False
        ):
            raise ValueError("Schema fields/required/extra drift: " + name)
        for field in expected["fields"]:
            if field["name"] in header_fields:
                continue
            prop = schema["properties"][field["name"]]
            choices = prop.get("anyOf", [prop])
            nullable = any(choice.get("type") == "null" for choice in choices)
            if nullable != field["nullable"]:
                raise ValueError("Schema nullability drift: " + name)
            nonnull = [choice for choice in choices if choice.get("type") != "null"]
            if len(nonnull) != 1 or len(choices) != 1 + int(field["nullable"]):
                raise ValueError("Schema union drift: " + name)
            primitive = (
                "string"
                if field["type"] in {"string", "uuid", "token", "email", "password", "datetime"}
                else {"integer": "integer", "boolean": "boolean", "version": "integer"}.get(
                    field["type"]
                )
            )
            if primitive and not any(choice.get("type") == primitive for choice in choices):
                raise ValueError("Schema primitive type drift: " + name)
            kind = field["type"]
            if kind.startswith("enum("):
                enum_schema = nonnull[0]
                if "$ref" in enum_schema:
                    enum_schema = schemas.get(enum_schema["$ref"].rsplit("/", 1)[-1], {})
                if enum_schema.get("type") != "string" or enum_schema.get("enum") != kind[
                    5:-1
                ].split("|"):
                    raise ValueError("Schema enum drift: " + name)
            if kind == "uuid" and prop.get("format") != "uuid":
                raise ValueError("Schema UUID format drift: " + name)
            if kind.endswith("[]"):
                item_type = kind[:-2]
                items = prop.get("items", {})
                valid_item = (
                    items.get("type") == "string"
                    if item_type == "string"
                    else items.get("$ref") == "#/components/schemas/" + item_type
                )
                if prop.get("type") != "array" or not valid_item:
                    raise ValueError("Schema array reference drift: " + name)
            elif kind in catalog_schemas and not any(
                choice.get("$ref") == "#/components/schemas/" + kind for choice in choices
            ):
                raise ValueError("Schema reference drift: " + name)
    # DTO shapes must be generated, not redeclared in application TypeScript.
    for base in (root / "apps/web", root / "packages/contracts/src"):
        for path in base.rglob("*.ts*"):
            if path.name == "generated.ts" or any(
                part in {"node_modules", ".next"} for part in path.parts
            ):
                continue
            for name in re.findall(
                r"\b(?:interface|type)\s+(\w+)\s*(?:=\s*\{|\{)", path.read_text(encoding="utf-8")
            ):
                if name in catalog_schemas:
                    raise ValueError("Handwritten catalog DTO: " + name)


def contract_document() -> dict[str, Any]:
    """Describe implemented routes without composing live authentication dependencies."""

    def unavailable(cookie: Callable[[str | None], None]) -> AuthenticationService:
        raise RuntimeError("Contract generation must not invoke authentication")

    app = create_app()
    app.include_router(create_identity_router(unavailable), prefix="/api/v1")
    return app.openapi()


def generate(check: bool, root: Path = ROOT) -> None:
    document = contract_document()
    validate(document, root)
    snapshot = json.dumps(document, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        spec, target = temp / "openapi.json", temp / "generated.ts"
        spec.write_text(snapshot, encoding="utf-8", newline="\n")
        pnpm = shutil.which("pnpm")
        if pnpm is None:
            raise RuntimeError("Pinned pnpm toolchain is required")
        subprocess.run(
            [pnpm, "exec", "openapi-typescript", str(spec), "--output", str(target)],
            cwd=ROOT,
            check=True,
        )
        generated = target.read_text(encoding="utf-8")
    for path, content in (
        (root / OPENAPI.relative_to(ROOT), snapshot),
        (root / TYPES.relative_to(ROOT), generated),
    ):
        if check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                raise ValueError("Generated contract drift: " + str(path.relative_to(root)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generate(args.check)
