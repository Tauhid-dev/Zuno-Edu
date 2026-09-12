# ADR 0003 — Transactional outbox and integration mirrors
Status: PROPOSED.

Use PostgreSQL outbox/inbox plus durable attempt/binding records. Redis is replaceable scheduling infrastructure, never the unique store of enrolment/payment work. Provider adapters are ports; transactions never span a database commit and a remote API. Every remote operation has a stable identity, retry policy and reconciliation path. Unknown create outcomes require lookup or operator resolution before another create.

Stripe server verification establishes payment state; enrolment capacity/access remains domain policy. Zoom meetings and Calendar events follow ClassSession desired versions. Calendar recurrence is represented as individual finite session events. Email deduplication is durable beyond provider windows. Files are quarantined and promoted to immutable versions so presigned overwrite cannot replace scanned bytes. These choices add bounded persistence records in exchange for recoverable real-world failures.
