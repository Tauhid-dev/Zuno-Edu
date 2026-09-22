"""Fail CI on detected secrets; report only file/line/type, never detected values."""

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def public_digest(path: str, match: dict[str, object]) -> bool:
    """Exempt only checksum values in known integrity metadata fields."""
    line = Path(path).read_text(encoding="utf-8").splitlines()[int(str(match["line_number"])) - 1]
    path = path.replace("\\", "/")
    patterns: list[str] = []
    if match["type"] == "Base64 High Entropy String" and path == "pnpm-lock.yaml":
        patterns.append(r"integrity: sha512-([A-Za-z0-9+/=]+)")
    if match["type"] == "Hex High Entropy String":
        if path == "docs/product/scope-lock.json" or path.startswith("memory/completions/"):
            patterns.append(r'"sha256":\s*"([a-f0-9]{64})"')
        if path == "docs/architecture/frontend-catalog.json":
            patterns.append(r'"reviewed_backend_snapshot":\s*"([a-f0-9]{64})"')
        if path.startswith(("docs/planning/", "memory/")):
            patterns.extend(
                [
                    r'"(?:base_master_sha|commit|master_sha_at_last_reconciliation)":\s*"([a-f0-9]{40})"',
                    r"^COMMIT: ([a-f0-9]{40})$",
                ]
            )
    return any(
        hashlib.sha1(value.encode()).hexdigest() == match["hashed_secret"]
        for pattern in patterns
        for value in re.findall(pattern, line)
    )


def main() -> int:
    executable = shutil.which("detect-secrets")
    if executable is None:
        raise RuntimeError("Pinned detect-secrets is required")
    result = subprocess.run(
        [executable, "scan", "--no-verify"], capture_output=True, text=True, check=True
    )
    report = json.loads(result.stdout)
    baseline = json.loads(Path(".secrets.baseline").read_text(encoding="utf-8"))
    allowed = {
        (item["filename"], item["type"], item["hashed_secret"])
        for item in baseline["allowlisted_test_values"]
    }
    findings = {
        path: [
            match
            for match in matches
            if (path.replace("\\", "/"), match["type"], match["hashed_secret"]) not in allowed
            and not public_digest(path, match)
        ]
        for path, matches in report["results"].items()
    }
    for path, matches in findings.items():
        for match in matches:
            print(f"{path}:{match['line_number']}: {match['type']}")
    return int(any(findings.values()))


if __name__ == "__main__":
    sys.exit(main())
