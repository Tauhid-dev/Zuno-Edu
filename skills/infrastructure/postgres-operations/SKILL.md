---
name: zuno-postgres-operations
description: "Apply postgresql production care rules when the selected Zuno Edu chunk changes this boundary."
---
# PostgreSQL production care

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Restrict network/users, monitor storage/pool, apply migrations under lock and encrypt off-host backup/WAL. Never use Redis as payment truth.

## Verification requirements
Run database restore/constraint/query plan checks and alert smoke tests. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
