---
name: state-reconciliation
description: Recompute effective Zuno Edu scope and chunk status from fresh remote master; use before selection, not to trust a cached handoff.
---

# State Reconciliation

## Required context

Read memory/repository.json, docs/planning/STATE_RECONCILIATION.md and the compact progress cache; the script loads canonical plan/evidence from master.

## Rules

Run scripts/reconcile_state.py after required synchronization. It must remain read-only and compare the server tip before and after fresh official GitHub HTTPS evidence reads. Prefer authenticated gh; standard-library token/public REST fallback supports a fresh session without gh installed. Rate/access/network errors stop selection. DRAFT/null candidate or BLOCKED output authorizes no work.

## Implementation standards

Trust merged PR identity, immutable witness inclusion and dependency completion; do not infer completion from a message, open PR, local head ancestry or progress flag. Squash/rebase support uses merge-tree evidence.

## Verification

Verify candidate has all dependencies effectively COMPLETE and no blocker. Persist corrections only after creating its feature branch. For changes to this skill/script, run isolated workflow behavior tests.

## Common failures

Failure signals: stale origin/master, unverified exported PR JSON, forged COMPLETE, modified witness, bot planning merge, altered locked plan, master writes.

See [the repository constitution](../../../AGENTS.md) and [state protocol](../../../docs/planning/STATE_RECONCILIATION.md) for shared authority. Do not load unrelated skills.
