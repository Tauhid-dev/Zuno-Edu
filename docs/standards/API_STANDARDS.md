# API standards

Version REST under /api/v1. API_CATALOG and typed schema catalog are authoritative. OpenAPI generated from implemented transport schemas must match documented contracts, then generate TypeScript clients once. Require JSON content type, reject unknown write fields and validate lengths, enums, IDs and timezone offsets. Collections use opaque cursor + limit default25/max100 and stable ordering. Return safe problem details with code, status, request_id, field errors where applicable; unauthorized resource IDs normally return indistinguishable 404.

Use 401 for absent/invalid session, 403 for capability denial, 404 for invisible resource, 409 for conflict/idempotency mismatch, 422 for invalid input, 429 with retry metadata, 503 for unavailable dependency when synchronous work is essential. Mutations carry CSRF protection and expected_version where documented. Idempotency is actor+operation scoped, stored with request hash and outcome. File/provider/webhook payloads have independent size limits. No generic unscoped admin endpoint or domain entity serialization. Contract tests assert forbidden fields are absent, not merely null.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
