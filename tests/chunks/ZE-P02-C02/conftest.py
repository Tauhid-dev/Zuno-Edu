"""Reuse the established MFA harness for cross-chunk security regressions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ZE-P02-C01"))
