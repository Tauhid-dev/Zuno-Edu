---
name: zuno-child-family-data-boundaries
description: "Apply child data minimization rules when the selected Zuno Edu chunk changes this boundary."
---
# Child data minimization

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DATA_ACCESS_BOUNDARIES.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Require name and declared age, keep school/extra fields optional. Teacher projection contains teaching need only. No billing, guardian private details or sensitive notes leak.

## Verification requirements
Assert DTO field absence and access after role/relationship changes. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
