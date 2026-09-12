# Engineering standards

Every change belongs to exactly one selected manifest. Read locked scope, relevant blueprint, API mapping and required skills. No opportunistic redesign, unrelated refactoring, new business capabilities or silent requirement removal. A missing material public contract stops the affected work and produces a blueprint conflict record with requirement, existing decision, evidence and proposed resolution. Small private helpers are permitted when behavior and architecture remain unchanged.

Prefer meaningful reuse: Money, time ranges, scoped actor context, errors, domain policies, request validation, shared UI and test factories. Do not build universal repositories/services to conceal distinct invariants. Keep dependencies explicit and direction checked with import tests. Documentation and generated contracts change in the same chunk as behavior. Record actual verification results; planned tests are not evidence. Critical/High review findings block handoff; human merges remotely.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
