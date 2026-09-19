# Integration contracts

All external systems implement application ports in PORTS_AND_REPOSITORIES.md. PostgreSQL owns schedule, enrolment, assets and notification intent. Provider records are reconciliation inputs, never an alternative authorization system. No provider SDK enters domain or API schemas.

| Port | Adapter | Credential boundary | Durable reconciliation identity |
|---|---|---|---|
| PaymentGateway | Stripe hosted Checkout | API/worker secret only; separate signing secret | order/payment UUID, Checkout session, PaymentIntent, charge, event and refund IDs |
| LiveClassProvider | Zoom account Server-to-Server OAuth | restricted account-owned hosts; encrypted references | class UUID, provider meeting ID/UUID, desired schedule version |
| CalendarProvider | Google Calendar dedicated business calendar | restricted service account with calendar explicitly shared | class/event UUID, deterministic provider event ID, etag, desired version |
| EmailProvider | Resend | send-only domain credential in worker | notification UUID, delivery attempt, provider message ID |
| ObjectStorageProvider | S3-compatible | private bucket scoped service identity | asset UUID, immutable object key/version, checksum |

Application commands commit domain changes and an outbox row in one transaction. Worker claims durable jobs using leases; Redis only schedules wakeups. Each handler is idempotent against aggregate ID and desired version. Retries: 1m, 5m, 15m, 1h, 6h with jitter; honor provider Retry-After and stop on non-retryable configuration errors. After five failures mark attention required and alert operations. Manual retries require operations privilege and reason; do not copy sensitive payloads to logs.

Before repeating an ambiguous creation timeout, search/read by stored external ID or deterministic correlation. If the provider cannot reconcile an unknown result, quarantine the operation for operator resolution; do not blindly duplicate a payment/meeting. Provider binding stores desired_version, applied_version, status, last_error_code, attempt_count and last_checked_at. Out-of-order jobs always re-read current desired state; deleted/cancelled domain records retain tombstone bindings until confirmed remotely removed.

Integration tests use port fakes for services, HTTP contract fixtures for adapters, and gated sandbox checks for real credentials. Failure/replay tests must prove one intended effect and no cross-role leakage. See individual architecture documents for operation semantics and DESIGN_INPUTS.md for dated primary sources.
