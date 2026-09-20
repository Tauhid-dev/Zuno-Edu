# Agent workflow

## Execution

Authority remains approved scope/requirements, accepted ADRs, Code Blueprint,
architecture/contracts, active chunk, standards/skills, implementation, assumptions.
Build the complete defined launch exactly; neither expansion nor erosion is allowed.
Use the existing scope-change process for explicit human changes; stop an affected
chunk for incompatible contracts instead of silently redesigning.

`next_chunk.py` reuses the existing reconciler and registry. It reads the registry in
code but returns only the selected chunk. It never synchronizes Git, writes master,
implements code or treats cache/handoff claims as proof. Synchronize first as AGENTS
instructs. Persist reconciliation corrections only on the new feature branch.

Load the manifest, packet, relevant current handoff and selected technical skills.
Read named requirements and domain/API/frontend entries through `--context`; read
referenced narrative sections. Frontend readers accept `route:/path`,
`mapping:ComponentName` and `presentation_type:Name`; use a justified expansion
when a shared component needs a route owned elsewhere. Expanded service reads retain
all method contracts, subject to the same explicit budget exception. Start source discovery with expected files/areas,
then targeted `rg` for needed symbols. Exclude unrelated modules, whole catalogs,
all-skill loading, previous chunks and historical handoffs.
Declared workflow skills are phase-specific: chunk-execution now, review-agent for
medium+ review, pr-handoff/memory-maintenance at handoff, scope-control for conflicts,
state-reconciliation for evidence/sync issues. Technical required skills remain
mandatory; optional skills load only for an actual changed boundary.

The chunk token budget covers cumulative repository context, not reasoning/test
execution. Estimates use UTF-8 bytes/4, not a tokenizer guarantee. Count packet,
manifest, skills and source excerpts too. Read one contract at a time; oversized
output is refused, never silently truncated. Before exceeding the budget, identify
the trigger and exact extra reference: contract ambiguity, missing dependency,
relevant failing test, architecture conflict, inconsistent state, regression/audit.
Use `--reason` for that targeted read and record one line in verification. Necessary
safety context must be loaded; budgets cannot excuse omitted invariants/acceptance.

API, application and repository ownership controls remain binding; UI guards are
additional. Teacher principals have zero finance; family/student/assignment isolation
and child data minimisation remain mandatory. Providers stay behind ports; server
payment proof is authoritative. Read the selected contracts, not prior chat summaries.

## Validation

The packet provides command profiles plus existing chunk acceptance/test requirements.
Commands are planned until executable/configuration exists. P01-C01 establishes the
pinned Python/web harness; never mark missing commands PASS or skip acceptance.
A missing prerequisite blocks the affected chunk. Use pinned repository tools;
record actual expanded source/test targets in verification, not invented scripts.

Every chunk runs plan/workflow metadata checks and applicable lint, format, typing,
unit, integration, build, migration or security checks. Scope product checks to the
chunk and affected regressions; its provider/database/security scenarios remain
mandatory. Run migration commands only against an isolated disposable test database,
never a production/default database. Keep counts/results and relevant failures in the handoff, full logs in
test artifacts. Rerun affected checks after fixes; broaden for demonstrated coupling
or safety concerns, not unchanged passing work.

## Review

Risk is the maximum of the chunk floor and actual change; `--preview <ID> --risk high`
(or critical) produces the raised packet without authorizing execution. Low: established public
UI/DTO/CRUD or mechanical docs with no new access boundary — deterministic checks
and lightweight author diff review. Medium: ordinary business/API integration or
multi-module behavior — focused AI second pass against scope, contracts and tests.
High/critical: authentication, authorization, child/family isolation, payments,
destructive operations, migrations, cross-domain contracts or security boundaries —
independent deep review; reviewer must not author implementation. Load relevant
contracts/diff/evidence, never the whole project by default.

Read review-agent for medium+. Record risk, depth, reviewer identity, independence,
findings and affected retests in the existing hashed review artifact. Resolve
Critical/High and practical material Medium. Completion adds `review.risk`,
`review.depth` (lightweight/focused/deep), `review.independent`; high/critical requires
deep and true. Deterministic validation and human merge are always required.
Systemic findings raise risk/depth. No expensive full AI review for trivial work.

## Handoff

Use the existing evidence protocol and PR template. Track local milestones in
`execution.stage`: IMPLEMENTED, VALIDATED, REVIEWED, PUSHED, PR_OPEN. Registry status
is IN_PROGRESS then PR_OPEN; only verified remote evidence establishes COMPLETE/MERGED.

Update the existing small progress cache with verified master SHA, confirmed merged
chunks, active chunk/PR and blockers. Never optimistically complete the current chunk.
Replace `memory/CURRENT_HANDOFF.md` (target ≤250 words): CHUNK, STATUS, COMMIT, PR,
CHANGE, VALIDATION, BLOCKERS, NEXT, NEXT_MODEL, REASONING, WHY, LOAD. Use actual refs;
unavailable PR creation is a blocker. Archive the final per-chunk handoff in existing
`memory/handoffs/<ID>.md`, not another state system. History loads only for regression,
architecture inconsistency or audit.

`next_chunk.py --recommend-after <ID>` forecasts the following candidate/model from
the current cache. It is explicitly conditional, never READY authority; the next
session must synchronize/recompute. Unresolved prerequisites cannot be invented away.
Use its packet for exact next LOAD references. Commit, push, open/update one PR,
record its actual number/final checks and STOP. Human merge only; no second chunk.

## Models

Recommendations are project policy, not benchmarks or automatic account changes.
Low: Luna/low. Normal: Terra/medium. Integrations/multi-module complexity: Sol/medium.
Difficult concurrency/debugging: Sol/high. Sensitive boundaries: Astra/high.
Critical migrations/systemic failures: Astra/xhigh. No Max/Ultra default. If unavailable,
recommend an available equivalent; never silently choose insufficient capability.

Escalate one tier for repeated unexplained failures, conflicting contracts, unexpected
security behavior, undeclared coupling, migration uncertainty or systemic review
findings. Record why/targeted context. Escalation grants no scope change; return to
normal settings once resolved. First runtime/test foundation: Terra/medium, since
architecture is fixed and the task establishes Python/TypeScript tooling, not features.

Policy informed by [official Codex model guidance](https://learn.chatgpt.com/docs/models)
(checked 2026-09-20): match capability to task and use the lowest adequate reasoning.
Model IDs reflect the available host catalog then, not a permanent availability promise.
