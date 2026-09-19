---
name: zuno-google-calendar
description: "Apply domain schedule mirror rules when the selected Zuno Edu chunk changes this boundary."
---
# Domain schedule mirror

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/CALENDAR_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Mirror individual sessions with deterministic event IDs and portal links. External edits never change authoritative domain schedule. No child roster in payload.

## Verification requirements
Test DST, etag conflict, external deletion and full resync after expired token. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
