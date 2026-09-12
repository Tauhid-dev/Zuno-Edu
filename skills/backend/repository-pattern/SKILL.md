---
name: zuno-repository-pattern
description: "Apply scoped persistence interfaces rules when the selected Zuno Edu chunk changes this boundary."
---
# Scoped persistence interfaces

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/PORTS_AND_REPOSITORIES.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Implement aggregate repositories with explicit family/student/teacher query scope. Avoid universal repository or session leakage into domain.

## Verification requirements
Prove cross-family/assignment queries return no unauthorized records. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
