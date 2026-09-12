---
name: zuno-security-review
description: "Apply independent access/security review rules when the selected Zuno Edu chunk changes this boundary."
---
# Independent access/security review

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/SECURITY_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Trace each data path API→service→query→DTO; inspect authorization negatives and leaked fields. Classify Critical/High/Medium/Low with concrete evidence.

## Verification requirements
Answer required blueprint review questions and recheck fixes; no Critical/High at handoff. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
