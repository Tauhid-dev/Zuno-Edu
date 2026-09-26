## Chunk

ZUNO_EDU_CHUNK:ZE-P02-C01

## Requirements

ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011.

## Objective

Implement authentication, server sessions, mandatory staff MFA and adult recovery. Staff password authentication now returns a limited challenge/setup context; only verified MFA creates a full staff session.

## Implemented

AuthenticationService and strict catalog HTTP routes; Argon2id credentials; signed browser binding, CSRF/Origin checks and secure cookies; account-state checks and revocation; encrypted TOTP, single-use recovery proofs and ADR 0004 enrolment replay/restart semantics; PostgreSQL migration and account-first locking; encrypted durable recovery intent with UUID-only outbox and audited transaction composition.

## Explicitly not changed

Registration/family orchestration, role-facing UI and deployment remain in their assigned chunks. Human merge only.

## Authorization impact

Current account state is checked under lock. Email-less student usernames resolve provisioned student Account UUIDs only. Limited MFA contexts cannot reach full-session operations. Recovery-code repository writes enforce factor ownership. Sessions and tokens are rechecked after lock waits, so waiting cannot extend expiry.

## Architecture impact

Preserves architecture 2 and ADR 0004. Audit, managed keys, breached-password screening and current staff approval are explicit fail-closed composition dependencies. Migration 0002 is additive and forward-only; deployment needs citext extension privileges.

## Tests

125 combined authentication/affected regression tests; 55 C01 tests; 61 workflow tests. Real PostgreSQL 16.15 and Redis 7, including concurrent enrolment, password-reset races and lock waits crossing expiry. Ruff, formatting, mypy, plan/workflow validation and secret scan pass. Two existing pinned Starlette/httpx deprecation warnings remain.

## Verification

docs/planning/verification/ZE-P02-C01.md maps acceptance to tests. memory/completions/ZE-P02-C01.json contains 31 verified artifact hashes.

## Independent review findings

Critical risk, independent deep review by /root/contract_review. All material findings fixed and retested; final approval with zero Critical/High/material Medium findings. See memory/handoffs/ZE-P02-C01-review.md.

## State

PR_OPEN: #12. Published feature implementation d92178f; execution metadata recorded on this branch. Not COMPLETE until verified human merge.

## Base master SHA

9e6974081241c28f4a31b0e7da4ca7ba6f7391ec

## Human action

Review and merge into master if approved.

## Next context

Conditional ZE-P02-C02, gpt-6-astra / xhigh, for critical authorization/audit boundaries. Synchronize master and run scripts/next_chunk.py after human merge; forecast is not execution authority.
