# Role capabilities

Status: DRAFT; scope candidate 1.0. Authorization is role/capability + resource ownership + active relationship/assignment + resource state. Deny by default at API, application service and scoped repository/query boundaries. Navigation is a usability boundary only.

| Capability/data | Public | Parent | Student | Teacher | Admin |
|---|---|---|---|---|---|
| Published business/catalogue/policy content | Read | Read | Read | Read | Publish with relevant grant |
| Parent account/contact | None | Own only | None | None | identity_admin, necessary support projection |
| Student profile | None | Active verified guardian links | Own safe projection | Active assigned learner educational projection | education_admin/identity_admin by purpose |
| Guardian relationships | None | View own links, no discovery/link mutation | None | None | identity_admin, verified and audited |
| Billing-family membership | None | Own active memberships | None | None | identity_admin/finance_admin by operation |
| Curriculum | Published overview only | Published catalogue and child's progress view | Released enrolled version | Assigned curriculum and teaching resources | education_admin manage/publish |
| Cohort/session schedules | Published metadata | Authorized child schedules | Own enrolled schedules | Assigned schedules | education_admin manage |
| Schedule changes | None | No direct mutation | None | Assigned, future, notice/conflict rules | education_admin with reason for exceptions |
| Zoom join/start | None | Assist authorized child's entry, no host credentials | Own active enrolment, join window | Assigned host, start window | Operations diagnostics; host action needs explicit assigned host authority |
| Attendance | None | Authorized child view | Own view | Record/amend assigned roster within window | education_admin oversight/correction |
| Assignment/submission | None | Child status and permitted submitted artifacts | Own eligible submissions | Assigned learners | education_admin oversight |
| Draft assessment/feedback | None | None | None | Assigned educators | education_admin |
| Released results/feedback | None | Authorized child | Own | Assigned learners | education_admin |
| Progress/certificates | None | Authorized child | Own | Assigned progress; certificate existence only | education_admin issue/revoke/override |
| Events/announcements | Explicit public audience | Relevant audience | Relevant audience | Relevant audience | education_admin/operations_admin publish relevant scopes |
| Notifications | None | Own recipient records | Own recipient records | Own recipient records | Own inbox; operations_admin delivery diagnostics |
| Prices | Published fee only | Published fee/own order | No portal finance; public prices remain public | Public fee only | finance_admin mutation |
| Payments/invoices/receipts | None | Active billing-family membership | None | **Denied** | finance_admin |
| Refunds/financial reports | None | Own refund outcome only | None | **Denied** | finance_admin |
| Integration settings | None | None | None | None | operations_admin; references only, never secret values |
| Audit records | None | No general audit access | None | No general audit access | audit_admin, least-data projection |
| Role grants | None | None | None | None | identity_admin with incompatible-role checks |

## Account and relationship rules

A parent account may have authorized guardian links to multiple children. A student may have multiple verified authorized guardians. Each child record has an owning family for administration, but guardian educational access is checked by the explicit GuardianStudent relationship. A billing record has one owning family. A guardian relationship alone does not grant billing membership to another family. Parents cannot search unrelated children or create guardian links by guessing names, emails or IDs. Administrators approve additional links only after verified authority and record the reason.

Student account provision/reset is initiated by an active guardian or authorized identity administrator. Child email, phone and DOB are not required. Students cannot alter age, roles, guardian links or billing data. Suspension/revocation invalidates sessions and permissions immediately. Closing a guardian account must first ensure that each active child retains an authorized adult or enters an explicit support-controlled suspension; never orphan an active child silently.

A teaching assignment references a cohort and, where needed, a session exception and validity period. Protected reads evaluate the current assignment at request time. Teacher data includes display name, age-as-of, authorized optional educational context, enrolment and learning records needed for the operation. It excludes adult contact, payment, receipt, invoice, refund, card/provider finance metadata and business reports. Teacher assignment does not grant global course administration.

Administrative capabilities are identity_admin, education_admin, finance_admin, operations_admin and audit_admin. Assign only necessary groups. A principal with Teacher role must not hold finance-admin capability or acquire it through another additive role; a person who performs both jobs must use a separate MFA-protected administrator principal. Identity changes require audited authorized grants; profile updates cannot grant roles. A student principal cannot become Parent/Teacher/Admin through self-service.

## Required negative evidence

AUTH-012 requires tests that directly manipulate requests and identifiers, not merely hide menus. Teacher→payment and teacher→unassigned learner fail at API/service/query scope. Parent→another family's child or bill fails. Student→another submission or billing fails. Non-finance admin→refund/report fails. A revoked guardian or expired teacher assignment fails even with an existing session and previously valid resource ID. Draft curriculum/assessment/feedback remains inaccessible to family/student. Staff role-combination attempts cannot restore teacher finance access.
