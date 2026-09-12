---
name: chunk-execution
description: Execute one eligible Zuno Edu implementation chunk after scope approval; use for next chunk requests, not freeform product planning.
---

# Chunk Execution

## Required context

Read AGENTS.md, the reconciler-selected chunk, required context and required skills. Follow its dependencies and locked acceptance criteria.

## Rules

Run the fresh-session synchronization/reconciliation protocol before choosing work. If no authoritative candidate exists, stop with evidence. Create a new branch from returned master SHA, persist state corrections there, and implement only the selected responsibility.

## Implementation standards

Use the documented OOP objects, services/ports, API contracts and component mapping. Load optional skills only for relevant touched work. Do not implement adjacent chunks or replace difficult requirements.

## Verification

Run manifest checks and independent review; fix all Critical/High findings. Record PR_OPEN, immutable evidence and actual PR number; hand off without merging or starting another chunk.

## Common failures

Failure signals: stale progress hints, branching from an unmerged dependency, DRAFT implementation, hidden deferred acceptance criteria, or COMPLETE before verified merge.

See [the repository constitution](../../../AGENTS.md) and [state protocol](../../../docs/planning/STATE_RECONCILIATION.md) for shared authority. Do not load unrelated skills.

