# ADR 0004 — One-time MFA provisioning and safe retries

Status: PROPOSED; scope 1.0, architecture 2. Human merge of the identified planning
PR is required before implementation. Supersedes only the generic enrolment replay
promise in architecture 1; ADRs 0001–0003 and other operations remain unchanged.

## Authority and problem

On 2026-09-24 the user instructed “continue” after the task requested authorization
for an architecture correction defining safe enrolment retries and recommended a
secret-bearing replay exception. Source task:
`01a0d0ec-832c-7042-80bb-d9b872b3bf66`.
This authorizes this proposal, not implementation before human merge.
The previous approved baseline is master
`f1f18fbd0e77bd305cd71d1ca6aa2d17d773bad3`, scope 1.0 / architecture 1,
planning PR #2; its immutable lock remains available in that Git tree.

`API_AUTH_MFA_ENROLRequest` required same-body result replay for seven days.
`MfaSetupView` contains a setup token and provisioning URI, while security requires
the URI to be returned once and setup tokens to be stored hashed. Exact response
replay conflicts with one-time return. Independent contract review confirmed this
in ZE-P02-C01. Encryption of a replay cache does not resolve repeated disclosure.

## Decision

Only `API-AUTH-MFA-ENROL` has this exception to generic safe-result replay:

1. Before any idempotency lookup or result, revalidate current trusted staff
   identity, account state, browser binding, setup purpose/expiry/attempt limits
   or full staff session with recent password reauthentication, plus CSRF/Origin.
   Invalid authentication keeps its documented denial and reveals no key history.
2. Serialize enrolment/restart and confirmation on the same account/factor state.
   All MFA repository operations acquire the account row lock before challenge or
   factor locks, including when no factor exists, then revalidate authorization
   and lifecycle state inside the transaction before replay or mutation. This
   shares the Account lock used by status/role writes; their existing membership
   lock before Account ordering is preserved (MFA paths never acquire that lock).
   Reserve principal + operation + key with a keyed canonical-body digest
   (including every request field). Passwords and setup tokens must not become
   offline-verifiable unkeyed body hashes. Keep the digest key outside the DB;
   retain versioned verification keys for the seven-day metadata window. Existing
   request_hash bytes encode a versioned format, digest-key version and keyed
   digest; result_ciphertext is NULL for this operation. Unknown/unavailable key
   versions fail closed; they do not turn a duplicate into a new enrolment.
3. The first successful transaction persists encrypted pending factor material,
   hashed setup credentials, safe idempotency metadata and required audit
   atomically. Only its original response may emit `MfaSetupView` with token and
   URI, over HTTPS/no-store. Never persist, log, queue or cache a replayable
   response, plaintext seed, provisioning URI or recoverable setup token.
4. A duplicate with the same key and body after commit returns secret-free
   `409 MFA_REPLAY`, with no new factor/token, expiry extension or attempt reset.
   Different body under that key returns `409 IDEMPOTENCY_CONFLICT` without effects.
   Concurrent duplicates wait for the transaction outcome: after rollback one may
   execute; after commit all others receive the safe replay error. Connection loss
   or uncertain commit never authorizes another successful response under that key.
5. Keep only the safe key/digest/outcome tombstone for seven days. Neither the
   provisioning response nor its secrets are replayable during that window or
   after expiry, consumption, suspension, role revocation or account closure.
   Metadata expiry does not authenticate a request or revive pending credentials.
6. If the client retained its original URI and token, it can continue confirmation
   within their original limits. A lost response/refresh requires an explicit
   user restart, never an automatic new-key retry. Restart requires a newly
   password-verified setup context from login, or the existing permitted full
   staff session with fresh password reauthentication, and a new idempotency key.
   An accepted invitation is not consumed again; its newly set password supports
   the ordinary limited-login setup flow.
7. A restart atomically invalidates the previous pending factor and all dependent
   pending setup credentials before installing the replacement. A prior active
   factor and its recovery codes stay valid until successful replacement proof;
   password-only callers cannot revoke or replace an active factor. Confirmation
   and restart races have one serial outcome; obsolete proofs cannot activate a
   replacement. No full privileges are issued before valid MFA confirmation.
   Apply existing abuse controls, five-failure limit and ten-minute setup bound;
   replay/restart never refreshes limits on an existing setup context.

“Returned once” means at most one successful emission from the committed operation,
not a promise of network delivery. A crash between commit and delivery intentionally
requires explicit restart. Error envelopes contain only safe code/message/request
metadata and no account existence, token, URI, seed or recovery code.

## Impact and alternatives

Requirements AUTH-001/002/003, ADM-001 and TCH-001 retain mandatory MFA, revocation,
audit and role separation. No launch requirement, role, capability, endpoint or
required response field is added or removed. The change removes automatic
secret-bearing result replay only for enrolment and defines its loss recovery.
Scope remains 1.0; the material contract correction increments architecture to 2.

Account, MfaFactor, MfaChallenge, AuthenticationService.enrol_mfa, MfaRepository and
the existing idempotency infrastructure retain their ownership. Safe metadata uses
existing idempotency records; no new durable public object/table is introduced.
The MfaRepository contract is extended with account-scoped, row-locking methods
`get_pending_factor_for_update(account_id, setup_token_hash, browser_hash, scope)` and
`invalidate_pending_setup(account_id, scope)`; neither permits an unscoped query,
touches an active factor, or returns plaintext secret material. The pending getter
validates account, browser, setup purpose, expiry, attempts and nonconsumption of
the locked challenge and follows its exact factor_id; a latest-by-account lookup
is forbidden. Invalidation revokes pending factors and consumes all dependent
pending setup credentials under the shared lock, preserving active factor and
recovery-code state. `get_factor_for_update` is
defined to return the active factor only. Adapters must prove transactional
uniqueness and rollback. No provider, billing,
guardian/student-data projection or permission boundary changes. No product
migration is included because authentication is not implemented on the approved
base. Implementation must verify storage constraints in ZE-P02-C01.

Backend ownership remains ZE-P02-C01; StaffMfaSetup remains ZE-P09-C03. Their
dependency graph and requirement traceability are unchanged. Cross-module audit
wiring retains the existing later integration gates. The C01 partial implementation
in the original worktree is excluded from this proposal.

Rejected alternatives: encrypted seven-day response cache still returns the URI
again; redacting required fields violates MfaSetupView; silently generating a new
seed on duplicate changes the result and breaks scanned authenticators; disabling
MFA or bypassing account/browser checks weakens the approved boundary.

## Acceptance and rollout

Before completing C01, test same-key same-body replay, changed-body conflict,
concurrent duplicates, rollback, uncertain commit/lost response, secret-free
persistence/logs/errors, expired/consumed/foreign-browser tokens, suspension/role
revocation, explicit restart, prior-proof rejection, restart/confirmation races,
active-factor preservation and unchanged limits. Before completing P09 C03,
test lost-response UX, no automatic new-key retry, explicit restart, volatile
secret state and role-neutral setup without portal access.

This planning-only PR must pass plan/witness, routing, graph and workflow checks
and independent deep security review. Human merge approves the new witnessed
baseline. A fresh task then synchronizes master and reconciles authorization;
neither this proposal nor an open PR authorizes product implementation.
