"""Routing safety and bounded context using the real plan in isolated copies."""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import next_chunk as routing
from reconcile_state import Blocked


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for name in ("docs", "skills", "memory"):
            shutil.copytree(ROOT / name, self.root / name)
        self.chunks, self.router = routing.load(self.root)
        self.byid = {c["id"]: c for c in self.chunks}

    def test_all_actual_routes_and_current_handoff_validate(self):
        self.assertEqual(routing.validate_workflow(self.root)["routed_chunks"], 62)

    def test_low_risk_established_crud_uses_lightweight_review(self):
        # A genuinely isolated established-pattern change can use the low route;
        # it cannot override an existing sensitive chunk's floor.
        chunk = copy.deepcopy(self.byid["ZE-P03-C02"])
        chunk["workflow"].update(review_risk="low", context_budget_tokens=6000)
        packet = routing.resolve(self.root, chunk, self.router)
        self.assertEqual(packet["review"]["depth"], "lightweight")
        self.assertFalse(packet["review"]["independent"])
        self.assertEqual(packet["model"]["reasoning"], "low")
        self.assertFalse(any("frontend/" in ref for ref in packet["instructions_by_phase"]["execution"]))

    def test_sensitive_routes_require_independent_deep_review(self):
        for cid in ("ZE-P02-C01", "ZE-P02-C02", "ZE-P06-C03", "ZE-P12-C03"):
            with self.subTest(chunk=cid):
                packet = routing.resolve(self.root, self.byid[cid], self.router)
                self.assertEqual(packet["review"]["depth"], "deep")
                self.assertTrue(packet["review"]["independent"])
                with self.assertRaisesRegex(Blocked, "downgraded"):
                    routing.resolve(self.root, self.byid[cid], self.router, "low")

    def test_first_foundation_uses_medium_without_maximum_default(self):
        packet = routing.resolve(self.root, self.chunks[0], self.router)
        self.assertEqual(packet["model"]["model"], "gpt-5.6-terra")
        self.assertEqual(packet["model"]["reasoning"], "medium")

    def test_targeted_contract_excludes_unrelated_operations(self):
        c = self.byid["ZE-P06-C03"]
        oid = c["api_operations"][0]
        value = routing.context(self.root, c, self.router, "operation:" + oid)
        self.assertEqual(value["content"]["id"], oid)
        self.assertLess(value["estimated_tokens"], 4000)
        other = self.byid["ZE-P02-C01"]["api_operations"][0]
        with self.assertRaisesRegex(Blocked, "outside this chunk"):
            routing.context(self.root, c, self.router, "operation:" + other)
        expanded = routing.context(self.root, c, self.router, "operation:" + other, "dependency_gap")
        self.assertEqual(expanded["expansion_reason"], "dependency_gap")

    def test_frontend_route_mapping_and_presentation_contracts_are_reachable(self):
        c = next(c for c in self.chunks if "PublishedPage" in c["frontend_components"])
        route = routing.context(self.root, c, self.router, "route:/")
        self.assertIn("guard", route["content"])
        mapping = routing.context(self.root, c, self.router, "mapping:PublishedPage")
        self.assertTrue(all(m["component"] == "PublishedPage" for m in mapping["content"]))
        with self.assertRaisesRegex(Blocked, "outside this chunk"):
            routing.context(self.root, self.chunks[0], self.router, "route:/")
        expanded = routing.context(self.root, self.chunks[0], self.router,
                                   "presentation_type:DownloadHandoff", "dependency_gap")
        self.assertIn("DownloadHandoff", expanded["content"])

    def test_expanded_service_retains_method_contracts(self):
        value = routing.context(self.root, self.chunks[0], self.router,
                                "service:PublicContentService", "dependency_gap")
        self.assertTrue(value["content"]["methods"])
        self.assertTrue(any(m["name"] == "get_page" for m in value["content"]["methods"]))

    def test_medium_integration_model_and_raised_risk_take_precedence(self):
        c = copy.deepcopy(self.chunks[0])
        c["workflow"]["route"] = "integration"
        self.assertEqual(routing.resolve(self.root, c, self.router)["model"]["model"], "gpt-5.6-sol")
        packet = routing.resolve(self.root, c, self.router, "high")
        self.assertEqual(packet["model"]["model"], "gpt-6-astra")
        self.assertIn("python_paths", packet["validation_parameters"])

    def test_budget_overflow_requires_explicit_reason_not_truncation(self):
        c = self.chunks[0]
        target = self.root / "docs/standards/ENGINEERING_STANDARDS.md"
        target.write_text("Necessary contract detail. " * 2000)
        item = "file:docs/standards/ENGINEERING_STANDARDS.md"
        with self.assertRaisesRegex(Blocked, "narrow the reference"):
            routing.context(self.root, c, self.router, item)
        value = routing.context(self.root, c, self.router, item, "contract_ambiguity")
        self.assertEqual(value["content"], target.read_text())
        self.assertGreater(value["estimated_tokens"], 4000)

    def test_whole_catalog_history_and_path_escape_are_rejected(self):
        for item in ("file:docs/architecture/backend-catalog.json", "file:../../secret",
                     "file:memory/handoffs/BOOTSTRAP.md"):
            with self.subTest(item=item), self.assertRaises(Blocked):
                routing.context(self.root, self.chunks[0], self.router, item)
        value = routing.context(self.root, self.chunks[0], self.router,
                                "file:memory/handoffs/BOOTSTRAP.md", "regression_audit")
        self.assertIn("Bootstrap", value["content"])

    def test_missing_route_reference_and_weak_review_policy_fail(self):
        (self.root / "skills/backend/python/SKILL.md").unlink()
        with self.assertRaisesRegex(Blocked, "Missing route reference"):
            routing.validate_workflow(self.root)
        shutil.copy2(ROOT / "skills/backend/python/SKILL.md", self.root / "skills/backend/python/SKILL.md")
        self.router["risk"]["high"]["independent"] = False
        (self.root / "docs/planning/workflow-routing.json").write_text(json.dumps(self.router))
        with self.assertRaisesRegex(Blocked, "weaken review"):
            routing.validate_workflow(self.root)

    def test_handoff_and_state_validation(self):
        path = self.root / "memory/CURRENT_HANDOFF.md"
        path.write_text(path.read_text() + " extra" * 251)
        with self.assertRaisesRegex(Blocked, "250 words"):
            routing.validate_workflow(self.root)
        shutil.copy2(ROOT / "memory/CURRENT_HANDOFF.md", path)
        state = routing.read(self.root, "memory/progress.json")
        state["next_candidate_chunk"] = "ZE-UNKNOWN"
        (self.root / "memory/progress.json").write_text(json.dumps(state))
        with self.assertRaisesRegex(Blocked, "Unknown state chunk"):
            routing.validate_workflow(self.root)

    def test_conditional_forecast_never_selects_completed_or_mutates_plan(self):
        # Pin execution state in this fixture; real chunks advance as PRs are opened.
        chunks = copy.deepcopy(self.chunks)
        for chunk in chunks:
            chunk["status"] = "PLANNED"
            chunk["blockers"] = []
        snapshot = copy.deepcopy(chunks)
        candidate = routing.forecast(chunks, "ZE-P01-C01", [])
        self.assertEqual(candidate["id"], "ZE-P01-C02")
        candidate = routing.forecast(chunks, "ZE-P01-C01", ["ZE-P01-C02"])
        self.assertEqual(candidate["id"], "ZE-P01-C03")
        self.assertEqual(chunks, snapshot)
        for chunk in chunks:
            if chunk["id"] == "ZE-P01-C02":
                chunk["status"] = "IN_PROGRESS"
        candidate = routing.forecast(chunks, "ZE-P01-C01", [])
        self.assertEqual(candidate["id"], "ZE-P01-C03")


if __name__ == "__main__":
    unittest.main()
