# Authoritative state reconciliation

## Authority and lifecycle

Freshly synchronized `origin/master` and its history are execution authority. Verified
completion evidence outranks declared chunk status; the chunk manifest outranks
`memory/progress.json`; all of these outrank prior chat context. Progress is a routing
cache, never a source of completion or eligibility.

| State | Meaning |
|---|---|
| PLANNED | Defined; execution gate/dependencies not yet satisfied |
| READY | Locked scope, all dependencies effectively complete, no blocker |
| BLOCKED | A documented blocker or unsupported completion claim requires resolution |
| IN_PROGRESS | Claimed active implementation; never silently execute it again |
| PR_OPEN | Awaiting proof of remote merge; push and open PR are insufficient |
| COMPLETE | Fresh master contains verified merged implementation evidence |

The registry is `docs/planning/chunks.json`: a JSON list of objects with unique `id`
and positive integer `sequence`, `status`, `dependencies`, nonempty `requirements`,
nonempty `required_context`, nonempty `required_skills`, `optional_skills`, and an
`execution` object. Execution fields are `base_master_sha`, `branch`, `commit`, `pr`
(positive GitHub PR number or null), and `completion_evidence` (canonical path or null).
Optional `blockers` is an array of current operational blockers. Keep Markdown chunk
frontmatter consistent with this machine-readable index; neither can override proof.

Readiness is recomputed from dependencies, not a stale READY flag. Select the first
eligible chunk ordered by `(sequence, id)`. Sequence numbers are unique; ID supplies
a stable defensive tie-break. Cycles, unknown dependencies and duplicate identities
are fatal validation errors. An unmerged PR blocks its descendants; another independent
eligible chunk can be selected. An IN_PROGRESS chunk is not eligible for duplicate work.

Master cannot contain the execution metadata of an unmerged feature PR. Therefore
reconciliation also discovers live open PRs against this repository's master. An
exact full-line `ZUNO_EDU_CHUNK:<ID>` and a same-repository head branch named
`feature/<id-lowercase>-<slug>` reserve that chunk as effective PR_OPEN without any
master edit. Duplicate or inconsistent claims block the chunk for human resolution.
Fork PRs cannot reserve internal work. Independent ready chunks remain eligible.

## Synchronization without master edits

Before any selection, verify the configured repository identity and clean working tree, then run:

```sh
git fetch origin
git checkout master
git pull --ff-only origin master
python3 scripts/reconcile_state.py
```

The reconciler **does not synchronize or mutate anything**. It checks repository root,
current branch, tracked/untracked cleanliness, configured repository origin, local master,
HEAD and `origin/master` equality, then uses read-only `git ls-remote` to compare the
server-advertised master SHA. It repeats the remote-tip check after API/evidence reads
to detect a merge during inspection. GitHub evidence comes from fresh official
GitHub HTTPS calls with cache disabled. Prefer an authenticated `gh` CLI. When it is
absent or not authenticated, Python's standard-library HTTPS client uses an existing
`GH_TOKEN`/`GITHUB_TOKEN`, or the public endpoint without a token. Private repositories
need read credentials. HTTP 403/404/rate limits and network failures stop selection;
tokens and provider error bodies are never logged. No provider SDK is required.

Repository identity in `memory/repository.json`:

```json
{
  "schema_version": 1,
  "expected_origin": null,
  "github_repository": null,
  "default_branch": "master"
}
```

The nulls deliberately mean unconfigured. A human must supply the actual origin URL
and `owner/repository`; never infer them from a project label. A setup branch can then
record this identity and be reviewed. A local bootstrap SHA is not a remote master SHA.
Origin validation accepts the exact approved `expected_origin` for compatibility,
plus `git@github.com:<owner/repository>.git`,
`https://github.com/<owner/repository>.git` and the same HTTPS URL without `.git`,
derived from `github_repository`. Arbitrary hosts, aliases and forks are not accepted
as equivalent origins. Repository roots are compared as resolved `pathlib.Path`
objects so native path separators do not require machine-specific configuration.
The actual approved repository identity is recorded in the repository file; these
nulls illustrate unconfigured setup only. Online scope approval remains blocked until
the real planning PR is published and human-merged.

Any failed sync, dirty/diverged checkout, identity mismatch, stale tip, missing evidence
or malformed input prevents unauthorized execution. Do not reset, force-push, discard
files or manufacture cached evidence to work around a failure. The script emits a JSON
BLOCKED result and exits 2 for a hard precondition failure. A valid reconciliation can
exit 0 with DRAFT scope or no candidate; **only LOCKED plus a non-null candidate permits
execution**. The offline `--validate-plan` option never authorizes execution.

Create the selected feature branch from the returned synchronized master SHA. Persist
any status/cache corrections there. Never write a report into the working tree while
on master; inspect stdout or use a temporary file outside the repository. If the remote
changes before branching, resynchronize and rerun. Never derive state from an old report.

## Planning approval and DRAFT → effective LOCKED

`docs/product/scope-lock.json` has this structure:

```json
{
  "schema_version": 1,
  "status": "DRAFT",
  "scope_version": "1.0",
  "architecture_version": 1,
  "planning_pr": null,
  "plan_artifacts": [
    {"path": "docs/product/LAUNCH_SCOPE.md", "sha256": "<64 lowercase hex characters>"},
    {"path": "docs/planning/chunks.json", "normalization": "chunk-plan-v1", "sha256": "<64 lowercase hex characters>"}
  ]
}
```

Before human review, populate planning_pr with the actual PR number and capture all
immutable authoritative product, requirement, architecture, contract and planning
artifacts in `plan_artifacts`. Commit this metadata on the planning feature branch.
The witness list is not optional or self-selecting: `mandatory_witnesses(repo, revision)`
requires the fixed core authority files, every product Markdown file and requirement
inventory, every architecture Markdown/JSON file including ADRs, chunks.json and every
chunk Markdown file named in that registry. The reconciler checks the union of required
paths on the approved merge and fresh master, so omitting, adding or deleting an
authority cannot leave it unprotected. Missing files/witnesses prevent LOCKED. The
same helper accepts revision=None for the generator and validator's working-tree check.
Do not include the lock file itself or mutable memory. The plan's PR cannot store its
own final commit hash without a self-reference; the fresh authoritative PR head SHA supplies
that exact identity at reconciliation.

The human's merge of the identified planning PR is the approval event requested by
the development contract. No extra approval comment or marker is required. The live
PR must be merged into this repository's master, `merged_by.type` must be `User`, and
its merge commit must be reachable from fresh master. Every plan witness must match
the exact live PR head tree, merge tree and current master. One recursive Git tree
query proves PR-head file blob IDs against their witnessed merge bytes; a truncated
tree blocks. Even normalized witnesses need no per-file content call when those raw
blob IDs agree. Only a normalized head/merge byte difference triggers a content query.
This avoids one API request per document under public rate limits. Scope version, architecture
version, PR number and witness list must match the merged lock record. Repository
protection and human ownership of merge credentials remain necessary operational
controls; account type alone cannot prove who physically operated an account.

`chunk-plan-v1` is supported only for `docs/planning/chunks.json`. Parse and validate
the list, sort by `(sequence,id)`, remove only `status`, `execution`, `blockers` from
each object, serialize with UTF-8, sorted keys, separators `(',', ':')`, and
`ensure_ascii=False`, then SHA-256.

`chunk-manifest-v1` is restricted to canonical chunk Markdown paths. Its frontmatter
must be JSON between `---` delimiter lines and identify the matching chunk. Remove
only status/execution/blockers, canonicalize the remaining JSON with the same settings,
append `\n---\n` and the unchanged Markdown body, then hash. All acceptance/design
text and required context/skill metadata stay protected while execution state changes.

`scope-document-v1` is restricted to SCOPE_LOCK.md. Remove exactly one full STATUS
line and one full APPROVAL_EVIDENCE line, leaving every other byte unchanged, then
hash. Scope/architecture versions and the complete authority/process text remain
protected. `witness_normalization(path)` supplies the required normalization; assigning
another normalization or omitting the required one blocks approval. Other witnesses
hash raw bytes. These rules permit state persistence without scope erosion.

Thus DRAFT committed in the planning PR becomes **effective LOCKED** after human
merge without editing master. The first implementation branch persists LOCKED in
human-readable/machine-readable state and updates caches. A self-reported LOCKED flag
without verified approval evidence grants no authority. Changed plan witnesses require
the scope/architecture-change process and a newly approved evidence record.

## Implementation completion evidence

The PR body must contain a full line `ZUNO_EDU_CHUNK:ZE-PXX-CXX`. After deterministic validation and
risk-based review, create `memory/completions/ZE-PXX-CXX.json` on the feature branch:

```json
{
  "schema_version": 1,
  "chunk_id": "ZE-P01-C01",
  "requirements": ["<exact IDs from the chunk>"],
  "artifacts": [
    {"path": "<implemented file>", "sha256": "<sha256 of file bytes>"},
    {"path": "memory/handoffs/ZE-P01-C01-review.md", "sha256": "<sha256 of report bytes>"}
  ],
  "verification": [
    {"name": "<required check>", "result": "PASS", "evidence": "memory/handoffs/ZE-P01-C01-review.md"}
  ],
  "review": {"risk": "medium", "depth": "focused", "independent": false, "critical": 0, "high": 0, "evidence": "memory/handoffs/ZE-P01-C01-review.md"}
}
```

Include meaningful implementation, test and review witnesses; review reports identify
the reviewer, risk/depth/independence, findings/fixes, required checks and acceptance criteria. High/critical work requires an independent deep reviewer.
Reports are assertions until the human reviews and merges their PR. This script proves
provenance and inclusion, not semantic correctness; required CI, risk-appropriate review
and human review are separate acceptance controls.

Set status PR_OPEN and execution.completion_evidence before handoff. Open the PR, then
record its actual number in execution.pr via a follow-up feature commit. The final
review/checks must cover that final diff. Do not set COMPLETE before remote merge.

Completion requires all of the following:

1. Fresh authoritative GitHub HTTPS PR record: merged by a User account into this
   repository's master; merge commit reachable on fresh master. Bot merges do not
   establish normal human-approved completion. PR body has the exact chunk marker.
2. The canonical completion path was changed in this PR, as shown by GitHub's fully
   paginated changed-file list. A potentially truncated 3,000-file listing blocks.
3. The completion file is byte-identical between its verified merge tree and current
   master; identity and exact requirement set match the chunk.
4. Every artifact has a valid SHA-256 matching the verified merge tree. At least one
   witnessed artifact changed in the PR. Verification and risk-appropriate review evidence
   are themselves hashed artifacts, checks passed and Critical/High counts are zero.
5. The artifact still exists on fresh master. Later edits can extend it: the reachable
   historical merge plus immutable witness proves original completion. A deleted or
   renamed witnessed path blocks until an explicitly reviewed evidence/protocol change;
   do not silently discard a witness.

This works for ordinary, squash and rebase merges: it uses GitHub's merge commit and
tree witnesses, not feature-head ancestry or commit-message conventions. A PR_OPEN
manifest already merged into master becomes effective COMPLETE. An unmerged PR, a
forged COMPLETE/cache flag, a cherry-picked message containing a chunk ID, unrelated
merged PR, altered witness or wrong target branch does not establish completion.
Dependencies of a completed chunk must themselves have verified completion evidence.

No local JSON export of a PR, arbitrary third-party response, progress cache or
agent claim is accepted in place of a fresh query to the official TLS-protected
GitHub API. Public repository responses are authoritative without user authentication;
private repository responses need credentials. In-memory tree caching lasts only for
the current invocation and never bypasses the before/after remote-tip checks. The test
transport is injectable only through the Python API for isolated tests; the CLI has
no offline cache or trust-bypass switch.

## Verification baseline

`python3 -m unittest discover -s tests/workflow -v` creates temporary real repositories
and bare origins. It exercises fresh-tip/dirty/diverged/wrong-branch stops, DRAFT merge
lock, deterministic independent readiness, unmerged dependency blocking, squash/rebase
completion, ignored cache/message claims, forged status/evidence, changed scope and
read-only master behavior. Public HTTPS fallback, rate-limit failure without secret
disclosure, one-tree witness optimization and truncated-tree rejection are covered.
Additional cases cover unmerged feature-only metadata without any master change,
duplicate/inconsistent open PRs, missing authority witnesses, normalized state
persistence with immutable chunk-body protection, and bot implementation merges.
Live credentials are not needed for these isolated tests.
Before initial PR publication, also run `python3 scripts/validate_plan.py` and the
offline schema/graph check. Online authority remains unproven until real origin and
GitHub setup are supplied and successfully queried.

## Compact routing and handoff

AGENTS synchronizes first; next_chunk.py calls this same reconciler and emits only the selected routing packet. progress.json and CURRENT_HANDOFF.md are advisory caches, never approval/completion proof. Reconciliation ignores stale handoff claims, reports stale cache SHA/selection, and persists corrections only on a new feature branch. Historical memory/handoffs files are archive/evidence only.

Closed-without-merge PR claims are BLOCKED rather than PR_OPEN/COMPLETE. Completion review includes risk, depth and independent fields under AGENT_WORKFLOW.md#Review; the verifier enforces the chunk risk floor and independent deep review for high/critical risk. Local execution.stage milestones do not replace registry status or remote merge proof. Conditional next-model recommendations cannot authorize another chunk.

### Closed without merge

A closed, unmerged PR with the exact chunk marker blocks that chunk, not independent
ready work. A bare chunk ID is not a claim. Do not silently retry a rejected change.
The human may reopen the PR (restoring PR_OPEN), or explicitly authorize a fresh
attempt and replace its marker line with `ZUNO_EDU_ABANDONED:<ID>` plus the disposition
reason in that closed PR body. On the next synchronized run, the old claim no longer
reserves the chunk; fresh dependency/approval checks determine readiness. This is
not completion evidence and never overrides a merged artifact. If an execution PR
pointer was already committed on master, its stale pointer must also be corrected
in a separate reviewed workflow-repair PR before retry; no direct master edits.
