# ZE-P01-C02 independent review

Date: 2026-09-21. Risk: critical. Depth: deep. Independent: true.
Reviewer: Codex independent review agent `/root/persistence_review`, separate
from the implementation author `/root`. The reviewer read and assessed source,
contracts and tests, and authored only this review artifact.

Reviewed the implementation on `feature/ze-p01-c02-persistence-durable-jobs`
against master `293e6c2b2d0f011cc95f6d6cb192aa4d1c754737`, including the final
BackgroundJob policy correction. Context was limited to the active manifest,
Review policy, relevant persistence/worker skills, targeted requirement,
object, port, operation and schema entries, backend dependency rules and the
three delivery-table schema sections. Inspected all new persistence,
migration, worker composition, operations domain/application and shared
persistence source files, dependency changes and C02 tests.

## Findings and resolution

- Critical: none.
- High: none.
- Medium, resolved: retry, claim exhaustion and lifecycle policy initially
  lived entirely in the SQL adapter while BackgroundJob was a passive record.
  This conflicted with the named BackgroundJob transitions and the architecture
  rule that domain entities own meaningful transitions. The author moved
  claim/succeed/retry/dead-letter decisions into the framework-free domain
  object, added invariant checks on reconstitution, and retained row locking,
  lease tokens and optimistic compare-and-swap in the data mapper. The reviewer
  inspected the resulting domain methods and repository call sites.
- Low: no outstanding actionable finding. The existing test-client deprecation
  warnings do not affect these changes.

Affected retests: the complete C02 PostgreSQL/Redis suite and C01 regression
suite were rerun after the correction. The final recorded result is 41 passed
(26 C02, 15 C01), with two dependency deprecation warnings, in
`docs/planning/verification/ZE-P01-C02-tests.log`. The reviewer inspected this
captured output and the test bodies; the reviewer did not independently claim
to execute the database suite. Added regressions cover direct domain
transitions/invalid state, claim exactly at the 24-hour cutoff, and eight
successive expired worker claims without a ninth attempt.

## Boundary assessment

- Explicit SQL-to-domain mapping preserves framework-free domain objects.
  Repository APIs do not expose sessions to application/domain callers.
- UoW commit and rollback keep outbox and injected audit writes atomic; a
  missing audit writer rejects nonempty audit input before accepting the
  transaction. Concrete audit feature persistence belongs to its owning chunk.
- PostgreSQL uniqueness and held-lock contention tests protect delivery
  identity. Lease-token/version checks prevent stale acknowledgements after
  reclamation. Immutable payload/identity triggers prevent retry rewriting.
- Redis carries opaque wakeups. SQL jobs survive flushed or unavailable Redis,
  and handlers execute outside held database transactions. Restart-after-effect
  tests use an idempotent handler; real provider adapters must implement the
  same reconciliation contract in their owning chunks.
- Retry delays, Retry-After, eight-attempt/24-hour limits and quarantine of
  ambiguous outcomes are covered. Worker handler kinds form an explicit scope.
  Dispatch requires trusted composition identity and has no browser route.
- The migration is explicit, PostgreSQL-only and absent from API startup. Tests
  cover fresh upgrade, metadata consistency, repeat upgrade and compatibility
  with the preceding application. Destructive schema downgrade is refused;
  application rollback and reviewed forward fixes preserve data.
- Changes implement the foundation objective. No settings/integration feature
  aggregate, role-facing endpoint, permission change or unrelated product chunk
  is introduced. Feature handlers and cross-module launch composition remain
  the responsibility of their scheduled owning chunks.

No unresolved Critical, High or practical material Medium finding remains in
the reviewed implementation. Deterministic workflow/evidence validation must
also pass before PR handoff. This review is not merge authority; human review
and human merge remain required.

## Supplemental check, 2026-09-22

Reviewed the adjustment to
`tests/workflow/test_routing.py::test_conditional_forecast_never_selects_completed_or_mutates_plan`.
It now creates a deep-copied, explicitly PLANNED fixture rather than depending
on the live execution status of C02. It preserves completed-chunk exclusion and
the original no-mutation assertion, and additionally checks IN_PROGRESS
exclusion. No runtime routing or safety assertion was weakened. The observed
registry/manifest changes affect execution metadata only; progress identifies
the previously merged C01 and active C02 consistently.

Inspected the initial verification document, persistence README,
CURRENT_HANDOFF and PROJECT_STATE against the captured product/static/build/
migration output and registry/progress. Their 41-test count, migration result,
scope boundaries, base SHA, branch and pending workflow/PR status are consistent
with the available evidence. The conditional C03 recommendation matches
`next_chunk.py --recommend-after ZE-P01-C02` and grants no execution authority.
No premature completed/merged claim is made. Completion witness hashes and
actual PR metadata remain to be checked after those artifacts are created.

## Final precommit evidence check, 2026-09-22

Independently recomputed the SHA-256 digests of all 29 distinct artifacts in
`memory/completions/ZE-P01-C02.json`: zero mismatches before this report update.
The witness names exactly NFR-007, OPS-004 and OPS-005, includes all four required
acceptance tests, and records critical/deep/independent review with zero Critical
or High findings. Source, migration, tests, lockfile, review and captured logs are
covered. The author must refresh this report's digest after this update.

Inspected the final workflow log: 61 tests completed successfully. The verification
document and both handoffs match this result and the 41 product/regression tests.
The static/build/migration log records successful checks. Independently reran
`scripts/validate_plan.py` and `scripts/next_chunk.py --validate`: both PASS,
including all 113 scope witnesses. The registry/manifest diff changes status and
execution metadata only; the manifest acceptance body remains unchanged.
Progress correctly leaves C02 active and C01 as the last completed chunk.

Precommit state is consistently IN_PROGRESS/REVIEWED, with commit and PR pending;
no remote PR or merge is falsely claimed. No additional finding. Actual PR
metadata must be recorded and checked after creation; human merge is still
required.
