# Data model and minimization

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

Canonical personal-data fields and retention classes are in [DATA_REQUIREMENTS](../product/DATA_REQUIREMENTS.md). [DATABASE_SCHEMA_PLAN](DATABASE_SCHEMA_PLAN.md) defines physical nullability, keys, constraints, indexes and deletion for every table; [AGGREGATES](AGGREGATES.md) defines transactional ownership. Request/response fields are in API_CATALOG and must be checked independently of database columns.

## Child registration contract

| Field | Required / validation | Purpose | Authorized visibility |
| --- | --- | --- | --- |
| first_name | Required, Unicode1–80 after trim | Required student name; single-name children supported | Linked guardian and identity admin write; own student/assigned teacher display |
| age_years | Required strict integer4–18 | Adult assertion for age-appropriate educational eligibility | Guardian/admin write; own student and assigned teacher read |
| age_recorded_on | Required server-generated date | Records age assertion timing; reconfirm at new enrolment if older than180d | Same as age; never infer or increment guessed DOB |
| preferred_name | Optional nullable,1–80 | Chosen classroom display; fallback to first_name | Guardian/admin and own student write; assigned teacher read |
| last_name | Optional nullable,1–80 | Optional family record/certificate preference | Guardian/identity admin and own student read; default teacher projection excludes |
| school_name | Optional nullable,1–160 | Family-provided educational context | Guardian/identity admin and own student read; default teacher projection excludes |
| school_year | Optional nullable closed Foundation,Year1–12,other,not_specified | Educational tailoring without school-system assumption | Guardian/admin write; own student/assigned teacher read |
| interests | Optional,<=10 unique topics from approved catalog | Relevant teaching examples without sensitive free text | Guardian/admin and own student write; assigned teacher read |
| prior_experience | Optional nullable none/some/experienced/prefer-not-to-say | Adjust teaching support | Guardian/admin and own student write; assigned teacher read |
| student account | Optional until guardian provisioning; opaque username; no child email | Independent safe learning login | Guardian step-up provisioning; student sign-in; staff support narrowly audited |


Initial approved interest vocabulary is artificial_intelligence, coding, robotics, creative_design, games, data and online_safety. `approved_child_interests` selects a reviewed subset; unknown values are rejected. Blank optional strings normalize to null; omission means unchanged on PATCH. Exact date of birth, health diagnoses, child email/phone/address, government identifiers, biometrics and arbitrary learning notes are not collected. Age4–18 is the explicit proposed technical boundary; approved production course/age-band settings must pass HG-AGE before enrolment starts.

## Relationships and lifecycle

Family1→many Students and Family1→many Guardians are administrative containers. Parent access to a Student requires the explicit active GuardianStudent many-to-many relation with matching family keys. An adult's BillingMembership is independently authorized. An empty family is valid: registration creates Family+Guardian+initial billing membership, and adding a first child creates Student+initial guardian link in one transaction. Reading family/dashboard filters child rows to current links and never assumes one already exists.

Program1→many Courses, Course1→many immutable CurriculumRevisions, revision1→many Modules→Lessons→typed Blocks, and Course1→many Cohorts express reuse. Every Cohort pins a published revision; every session/assignment reference is constrained to it. Enrolment joins one student to one cohort. Attendance belongs to one enrolled student/session. QuizAttempt and Submission belong to student+enrolment+immutable published definition. Assessment belongs to a frozen submission version; feedback belongs to learner/cohort and optional frozen work. A resource with a valid UUID remains inaccessible unless these relationships and publication/release states authorize it.

StudentProgress stores derived counts and never overwrites marks or attendance. Standard completion is all required items plus>=80% delivered non-cancelled attendance; CompletionOverride is separate immutable evidence with reason/actor/revocation. Certificates retain immutable issue snapshots and reissue lineage, while personal display data can be anonymized under approved retention. No public child-name certificate search is designed.

Prices are effective-dated integer AUD values; Payment snapshots price, merchant, tax and purchaser at checkout. CheckoutAttempt captures every provider session retry without changing purchase truth. Payment success, enrolment access, Refund and purchase-document statuses remain separate. Parent financial DTOs never expose card data or unrestricted provider metadata. Refunds preserve captured-balance constraints and explicit KEEP/CANCEL educational disposition.

Event/Announcement audiences contain target kind plus recipient role filter and optional course/cohort FK. Course audiences resolve across its cohorts; cohort audiences resolve exact current enrolments, guardian links and teaching assignments. Delivery notices snapshot only needed recipient IDs, and subsequent reads still check current ownership. FileAsset stores private metadata and object references; explicit FK asset links determine access. Presigned URLs and meeting host URLs are ephemeral credentials and never durable profile fields.

## Retention and deletion

Child educational/profile records and uploads: active service plus24months. Optional enquiries:90days after closure. Delivery metadata:90days with safe dedupe hash1year. Application logs:30days. Security/admin audit:1year; financial records/audit and certificate metadata:proposed7years. Expired session metadata:30days; unused adult recovery token:30minutes. Unfinalized objects:24hours. Database base backups:35days with7-day PITR; deleted object versions:35days. These are proposed defaults requiring HG-LEGAL and finance approval where relevant, not statements of legal sufficiency.

Retention applies by data purpose, not whole account: retaining a payment does not authorize retaining unnecessary child work. Suspend/archive revokes access without immediate erasure. Verified privacy workflow resolves request authority, retention and legal hold, schedules deletion/anonymization, deletes eligible object versions and appends minimal decision evidence. Active holds block all purge paths. A restore must reapply approved deletion tombstones before reopening access. Normal APIs have no hard-delete route for paid transactions, released assessment history, audit records or published curriculum.

## Separate delivery and retention state

assignment_delivery_rules stores AssignmentDeliveryRule, independent of the immutable assignment definition. retention_holds stores RetentionHold, independent of the target's version. Both retain their own positive persisted counters; missing rows are explicitly represented by their read contracts, never initialized by GET. Attendance/assessment first writes use conditional absence with unique-key protection. Family root and guardian-link/billing-membership rows have distinct counters with atomic update rules; RoleGrant instead uses its owning Account counter.

The named education learner selector joins enrolments to only student id/first_name/preferred_name after cohort scope validation. Identity-only hold reference queries project target IDs and established family/student relationships, never financial values or file content. These are column-whitelisted read projections, not additional domain models or databases.
