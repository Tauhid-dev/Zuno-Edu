---
name: zuno-frontend-testing
description: "Apply frontend behavior verification rules when the selected Zuno Edu chunk changes this boundary."
---
# Frontend behavior verification

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/FRONTEND_ROUTE_MAP.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Test observable role journeys and error states with synthetic data, not component internals. Direct API negative tests remain necessary.

## Verification requirements
Run affected component, accessibility and end-to-end flows. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
