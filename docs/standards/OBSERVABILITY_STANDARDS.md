# Observability standards

Log operation ID, request/correlation ID, actor pseudonymous ID where necessary, result code, duration and aggregate opaque ID; never child names/notes, password/token, email body, signed URL, raw webhook payload or card information. Use structured JSON and centralized redaction. Audit records are separate append-only security/financial history with protected reason and changed-field names; audit access itself is logged.

Metrics track latency/errors, queue age/retry, dead letters, integration sync lag, payment mismatch, rejected uploads, database pool/disk and backup age. Alerts have owner, threshold and runbook, tested before launch. Trace external calls using opaque correlation without private payload. Error reporting uses scrubbed contexts. Health readiness distinguishes fatal database/configuration faults from recoverable provider degradation. Incident evidence records user impact, recovery/reconciliation and follow-up chunk; it does not become a narrative diary in memory.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
