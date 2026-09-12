---
name: zuno-python
description: "Apply typed python implementation rules when the selected Zuno Edu chunk changes this boundary."
---
# Typed Python implementation

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/BACKEND_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Keep domain framework-free; use immutable value objects and explicit types/errors. Never use float for money or naive datetime for schedule.

## Verification requirements
Run type/lint and changed domain/application tests. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
