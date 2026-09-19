---
name: zuno-sqlalchemy-alembic
description: "Apply data mapping and migrations rules when the selected Zuno Edu chunk changes this boundary."
---
# Data mapping and migrations

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DATABASE_SCHEMA_PLAN.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Use explicit data mappers, named constraints and aggregate transaction scope. Test on PostgreSQL. Expand-contract migrations and avoid startup auto-migrate.

## Verification requirements
Prove upgrade, compatibility rollback, uniqueness and concurrent writes. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
