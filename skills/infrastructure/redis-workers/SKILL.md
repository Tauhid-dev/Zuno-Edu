---
name: zuno-redis-workers
description: "Apply durable background processing rules when the selected Zuno Edu chunk changes this boundary."
---
# Durable background processing

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/INTEGRATIONS.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Redis wakes workers; PostgreSQL outbox/leases preserve work. Handlers deduplicate by aggregate/version and recheck latest desired state.

## Verification requirements
Lose Redis/restart worker mid-effect; prove recovery, bounded retry and no duplicate effect. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
