---
name: zuno-backend-testing
description: "Apply backend verification rules when the selected Zuno Edu chunk changes this boundary."
---
# Backend verification

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/BACKEND_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Choose domain/application/repository/API/adapter tests appropriate to changed boundaries; authorization negatives are mandatory where access changes.

## Verification requirements
Run targeted tests plus relevant regression; record real command/result evidence. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
