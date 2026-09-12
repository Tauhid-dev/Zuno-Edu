---
name: zuno-api-design
description: "Apply durable api contracts rules when the selected Zuno Edu chunk changes this boundary."
---
# Durable API contracts

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/API_CATALOG.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Follow versioned REST schemas, bounded pagination, idempotency and safe error codes. Changed durable contract requires blueprint update under authorized scope.

## Verification requirements
Compare generated OpenAPI/client types and request/response tests. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
