---
name: zuno-deployment
description: "Apply controlled release promotion rules when the selected Zuno Edu chunk changes this boundary."
---
# Controlled release promotion

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Promote immutable tested digest staging→production, record migration/config versions and run smoke tests. No app auto-merge/deploy from chunk PR.

## Verification requirements
Rehearse compatible rollback and health/degraded provider cases. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
