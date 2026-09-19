---
name: zuno-observability
description: "Apply operational metrics/logs/alerts rules when the selected Zuno Edu chunk changes this boundary."
---
# Operational metrics/logs/alerts

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Scrub child/payment/secret payloads; use opaque correlation. Measure queue age, sync failures, mismatch, backup freshness and service latency.

## Verification requirements
Trigger alerts and inspect captured logs for forbidden content. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
