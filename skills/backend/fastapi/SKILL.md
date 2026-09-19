---
name: zuno-fastapi
description: "Apply transport/api implementation rules when the selected Zuno Edu chunk changes this boundary."
---
# Transport/API implementation

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/API_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Routers validate and dispatch use cases; no ORM/provider calls or business transitions inside endpoints. Apply session/CSRF guards and safe DTOs.

## Verification requirements
Check OpenAPI, errors, field omission and direct unauthorized requests. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
