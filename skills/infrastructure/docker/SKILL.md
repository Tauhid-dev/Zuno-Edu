---
name: zuno-docker
description: "Apply container images rules when the selected Zuno Edu chunk changes this boundary."
---
# Container images

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Use pinned minimal non-root images, multi-stage build, runtime-only secrets and health checks. API and worker share artifact with separate commands.

## Verification requirements
Build/scan images; check user, permissions and absence of secrets. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
