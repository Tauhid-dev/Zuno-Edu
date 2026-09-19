---
name: zuno-resend
description: "Apply transactional email delivery rules when the selected Zuno Edu chunk changes this boundary."
---
# Transactional email delivery

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/COMMUNICATION_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Outbox and recipient delivery ledger govern retries/preferences. Provider 24h idempotency is insufficient for durable dedup; ambiguous old sends need review.

## Verification requirements
Test rollback/no-send, replay, recipient revocation, preferences and bounce. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
