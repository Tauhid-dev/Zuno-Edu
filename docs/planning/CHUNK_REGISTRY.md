# Chunk registry

Canonical metadata: [chunks.json](chunks.json). All implementation remains PLANNED during bootstrap; sequence selects only eligible work after verified scope approval.

| Sequence | Chunk | Responsibility | Dependencies |
|---|---|---|---|
| 10 | [ZE-P01-C01](chunks/ZE-P01-C01.md) | Runtime, package and test foundation | Scope approval only |
| 20 | [ZE-P01-C02](chunks/ZE-P01-C02.md) | Persistence, unit of work and durable jobs | ZE-P01-C01 |
| 30 | [ZE-P01-C03](chunks/ZE-P01-C03.md) | Transport contracts, errors and CI controls | ZE-P01-C01 |
| 40 | [ZE-P02-C01](chunks/ZE-P02-C01.md) | Authentication, sessions and adult recovery | ZE-P01-C02, ZE-P01-C03 |
| 50 | [ZE-P02-C02](chunks/ZE-P02-C02.md) | Resource authorization and audit foundation | ZE-P02-C01 |
| 60 | [ZE-P02-C03](chunks/ZE-P02-C03.md) | Accounts, family links and student profiles | ZE-P02-C02 |
| 70 | [ZE-P02-C04](chunks/ZE-P02-C04.md) | Teacher profiles and staff administration | ZE-P02-C02 |
| 80 | [ZE-P02-C05](chunks/ZE-P02-C05.md) | Versioned consent and privacy lifecycle | ZE-P02-C03 |
| 90 | [ZE-P03-C01](chunks/ZE-P03-C01.md) | Published public content and contact | ZE-P02-C02 |
| 100 | [ZE-P03-C02](chunks/ZE-P03-C02.md) | Reusable programs and course catalogue | ZE-P02-C02 |
| 110 | [ZE-P03-C03](chunks/ZE-P03-C03.md) | Curriculum hierarchy, typed blocks and release | ZE-P03-C02 |
| 120 | [ZE-P03-C04](chunks/ZE-P03-C04.md) | Learning resources and teaching projections | ZE-P03-C03, ZE-P04-C02 |
| 130 | [ZE-P04-C01](chunks/ZE-P04-C01.md) | Private object storage upload lifecycle | ZE-P02-C02 |
| 140 | [ZE-P04-C02](chunks/ZE-P04-C02.md) | Scanning, immutable promotion and file cleanup | ZE-P04-C01 |
| 150 | [ZE-P05-C01](chunks/ZE-P05-C01.md) | Cohorts and teaching assignments | ZE-P02-C03, ZE-P02-C04, ZE-P03-C02 |
| 160 | [ZE-P05-C02](chunks/ZE-P05-C02.md) | Authoritative sessions and bounded rescheduling | ZE-P05-C01 |
| 170 | [ZE-P05-C03](chunks/ZE-P05-C03.md) | Zoom live class integration | ZE-P05-C02, ZE-P06-C02 |
| 180 | [ZE-P05-C04](chunks/ZE-P05-C04.md) | Calendar mirror and authorized exports | ZE-P05-C02, ZE-P08-C02 |
| 190 | [ZE-P05-C05](chunks/ZE-P05-C05.md) | Attendance recording and oversight | ZE-P05-C02, ZE-P06-C02 |
| 200 | [ZE-P06-C01](chunks/ZE-P06-C01.md) | Course/cohort price configuration | ZE-P05-C01 |
| 210 | [ZE-P06-C02](chunks/ZE-P06-C02.md) | Enrolment eligibility and seat reservations | ZE-P02-C05, ZE-P06-C01 |
| 220 | [ZE-P06-C03](chunks/ZE-P06-C03.md) | Checkout, payment ledger and verified webhooks | ZE-P06-C02 |
| 230 | [ZE-P06-C04](chunks/ZE-P06-C04.md) | Invoices, receipts and refund administration | ZE-P04-C02, ZE-P06-C03 |
| 240 | [ZE-P06-C05](chunks/ZE-P06-C05.md) | Financial reconciliation and reports | ZE-P06-C04 |
| 250 | [ZE-P07-C01](chunks/ZE-P07-C01.md) | Quiz definitions and student attempts | ZE-P03-C03, ZE-P06-C02 |
| 260 | [ZE-P07-C02](chunks/ZE-P07-C02.md) | Assignment/project definitions | ZE-P03-C03 |
| 270 | [ZE-P07-C03](chunks/ZE-P07-C03.md) | Versioned submissions and resubmission | ZE-P04-C02, ZE-P06-C02, ZE-P07-C02 |
| 280 | [ZE-P07-C04](chunks/ZE-P07-C04.md) | Assessment marking and feedback release | ZE-P07-C03 |
| 290 | [ZE-P07-C05](chunks/ZE-P07-C05.md) | Progress and deterministic completion | ZE-P05-C05, ZE-P07-C01, ZE-P07-C04 |
| 300 | [ZE-P07-C06](chunks/ZE-P07-C06.md) | Completion certificate lifecycle | ZE-P07-C05 |
| 310 | [ZE-P08-C01](chunks/ZE-P08-C01.md) | Transactional notification delivery | ZE-P02-C03 |
| 320 | [ZE-P08-C02](chunks/ZE-P08-C02.md) | Events and scoped announcements | ZE-P03-C01, ZE-P05-C01, ZE-P08-C01 |
| 330 | [ZE-P08-C03](chunks/ZE-P08-C03.md) | Operational settings, jobs and audit views | ZE-P08-C01 |
| 340 | [ZE-P08-C04](chunks/ZE-P08-C04.md) | Private export and retention integration | ZE-P06-C05, ZE-P07-C06 |
| 350 | [ZE-P08-C05](chunks/ZE-P08-C05.md) | Notification producer integration | ZE-P05-C04, ZE-P08-C04 |
| 360 | [ZE-P09-C01](chunks/ZE-P09-C01.md) | Shared web shell, forms and API state | ZE-P02-C01 |
| 370 | [ZE-P09-C02](chunks/ZE-P09-C02.md) | Public website and enrolment discovery | ZE-P02-C05, ZE-P05-C02, ZE-P06-C01, ZE-P08-C02, ZE-P09-C01 |
| 380 | [ZE-P09-C03](chunks/ZE-P09-C03.md) | Authentication, recovery and role entry UX | ZE-P02-C05, ZE-P09-C01 |
| 390 | [ZE-P10-C01](chunks/ZE-P10-C01.md) | Parent account, children and consent | ZE-P09-C03 |
| 400 | [ZE-P10-C02](chunks/ZE-P10-C02.md) | Parent checkout and family billing | ZE-P03-C01, ZE-P06-C04, ZE-P10-C01 |
| 410 | [ZE-P10-C03](chunks/ZE-P10-C03.md) | Parent learning, schedule and communications | ZE-P05-C03, ZE-P05-C04, ZE-P07-C06, ZE-P10-C01 |
| 420 | [ZE-P10-C04](chunks/ZE-P10-C04.md) | Student dashboard, curriculum and lessons | ZE-P03-C04, ZE-P07-C05, ZE-P09-C03 |
| 430 | [ZE-P10-C05](chunks/ZE-P10-C05.md) | Student quizzes and assignment work | ZE-P10-C04 |
| 440 | [ZE-P10-C06](chunks/ZE-P10-C06.md) | Student results, progress and certificates | ZE-P07-C06, ZE-P10-C05 |
| 450 | [ZE-P10-C07](chunks/ZE-P10-C07.md) | Student live classes and notifications | ZE-P05-C03, ZE-P08-C02, ZE-P10-C04 |
| 460 | [ZE-P11-C01](chunks/ZE-P11-C01.md) | Teacher delivery workspace | ZE-P05-C03, ZE-P08-C02, ZE-P10-C04 |
| 470 | [ZE-P11-C02](chunks/ZE-P11-C02.md) | Teacher marking and feedback workspace | ZE-P11-C01 |
| 480 | [ZE-P11-C03](chunks/ZE-P11-C03.md) | Admin account and role workspace | ZE-P02-C04, ZE-P09-C03 |
| 490 | [ZE-P11-C04](chunks/ZE-P11-C04.md) | Admin public content and catalogue editors | ZE-P03-C01, ZE-P03-C03, ZE-P09-C03 |
| 500 | [ZE-P11-C09](chunks/ZE-P11-C09.md) | Admin curriculum and resource authoring | ZE-P03-C04, ZE-P07-C01, ZE-P07-C02, ZE-P09-C03 |
| 510 | [ZE-P11-C10](chunks/ZE-P11-C10.md) | Admin quiz and assignment definition editors | ZE-P07-C01, ZE-P07-C02, ZE-P09-C03 |
| 520 | [ZE-P11-C05](chunks/ZE-P11-C05.md) | Admin delivery and enrolment workspace | ZE-P05-C03, ZE-P05-C04, ZE-P05-C05, ZE-P07-C02, ZE-P09-C03 |
| 530 | [ZE-P11-C06](chunks/ZE-P11-C06.md) | Admin educational oversight | ZE-P07-C06, ZE-P09-C03 |
| 540 | [ZE-P11-C07](chunks/ZE-P11-C07.md) | Admin finance workspace | ZE-P06-C05, ZE-P09-C03 |
| 550 | [ZE-P11-C08](chunks/ZE-P11-C08.md) | Admin communications, assets and operations | ZE-P08-C02, ZE-P08-C03, ZE-P08-C04, ZE-P09-C03 |
| 560 | [ZE-P12-C01](chunks/ZE-P12-C01.md) | Containerized staging and production topology | ZE-P08-C03 |
| 570 | [ZE-P12-C02](chunks/ZE-P12-C02.md) | Monitoring and incident readiness | ZE-P12-C01 |
| 580 | [ZE-P12-C03](chunks/ZE-P12-C03.md) | Database and object backup restore | ZE-P02-C05, ZE-P04-C02, ZE-P12-C01 |
| 590 | [ZE-P12-C04](chunks/ZE-P12-C04.md) | Release pipeline, scans and performance | ZE-P12-C02 |
| 600 | [ZE-P12-C05](chunks/ZE-P12-C05.md) | Provider sandbox and critical journey verification | ZE-P08-C05, ZE-P09-C02, ZE-P10-C02, ZE-P10-C03, ZE-P10-C06, ZE-P10-C07, ZE-P11-C02, ZE-P11-C03, ZE-P11-C04, ZE-P11-C05, ZE-P11-C06, ZE-P11-C07, ZE-P11-C08, ZE-P11-C09, ZE-P11-C10, ZE-P12-C03, ZE-P12-C04 |
| 610 | [ZE-P12-C06](chunks/ZE-P12-C06.md) | Accessibility and authorization launch audit | ZE-P12-C05 |
| 620 | [ZE-P12-C07](chunks/ZE-P12-C07.md) | Complete launch readiness gate | ZE-P12-C06 |
