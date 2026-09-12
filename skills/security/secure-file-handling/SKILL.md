---
name: zuno-secure-file-handling
description: "Apply private asset lifecycle rules when the selected Zuno Edu chunk changes this boundary."
---
# Private asset lifecycle

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/FILE_STORAGE_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Authorize upload purpose, quarantine actual bytes, constrain archives and promote immutable versions. Download only CLEAN assets through fresh ownership check.

## Verification requirements
Test spoofing, oversized/hostile ZIP, overwrite race and unauthorized download. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
