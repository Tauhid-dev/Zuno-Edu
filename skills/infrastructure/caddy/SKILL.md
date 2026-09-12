---
name: zuno-caddy
description: "Apply https reverse proxy rules when the selected Zuno Edu chunk changes this boundary."
---
# HTTPS reverse proxy

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Terminate TLS, route /api/v1 correctly, apply safe headers/body limits and do not expose internal services. Preserve raw webhook bytes.

## Verification requirements
Check HTTPS redirects, route boundaries, request limits and certificate renewal. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
