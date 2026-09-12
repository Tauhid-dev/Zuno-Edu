# Launch scope

Status: DRAFT. Scope candidate: 1.0. This document and `SCOPE_LOCK.md` are authoritative for what must exist before business launch once human approval is evidenced on merged remote master. All 219 canonical requirements in `requirements.json` are REQUIRED FOR LAUNCH; none are future-only placeholders.

## Public Website

Home; About; published programs/courses and detailed curriculum, outcomes, age suitability, duration, delivery and fees; upcoming cohorts and timezone-aware timetables; approved teacher biographies; how classes work; parent information; FAQs; validated contact enquiries; published privacy/terms/service policies and child-safety information; parent registration/sign-in and context-preserving enrolment entry. Explicit publication governs every public response. Private class rosters, family data, finance records and provider credentials are excluded.

## Parent Portal

Verified adult registration, authentication and recovery; own profile/contact and optional communication preferences; versioned policy acknowledgements; one or more minimum-data child registrations; verified guardian-child relationships; course/cohort selection; checkout and actionable payment recovery; own child enrolment, class schedule, attendance, progress, assignment/submission state, released assessment/feedback, completion and certificates; relevant events, announcements and notifications; billing-family payment history, invoices/receipts and permitted checkout actions; logout, password and verified account lifecycle. A parent sees relevant schedules and receives change notices. Schedule changes are made by constrained teachers or administrators; a parent may contact support but cannot directly reschedule sessions.

## Student LMS

Guardian-provisioned sign-in, own safe profile display, focused dashboard and enrolled courses; released modules/lessons and all eight supported content block types; downloadable and video resources; activity completion/reflection, quizzes, assignments and project work; validated file hand-in and submission versions; own released results and feedback; upcoming classes and secure join; attendance, progress, completion and certificates; scoped announcements and notifications. The learning path is Learn → Attend / Watch → Try → Build → Submit → Review / Reflect. There is no financial or family-administration capability.

## Teacher Portal

Invited MFA-protected teacher identity; assigned dashboard, courses, cohorts and sessions; curriculum/lesson plans/internal teaching resources; assigned learner educational projections; authorized live-class start; assigned future session rescheduling under the notice/conflict policy; roster and attendance recording/correction; assignment and submission review; marking, return-for-revision and feedback release; progress visibility; relevant notifications. All reads and writes are assignment constrained. Teacher has zero financial administration, including where another role label could otherwise confer finance access.

## Admin Portal

Invited MFA-protected administrative identity with explicit capability groups; operational dashboard; parent/student/teacher lifecycle, verified guardian links and role grants; programs/courses, immutable curriculum revisions, modules, lessons, content blocks and resources; quizzes, assignments, rubrics, assessment and feedback oversight; cohorts, session schedules, teacher assignments and enrolments; attendance/progress/completion oversight and certificates; scoped events, announcements, notifications and files; AUD prices, payments/status/reconciliation, invoices/receipts, full/partial refunds and launch financial reports/exports; nonsecret operational/integration settings; audit review. The interface must not expose an operation beyond the granted administrative capability.

## Shared launch capabilities

One OOP domain/application model and REST contract; account and relationship authorization at API, service and query levels; reusable public/portal components; Stripe verified payment and webhook lifecycle; Zoom meeting lifecycle; Google Calendar mirror and ICS; Resend outbox-backed communications; S3-compatible file storage, scanning and lifecycle; audit and privacy-request workflows; secure secrets and configuration; Docker/Compose/Caddy HTTPS production architecture on OCI-compatible VPS; PostgreSQL migrations; Redis workers with durable outbox; CI, tests and security scans; isolated staging; logs, errors, metrics and alerts; encrypted backups, proven restore, recovery/rollback runbooks and a verified launch gate.

## Explicit policy defaults to implement

- Course/cohort age bands are admin-configured and human approved before publication. Registration stores age and date, reconfirmed when older than 180 days at enrolment; it does not infer a DOB.
- Price is one upfront AUD amount in cents. A 30-minute transactional seat hold aligns with checkout expiry. A verified late payment with no capacity enters a paid exception requiring allocation or refund, never overselling. Refund and educational-entitlement disposition are separate explicit administrative decisions.
- Student joins are allowed from 15 minutes before session start until session end; assigned teacher start is allowed from 30 minutes before until end. No join/start for cancelled sessions or inactive actors. Parent can see logistics and assist the authorized child, but never receives host credentials.
- Teacher rescheduling preserves duration, cohort, capacity and price; old and new starts must both be at least 24 hours away. Validate cohort delivery bounds and teacher/cohort/learner conflicts. Only admin can approve later exceptions, with a recorded reason and mandatory notices.
- Attendance values are present, absent, late and excused. Teacher corrections require reason and are allowed until seven days after session end; authorized education administrators correct later records.
- Quizzes support single-choice and multiple-choice exact-match scoring; default 70% pass mark and three attempts, configurable one to five per published definition. Results release after submit. Assignment late submissions are accepted and labelled until cohort completion unless the published assignment is explicitly closed. Student resubmission follows configured policy or educator return-for-revision.
- Completion requires all required learning items and at least 80% attendance among delivered, noncancelled sessions. Present and late count as attended; excused counts as attended for completion only when education-admin confirms the excuse. An evidenced education-admin override can resolve exceptional cases. Optional activities do not increase required denominator. Certificate is the only launch achievement.
- Download grants expire within five minutes and upload grants within ten. Submission allowlist: PDF, PNG, JPEG, TXT and approved project ZIP; 25 MiB (26,214,400 bytes) per file and 100 MiB (104,857,600 bytes) per submission. ZIP constraints: 100 entries, 100 MiB (104,857,600 bytes) maximum expanded bytes, compression ratio ≤20:1, no nested archives, path traversal, encrypted entries or executable/script payloads. Student files remain quarantined until validation/scan succeeds.
- Learning resource allowlist: PDF, PNG, JPEG and TXT up to 50 MiB (52,428,800 bytes); MP4 up to 500 MiB (524,288,000 bytes) or approved HTTPS video references. Internal assets: PDF, PNG, JPEG and TXT up to 25 MiB (26,214,400 bytes). Certificates: generated PDF up to 5 MiB (5,242,880 bytes). No arbitrary HTML or scripts. File extension, declared MIME and detected content must agree.
- Adult verified contacts receive security, service and billing email. Students receive learning notifications in-app; a child email is not required. Optional preferences never suppress mandatory security, payment or material service-change notices.

## Human production decision gates

The technical contracts are fully specified; these external decisions block production activation, not design completion. The repository must not claim approval that has not occurred.

| Gate | Required evidence | Owner | Blocking effect |
|---|---|---|---|
| HG-LEGAL | Approved current privacy, terms, refund/cancellation, consent and child-safety texts; retention schedule reviewed | Business owner with qualified adviser | Public policy publication and production checkout disabled |
| HG-MERCHANT | Stripe merchant identity, tax treatment, invoice/receipt wording, fees and production credentials approved | Business owner / finance adviser | Production checkout disabled |
| HG-AGE | Launch course age bands, descriptions and teaching suitability confirmed | Education lead | Course/cohort publication disabled |
| HG-PROVIDERS | Zoom host licensing/capacity and waiting-room controls, Google business calendar, sending domain and object storage configured/tested | Operations owner | Affected production delivery disabled |
| HG-STAFF | Initial administrators, role separation, teacher approvals and operational incident contacts verified | Business owner | Staff activation and production launch disabled |

The system stores approval version/date/actor and gates the affected action. No agent invents legal advice or silently bypasses the gate.
