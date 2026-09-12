---
name: zuno-component-architecture
description: "Apply frontend component boundaries rules when the selected Zuno Edu chunk changes this boundary."
---
# Frontend component boundaries

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/FRONTEND_COMPONENT_CATALOG.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Route composes feature; feature composes domain component and UI primitives. Receive least-privilege DTOs. Do not duplicate forms/business decisions across surfaces.

## Verification requirements
Verify component API mapping and dependency boundaries. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
