---
name: zuno-frontend-api-integration
description: "Apply api queries, forms and mutations rules when the selected Zuno Edu chunk changes this boundary."
---
# API queries, forms and mutations

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/API_CATALOG.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Use generated client and actor-scoped cache keys; invalidate after mutations and clear on logout. Treat 401/403/404 distinctly without revealing hidden resources.

## Verification requirements
Test failed/duplicate mutations, validation and stale permission responses. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
