---
name: zuno-authorization-rbac
description: "Apply role and privilege enforcement rules when the selected Zuno Edu chunk changes this boundary."
---
# Role and privilege enforcement

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/AUTHORIZATION_MODEL.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Role alone never authorizes a resource. Enforce ownership/assignment/state and incompatible teacher financial role grants. UI guards are not authority.

## Verification requirements
Test every allowed role and denied role, including forged client identifiers. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
