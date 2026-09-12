---
name: zuno-nextjs
description: "Apply next.js routes and server rendering rules when the selected Zuno Edu chunk changes this boundary."
---
# Next.js routes and server rendering

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/FRONTEND_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Keep App Router routes thin; call the authoritative API through generated contracts. Set private responses no-store. Authorize Server Functions and avoid a second business backend.

## Verification requirements
Render public/private routes and prove logout invalidates private cached views. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
