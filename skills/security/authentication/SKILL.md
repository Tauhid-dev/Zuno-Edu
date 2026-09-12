---
name: zuno-authentication
description: "Apply account/session security rules when the selected Zuno Edu chunk changes this boundary."
---
# Account/session security

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/SECURITY_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Use approved server sessions, CSRF/origin validation, secure cookies, revocation and staff MFA. Child account recovery goes through authorized guardian.

## Verification requirements
Test expiry, replay, suspension, recovery and session revocation. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
