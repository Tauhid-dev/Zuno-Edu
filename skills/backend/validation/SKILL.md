---
name: zuno-validation
description: "Apply input and domain validation rules when the selected Zuno Edu chunk changes this boundary."
---
# Input and domain validation

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DATA_MODEL.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Reject unknown write fields, invalid enums/timezones, mutable ownership and unbounded text. School stays nullable; name and declared age required.

## Verification requirements
Exercise boundary, malformed, mass-assignment and optional-field cases. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
