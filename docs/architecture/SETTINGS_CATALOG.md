# Closed application setting catalog

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

Settings are typed approved data, never arbitrary configuration code. The following29keys are the complete launch admin-editable setting catalog. Unlisted keys and JSON value fields are rejected. `SettingValue` contains exactly the indicated `text`, `number`, `flag` or `items` field; every other field is forbidden. Integers/booleans are strict JSON types. The request path key is a closed enum restricted to the caller's exact capability.

| Key | SettingValue field | Validation | Required privilege | Human gate | Proposed default |
| --- | --- | --- | --- | --- | --- |
| child_age_min | number | integer4–18; <=child_age_max | operations_admin | HG-AGE | 4 |
| child_age_max | number | integer4–18; >=child_age_min | operations_admin | HG-AGE | 18 |
| approved_child_interests | items | Nonempty subset of artificial_intelligence,coding,robotics,creative_design,games,data,online_safety; max7 | operations_admin | HG-AGE | all seven topics |
| support_email | text | Verified monitored business email | operations_admin | HG-LEGAL | unconfigured |
| safeguarding_email | text | Verified monitored child-safety business email | operations_admin | HG-LEGAL | unconfigured |
| business_phone | text | E164 business contact | operations_admin | HG-LEGAL | unconfigured |
| policy_privacy_id | text | UUID of approved published privacy policy | operations_admin | HG-LEGAL | unconfigured |
| policy_terms_id | text | UUID of approved published terms policy | operations_admin | HG-LEGAL | unconfigured |
| policy_child_safety_id | text | UUID of approved published child-safety policy | operations_admin | HG-LEGAL | unconfigured |
| required_consent_policy_ids | items | 1–10 UUIDs of effective approved consent documents | operations_admin | HG-LEGAL | unconfigured |
| retention_matrix_version | text | Exact approved matrix version, starts1.0; maps durations below | operations_admin | HG-LEGAL | unconfigured |
| retention_child_months | number | 24; any changed approved value requires explicit scope/retention review | operations_admin | HG-LEGAL | 24 |
| retention_contact_days | number | 90 | operations_admin | HG-LEGAL | 90 |
| retention_delivery_days | number | 90 | operations_admin | HG-LEGAL | 90 |
| retention_finance_years | number | 7 | finance_admin | HG-MERCHANT+HG-LEGAL | 7 |
| retention_certificate_years | number | 7 | operations_admin | HG-LEGAL | 7 |
| merchant_legal_name | text | 1–200 trimmed legal business name | finance_admin | HG-MERCHANT | unconfigured |
| merchant_abn | text | 11 digits validated Australian Business Number or empty only when professionally approved | finance_admin | HG-MERCHANT | unconfigured |
| merchant_address | text | 1–500 approved invoice business address | finance_admin | HG-MERCHANT | unconfigured |
| tax_treatment | text | enum inclusive,exclusive,exempt | finance_admin | HG-MERCHANT | unconfigured |
| tax_rate_basis_points | number | 0–10000; consistent with approved tax_treatment | finance_admin | HG-MERCHANT | unconfigured |
| refund_policy_id | text | UUID of approved effective refund/cancellation policy | finance_admin | HG-MERCHANT+HG-LEGAL | unconfigured |
| zoom_host_assignments | items | Nonsecret provider-user references for approved licensed hosts; each maps active teacher ID | operations_admin | HG-PROVIDERS | unconfigured |
| google_calendar_id | text | Dedicated business calendar identifier; no learner personal calendar OAuth | operations_admin | HG-PROVIDERS | unconfigured |
| email_from_address | text | Verified Resend sender email under authenticated business domain | operations_admin | HG-PROVIDERS | unconfigured |
| approved_video_hosts | items | Subset of youtube.com,youtu.be,vimeo.com; no credentials/IP literals; HTTPS only | operations_admin | HG-LEGAL | unconfigured |
| enrolment_enabled | flag | boolean; true only with approved legal/merchant/age/provider/staff gates and passing launch acceptance | operations_admin | HG-LEGAL+HG-MERCHANT+HG-AGE+HG-PROVIDERS+HG-STAFF | false |
| public_publication_enabled | flag | boolean; true only approved legal/contact/age/staff settings complete | operations_admin | HG-LEGAL+HG-AGE+HG-STAFF | false |
| retention_purge_enabled | flag | boolean; true only approved retention_matrix_version and hold checks configured | operations_admin | HG-LEGAL | false |


An approval reference resolves a recorded human decision with approving actor,time,version and purpose. A free-form string alone does not establish approval; application validation verifies its evidence record. Missing/unapproved required values return409 HUMAN_APPROVAL_REQUIRED or LAUNCH_CONFIGURATION_REQUIRED and keep the affected production feature disabled. HG-AGE is age bands; HG-LEGAL is policies/privacy/retention/contact; HG-MERCHANT is merchant/tax/refund approval; HG-PROVIDERS is licensed host allocation; HG-PROVIDERS is production provider configuration; HG-LAUNCH is business launch activation. These are review gate labels, not assertions that approval has occurred.

No secrets are accepted in SettingValue. Integration provider keys are the separate fixed enum stripe,zoom,calendar,resend,storage. Configure accepts enabled:boolean and secret_reference:string identifying an allowlisted environment secret, plus reason; response returns only configured/enabled/secret version label and safe health. Stripe credential changes/resynchronization require both operations_admin and finance_admin. Provider endpoints/SDK versions, JWT algorithms, MFA bypasses and arbitrary code are not user-editable settings. Security constants, file limits and completion policy are locked architecture decisions changed only through approved scope/architecture review.

Policy IDs refer to approved immutable effective versions. `refund_policy_id` references the approved terms/policy version containing refund and cancellation clauses; it does not introduce an unapproved extra payment mode. Tax fields are finance-owned and Price snapshot validates them before checkout. Host assignments map active teacher identities to licensed nonsecret Zoom account references; they are validated against provider state before activation. Google Calendar uses one dedicated business calendar. Approved video hosts do not allow arbitrary embed scripts or private network fetches.

All changes use version preconditions, immutable audit and recorded approval. A setting version becomes effective transactionally and queues any necessary integration validation. In-flight orders retain their original immutable purchase snapshot. Invalid/stale provider configuration never mutates the authoritative schedule. Retention worker checks policy approval and holds immediately before deleting; toggling a flag cannot override an active hold.

Canonical human gate identities are exactly LAUNCH_SCOPE: HG-LEGAL, HG-MERCHANT, HG-AGE, HG-PROVIDERS and HG-STAFF. The historical architecture labels HG-FINANCE mean HG-MERCHANT; HG-ZOOM and HG-INTEGRATIONS are subchecks of HG-PROVIDERS. HG-LAUNCH is the composite launch decision, never an alternative approval that bypasses any canonical gate. HG-STAFF requires verified initial administrators, role separation, approved teachers and incident contacts before staff activation or production launch. Approval evidence is recorded by the authorized human owner and verified through the typed settings/administration application services. Public publication and enrolment flags cannot bypass these checks.
