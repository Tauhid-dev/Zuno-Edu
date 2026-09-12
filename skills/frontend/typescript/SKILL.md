---
name: zuno-typescript
description: "Apply typescript contracts and strict typing rules when the selected Zuno Edu chunk changes this boundary."
---
# TypeScript contracts and strict typing

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/FRONTEND_STATE_AND_API_MODEL.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Generate transport types from OpenAPI; use discriminated unions for lesson blocks and errors. Avoid any casts concealing absent authorization-safe fields.

## Verification requirements
Run strict type checking and verify schema/client drift. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
