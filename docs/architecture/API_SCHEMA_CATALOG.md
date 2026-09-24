# API schema catalog

Status: DRAFT, scope 1.0 / architecture 2. Canonical structured contracts: [backend-catalog.json](backend-catalog.json). These are design contracts, not implemented classes or endpoints. Implementation ownership and requirement traceability are in CODE_BLUEPRINT.md and docs/planning/REQUIREMENT_TRACEABILITY.md.

`required` means key presence is mandatory; nullable independently permits null. Optional blank child fields normalize to null. Unknown write properties are rejected. Referenced DTO fields validate recursively. Enum values are closed. Path IDs are opaque UUIDs and never confer access.

## Empty

No JSON body; successful deletion is HTTP 204.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## Accepted

HTTP 202 durable operation accepted; poll authorized job.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| job_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(queued\|running) | True | False | body | Closed enum; reject unknown values |
| status_url | string | True | False | body | Allowlisted same-origin relative authorized job status path |

## Error

RFC9457-style JSON problem body; HTTP status specified in error catalog.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| code | string | True | False | body | Stable documented error code |
| message | string | True | False | body | Safe actionable text without resource existence leaks |
| request_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| field_errors | FieldError[] | False | False | body | Validate referenced schema recursively |
| retry_after_seconds | integer | False | False | body | 1–3600 |

## FieldError

FieldError

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| field | string | True | False | body | Known input field path |
| code | string | True | False | body | Validation code |
| message | string | True | False | body | Safe validation message |

## PageMeta

Opaque signed cursor binds principal, query, order and expiry.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| next_cursor | token | True | True | body | opaque cryptographic token; max 512 characters; never logged |
| has_more | boolean | True | False | body | strict JSON boolean |

## SessionView

No bearer session secret in JSON; HttpOnly cookie set separately.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| privileges | string[] | True | False | body | Closed identifiers: identity_admin,education_admin,finance_admin,operations_admin,audit_admin |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| csrf_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| mfa_required | boolean | True | False | body | strict JSON boolean |

## AccountView

Child identity may have no email; staff privileges only in authorized admin projection.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | True | body | normalized verified deliverable address; max 254 characters |
| status | enum(invited\|pending_verification\|active\|suspended\|closed) | True | False | body | Closed enum; reject unknown values |
| mfa_enabled | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

## DeviceSessionView

No IP address or raw credential exposed.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| last_seen_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| device_label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| current | boolean | True | False | body | strict JSON boolean |

## GuardianView

GuardianView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| phone | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| essential_contact | enum(email) | True | False | body | Closed enum; reject unknown values |
| optional_email | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

## FamilyView

Parent projection includes only actively linked students, not every family sibling. Billing membership never inferred from list membership.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| guardians | GuardianSummary[] | True | False | body | Validate referenced schema recursively |
| students | StudentSummary[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |

## GuardianSummary

GuardianSummary

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| relationship | enum(primary\|verified_guardian) | True | False | body | Closed enum; reject unknown values |
| status | enum(active\|revoked) | True | False | body | Closed enum; reject unknown values |

## StudentSummary

StudentSummary

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 proposed technical input; approved launch bands enforced separately |
| age_recorded_on | date | True | False | body | ISO8601 calendar date |
| status | enum(active\|archived) | True | False | body | Closed enum; reject unknown values |

## StudentProfileView

StudentProfileView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 |
| age_recorded_on | date | True | False | body | ISO8601 calendar date |
| school_name | string | True | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | True | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | True | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | True | True | body | Optional closed educational-experience enum |
| status | enum(active\|archived) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

## TeachingStudentView

Purpose-limited teaching projection: excludes family ID, school name, last name, email, phone, billing and credentials.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 |
| age_recorded_on | date | True | False | body | ISO8601 calendar date |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | True | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | True | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | True | True | body | Optional closed educational-experience enum |

## StudentCredentialsView

Returned only once to authorized guardian after step-up; no child email required.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| username | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| one_time_secret | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## TeacherView

TeacherView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| biography | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| public_photo_asset_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(invited\|active\|suspended\|archived) | True | False | body | Closed enum; reject unknown values |
| public_profile_published | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

## PublicTeacherView

Explicitly published teacher profile only.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| biography | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| photo_url | url | True | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |

## RoleGrantView

RoleGrant value object projected from Account.admin_privileges. version is the current owning Account.version; there is no independent role counter.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| admin_privileges | string[] | True | False | body | Closed identifiers: identity_admin,education_admin,finance_admin,operations_admin,audit_admin |
| version | version | True | False | body | Current owning Account.version for user_id; same counter as AccountView.version; every status or role change increments it |

## PolicyView

PolicyView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| key | enum(privacy\|terms\|child_safety\|consent) | True | False | body | Closed enum; reject unknown values |
| version_label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| requires_acknowledgement | boolean | True | False | body | strict JSON boolean |
| effective_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## AcknowledgementView

Immutable evidence, not an editable boolean.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| policy_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| policy_version | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| guardian_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| acknowledged_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## PublicPageView

PublicPageView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| slug | string | True | False | body | home,about,how-classes-work,parents,faq,contact,age-groups only |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## ContactReceipt

No contact payload echoed; submission becomes restricted operational notice.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| reference | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| accepted_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## ProgramView

ProgramView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(draft\|published\|archived) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

## PublicProgramView

PublicProgramView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |

## CourseView

CourseView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| program_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | True | False | body | Validate referenced schema recursively |
| min_age | integer | True | False | body | 4–18 |
| max_age | integer | True | False | body | 4–18 and >= min_age |
| duration_weeks | integer | True | False | body | 1–52 |
| delivery_method | enum(live_online) | True | False | body | Closed enum; reject unknown values |
| status | enum(draft\|published\|archived) | True | False | body | Closed enum; reject unknown values |
| current_revision_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| version | version | True | False | body | positive integer optimistic concurrency token |

## PublicCourseView

Published marketing projection. Does not expose lesson drafts, content URLs, answers or internal settings.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| program_title | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | True | False | body | Validate referenced schema recursively |
| min_age | integer | True | False | body | strict integer |
| max_age | integer | True | False | body | strict integer |
| duration_weeks | integer | True | False | body | strict integer |
| delivery_method | enum(live_online) | True | False | body | Closed enum; reject unknown values |
| display_price | PriceView | True | True | body | Type validation; no unknown fields |
| curriculum_outline | OutlineModule[] | True | False | body | Validate referenced schema recursively |

## OutlineModule

Only explicitly publishable outline titles.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| lesson_titles | string[] | True | False | body | Validate referenced schema recursively |

## CurriculumRevisionView

CurriculumRevisionView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_number | integer | True | False | body | >=1 |
| status | enum(draft\|published\|retired) | True | False | body | Closed enum; reject unknown values |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| modules | ModuleView[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |

## ModuleView

ModuleView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | >=0 |
| release_offset_days | integer | True | False | body | 0–365 |
| lessons | LessonSummary[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |

## LessonSummary

Learner responses omit unreleased lessons entirely; administrative summaries may include released false.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | strict integer |
| released | boolean | True | False | body | strict JSON boolean |

## LessonView

LessonView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| module_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | strict integer |
| release_offset_days | integer | True | False | body | 0–365 |
| blocks | LessonBlockView[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

## LessonBlockView

Discriminated union described below; no arbitrary HTML, embeds or scripts.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | enum(heading\|rich_text\|image\|video\|download\|activity\|quiz\|assignment) | True | False | body | Closed enum; reject unknown values |
| position | integer | True | False | body | strict integer |
| content | LessonBlockContent | True | False | body | Type validation; no unknown fields |
| version | version | True | False | body | positive integer optimistic concurrency token |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

## LessonBlockContent

Exactly branch fields allowed by kind: heading=heading; rich_text=sanitized_html; image=asset_id+alt_text; video=asset_id XOR approved video_url; download=asset_id; activity=instructions; quiz=quiz_id; assignment=assignment_id. All other fields forbidden; no answer fields. Video additionally requires captions_asset_id or transcript before publication; image alt text mandatory. Resource video equivalent accessibility metadata required.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| heading | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| asset_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| alt_text | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| video_url | url | False | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| instructions | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| quiz_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| captions_asset_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| transcript | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |

## ResourceView

Exactly one ready asset or approved HTTPS external URL; learner read additionally release-gated.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| asset_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| external_url | url | True | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| kind | enum(document\|image\|video\|project) | True | False | body | Closed enum; reject unknown values |
| status | enum(draft\|ready\|archived) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

## CohortView

CohortView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| capacity | integer | True | False | body | 1–100 |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| status | enum(draft\|open\|closed\|in_progress\|completed\|cancelled) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | <=starts_at |

## PublicCohortView

No roster, meeting reference, capacity counters or teacher operational data.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| availability | enum(available\|full\|closed) | True | False | body | Closed enum; reject unknown values |
| price | PriceView | True | False | body | Type validation; no unknown fields |
| sessions | PublicSessionView[] | True | False | body | Validate referenced schema recursively |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## PublicSessionView

Published timetable only.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |

## ClassSessionView

No stored host URL or meeting credential; actions separately authorized. Learner projection hides provider failure detail.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| status | enum(scheduled\|cancelled\|completed) | True | False | body | Closed enum; reject unknown values |
| lesson_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| can_join | boolean | True | False | body | strict JSON boolean |
| can_start | boolean | True | False | body | strict JSON boolean |
| integration_status | enum(pending\|ready\|failed) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |
| teacher_display_names | string[] | True | False | body | Validate referenced schema recursively |
| student_ids | uuid[] | False | False | body | Parent response only, linked children only; forbidden in public/student/teacher details |

## TeacherAssignmentView

TeacherAssignmentView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| teacher_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| session_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(lead\|assistant) | True | False | body | Closed enum; reject unknown values |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## JoinLinkView

Sensitive short-lived handoff; Cache-Control no-store, referrer policy no-referrer; never analytics logged.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## EnrolmentView

Learner projection never includes Payment or Price.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(held\|pending_payment\|active\|cancelled\|completed\|expired\|payment_exception) | True | False | body | Closed enum; reject unknown values |
| hold_expires_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| access_ends_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## AttendanceView

No internal attendance notes are exposed to parents or students.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(present\|absent\|late\|excused\|unrecorded) | True | False | body | Closed enum; reject unknown values |
| minutes_attended | integer | True | True | body | strict integer |
| recorded_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## QuizView

Authoring quiz definition; correct keys and approved explanation included only to authorized curriculum/teaching scope. LearnerQuizView excludes both until own attempt submitted.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lesson_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| pass_percent | integer | True | False | body | 0–100 |
| max_attempts | integer | True | False | body | 1–5; default3 |
| questions | QuizQuestionView[] | True | False | body | Validate referenced schema recursively |
| status | enum(draft\|ready) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

## QuizQuestionView

Never included in learner schema.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| prompt | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| position | integer | True | False | body | strict integer |
| kind | enum(single_choice\|multiple_choice) | True | False | body | Closed enum; reject unknown values |
| options | QuizOption[] | True | False | body | Validate referenced schema recursively |
| correct_option_ids | uuid[] | True | False | body | Validate referenced schema recursively |
| points | integer | True | False | body | 1–100 |
| explanation | text | True | False | body | Approved explanation shown after learner submission; immutable with published quiz |

## QuizOption

QuizOption

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| text | string | True | False | body | 1–500 |

## LearnerQuizView

Correct-answer identifiers and grading rules omitted.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| max_attempts | integer | True | False | body | strict integer |
| attempts_remaining | integer | True | False | body | strict integer |
| questions | LearnerQuestionView[] | True | False | body | Validate referenced schema recursively |

## LearnerQuestionView

LearnerQuestionView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| prompt | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| position | integer | True | False | body | strict integer |
| kind | enum(single_choice\|multiple_choice) | True | False | body | Closed enum; reject unknown values |
| options | QuizOption[] | True | False | body | Validate referenced schema recursively |

## QuizAnswer

QuizAnswer

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| question_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| selected_option_ids | uuid[] | True | False | body | IDs in attempt snapshot; unique; one for single choice; up to all options for multiple choice |

## QuizAttemptView

Result null until release; answers only own selections, never correct-answer key.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(in_progress\|submitted\|released) | True | False | body | Closed enum; reject unknown values |
| answers | QuizAnswer[] | True | False | body | Validate referenced schema recursively |
| submitted_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| result | ReleasedQuizResult | True | True | body | Type validation; no unknown fields |
| version | version | True | False | body | positive integer optimistic concurrency token |

## ReleasedQuizResult

Immediate formative result for submitted own attempt: score plus per-question correctness and approved explanation. Never an unsubmitted quiz answer-key endpoint.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| score | integer | True | False | body | max possible score |
| max_score | integer | True | False | body | strict integer |
| passed | boolean | True | False | body | strict JSON boolean |
| released_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| questions | ReleasedQuestionFeedback[] | True | False | body | Validate referenced schema recursively |

## AssignmentView

Published/draft curriculum definition projection; version is the owning curriculum definition token only, never the separate delivery closure token. closed/due_at are read-only delivery-resolved convenience values when used in learner context; admin closure writes use AssignmentClosureView.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lesson_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| kind | enum(assignment\|project) | True | False | body | Closed enum; reject unknown values |
| due_offset_days | integer | True | True | body | 0–365 |
| max_score | integer | True | False | body | 1–1000 |
| max_files | integer | True | False | body | 1–5 |
| status | enum(draft\|ready) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | Current curriculum definition version; immutable after publication; never use for per-cohort closure mutation |
| rubric | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| passing_score | integer | True | False | body | 0–max_score |
| allow_resubmission | boolean | True | False | body | strict JSON boolean |
| closed | boolean | True | False | body | strict JSON boolean |
| due_at | datetime | True | True | body | Resolved cohort-relative due time in learner context |

## SubmissionView

Immutable submitted version; returning permits new attempt linked to previous, not overwriting evidence.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| attempt_number | integer | True | False | body | >=1 |
| body | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| files | FileAssetView[] | True | False | body | Validate referenced schema recursively |
| status | enum(draft\|submitted\|returned\|assessed) | True | False | body | Closed enum; reject unknown values |
| submitted_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |
| late | boolean | True | False | body | strict JSON boolean |

## AssessmentView

Learner endpoint returns only released record; withdrawn becomes unavailable, retaining audit.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| score | integer | True | True | body | strict integer |
| max_score | integer | True | False | body | strict integer |
| rubric_comment | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(draft\|released\|withdrawn) | True | False | body | Closed enum; reject unknown values |
| released_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## FeedbackView

FeedbackView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(draft\|released\|withdrawn) | True | False | body | Closed enum; reject unknown values |
| released_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## ProgressView

Derived source counts remain unchanged. Eligibility is standard policy OR active evidenced education-admin override; private override evidence is never learner/parent projected.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lessons_completed | integer | True | False | body | strict integer |
| lessons_required | integer | True | False | body | strict integer |
| assignments_passed | integer | True | False | body | strict integer |
| assignments_required | integer | True | False | body | strict integer |
| quizzes_passed | integer | True | False | body | strict integer |
| quizzes_required | integer | True | False | body | strict integer |
| completion_percent | integer | True | False | body | 0–100 |
| status | enum(not_started\|in_progress\|complete) | True | False | body | Closed enum; reject unknown values |
| updated_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| delivered_sessions | integer | True | False | body | strict integer |
| attended_sessions | integer | True | False | body | strict integer |
| attendance_percent | integer | True | False | body | 0–100 |
| completion_eligible | boolean | True | False | body | strict JSON boolean |
| completion_basis | enum(incomplete\|standard\|admin_override) | True | False | body | Closed enum; reject unknown values |

## CertificateView

No public directory or searchable child names. Download separately authorized.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| issued_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| status | enum(pending\|issued\|revoked) | True | False | body | Closed enum; reject unknown values |
| verification_code | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| asset_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## PriceView

Admin-approved tax configuration required before checkout. Snapshot immutable on Payment.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| tax_treatment | enum(inclusive\|exclusive\|exempt) | True | False | body | Closed enum; reject unknown values |
| tax_rate_basis_points | integer | True | False | body | 0–10000 |
| label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## PriceConfigView

PriceConfigView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| price | PriceView | True | False | body | Validate referenced schema recursively |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## CheckoutSessionView

Server-generated Stripe hosted checkout URL; redirect does not activate enrolment.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| checkout_url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| price | PriceView | True | False | body | Validate referenced schema recursively |

## PaymentView

Parent-safe projection; excludes Stripe customer/payment-method metadata and integration raw payload.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| status | enum(pending\|succeeded\|failed\|expired\|partially_refunded\|refunded\|exception) | True | False | body | Closed enum; reject unknown values |
| paid_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| refunded_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| receipt_available | boolean | True | False | body | strict JSON boolean |

## AdminPaymentView

Finance privilege only; no card data or sensitive webhook raw payload.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment | PaymentView | True | False | body | Validate referenced schema recursively |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| provider_payment_id | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| provider_checkout_id | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reconciliation_status | enum(unreconciled\|matched\|exception) | True | False | body | Closed enum; reject unknown values |
| exception_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| version | version | True | False | body | positive integer optimistic concurrency token |

## ReceiptView

Legal content approved before billing live; short-lived authorized document URL.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| document_type | enum(receipt\|invoice) | True | False | body | Closed enum; reject unknown values |
| number | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| issued_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| seller_legal_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| seller_abn | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| purchaser_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| line_description | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| tax_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| download_url | url | True | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |

## RefundView

RefundView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| access_disposition | enum(KEEP\|CANCEL) | True | False | body | Closed enum; reject unknown values |
| status | enum(requested\|processing\|succeeded\|failed) | True | False | body | Closed enum; reject unknown values |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## FinanceReportView

Bounded 366-day range; cash ledger reporting, not unapproved accounting/tax engine.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | date | True | False | body | ISO8601 calendar date |
| to | date | True | False | body | ISO8601 calendar date |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| gross_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| refund_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| net_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| succeeded_count | integer | True | False | body | strict integer |
| exception_count | integer | True | False | body | strict integer |

## EventView

EventView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| description | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| audience | Audience | True | False | body | Type validation; no unknown fields |
| status | enum(draft\|published\|cancelled) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

## Audience

Discriminated target: public has empty roles and null IDs; role has nonempty role allowlist and null IDs; course has course_id only; cohort has cohort_id only. Course/cohort recipients must have current educational relation and be in role filter. Global student role announcements permitted only approved operational education notice, never marketing. Public announcements contain no private relations.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| kind | enum(public\|role\|course\|cohort) | True | False | body | Closed enum; reject unknown values |
| roles | enum(parent\|student\|teacher)[] | True | False | body | Nonempty except public; optional audience roles are explicit inclusion filter |
| course_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## AnnouncementView

AnnouncementView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| status | enum(draft\|published\|withdrawn) | True | False | body | Closed enum; reject unknown values |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## NotificationView

Only principal-owned recipient; no teacher payment notification.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | enum(account\|enrolment\|payment\|class\|assignment\|feedback\|certificate\|operations) | True | False | body | Closed enum; reject unknown values |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| portal_path | string | True | False | body | Allowlisted same-origin route |
| read_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## FileAssetView

Object keys and bucket credentials never returned.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| filename | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| media_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| size_bytes | integer | True | False | body | strict integer |
| purpose | enum(resource\|submission\|certificate\|internal\|public_asset\|financial_document\|financial_export) | True | False | body | Closed enum; reject unknown values |
| status | enum(quarantined\|scanning\|ready\|rejected\|deleted) | True | False | body | Closed enum; reject unknown values |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | Current FileAsset.version for id; use for API-FILE-DELETE If-Match, never a resource/revision/owner token |

## UploadTicketView

Unique staging key; presigned 5-minute validity; cannot overwrite final key.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| asset_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| upload_url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| method | enum(PUT) | True | False | body | Closed enum; reject unknown values |
| required_headers | UploadHeaders | True | False | body | Type validation; no unknown fields |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| max_size_bytes | integer | True | False | body | strict integer |

## UploadHeaders

UploadHeaders

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| content_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| checksum_sha256 | string | True | False | body | base64 SHA256 checksum; provider-independent required-header names serialized by API |

## DownloadTicketView

Presigned GET valid <=60 seconds; permission rechecked each issuance.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| filename | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| media_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## SettingView

Never returns credential value; public config uses separate schema.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| key | enum(child_age_min\|child_age_max\|approved_child_interests\|support_email\|safeguarding_email\|business_phone\|policy_privacy_id\|policy_terms_id\|policy_child_safety_id\|required_consent_policy_ids\|retention_matrix_version\|retention_child_months\|retention_contact_days\|retention_delivery_days\|retention_finance_years\|retention_certificate_years\|merchant_legal_name\|merchant_abn\|merchant_address\|tax_treatment\|tax_rate_basis_points\|refund_policy_id\|zoom_host_assignments\|google_calendar_id\|email_from_address\|approved_video_hosts\|enrolment_enabled\|public_publication_enabled\|retention_purge_enabled) | True | False | body | Closed key catalog in SETTINGS_CATALOG |
| value | SettingValue | True | False | body | Type validation; no unknown fields |
| approved | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

## SettingValue

Exactly one value field according to approved key schema; no arbitrary secrets.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| text | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| number | integer | False | False | body | strict integer |
| flag | boolean | False | False | body | strict JSON boolean |
| items | string[] | False | False | body | Validate referenced schema recursively |

## IntegrationStatusView

Masked reference only; configuration cannot accept executable endpoint URLs.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| provider | enum(stripe\|zoom\|calendar\|resend\|storage) | True | False | body | Closed enum; reject unknown values |
| configured | boolean | True | False | body | strict JSON boolean |
| enabled | boolean | True | False | body | strict JSON boolean |
| last_success_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| failure_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| secret_version_label | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## JobView

Safe error codes; no payload or PII.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| status | enum(queued\|running\|succeeded\|failed\|dead_letter) | True | False | body | Closed enum; reject unknown values |
| attempts | integer | True | False | body | strict integer |
| last_error_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| next_attempt_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |

## AuditView

Redacted purpose-bound audit view; no passwords, tokens, secret URLs or full child content.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| actor_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| action | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| resource_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| resource_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| occurred_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| outcome | enum(allowed\|denied\|failed) | True | False | body | Closed enum; reject unknown values |
| request_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| reason | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## DashboardView

Role-specific safe counts. Admin uses privilege-specific dashboard parts, never all-data dump.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| upcoming_count | integer | True | False | body | strict integer |
| unread_notifications | integer | True | False | body | strict integer |
| pending_actions | DashboardAction[] | True | False | body | Validate referenced schema recursively |

## DashboardAction

Allowed kinds filtered by role; teacher/student cannot receive payment.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| kind | enum(class\|assignment\|payment\|review\|operations) | True | False | body | Closed enum; reject unknown values |
| count | integer | True | False | body | strict integer |
| portal_path | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## OperationsSummaryView

Operations-admin only; no finance sums.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| failed_jobs | integer | True | False | body | strict integer |
| unsynced_sessions | integer | True | False | body | strict integer |
| quarantined_files | integer | True | False | body | strict integer |
| unconfigured_launch_settings | integer | True | False | body | strict integer |

## DeliveryView

Operations-admin; recipient email masked.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| notification_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| channel | enum(in_app\|email) | True | False | body | Closed enum; reject unknown values |
| status | enum(queued\|sent\|failed\|suppressed) | True | False | body | Closed enum; reject unknown values |
| attempt_count | integer | True | False | body | strict integer |
| sent_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| last_error_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## ExportView

Purpose-scoped export lifecycle metadata. Privacy exports require verified requester ownership; finance exports require finance_admin requester or explicit oversight. A separate authorized download operation returns a short-lived URL only while ready and unexpired.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(requested\|processing\|ready\|failed\|expired) | True | False | body | Closed enum; reject unknown values |
| expires_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| failure_code | enum(GENERATION_FAILED\|LIMIT_EXCEEDED\|STORAGE_UNAVAILABLE) | True | True | body | Null except terminal failed state; sanitized code only, no provider details or file contents. |

## API_AUTH_REGISTERRequest

Register guardian and create family input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| policy_ids | uuid[] | True | False | body | All required current policy versions |

## API_AUTH_VERIFYRequest

Consume single-use email verification input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |

## API_AUTH_RESENDRequest

Resend verification without account enumeration input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |

## API_AUTH_LOGINRequest

Authenticate parent/staff/student input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| identifier | string | True | False | body | Email for adult/staff or opaque student username |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

## API_AUTH_MFARequest

Complete staff MFA challenge input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| challenge_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| code | string | True | False | body | 6-digit TOTP or unused recovery code |

## MfaSetupView

Original successful enrolment response only; never replayable. Duplicate and restart semantics are defined by ADR 0004.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| setup_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| otpauth_uri | string | True | False | body | TOTP provisioning URI shown once over HTTPS |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## API_AUTH_MFA_ENROLRequest

Begin staff TOTP setup from either password-login or invitation limited context, or permitted full-session re-enrolment; no role field required.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| Idempotency-Key | uuid | True | False | header | ADR 0004 exception: validate current account/session or limited setup context, browser, purpose, expiry, attempts and CSRF/Origin before idempotency. First committed enrolment returns MfaSetupView once; same key/body after commit returns secret-free 409 MFA_REPLAY; changed body returns 409 IDEMPOTENCY_CONFLICT. Serialize duplicates, restart and confirmation; rollback permits retry, uncertain commit requires authoritative lookup. Keep only safe principal/operation/key, keyed canonical-body digest and outcome metadata for 7 days; never store/replay the URI or recoverable setup token. A lost response requires explicit restart with fresh permitted password authentication and a new key, invalidating pending setup credentials atomically without removing an active factor before replacement confirmation. Existing lifetime, attempt and abuse limits apply. |
| setup_token | token | False | False | body | Required without full session for either login mfa_setup_required or invitation-accepted limited setup; bound to same staff account and setup purpose; expired/consumed/foreign tokens rejected; unrelated full session forbidden |

## RecoveryCodeView

RecoveryCodeView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| recovery_codes | string[] | True | False | body | 10 cryptographically random single-use codes shown once |

## API_AUTH_MFA_CONFIRMRequest

Activate TOTP and issue recovery codes once input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| setup_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| code | string | True | False | body | 6 digits |

## API_AUTH_RESET_REQUESTRequest

Request account recovery input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |

## API_AUTH_RESETRequest

Reset adult password and revoke sessions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| new_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

## API_AUTH_MERequest

Get safe authenticated session identity input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_AUTH_LOGOUTRequest

Revoke current session input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_ACCOUNT_PASSWORDRequest

Change own adult/staff password and revoke other sessions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| current_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| new_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ACCOUNT_SESSIONSRequest

List own devices input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## DeviceSessionViewPage

DeviceSessionViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | DeviceSessionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ACCOUNT_REVOKERequest

Revoke selected own device input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ACCOUNT_PROFILERequest

Read own profile input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_FAMILY_GETRequest

Read own family and linked students input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_PARENT_PROFILERequest

Read guardian contact/preferences input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_PARENT_UPDATERequest

Update guardian contact/preferences input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| first_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| phone | string | False | True | body | E164, nullable |
| optional_email | boolean | False | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_PARENT_EMAIL_CHANGERequest

Begin verified contact email change input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| new_email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

## API_PARENT_EMAIL_CONFIRMRequest

Confirm new email and notify old address input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |

## API_STUDENT_CREATERequest

Register child with required name and age input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 |
| preferred_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| school_name | string | False | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | False | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | False | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | False | True | body | Optional closed educational-experience enum |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_STUDENT_GETRequest

Read linked child profile input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_STUDENT_UPDATERequest

Update optional child information input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| first_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| school_name | string | False | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | False | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | False | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | False | True | body | Optional closed educational-experience enum |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_STUDENT_AGERequest

Reconfirm required age input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| age_years | integer | True | False | body | 4–18;recorded date set by server |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_STUDENT_CREDENTIALSRequest

Provision or rotate child login input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| guardian_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_STUDENT_SELFRequest

Read own limited profile input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_STUDENT_PREFERREDRequest

Change own preferred display name input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| preferred_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | False | False | body | 0–10 unique |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | False | True | body | Closed enum; reject unknown values |

## API_POLICY_LISTRequest

Read published policy versions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PolicyViewPage

PolicyViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PolicyView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_CONSENT_LISTRequest

Read family acknowledgement evidence input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## AcknowledgementViewPage

AcknowledgementViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AcknowledgementView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_CONSENT_ACKRequest

Record current policy acknowledgement input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| policy_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | False | True | body | Linked child scope where policy requires |

## API_PUBLIC_PAGERequest

Read get page input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| slug | string | True | False | path | Known allowlisted key |

## API_PUBLIC_PROGRAMSRequest

Read list programs input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PublicProgramViewPage

PublicProgramViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PublicProgramView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PUBLIC_COURSESRequest

Read list courses input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PublicCourseViewPage

PublicCourseViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PublicCourseView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PUBLIC_COURSERequest

Read get course input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| slug | string | True | False | path | Known allowlisted key |

## API_PUBLIC_COHORTSRequest

Read list public cohorts input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PublicCohortViewPage

PublicCohortViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PublicCohortView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PUBLIC_TEACHERSRequest

Read list public teachers input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PublicTeacherViewPage

PublicTeacherViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PublicTeacherView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PUBLIC_CONTACTRequest

Submit contact enquiry to operations queue input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| message | text | True | False | body | 20–2000 |
| captcha_token | token | False | False | body | opaque cryptographic token; max 512 characters; never logged |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_PROGRAM_LISTRequest

List draft and published programs input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ProgramViewPage

ProgramViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ProgramView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_PROGRAM_CREATERequest

Create offering grouping input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| slug | string | True | False | body | lowercase URL slug 3–80, unique |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_PROGRAM_UPDATERequest

Edit offering grouping input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| program_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_PROGRAM_STATUSRequest

Publish or archive program input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| program_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(published\|archived) | True | False | body | Closed enum; reject unknown values |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_COURSESRequest

List all curriculum courses input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(draft\|published\|archived) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## CourseViewPage

CourseViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | CourseView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_COURSERequest

Read administrative course details input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_COURSE_CREATERequest

Create reusable course input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| program_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | unique lowercase slug 3–80 |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | True | False | body | 1–30 |
| min_age | integer | True | False | body | 4–18 |
| max_age | integer | True | False | body | >= min_age, <=18 |
| duration_weeks | integer | True | False | body | 1–52 |
| delivery_method | enum(live_online) | True | False | body | Closed enum; reject unknown values |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_COURSE_UPDATERequest

Edit course marketing metadata input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| program_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | False | False | body | Validate referenced schema recursively |
| min_age | integer | False | False | body | 4–18 |
| max_age | integer | False | False | body | >= min_age, <=18 |
| duration_weeks | integer | False | False | body | 1–52 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_COURSE_PUBLISHRequest

Publish approved course with ready revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_COURSE_ARCHIVERequest

Archive course acquisition; preserve existing learning access input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_REVISION_LISTRequest

List curriculum revisions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## CurriculumRevisionViewPage

CurriculumRevisionViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | CurriculumRevisionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_REVISION_CREATERequest

Create draft revision optionally copied from same course input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| source_revision_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_REVISION_GETRequest

Read full authoring hierarchy input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_REVISION_PUBLISHRequest

Freeze validated curriculum revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_MODULE_CREATERequest

Create draft module input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | >=0 |
| release_offset_days | integer | True | False | body | 0–365 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_MODULE_UPDATERequest

Edit draft module input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| module_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | False | False | body | >=0 |
| release_offset_days | integer | False | False | body | 0–365 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_MODULE_DELETERequest

Remove unreferenced draft module input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| module_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_LESSON_CREATERequest

Create draft lesson input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| module_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | >=0 |
| release_offset_days | integer | True | False | body | 0–365 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

## API_ADMIN_LESSON_UPDATERequest

Edit draft lesson input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | False | False | body | >=0 |
| release_offset_days | integer | False | False | body | 0–365 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| required_for_completion | boolean | False | False | body | strict JSON boolean |

## API_ADMIN_LESSON_DELETERequest

Remove unreferenced draft lesson input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_BLOCK_CREATERequest

Create draft block input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| kind | enum(heading\|rich_text\|image\|video\|download\|activity\|quiz\|assignment) | True | False | body | Closed enum; reject unknown values |
| position | integer | True | False | body | >=0 |
| content | LessonBlockContent | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

## API_ADMIN_BLOCK_UPDATERequest

Edit draft block input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| block_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| position | integer | False | False | body | >=0 |
| content | LessonBlockContent | False | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| required_for_completion | boolean | False | False | body | strict JSON boolean |

## API_ADMIN_BLOCK_DELETERequest

Remove unreferenced draft block input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| block_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_RESOURCE_CREATERequest

Create draft resource input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| kind | enum(document\|image\|video\|project) | True | False | body | Closed enum; reject unknown values |
| asset_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| external_url | url | False | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_RESOURCE_UPDATERequest

Edit draft resource input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| asset_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| external_url | url | False | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_RESOURCE_DELETERequest

Remove unreferenced draft resource input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_RESOURCE_LISTRequest

List teaching assets in revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ResourceViewPage

ResourceViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ResourceView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_LESSON_GETRequest

Read authoring lesson and all block fields input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_STUDENT_ENROLMENTSRequest

List own enrolled courses input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## EnrolmentViewPage

EnrolmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | EnrolmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PARENT_ENROLMENTSRequest

List linked child enrolment status input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_CURRICULUMRequest

Read released modules of pinned revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_STUDENT_LESSONRequest

Read released lesson and safe blocks input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_STUDENT_RESOURCERequest

List released learning resources input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_COURSESRequest

List assigned courses input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_COHORTSRequest

List assigned cohorts input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## CohortViewPage

CohortViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | CohortView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_TEACHER_CURRICULUMRequest

Read pinned teaching curriculum including planned lessons input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_TEACHER_LESSONRequest

Read assigned teaching lesson plan input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_TEACHER_RESOURCESRequest

Read assigned teaching resources input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_STUDENTSRequest

Read assigned roster educational fields input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## TeachingStudentViewPage

TeachingStudentViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | TeachingStudentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_TEACHER_STUDENTRequest

Read assigned learner educational profile input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_PARENTSRequest

Read authorized list parents input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| query | string | False | False | query | 1–100 exact/limited contact search |
| status | enum(active\|suspended\|closed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## GuardianViewPage

GuardianViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | GuardianView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_FAMILYRequest

Read authorized get family input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| family_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_STUDENTSRequest

Read authorized list students input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| family_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| query | string | False | False | query | 1–100 |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## StudentProfileViewPage

StudentProfileViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | StudentProfileView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_STUDENTRequest

Read authorized get student input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_TEACHERSRequest

Read authorized list teachers input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(invited\|active\|suspended\|archived) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## TeacherViewPage

TeacherViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | TeacherView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_TEACHERRequest

Read authorized get teacher input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_GUARDIAN_LINKRequest

Link verified guardian to same family child input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| guardian_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| verification_reference | string | True | False | body | Audited external evidence ID, no sensitive document body |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| If-Match | version | True | False | header | Current AdminFamilyRelationshipsView.version for the same family; required even for first relationship; stale 409 VERSION_CONFLICT |

## API_ADMIN_GUARDIAN_REVOKERequest

Revoke guardian child access input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| guardian_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Current matching GuardianStudent.version from AdminFamilyRelationshipsView for guardian_id + student_id; never substitute Family.version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_STUDENT_UPDATERequest

Correct student data with reason input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| first_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | False | False | body | 4–18 |
| school_name | string | False | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_STUDENT_ARCHIVERequest

Archive child after active obligations resolved input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_INVITERequest

Invite teacher or constrained admin principal input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| role | enum(teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| admin_privileges | string[] | False | False | body | Closed list identity_admin,education_admin,finance_admin,operations_admin,audit_admin; incompatible teacher grants forbidden |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_AUTH_INVITE_ACCEPTRequest

Accept staff invitation and require MFA setup input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

## API_ADMIN_ROLERequest

Read constrained role grants input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| account_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_ROLE_UPDATERequest

Change admin privileges with audit and session revocation input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| account_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| admin_privileges | string[] | True | False | body | Closed list identity_admin,education_admin,finance_admin,operations_admin,audit_admin; incompatible teacher grants forbidden |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected owning Account.version from current account detail or RoleGrantView for this account_id; 409 VERSION_CONFLICT on stale value; never a separate role counter |

## API_ADMIN_ACCOUNT_STATUSRequest

Suspend or reactivate account and revoke affected sessions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| account_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(active\|suspended) | True | False | body | Closed enum; reject unknown values |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected owning Account.version from current account detail or RoleGrantView for this account_id; 409 VERSION_CONFLICT on stale value; never a separate role counter |

## API_ADMIN_TEACHER_UPDATERequest

Edit teacher public biography/profile input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| display_name | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| biography | text | False | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| public_photo_asset_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_TEACHER_PUBLISHRequest

Publish or withdraw explicitly approved instructor profile input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| published | boolean | True | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_TEACHER_ARCHIVERequest

Archive teacher after assignment reassignment input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_PROFILERequest

Read own teacher profile input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_ADMIN_COHORTSRequest

List operational cohorts input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(draft\|open\|closed\|in_progress\|completed\|cancelled) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_COHORTRequest

Read cohort operational details input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_COHORT_CREATERequest

Create course delivery pinned to published revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| capacity | integer | True | False | body | 1–100 |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | > starts_at |
| timezone | timezone | True | False | body | valid IANA timezone |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | >opens and <=starts |

## API_ADMIN_COHORT_UPDATERequest

Edit future cohort metadata and safe capacity input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| capacity | integer | False | False | body | >= active enrolments plus live holds |
| starts_at | datetime | False | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | False | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | False | False | body | valid IANA timezone |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | >opens and <=starts |

## API_ADMIN_COHORT_STATUSRequest

Open, close, start or complete delivery input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(open\|closed\|in_progress\|completed) | True | False | body | Closed enum; reject unknown values |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_COHORT_CANCELRequest

Cancel delivery and create refund review tasks input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_ASSIGNMENTSRequest

List cohort teaching grants input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## TeacherAssignmentViewPage

TeacherAssignmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | TeacherAssignmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_ASSIGNMENT_CREATERequest

Assign active teacher to cohort/session input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| teacher_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| session_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(lead\|assistant) | True | False | body | Closed enum; reject unknown values |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | False | True | body | RFC3339 timezone-aware instant, UTC persisted |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_ASSIGNMENT_REVOKERequest

Revoke teaching access immediately input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_SESSIONSRequest

List all delivery sessions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ClassSessionViewPage

ClassSessionViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ClassSessionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_SESSION_CREATERequest

Schedule one class occurrence input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | Must resolve chosen DST occurrence |
| duration_minutes | integer | True | False | body | 15–240 |
| lesson_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_RECURRENCERequest

Materialize bounded weekly occurrences transactionally input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| first_local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | strict integer |
| duration_minutes | integer | True | False | body | 15–240 |
| occurrences | integer | True | False | body | 1–52 |
| interval_weeks | integer | True | False | body | 1–4 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_SESSION_UPDATERequest

Edit session title/lesson without rescheduling input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| lesson_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_PARENT_SCHEDULERequest

List parent authorized upcoming classes input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | > from, <=93 day range |
| student_id | uuid | False | False | query | parent only; forbidden for student/teacher |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_PARENT_SESSIONRequest

Read authorized class session details input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_STUDENT_SCHEDULERequest

List student authorized upcoming classes input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | > from, <=93 day range |
| student_id | uuid | False | False | query | parent only; forbidden for student/teacher |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_SESSIONRequest

Read authorized class session details input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_TEACHER_SCHEDULERequest

List teacher authorized upcoming classes input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | > from, <=93 day range |
| student_id | uuid | False | False | query | parent only; forbidden for student/teacher |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_SESSIONRequest

Read authorized class session details input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_TEACHER_RESCHEDULERequest

Reschedule authorized session and queue provider updates input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | strict integer |
| duration_minutes | integer | True | False | body | 15–240 |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_RESCHEDULERequest

Reschedule authorized session and queue provider updates input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | strict integer |
| duration_minutes | integer | True | False | body | 15–240 |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_SESSION_CANCELRequest

Cancel class and queue Zoom/calendar cancellation and notices input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_SESSION_COMPLETERequest

Complete past session after attendance review input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_STARTRequest

Fetch fresh authorized Zoom host handoff input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_STUDENT_JOINRequest

Fetch eligible learner Zoom join handoff input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_PARENT_JOINRequest

Fetch eligible learner Zoom join handoff input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## API_ADMIN_ENROLMENTSRequest

List delivery enrolments without financial fields input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(held\|pending_payment\|active\|cancelled\|completed\|expired\|payment_exception) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_ENROLMENTRequest

Read educational enrolment status input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_ENROLMENT_CANCELRequest

Cancel educational access with auditable reason input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| access_ends_at | datetime | False | True | body | RFC3339 timezone-aware instant, UTC persisted |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_PARENT_CHECKOUT_CANCELRequest

Release own unpaid hold input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_ATTENDANCERequest

Read authorized session attendance roster input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | Optional exact student from authorized cohort learner/assigned roster read. Validate enrolment in session cohort before querying attendance; wrong cohort/inaccessible learner returns NOT_FOUND, not an empty absence result. |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## AttendanceViewPage

AttendanceViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AttendanceView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_TEACHER_ATTENDANCE_RECORDRequest

Record or amend attendance input Exactly one of If-Match (positive existing version) or If-None-Match:* (first creation) is required; both or neither -> VALIDATION_ERROR.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(present\|absent\|late\|excused) | True | False | body | Closed enum; reject unknown values |
| minutes_attended | integer | False | True | body | 0–240 |
| reason | string | True | False | body | Required change reason; no diagnoses or sensitive notes |
| If-Match | version | False | False | header | Current persisted AttendanceRecord.version for exact selected resource; required iff updating existing row. Mutually exclusive with If-None-Match. No guessed initial version; mismatch 409 VERSION_CONFLICT. |
| If-None-Match | string | False | False | header | Only literal * accepted. Required iff creating first row proven absent by authorized read. Mutually exclusive with If-Match; concurrent row creation returns 409 VERSION_CONFLICT. |

## API_ADMIN_ATTENDANCERequest

Read authorized session attendance roster input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | Optional exact student from authorized cohort learner/assigned roster read. Validate enrolment in session cohort before querying attendance; wrong cohort/inaccessible learner returns NOT_FOUND, not an empty absence result. |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_ATTENDANCE_RECORDRequest

Record or amend attendance input Exactly one of If-Match (positive existing version) or If-None-Match:* (first creation) is required; both or neither -> VALIDATION_ERROR.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(present\|absent\|late\|excused) | True | False | body | Closed enum; reject unknown values |
| minutes_attended | integer | False | True | body | 0–240 |
| reason | string | True | False | body | Required change reason; no diagnoses or sensitive notes |
| If-Match | version | False | False | header | Current persisted AttendanceRecord.version for exact selected resource; required iff updating existing row. Mutually exclusive with If-None-Match. No guessed initial version; mismatch 409 VERSION_CONFLICT. |
| If-None-Match | string | False | False | header | Only literal * accepted. Required iff creating first row proven absent by authorized read. Mutually exclusive with If-Match; concurrent row creation returns 409 VERSION_CONFLICT. |

## API_PARENT_ATTENDANCERequest

Read own or linked child attendance input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_ATTENDANCERequest

Read own or linked child attendance input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_QUIZZESRequest

List quiz authoring definitions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## QuizViewPage

QuizViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | QuizView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_QUIZRequest

Read quiz questions and grading keys input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_QUIZ_CREATERequest

Create draft formative quiz input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| pass_percent | integer | True | False | body | 0–100, default70 |
| max_attempts | integer | True | False | body | 1–5, default3 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_QUIZ_UPDATERequest

Edit draft quiz rules input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| pass_percent | integer | False | False | body | 0–100 |
| max_attempts | integer | False | False | body | 1–5 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_QUESTION_PUTRequest

Replace ordered draft questions atomically input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| questions | QuizQuestionView[] | True | False | body | 1–100; all correct option IDs reference that question; unique IDs and positions |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_QUIZ_DELETERequest

Delete unreferenced draft quiz input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_STUDENT_QUIZRequest

Read released quiz without answer key input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_STUDENT_ATTEMPTSRequest

Read own attempt history input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## QuizAttemptViewPage

QuizAttemptViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | QuizAttemptView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_STUDENT_ATTEMPT_CREATERequest

Start attempt with immutable quiz snapshot input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_STUDENT_ATTEMPT_SAVERequest

Save selections on own in-progress attempt input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| attempt_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| answers | QuizAnswer[] | True | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_STUDENT_ATTEMPT_SUBMITRequest

Submit once and release formative score input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| attempt_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| answers | QuizAnswer[] | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_TEACHER_QUIZ_RESULTSRequest

Read assigned learners submitted quiz scores input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_QUIZ_RESULTSRequest

Oversee submitted quiz outcomes input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_PARENT_QUIZ_RESULTSRequest

Read released child quiz results input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_ASSIGNMENTS_LISTRequest

List assignment/project authoring definitions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## AssignmentViewPage

AssignmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AssignmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_ASSIGNMENT_GETRequest

Read assignment authoring detail input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_ASSIGNMENT_DEFINERequest

Create assignment or project definition input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| kind | enum(assignment\|project) | True | False | body | Closed enum; reject unknown values |
| due_offset_days | integer | False | True | body | 0–365 |
| max_score | integer | True | False | body | 1–1000 |
| max_files | integer | True | False | body | 1–5 |
| rubric | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| passing_score | integer | True | False | body | 0–max_score |
| allow_resubmission | boolean | True | False | body | strict JSON boolean |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_ASSIGNMENT_EDITRequest

Edit draft assignment definition input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| due_offset_days | integer | False | True | body | 0–365 |
| max_score | integer | False | False | body | 1–1000 |
| rubric | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| passing_score | integer | False | False | body | 0–max_score |
| allow_resubmission | boolean | False | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_ASSIGNMENT_DELETERequest

Delete unreferenced draft assignment input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_STUDENT_ASSIGNMENTSRequest

Read permitted assignment and project work input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_PARENT_ASSIGNMENTSRequest

Read permitted assignment and project work input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_ASSIGNMENTSRequest

Read permitted assignment and project work input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_SUBMISSIONSRequest

Read own immutable submission history input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## SubmissionViewPage

SubmissionViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | SubmissionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_STUDENT_SUBMISSION_CREATERequest

Start own assignment submission/revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| previous_submission_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_STUDENT_SUBMISSION_SAVERequest

Save own draft work and ready scanned file links input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| body | text | False | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| asset_ids | uuid[] | True | False | body | 0–5 own ready submission-purpose assets; each<=25MiB; sum<=100MiB; unknown, duplicate or unready assets rejected |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_STUDENT_SUBMISSION_SENDRequest

Freeze own work and enqueue assessment notice input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_STUDENT_SUBMISSION_DELETERequest

Discard own unsubmitted draft input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_PARENT_SUBMISSIONSRequest

Read child submission status/history input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| assignment_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_SUBMISSIONSRequest

Read authorized submitted work review queue input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(submitted\|returned\|assessed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_SUBMISSIONRequest

Read authorized frozen work version input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_TEACHER_RETURNRequest

Return work for a new immutable revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | text | True | False | body | 1–2000 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_ASSESSMENTRequest

Save draft marking against frozen submission input Exactly one of If-Match (positive existing version) or If-None-Match:* (first creation) is required; both or neither -> VALIDATION_ERROR.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| score | integer | True | False | body | 0–assignment max_score |
| rubric_comment | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | False | False | header | Current persisted Assessment.version for exact selected resource; required iff updating existing row. Mutually exclusive with If-None-Match. No guessed initial version; mismatch 409 VERSION_CONFLICT. |
| If-None-Match | string | False | False | header | Only literal * accepted. Required iff creating first row proven absent by authorized read. Mutually exclusive with If-Match; concurrent row creation returns 409 VERSION_CONFLICT. |

## API_TEACHER_ASSESSMENT_GETRequest

Read permitted draft/released marking input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_TEACHER_ASSESSMENT_RELEASERequest

Release validated assessment to learner and guardian input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_ASSESSMENT_WITHDRAWRequest

Withdraw erroneous release and preserve correction history input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_FEEDBACK_LISTRequest

Read permitted feedback drafts/releases input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## FeedbackViewPage

FeedbackViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | FeedbackView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_TEACHER_FEEDBACK_CREATERequest

Create draft educational feedback input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_TEACHER_FEEDBACK_UPDATERequest

Revise draft feedback; released content requires withdrawal first input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_FEEDBACK_RELEASERequest

Release educational feedback and notify input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_FEEDBACK_WITHDRAWRequest

Withdraw mistaken feedback release with reason input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_TEACHER_PROGRESSRequest

Read permitted learner completion evidence input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ProgressViewPage

ProgressViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ProgressView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_SUBMISSIONSRequest

Read authorized submitted work review queue input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(submitted\|returned\|assessed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_SUBMISSIONRequest

Read authorized frozen work version input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_RETURNRequest

Return work for a new immutable revision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | text | True | False | body | 1–2000 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_ASSESSMENTRequest

Save draft marking against frozen submission input Exactly one of If-Match (positive existing version) or If-None-Match:* (first creation) is required; both or neither -> VALIDATION_ERROR.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| score | integer | True | False | body | 0–assignment max_score |
| rubric_comment | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | False | False | header | Current persisted Assessment.version for exact selected resource; required iff updating existing row. Mutually exclusive with If-None-Match. No guessed initial version; mismatch 409 VERSION_CONFLICT. |
| If-None-Match | string | False | False | header | Only literal * accepted. Required iff creating first row proven absent by authorized read. Mutually exclusive with If-Match; concurrent row creation returns 409 VERSION_CONFLICT. |

## API_ADMIN_ASSESSMENT_GETRequest

Read permitted draft/released marking input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_ASSESSMENT_RELEASERequest

Release validated assessment to learner and guardian input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_ASSESSMENT_WITHDRAWRequest

Withdraw erroneous release and preserve correction history input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_FEEDBACK_LISTRequest

Read permitted feedback drafts/releases input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_FEEDBACK_CREATERequest

Create draft educational feedback input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_FEEDBACK_UPDATERequest

Revise draft feedback; released content requires withdrawal first input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_FEEDBACK_RELEASERequest

Release educational feedback and notify input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_FEEDBACK_WITHDRAWRequest

Withdraw mistaken feedback release with reason input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_PROGRESSRequest

Read permitted learner completion evidence input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_ASSESSMENTSRequest

Read own/linked child released assessments input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## AssessmentViewPage

AssessmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AssessmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_STUDENT_FEEDBACKRequest

Read own/linked child released feedback input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_PROGRESSRequest

Read own/linked child released progress input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_CERTIFICATESRequest

Read own/linked child released certificates input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## CertificateViewPage

CertificateViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | CertificateView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PARENT_ASSESSMENTSRequest

Read own/linked child released assessments input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_PARENT_FEEDBACKRequest

Read own/linked child released feedback input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_PARENT_PROGRESSRequest

Read own/linked child released progress input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_PARENT_CERTIFICATESRequest

Read own/linked child released certificates input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ActivityCompletionView

ActivityCompletionView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lesson_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| block_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| completed | boolean | True | False | body | strict JSON boolean |
| reflection | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| completed_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## API_STUDENT_ACTIVITY_GETRequest

Read own activity/reflection status input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| lesson_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ActivityCompletionViewPage

ActivityCompletionViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ActivityCompletionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_STUDENT_ACTIVITYRequest

Record own non-graded activity and reflection input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| block_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| completed | boolean | True | False | body | strict JSON boolean |
| reflection | text | False | True | body | max2000, optional; no sensitive data prompts |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_STUDENT_LESSON_COMPLETERequest

Record own lesson acknowledgement input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| completed | boolean | True | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_COMPLETION_REVIEWRequest

Recompute and record completion decision from evidence input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| decision | enum(RECOMPUTE\|GRANT_OVERRIDE\|REVOKE_OVERRIDE) | True | False | body | Closed enum; reject unknown values |
| evidence_references | string[] | False | False | body | 1–10 nonempty verified evidence references required iff GRANT_OVERRIDE; forbidden for RECOMPUTE and REVOKE_OVERRIDE |
| override_id | uuid | False | False | body | Required iff REVOKE_OVERRIDE; must equal current active_override_id from history for this same enrolment. Forbidden for RECOMPUTE and GRANT_OVERRIDE; reject foreign/revoked overrides. |
| If-Match | version | True | False | header | CompletionReviewView.progress_version for enrolment_id; required for RECOMPUTE, GRANT_OVERRIDE and REVOKE_OVERRIDE; stale 409 VERSION_CONFLICT |

## API_ADMIN_CERTIFICATESRequest

List certificate issue/revocation state input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_CERTIFICATE_ISSUERequest

Issue completion certificate once from eligible progress input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_CERTIFICATE_REVOKERequest

Revoke incorrect certificate with reason input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| certificate_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_CERTIFICATE_REISSUERequest

Issue replacement linked to revoked certificate input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| certificate_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_PARENT_CHECKOUTRequest

Reserve seat and create server-priced hosted checkout input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| accepted_policy_ids | uuid[] | True | False | body | Current payment/cancellation policies |
| return_path | string | True | False | body | Allowlisted same-origin path; no arbitrary redirect |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_PARENT_CHECKOUT_RETRYRequest

Retry failed/expired checkout with fresh eligibility and seat check input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| return_path | string | True | False | body | Allowlisted same-origin |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_PARENT_PAYMENTSRequest

Read own family payment history input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(pending\|succeeded\|failed\|expired\|partially_refunded\|refunded\|exception) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PaymentViewPage

PaymentViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PaymentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PARENT_PAYMENTRequest

Read authoritative payment/checkout state input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_PARENT_RECEIPTSRequest

Read own immutable invoice/receipt documents input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ReceiptViewPage

ReceiptViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ReceiptView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_PARENT_REFUNDSRequest

Read own refund outcome input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## RefundViewPage

RefundViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | RefundView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_PRICESRequest

List current and historic fees input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PriceConfigViewPage

PriceConfigViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PriceConfigView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_PRICE_CREATERequest

Create effective dated course default/cohort override fee input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| price | PriceView | True | False | body | Validate referenced schema recursively |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | False | True | body | RFC3339 timezone-aware instant, UTC persisted |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_PRICE_RETIRERequest

End future pricing without changing purchase snapshots input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| price_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| active_until | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## API_ADMIN_PAYMENTSRequest

Inspect financial transactions and exceptions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| family_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(pending\|succeeded\|failed\|expired\|partially_refunded\|refunded\|exception) | False | False | query | Closed enum; reject unknown values |
| from | date | False | False | query | ISO8601 calendar date |
| to | date | False | False | query | ISO8601 calendar date |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## AdminPaymentViewPage

AdminPaymentViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AdminPaymentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_PAYMENTRequest

Read payment reconciliation references input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_PAYMENT_RECONCILERequest

Queue server-to-server reconciliation input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## API_ADMIN_DOCUMENTSRequest

Inspect immutable invoices/receipts input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_REFUNDSRequest

Inspect refund ledger input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_REFUND_CREATERequest

Request full/partial refund with explicit entitlement disposition input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| amount_minor | money | True | False | body | >0 and <= captured minus successful/pending refunds |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| access_disposition | enum(KEEP\|CANCEL) | True | False | body | Closed enum; reject unknown values |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_REFUND_RETRYRequest

Retry confirmed failed refund under same provider idempotency key input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| refund_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_REPORTRequest

Read bounded AUD gross/refund/net report input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | date | True | False | query | ISO8601 calendar date |
| to | date | True | False | query | <=366 days; >=from |

## API_ADMIN_REPORT_EXPORTRequest

Generate bounded finance CSV export input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | date | True | False | body | ISO8601 calendar date |
| to | date | True | False | body | <=366 days |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_PAGESRequest

Read public page drafts input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PublicPageViewPage

PublicPageViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PublicPageView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_PAGE_UPDATERequest

Save allowlisted public-page draft input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| slug | string | True | False | path | Known allowlisted key |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | Sanitize allowlisted semantic tags; scripts/styles/iframes forbidden |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_PAGE_PUBLISHRequest

Publish reviewed public page input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| slug | string | True | False | path | Known allowlisted key |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_POLICIESRequest

Read draft and published legal policies input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_POLICY_CREATERequest

Create immutable policy-version draft input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| key | enum(privacy\|terms\|child_safety\|consent) | True | False | body | Closed enum; reject unknown values |
| version_label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| requires_acknowledgement | boolean | True | False | body | strict JSON boolean |
| effective_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_POLICY_PUBLISHRequest

Publish policy with human/legal approval evidence input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| policy_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| approval_reference | string | True | False | body | Recorded human approval evidence |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_EVENT_LISTRequest

List event drafts and releases input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## EventViewPage

EventViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | EventView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_EVENT_CREATERequest

Create audience-scoped event input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| description | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | >starts_at |
| timezone | timezone | True | False | body | valid IANA timezone |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_EVENT_UPDATERequest

Revise draft event input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| event_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| description | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | >starts_at |
| timezone | timezone | True | False | body | valid IANA timezone |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_EVENT_PUBLISHRequest

Publish event and resolve recipients input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| event_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_EVENT_WITHDRAWRequest

Cancel or withdraw event and notify affected audience input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| event_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_PARENT_EVENTSRequest

Read relevant published events input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_EVENTSRequest

Read relevant published events input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_EVENTSRequest

Read relevant published events input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_ANNOUNCEMENT_LISTRequest

List announcement drafts and releases input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## AnnouncementViewPage

AnnouncementViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AnnouncementView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_ANNOUNCEMENT_CREATERequest

Create audience-scoped announcement input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_ANNOUNCEMENT_UPDATERequest

Revise draft announcement input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| announcement_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_ANNOUNCEMENT_PUBLISHRequest

Publish announcement and resolve recipients input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| announcement_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_ANNOUNCEMENT_WITHDRAWRequest

Cancel or withdraw announcement and notify affected audience input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| announcement_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_PARENT_ANNOUNCEMENTSRequest

Read relevant published announcements input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_STUDENT_ANNOUNCEMENTSRequest

Read relevant published announcements input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_TEACHER_ANNOUNCEMENTSRequest

Read relevant published announcements input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_PUBLIC_EVENTSRequest

Read explicitly public upcoming events input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_NOTIFICATIONSRequest

Read own recipient-scoped inbox input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| unread_only | boolean | False | False | query | strict JSON boolean |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## NotificationViewPage

NotificationViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | NotificationView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_NOTIFICATION_READRequest

Mark own notification read input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| notification_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| read | boolean | True | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_DELIVERIESRequest

Inspect redacted delivery errors input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(queued\|sent\|failed\|suppressed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## DeliveryViewPage

DeliveryViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | DeliveryView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_DELIVERY_RETRYRequest

Retry failed authorized delivery with deduplication input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| delivery_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_PARENT_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_STUDENT_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_TEACHER_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_ADMIN_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_FILE_UPLOADRequest

Closed purpose/context upload reservation. submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. Upload reservation never publishes an asset; publication requires explicit approved public-content linkage.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| filename | string | True | False | body | basename only,1–200 |
| media_type | string | True | False | body | Purpose allowlist: submission application/pdf,image/png,image/jpeg,text/plain,application/zip with constrained ZIP policy; resource PDF/PNG/JPEG/TXT or video/mp4; internal/public_asset PDF/PNG/JPEG/TXT only. Declared MIME must match independent sniffing; reject SVG/HTML/scripts. |
| size_bytes | integer | True | False | body | Strict positive bytes: submission <=26,214,400 (25MiB); resource PDF/PNG/JPEG/TXT <=52,428,800 (50MiB), MP4 <=524,288,000 (500MiB); internal/public_asset PDF/PNG/JPEG/TXT <=26,214,400 (25MiB). Submission attachment total <=104,857,600 (100MiB) checked under submission lock. |
| checksum_sha256 | string | True | False | body | base64 SHA256 |
| purpose | enum(resource\|submission\|internal\|public_asset) | True | False | body | Closed enum; reject unknown values |
| context_id | uuid | True | False | body | submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here. |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_FILE_CONFIRMRequest

Confirm upload and queue independent scanning input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_FILE_GETRequest

Read authorized file scan/metadata state input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_FILE_DOWNLOADRequest

Issue ready-file short-lived download input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_FILE_DELETERequest

Delete eligible unreferenced owned draft asset input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Exact FileAssetView.version for asset_id; lock FileAsset and recheck draft ownership, references, state and legal holds before compare-and-update; 409 VERSION_CONFLICT on mismatch |

## API_ADMIN_FILESRequest

Browse assets by permitted educational/operations purpose input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| purpose | enum(resource\|submission\|certificate\|internal\|public_asset) | False | False | query | Closed enum; reject unknown values |
| status | enum(quarantined\|scanning\|ready\|rejected\|deleted) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## FileAssetViewPage

FileAssetViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | FileAssetView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## CalendarExport

CalendarExport

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| content | string | True | False | body | RFC5545 text/calendar; UID stable; portal links only, no student name/host URL |
| content_type | enum(text/calendar) | True | False | body | Closed enum; reject unknown values |

## API_PARENT_CALENDARRequest

Export authorized family schedule with portal deep links input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | date | True | False | query | ISO8601 calendar date |
| to | date | True | False | query | <=93-day range |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |

## API_ADMIN_SETTINGSRequest

Read allowlisted non-secret operational settings input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## SettingViewPage

SettingViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | SettingView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_SETTING_PUTRequest

Set validated key with approval evidence for launch-sensitive values input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| key | enum(child_age_min\|child_age_max\|approved_child_interests\|support_email\|safeguarding_email\|business_phone\|policy_privacy_id\|policy_terms_id\|policy_child_safety_id\|required_consent_policy_ids\|retention_matrix_version\|retention_child_months\|retention_contact_days\|retention_delivery_days\|retention_certificate_years\|zoom_host_assignments\|google_calendar_id\|email_from_address\|approved_video_hosts\|enrolment_enabled\|public_publication_enabled\|retention_purge_enabled) | True | False | path | Closed key enum; key-specific type, value bounds and approval gate in SETTINGS_CATALOG |
| value | SettingValue | True | False | body | Validate referenced schema recursively |
| approval_reference | string | False | True | body | Required for age bands, policies, retention |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_FINANCE_SETTINGSRequest

Read merchant identity/tax configuration input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_FINANCE_SETTING_PUTRequest

Set approved merchant/tax/refund policy value input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| key | enum(retention_finance_years\|merchant_legal_name\|merchant_abn\|merchant_address\|tax_treatment\|tax_rate_basis_points\|refund_policy_id) | True | False | path | Closed key enum; key-specific type, value bounds and approval gate in SETTINGS_CATALOG |
| value | SettingValue | True | False | body | Validate referenced schema recursively |
| approval_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_INTEGRATIONSRequest

Read masked provider configuration and synchronization health input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## IntegrationStatusViewPage

IntegrationStatusViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | IntegrationStatusView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_INTEGRATION_UPDATERequest

Enable/disable provider using managed secret reference input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| provider | string | True | False | path | Known allowlisted key |
| enabled | boolean | True | False | body | strict JSON boolean |
| secret_reference | string | True | False | body | Approved secret-manager reference only, not credential bytes |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_INTEGRATION_CHECKRequest

Queue bounded provider connectivity check input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| provider | string | True | False | path | Known allowlisted key |

## API_ADMIN_INTEGRATION_RESYNCRequest

Queue provider mirror reconciliation input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| provider | string | True | False | path | Known allowlisted key |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## API_ADMIN_JOBSRequest

Read redacted job processing state input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(queued\|running\|succeeded\|failed\|dead_letter) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## JobViewPage

JobViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | JobView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_JOBRequest

Read authorized background operation status input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| job_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_JOB_RETRYRequest

Retry dead-letter job after cause correction input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| job_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_OPERATIONSRequest

Read actionable operational summary input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|

## API_ADMIN_AUDITRequest

Read filtered redacted audit history input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| actor_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| resource_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| action | string | False | False | query | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | <=31-day range |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## AuditViewPage

AuditViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AuditView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## PrivacyRequestView

PrivacyRequestView

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | enum(access\|correction\|deletion\|closure) | True | False | body | Closed enum; reject unknown values |
| student_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(requested\|verified\|processing\|completed\|rejected) | True | False | body | Closed enum; reject unknown values |
| decision_reason | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## API_PARENT_PRIVACY_REQUESTRequest

Request family data access/correction/deletion or account closure input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| kind | enum(access\|correction\|deletion\|closure) | True | False | body | Closed enum; reject unknown values |
| student_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| details | text | True | False | body | 1–2000 |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_PARENT_PRIVACY_LISTRequest

Read own privacy request state input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## PrivacyRequestViewPage

PrivacyRequestViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PrivacyRequestView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_PRIVACY_LISTRequest

Read restricted privacy work queue input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(requested\|verified\|processing\|completed\|rejected) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_PRIVACY_DECIDERequest

Record verified authority and retention-aware decision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| request_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| decision | enum(approve\|reject) | True | False | body | Closed enum; reject unknown values |
| verification_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

## API_PARENT_PRIVACY_EXPORTRequest

Get ready verified family export input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| request_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_LEGAL_HOLDRequest

Set or release audited retention hold input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| resource_type | enum(family\|student\|payment\|file) | True | False | body | Closed enum; reject unknown values |
| held | boolean | True | False | body | strict JSON boolean |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| approval_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | integer | True | False | header | Exact LegalHoldStateView.hold_version for this resource_type + resource_id; >=0. Zero requires hold row absent; positive requires matching RetentionHold.version. Never underlying resource version; mismatch/concurrent insert -> 409 VERSION_CONFLICT. |

## API_STRIPE_WEBHOOKRequest

Validate raw signature and persist deduplicated provider event input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| raw_body | string | True | False | body | Original bytes, <=1MiB |
| stripe_signature | string | True | False | body | Header HMAC timestamp within300s; no JSON reserialization |

## JOB_PAYMENT_PROCESSRequest

Retrieve authoritative provider state and activate paid seat safely input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| inbox_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_PAYMENT_RECONCILERequest

Compare Stripe state with immutable local ledger input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_HOLD_EXPIRERequest

Expire elapsed holds under row lock; release capacity input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cutoff | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## JOB_REFUND_PROCESSRequest

Execute idempotent requested refund and apply explicit access disposition input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| refund_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_DOCUMENT_GENERATERequest

Generate immutable receipt/invoice after verified payment input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_LIVE_CREATERequest

Create provider meeting from authoritative session version input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| expected_version | version | True | False | body | positive integer optimistic concurrency token |

## JOB_LIVE_UPDATERequest

Update/cancel meeting from latest authoritative session state input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| expected_version | version | True | False | body | positive integer optimistic concurrency token |

## JOB_LIVE_RECONCILERequest

Resolve provider drift without overwriting domain schedule input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| binding_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_CALENDAR_SYNCRequest

Upsert/cancel individual business calendar mirror event input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| resource_type | enum(session\|event) | True | False | body | Closed enum; reject unknown values |
| expected_version | version | True | False | body | positive integer optimistic concurrency token |

## JOB_CALENDAR_RESYNCRequest

Recover invalid sync token with full mirror reconciliation input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| integration_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_NOTIFICATION_PREPARERequest

Resolve outbox recipients and create deduplicated notices input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| outbox_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_EMAIL_SENDRequest

Deliver transactional email with durable local deduplication input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| delivery_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_REMINDER_SCHEDULERequest

Queue class reminders once per current session version input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| window_start | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| window_end | datetime | True | False | body | <=24h |

## JOB_FILE_SCANRequest

Verify metadata/MIME/archive limits/malware and promote immutable object input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| asset_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_FILE_CLEANRequest

Delete expired unreferenced staging objects after retention/hold checks input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cutoff | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## JOB_FILE_DELETERequest

Delete eligible private object/version per approved retention decision input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| asset_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| retention_decision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_PROGRESS_RECOMPUTERequest

Recalculate completion from latest released work and attendance evidence input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_CERTIFICATE_RENDERRequest

Render immutable certificate artifact and mark issued after ready storage input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| certificate_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_PRIVACY_PROCESSRequest

Generate protected export or execute approved retention-aware deletion/closure input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| request_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## JOB_RETENTIONRequest

Purge/anonymize only eligible unheld records from approved matrix input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| policy_version | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| cutoff | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## JOB_OUTBOX_DISPATCHRequest

Publish durable intent to queue and recover expired leases input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| batch_size | integer | True | False | body | 1–100 |

## JOB_INTEGRATION_CHECKRequest

Check configured provider and persist masked operational state input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| provider | enum(stripe\|zoom\|calendar\|resend\|storage) | True | False | body | Closed enum; reject unknown values |

## JOB_FINANCE_EXPORTRequest

Write formula-injection-safe CSV to private export storage input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| export_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

## ChildSubmissionStatusView

Parent support projection; no draft work body or files.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| attempt_number | integer | True | False | body | strict integer |
| status | enum(draft\|submitted\|returned\|assessed) | True | False | body | Closed enum; reject unknown values |
| submitted_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| late | boolean | True | False | body | strict JSON boolean |

## ChildQuizResultView

Parent only released result; no child draft answers.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| attempt_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| result | ReleasedQuizResult | True | False | body | Validate referenced schema recursively |

## ChildQuizResultViewPage

ChildQuizResultViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ChildQuizResultView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## ChildSubmissionStatusViewPage

ChildSubmissionStatusViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ChildSubmissionStatusView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_ASSIGNMENT_CLOSERequest

Close/reopen assignment submissions for a delivery input Exactly one of If-Match (positive existing version) or If-None-Match:* (first creation) is required; both or neither -> VALIDATION_ERROR.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| closed | boolean | True | False | body | strict JSON boolean |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | False | False | header | Current persisted AssignmentDeliveryRule.version for exact selected resource; required iff updating existing row. Mutually exclusive with If-None-Match. No guessed initial version; mismatch 409 VERSION_CONFLICT. |
| If-None-Match | string | False | False | header | Only literal * accepted. Required iff creating first row proven absent by authorized read. Mutually exclusive with If-Match; concurrent row creation returns 409 VERSION_CONFLICT. |

## API_ADMIN_BILLING_MEMBERRequest

Grant verified adult family billing visibility separately from child links input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| family_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| guardian_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| finance_approval_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| If-Match | version | True | False | header | Current AdminFamilyRelationshipsView.version for the same family; required even for first relationship; stale 409 VERSION_CONFLICT |

## API_ADMIN_BILLING_MEMBER_REVOKERequest

Revoke adult family financial membership input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| guardian_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| family_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Current matching BillingMembership.version from AdminFamilyRelationshipsView for family_id + guardian_id; never substitute Family.version; mismatch 409 VERSION_CONFLICT |

## ContactEnquiryView

Operations only; no child association inferred from enquiry.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(new\|handled) | True | False | body | Closed enum; reject unknown values |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

## API_ADMIN_ENQUIRIESRequest

Read inbound enquiries to support customers input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(new\|handled) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ContactEnquiryViewPage

ContactEnquiryViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ContactEnquiryView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_ENQUIRY_STATUSRequest

Mark enquiry handled without sending unauthorized messages input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enquiry_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(new\|handled) | True | False | body | Closed enum; reject unknown values |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

## API_ADMIN_PAID_EXCEPTIONRequest

Resolve late paid no-seat exception exactly once by allocation or refund input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| decision | enum(ALLOCATE\|REFUND) | True | False | body | Closed enum; reject unknown values |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected Payment aggregate version |
| Idempotency-Key | uuid | True | False | header | Payment+decision request dedupe;90d retention; body mismatch409 |

## AuthOutcomeView

Discriminated outcome: authenticated has session and null challenge/setup; mfa_challenge has one purpose-bound 5-minute challenge_token and null session/setup; mfa_setup_required has a 10-minute limited setup_token and null session/challenge. Partial authentication grants no teaching/admin API access.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(authenticated\|mfa_challenge\|mfa_setup_required) | True | False | body | Closed enum; reject unknown values |
| session | SessionView | True | True | body | Validate referenced schema recursively |
| challenge_token | token | True | True | body | opaque cryptographic token; max 512 characters; never logged |
| setup_token | token | True | True | body | opaque cryptographic token; max 512 characters; never logged |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## StaffSetupSessionView

Invitation establishes limited 10-minute MFA setup session only. Permitted operations are enrol MFA, confirm MFA, logout; no role data APIs.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| account | AccountView | True | False | body | Validate referenced schema recursively |
| setup_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

## MfaActivationView

Successful TOTP proof activates staff role session; setup credentials revoked atomically.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| session | SessionView | True | False | body | Validate referenced schema recursively |
| recovery_codes | string[] | True | False | body | 10 single-use high-entropy codes shown once |

## ReleasedQuestionFeedback

Own submitted attempt only; explanation is immutable approved quiz-version text. No cross-quiz key or hidden correct_option_ids returned.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| question_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| correct | boolean | True | False | body | strict JSON boolean |
| awarded_points | integer | True | False | body | strict integer |
| max_points | integer | True | False | body | strict integer |
| explanation | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |

## JOB_PAYMENT_DISCOVERYRequest

Discover provider-side payments/refunds and reconcile missing local references input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | body | <=24h range with overlap for eventual consistency |
| cursor | token | False | False | body | opaque cryptographic token; max 512 characters; never logged |

## StudentSelfProfileView

Own child profile only; no family identifiers, guardian contacts or financial fields.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | 1–80 |
| preferred_name | string | True | True | body | 1–80 |
| last_name | string | True | True | body | 1–80 |
| age_years | integer | True | False | body | 4–18 |
| age_recorded_on | date | True | False | body | ISO8601 calendar date |
| school_name | string | True | True | body | 1–160 |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | True | True | body | Closed enum; reject unknown values |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | True | False | body | Validate referenced schema recursively |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | True | True | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

## API_ADMIN_REPORT_EXPORT_STATUSRequest

Read own authorized financial report export status input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| export_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## API_ADMIN_REPORT_EXPORT_DOWNLOADRequest

Download ready private financial report export under finance scope input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| export_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

## ReconciliationExceptionView

Finance-only unknown/mismatched provider transaction evidence; no invented family/student owner.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| provider_transaction_id | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| provider_status | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| payment_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(open\|linked\|provider_reversed) | True | False | body | Closed enum; reject unknown values |
| first_seen_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| last_checked_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| reason_code | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| version | version | True | False | body | positive integer optimistic concurrency token |

## API_ADMIN_RECONCILIATION_EXCEPTIONSRequest

Inspect provider transactions unmatched to local financial records input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| status | enum(open\|linked\|provider_reversed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

## ReconciliationExceptionViewPage

ReconciliationExceptionViewPage

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | ReconciliationExceptionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## API_ADMIN_RECONCILIATION_EXCEPTION_RETRYRequest

Recheck provider truth and resolve only verified matching or reversed transaction input

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| exception_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

## API_ADMIN_TEACHING_CANDIDATESRequest

Education-only active teacher candidate lookup. No caller-controlled status or privilege filter.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |
| q | string | False | False | query | Optional trimmed display-name search; max80characters; parameterized query; no email search |

## TeachingCandidateView

Minimal adult teacher assignment reference; no private identity fields.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | Opaque teacher identifier, validated again at assignment write |
| display_name | string | True | False | body | Approved teacher display name, max160characters |

## TeachingCandidateViewPage

Education-scoped active teacher candidates with bounded opaque pagination.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | TeachingCandidateView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

## AccountDirectoryFilter

Internal typed identity-administration query filter; query values are validated before scoped repository use.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| q | string | False | False | query | Optional trimmed display-name or normalized adult-account email search,1–80 Unicode characters; parameterized matching; no credential, token, child-login-alias or MFA-secret search |
| role | enum(parent\|student\|teacher\|admin) | False | False | query | Optional closed role filter; does not authorize access |
| status | enum(invited\|pending_verification\|active\|suspended\|closed) | False | False | query | Optional closed account lifecycle filter; no implicit exclusion of suspended/closed accounts needed for lifecycle management |

## API_ADMIN_ACCOUNTSRequest

Identity-admin account directory query; bounded search and pagination, no secret or unconstrained expansion fields.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| q | string | False | False | query | Optional trimmed display-name or normalized adult-account email search,1–80 Unicode characters; parameterized matching; no credential, token, child-login-alias or MFA-secret search |
| role | enum(parent\|student\|teacher\|admin) | False | False | query | Optional closed role filter; does not authorize access |
| status | enum(invited\|pending_verification\|active\|suspended\|closed) | False | False | query | Optional closed account lifecycle filter; no implicit exclusion of suspended/closed accounts needed for lifecycle management |
| cursor | token | False | False | query | Opaque signed cursor bound to actor, capability, normalized filters, stable ordering and expiry; never client authority |
| limit | integer | False | False | query | 1–100; default25 |

## API_ADMIN_ACCOUNTRequest

Identity-admin read of one selected account and its current Account aggregate version.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| account_id | uuid | True | False | path | Opaque Account identifier selected from authorized AccountView result; resource scope checked again |

## AccountViewPage

Identity-admin account directory page. Items contain only the existing AccountView whitelist, including current Account.version; no credential/session/MFA secrets.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | AccountView[] | True | False | body | At most requested page limit; explicit AccountView projection only |
| page | PageMeta | True | False | body | Opaque stable cursor; no unbounded directory |

## PriceTargetFilter

Internal typed finance-only naming projection filter; no publication or existing-price prerequisite.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| kind | enum(course\|cohort) | False | False | query | Optional target discriminator filter |
| course_id | uuid | False | False | query | Optional existing course filter; normally selected from this same finance lookup, never a broader education directory |
| q | string | False | False | query | Optional trimmed course/cohort title search,1–100 characters; parameterized query; no learner/staff/financial-record search |

## API_ADMIN_PRICE_TARGETSRequest

Finance-admin minimal named course/cohort targets, including unpublished and unpriced records.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| kind | enum(course\|cohort) | False | False | query | Optional target discriminator filter |
| course_id | uuid | False | False | query | Optional existing course filter; normally selected from this same finance lookup, never a broader education directory |
| q | string | False | False | query | Optional trimmed course/cohort title search,1–100 characters; parameterized query; no learner/staff/financial-record search |
| cursor | token | False | False | query | Opaque signed cursor bound to actor, capability, normalized filters, stable ordering and expiry; never client authority |
| limit | integer | False | False | query | 1–100; default25 |

## PriceTargetView

Closed discriminated finance-only target identity projection. kind=course requires cohort_id,cohort_title,cohort_status all null. kind=cohort requires all three nonnull and matching course_id. Course/cohort publication or presence of a configured Price is not required. Titles/status provide context only; lookup never grants curriculum, roster, schedule or editing authority.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| kind | enum(course\|cohort) | True | False | body | Closed discriminator; conditional nullability constraints are mandatory |
| course_id | uuid | True | False | body | Existing Course ID; always present for either target kind |
| course_title | string | True | False | body | Current course title,1–200 characters; plain text only |
| course_status | enum(draft\|published\|archived) | True | False | body | Current Course lifecycle label only; no draft content |
| cohort_id | uuid | True | True | body | Null iff kind=course; otherwise existing cohort belongs to course_id |
| cohort_title | string | True | True | body | Null iff kind=course; otherwise current cohort title,1–200 characters |
| cohort_status | enum(draft\|open\|closed\|in_progress\|completed\|cancelled) | True | True | body | Null iff kind=course; otherwise current Cohort lifecycle label only |

## PriceTargetViewPage

Bounded finance-scope course/cohort naming projection; no price/education entity dump.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | PriceTargetView[] | True | False | body | Validate each discriminated target and conditional nullability; at most limit |
| page | PageMeta | True | False | body | Opaque cursor scoped to requesting finance principal and filters |

## GuardianStudentRelationshipView

Identity-only exact guardian-child relationship; no inference from sharing a family.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| family_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| guardian_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| student_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| status | enum(active\|revoked) | True | False | body | active iff revoked_at is null and verification is current |
| verified_at | datetime | True | False | body | RFC3339 verified relationship timestamp |
| revoked_at | datetime | True | True | body | RFC3339 or null while active |
| version | version | True | False | body | Current GuardianStudent.version for this guardian_id + student_id; required by guardian-link revocation |

## BillingMembershipStateView

Identity-only independently approved membership state. Contains no financial amounts, transactions, receipt identifiers or payment method data.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| family_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| guardian_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| status | enum(active\|revoked) | True | False | body | active iff revoked_at is null |
| granted_at | datetime | True | False | body | RFC3339 grant time |
| revoked_at | datetime | True | True | body | RFC3339 or null while active |
| version | version | True | False | body | Current BillingMembership.version for this family_id + guardian_id; required by membership revocation |

## AdminFamilyRelationshipsView

Identity-admin family management projection; parent FamilyView remains unchanged. Links and independent billing memberships are explicit, including revoked entries. Empty arrays are valid. Every nested family ID equals id.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| version | version | True | False | body | Current Family.version; creating or reactivating a link/membership requires this aggregate token |
| guardians | GuardianSummary[] | True | False | body | All existing family guardians; candidate selection for this same family only |
| students | StudentSummary[] | True | False | body | All existing family students visible under identity-admin purpose |
| guardian_links | GuardianStudentRelationshipView[] | True | False | body | Exact pairs only, including revoked state; do not fabricate Cartesian relationships |
| billing_memberships | BillingMembershipStateView[] | True | False | body | Independent membership rows only; absence means no grant |

## CompletionOverrideView

Education-admin-only completion override history; private evidence never appears in shared ProgressView.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| id | uuid | True | False | body | Override ID owned by the enclosing enrolment |
| enrolment_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| status | enum(active\|revoked) | True | False | body | active iff revoked_at is null |
| actor_id | uuid | True | False | body | Audited decision actor reference; no account directory expansion |
| reason | string | True | False | body | Audited decision reason, 1–200 characters |
| evidence_references | string[] | True | False | body | 1–10 verified evidence references; no evidence bodies |
| granted_at | datetime | True | False | body | RFC3339 timestamp |
| revoked_at | datetime | True | True | body | RFC3339 revocation timestamp or null |
| version | version | True | False | body | Current CompletionOverride row version for audit; mutation concurrency uses enclosing progress_version |

## CompletionReviewView

Education-admin read of one enrolment completion decision state from one consistent snapshot. Empty overrides is valid; a progress row is initialized when an enrolment activates. Before activation/initialization has completed, return INVALID_STATE with retryable progress initialization state; never synthesize progress_version=1 in a read.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| progress_version | version | True | False | body | Current StudentProgress.version including every recomputation, override grant or revocation; required completion-review If-Match |
| active_override_id | uuid | True | True | body | Null if no active override; otherwise exactly one active overrides[].id owned by this enrolment |
| overrides | CompletionOverrideView[] | True | False | body | Complete ordered decision history by granted_at,id for this single enrolment; only education-admin projection |

## API_ADMIN_COMPLETION_HISTORYRequest

Read one enrolment completion decision and override identities before any completion mutation.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| enrolment_id | uuid | True | False | path | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |

## LegalHoldTargetView

Identity-only retention target reference. Payment/file labels contain only resource type and opaque record reference; no amounts, currency, provider/customer identifiers, filename, MIME, contents, object keys or signed URLs.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_type | enum(family\|student\|payment\|file) | True | False | body | Closed target discriminator |
| resource_id | uuid | True | False | body | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| display_reference | string | True | False | body | Server-generated plain reference: resource type plus record ID; never derived from financial/file content |
| family_id | uuid | True | True | body | Associated family only when already represented by identity-authorized ownership; null for non-family operational/public assets |
| student_id | uuid | True | True | body | Associated student only when directly owned; null otherwise; no inferred household sibling data |

## LegalHoldTargetViewPage

Bounded purpose-scoped page; filter before projection and pagination.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | LegalHoldTargetView[] | True | False | body | At most requested limit; whitelist nested fields |
| page | PageMeta | True | False | body | Stable opaque cursor bound to actor, scope and filters |

## LegalHoldStateView

Identity-only retention hold aggregate state. A missing hold row is an explicit immutable read result: hold_id=null, held=false, hold_version=0, reason/approval_reference=null. Reading never creates a row.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_type | enum(family\|student\|payment\|file) | True | False | body | Same type as selected target |
| resource_id | uuid | True | False | body | Same ID as selected existing target |
| hold_id | uuid | True | True | body | Persisted RetentionHold ID, null only when no row exists |
| held | boolean | True | False | body | Current legal hold state; false if no hold row |
| hold_version | integer | True | False | body | >=0; zero only means no hold row for this exact (resource_type, resource_id), otherwise current RetentionHold.version>=1; never underlying Payment/File/Family/Student version |
| reason | string | True | True | body | Latest audited hold decision reason, 1–200 characters; null only for absent row |
| approval_reference | string | True | True | body | Latest audited approval reference, 1–200 characters; null only for absent row |

## API_ADMIN_LEGAL_HOLD_TARGETSRequest

Identity-only bounded retention target selector, usable without financial or file read privileges.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_type | enum(family\|student\|payment\|file) | True | False | query | Required target kind; restrict query to one underlying table |
| family_id | uuid | False | False | query | Optional exact existing family selected from authorized identity reads; restrict targets by actual owned resource links, not arbitrary cross-family associations |
| cursor | token | False | False | query | Opaque signed cursor bound to actor, capability, normalized filters and expiry |
| limit | integer | False | False | query | 1–100; default 25 |

## API_ADMIN_LEGAL_HOLD_STATERequest

Read current independent hold state for an existing typed target.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| resource_id | uuid | True | False | path | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| resource_type | enum(family\|student\|payment\|file) | True | False | query | Exact discriminator from selected LegalHoldTargetView |

## EducationLearnerView

Cohort-scoped education-admin selector for both empty feedback forms and existing educational records. No surname, age, school, contacts, family IDs, identity account details or financial state.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| student_id | uuid | True | False | body | Existing student attached to this cohort enrolment; not an identity-directory grant |
| display_name | string | True | False | body | Preferred name when nonblank, otherwise first_name; 1–80 characters; no surname |
| enrolment_id | uuid | True | False | body | Existing enrolment belonging to this student and cohort; selected reference for learning/attendance/completion queries |
| cohort_id | uuid | True | False | body | Equals path cohort_id |
| education_status | enum(reserved\|active\|cancelled\|completed\|expired) | True | False | body | held/pending_payment/payment_exception map to reserved; active/cancelled/completed/expired map unchanged. Never expose payment/provider status. |

## EducationLearnerViewPage

Bounded purpose-scoped page; filter before projection and pagination.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| items | EducationLearnerView[] | True | False | body | At most requested limit; whitelist nested fields |
| page | PageMeta | True | False | body | Stable opaque cursor bound to actor, scope and filters |

## API_ADMIN_COHORT_LEARNERSRequest

Bounded named learner selector restricted to an explicit existing educational cohort.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| q | string | False | False | query | Optional preferred/first-name search,1–80 characters; parameterized within cohort scope |
| cursor | token | False | False | query | Opaque signed cursor bound to actor, capability, normalized filters and expiry |
| limit | integer | False | False | query | 1–100; default 25 |

## FileUploadContext

Internal repository DTO only; never a client-minted authorization grant. Each branch is constructed from current source rows and authenticated scope. No HTTP endpoint returns or accepts this internal scope.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| purpose | enum(submission\|resource\|internal\|public_asset) | True | False | body | Closed discriminator |
| context_id | uuid | True | False | body | Exact typed source ID |
| owner_account_id | uuid | True | False | body | Authenticated upload owner; for internal/public_asset equals context_id |
| context_kind | enum(submission\|curriculum_revision\|account_asset_collection) | True | False | body | submission->submission; resource->curriculum_revision; internal/public_asset->account_asset_collection |
| writable | boolean | True | False | body | Must be true to reserve/confirm/delete a draft asset; derived current state |
| max_size_bytes | integer | True | False | body | Positive exact purpose/media-type cap from server policy; never client chosen |

## AssessmentStateView

Teacher/education-admin marking state for one authorized frozen submission. assessment=null means precisely no persisted assessment, after submission scope/state validation. Missing/inaccessible submission returns NOT_FOUND; GET never creates rows.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| submission_id | uuid | True | False | body | Same authorized frozen submission as path |
| assessment | AssessmentView | True | True | body | Current persisted assessment including exact version, or null if absent |

## AssignmentClosureView

Education-admin-only per-delivery closure state, independent of immutable assignment definition version. If no rule exists, rule_exists=false, version=null, closed=false and due_at is deterministically derived from the cohort/pinned definition. GET never persists a default.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| assignment_id | uuid | True | False | body | Assignment belongs to cohort pinned curriculum revision |
| cohort_id | uuid | True | False | body | Existing authorized educational cohort |
| rule_exists | boolean | True | False | body | True iff assignment_delivery_rules contains this exact assignment/cohort pair |
| version | version | True | True | body | Current AssignmentDeliveryRule.version when rule_exists=true; null iff no row. Never AssignmentView.version. |
| closed | boolean | True | False | body | Existing rule value, or false for absent rule; cohort completion may still block submissions separately |
| due_at | datetime | True | True | body | Existing saved due time or deterministic pinned-assignment/cohort resolution; null iff no due offset |
| reason | string | True | True | body | Latest closure reason; null for no explicit rule |

## API_ADMIN_ASSIGNMENT_CLOSURERequest

Read exact delivery closure state without modifying immutable assignment definition.

| Field | Type | Required | Nullable | Location | Validation |
|---|---|---|---|---|---|
| cohort_id | uuid | True | False | path | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
| assignment_id | uuid | True | False | path | Existing opaque UUID; purpose-scoped lookup; IDs never grant access |
