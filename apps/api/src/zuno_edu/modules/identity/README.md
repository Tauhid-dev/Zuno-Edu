# Authentication composition

This module owns C01 authentication, sessions, staff MFA and adult recovery. Registration,
guardian provisioning, staff approval and audit persistence stay with their owning chunks.
The opaque Account UUID is the student's non-public username after guardian credential
provisioning; accounts without a credential, adult account UUIDs and StudentProfile IDs are
not alternate login identifiers. Future StudentCredentialsView must return this same value.

Compose AuthenticationService per request, passing its cookie callback from the HTTP
router. Use Database.identity_transaction with the same injected Clock, an AuditWriter
and IdentityNotificationWriter. Audit writes share the identity transaction; absent
writers fail closed. The deployment must supply current staff-approval policy,
breached-password screening, Redis and versioned managed keys. No default grant or
development secret enables these routes. create_app(factory, request_security) installs
the catalog routes; unconfigured create_app retains the health-only foundation.

GET /api/v1/account/session bootstraps a signed HttpOnly browser cookie and a readable
CSRF cookie even when it returns 401. Mutations require its CSRF value in X-CSRF-Token
and the configured HTTPS Origin. Session and limited-setup cookies are Secure, HttpOnly,
SameSite=Lax, host-only and path /. Only SessionView selects a role landing.

Recovery intent stores recipient/token/purpose in the approved encrypted token payload.
The durable identity.email_requested event carries only token_id; the later email
worker resolves that reference and decrypts with the token-ID-bound context. It must
recheck purpose, expiry, consumption and current account before delivery. There are
no provider calls in the authentication transaction, and no secret in the outbox.

All competing identity changes acquire Account before credentials, session, token or
MFA rows. Read current state and time after acquiring that lock. Failed/uncertain
commits never issue a browser cookie or return MFA provisioning secrets; enrolment
retries use the retained keyed digest and never cache the provisioning response.

Migration 0002 is additive and forward-only. Roll back the application without dropping
identity state. The migration installs citext and requires extension-creation privileges.
