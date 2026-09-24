# Frontend state and API model

Status: DRAFT. Scope version 1.0; architecture version 1. This is a documented client contract model, not implemented product code. Exact operation and component bindings are in [frontend-catalog.json](frontend-catalog.json) and [FRONTEND_BACKEND_MAPPING](FRONTEND_BACKEND_MAPPING.md); backend fields remain authoritative in [backend-catalog.json](backend-catalog.json).

## State ownership

| State class | Owner and storage | Examples | Forbidden use |
|---|---|---|---|
| Authoritative domain state | PostgreSQL through the documented API | Enrolment/payment state, roles and links, marks, releases, schedule, capacity, file readiness, completion | Browser calculation or optimistic claim of business success |
| Browser server-state cache | Actor-scoped, in-memory TanStack Query v5 cache | Current permitted DTO pages, current session identity, own work/progress | Shared family/teacher cache, localStorage persistence or a parallel entity database |
| Ephemeral presentation | React component state | Open dialog, active tab, expanded module, selected returned row | Treating a selected ID or hidden menu as authorization |
| Unsaved form state | Component memory with dirty/version tracking | Feedback draft, quiz selections, profile change, submission text | Persisting child work or passwords in localStorage, overwriting a new server version silently |
| Navigable filter state | Validated URL query/path fields | Bounded dates, cursor, selected course/cohort/lesson and presentation tab | Secrets, child names, submission bodies, MFA token, signed URL or provider host credential |
| Security context | Server-issued secure cookie plus limited in-memory safe response data | Full SessionView, CSRF token, temporary MFA challenge/setup context | JavaScript-readable session bearer token or client-minted role/scope |
| Provider/storage handoff | Short-lived, no-store response used immediately | Checkout URL, live class handoff, download/upload ticket | Permanent bookmark, durable cache, analytics event or authority for later unrelated actions |

The only durable identity authority is the backend session and current relationships. A frontend query key is a cache partition, not an access grant. Reloading or modifying a path cannot change ownership or privileges.

## Typed transport and request construction

Implement each reviewed API operation through a generated typed client built from the authoritative OpenAPI/schema contract. Feature code imports named operation functions and their generated DTOs; it does not create ad-hoc endpoint strings, duplicate handwritten request interfaces or serialize an ORM/domain object. Generated validation checks shape, types, closed enums, nullability and field constraints. Business eligibility is still checked by the API.

The client separates path, query, header and JSON body fields exactly as documented. It sends JSON only where a body exists; 204 Empty responses are not parsed as JSON. A required nullable response field must remain present with null when unavailable. In PATCH, omission means unchanged and an explicit null clears a nullable value. Unknown fields are rejected. URL query state is parsed before use; pagination defaults to 25 and never exceeds the declared 100 limit.

Path IDs come from route context matched against an authorized read or from a selected returned row. Related IDs come from returned DTO relationships, such as course.id before loading public cohorts, payment.enrolment_id for an eligible hold cancellation, and a submitted work record before assessment. User-facing selectors show permitted names/titles. Teacher assignment uses the education-safe candidate API; it never uses the private identity directory under an education-only session or asks a user to invent an opaque ID.

Native fetch uses same-origin credentials. The shared transport attaches the current CSRF token to state-changing browser calls and honors backend Origin checks. It never exposes the cookie value. `If-Match` carries the documented current aggregate version, and `Idempotency-Key` carries a stable key for the same logical request where required. Current-session logout and own-session revocation follow their explicitly idempotent no-version contracts. No generic helper silently drops a required header.

## Query identity, isolation and invalidation

A private query key has the logical shape `[apiVersion, principalId, role, privilegeFingerprint, operationId, normalizedPath, normalizedFilters]`. The privilege fingerprint describes the current safe SessionView partition; it grants no authority and contains no secret. Resource-specific keys include student/enrolment/cohort/session IDs where relevant. A parent changes child context by selecting another authorized returned child, which changes the relevant keys. A teaching cohort switch never reuses an unrelated learner page.

Server-side query clients are created per request. Browser query data remains in memory and is cleared on logout, account/role change, invalid session or terminal access denial affecting that resource. No private response uses CDN/static/shared Next.js caches. A revoked guardian/assignment response removes the inaccessible data rather than showing stale content with a warning. Cross-tab logout can broadcast a nonsecret invalidation signal; no tokens or private DTOs are broadcast. A browser back navigation after logout must not restore a visible private record.

Public queries are separately keyed by publication context and permitted filters. Public data must never hydrate private cache entries. Cached public timetables may assist browsing but the checkout/join API checks current state. A child, teacher or finance record cannot be prefetched because it appears in a navigation manifest alone.

Mutations invalidate the smallest complete set of affected owned queries:

| Successful mutation | Required invalidation/refetch |
|---|---|
| Parent profile/email/preferences | Own profile and session identity where changed; no other-family cache |
| Child create/edit/age/credentials | Own family linked-child list, that child's profile, affected enrolment eligibility; credential reset removes affected session assumptions |
| Consent acknowledgement | Own acknowledgement set and gated checkout eligibility |
| Checkout/hold cancellation/payment retry | Own payment, eligible enrolment and public cohort availability; payment status still comes from server verification |
| Lesson/activity or quiz/submission action | Own work/attempt/activity state, enrolment progress and relevant dashboard counts; no invented completion |
| Attendance/reschedule/teacher assignment | Authorized session/cohort schedule, attendance/roster and affected progress; no broad private prefetch |
| Marking/feedback release or withdrawal | Permitted work/result/feedback/progress views and relevant notices; remove withdrawn learner projection |
| Course/revision/publication | Draft/current revision and related permitted catalogue views; cohort pins are not changed in client state |
| Refund/paid exception/price | Finance-authorized payment/refund/reconciliation/report views and server-reported entitlement outcome |
| Notification read | Own inbox and own unread count only |
| File confirmation/deletion | Owning asset metadata and draft attachment list; never mark ready before server response |
| Role/account/guardian/billing grant | Current actor identity/navigation when affected and invalidated protected queries; backend revocation remains immediate |
| Settings/integration retry | Authorized setting/provider/job view; no fabricated healthy state |

Mutation responses may replace the exact affected DTO under its current actor/resource key. Do not optimistically change price, payment, seat availability, attendance evidence, grades, release, certificate, role or file readiness. A notification read indicator may update optimistically because it is reversible and recipient-owned, but must roll back on rejection and never suppress a server error.

## Errors, retries and conflict recovery

| Outcome | User-visible behavior | Client action |
|---|---|---|
| 401 | Session expired or sign-in required | Clear private state; retain only an allowlisted nonsecret return path; restart the appropriate authentication flow |
| 403 | This account lacks the capability | Hide the unavailable action/section and clear its data; do not retry as another role |
| 404 | Resource unavailable | Treat missing and inaccessible identically; do not expose inferred existence or search a broader endpoint |
| 409 version conflict | A newer version is available | Preserve unsaved draft in memory, refetch current safe DTO and require deliberate review/reapply; never auto-overwrite |
| 409 lifecycle/idempotency/eligibility | Specific bounded action cannot complete | Show stable code's safe explanation and allowed next action; same-body idempotent retry only where appropriate |
| 422 | Field validation failed | Show error summary and field associations; focus first invalid field; retain nonsecret draft |
| 429 | Too many requests | Honor retry metadata/countdown; do not tight-loop or switch identity to bypass limits |
| 503/network failure | Service/provider temporarily unavailable | Distinguish unknown mutation outcome from rejected request; use status/refetch or the same idempotency key |

Only safe read requests receive bounded automatic retries, at most two with backoff; never retry 401/403/404/422. Respect Retry-After. Financial, submission and privileged mutation retries are explicit and preserve the original idempotency key/body. A timeout does not prove failure and is never a reason to start another checkout/refund blindly. Structured errors expose code, message, request_id, optional field_errors and retry_after_seconds, not raw provider responses or stack traces.

Each feature has loading, empty, denied, validation, stale/conflict, retryable failure and authoritative success states. Empty is contextual: a new family may have no children, a teacher may have no current assignment, a learner may have no released lesson, and a payment history may be legitimately empty. No empty state offers an action unavailable to that role. Polling pauses when the page is hidden, access expires or the result is terminal, and has a visible manual retry path.

## Authentication and MFA state machine

Sign-in consumes AuthOutcomeView as a discriminated response:

1. `authenticated`: session is present, challenge/setup are null. Install the safe actor context and enter the authorized role route.
2. `mfa_challenge`: only the five-minute challenge token is present. Render TOTP/recovery-code verification. No teacher/admin portal query runs yet.
3. `mfa_setup_required`: only the ten-minute restricted setup token is present. Enter the role-neutral /mfa-setup route; no portal authority exists until confirmation succeeds.

Staff invitation acceptance returns StaffSetupSessionView and follows the same limited setup path. Enrollment returns a one-time provisioning URI; confirmation returns MfaActivationView with full session and once-only recovery codes. Preserve these sensitive values only in memory, omit them from analytics/error reports and remove consumed URL tokens from browser-visible history. A refresh that loses limited context restarts sign-in/invitation handling safely rather than persisting a seed or bypassing MFA. TOTP and recovery-code modes have appropriate input validation; a recovery code must not be forced through a six-digit widget.

The browser may show `expires_at` for clarity, but backend expiry/replay checks decide validity. Current backend session idle limits are 30 minutes for staff and 12 hours for parent/student, with a seven-day absolute maximum. The UI does not extend these limits locally. MFA challenge/setup expiry and attempt limits follow SECURITY_ARCHITECTURE. Lost-factor support does not expose a password-only disable-MFA button. Logout, credential reset, role change and suspension flush stale client authority.

## Editable work and release states

Use generated schemas for parent child forms, preserving required name/age and optional school. Store unsaved form drafts only in component memory. Warn before leaving significant unsaved work, without blocking ordinary browser accessibility controls. Explicit saves send the displayed server version. A 409 retains the draft while fetching the current record; the user chooses whether to reapply it. No background merge silently overwrites another teacher's changes.

Quiz state is initial released definition → started own attempt → saved selections → submitted immutable attempt → released score/correctness/approved explanation. Starting and submitting use the documented idempotency. Initial question DTOs never contain keys or explanations unavailable before submission. The UI shows attempts remaining from the server and cannot grant an extra attempt. Submitted results render the approved explanation of that own attempt only.

Assignment state is authorized definition → own draft → ready file attachments → frozen submitted version → returned/new version or assessed. Late acceptance and closure come from the backend; the UI can display a due time but cannot determine permission from its clock. Parent work views show the allowed summary/released projections and do not offer submission authoring. Teacher/admin marks and feedback distinguish draft save from release, and withdrawal/correction from destructive editing. Completion percentages and override basis are supplied by ProgressView; overrides retain required evidence and do not rewrite source marks/attendance.

## Files and protected artifacts

The upload pipeline is explicit: choose a permitted file; request UploadTicketView with purpose/context/checksum/size; upload using returned method/headers; confirm via the API; poll authorized FileAssetView while quarantined/scanning; attach only when status is ready. Browser transfer completion is not scan approval. Failure/rejection leaves the draft intact and offers permitted removal/replacement. Upload tickets expire after five minutes and are never reused for another file or immutable final key.

Student limits are 25 MiB per file, 100 MiB total per submission and at most five files. Allowed formats and current archive rules are stated in FILE_STORAGE_ARCHITECTURE; ZIP rules include at most 100 entries, 100 MiB expanded and no nested archives. Frontend checks are immediate guidance; independent server validation/scanning remains authoritative. Staff resource limits differ by approved purpose. Parent and teacher interfaces do not acquire a student upload/submit capability through reuse of UploadControl.

ProtectedDownloadAction acquires a short-lived ticket only after a deliberate click. It does not persist the returned URL. Expiry or denied access requires a new authorized issuance, not direct reconstruction of a bucket path. Certificate status is respected before requesting a current document. Generic learning-file endpoints reject financial_document and financial_export; parent receipt retrieval uses own billing-family operations, and administrative finance exports use their dedicated status/download APIs.

Finance export UI handles every ExportView state: requested, processing, ready, failed and expired. It polls the finance-authorized status operation without requiring a ready asset. A ready, unexpired state enables the finance-only download operation; failed renders its sanitized failure_code; expired offers a new export request only if still authorized. A successful export creation alone is not a downloadable file, and the UI never routes around the dedicated grant using a generic file ID.

## Payments, live classes and operational requests

Checkout sends the selected authorized child/cohort and current required policy IDs, never an amount. Preserve the server-returned payment/enrolment references with an allowlisted return path. On return, read PaymentView and show pending, succeeded, failed, expired, refunded or exception as supplied. Poll a pending payment with bounded backoff, then offer manual refresh; do not activate learning from a redirect, browser receipt or client success flag. Retry uses the eligible payment checkout operation and its stable logical idempotency key.

Finance actions display server amounts and refundable balance constraints. Full/partial refund explicitly declares KEEP or CANCEL educational disposition. Late-paid exception resolution ALLOCATE/REFUND includes version and idempotency preconditions. Show pending/unknown outcome until the backend proves it; no optimistic revenue/refund or seat allocation. Neither teacher nor student features import these workflows.

Schedules display UTC instants in the chosen IANA zone while retaining the original scheduled zone label. Display-zone changes do not reschedule a class. Teacher reschedule submits local intent, zone, offset, duration and reason; the server checks the 24-hour rule, DST and conflicts. Teacher start is authorized from 30 minutes before through scheduled end; learner/guardian join from 15 minutes before through end. Show server-returned eligibility and handle window/cancellation/provider errors. Host/join URLs remain transient and excluded from analytics.

Events/announcements use the exact Audience target and role-filter schema. The client can preview the selected target description; it cannot claim a recipient count or enumerate recipients without a documented API. Settings use the closed reviewed key/value/privilege/approval catalog, with masked provider references and safe status. Accepted background actions show the authorized job status; status polling does not grant the user worker identity or access to payloads. No frontend sends a worker queue message or calls provider webhooks.

## Required state/contract verification

Test generated contract drift and actual request headers/body separation; 204 handling; nullable fields; unknown enum rejection; actor/role/child/cohort cache partition; logout/back-navigation and revoked relationships; server/client hydration without cross-request data; MFA challenge/setup gating; stable idempotent retry after unknown outcome; conflict reapply without overwrite; all file scan states; payment return without false activation; release withdrawal; finance export failed/expired states; typed audience filters; and accessible loading/error/focus behavior. The frontend mapping must contain every declared component-operation pair and copy the reviewed backend service, objects and ports exactly.

## Read prerequisites and least-data adapters

Forms load their declared selector/current-version operations before enabling dependent writes. Fresh route entry cannot depend on a prior page cache or a person typing opaque identifiers. Use the exact aggregate version declared by each mutation; relationship, account, file and retention tokens are not interchangeable.

All staff MFA enrollment uses the role-neutral `/mfa-setup` route. The limited token is enough to enter enrollment; no API-AUTH-ME full-session guard runs first. Do not infer role/account by decoding the opaque token. Activation returns the full SessionView used for the role landing. Staff invitation and login setup-required outcomes use this same route.

ScheduleView explicitly accepts PublicSessionView or ClassSessionView. The public branch renders only id/start/end/timezone. Type narrowing is required before private title/status/integration/action fields; no invented private defaults. Public schedule actions are optional callbacks supplied by the course/cohort controller.

DownloadHandoff is a presentation-only discriminated union: `{kind: ticket, ticket: DownloadTicketView}` or `{kind: issued_url, url: ApprovedHttpsUrl, label: string}`. File/certificate/export adapters wrap a freshly authorized ticket. A receipt/invoice adapter refetches the authorized receipt/document list on click, selects the requested document and uses only its nonnull download_url. Null means not ready. It must not fabricate ticket expiry, filename or MIME metadata. Both variants use returned HTTPS URLs immediately without persistence; a failed/expired link requires fresh authorized issuance. This shared primitive imports no financial model or API client.

## Exact first-write and delivery-state reads

Attendance, assessment and assignment-delivery closure distinguish authorized absence from an existing row. Attendance uses the exact-student filtered session read; an empty result is absence only after current session/cohort authorization. AssessmentStateView.assessment=null denotes no mark row for an authorized frozen submission. AssignmentClosureView.rule_exists=false and version=null denote no delivery-rule row, independently of the assignment definition version. Create with exactly If-None-Match:* or update with exactly If-Match containing the returned positive row version; never send both, infer absence from an error, or invent version 1. Refetch after concurrent creation or stale updates.

The standalone admin asset desk offers internal/public_asset creation only, with context_id from the authenticated SessionView.user_id. Curriculum resource uploads live in the writable revision resource editor; the admin desk never creates student submissions. Existing asset inspection/deletion remains capability-scoped and uses the returned FileAssetView.version.

## MFA enrolment retry exception (architecture 2)

For API-AUTH-MFA-ENROL, [ADR 0004](ADR/0004-mfa-enrolment-retry.md) overrides generic same-result replay. ADR 0004 exception: validate current account/session or limited setup context, browser, purpose, expiry, attempts and CSRF/Origin before idempotency. First committed enrolment returns MfaSetupView once; same key/body after commit returns secret-free 409 MFA_REPLAY; changed body returns 409 IDEMPOTENCY_CONFLICT. Serialize duplicates, restart and confirmation; rollback permits retry, uncertain commit requires authoritative lookup. Keep only safe principal/operation/key, keyed canonical-body digest and outcome metadata for 7 days; never store/replay the URI or recoverable setup token. A lost response requires explicit restart with fresh permitted password authentication and a new key, invalidating pending setup credentials atomically without removing an active factor before replacement confirmation. Existing lifetime, attempt and abuse limits apply.
