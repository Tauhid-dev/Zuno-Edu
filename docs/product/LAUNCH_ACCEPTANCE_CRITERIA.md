# Launch acceptance criteria

Status: DRAFT. This is a future production gate, not a claim that the planning/bootstrap run has built or validated a working application. Every required acceptance test must attach concrete versioned evidence before launch approval.

## Required gate

| Gate | Observable pass condition | Required evidence |
|---|---|---|
| Scope coverage | 219/219 locked launch requirements have design, chunk and verification mapping; zero orphan requirements/chunks | Machine validator result and traceability at final master SHA |
| Implementation | 100% required launch requirements implemented; no partial/deferred substitute counted complete | Merged chunk evidence plus requirement-specific acceptance results |
| Review | Zero unresolved Critical or High findings; material Medium disposition recorded | Independent product, OOP/backend, frontend, security, chunk and state/workflow reports |
| Blueprint consistency | Object/service/port/API/frontend mappings agree; no undocumented durable public behavior | Contract and blueprint consistency checks at release SHA |
| Authorization | All positive/negative role, ownership, guardian, assignment and resource-state cases pass | API/service/query tests including Teacher→finance and cross-family/cross-student attempts |
| Child privacy | Minimum profile matches requirements; no optional field made required; no unnecessary child fields; released-state checks pass | Schema validation, projected DTO review, privacy workflow tests |
| Authentication | Staff MFA, session expiry/revocation, reset and guardian-controlled student recovery pass | Automated account lifecycle tests and manual MFA/recovery evidence |
| Billing | Live-mode configuration approved; verified success/failure/duplicate/out-of-order/late payment and full/partial refund reconcile accurately | Stripe test evidence, approved production config and controlled live verification |
| Learning | Enrolled released curriculum, quiz, project file hand-in, marking/release, progress and certificate journey passes | End-to-end student/teacher/parent/admin evidence |
| Delivery | Correct timezone/DST, capacity/teacher/learner conflicts, reschedule/cancel, host/join boundaries and attendance pass | Domain/API and controlled Zoom integration results |
| Calendar/communications | Creation/update/cancel/retry mirrors correct domain revision; reminders and notices reach intended audiences once | Adapter tests, provider sandbox/staging evidence and delivery ledger inspection |
| File safety | Type/size/archive/scanner/access/expiry/deletion tests pass; private buckets confirmed | Adversarial upload and ownership tests plus storage configuration review |
| Database | Migrations succeed on clean and representative prior schema; constraints/concurrency/persistence tests pass | Migration dry run, data checks and rollback/forward-fix procedure |
| Production security | HTTPS, private internal ports, secrets, rate limits, CSRF/CORS, log redaction and scans validated | Config audit plus zero unresolved exploitable Critical/High scan findings |
| Performance | NFR-001 performance targets met on documented representative load profile | Dated load test report with environment and percentiles |
| Accessibility/responsiveness | WCAG 2.2 AA checks on all critical journeys; keyboard/screen reader and 360px/mobile/browser matrix pass | Automated checks and manual accessibility report with no launch-blocking findings |
| Deployment | Versioned build deploys to staging then approved production with health/smoke checks | Artifact digest, release SHA, config version, deployment and smoke results |
| Monitoring | Actionable alerts and safe logs/errors operate; owners can see payment/provider/job/backup failures | Triggered test alerts and runbook links |
| Backups/restore | Database RPO ≤15 minutes and isolated full restore RTO ≤4 hours proven; object references intact | Successful restore report and backup retention/encryption review |
| Recovery | Rollback, migration failure, provider outage, queue recovery, secret rotation and incident runbooks are executable | Rehearsal evidence and named responsible operator |
| Human gates | HG-LEGAL, HG-MERCHANT, HG-AGE, HG-PROVIDERS and HG-STAFF approved with version/date/actor | Approval registry entries with real sign-off, not placeholder text |
| Launch authorization | Business owner explicitly approves launch after evidence review | Recorded human release decision |

## Critical end-to-end journeys

1. Public course → parent verify → two child profiles → eligible cohort → paid enrolment → correct family receipt.
2. Failed/cancelled checkout retry, concurrent final-seat race, duplicate webhook and late paid exception without oversell.
3. Guardian-provisioned student → released lesson/video/download → quiz → scanned project submission → teacher marks/releases → student/parent result → progress → certificate.
4. Assigned teacher starts Zoom; student joins only within entitlement/window; unrelated teacher and unauthorized student fail.
5. Teacher permitted reschedule succeeds, notice/conflict violations fail, admin exception is audited, participant notices and Calendar/Zoom update correctly.
6. Teacher attendance correction inside window, admin correction after window, recalculated completion with preserved history.
7. Finance full/partial refund reconciles once with explicit keep/cancel entitlement and correct family notice/report.
8. Parent cannot access another family; student cannot access another student; Teacher principal cannot acquire financial access through additive roles.
9. Account suspension/guardian revocation/teacher assignment expiry invalidates previously valid session access.
10. Provider/job outage recovery, unsafe upload quarantine and isolated DB/object restore retain authoritative records and access boundaries.

The final production gate may fail after feature completion. That failure is not permission to remove a requirement. Record the blocker, remediate in an authorized bounded change and rerun affected verification.
