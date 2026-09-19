# User journeys

Status: DRAFT. Each journey connects the defined surfaces through the same backend and authorization model. Requirement IDs are stable references, not optional scope suggestions.

## Visitor becomes an enrolled family

1. Visitor reads published course outcomes, age suitability, fees and upcoming cohort timetable (WEB-001–012).
2. Course CTA preserves the selected cohort through parent registration, email verification and required policy acknowledgements (PAR-001, PAR-004; AUTH-001–004).
3. Parent creates a child with required name and numeric age; school/last/preferred name are optional. The system records the explicit guardian relationship (PAR-005–006; SEC-001–002).
4. Parent selects child and cohort. Backend validates guardian authority, billing-family membership, current age assertion, course band, consent, enrolment window, learner schedule conflicts and capacity (ENR-001).
5. Parent reviews immutable AUD order summary and relevant policy version. Server creates a 30-minute seat hold and Stripe-hosted checkout (PAR-019; ENR-002, ENR-006; PAY-001–003).
6. Provider verification, independently of browser redirect, activates the enrolment exactly once. Family receives confirmation and receipt notification; student gets learning entitlement (ENR-003–004; PAY-004–007; COM-002–003).
7. If checkout is cancelled/failed, the parent sees an accurate retryable state. A late paid event without capacity becomes a visible administrative exception; the system does not oversell or pretend success (PAR-020; ENR-007).

## Parent supports multiple children

1. Parent switches among explicitly authorized children, viewing each child's courses, timetable, progress, attendance and released work (PAR-006–014).
2. The family dashboard combines schedules without revealing unrelated classmates. Notifications deep-link to authorized records (PAR-009, PAR-015–016).
3. An additional guardian is verified and linked by administration. Revocation removes educational access immediately; it does not grant or transfer unrelated financial access (AUTH-007; ADM-004).
4. Parent views billing only for active billing-family memberships. Downloaded invoice/receipt still requires authorization (PAR-017–018).
5. Parent can contact support regarding schedule or account matters, but cannot mutate the global schedule or submit the child's work (WEB-009; PAR-009, PAR-013, PAR-021).

## Student learns, attends and completes

1. Guardian provisions student credentials with no required child email. Student signs in to own dashboard (STU-001–002; AUTH-005).
2. Student navigates released enrolled curriculum and resources, then completes practice/reflection (STU-003–006; LRN-001–006).
3. Before a class, the student sees the correct timezone and requests an authorized short-lived Zoom join. Revoked enrolment, cancelled session or outside join window is denied (STU-013–015; CLS-006–009).
4. Student attempts a quiz, receives own formative result, builds assignment/project work and uploads validated files. Pending/quarantined uploads cannot be submitted (STU-007–010; ASM-001–005; FILE-001–005).
5. Teacher releases assessment/feedback. Student reviews it, resubmits if returned/allowed, and sees progress recompute consistently (STU-011–012, STU-016; ASM-006–008).
6. When required work and attendance policy pass, completion is recorded and one active certificate is issued. Student and guardian receive appropriate notice and authenticated download (STU-017; LRN-007–010; COM-006).

## Teacher delivers an assigned cohort

1. Invited teacher completes MFA and sees only assigned cohorts, sessions, learning resources and learners (TCH-001–003; AUTH-002, AUTH-009).
2. Teacher prepares and starts the assigned class through a just-in-time host action; host credentials never enter student/public payloads (TCH-004; CLS-008).
3. If a future session needs moving, teacher chooses a candidate time. Server checks both notice windows, cohort bounds, preserved duration and teacher/cohort/learner conflicts before commit. Notifications and provider sync follow the committed revision (TCH-005; CLS-003, CLS-011).
4. Teacher records attendance and can amend with reason until seven days after session end; later correction requires administrator (TCH-007–008).
5. Teacher reviews assigned learner work, drafts marks/feedback, returns for revision or releases approved results (TCH-010–014).
6. Assignment revocation ends protected data access immediately. Direct payment, receipt, refund or financial-report calls remain denied even if a teacher guesses the route/ID or attempts an incompatible additive role (TCH-016; AUTH-009–010).

## Administrator prepares a course and operates launch

1. Authorized staff use MFA and only granted capability groups. Identity administrator verifies teacher accounts and guardian links (ADM-001–006).
2. Education administrator builds and publishes a stable course revision with modules, lessons, blocks, resources, quizzes, assignments and completion policy (ADM-007–012; LRN-001–004).
3. Education administrator creates cohort capacity, individual sessions/finite recurrence and teacher assignments. Finance administrator sets approved upfront AUD fee. Publication requires approved age, policy and production settings (ADM-013–015, ADM-024; PAY-012).
4. Operations verify Zoom meeting and Google Calendar mirroring, email sending domain and object storage readiness. Failures show actionable sync status and retry controls (CLS-006–009; CAL-001–005; COM-009).
5. Education staff oversee attendance, progress, released results, feedback and certificates. Exceptions require reasons without erasing historical evidence (ADM-016–020).
6. Operations publish audience-scoped events/announcements and diagnose notifications/resources without seeing unnecessary sensitive content (ADM-021–023).
7. Finance staff reconcile payments, resolve late payment exceptions, issue full/partial refunds with explicit entitlement disposition and export AUD financial reports (ADM-025–027; PAY-008–011).
8. Privileged settings and audit review use explicit operations/audit grants; launch waits for all required evidence and approved human gates (ADM-028–029; OPS-015).

## Failure, recovery and privacy

A duplicate/out-of-order Stripe event reuses recorded provider identity and cannot duplicate enrolment or refund. A Zoom/Calendar/Resend outage leaves committed schedule/notification intent in PostgreSQL and exposes retry/dead-letter status. An unsafe upload remains quarantined. A privacy request verifies guardian authority, separates child education records from financial retention and deletes only permitted data. An infrastructure incident follows recovery runbooks and a proven isolated restore; older restored backups reapply pending erasure before reopening service (PAY-004–005, PAY-009; COM-009; FILE-004; SEC-009–010; OPS-010–012).
