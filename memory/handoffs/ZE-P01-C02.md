CHUNK: ZE-P01-C02
STATUS: PR_OPEN; awaiting human review and merge
COMMIT: 7578359c6837fea5bff5508b54137106b504c862
PR: https://github.com/Tauhid-dev/Zuno-Edu/pull/7; branch feature/ze-p01-c02-persistence-durable-jobs
CHANGE: PostgreSQL UoW, Clock/version types, outbox/inbox/job leases, Redis wakeups and recovery, Alembic migration harness and focused tests.
VALIDATION: 41 product/regression tests and 61 workflow tests passed; lint/format/mypy/compile, plan/routing, PostgreSQL migration/metadata/compatibility and package build passed. Independent critical/deep review resolved its domain-policy finding. Evidence: docs/planning/verification/ZE-P01-C02.md and memory/completions/ZE-P01-C02.json.
BLOCKERS: None; human review/merge remains required.
NEXT: Human-review/merge this chunk. Then synchronize master and run next_chunk.py; ZE-P01-C03 remains conditional.
NEXT_MODEL: gpt-6-astra
REASONING: high
WHY: Conditional API/CI foundation requires independent review of security-sensitive boundaries.
LOAD: AGENTS.md; memory/repository.json; fresh synchronized next_chunk.py packet; docs/planning/chunks/ZE-P01-C03.md and only its routed context if authorized.
