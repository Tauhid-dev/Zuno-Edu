# Zuno Edu operating constitution

This is the complete defined launch product, not an MVP. Bootstrap may create plans,
contracts as documentation, repository memory, skills and tooling; it must not implement
application features. During DRAFT, implement no product chunk.

## Authority

Apply, in order: approved SCOPE_LOCK/LAUNCH_SCOPE; functional and non-functional
requirements; accepted architecture decisions; CODE_BLUEPRINT; detailed architecture;
API/frontend contracts; active chunk; skills/standards; existing implementation;
conversational assumptions. Explicit human instructions to change scope invoke
[the scope-change process](docs/planning/SCOPE_CHANGE_PROCESS.md); implementation
inconvenience does not. Protect against both scope creep and scope erosion.

## Fresh-session startup / `next chunk`

1. Read this file, `memory/PROJECT_STATE.md`, `memory/CONSTRAINTS.md` and
   `memory/repository.json`. Confirm the repository root and expected origin. If origin
   identity is not configured, STOP with the setup blocker; never invent a repository.
2. Require a clean working tree. Run `git fetch origin`, `git checkout master`, and
   `git pull --ff-only origin master`. If any step fails or master has diverged, STOP.
   Do not reset, stash, discard, rebase, or destructively repair someone else's work.
3. Run `python3 scripts/reconcile_state.py` on synchronized master. It performs a fresh
   remote-tip check and fresh GitHub HTTPS reads. Reconciliation is read-only. On an
   error, DRAFT scope, or absent candidate, report the reason and STOP. Do not use
   `progress.json` or chat history to override the result.
4. Select exactly the reported `next_candidate_chunk`. Read its Markdown manifest,
   declared required context, required skills, and relevant implementation files.
   Load optional context/skills only when needed; never load every skill.
5. Create `feature/<chunk-id-lowercase>-<slug>` from that synchronized master and record
   `base_master_sha`. Persist effective state/scope corrections only on this feature
   branch. Never branch from an unmerged feature PR or write/commit directly on master.
6. Implement exactly this one chunk. Follow the locked object model, service and port
   boundaries, Code Blueprint, API contracts and frontend/backend mappings. Reuse
   meaningful domain behavior. No unrelated refactoring, speculative abstraction,
   partial substitution, postponed acceptance criteria, or next-chunk implementation.
7. Run the manifest's required tests and affected checks. Prove negative authorization,
   ownership and resource-state cases, not only happy paths. Spawn an independent
   reviewer with the chunk, relevant authority, diff and test results. Resolve all
   Critical and High findings and rerun affected checks.
8. On the feature branch, update compact memory and both registry/manifest metadata.
   Set the active chunk `PR_OPEN`, never `COMPLETE`. Record immutable completion
   evidence using [the evidence protocol](docs/planning/STATE_RECONCILIATION.md).
9. Commit, push the feature branch, and open a PR targeting `master`. Add the assigned
   PR number to execution metadata in a follow-up feature-branch commit if necessary.
   Ensure all final checks and independent review cover the final diff.
10. Give a bounded PR handoff and STOP. The human reviews and merges remotely. Never
    auto-merge, start a second chunk, or treat PR_OPEN as COMPLETE.

## Boundaries and stop conditions

- One backend, one PostgreSQL source of truth, one domain and authorization model.
- Parent resources are family-owned; students see only their own released learning
  data; teachers access only assigned educational data and have zero financial
  administration; only appropriately authorized admins operate finance.
- Enforce access in API, application service and repository scope, with UI guards as
  additional controls. Never rely on hidden navigation. Do not broaden permissions.
- Student name and age are required; school is optional. Minimize child data.
- External providers remain behind ports; browser redirects cannot confirm payments.
- Stop the affected chunk for incompatible locked design, unknown required business
  decisions, missing dependencies, required context/skills, or Critical/High findings.
  Record the concrete conflict on the feature branch; do not silently redesign.
- A historical chunk is COMPLETE only through verified merged-PR and Git artifact
  evidence on fresh master. Independent ready work may proceed when another PR is
  unmerged, according to deterministic selection; dependent work may not.

`skills/skill-router.md` is the routing index. Repository-owned skills use
`skills/<category>/<name>/SKILL.md`. Detailed docs are authority; memory is a compact
cache. Do not create vector/embedding memory or a chronological execution diary.
