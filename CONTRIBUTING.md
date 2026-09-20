# Contributing to Zuno Edu

Start with [AGENTS.md](AGENTS.md). The launch baseline must be approved and merged
before product implementation. This bootstrap contains no business feature code.

Use Python 3.11+ and Git for bootstrap validation:

```sh
python3 scripts/validate_plan.py
python3 scripts/reconcile_state.py --validate-plan
python3 scripts/next_chunk.py --validate
python3 -m unittest discover -s tests/workflow -v
```

These offline checks validate the plan and workflow implementation. They do not prove
a remote merge or authorize a product chunk. Online reconciliation prefers an
authenticated `gh` CLI, then uses Python's standard-library HTTPS client with an
existing `GH_TOKEN`/`GITHUB_TOKEN` or public GitHub access. Private repositories require
read credentials; public queries need no installation or token but have lower rate
limits. Network/access/rate-limit failures stop selection. The script never logs
tokens or uses a caller-provided evidence cache.

Repository setup requires a real, human-provided GitHub origin and repository slug in
`memory/repository.json`. Until configured, synchronization, push, PR creation and
scope approval remain blocked. Never manufacture a remote URL or master SHA.

Use `master` as the default branch and human remote merges as the normal merge path.
Synchronize with `git fetch origin`, `git checkout master`, and
`git pull --ff-only origin master`; reconcile without modifying master. Create a fresh
feature branch for one eligible chunk. Do not build on an unmerged dependency.

Branches: `feature/<chunk-id-lowercase>-<slug>`. Bootstrap branch:
`feature/project-bootstrap-planning`. Commit subjects use
`feat(ZE-PXX-CXX): ...`, `fix(...)`, `test(...)` or `docs(...)` as appropriate.

Every implementation PR must include the exact full-line marker
`ZUNO_EDU_CHUNK:<CHUNK-ID>`, the completed [PR template](.github/pull_request_template.md),
required validation and risk-based review with zero unresolved Critical/High findings. High/critical work requires independent deep review.
Record its number and immutable completion evidence on the feature branch after PR
creation. A merged PR can retain `PR_OPEN` in files; reconciliation recognizes the
actual merge and persists corrections in the next feature branch.

Use the [scope-change process](docs/planning/SCOPE_CHANGE_PROCESS.md) for an explicit
human change to locked scope. Do not reinterpret hard requirements as optional.
The PR author hands off; the human reviews and merges into master if approved.

Normal entry point: start a fresh Codex context and say `next chunk`. AGENTS routes remote synchronization, existing evidence reconciliation and one bounded context packet. Detailed policy is lazy-loaded from docs/planning/AGENT_WORKFLOW.md; historical handoffs are not startup context.
