# Security standards

Deny by default at API, use case and repository scope. Bind trusted actor from validated server session; ignore actor/family/privilege fields supplied by client. Enforce resource state and assignment as well as role. Staff MFA, secure password hashing, short privileged idle timeouts and revocation are required. Teacher principals cannot carry financial privileges. Require separate admin identity for those duties.

Protect session cookies with HttpOnly/Secure/SameSite, CSRF tokens and origin checking for writes. Rotate credentials after login/recovery and revoke on suspension/role changes. Validate upload contents, sanitize rich text, allowlist video domains and reject arbitrary embeds. Use parameterized queries, redacted logs, restricted secret injection, provider signature validation and bounded rates. Security review tests IDOR, mass assignment, stale permissions, cache leaks and webhook replay. Policy/retention/legal decisions gate launch configuration; do not claim legal compliance from technical controls.

Authority: approved scope and architecture precede this standard. Apply only to the selected chunk; verify against its acceptance criteria and record evidence in its handoff.
