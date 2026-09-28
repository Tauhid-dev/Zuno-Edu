# ADR 0005 — Fixed recent-MFA freshness and step-up

Status: PROPOSED for repository approval; scope 1.0, architecture 3.
Human merge and fresh reconciliation precede dependent C02 implementation.

## Authority and problem

On 2026-09-28, the human explicitly approved a 30-minute recent-MFA window for
ZE-P02-C02 and requested resumption on feature/ze-p02-c02-authorization-audit.
The instruction defines a fixed window from successful MFA, no activity-based
extension, no logout on freshness expiry, server-side step-up, a centralized policy
value, documentation and seven boundary tests. This ADR records that decision.
The branch is retained as explicitly requested; this PR contains the policy only.

The approved baseline is master af5dbd9cd1d1dfa75f67367d9bb4eb3931cf2ba0,
scope 1.0 / architecture 2 (planning PR #11). It requires recent MFA for protected
administrative operations, including API-ADMIN-AUDIT, without defining its age.
Thirty-minute staff inactivity and seven-day absolute session expiry are separate
existing controls and cannot supply an implicit MFA-freshness definition.

## Decision

1. Define one reusable server-side security policy value, `RECENT_MFA_MAX_AGE`,
   as 30 minutes. Endpoints and repositories consume the same policy; no separate
   per-endpoint literal, longer override or client-provided duration is permitted.
2. Freshness is evaluated from the server-recorded timestamp of the most recent
   successful MFA verification. At authorization time `now`, evidence is recent
   exactly when `0 <= now - mfa_verified_at < RECENT_MFA_MAX_AGE`. At exactly
   30 minutes it has expired. Use timezone-aware instants and an injected Clock;
   missing or future-dated evidence fails closed for protected operations.
3. User activity, session reads, idle-time refresh, cursor use and failed MFA
   attempts cannot modify the MFA timestamp or extend freshness. Authorization
   evaluates current server-side evidence, never browser claims or cached roles.
4. Expired/missing recent MFA denies the next operation that requires it before
   data access or mutation. It does not itself revoke, lock, terminate or log out
   an otherwise valid session. Ordinary authenticated operations continue under
   their existing role/resource/session rules. Account suspension, revocation,
   idle expiry and absolute expiry remain independent grounds for denial.
5. Require successful step-up MFA before retrying the protected operation. Reuse
   the existing password-login → limited MFA challenge → verified full-session
   flow and its approved TOTP/recovery-code checks. The existing session is not
   revoked merely because freshness expired or step-up failed. Successful step-up
   records the new successful MFA timestamp and starts a new 30-minute window;
   normal successful-authentication session rotation remains permitted. A step-up
   restoring the current principal's protected access must verify that same
   principal; a different-account login is not proof for the original principal.
6. Keep current account status, role/capability, staff approval, ownership, purpose,
   release/state and session revocation checks. Fresh MFA grants none of these by
   itself. Recheck current state/time after lock waits before protected reads or
   writes. Missing MFA cannot be synthesized from password-only or setup state.
7. Enforce the policy in server authorization and scoped persistence boundaries.
   Frontend freshness checks can offer step-up UX but never authorize access.
   Keep the existing `FORBIDDEN` (403) contract for insufficient recent MFA on
   API-ADMIN-AUDIT, and `UNAUTHENTICATED` (401) for invalid authentication. No new
   endpoint, response field, token kind or error code is introduced.
8. This defines “recent MFA” consistently wherever the approved contracts use
   that phrase. It does not add a freshness requirement to ordinary operations
   that do not already require it. ADR 0004 enrolment/retry rules remain binding.

## Impact, ownership and alternatives

Requirements AUTH-003/006/010/012, ADM-029 and SEC-007 retain their existing
mandatory MFA, authorization and audit intent. No launch requirement is removed,
postponed or added; scope stays 1.0 and architecture increments to 3 for the
security-contract clarification. C02 owns the reusable freshness policy and audit
boundary integration/tests. Existing AuthenticationService, Session and MFA ports
remain authoritative for successful verification. The current login implementation
calls the session-cookie callback with None when issuing a staff challenge, which
removes the ordinary browser session cookie. C02 must narrowly adapt that existing
service/HTTP flow so valid same-principal sessions and their cookies survive
challenge initiation and failed verification. Only successful verified rotation or
an independent existing session-invalidating event may replace/remove them. Test
both the HTTP cookie and persisted session behavior; do not introduce a second
login system or treat limited challenge state as a full principal.
Future admin endpoints reuse
this interpretation. Frontend mappings and dependency/chunk ordering are unchanged.

No new durable object, provider, public DTO or migration is required for freshness:
Session already records mfa_verified_at. Implementing C02 audit storage remains
in its existing scope. Do not reset stored MFA timestamps during rollout; existing
sessions are evaluated against their real timestamps. A rollback must preserve
server-side protection rather than restoring an undefined or activity-extended
window. Never relax teacher finance, family isolation or child-data boundaries.

Rejected alternatives: using last_seen_at makes activity extend MFA authority;
logging out on freshness expiry disrupts ordinary access; trusting browser time or
claims moves the boundary to an untrusted client; re-verification on every request
contradicts the approved 30-minute window.

## Required implementation proof

C02 must test API, application and scoped repository enforcement as applicable:

| Case | Required result |
| --- | --- |
| Valid evidence at 29m59.999999s | Protected access allowed only with all other permissions valid |
| Exact 30m boundary | Protected access denied; step-up required |
| Evidence older than 30m | Protected access denied |
| Missing or future MFA evidence | Protected access denied |
| Successful real step-up | New server timestamp; protected access restored for 30m |
| Ordinary authenticated operation after freshness expiry | Valid session still works when that operation does not require freshness |
| Activity before/after expiry | last_seen may change, mfa_verified_at does not; no window extension |
| Failed/replayed/foreign step-up | No new MFA timestamp or protected access; valid ordinary session and cookie retained |
| Initiating same-principal step-up | Existing ordinary session and cookie retained while challenge is pending |
| Lock wait crossing expiry | Re-evaluated current time denies protected operation |

These are required tests, not claims of implementation or passing product tests.
This proposal must pass planning/witness, routing, graph and workflow validation
and independent deep review. Record its actual PR number in scope-lock.json before
human merge. On the next run, synchronize and verify approval before C02 resumes.
