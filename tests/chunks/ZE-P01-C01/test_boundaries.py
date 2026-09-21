"""Guard the documented dependency direction before capability code is introduced."""

import ast
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[3] / "apps/api/src/zuno_edu"
FRAMEWORKS = {"fastapi", "starlette", "pydantic", "sqlalchemy", "redis", "httpx", "stripe"}


def violations(source: str, module: str) -> list[str]:
    parts = module.split(".")
    layer = next(
        (name for name in ("domain", "application", "infrastructure") if name in parts), None
    )
    if layer not in {"domain", "application"}:
        return []
    invalid: list[str] = []
    for node in ast.walk(ast.parse(source)):
        imports: list[str] = []
        if isinstance(node, ast.Import):
            imports = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = parts[: -node.level] if node.level else []
            prefix = ".".join([*base, *([node.module] if node.module else [])])
            imports = [f"{prefix}.{alias.name}" for alias in node.names]
        for target in imports:
            tokens = target.split(".")
            if (
                tokens[0] in FRAMEWORKS
                or any(name in tokens for name in ("infrastructure", "interfaces", "bootstrap"))
                or (layer == "domain" and "application" in tokens)
            ):
                invalid.append(target)
    return invalid


def test_capability_imports_respect_dependency_direction() -> None:
    for path in (SOURCE / "modules").rglob("*.py"):
        module = ".".join(("zuno_edu", *path.relative_to(SOURCE).with_suffix("").parts))
        assert not violations(path.read_text(encoding="utf-8"), module), path


@pytest.mark.parametrize(
    "source",
    [
        "import fastapi",
        "from sqlalchemy.orm import Session",
        "from zuno_edu.modules.identity.infrastructure import repository",
        "from ..application import service",
        "from .. import infrastructure",
    ],
)
def test_domain_guard_rejects_framework_and_outward_imports(source: str) -> None:
    assert violations(source, "zuno_edu.modules.identity.domain.entity")


def test_application_guard_rejects_concrete_adapter() -> None:
    assert violations(
        "from ..infrastructure import repository", "zuno_edu.modules.identity.application.service"
    )


def test_domain_guard_allows_standard_library_and_domain_types() -> None:
    assert not violations(
        "from dataclasses import dataclass\nfrom .value import Value",
        "zuno_edu.modules.identity.domain.entity",
    )
