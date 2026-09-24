CHUNK: BOOTSTRAP / ADR-0004; ZE-P02-C01 remains conditional
STATUS: DRAFT planning correction, reviewed; publication pending
COMMIT: Base f1f18fbd0e77bd305cd71d1ca6aa2d17d773bad3
PR: pending; branch feature/mfa-enrolment-retry-contract
CHANGE: Architecture 2 defines one-time MFA provisioning, safe duplicate errors and explicit restart. Scoped repository and keyed metadata contracts included. Scope 1.0 unchanged.
VALIDATION: Plan, routing and graph pass; independent deep review approved. See docs/planning/verification/ADR-0004-mfa-enrolment-retry.md and memory/handoffs/ADR-0004-review.md. Workflow rerun pending.
BLOCKERS: Human planning merge required before product implementation. Partial C01 work is preserved uncommitted in worktree 9047 and excluded here.
NEXT: After human merge, synchronize clean master and run scripts/next_chunk.py. Preserve and assess partial local C01 work before resuming; never reset or discard it.
NEXT_MODEL: gpt-6-astra
REASONING: xhigh
WHY: Authentication boundaries require independent security review.
LOAD: AGENTS.md; memory/repository.json; ADR 0004; fresh synchronized next_chunk.py packet; docs/planning/chunks/ZE-P02-C01.md only if selected.
