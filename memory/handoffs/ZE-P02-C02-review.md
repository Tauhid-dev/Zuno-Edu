# ZE-P02-C02 review and acceptance evidence

Date: 2026-09-28. Base: b9acb4b6448f3e719465d9d654e7b078f0d6a08d.
Implementation: 82cd43f6510055b5c31271af23ea7e0878afa442.
Risk: critical. Depth: independent deep review. Reviewer: /root/c02_security_review;
reviewer did not author implementation. Final result PASS; Critical 0, High 0,
unresolved Medium 0. Human merge is still required.

Two Medium findings fixed and independently rechecked: empty SQL results after a
lock wait now unconditionally recheck current session/MFA authority; identity
factories receive the server request ID and persisted actor/correlation is tested.
Shared scopes explicitly re-resolve identity, bind resource and enforce current
entitlement/enrolment. No product scope, API contract or architecture change.

Acceptance proof in tests/chunks/ZE-P02-C02:
- Fixed MFA tests cover within/exact/older/missing/future evidence. Real PostgreSQL
  and HTTP step-up proves ordinary session/cookie survives pending/failed MFA,
  activity never extends freshness, successful proof restores audit, replay and
  foreign proof do not refresh original authority.
- Direct API, service and repository tests deny parent/student/teacher/non-audit
  admins; forged client role/privilege/principal input cannot supply authority.
  Current roles, account/session revocation and purpose are rechecked in SQL.
- Resource policy tests cover cross-student, current guardian/assignment revocation,
  independent billing, release and entitlement; concrete future feature SQL remains
  owned by its planned chunk. Existing RoleGrant rejects teacher/admin capabilities.
- Audit tests prove bounded actor/action/target/time filtering, encrypted cursor
  binding, safe field projection, immutable records and SQL update/delete/truncate
  denial, exact writer/reader privileges, and rollback/fail-closed audit failures.
- Real account-lock and empty-table-lock waits across expiry deny protected reads.
- Migration head upgrade/idempotence/metadata/application rollback passes; downgrade
  fails safely without deleting evidence. Session revocation trigger is transactional.

Validation: final focused suite 41 PASS; earlier affected authentication/boundary
suite 94 PASS; workflow 61/61 PASS. Python lint/format/typecheck, generated contract
check, frontend typecheck, secret scan, plan/witness/routing/graph and whitespace PASS.
Full local product run: 162 PASS; details in docs/planning/verification/ZE-P02-C02.md.
Two unchanged Redis-dependent tests require CI's isolated Redis service; no tests
were disabled in repository configuration. CI must pass before human merge.
