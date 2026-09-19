---
name: scope-control
description: Guard a Zuno Edu implementation against additions, erosion or architecture drift; use when work risks departing from the approved baseline.
---

# Scope Control

## Required context

Read SCOPE_LOCK, LAUNCH_SCOPE, OUT_OF_SCOPE, affected requirements and docs/planning/SCOPE_CHANGE_PROCESS.md.

## Rules

Treat the human-approved merged baseline as binding. Explicit human instruction identifying a scope change is required to propose changed scope; implementation inconvenience is not authorization. Stop the affected chunk on a concrete design conflict.

## Implementation standards

A proposal records exact behavioral changes, requirements, architecture/security/data impact, acceptance criteria, dependency changes, versions and approval evidence. Keep unapproved implementation out of its planning PR.

## Verification

Independently review and validate traceability plus plan witnesses. Human reviews/merges the proposal; synchronize/reconcile before executing a changed-scope chunk.

## Common failures

Failure signals: MVP reinterpretation, silently postponed requirement, opportunistic redesign, weakened permissions, hidden extra capability or stale approval witnesses.

See [the repository constitution](../../../AGENTS.md) and [state protocol](../../../docs/planning/STATE_RECONCILIATION.md) for shared authority. Do not load unrelated skills.
