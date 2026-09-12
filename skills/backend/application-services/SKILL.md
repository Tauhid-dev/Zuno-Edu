---
name: zuno-application-services
description: "Apply use case orchestration rules when the selected Zuno Edu chunk changes this boundary."
---
# Use case orchestration

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/BACKEND_SERVICE_CATALOG.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Authorize trusted actor/resource relationships before work; scope queries; transact aggregate changes with outbox. Remote calls occur outside database transaction with durable intent.

## Verification requirements
Use fake ports for success, denied access, rollback and retry cases. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
