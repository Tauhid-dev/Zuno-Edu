"""Behavioral tests using actual temporary Git repos and injectable authenticated API transport.

The fake replaces only remote GitHub responses; production exposes no evidence-cache flag.
All branch, merge, artifact, freshness, and read-only checks execute Git itself.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[2] / "scripts/reconcile_state.py"
SPEC = importlib.util.spec_from_file_location("reconciler", SCRIPT)
r = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)


class FakeGitHub:
    slug = "example/zuno-edu"

    def __init__(self, repo):
        self.repo, self.records, self.changed = repo, {}, {}

    def pr(self, number):
        if number not in self.records:
            raise r.Blocked("GitHub evidence unavailable")
        return copy.deepcopy(self.records[number])

    def files(self, number):
        return self.changed.get(number, set())

    def open_prs(self):
        return [dict(copy.deepcopy(record), number=number) for number, record in self.records.items()
                if record.get("state") == "open"]

    def file_at(self, revision, path):
        return self.repo.read(revision, path)

    def verify_plan_artifact(self, revision, artifact, merge_raw):
        r.require(r.plan_digest(self.file_at(revision, artifact["path"]), artifact) == artifact["sha256"],
                  "Plan artifact differs from human-merged PR head")


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root, self.origin = self.base / "work", self.base / "origin.git"
        self.root.mkdir()
        self.call(self.base, "git", "init", "--bare", str(self.origin))
        self.git("init", "-b", "master")
        self.git("config", "user.name", "Workflow Test")
        self.git("config", "user.email", "workflow@example.invalid")
        self.git("remote", "add", "origin", str(self.origin))
        self.chunks = [self.chunk("ZE-P01-C01", 1), self.chunk("ZE-P01-C02", 2, ["ZE-P01-C01"]), self.chunk("ZE-P01-C03", 3)]
        self.write_json("docs/planning/chunks.json", self.chunks)
        self.write_json("memory/repository.json", {"schema_version": 1, "expected_origin": str(self.origin),
                          "github_repository": "example/zuno-edu", "default_branch": "master"})
        self.write_json("memory/progress.json", {"schema_version": 1, "completed_chunks": ["ZE-P01-C01"],
                                                  "next_candidate_chunk": "ZE-P01-C02"})
        self.write("docs/product/LAUNCH_SCOPE.md", "Approved complete product scope\n")
        self.write("docs/product/SCOPE_LOCK.md", "STATUS: DRAFT\nSCOPE_VERSION: 1.0\nAPPROVAL_EVIDENCE: none\nLocked body.\n")
        for path in r.CORE_AUTHORITIES:
            if not (self.root / path).exists():
                self.write(path, "Fixture authority for " + path + "\n")
        for chunk in self.chunks:
            self.write_manifest(chunk)
        self.repo = r.Repository(self.root)
        witnesses = []
        for path in sorted(r.mandatory_witnesses(self.repo)):
            witness = {"path": path}
            normalization = r.witness_normalization(path)
            if normalization:
                witness["normalization"] = normalization
            witness["sha256"] = r.plan_digest((self.root / path).read_bytes(), witness)
            witnesses.append(witness)
        self.lock = {"schema_version": 1, "status": "DRAFT", "scope_version": "1.0", "architecture_version": 1,
                     "planning_pr": 1, "plan_artifacts": witnesses}
        self.write_json("docs/product/scope-lock.json", self.lock)
        self.commit("Planning bootstrap")
        self.repo = r.Repository(self.root)
        self.api = FakeGitHub(self.repo)
        self.api.records[1] = self.pr(self.sha(), self.sha())
        self.publish()

    @staticmethod
    def call(cwd, *args):
        return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()

    def git(self, *args):
        return self.call(self.root, "git", *args)

    def sha(self):
        return self.git("rev-parse", "HEAD")

    def write(self, path, body):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)

    def write_json(self, path, body):
        self.write(path, json.dumps(body, indent=2) + "\n")

    def write_manifest(self, chunk):
        self.write(f"docs/planning/chunks/{chunk['id']}.md", "---\n" + json.dumps(chunk, indent=2)
                   + "\n---\n\n# Locked chunk objective\nAcceptance remains fixed.\n")

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-m", message)

    def publish(self):
        self.git("push", "origin", "master")
        self.git("fetch", "origin")

    @staticmethod
    def chunk(cid, seq, deps=None):
        return {"id": cid, "sequence": seq, "dependencies": deps or [], "requirements": [f"REQ-{seq}"],
                "status": "PLANNED", "required_context": ["docs/product/LAUNCH_SCOPE.md"],
                "required_skills": ["skills/workflow/chunk-execution/SKILL.md"], "optional_skills": [],
                "execution": {"pr": None, "completion_evidence": None}}

    @staticmethod
    def pr(merge, head, cid=None, merged=True):
        return {"merged": merged, "state": "closed" if merged else "open", "merged_at": "2026-09-11T00:00:00Z" if merged else None,
                "merged_by": {"type": "User", "login": "human-owner"}, "merge_commit_sha": merge,
                "head": {"sha": head, "ref": f"feature/{cid.lower()}-work" if cid else "feature/planning",
                         "repo": {"full_name": "example/zuno-edu"}},
                "base": {"ref": "master", "repo": {"full_name": "example/zuno-edu"}},
                "body": f"ZUNO_EDU_CHUNK:{cid}" if cid else "Planning scope approved by human merge"}

    def implement(self, index=0, merged=True, mode="squash"):
        chunk = self.chunks[index]
        cid, number = chunk["id"], index + 2
        self.git("checkout", "-b", f"feature/{cid.lower()}-work")
        code, report = f"artifacts/{cid}.txt", f"memory/handoffs/{cid}-review.md"
        self.write(code, f"Observable implementation {cid}\n")
        self.write(report, "Independent review: Critical 0, High 0; required checks passed.\n")
        # Two feature commits deliberately differ from the eventual squash/rebase SHA.
        self.commit(f"feat({cid}): implementation")
        evidence_path = f"memory/completions/{cid}.json"
        evidence = {"schema_version": 1, "chunk_id": cid, "requirements": chunk["requirements"],
                    "artifacts": [{"path": p, "sha256": hashlib.sha256((self.root / p).read_bytes()).hexdigest()}
                                  for p in (code, report)],
                    "verification": [{"name": "Acceptance suite", "result": "PASS", "evidence": report}],
                    "review": {"critical": 0, "high": 0, "evidence": report}}
        chunk["status"] = "PR_OPEN"
        chunk["execution"] = {"pr": number, "completion_evidence": evidence_path}
        self.write_json("docs/planning/chunks.json", self.chunks)
        self.write_manifest(chunk)
        self.write_json(evidence_path, evidence)
        self.commit(f"docs({cid}): review evidence")
        feature_head = self.sha()
        self.git("checkout", "master")
        if merged:
            if mode == "squash":
                self.git("merge", "--squash", f"feature/{cid.lower()}-work")
                self.commit("Human squash merge with arbitrary message")
            elif mode == "rebase":
                # Cherry-picking the feature commits reproduces GitHub rebase merge ancestry.
                commits = self.git("rev-list", "--reverse", f"master..feature/{cid.lower()}-work").splitlines()
                self.git("cherry-pick", *commits)
            else:
                self.git("merge", "--no-ff", f"feature/{cid.lower()}-work", "-m", "Human merge")
        self.api.records[number] = self.pr(self.sha() if merged else None, feature_head, cid, merged)
        self.api.changed[number] = {code, report, evidence_path, "docs/planning/chunks.json"}
        self.publish()
        return evidence_path, code

    def reconcile(self):
        return r.reconcile(self.repo, self.api)

    def test_draft_effectively_locks_after_human_merge_without_master_writes(self):
        before = (self.sha(), self.git("show-ref"), self.git("status", "--porcelain"),
                  {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file() and ".git" not in p.parts})
        state = self.reconcile()
        after = (self.sha(), self.git("show-ref"), self.git("status", "--porcelain"),
                 {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file() and ".git" not in p.parts})
        self.assertEqual(before, after)
        self.assertEqual(state["scope_status"], "LOCKED")
        self.assertEqual(state["next_candidate_chunk"], "ZE-P01-C01")
        self.assertEqual(state["completed_chunks"], [])  # Ignores forged/stale progress cache.

    def test_squash_merged_pr_open_becomes_complete_and_dependency_ready(self):
        self.implement()
        state = self.reconcile()
        self.assertEqual(state["completed_chunks"], ["ZE-P01-C01"])
        self.assertEqual(state["next_candidate_chunk"], "ZE-P01-C02")
        self.assertEqual(state["effective_states"]["ZE-P01-C03"], "READY")
        self.assertFalse(self.repo.ancestor(self.api.records[2]["head"]["sha"], self.sha()))

    def test_rebase_merged_evidence_is_recognized(self):
        self.implement(mode="rebase")
        self.assertEqual(self.reconcile()["completed_chunks"], ["ZE-P01-C01"])

    def test_unmerged_pr_blocks_dependents_but_allows_independent_chunk(self):
        master_before = self.sha()
        self.implement(merged=False)
        self.assertEqual(master_before, self.sha())
        self.assertEqual(self.repo.json("HEAD", "docs/planning/chunks.json")[0]["status"], "PLANNED")
        state = self.reconcile()
        self.assertEqual(state["effective_states"]["ZE-P01-C01"], "PR_OPEN")
        self.assertEqual(state["effective_states"]["ZE-P01-C02"], "PLANNED")
        self.assertEqual(state["next_candidate_chunk"], "ZE-P01-C03")

    def test_duplicate_or_wrong_branch_open_claims_are_blocked(self):
        self.implement(merged=False)
        self.api.records[3] = copy.deepcopy(self.api.records[2])
        self.api.records[3]["head"]["ref"] = "feature/ze-p01-c01-second"
        self.assertEqual(self.reconcile()["effective_states"]["ZE-P01-C01"], "BLOCKED")
        del self.api.records[3]
        self.api.records[2]["head"]["ref"] = "feature/ze-p01-c02-wrong"
        self.assertEqual(self.reconcile()["effective_states"]["ZE-P01-C01"], "BLOCKED")

    def test_persisted_scope_status_preserves_digest_but_version_change_does_not(self):
        self.write("docs/product/SCOPE_LOCK.md", "STATUS: LOCKED\nSCOPE_VERSION: 1.0\nAPPROVAL_EVIDENCE: PR 1 human merge\nLocked body.\n")
        self.commit("Persist effective scope metadata")
        self.publish()
        self.assertEqual(self.reconcile()["scope_status"], "LOCKED")
        self.write("docs/product/SCOPE_LOCK.md", "STATUS: LOCKED\nSCOPE_VERSION: 2.0\nAPPROVAL_EVIDENCE: PR 1 human merge\nLocked body.\n")
        self.commit("Unapproved version change")
        self.publish()
        self.assertEqual(self.reconcile()["scope_status"], "DRAFT")

    def test_omitted_authority_witness_cannot_leave_scope_unprotected(self):
        self.lock["plan_artifacts"] = [a for a in self.lock["plan_artifacts"] if a["path"] != "docs/product/LAUNCH_SCOPE.md"]
        self.write_json("docs/product/scope-lock.json", self.lock)
        self.commit("Planning approval accidentally omits launch scope")
        self.api.records[1] = self.pr(self.sha(), self.sha())
        self.publish()
        self.assertEqual(self.reconcile()["scope_status"], "DRAFT")
        self.write("docs/product/LAUNCH_SCOPE.md", "Silently reduced scope\n")
        self.commit("Exploit missing witness")
        self.publish()
        self.assertEqual(self.reconcile()["scope_status"], "DRAFT")

    def test_chunk_markdown_acceptance_body_is_scope_protected(self):
        path = "docs/planning/chunks/ZE-P01-C01.md"
        self.write(path, (self.root / path).read_text().replace("Acceptance remains fixed.", "Omit difficult acceptance."))
        self.commit("Unapproved chunk body change")
        self.publish()
        self.assertEqual(self.reconcile()["scope_status"], "DRAFT")

    def test_bot_implementation_merge_is_not_human_completion(self):
        self.implement()
        self.api.records[2]["merged_by"]["type"] = "Bot"
        self.assertEqual(self.reconcile()["completed_chunks"], [])

    def test_self_reported_complete_does_not_count(self):
        self.chunks[0]["status"] = "COMPLETE"
        self.write_json("docs/planning/chunks.json", self.chunks)
        self.commit("Claim completion without evidence")
        self.publish()
        state = self.reconcile()
        self.assertEqual(state["completed_chunks"], [])
        self.assertEqual(state["effective_states"]["ZE-P01-C01"], "BLOCKED")

    def test_later_legitimate_artifact_edits_preserve_historical_completion(self):
        _, code = self.implement()
        self.write(code, "Subsequent reviewed extension\n")
        self.commit("Later implementation extends artifact")
        self.publish()
        self.assertEqual(self.reconcile()["completed_chunks"], ["ZE-P01-C01"])

    def test_tampered_manifest_cannot_forge_completion(self):
        path, _ = self.implement()
        witness = json.loads((self.root / path).read_text())
        witness["artifacts"][0]["sha256"] = "0" * 64
        self.write_json(path, witness)
        self.commit("Tampered evidence")
        self.publish()
        self.assertEqual(self.reconcile()["completed_chunks"], [])

    def test_commit_message_is_not_completion_evidence(self):
        self.write("ordinary.txt", "No implementation evidence\n")
        self.commit("feat(ZE-P01-C01): COMPLETE")
        self.publish()
        self.assertEqual(self.reconcile()["completed_chunks"], [])

    def test_wrong_base_and_absent_merge_cannot_complete(self):
        self.implement()
        self.api.records[2]["base"]["ref"] = "develop"
        self.assertEqual(self.reconcile()["completed_chunks"], [])
        self.api.records[2]["base"]["ref"] = "master"
        self.api.records[2]["merge_commit_sha"] = "f" * 40
        self.assertEqual(self.reconcile()["completed_chunks"], [])

    def test_dirty_untracked_wrong_branch_and_diverged_master_stop(self):
        self.write("untracked.txt", "untracked")
        with self.assertRaisesRegex(r.Blocked, "clean"):
            self.reconcile()
        (self.root / "untracked.txt").unlink()
        self.git("checkout", "-b", "feature/unmerged")
        with self.assertRaisesRegex(r.Blocked, "master"):
            self.reconcile()
        self.git("checkout", "master")
        self.write("local.txt", "local commit")
        self.commit("Local divergence")
        with self.assertRaisesRegex(r.Blocked, "differs"):
            self.reconcile()

    def test_stale_remote_tracking_ref_stops(self):
        clone = self.base / "other"
        self.call(self.base, "git", "clone", "--branch", "master", str(self.origin), str(clone))
        self.call(clone, "git", "config", "user.name", "Another Human")
        self.call(clone, "git", "config", "user.email", "human@example.invalid")
        (clone / "remote.txt").write_text("Remote advance\n")
        self.call(clone, "git", "add", ".")
        self.call(clone, "git", "commit", "-m", "Remote merge")
        self.call(clone, "git", "push", "origin", "master")
        with self.assertRaisesRegex(r.Blocked, "stale"):
            self.reconcile()

    def test_scope_unmerged_bot_merge_or_modified_plan_prevents_selection(self):
        self.api.records[1]["merged"] = False
        self.assertIsNone(self.reconcile()["next_candidate_chunk"])
        self.api.records[1]["merged"] = True
        self.api.records[1]["merged_by"]["type"] = "Bot"
        self.assertIsNone(self.reconcile()["next_candidate_chunk"])
        self.api.records[1]["merged_by"]["type"] = "User"
        self.write("docs/product/LAUNCH_SCOPE.md", "Silently reduced scope\n")
        self.commit("Unapproved scope erosion")
        self.publish()
        self.assertIsNone(self.reconcile()["next_candidate_chunk"])

    def test_dependency_graph_rejects_cycles_unknown_dependencies_duplicates(self):
        chunks = copy.deepcopy(self.chunks)
        chunks[0]["dependencies"] = [chunks[1]["id"]]
        with self.assertRaisesRegex(r.Blocked, "cycle"):
            r.validate_plan(chunks)
        chunks[0]["dependencies"] = ["ZE-P99-C99"]
        with self.assertRaisesRegex(r.Blocked, "dependency"):
            r.validate_plan(chunks)
        chunks[0]["dependencies"] = []
        chunks[1]["sequence"] = chunks[0]["sequence"]
        with self.assertRaisesRegex(r.Blocked, "sequence"):
            r.validate_plan(chunks)

    def test_evidence_paths_cannot_escape_repository(self):
        for path in ("../secrets", "/tmp/private", "file:other", "a/../b"):
            with self.assertRaises(r.Blocked):
                r.safe_path(path)

    def test_github_public_fallback_uses_fresh_tls_request(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return None
            def read(self): return b'{"merged": false}'
        with patch.object(r.shutil, "which", return_value=None), patch.dict(r.os.environ, {}, clear=True), \
             patch.object(r, "urlopen", return_value=Response()) as request:
            api = r.GitHub(self.root, "example/zuno-edu")
            self.assertEqual(api.pr(4), {"merged": False})
            req = request.call_args.args[0]
            self.assertEqual(req.full_url, "https://api.github.com/repos/example/zuno-edu/pulls/4")
            self.assertEqual(req.get_header("Cache-control"), "no-cache")
            self.assertIsNone(req.get_header("Authorization"))

    def test_github_rate_limit_stops_selection_without_secret_disclosure(self):
        with patch.object(r.shutil, "which", return_value=None), \
             patch.dict(r.os.environ, {"GH_TOKEN": "secret-token-value"}, clear=True), \
             patch.object(r, "urlopen", side_effect=HTTPError("https://api.github.com", 403, "secret-token-value", {}, None)):
            api = r.GitHub(self.root, "example/zuno-edu")
            with self.assertRaises(r.AuthorityUnavailable) as raised:
                r.reconcile(self.repo, api)
            self.assertIn("HTTP 403", str(raised.exception))
            self.assertNotIn("secret-token-value", str(raised.exception))

    def test_github_scope_raw_witnesses_share_one_tree_query(self):
        raw = b"same file bytes\n"
        blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        response = {"truncated": False, "tree": [
            {"path": p, "sha": blob, "mode": "100644", "type": "blob"} for p in ("one.md", "two.md")]}
        with patch.object(r.shutil, "which", return_value=None):
            api = r.GitHub(self.root, "example/zuno-edu")
        with patch.object(api, "api", return_value=response) as query:
            for path in ("one.md", "two.md"):
                api.verify_plan_artifact(self.sha(), {"path": path, "sha256": hashlib.sha256(raw).hexdigest()}, raw)
            self.assertEqual(query.call_count, 1)
        api._trees.clear()
        with patch.object(api, "api", return_value={"truncated": True, "tree": []}):
            with self.assertRaisesRegex(r.Blocked, "truncated"):
                api.verify_plan_artifact(self.sha(), {"path": "one.md"}, raw)


if __name__ == "__main__":
    unittest.main()
