---
name: zuno-secrets-and-integrations
description: "Apply provider credential boundaries rules when the selected Zuno Edu chunk changes this boundary."
---
# Provider credential boundaries

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/INTEGRATIONS.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Keep secrets in server/worker runtime, scope credentials and separate environments. Redact tokens, host URLs, signed storage URLs and raw webhook data.

## Verification requirements
Scan diff/config/bundle and test rotation plus wrong-environment rejection. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
