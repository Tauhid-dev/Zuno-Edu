# Aggregates and transaction boundaries

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

An aggregate is the smallest consistency boundary whose invariants must change together. It is not a database table. Entities inside an aggregate are mutated through its root. Larger read screens use projections and do not enlarge aggregate transaction ownership.

| Root | Owned state | Atomic boundary / concurrency | External references |
| --- | --- | --- | --- |
| Account | Credential and role representation; sessions separately revocable security records | Account role/status/password change and session invalidation with audit | Guardian,StudentProfile,TeacherProfile reference account by ID |
| Family | Guardian memberships, GuardianStudent links, BillingMembership grants | Verify/revoke explicit links; child creation and initial link same transaction; preserve active guardian invariant | StudentProfile,Account |
| StudentProfile | Names, AgeSnapshot and optional educational fields | Version-controlled profile edits; no automatic DOB inference | Family via foreign key |
| Course | Marketing metadata, publication pointer | Publish only ready published revision of same course | Program,CurriculumRevision |
| CurriculumRevision | Modules, Lessons, LessonBlocks, resources, Quiz/Assignment definitions | Draft edit locks revision version; freeze all children at publication; no published edits | Course,ready FileAsset |
| Cohort | Delivery metadata, pinned revision and teacher-grant relationships | Capacity/state change locks cohort; cannot reduce below active+live holds | Course,revision |
| ClassSession | One occurrence and authoritative schedule state | Lock schedule participants in deterministic sorted order; no overlapping teacher/cohort/learner session; audit+outbox same commit | Cohort,teaching assignments,provider binding |
| Enrolment | Reservation and educational entitlement | Lock Cohort then Enrolment; unique live child/cohort;30m hold; verified payment activation | StudentProfile,Cohort,Payment |
| Payment | Immutable purchase snapshot, append-only provider/payment events, Refund children and purchase document evidence | Lock Payment then Enrolment then Cohort for exception/refund allocation; all cross-module locking uses same global sorted lock order; pending+success refunds never exceed capture | Enrolment,Family |
| QuizAttempt | Frozen quiz snapshot, own saved selections and released result | Lock enrolment/quiz attempt-counter key; enforce max attempts and one in-progress; idempotent submit | Published Quiz definition |
| Submission | One attempt text and asset references | Draft mutable; submission freezes files/text; return creates linked successor | Assignment,Enrolment,FileAsset |
| Assessment / TeacherFeedback | Current state and immutable revisions | Version checks; explicit release/withdraw; outbox recompute/notify | Frozen Submission or learner/cohort |
| AttendanceRecord | One learner/session status | Unique student/session; amendment reason; update attendance and outbox atomically | ClassSession,Enrolment |
| StudentProgress | Derived counts, ActivityCompletion records, CompletionOverride evidence | Rebuild projection from authoritative evidence; override adds evidence only; certificate eligibility serialized by enrolment key | Released assessments/quiz attempts and attendance |
| Certificate | Immutable issue snapshot, asset reference, replacement/revocation lineage | Unique current certificate per enrolment; idempotent render request; revoke remains visible | StudentProgress,FileAsset |
| Event / Announcement | One versioned audience-scoped publication | Publish/withdraw with audience notice outbox | Audience relationships,Calendar binding |
| Notification | Recipient inbox state and delivery ledger | Unique recipient/source/type and separate channel dedupe; read owned by recipient | Account,outbox source |
| FileAsset | Quarantine/scan/promotion metadata, immutable final key | Compare checksum/type/size; mark ready only after promotion confirmed; no referenced/held delete | Explicit authorized resource links |
| ApplicationSetting / IntegrationBinding | Typed config or desired/applied provider version | Optimistic version; secret references only; desired version never rolls back from stale worker result | Provider managed secrets |
| PrivacyRequest | Authority verification, decision, export/retention evidence | Approval precedes processing; legal holds block purge; closure cannot orphan active child | Family,StudentProfile,protected artifacts |
| Outbox / Inbox / BackgroundJob | Durable intent/dedupe/lease processing state | Unique source keys, SKIP LOCKED claims, finite lease, idempotent consumers | Application aggregates by opaque ID |


Global lock order prevents deadlocks: acquire required aggregate advisory keys sorted by stable `(module, id)` before row locks; never mix ad-hoc order from individual services. Cohort capacity uses the same cohort lock for checkout, hold expiry, capacity edit, payment activation and paid-exception allocation. Refund balance and paid-exception decision share the Payment lock. Recheck all predicates inside the transaction after lock acquisition. Version changes return409 and the current safe resource projection must be refetched; retries cannot discard a user's newer edits.

Domain event handlers cross aggregate boundaries after commit unless a listed business invariant requires one local transaction. Outbox insertion always participates in the originating transaction. Providers cannot take part in a database transaction. Reserve intent, commit, call provider, then record verified outcome in a new transaction; unknown outcomes remain reconcilable and do not invent success.

## Mutation ownership clarifications

RetentionHold is the independent aggregate keyed by resource_type/resource_id. It is stored in retention_holds, carries its own positive persisted version and remains after release; absence is represented read-only by hold_version 0. Hold mutation and purge use common typed-resource/ancestor advisory keys before row locks.

AssignmentDeliveryRule is the independent delivery aggregate keyed by assignment_id/cohort_id. Its version never reuses the immutable published assignment definition token. An absent rule has no persisted version; first writes use conditional absence, and closure shares a lock with submission finalization.

Family keeps its root version and child link/membership row versions. Relationship creation compares the root version; revocation compares the exact child row version while holding the root lock. Both root and changed child increment atomically. Account owns RoleGrant's version; two independent counters must not be introduced.

Attendance and assessment first writes assert absence under their unique keys before inserting version 1. Existing writes compare their own current version, and reads never create placeholder rows. StudentProgress initialization is a durable activation consumer; completion review remains unavailable until its persisted row exists. Every recompute/override change increments that same progress version while preserving private override evidence and immutable source work.
