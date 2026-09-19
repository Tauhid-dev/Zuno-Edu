# Bootstrap handoff

Repository: Tauhid-dev/Zuno-Edu. Base master: 9f926298f105cb6736ba16f4b0d3f2b94941daea, the human-authorized one-time empty baseline. All planning content is on feature/project-bootstrap-planning. Application implementation has not started.

Planning is complete: 219 launch requirements, 12 phases, 62 PLANNED chunks, 100% planned coverage. All independent planning reviews passed with zero unresolved Critical/High/Medium findings. All 37 workflow tests passed; full validation includes 111 authority witnesses. See docs/planning/INDEPENDENT_REVIEW.md and BOOTSTRAP_VALIDATION.md.

The actual planning PR number is recorded in docs/product/scope-lock.json and memory/progress.json after creation. Scope remains DRAFT. The human reviews scope, architecture, object model, frontend/backend mappings and chunk plan, then merges remotely only if approved. Production human gates remain separate launch prerequisites.

After that merge, a fresh `next chunk` follows AGENTS.md: synchronize master, run read-only reconciliation, obtain effective LOCKED plus the deterministic candidate, load only that manifest/context/skills and create one feature branch. The initial candidate is ZE-P01-C01 only if fresh evidence confirms readiness. Never treat this cache or conversation as completion or approval evidence. Stop after the next chunk PR handoff; no automatic merge.

## Current publication blocker

The validated feature branch is pushed to origin. The GitHub connector returned HTTP 403 (Resource not accessible by integration) for PR creation. The in-app GitHub browser is signed out; a usable authenticated CLI session is absent. The user has been asked to sign in so the agent can finish creating the already-authorized PR. Prepared title/body/base/head are in docs/planning/BOOTSTRAP_PR_DESCRIPTION.md. No PR exists yet; do not invent its number or mark the scope approved.

Once authenticated, create exactly one PR against master, attach its URL to this Codex task, record its actual number in scope-lock.json and memory/progress.json on this feature branch, commit/push that metadata and inspect the final GitHub checks. All planning reviews are already complete; do not restart design or implement a product chunk.
