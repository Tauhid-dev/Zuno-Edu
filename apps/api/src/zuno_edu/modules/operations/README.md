# Authorization and audit composition

C02 implements the approved AuditRecord/AuditService/AuditRepository boundary.
`create_app(identity_factory, request_security, audit_factory)` installs audit reads.
Construct `AuditService(AuditTransactions(database.sessions, clock, staff_approved,
CursorCodec(managed_key, clock)), clock)`. There is no default key or staff approval.

Identity factories now receive `(cookie_callback, request_id)` from trusted server
middleware. Compose a request-local `IdentityAuditWriter(clock, request_id, actor_id)`
with `Database.identity_transaction`; omit actor_id before authentication. Successful
identity events derive their actor from the verified subject. Anonymous email and
failed-login targets do not become actors. Audit writes participate in the same
transaction; failure prevents the operation or protected response from succeeding.

The domain `RECENT_MFA_MAX_AGE` is the only freshness duration. Audit service and SQL
repository independently re-resolve live session/roles/approval and check freshness,
including after SQL waits and empty results. Expiry does not revoke the session;
activity changes only last_seen_at. MFA challenge initiation/failed proof leaves
cookies intact; successful same-principal proof rotates to a freshly verified session.

Shared ResourcePolicy requires a current-principal resolver plus current relationship
ports. Feature-owned SQL adapters must implement entitlement, pinned revision/release,
active guardian/billing/assignment and learner-enrolment predicates in their own
transaction and apply the typed scope BEFORE projection/pagination. Scope values
are never client authority or cross-request cached grants. Parent education does
not imply billing. Teacher scope carries no financial capability or financial DTO.
C02 provides these interfaces; later owning chunks implement their concrete queries.
RoleGrant rejects all non-admin capability combinations. Role mutation owners must
audit rejected grant attempts and enforce identity-admin/last-admin policy.

Migration 0003 is additive and forward-only. Run via the dedicated migration owner
with CREATEROLE rights. It defines separate NOLOGIN zuno_audit_writer (INSERT only)
and zuno_audit_reader (SELECT only) roles. Provision runtime membership explicitly;
never use the migration owner/superuser at runtime. Grant only these table rights,
not DDL/UPDATE/DELETE/TRUNCATE; application roles must not own the table/functions.
The immutable trigger independently rejects UPDATE/DELETE/TRUNCATE. No ordinary
admin deletion API exists. Account role/capability/status changes revoke sessions in
that same transaction. Application rollback keeps table, trigger and audit evidence.
Retention/deletion needs the separately approved retention owner and human gates.

Audit records accept reviewed event/reason codes, opaque IDs and timestamps only.
Metadata is constrained to an empty object. No arbitrary JSON, credential, signed
URL, child work or provider payload is stored/projected. Owning feature chunks must
extend the explicit safe vocabulary when adding their events. Reads filter actor,
resource, action and a maximum 31-day interval, order by time/id, and use encrypted
cursors bound to actor, capability, filters and limit. Every successful read is audited.
