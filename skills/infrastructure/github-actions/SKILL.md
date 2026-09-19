---
name: zuno-github-actions
description: "Apply continuous integration workflows rules when the selected Zuno Edu chunk changes this boundary."
---
# Continuous integration workflows

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/DEPLOYMENT_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Pin actions to reviewed commit SHAs, minimal permissions, no production secrets on fork PRs. Build/test/scan before human deployment approval.

## Verification requirements
Verify failure gates, permissions and artifact provenance. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
