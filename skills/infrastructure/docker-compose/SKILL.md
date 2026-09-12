---
name: zuno-docker-compose
description: "Apply local/staging/vps service topology rules when the selected Zuno Edu chunk changes this boundary."
---
# Local/staging/VPS service topology

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Expose only Caddy; keep database/Redis private and persist required volumes. Startup ordering is not readiness; migrations run once separately.

## Verification requirements
Validate topology/readiness, restart behavior and persistence. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
