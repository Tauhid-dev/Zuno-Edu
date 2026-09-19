---
name: zuno-backups-restore
description: "Apply backup and recovery drills rules when the selected Zuno Edu chunk changes this boundary."
---
# Backup and recovery drills

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Restore DB/WAL and object versions into isolated environment with outbound effects disabled. Replay privacy tombstones and reconcile provider state before reopening.

## Verification requirements
Measure RPO/RTO, verify financial totals/assets and save drill evidence. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
