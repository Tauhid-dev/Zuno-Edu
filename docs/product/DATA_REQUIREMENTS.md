# Data requirements

Status: DRAFT. This is a technical minimization and retention proposal, not legal advice. Required human approval of policy/retention wording is tracked by HG-LEGAL. Production must not claim approval or silently publish placeholder text.

## Minimum child profile

| Field | Required/type | Purpose and validation | Readers/writers | Retention/security |
|---|---|---|---|---|
| student_id | System UUID | Stable opaque identity; never sequential public identifier | Scoped system operations | Educational record class; not a public lookup key |
| first_name | Required string, 1–80 Unicode characters after trim | Required student name; single-name children are supported | Guardian/admin edit; child own view; assigned teacher display | Child profile; no public indexing |
| preferred_name | Optional nullable string, 1–80 characters | Comfortable classroom display; fallback to first_name | Guardian/admin and student own limited edit; assigned teacher view | Child profile; sanitize as text |
| last_name | Optional nullable string, 1–80 characters | Optional family preference for records/certificate | Guardian/admin; student own view; teacher only if approved display requires it | Never required by schema or certificate issuance |
| display_name | Derived | preferred_name or first_name; append optional last_name only with approved display setting | Scoped viewers | Avoid exposing full legal name by default |
| age_years | Required integer, 4–18 inclusive | User explicitly provides child's age; published course band determines eligibility | Guardian/admin edit; child own view; assigned teacher read | Child profile; not computed from guessed DOB |
| age_recorded_on | Required server date | Records when adult confirmed numeric age | Guardian confirmation generates date; admin correction audited | Reconfirm at next enrolment if >180 days old |
| school_name | Optional nullable string, 1–160 characters | Family-provided educational context and support, never prerequisite | Guardian/admin; child own view; not in default teacher projection | Child profile; no school contact lookup/integration |
| school_year | Optional nullable enum | Tailoring age-appropriate learning, e.g. Foundation/Year 1–12/other/not-specified | Guardian/admin edit; assigned teacher read | Child profile; avoid assuming school or curriculum system |
| interests | Optional bounded list of approved topics, ≤10 selections | Prepare relevant teaching examples | Guardian/student own edit; assigned teacher/admin read | Child profile; no open-ended sensitive notes |
| prior_experience | Optional enum none/some/experienced/prefer-not-to-say | Adjust teaching support | Guardian/student own edit; assigned teacher/admin read | Child profile; educational purpose only |
| family_id | System UUID, required relationship | Administrative ownership context | Authorized identity/education operations | Never treated as a substitute for guardian authorization |
| guardian links | At least one active verified adult for active child | Authorizes adult educational access | Admin verifies/revokes; parent sees own links | Relationship audit retained separately |
| login identifier | System-generated non-public alias, optional until provisioned | Independent student access without email | Guardian provision/reset; student uses alias | Credential class; not public name lookup |

No date of birth, child address, personal email, phone, health diagnosis, government identity document, biometric identifier or arbitrary sensitive learning-notes field is collected at launch. The registration UX explicitly labels name and age as required and school as optional. Blank optional strings normalize to null. Unknown fields are rejected. Numeric age records an adult assertion on a known date; the platform must never fabricate a precise birth date or silently increment age at an invented birthday.

The 4–18 technical registration bounds are proposed for school-age service and must be confirmed under HG-AGE alongside actual course bands before production. The schema and rules are explicit; approval config supplies permitted launch bands rather than requiring later architecture redesign.

## Other required records

| Record | Minimum data and purpose | Access boundary |
|---|---|---|
| Adult account | Name, normalized verified email, optional phone, password hash, role grants, session status, MFA state where privileged | Self account operations or explicitly privileged support; teachers never receive guardian contact through learner profile |
| Family and membership | Opaque family ID, adult memberships, primary/account holder marker, billing authorization, lifecycle | Active adult member or scoped identity/finance administration |
| Consent/policy acknowledgement | Policy ID/version/hash/effective date, actor, scope, timestamp and action context | Adult own records and authorized administration; no unnecessary fingerprint/device tracking |
| Teacher profile | Professional name, optional approved biography/photo, teaching qualifications summary, lifecycle | Operational profile admin only; assigned/public projections whitelist fields |
| Curriculum | Versioned program/course/module/lesson/block IDs, validated payloads, required flags and publication/release state | Public summary vs enrolled/assigned/admin projections |
| Cohort/session | Pinned course revision, capacity, schedule UTC/IANA timezone/local intent, teacher assignment, status | Public safe schedule only; learner roster and meeting data separately protected |
| Enrolment | Child/family/cohort, course version, lifecycle, reservation expiry, consent/order linkage, completion | Authorized guardian, own learner, assigned teacher educational projection and authorized admin |
| Attendance/progress | Session/student status, actor/reason/revision; item completion and calculated policy outcome | Own student, authorized guardian, assigned educator and education admin |
| Quiz/assignment/submission | Published question/rubric version, own responses, attempt state, immutable file/version references and timestamps | Answer keys/draft marking educator-only; submitted student content never peer-visible |
| Assessment/feedback | Submission/rubric revision, outcome/score, private draft/release state, author and history | Release gates family/student; assigned educator/admin draft access |
| Certificate | Unique serial, enrolment/course version, permitted student display name, completion/issue/revoke timestamps and PDF asset | Student, authorized guardian and authorized education admin; no public child-name directory |
| Order/payment/refund/document | Integer AUD amounts, tax/price snapshot, provider identifiers, lifecycle, ledger and actor/reason | Billing-family adult or finance admin only; no card PAN/CVC stored |
| Notification/delivery | Recipient, audience, event ID, safe summary, read/delivery state, attempt history | Own recipient; operations admin redacted delivery view |
| File asset | Owner/purpose/audience, expected/detected type and size, checksum, immutable storage key, scan/lifecycle state | Access derives from linked resource and actor scope; private object storage |
| Audit record | Opaque actor/resource references, action, time, reason, safe before/after metadata, correlation ID | Audit admin, immutable; no tokens, full work content or payment credentials |
| Privacy request | Adult requester, verified relationship, request kind/status, decision/evidence refs and completion time | Identity/privacy operations admin; exports enforce resource scope |
| Operational setting/approval | Typed nonsecret value or secret reference, version, approving actor/time and policy/config gate | Operations/admin capability; secrets not returned |

## Proposed retention classes

These are explicit implementation defaults proposed for human review. HG-LEGAL must approve a versioned retention matrix before production; configured legal hold overrides scheduled erasure without permitting wider access.

| Class | Proposed retention | Deletion/archival behavior |
|---|---|---|
| Child profile and educational records | Active relationship/service plus 24 months after last enrolment ends | Verified request may trigger earlier permitted erasure/anonymization; retain only records required by approved hold/policy |
| Student uploads | Same linked educational-record retention | Delete object and tombstone metadata; audit retains safe references only |
| Unfinalized uploaded objects | 24 hours | Orphan cleanup checks references before deletion |
| Account/session/recovery | Active account; expired/revoked session metadata 30 days; unused recovery token 30 minutes | Purge tokens immediately on consumption; hashes only; support lifecycle does not erase required finance/audit |
| Optional contact enquiries | 90 days after closure | Delete body/contact unless explicitly converted to an authorized service-support record |
| Transactional delivery logs | 90 days | Redacted operational metadata only; deduplication intent key retained as safe hash for one year |
| Ordinary application/error logs | 30 days | Redact at source and remove according to log store policy |
| Security/admin audit | One year | Append-only access; privileged export is audited; financial audit follows financial class |
| Orders/payments/refunds/invoices | Proposed seven years after transaction pending finance/legal approval | Immutable retained financial evidence; minimize/remove unrelated child educational details |
| Certificate issuance metadata | Seven years proposed, subject to approval | Revoked/erased certificates remain represented by safe serial/status where justified; child display data can be anonymized |
| Database backups | Daily base backups 35 days with encrypted WAL/PITR window seven days | Expire automatically; approved erasure is re-applied if restoring older backups before service reopening |
| Object versions/backups | 35 days after object deletion | Private, encrypted and restore-only; lifecycle cleanup respects legal holds |

Deletion is a controlled workflow: verify requester and resource authority, resolve retention/hold, schedule purge/anonymization, revoke access, delete eligible objects and record safe evidence. The system must not delete records merely because an account is suspended, nor keep all child data indefinitely because one payment is retained. Production copies to developer machines are prohibited; staging uses synthetic data.
