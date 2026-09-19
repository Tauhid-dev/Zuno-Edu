---
name: zuno-oop-domain-modeling
description: "Apply entities, policies and value objects rules when the selected Zuno Edu chunk changes this boundary."
---
# Entities, policies and value objects

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/BACKEND_OBJECT_CATALOG.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Preserve aggregate invariants with meaningful methods. Prefer composition; map ORM rows outside domain. Material missing durable behavior is a blueprint conflict.

## Verification requirements
Test illegal transitions, invariant boundaries and domain import isolation. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
