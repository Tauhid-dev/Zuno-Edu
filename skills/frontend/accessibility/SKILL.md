---
name: zuno-accessibility
description: "Apply accessible interaction implementation rules when the selected Zuno Edu chunk changes this boundary."
---
# Accessible interaction implementation

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/FRONTEND_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Use semantic labels, focus management, error summaries, reduced motion and non-color status. Video publication requires captions/transcript.

## Verification requirements
Run axe and keyboard/screen-reader checks for changed journeys. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
