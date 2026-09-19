---
name: zuno-resource-ownership
description: "Apply family, student and teacher scope rules when the selected Zuno Edu chunk changes this boundary."
---
# Family, student and teacher scope

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DATA_ACCESS_BOUNDARIES.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Derive family and student relationships from trusted actor, never supplied ownership fields. Recheck active assignment and resource cohort/student consistency.

## Verification requirements
Test cross-family, other student, unrelated teacher and revoked links. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
