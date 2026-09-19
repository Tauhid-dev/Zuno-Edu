---
name: zuno-stripe
description: "Apply stripe checkout, refunds and reconciliation rules when the selected Zuno Edu chunk changes this boundary."
---
# Stripe Checkout, refunds and reconciliation

## When to invoke
Load when declared by the selected chunk or when its changed files directly affect this capability.

## When not to invoke
Do not load for unrelated changes or use this skill to expand the selected chunk.

## Required context
Read the active manifest and `docs/architecture/BILLING_ARCHITECTURE.md`, plus the requirement IDs it names. Paths are relative to repository root. Repository AGENTS.md governs workflow.

## Rules and implementation standards
Use one-time AUD server-priced Checkout, signed server verification, durable idempotency and seat/refund locks. Unknown outcome must reconcile before retry.

## Verification requirements
Test last seat, late payment, duplicate webhook and concurrent partial refunds. Record actual results and evidence in the chunk handoff; planned checks are not passes.

## Common failure conditions
Stop affected work for a material blueprint conflict. Reject silent scope reduction, undeclared durable contracts, weakened authorization, or assertions of completion unsupported by fresh master evidence.
