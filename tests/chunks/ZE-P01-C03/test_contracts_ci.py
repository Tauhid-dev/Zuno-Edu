"""Negative CI gates: contract drift, orphan requirements, and untrusted PR safety."""

import copy
import importlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import generate_contracts as contracts  # noqa: E402
from zuno_edu.bootstrap.app import create_app  # noqa: E402

plan = importlib.import_module("validate_plan")


def test_checked_in_types_are_generated_and_drift_fails(tmp_path: Path) -> None:
    for directory in ("docs", "packages/contracts"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    # Resolve pinned generator from the actual installed toolchain, using the isolated output root.
    contracts.generate(True, tmp_path)
    target = tmp_path / "packages/contracts/src/generated.ts"
    target.write_text(
        target.read_text(encoding="utf-8") + "\n// unexpected drift\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="Generated contract drift"):
        contracts.generate(True, tmp_path)


def test_catalog_rejects_missing_routes_schema_changes_and_duplicate_dtos(tmp_path: Path) -> None:
    document = create_app().openapi()
    invalid = copy.deepcopy(document)
    invalid["paths"].clear()
    with pytest.raises(ValueError, match="Missing implemented"):
        contracts.validate(invalid)
    invalid = copy.deepcopy(document)
    invalid["components"]["schemas"]["Error"]["required"].remove("code")
    with pytest.raises(ValueError, match="Schema fields"):
        contracts.validate(invalid)
    invalid = copy.deepcopy(document)
    invalid["components"]["schemas"]["Error"]["properties"]["message"]["type"] = "integer"
    with pytest.raises(ValueError, match="primitive type"):
        contracts.validate(invalid)
    for field, change in (("request_id", {"type": "string"}), ("field_errors", {"type": "string"})):
        invalid = copy.deepcopy(document)
        invalid["components"]["schemas"]["Error"]["properties"][field] = change
        with pytest.raises(ValueError, match="Schema .* drift"):
            contracts.validate(invalid)
    shutil.copytree(ROOT / "docs", tmp_path / "docs")
    (tmp_path / "apps/web").mkdir(parents=True)
    (tmp_path / "apps/web/duplicate.ts").write_text(
        "export interface Error { code: string }", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="Handwritten catalog DTO"):
        contracts.validate(document, tmp_path)


def test_plan_coverage_validator_detects_orphan_requirement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shutil.copytree(ROOT / "docs", tmp_path / "docs")
    shutil.copytree(ROOT / "skills", tmp_path / "skills")
    path = tmp_path / "docs/product/requirements.json"
    requirements = json.loads(path.read_text(encoding="utf-8"))
    requirements.append({**requirements[0], "id": "TEST-ORPHAN"})
    path.write_text(json.dumps(requirements), encoding="utf-8")
    monkeypatch.setattr(plan, "ROOT", tmp_path)
    with pytest.raises(ValueError, match="Orphan requirements"):
        plan.validate()


def assert_untrusted_safe(workflow: dict[str, Any]) -> None:
    assert set(workflow["on"]) <= {"pull_request", "push"}
    assert workflow["permissions"] == {"contents": "read"}
    text = json.dumps(workflow)
    assert not re.search(r"\bsecrets\s*[.\[]", text)
    assert "pull_request_target" not in text and "workflow_run" not in text
    assert "continue-on-error" not in text
    for job in workflow["jobs"].values():
        assert job["runs-on"] == "ubuntu-latest"
        assert "permissions" not in job
        for step in job["steps"]:
            if "uses" in step:
                assert re.fullmatch(r"actions/[a-z-]+@[0-9a-f]{40}", step["uses"])
                if step["uses"].startswith("actions/checkout@"):
                    assert step["with"]["persist-credentials"] == "false"
            if "run" in step:
                assert "${{" not in step["run"]


def test_no_secret_bearing_ci_on_untrusted_pr() -> None:
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        assert_untrusted_safe(workflow)
        for field, value in (
            ("on", {"pull_request_target": {}}),
            ("permissions", {"contents": "write"}),
        ):
            invalid = copy.deepcopy(workflow)
            invalid[field] = value
            with pytest.raises(AssertionError):
                assert_untrusted_safe(invalid)
        invalid = copy.deepcopy(workflow)
        invalid["jobs"][next(iter(invalid["jobs"]))]["env"] = {"TOKEN": "${{ secrets.PRODUCTION }}"}
        with pytest.raises(AssertionError):
            assert_untrusted_safe(invalid)
    quality = (ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    for gate in (
        "generate_contracts.py --check",
        "pip-audit",
        "pnpm audit",
        "check_secrets.py",
        "pytest tests/chunks",
        "mypy",
        "ruff",
        "next build",
        "--frozen-lockfile",
    ):
        assert gate in quality


def test_secret_scan_rejects_seeded_private_key(tmp_path: Path) -> None:
    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    # Assemble a clearly synthetic scanner canary without checking in a key-shaped secret.
    key = (
        "-----BEGIN "
        + "RSA PRIVATE KEY-----\nsynthetic-test-content\n-----END RSA PRIVATE KEY-----"
    )
    (tmp_path / "canary.txt").write_text(key, encoding="utf-8")
    (tmp_path / ".secrets.baseline").write_text('{"allowlisted_test_values": []}', encoding="utf-8")
    subprocess.run(["git", "add", "canary.txt"], cwd=tmp_path, check=True, capture_output=True)
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/check_secrets.py")],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 1 and "Private Key" in result.stdout
    assert "synthetic-test-content" not in result.stdout
