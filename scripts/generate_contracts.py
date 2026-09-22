"""Validate implemented transport against the catalog; generate or check OpenAPI/TS."""

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from zuno_edu.bootstrap.app import create_app

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
        if name not in catalog_schemas:
            raise ValueError("Undocumented transport schema: " + name)
        expected = catalog_schemas[name]
        fields = {field["name"] for field in expected["fields"]}
        required = {field["name"] for field in expected["fields"] if field["required"]}
        if (
            set(schema.get("properties", {})) != fields
            or set(schema.get("required", [])) != required
            or schema.get("additionalProperties") is not False
        ):
            raise ValueError("Schema fields/required/extra drift: " + name)
        for field in expected["fields"]:
            prop = schema["properties"][field["name"]]
            choices = prop.get("anyOf", [prop])
            nullable = any(choice.get("type") == "null" for choice in choices)
            if nullable != field["nullable"]:
                raise ValueError("Schema nullability drift: " + name)
            primitive = {"string": "string", "integer": "integer", "uuid": "string"}.get(
                field["type"]
            )
            if primitive and not any(choice.get("type") == primitive for choice in choices):
                raise ValueError("Schema primitive type drift: " + name)
            kind = field["type"]
            if kind == "uuid" and prop.get("format") != "uuid":
                raise ValueError("Schema UUID format drift: " + name)
            if kind.endswith("[]"):
                item_type = kind[:-2]
                if prop.get("type") != "array" or prop.get("items", {}).get("$ref") != (
                    "#/components/schemas/" + item_type
                ):
                    raise ValueError("Schema array reference drift: " + name)
            elif kind in catalog_schemas and prop.get("$ref") != "#/components/schemas/" + kind:
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


def generate(check: bool, root: Path = ROOT) -> None:
    document = create_app().openapi()
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
