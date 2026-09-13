# Permission matrix

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

`Own` means authenticated subject; `linked` requires active verified GuardianStudent; `billing family` is independent active BillingMembership; `assigned` requires current teacher grant and relevant learner enrolment. All reads also obey publication/release/state rules. Each API_CATALOG role/ownership row is the exact operation contract.

| Capability / data | Public | Parent | Student | Teacher | Admin privilege |
| --- | --- | --- | --- | --- | --- |
| Published site/catalogue/safe timetable | Published | Published | Published | Published | operations_admin page;education_admin curriculum |
| Accounts and contacts | Register/login only | Own | Own safe fields | Own | identity_admin |
| Child registration and identity | No | Own family create;linked child edit | Own preferred/interests/experience | No | identity_admin |
| Guardian link / billing membership grants | No | View own permitted relationship | No | No | identity_admin;financial grant approval evidence |
| Child educational profile | No | Linked | Own | Assigned minimum fields | identity_admin full;education_admin purpose-limited |
| Curriculum drafts and answer keys | No | No | No | Assigned teaching published plan/quiz pedagogy only | education_admin |
| Released enrolled learning content | Safe marketing only | Child educational summaries | Own enrolled/released | Assigned planned/published revision | education_admin |
| Course/cohort/session administration | No | No | No | Assigned future reschedule>=24h only | education_admin |
| Schedules/class detail | Published times | Linked children | Own | Assigned | education_admin |
| Live start URL | No | No | No | Assigned authorized host/window | No generic host override;designated teaching host required |
| Live learner join | No | Assist linked child/window | Own enrolled/window | No learner impersonation | No learner impersonation |
| Attendance | No | Linked read | Own read | Assigned record/amend | education_admin |
| Submission authoring | No | No | Own eligible draft/submit | No | No impersonation |
| Submitted work/marking | No | Linked status/released result | Own work/released result | Assigned review/mark/release | education_admin |
| Feedback | No | Linked released read | Own released read | Assigned draft/release/withdraw | education_admin |
| Progress/certificates | No | Linked read/download | Own read/download | Assigned progress read | education_admin issue/revoke/override with evidence |
| Price configuration | Public displayed fee only | Displayed fee only | Displayed fee only | Displayed fee only | finance_admin |
| Payments/receipts/refunds | No | Billing family read and allowed checkout | No | Never | finance_admin |
| Financial reports/export | No | No | No | Never | finance_admin |
| Events/announcements | Public audience only | Relevant published | Relevant published | Relevant published | education_admin publication |
| Notification inbox | No | Own | Own | Own;no payment notices | Own;operations_admin redacted delivery operations |
| Resource/upload files | Published assets only | Authorized child ready downloads | Own submissions and released resources | Assigned ready resources/work | education_admin/operations_admin by purpose |
| Settings/integrations | No | No | No | No | operations_admin;finance settings finance_admin;Stripe config both |
| Audit history | No | No | No | No | audit_admin redacted |
| Privacy/export/deletion requests | No | Own family request;approved own export | No independent adult-authority action | No | identity_admin verification/decision;finance record access remains scoped |


No global administrative role bypass exists. A single API listing never returns all columns then relies on the frontend to hide them. Filter, pagination cursor and include/expand parameters are validated and bound to the same scope. An admin endpoint has exactly the capability listed even if a route name shares a resource group with another capability.
