# Master implementation plan

Status DRAFT. Scope1.0, architecture1. 219 required launch requirements,12 capability phases,62 bounded implementation chunks. No product requirement is implemented during bootstrap.

Read LAUNCH_SCOPE and the Code Blueprint first for human review. Future agents use AGENTS.md, synchronized origin/master, read-only verified merge reconciliation and the selected manifest only. Exactly one chunk per PR; human merges. Independent READY branches may proceed without treating an unmerged dependency as complete. The deterministic sequence breaks ties among eligible nodes.

Each backend chunk owns a cohesive domain/application/API boundary, each frontend chunk consumes already specified APIs, and each operations chunk supplies explicit launch evidence. Integration/provider actions have dedicated failure/replay tests. Larger curriculum and billing areas split by durable responsibility; pure helpers and each CRUD verb do not become administrative chunks. The DAG records real coupling and allows parallel file/content work.

Planned requirement coverage is 100%; actual implementation coverage is 0%. See traceability.json and CHUNK_REGISTRY.md. Final production approval is separate from planning scope approval and requires every acceptance criterion, complete security/accessibility/provider checks, migration/restore/rollback evidence and human business/legal configuration gates. Future considerations are never automatically executed.

Planning review and validation results are in INDEPENDENT_REVIEW.md and BOOTSTRAP_VALIDATION.md. Scope remains DRAFT until the identified planning PR is human-merged and reconciliation verifies the exact approved artifact witnesses. Draft status in the merged file is resolved without editing master; the next feature branch persists the effective LOCKED state.
