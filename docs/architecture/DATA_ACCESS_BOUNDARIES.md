# Data access boundaries

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

The database is shared; visibility is not. Authoritative relationship predicates and purpose-specific columns apply to every list, detail, dashboard, file grant, report, export and background notification recipient selection. IDs are opaque but secrecy of an ID is never a security control.

| Projection | Allowed columns/data | Excluded data | Repository predicate |
| --- | --- | --- | --- |
| PublicCourse / PublicCohort | Published title/outcomes/age/duration/price and timetable/enrolment window | Draft curriculum, roster,capacity counters,meeting secrets,payment records | Published course+published eligible cohort projection |
| Parent StudentProfile | Linked child required/optional registration data | Unrelated siblings,staff private notes,other family records | Active GuardianStudent AND same family candidate key |
| FamilyView | Own adult summary and individually linked child summaries | Every unlinked family sibling;billing access inferred from child relation | Own active adult family membership;child rows joined per guardian |
| Student self | Own profile presentation,age,optional own registration values | Family contacts/administration,money,roles,peer data | Authenticated account linked to exactly own student ID |
| TeachingStudentView | First/preferred name,age as-of,school year,interests,experience | Family ID,email,phone,school name,optional surname by default,billing | Active teacher assignment AND requested learner enrolment |
| Learner curriculum | Released modules/lessons/blocks of pinned revision,ready resources | Draft revisions,unreleased future content,quiz keys | Own eligible enrolment AND revision pin AND release timestamp |
| Learner result | Own submitted quiz correctness/explanation and released assessment/feedback | Unsubmitted quiz key,draft marks,other child work | Own/linked identity AND submitted/released state in WHERE clause |
| Parent submission status | Assignment,attempt,status,submitted time,late flag | Child unsubmitted body and uploaded files | Linked child scope,summary-only SQL projection |
| PaymentView / ReceiptView | Billing-family amount/status/date/refund total,immutable purchase documents | Card data,otherfamily payments,raw webhook/provider payload | Independent active BillingMembership;finance admin separate scope |
| Finance admin | Ledger references,reconciliation,state,amounts and approved report | Teacher learning notes,full submission bodies,unneeded profile fields | finance_admin scope;explicit finance projection |
| File grant | Opaque asset metadata then<=60s download ticket | Bucket keys,credentials,unsafe asset,permanent links | Ready + owning educational/finance resource authorization |
| Audit view | Redacted actor/action/target/reason/time/correlation | Passwords,session/MFA tokens,host URLs,card data,child work bodies | audit_admin scope;bounded audited query |
| Worker identity | Exact durable job source IDs needed by handler | Arbitrary browser-selected internal privilege | Trusted worker entrypoint+job kind capability+current source state |


The application mints scope from current database relationships; a scope is never serialized as client authority. Repository APIs require it and may return no row rather than an unauthorized object. Purpose-specific admin scopes are explicit. Responses whitelist fields; domain/ORM conversion via `__dict__`, generic model serialization or expanding arbitrary relationships is forbidden. Cache entries include principal/scope/release version; private responses are no-store and never shared CDN content.

File authorization follows explicit FK links to a resource, submission, certificate or published asset. The FileAsset owner is necessary for draft uploads but insufficient for making a resource public. Direct S3 access is private; every signed grant is a bearer credential with short expiry. Receipt/finance CSV downloads use BillingService/ReportingService grants under finance scope, not generic education file privileges. Privacy export construction splits educational and finance datasets by independently verified authority; an adult receives no other guardian's unrelated payments.

Teacher financial prohibition is structural: teacher use cases do not depend on PaymentRepository, teacher API schemas do not contain finance DTOs, query scope never grants finance, frontend teacher modules do not import financial features, and negative tests try every finance operation class. Revoking a teacher assignment, guardian relation, billing membership or user session invalidates access on the next request even when earlier pages remain open.

Education assignment candidate lookup uses API-ADMIN-TEACHING-CANDIDATES and UserRepository.list_assignment_candidates. The current education-admin scope can see only approved active teacher id/display_name references; private teacher contacts, account security, identity administration and financial data remain excluded. Search/pagination is scoped before projection. Assignment writes recheck teacher state, approval and conflicts; a prior candidate result is not authority.

## Privileged selectors and mutation state

| Projection | Exact authority and permitted data | Explicit exclusions |
| --- | --- | --- |
| AdminFamilyRelationshipsView | identity_admin; named existing family guardians/students, exact guardian-child pairs, independently approved billing memberships and each current row version | Payment amounts, transactions, receipts; no parent projection expansion |
| CompletionReviewView | education_admin; one authorized enrolment's persisted progress_version, active override ID and audited override history | Guardian/contact/financial data; override evidence in parent/student/teacher progress |
| LegalHoldTargetView / LegalHoldStateView | identity_admin; typed resource identity and already represented ownership references, then independent hold state/version and decision references | Amount/currency/provider identifiers; filename/MIME/file content/storage keys/signed URLs; finance/file read capability |
| EducationLearnerView | education_admin; one cohort's student_id, first/preferred display name, enrolment_id, cohort_id and coarse educational state | Surname, age, school, contact/family/account data and payment/provider state; identity directory access |
| AssignmentClosureView | education_admin; selected cohort's pinned assignment delivery rule, existence and separate version | Mutation of published assignment definition |

Legal-hold target listings include records with no hold row. Optional family filtering follows existing resource ownership links and does not expose unrelated family data. Operational/public assets without a family association remain nullable references. A resource type and opaque display reference identify payment/file targets without exposing their contents. Repository methods whitelist these columns and never hydrate broader Payment/FileAsset objects for identity admins.

Education learner selection is independent of existing feedback/assessment rows, so a first feedback can select an eligible learner from the cohort. Queries require an explicit cohort and filter before pagination. Downstream attendance, feedback, assessment and completion services recheck that learner/enrolment/cohort correspond and that the resource state permits the action. Existing teacher assigned-roster APIs remain the teacher source.
