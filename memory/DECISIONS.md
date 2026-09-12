# Durable decisions

- Scope 1.0 is a complete launch baseline; bootstrap contains planning/tooling only. See ADR/0001.
- One modular OO backend, one PostgreSQL authority, five frontend surfaces and generated API contracts.
- Course revisions are reusable and cohort-pinned; sessions are individual authoritative occurrences.
- Child name and age are required; declared age plus observation date avoids mandatory DOB; school optional. See ADR/0002.
- One-time AUD Stripe Checkout, explicit refund/access disposition, no subscriptions/instalments/discounts.
- Teacher assignment constrains educational access; teacher principal never has finance capability.
- PostgreSQL outbox/inbox and provider binding state support idempotency/recovery; Redis is disposable. See ADR/0003.
- Zoom native handoff, Calendar mirror, Resend transactional messages and S3-compatible private immutable assets are behind ports.
- Completion certificate is the defined achievement; no gamification or automatic recording.
- Real Codex skills use category/name/SKILL.md; deterministic catalogs and file references replace embeddings.
- Fresh origin/master plus authenticated merge evidence outrank manifests/progress caches; human merge locks the approved plan.
