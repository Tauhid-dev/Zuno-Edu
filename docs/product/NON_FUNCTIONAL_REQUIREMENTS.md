# Non-functional requirements

Status: DRAFT — proposed complete launch baseline, pending human review and remote merge.

Canonical inventory: `requirements.json`. These readable records are generated from that inventory; IDs are stable and are never renumbered or reused. Every requirement is REQUIRED FOR LAUNCH. No item is implicitly deferred. Related domain capability is the routing key used by design and chunk traceability.

## NFR-001 — Meet a measurable interactive performance baseline.

Rationale: Users need responsive service on ordinary connections.

Roles: Public, Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `performance`.

Acceptance:

- At 100 concurrent authenticated users, read API p95 ≤500ms and write p95 ≤1s excluding file transfer/provider checkout.
- Normal authenticated navigation p75 LCP ≤2.5s on defined mobile test profile.

## NFR-002 — Target reliable monthly service and visible degradation.

Rationale: Scheduled teaching needs dependable access.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `availability`.

Acceptance:

- Production target is 99.5% monthly availability excluding approved maintenance.
- Health/alerting and incident records permit calculation and failed integrations expose retryable status.

## NFR-003 — Meet WCAG 2.2 AA for launch critical journeys.

Rationale: Every surface should be usable with assistive technology.

Roles: Public, Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `accessibility`.

Acceptance:

- Keyboard, focus, labels, contrast, error announcements and screen-reader checks pass critical flows.
- Video content includes captions/transcript and diagrams have text alternatives.

## NFR-004 — Support current desktop and mobile web viewports.

Rationale: Families need access across common devices.

Roles: Public, Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `responsive_ui`.

Acceptance:

- Critical flows work at 360px mobile and 1280px desktop with current Chrome/Safari/Firefox/Edge plus previous major browser versions.
- No essential action depends on hover alone.

## NFR-005 — Use one OOP modular backend with dependency inversion.

Rationale: All portals need one authoritative business model.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `architecture`.

Acceptance:

- Domain entities/value objects/policies contain invariants without framework/provider imports.
- Application services orchestrate repositories/ports.
- API endpoints contain no scattered business rules.

## NFR-006 — Maintain one versioned API contract and generated frontend types.

Rationale: Surfaces must not drift from backend meaning.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `contracts`.

Acceptance:

- Every UI operation maps to documented /api/v1 contract/service and permission policy.
- Contract validation detects missing routes, incompatible schemas and duplicated handwritten frontend DTO definitions.

## NFR-007 — Preserve transactional consistency and concurrency safety.

Rationale: Seats, money and learning revisions need reliable state.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `consistency`.

Acceptance:

- Unit-of-work boundaries, unique constraints, version preconditions and outbox protect concurrent mutations.
- Conflict returns actionable 409 and never silently overwrites newer data.

## NFR-008 — Prove critical behavior at domain, API, persistence, adapter and UI layers.

Rationale: Feature presence is insufficient without verification.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `testing`.

Acceptance:

- Negative authorization, migration, provider retry/idempotency and critical end-to-end journeys have required automated coverage.
- Accessibility and restore tests have recorded evidence.

## NFR-009 — Follow the locked blueprint and purposeful reuse.

Rationale: Future chunks need predictable architecture.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `maintainability`.

Acceptance:

- Durable classes/services/ports/components map to blueprint and requirements.
- Material deviations stop affected chunk for review.
- Private helpers need no architecture redesign.

## NFR-010 — Keep requirement, design, chunk and verification traceability complete.

Rationale: Launch scope must resist creep and erosion.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `planning_integrity`.

Acceptance:

- Every required ID maps to object/service/API or justified operational consumer, chunk and tests.
- Every chunk serves approved requirements and dependency graph is acyclic.

## NFR-011 — Execute one deterministic chunk from synchronized remote master.

Rationale: Fresh sessions need safe repeatable continuation.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `workflow`.

Acceptance:

- Agent fetches/fast-forwards master without modification, reconciles merged evidence read-only, selects eligible chunk deterministically, branches once, reviews/tests and hands off PR_OPEN.
- Only human remote merge enables COMPLETE.

## NFR-012 — Use least-data projections across all five surfaces.

Rationale: Shared backend must not mean shared visibility.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `privacy_by_design`.

Acceptance:

- DTOs explicitly whitelist permitted fields for public, family, student, assigned teacher and admin capabilities.
- Cross-surface tests prove financial and child-data segregation.

