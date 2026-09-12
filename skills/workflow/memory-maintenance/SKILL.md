---
name: memory-maintenance
description: Maintain compact Zuno Edu operational memory during chunk work and handoff; not duplicate authoritative design documents.
---

# Memory Maintenance

## Required context

Read current effective reconciliation, active chunk, memory/PROJECT_STATE.md, progress.json and relevant durable decisions.

## Rules

Write only on the selected feature branch. Cache actual effective states and master SHA; progress hints never override master. PROJECT_STATE holds project/version/phase/execution/next candidate/blockers/constraints/test baseline only.

## Implementation standards

Keep architecture snapshot compact and decisions durable. Put exact task context in the chunk; put long evidence in named handoff records. Keep canonical registry and Markdown metadata consistent. Do not create diary, embeddings or vector memory.

## Verification

Validate JSON, required metadata, references and absence of premature COMPLETE. Preserve immutable completion evidence files after merge; update current cache rather than historical witnesses.

## Common failures

Failure signals: verbose history in progress.json, copied architecture, contradictory next candidate, missing base master SHA or treating conversational history as authority.

See [the repository constitution](../../../AGENTS.md) and [state protocol](../../../docs/planning/STATE_RECONCILIATION.md) for shared authority. Do not load unrelated skills.

