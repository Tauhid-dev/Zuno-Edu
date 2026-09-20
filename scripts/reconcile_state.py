#!/usr/bin/env python3
"""Read-only reconciliation against freshly advertised origin/master and live GitHub evidence.

No fetch, checkout, update-ref, file writes, or cached PR evidence are performed here.
Synchronize as documented before invoking. Standard-library Python 3.11+ only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


STATES = {"PLANNED", "READY", "BLOCKED", "IN_PROGRESS", "PR_OPEN", "COMPLETE"}
SHA = re.compile(r"^[0-9a-f]{40,64}$")
CORE_AUTHORITIES = {
    "docs/planning/workflow-routing.json", "docs/planning/AGENT_WORKFLOW.md",
    "docs/product/requirements.json", "docs/planning/chunks.json",
    *{f"docs/product/{name}.md" for name in (
        "PRODUCT_DEFINITION", "LAUNCH_SCOPE", "OUT_OF_SCOPE", "FUTURE_CONSIDERATIONS",
        "FUNCTIONAL_REQUIREMENTS", "NON_FUNCTIONAL_REQUIREMENTS", "DATA_REQUIREMENTS",
        "ROLE_CAPABILITIES", "USER_JOURNEYS", "LAUNCH_ACCEPTANCE_CRITERIA", "SCOPE_LOCK")},
    *{f"docs/architecture/{name}.md" for name in (
        "SYSTEM_ARCHITECTURE", "BACKEND_ARCHITECTURE", "DOMAIN_MODEL", "AGGREGATES",
        "BACKEND_OBJECT_CATALOG", "BACKEND_SERVICE_CATALOG", "PORTS_AND_REPOSITORIES",
        "DATA_MODEL", "DATABASE_SCHEMA_PLAN", "API_ARCHITECTURE", "API_CATALOG",
        "API_SCHEMA_CATALOG", "AUTHORIZATION_MODEL", "PERMISSION_MATRIX", "DATA_ACCESS_BOUNDARIES",
        "SECURITY_ARCHITECTURE", "FRONTEND_ARCHITECTURE", "FRONTEND_ROUTE_MAP",
        "FRONTEND_COMPONENT_CATALOG", "FRONTEND_STATE_AND_API_MODEL", "FRONTEND_BACKEND_MAPPING",
        "CODE_BLUEPRINT", "INTEGRATIONS", "BILLING_ARCHITECTURE", "LIVE_CLASS_ARCHITECTURE",
        "CALENDAR_ARCHITECTURE", "COMMUNICATION_ARCHITECTURE", "FILE_STORAGE_ARCHITECTURE",
        "DEPLOYMENT_ARCHITECTURE")},
    "docs/architecture/backend-catalog.json", "docs/architecture/frontend-catalog.json",
}


class Blocked(Exception):
    """Evidence is missing, inconsistent, or cannot be authenticated."""


class AuthorityUnavailable(Blocked):
    """A live authority could not be queried; selection must stop entirely."""


class ClosedUnmergedPR(Blocked):
    """A rejected/abandoned PR cannot remain an open completion claim."""


def require(condition, message):
    if not condition:
        raise Blocked(message)


def run(argv, cwd):
    try:
        result = subprocess.run(argv, cwd=cwd, capture_output=True, check=True, timeout=45)
        return result.stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        # Do not echo URLs, credentials, or tool stderr into operational state.
        raise Blocked(f"Command unavailable or failed: {argv[0]} {argv[1]}") from exc


def safe_path(value):
    require(isinstance(value, str) and value and ":" not in value and "\\" not in value,
            "Evidence path must be a relative repository path")
    p = PurePosixPath(value)
    require(not p.is_absolute() and ".." not in p.parts and str(p) == value,
            "Evidence path must be normalized and inside the repository")
    return value


def decode(raw, label):
    try:
        return json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise Blocked(f"Invalid JSON: {label}") from exc


def plan_digest(raw, artifact):
    normalization = artifact.get("normalization")
    if normalization == "chunk-plan-v1":
        require(artifact.get("path") == "docs/planning/chunks.json", "Chunk normalization is restricted to the chunk registry")
        chunks = validate_plan(decode(raw, "chunk plan witness"))
        content = [{k: v for k, v in c.items() if k not in {"status", "execution", "blockers"}} for c in chunks]
        raw = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    elif normalization == "scope-document-v1":
        require(artifact.get("path") == "docs/product/SCOPE_LOCK.md", "Scope normalization is restricted to the scope document")
        for key in (b"STATUS", b"APPROVAL_EVIDENCE"):
            pattern = rb"^" + key + rb":[^\r\n]*(?:\r?\n|$)"
            require(len(re.findall(pattern, raw, flags=re.MULTILINE)) == 1,
                    "Scope document needs exactly one status and approval-evidence line")
            raw = re.sub(pattern, b"", raw, flags=re.MULTILINE)
    elif normalization == "chunk-manifest-v1":
        path = artifact.get("path", "")
        require(re.fullmatch(r"docs/planning/chunks/ZE-P\d{2}-C\d{2}\.md", path),
                "Chunk manifest normalization is restricted to canonical chunk Markdown")
        match = re.match(rb"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", raw, flags=re.DOTALL)
        require(match is not None, "Chunk manifest needs JSON frontmatter")
        metadata = decode(match.group(1), path)
        require(isinstance(metadata, dict) and metadata.get("id") == PurePosixPath(path).stem,
                "Chunk manifest frontmatter identity mismatch")
        content = {k: v for k, v in metadata.items() if k not in {"status", "execution", "blockers"}}
        raw = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n---\n" + raw[match.end():]
    else:
        require(normalization is None, "Unsupported scope witness normalization")
    return hashlib.sha256(raw).hexdigest()


def witness_normalization(path):
    if path == "docs/planning/chunks.json":
        return "chunk-plan-v1"
    if path == "docs/product/SCOPE_LOCK.md":
        return "scope-document-v1"
    if re.fullmatch(r"docs/planning/chunks/ZE-P\d{2}-C\d{2}\.md", path):
        return "chunk-manifest-v1"
    return None


def mandatory_witnesses(repo, revision=None):
    """Required authority paths. None reads the working tree for generation/validation only."""
    if revision is None:
        files = {str(p.relative_to(repo.root)) for p in (repo.root / "docs").rglob("*") if p.is_file()}
        chunks = decode((repo.root / "docs/planning/chunks.json").read_bytes(), "chunk registry")
    else:
        files = set(repo.git("ls-tree", "-r", "--name-only", revision).splitlines())
        chunks = repo.json(revision, "docs/planning/chunks.json")
    required = set(CORE_AUTHORITIES)
    for path in files:
        p = PurePosixPath(path)
        if (p.parent == PurePosixPath("docs/product") and p.suffix == ".md"
                or path.startswith("docs/architecture/") and p.suffix in {".md", ".json"}
                or re.fullmatch(r"docs/planning/chunks/ZE-P\d{2}-C\d{2}\.md", path)):
            required.add(path)
    required.update(f"docs/planning/chunks/{chunk['id']}.md" for chunk in validate_plan(chunks))
    require(required <= files, "Required authoritative files are missing: " + ", ".join(sorted(required - files)))
    return required


class Repository:
    def __init__(self, root):
        self.root = Path(root).resolve()

    def git(self, *args):
        return run(["git", *args], self.root).decode().strip()

    def read(self, revision, path):
        return run(["git", "show", f"{revision}:{safe_path(path)}"], self.root)

    def json(self, revision, path):
        return decode(self.read(revision, path), path)

    def ancestor(self, older, newer):
        require(SHA.fullmatch(older or "") is not None, "Invalid merge commit identifier")
        result = subprocess.run(["git", "merge-base", "--is-ancestor", older, newer],
                                cwd=self.root, capture_output=True, timeout=45)
        return result.returncode == 0

    def synchronize_check(self):
        require(self.git("rev-parse", "--show-toplevel") == str(self.root), "Run at the repository root")
        require(self.git("branch", "--show-current") == "master", "Checkout synchronized master before reconciliation")
        require(not self.git("status", "--porcelain", "--untracked-files=all"), "Working tree must be clean")
        require(not self.git("ls-files", "--others", "--exclude-standard"), "Untracked files prevent reconciliation")
        head = self.git("rev-parse", "HEAD")
        config = self.json(head, "memory/repository.json")
        require(config.get("schema_version") == 1 and config.get("default_branch") == "master",
                "Repository identity configuration is unsupported")
        expected = config.get("expected_origin")
        slug = config.get("github_repository")
        require(isinstance(expected, str) and expected.strip(), "Expected origin is not configured; human repository setup required")
        require(isinstance(slug, str) and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", slug),
                "Expected GitHub repository is not configured")
        require(self.git("remote", "get-url", "origin") == expected, "origin does not match the approved repository identity")
        require(self.git("rev-parse", "refs/heads/master") == head, "Local master does not match HEAD")
        require(self.git("rev-parse", "refs/remotes/origin/master") == head,
                "Local master differs from origin/master; synchronize without destructive repair")
        self.assert_remote_tip(head)
        return head, config

    def assert_remote_tip(self, head):
        advertised = self.git("ls-remote", "--exit-code", "origin", "refs/heads/master").split()
        require(len(advertised) == 2 and advertised[1] == "refs/heads/master" and advertised[0] == head,
                "origin/master is stale; fetch and fast-forward, then reconcile again")


class GitHub:
    """Fresh GitHub TLS reads; prefer gh auth, otherwise token/public standard-library REST."""
    def __init__(self, root, slug):
        self.root, self.slug = root, slug
        self._trees = {}
        self._use_gh = False
        if shutil.which("gh"):
            try:
                run(["gh", "auth", "status", "--hostname", "github.com"], root)
                self._use_gh = True
            except Blocked:
                pass
        self._token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    def _request(self, suffix, raw=False):
        accept = "application/vnd.github.raw+json" if raw else "application/vnd.github+json"
        if self._use_gh:
            try:
                return run(["gh", "api", "--hostname", "github.com", "-H", f"Accept: {accept}",
                            "-H", "Cache-Control: no-cache", f"repos/{self.slug}/{suffix}"], self.root)
            except Blocked as exc:
                raise AuthorityUnavailable("Fresh GitHub query failed; resolve credentials/network/rate limit before selection") from exc
        headers = {"Accept": accept, "Cache-Control": "no-cache", "User-Agent": "ZunoEduPlanReconciler/1",
                   "X-GitHub-Api-Version": "2022-11-28"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        request = Request(f"https://api.github.com/repos/{self.slug}/{suffix}", headers=headers)
        try:
            with urlopen(request, timeout=45) as response:
                return response.read()
        except HTTPError as exc:
            raise AuthorityUnavailable(f"Fresh GitHub query returned HTTP {exc.code}; check access, repository identity and rate limits") from None
        except (URLError, OSError, TimeoutError):
            raise AuthorityUnavailable("Fresh GitHub HTTPS query failed; check network and retry") from None

    def api(self, suffix, paginate=False):
        if not paginate:
            return decode(self._request(suffix), "live GitHub response")
        values = []
        for page in range(1, 1001):
            connector = "&" if "?" in suffix else "?"
            data = decode(self._request(f"{suffix}{connector}page={page}"), "live GitHub response")
            require(isinstance(data, list), "Invalid paginated GitHub response")
            values.extend(data)
            if len(data) < 100:
                return values
        raise AuthorityUnavailable("GitHub pagination limit exceeded; selection stopped")

    def pr(self, number):
        require(type(number) is int and number > 0, "PR number must be a positive integer")
        return self.api(f"pulls/{number}")

    def files(self, number):
        items = self.api(f"pulls/{number}/files?per_page=100", paginate=True)
        require(len(items) < 3000, "PR file listing may be truncated; split/review evidence manually")
        return {item["filename"] for item in items}

    def open_prs(self):
        return self.api("pulls?state=open&base=master&per_page=100", paginate=True)

    def closed_prs(self):
        return self.api("pulls?state=closed&base=master&per_page=100", paginate=True)

    def file_at(self, revision, path):
        require(SHA.fullmatch(revision or "") is not None, "Invalid PR head identifier")
        return self._request(f"contents/{quote(safe_path(path), safe='/')}?ref={revision}", raw=True)

    def verify_plan_artifact(self, revision, artifact, merge_raw):
        require(SHA.fullmatch(revision or "") is not None, "Invalid PR head identifier")
        path = safe_path(artifact["path"])
        if revision not in self._trees:
            response = self.api(f"git/trees/{revision}?recursive=1")
            require(response.get("truncated") is False, "GitHub PR-head tree is truncated; cannot verify scope")
            self._trees[revision] = {item["path"]: item for item in response.get("tree", [])}
        entry = self._trees[revision].get(path, {})
        require(entry.get("type") == "blob" and entry.get("mode") in {"100644", "100755"},
                "Plan artifact is absent or not a regular file in PR head")
        blob = hashlib.sha1(f"blob {len(merge_raw)}\0".encode() + merge_raw).hexdigest()
        if entry.get("sha") == blob:
            return
        if artifact.get("normalization"):
            require(plan_digest(self.file_at(revision, path), artifact) == artifact["sha256"],
                    "Plan artifact differs from human-merged PR head")
            return
        raise Blocked("Plan artifact differs from human-merged PR head tree")


def validate_plan(chunks):
    require(isinstance(chunks, list) and chunks, "Chunk registry must be a nonempty list")
    ids, sequence = set(), set()
    for item in chunks:
        require(isinstance(item, dict), "Each chunk must be an object")
        cid = item.get("id")
        require(isinstance(cid, str) and re.fullmatch(r"ZE-P\d{2}-C\d{2}", cid), "Invalid chunk identifier")
        require(cid not in ids, f"Duplicate chunk: {cid}")
        ids.add(cid)
        rank = item.get("sequence")
        require(type(rank) is int and rank > 0 and rank not in sequence, f"Invalid/duplicate sequence: {cid}")
        sequence.add(rank)
        require(item.get("status") in STATES, f"Invalid status: {cid}")
        for key in ("dependencies", "requirements", "required_context", "required_skills", "optional_skills"):
            values = item.get(key)
            require(isinstance(values, list) and all(isinstance(v, str) and v for v in values), f"Invalid {key}: {cid}")
            require(len(values) == len(set(values)), f"Duplicate {key}: {cid}")
        require(item["requirements"] and item["required_context"] and item["required_skills"], f"Missing bounded context: {cid}")
        require(isinstance(item.get("execution"), dict), f"Missing execution metadata: {cid}")
    graph = {item["id"]: item["dependencies"] for item in chunks}
    for cid, deps in graph.items():
        require(cid not in deps and all(d in ids for d in deps), f"Invalid dependency: {cid}")
    visiting, seen = set(), set()
    def visit(cid):
        require(cid not in visiting, f"Dependency cycle at {cid}")
        if cid in seen:
            return
        visiting.add(cid)
        for dep in graph[cid]:
            visit(dep)
        visiting.remove(cid)
        seen.add(cid)
    for cid in graph:
        visit(cid)
    return sorted(chunks, key=lambda item: (item["sequence"], item["id"]))


def merged_pr(repo, github, number, head):
    pr = github.pr(number)
    if pr.get("state") == "closed" and pr.get("merged") is not True:
        raise ClosedUnmergedPR(f"PR #{number} was closed without merge; resolve before retrying its chunk")
    require(pr.get("merged") is True and pr.get("merged_at"), f"PR #{number} is not merged")
    require(pr.get("base", {}).get("ref") == "master", f"PR #{number} targets another branch")
    require(pr.get("base", {}).get("repo", {}).get("full_name", "").lower() == github.slug.lower(),
            f"PR #{number} belongs to another repository")
    merge = pr.get("merge_commit_sha")
    require(repo.ancestor(merge, head), f"PR #{number} merge is absent from current master")
    return pr, merge


def scope_status(repo, github, head, lock):
    require(lock.get("schema_version") == 1 and lock.get("status") in {"DRAFT", "LOCKED"}, "Invalid scope-lock schema")
    number = lock.get("planning_pr")
    if number is None:
        return "DRAFT", "Planning PR evidence is not configured"
    try:
        pr, merge = merged_pr(repo, github, number, head)
        require(pr.get("merged_by", {}).get("type") == "User", "Planning scope must be merged by a human")
        artifacts = lock.get("plan_artifacts")
        require(isinstance(artifacts, list) and artifacts, "Scope approval has no immutable plan artifact witnesses")
        required = mandatory_witnesses(repo, merge) | mandatory_witnesses(repo, head)
        witnessed = {item.get("path") for item in artifacts}
        require(required <= witnessed, "Scope approval omits mandatory witnesses: " + ", ".join(sorted(required - witnessed)))
        paths = set()
        for artifact in artifacts:
            path = safe_path(artifact.get("path"))
            require(path not in paths and path != "docs/product/scope-lock.json", "Duplicate/self-referential plan witness")
            paths.add(path)
            require(artifact.get("normalization") == witness_normalization(path), "Incorrect authority witness normalization")
            expected = artifact.get("sha256")
            require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected), "Invalid plan artifact digest")
            merge_raw = repo.read(merge, path)
            for raw in (merge_raw, repo.read(head, path)):
                require(plan_digest(raw, artifact) == expected, "Plan artifact differs from human-merged scope")
            github.verify_plan_artifact(pr.get("head", {}).get("sha"), artifact, merge_raw)
        merged_lock = repo.json(merge, "docs/product/scope-lock.json")
        for key in ("scope_version", "architecture_version", "plan_artifacts", "planning_pr"):
            require(merged_lock.get(key) == lock.get(key), "Scope evidence changed outside the approved planning PR")
        return "LOCKED", None
    except AuthorityUnavailable:
        raise
    except Blocked as exc:
        return "DRAFT", str(exc)


def completion(repo, github, head, chunk):
    cid, execution = chunk["id"], chunk["execution"]
    number, path = execution.get("pr"), execution.get("completion_evidence")
    require(number is not None and path == f"memory/completions/{cid}.json", "Missing completion PR or canonical evidence path")
    pr, merge = merged_pr(repo, github, number, head)
    require(pr.get("merged_by", {}).get("type") == "User", "Implementation completion requires human merge")
    require(f"ZUNO_EDU_CHUNK:{cid}" in (pr.get("body") or "").splitlines(), "Merged PR lacks the exact chunk marker")
    changed = github.files(number)
    require(path in changed, "Completion evidence was not delivered by this PR")
    raw = repo.read(head, path)
    require(raw == repo.read(merge, path), "Completion evidence differs from the verified merge tree")
    evidence = decode(raw, path)
    require(evidence.get("schema_version") == 1 and evidence.get("chunk_id") == cid, "Completion evidence identity mismatch")
    require(sorted(evidence.get("requirements", [])) == sorted(chunk["requirements"]), "Completion evidence omits/adds chunk requirements")
    artifacts = evidence.get("artifacts")
    require(isinstance(artifacts, list) and artifacts, "Completion evidence needs artifact witnesses")
    paths = set()
    for artifact in artifacts:
        p = safe_path(artifact.get("path"))
        require(p != path and p not in paths, "Duplicate/self-referential artifact witness")
        paths.add(p)
        expected = artifact.get("sha256")
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected), "Invalid artifact digest")
        require(hashlib.sha256(repo.read(merge, p)).hexdigest() == expected, "Artifact digest does not match verified merge tree")
        repo.read(head, p)  # Current master must retain the artifact; later edits are allowed.
    require(paths & changed, "No witnessed implementation artifact was changed by the verified PR")
    checks = evidence.get("verification")
    require(isinstance(checks, list) and checks, "Verification evidence is missing")
    review = evidence.get("review", {})
    require(review.get("critical") == 0 and review.get("high") == 0, "Unresolved Critical/High review findings")
    if chunk.get("workflow"):
        rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        depth = {"lightweight": 0, "focused": 1, "deep": 2}
        risk = chunk["workflow"]["review_risk"]
        require(review.get("risk") in rank and rank[review["risk"]] >= rank[risk], "Review risk is below chunk floor")
        required_depth = min(rank[review["risk"]], 2)
        require(depth.get(review.get("depth"), -1) >= required_depth, "Review depth is insufficient")
        if required_depth == 2:
            require(review.get("independent") is True, "Sensitive chunk requires independent deep review")
    for record in [*checks, {"result": "PASS", "evidence": review.get("evidence")}]:
        require(record.get("result") == "PASS", "Verification did not pass")
        p = safe_path(record.get("evidence"))
        require(p in paths, "Verification/review record must have a hashed artifact witness")
    return {"pr": number, "merge_commit": merge, "evidence": path}


def open_chunk_claims(github, chunks):
    """Discover feature-only handoffs that unmerged master cannot contain."""
    known = {chunk["id"] for chunk in chunks}
    claims = {}
    for pr in github.open_prs():
        if pr.get("state") != "open" or pr.get("base", {}).get("ref") != "master":
            continue
        if pr.get("base", {}).get("repo", {}).get("full_name", "").lower() != github.slug.lower():
            continue
        if pr.get("head", {}).get("repo", {}).get("full_name", "").lower() != github.slug.lower():
            continue
        markers = [line.removeprefix("ZUNO_EDU_CHUNK:") for line in (pr.get("body") or "").splitlines()
                   if re.fullmatch(r"ZUNO_EDU_CHUNK:ZE-P\d{2}-C\d{2}", line)]
        for cid in set(markers) & known:
            branch = pr.get("head", {}).get("ref", "")
            expected = rf"feature/{cid.lower()}-[a-z0-9]+(?:-[a-z0-9]+)*"
            valid = (len(markers) == 1 and re.fullmatch(expected, branch) is not None
                     and type(pr.get("number")) is int and pr["number"] > 0)
            claims.setdefault(cid, []).append({"pr": pr.get("number"), "branch": branch, "valid": valid})
    return claims


def closed_chunk_claims(github, chunks):
    """Find abandoned same-repository chunk PRs without loading their diffs/history."""
    known = {chunk["id"] for chunk in chunks}
    claims = {}
    for pr in github.closed_prs():
        if pr.get("state") != "closed" or pr.get("merged") is True or pr.get("merged_at"):
            continue
        if pr.get("base", {}).get("ref") != "master":
            continue
        if any(pr.get(side, {}).get("repo", {}).get("full_name", "").lower() != github.slug.lower()
               for side in ("base", "head")):
            continue
        for line in (pr.get("body") or "").splitlines():
            if not re.fullmatch(r"ZUNO_EDU_CHUNK:ZE-P\d{2}-C\d{2}", line):
                continue
            cid = line.removeprefix("ZUNO_EDU_CHUNK:")
            if cid in known and re.fullmatch(rf"feature/{cid.lower()}-[a-z0-9]+(?:-[a-z0-9]+)*", pr.get("head", {}).get("ref", "")):
                claims.setdefault(cid, []).append(pr["number"])
    return claims


def reconcile(repo, github=None):
    head, config = repo.synchronize_check()
    chunks = validate_plan(repo.json(head, "docs/planning/chunks.json"))
    # Read cache for diagnostic visibility only; never use its selections/completions.
    progress = repo.json(head, "memory/progress.json")
    require(progress.get("schema_version") == 1, "Unsupported progress cache schema")
    github = github or GitHub(repo.root, config["github_repository"])
    lock = repo.json(head, "docs/product/scope-lock.json")
    effective_scope, scope_blocker = scope_status(repo, github, head, lock)
    result = {"schema_version": 1, "master_sha": head, "scope_status": effective_scope,
              "scope_blocker": scope_blocker, "effective_states": {}, "completed_chunks": [],
              "unresolved_prs": [], "blocked_chunks": [], "completion_evidence": {},
              "next_candidate_chunk": None, "warnings": []}
    open_claims = open_chunk_claims(github, chunks) if effective_scope == "LOCKED" else {}
    closed_claims = closed_chunk_claims(github, chunks) if effective_scope == "LOCKED" else {}
    result["open_prs"] = {cid: [claim["pr"] for claim in claims] for cid, claims in sorted(open_claims.items())}
    for chunk in chunks:
        cid, status = chunk["id"], chunk["status"]
        if cid in open_claims and (len(open_claims[cid]) != 1 or not open_claims[cid][0]["valid"]):
            result["effective_states"][cid] = "BLOCKED"
            result["blocked_chunks"].append(cid)
            result["warnings"].append(f"{cid}: duplicate or inconsistent open chunk PR claims require human resolution")
            continue
        if status in {"PR_OPEN", "COMPLETE"} or chunk["execution"].get("pr") is not None:
            try:
                result["completion_evidence"][cid] = completion(repo, github, head, chunk)
                result["completed_chunks"].append(cid)
                result["effective_states"][cid] = "COMPLETE"
                continue
            except AuthorityUnavailable:
                raise
            except ClosedUnmergedPR as exc:
                result["effective_states"][cid] = "BLOCKED"
                result["blocked_chunks"].append(cid)
                result["warnings"].append(f"{cid}: {exc}")
                continue
            except Blocked as exc:
                result["warnings"].append(f"{cid}: {exc}")
                if status == "COMPLETE":
                    result["effective_states"][cid] = "BLOCKED"
                    result["blocked_chunks"].append(cid)
                    continue
                result["unresolved_prs"].append(cid)
                result["effective_states"][cid] = "PR_OPEN"
                continue
        if cid in open_claims:
            result["effective_states"][cid] = "PR_OPEN"
            result["unresolved_prs"].append(cid)
            continue
        if cid in closed_claims:
            result["effective_states"][cid] = "BLOCKED"
            result["blocked_chunks"].append(cid)
            result["warnings"].append(f"{cid}: PRs {closed_claims[cid]} closed without merge; obtain explicit retry/disposition before resuming")
            continue
        if status in {"BLOCKED", "IN_PROGRESS"} or chunk.get("blockers"):
            result["effective_states"][cid] = "BLOCKED" if chunk.get("blockers") else status
            if result["effective_states"][cid] == "BLOCKED":
                result["blocked_chunks"].append(cid)
    complete = set(result["completed_chunks"])
    # A forged completion cannot manufacture dependency satisfaction.
    for chunk in chunks:
        cid = chunk["id"]
        if cid in complete and not set(chunk["dependencies"]) <= complete:
            raise Blocked(f"Completed chunk has unverified dependencies: {cid}")
    for chunk in chunks:
        cid = chunk["id"]
        if cid in result["effective_states"]:
            continue
        ready = (effective_scope == "LOCKED" and not chunk.get("blockers")
                 and set(chunk["dependencies"]) <= complete)
        result["effective_states"][cid] = "READY" if ready else "PLANNED"
        if ready and result["next_candidate_chunk"] is None:
            result["next_candidate_chunk"] = cid
    # Catch a remote merge during API/evidence inspection. Restart on a new tip.
    if progress.get("master_sha_at_last_reconciliation") not in (None, head):
        result["warnings"].append("Progress cache uses an older master; persist recomputed state only on the next feature branch")
    if progress.get("next_candidate_chunk") not in (None, result["next_candidate_chunk"]):
        result["warnings"].append("Cached next candidate is stale and was ignored")
    repo.assert_remote_tip(head)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--validate-plan", action="store_true", help="Offline schema/graph check only; never authorizes execution")
    args = parser.parse_args()
    try:
        if args.validate_plan:
            path = args.repo / "docs/planning/chunks.json"
            chunks = validate_plan(decode(path.read_bytes(), str(path)))
            print(json.dumps({"validation": "PASS", "chunks": len(chunks), "execution_authorized": False}, indent=2))
        else:
            print(json.dumps(reconcile(Repository(args.repo)), indent=2, sort_keys=True))
    except (Blocked, OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc), "next_candidate_chunk": None}, indent=2))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
