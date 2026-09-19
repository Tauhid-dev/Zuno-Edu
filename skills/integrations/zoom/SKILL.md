---
name: zuno-zoom
description: "Apply assigned live class provider rules when the selected Zuno Edu chunk changes this boundary."
---
# Assigned live class provider

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/LIVE_CLASS_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Meeting follows ClassSession version. Fetch host link only for assigned host; waiting room on, join-before-host/recording off. Do not blind-retry ambiguous creates.

## Verification requirements
Test create/update/cancel, stale jobs, expired link and unauthorized host access. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
