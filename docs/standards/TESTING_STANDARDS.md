# Testing standards

Domain tests prove lifecycle and invariants, application tests prove orchestration/authorization with fake ports, repository tests use PostgreSQL constraints/locking and query scope, API tests assert exact DTO/error contracts. Adapter tests prove webhook validation, retries, idempotency and timeout/reconciliation against recorded HTTP fixtures; staging sandbox evidence validates real provider configuration. Frontend tests verify components and route guards; Playwright journeys exercise actual backend boundaries.

Mandatory negatives: teacher payment access, teacher unrelated student, parent other family/child, student other submission and student billing; repeat direct API calls after client manipulation. Include cross-role field omission and revoked relationship/session cases. Migration upgrade/rollback compatibility, duplicate/reordered events, concurrent last seat/refund, DST, file poisoning, keyboard/reader behavior and backup restore are launch gates. Use synthetic fixtures. Each requirement has named tests and a verification evidence location; tests are PLANNED until actually run. No fabricated green checks. Bootstrap tests cover only planning/workflow tooling.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
