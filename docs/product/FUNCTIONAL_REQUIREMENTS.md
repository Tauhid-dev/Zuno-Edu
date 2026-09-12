# Functional requirements

Status: DRAFT — proposed complete launch baseline, pending human review and remote merge.

Canonical inventory: `requirements.json`. These readable records are generated from that inventory; IDs are stable and are never renumbered or reused. Every requirement is REQUIRED FOR LAUNCH. No item is implicitly deferred. Related domain capability is the routing key used by design and chunk traceability.

## WEB-001 — Publish a Home page describing Zuno Edu and enrolment entry points.

Rationale: Visitors need an accurate starting point.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `public_content`.

Acceptance:

- Home displays approved business introduction and course discovery CTA.
- Draft content is absent from public responses.

## WEB-002 — Publish About Zuno Edu information.

Rationale: Parents need to understand the provider.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `public_content`.

Acceptance:

- About displays only the current published content version.

## WEB-003 — Browse published programs and courses.

Rationale: Families need course discovery.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `catalogue`.

Acceptance:

- Course index lists published courses and program grouping.
- Unpublished course identifiers do not reveal draft details.

## WEB-004 — View complete published course detail.

Rationale: Families need to assess course fit.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `catalogue`.

Acceptance:

- Detail includes age group, curriculum outcomes, duration, delivery method and AUD fee.
- Course reusable curriculum is separate from scheduled cohort details.

## WEB-005 — View published upcoming cohorts and timetables.

Rationale: Families need to select a suitable delivery.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Published cohort detail shows timezone, future session times, availability and enrolment window.
- No learner roster or private meeting credential is exposed.

## WEB-006 — View approved public instructor biographies.

Rationale: Families need confidence in teaching staff.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `teacher_profiles`.

Acceptance:

- Only teacher-approved public biography, display name and approved photo are visible.
- Teacher contact and operational profile fields never appear.

## WEB-007 — Publish how-classes-work guidance.

Rationale: Families need technical and learning expectations.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `public_content`.

Acceptance:

- Published guidance covers live attendance, preparation, resources and support entry points.

## WEB-008 — Publish parent information and FAQs.

Rationale: Parents need consistent service guidance.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `public_content`.

Acceptance:

- Published parent information and ordered FAQ entries are readable and searchable by page text.

## WEB-009 — Provide a contact/support entry point.

Rationale: Visitors need a reachable business channel.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `contact`.

Acceptance:

- Contact page offers approved business contact information and validated enquiry form.
- Submission acknowledges receipt without disclosing other enquiries.

## WEB-010 — Publish versioned privacy, terms, policy and child-safety information.

Rationale: Families need clear service conditions.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `policies`.

Acceptance:

- Each current published policy has title, version and effective date.
- Draft legal text cannot be published until the recorded human approval gate is satisfied.

## WEB-011 — Offer parent registration and sign-in entry points.

Rationale: Acquisition must lead into family enrolment.

Roles: Public, Parent. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Every enrolment CTA retains selected course/cohort through successful parent authentication.

## WEB-012 — Expose only expressly published public information.

Rationale: Public access must not leak private data.

Roles: Public. Priority: REQUIRED FOR LAUNCH. Capability: `public_content`.

Acceptance:

- Public responses exclude family, learner, billing, meeting-secret and operational data.
- Direct-object requests cannot bypass publication state.

## PAR-001 — Create and verify a parent account.

Rationale: The primary account holder must be identifiable and contactable.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Registration requires adult account holder name, email and password plus current required acknowledgements.
- Account email is verified before checkout or child account activation.

## PAR-002 — Manage own profile and contact information.

Rationale: Service communications need accurate contact information.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `account`.

Acceptance:

- Parent can edit own name and optional phone.
- Email change requires confirmation of new address and invalidates affected verification until confirmed.

## PAR-003 — Manage optional communication preferences.

Rationale: Parents need control of optional communications.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- Parent can update per-channel optional announcement preferences.
- Security, billing and material service messages remain mandatory and are labelled as such.

## PAR-004 — Record versioned policy and child-service acknowledgements.

Rationale: The service needs attributable acknowledgements.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `consent`.

Acceptance:

- Stored record identifies adult, family/student scope, policy version and timestamp.
- Changed required terms prompt a new acknowledgement before the affected action.

## PAR-005 — Register one or more children with minimum required information.

Rationale: Families can enrol siblings without excessive data collection.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `students`.

Acceptance:

- Each child has required first/display name and integer age with age_as_of date.
- School, last name and preferred name remain nullable.
- Guardian reconfirms numeric age at each new enrolment if age_as_of is older than 180 days; no exact birth date is inferred.

## PAR-006 — Access only children for whom the parent is an active authorized guardian.

Rationale: Shared guardianship must preserve family boundaries.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `family`.

Acceptance:

- Revoked or missing guardian-student relationship returns no child data.
- A parent may be linked to several children without gaining access to unrelated siblings.

## PAR-007 — Browse courses and choose an available cohort for a child.

Rationale: Parents purchase an appropriate scheduled course.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `catalogue`.

Acceptance:

- Course selection identifies child, course, cohort, fee and schedule.
- Age eligibility and available capacity are evaluated server-side.

## PAR-008 — View each child's enrolment status and history.

Rationale: Parents need a reliable service record.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Own authorized children display pending payment, active, cancelled and completed enrolments with dates and reason where relevant.

## PAR-009 — View family schedules and class information.

Rationale: Parents coordinate attendance.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Calendar/list views include authorized children's sessions, teacher display name, timezone and status.
- Parent has no mutation granting general scheduling authority.

## PAR-010 — View each authorized child's attendance.

Rationale: Parents need attendance visibility.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `attendance`.

Acceptance:

- Attendance history shows session, recorded status and parent-visible correction state.
- Other children and private attendance notes are excluded.

## PAR-011 — View child's course progress and completion.

Rationale: Parents need educational progress visibility.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `progress`.

Acceptance:

- Progress includes required learning items completed and completion status for own authorized child.

## PAR-012 — Read released teacher feedback.

Rationale: Parents need actionable educational feedback.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `feedback`.

Acceptance:

- Only released feedback for an authorized child's learning work is returned.
- Draft teacher notes remain inaccessible.

## PAR-013 — View child's assignments, submissions and released results.

Rationale: Parents need to support learning.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `assessment`.

Acceptance:

- Assignment due dates, submission status and released assessments are shown.
- Parent cannot submit work as the child.

## PAR-014 — Access child's completion certificates.

Rationale: Families need evidence of completion.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `certificates`.

Acceptance:

- An authorized parent can download valid child certificate.
- Revoked certificates are visibly revoked and cannot masquerade as current.

## PAR-015 — View relevant events and announcements.

Rationale: Families need contextual service notices.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `events`.

Acceptance:

- Parent sees public, family-role and authorized-child-cohort events/announcements only.

## PAR-016 — Read relevant notifications and unread state.

Rationale: Parents need a dependable inbox.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `notifications`.

Acceptance:

- Inbox shows recipient-specific notifications.
- Read action changes only the authenticated parent's record.

## PAR-017 — View own family's billing and payment history.

Rationale: The purchaser needs accurate financial history.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Family financial membership is checked independently of child guardianship.
- Payments, status, amounts and dates belonging to other families are denied.

## PAR-018 — Retrieve own family's invoices and receipts.

Rationale: Parents need purchase documents.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- A parent with active billing-family membership can retrieve issued invoice/receipt.
- Documents contain provider reference and immutable purchase amounts.

## PAR-019 — Pay an outstanding eligible enrolment through hosted checkout.

Rationale: Parents need an authorized payment action.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Checkout uses server-resolved child, family, cohort and price.
- Repeated create request reuses its idempotent result and does not duplicate a reservation.

## PAR-020 — Recover from cancelled or failed checkout.

Rationale: Payment failure must be actionable without false enrolment.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Parent sees pending/failed/expired status and can retry while eligible.
- Browser return never alone activates enrolment.

## PAR-021 — Manage logout, password and account closure requests.

Rationale: Parents need account security and lifecycle control.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `account`.

Acceptance:

- Logout revokes current session.
- Password recovery and closure request use authenticated or verified flows without orphaning child guardianship.

## STU-001 — Use a guardian-provisioned student sign-in account.

Rationale: Children need safe independent learning access.

Roles: Student, Parent. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Guardian initiates credentials for an authorized child.
- Student identifier is non-public and child email/phone is not required.

## STU-002 — View an age-appropriate learning dashboard.

Rationale: Students need a focused next learning action.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `student_dashboard`.

Acceptance:

- Dashboard shows own enrolled courses, next class, due work and released announcements.
- No billing or family-management data is loaded.

## STU-003 — Navigate own enrolled courses by module and lesson.

Rationale: Students need a consistent learning journey.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `curriculum`.

Acceptance:

- Active/completed entitlement exposes only released modules and lessons for own enrolments.
- Unreleased content is denied via direct URL/API.

## STU-004 — Read supported lesson blocks and learning resources.

Rationale: Courses need varied instructional media.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `curriculum`.

Acceptance:

- Heading, rich text, image, video, download, activity, quiz reference and assignment reference render accessibly.
- Disallowed embedded content is rejected before publication.

## STU-005 — Download authorized learning resources.

Rationale: Students need reusable learning materials.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `resources`.

Acceptance:

- Resource access checks enrolment/release state before issuing short-lived link.
- Guessing another course asset identifier is denied.

## STU-006 — Complete non-graded lesson activities.

Rationale: Students need low-pressure practice and reflection.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `activities`.

Acceptance:

- Student can mark an eligible activity done and update own reflection response.
- Other students' activity state is not returned.

## STU-007 — Attempt eligible course quizzes.

Rationale: Students need formative checks.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `quizzes`.

Acceptance:

- Student can begin, save and submit own eligible attempt within configured attempt limit.
- Unsubmitted answers and answer keys are not exposed to peers.

## STU-008 — View assignments and project-work requirements.

Rationale: Students need clear deliverables.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `assignments`.

Acceptance:

- Assignment detail shows instructions, resources, rubric, due time and allowed submission formats.

## STU-009 — Submit own assignment and project files.

Rationale: Students need a safe work hand-in flow.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `submissions`.

Acceptance:

- Submission references validated owned file assets and eligible assignment.
- Successful submit creates immutable version and visible status.

## STU-010 — Track submission history and resubmit when allowed.

Rationale: Students need clear retry and correction rules.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `submissions`.

Acceptance:

- Student sees draft, submitted, returned and assessed state plus version history.
- Resubmission is accepted only while assignment policy or explicit teacher return permits.

## STU-011 — View released assessments and quiz results.

Rationale: Students need trustworthy learning results.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `assessment`.

Acceptance:

- Only own released results are visible.
- Scores and rubric comments match the released assessment revision.

## STU-012 — View released teacher feedback.

Rationale: Students need guidance for reflection.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `feedback`.

Acceptance:

- Own feedback includes release timestamp and related work/session.
- Draft feedback is denied.

## STU-013 — View upcoming classes and details.

Rationale: Students need to find the correct live lesson.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Schedule contains own enrolled cohort sessions and status in user timezone.
- Other cohort private detail is excluded.

## STU-014 — Join an eligible assigned live class.

Rationale: Students need secure entry to scheduled learning.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `live_class`.

Acceptance:

- Active enrolled student receives just-in-time authorized join link within the join window.
- Teacher start credential is never returned.

## STU-015 — View own attendance.

Rationale: Students need a personal learning record.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `attendance`.

Acceptance:

- Own session attendance is visible without peer roster or private teacher notes.

## STU-016 — Track own course progress.

Rationale: Students need learning continuity.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `progress`.

Acceptance:

- Lesson/activity/quiz/assignment completion feeds a consistent progress view.
- Refresh does not reset recorded progress.

## STU-017 — View completion status and own certificates.

Rationale: Students need recognition on completion.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `certificates`.

Acceptance:

- Certificate becomes available only after course completion policy passes.
- Launch achievement is course completion only.

## STU-018 — Read relevant released announcements.

Rationale: Students need useful course notices.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `announcements`.

Acceptance:

- Only student-role/cohort audience announcements are displayed.
- Business or teacher-only notices remain inaccessible.

## STU-019 — Manage safe own profile presentation and logout.

Rationale: Students need limited personal control.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `account`.

Acceptance:

- Student can update optional preferred display name within validation limits and logout.
- Student cannot alter age, guardianship, roles or billing profile.

## TCH-001 — Authenticate as an invited teacher with MFA.

Rationale: Teachers access sensitive child educational data.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Only activated invited teacher account can enter portal.
- MFA is required before accessing educational records.

## TCH-002 — View assigned teaching responsibilities.

Rationale: Teachers need focused delivery information.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `teacher_dashboard`.

Acceptance:

- Dashboard includes assigned courses, cohorts, future sessions and work awaiting review.
- Unassigned cohorts do not appear.

## TCH-003 — Access lesson plans and teaching resources for assigned delivery.

Rationale: Teachers need prepared teaching material.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `curriculum`.

Acceptance:

- Assigned teacher can access published curriculum and cohort teaching resources.
- Internal teacher material never appears in student projection.

## TCH-004 — Initiate assigned live classes.

Rationale: Teachers need authorized host access.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `live_class`.

Acceptance:

- A current assigned teacher can request short-lived host action in permitted start window.
- Unassigned teacher and student requests are denied.

## TCH-005 — Reschedule a permitted future assigned session.

Rationale: Teachers need bounded operational flexibility.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Teacher may move assigned not-started session with at least 24 hours notice before original and new start, preserving duration.
- Overlap with teacher, cohort or enrolled learner sessions, course delivery bounds and cancelled sessions is rejected.

## TCH-006 — View assigned class and schedule details.

Rationale: Teachers need correct delivery context.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Teacher sees assigned session roster and educational logistics.
- Provider secrets are disclosed only through separately authorized start action.

## TCH-007 — Record attendance for assigned sessions.

Rationale: Attendance needs accountable recording.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `attendance`.

Acceptance:

- Assigned teacher records present, absent, late or excused for active roster students.
- Actor and recording time are auditable.

## TCH-008 — Amend attendance with a reason.

Rationale: Mistakes require traceable correction.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `attendance`.

Acceptance:

- Assigned teacher can amend before session ends plus seven days and must provide reason.
- Later correction requires authorized administrator.

## TCH-009 — View assigned learners' necessary educational profiles.

Rationale: Teachers need relevant context without excessive child data.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `students`.

Acceptance:

- Projection includes display name, age-as-of, optional educational information and enrolment.
- Guardian financial/contact details and sensitive internal account data are excluded.

## TCH-010 — View assigned course assignments and learner work queue.

Rationale: Teachers need efficient review.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `assignments`.

Acceptance:

- Queue scopes by active teaching assignment and course.
- Unassigned learner submissions are denied even when identifiers are known.

## TCH-011 — Assess and mark assigned learners' submissions.

Rationale: Instruction needs consistent assessment.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `assessment`.

Acceptance:

- Teacher records rubric/scoring and outcome in draft assessment.
- Marking cannot cross assigned cohort boundaries.

## TCH-012 — Return assigned work for revision.

Rationale: Students need a controlled improvement cycle.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `assessment`.

Acceptance:

- Return action includes learner-facing explanation and opens a new eligible submission version.
- Previously submitted versions remain immutable.

## TCH-013 — Create, revise and release feedback for assigned learners.

Rationale: Feedback requires deliberate release.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `feedback`.

Acceptance:

- Draft is visible only to authorized educators.
- Release publishes to own learner and guardian audience with notification event.

## TCH-014 — Review assigned learners' learning progress.

Rationale: Teachers need to identify support needs.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `progress`.

Acceptance:

- Progress view includes assigned cohort learners and required-item state.
- No global cross-teacher analytics are exposed.

## TCH-015 — Read relevant operational notifications.

Rationale: Teachers need schedule and delivery updates.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `notifications`.

Acceptance:

- Recipient/cohort scoped inbox includes changes and provider issues relevant to assignments.

## TCH-016 — Exclude all teacher financial administration access.

Rationale: Educational role must have zero finance authority.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `authorization`.

Acceptance:

- Payment, refund, invoice, receipt, payment-method, financial-report and price mutation endpoints deny Teacher.
- Teacher routes and feature modules do not include financial administration components.

## ADM-001 — Authenticate as an invited administrator with MFA.

Rationale: Privileged control needs strong identity.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Admin invitation and activation are auditable.
- MFA is mandatory for every privileged session.

## ADM-002 — View authorized operational dashboard.

Rationale: Administrators need business control.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `admin_dashboard`.

Acceptance:

- Dashboard projects only the admin's granted capability groups.
- Finance summary requires finance permission.

## ADM-003 — Manage parent accounts and account lifecycle.

Rationale: Operations need account support.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `accounts_admin`.

Acceptance:

- Authorized admin can search, suspend, reactivate and process verified closure with audit reason.
- Suspension revokes sessions and blocks new protected actions.

## ADM-004 — Manage student profiles and verified guardian links.

Rationale: Operations need accurate and safe child records.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `students`.

Acceptance:

- Admin can correct minimum profile and approve/revoke verified guardian association.
- Link changes preserve history and require reason.

## ADM-005 — Manage teacher operational and public profiles.

Rationale: Operations need controlled staffing.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `teacher_profiles`.

Acceptance:

- Admin invites, suspends and edits teaching profile separately from approved published biography.

## ADM-006 — Manage narrowly defined role and admin capability grants.

Rationale: Privilege changes need explicit control.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `roles`.

Acceptance:

- Only identity_admin may grant/revoke roles and admin capability groups.
- Teacher/student privilege escalation through profile edit is rejected and grants are audited.
- Granting an admin finance capability to a Teacher principal is rejected, including indirect role combinations.

## ADM-007 — Manage programs and reusable courses.

Rationale: The business needs a curriculum catalogue.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `catalogue`.

Acceptance:

- Admin can create, revise, archive and explicitly publish programs/courses.
- Referenced courses cannot be destructively deleted.

## ADM-008 — Manage modules, lessons, lesson blocks and release rules.

Rationale: The business needs structured published learning.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `curriculum`.

Acceptance:

- Admin orders and validates supported block types.
- Publication pins coherent curriculum version and cohort release schedule.

## ADM-009 — Manage learning and internal teaching resources.

Rationale: Educators need safe content assets.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `resources`.

Acceptance:

- Resource metadata defines purpose, audience and course linkage.
- Only validated ready assets can be published.

## ADM-010 — Manage quiz definitions and questions.

Rationale: Courses need planned formative assessments.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `quizzes`.

Acceptance:

- Admin configures supported choice questions, answer key, passing score and attempt limits.
- Attempted versions remain immutable.

## ADM-011 — Manage assignments and project-work definitions.

Rationale: Courses need controlled deliverables.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `assignments`.

Acceptance:

- Admin defines instructions, due rule, accepted formats, rubric and resubmission policy.
- Published assignment version remains consistent with existing submissions.

## ADM-012 — Oversee assessments and released results.

Rationale: Operations need to resolve educational issues.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `assessment`.

Acceptance:

- education_admin can inspect and correct assessment through new audited revision.
- Original grade and release history remain preserved.

## ADM-013 — Manage cohort lifecycle and delivery capacity.

Rationale: Courses need independently scheduled delivery.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `cohorts`.

Acceptance:

- Admin creates draft cohort linked to reusable course version then publishes/enrols, closes and completes it.
- Capacity cannot be reduced below confirmed active seats.

## ADM-014 — Create, revise and cancel class sessions.

Rationale: Operations need schedule authority.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Authorized admin creates non-overlapping timezone-aware sessions, expands recurrence and reschedules with reason.
- Late change/cancellation triggers participant notices and provider reconciliation.

## ADM-015 — Assign and revoke teachers for cohorts/sessions.

Rationale: Teaching access requires authoritative assignment.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `teacher_assignments`.

Acceptance:

- Assignment dates and scopes are explicit.
- Revocation immediately removes protected access and checks remaining session staffing.

## ADM-016 — Manage enrolments and cancellation decisions.

Rationale: Operations need to resolve delivery changes.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Admin can review, cancel or approve authorized enrolment exception with audited reason.
- Cancellation and financial refund remain separate explicit decisions.

## ADM-017 — Oversee and correct attendance.

Rationale: Operations need auditable attendance support.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `attendance`.

Acceptance:

- education_admin can inspect scoped roster and correct a record with reason even after teacher correction window.

## ADM-018 — Oversee progress and course completion decisions.

Rationale: The business needs accountable completion.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `progress`.

Acceptance:

- education_admin can inspect progress and apply evidenced completion override with reason.
- Override does not erase source learning records.

## ADM-019 — Oversee teacher feedback release and correction.

Rationale: Operations need safeguarding and quality control.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `feedback`.

Acceptance:

- education_admin can review drafts and release/retract inappropriate feedback with audit reason.

## ADM-020 — Issue, revoke and reissue completion certificates.

Rationale: The business needs controlled completion evidence.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `certificates`.

Acceptance:

- Admin reissue/revoke actions preserve prior certificate identifier and reason.
- Issue requires policy-qualified completion or evidenced override.

## ADM-021 — Manage events and audience-scoped announcements.

Rationale: The business needs targeted communication.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `events`.

Acceptance:

- Admin can create, publish, expire and cancel scoped events/announcements.
- Audience expansion is validated against admin privileges.

## ADM-022 — Inspect and retry operational notification delivery.

Rationale: Operations need to diagnose missed messages.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `notifications`.

Acceptance:

- Admin sees redacted delivery status, attempt count and permitted retry.
- Retry deduplicates recipient/message intent.

## ADM-023 — Manage authorized resources and internal assets.

Rationale: Operations need asset lifecycle control.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- Admin can inspect metadata, quarantine or request deletion with reason.
- Download still checks asset audience and access purpose.

## ADM-024 — Configure approved course/cohort fees.

Rationale: Commercial offers need controlled AUD prices.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `pricing`.

Acceptance:

- finance_admin can set integer-cent prices and valid effective windows.
- Existing checkout/order snapshots retain original agreed amount.

## ADM-025 — Inspect payment records and reconciliation status.

Rationale: The business needs payment operations.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- finance_admin searches by internal order and provider identifiers and sees authoritative status.
- Teacher/student and non-finance admin requests are denied.

## ADM-026 — Administer full and partial refunds.

Rationale: Operations need controlled post-payment remedies.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `refunds`.

Acceptance:

- finance_admin requests amount up to unrefunded captured balance with reason.
- Provider result and retries are idempotent and auditable.

## ADM-027 — View and export launch financial reports.

Rationale: Operations need reconciled business records.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `financial_reporting`.

Acceptance:

- finance_admin filters gross payments, refunds and net amounts by date/status with AUD totals.
- Export is scoped, audited and excludes card data.

## ADM-028 — Manage operational and integration settings.

Rationale: Operations need controlled configuration.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `settings`.

Acceptance:

- operations_admin changes validated nonsecret settings and references externally managed secrets.
- Secret values are never returned in API or audit response.

## ADM-029 — Read authorized audit and operational history.

Rationale: Privileged actions need review.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `audit`.

Acceptance:

- audit_admin can filter actor, action, target and time.
- Audit content is append-only and excludes credentials and unnecessary child content.

## LRN-001 — Reuse one course across many cohorts.

Rationale: Curriculum must not be duplicated for each delivery.

Roles: Admin, Parent, Student, Teacher, Public. Priority: REQUIRED FOR LAUNCH. Capability: `catalogue`.

Acceptance:

- Course has independently versioned reusable curriculum.
- Multiple cohorts reference the same version with separate session and roster data.

## LRN-002 — Maintain Program → Course → Module → Lesson → LessonBlock hierarchy.

Rationale: Learning needs a coherent structure.

Roles: Admin, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `curriculum`.

Acceptance:

- Each child has one owning parent within course version and unique position.
- Cross-course block references are rejected unless explicitly reusable resource links.

## LRN-003 — Support the eight launch lesson-block variants.

Rationale: Structured content must meet launch teaching needs.

Roles: Admin, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `curriculum`.

Acceptance:

- Heading, RichText, Image, Video, DownloadableResource, Activity, QuizRef and AssignmentRef have validated type-specific payloads.
- Quiz/assignment references resolve within the course version.

## LRN-004 — Version and release curriculum predictably.

Rationale: Student work must remain tied to stable learning definitions.

Roles: Admin, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `curriculum`.

Acceptance:

- A published referenced version is immutable.
- Admin release schedule controls when enrolled learners can access each module/lesson.

## LRN-005 — Support uploaded media and approved external video resources.

Rationale: Lessons need video without unrestricted embedding.

Roles: Admin, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `resources`.

Acceptance:

- Video sources are owned assets or approved allowlisted provider URLs with captions/transcript support.
- No live-class recordings are captured or published at launch.

## LRN-006 — Record activity and lesson completion per enrolment.

Rationale: Learning progress needs a reliable source record.

Roles: Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `activities`.

Acceptance:

- Completion writes are idempotent for enrolment/item.
- Only eligible released learning items can be completed.

## LRN-007 — Calculate progress from required course items.

Rationale: Completion must have documented meaning.

Roles: Student, Parent, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `progress`.

Acceptance:

- Numerator includes completed required lessons/activities, passed required quizzes and satisfactory required assignments.
- Denominator is pinned to enrolment course version and excludes optional items.

## LRN-008 — Evaluate course completion against explicit policy.

Rationale: Certificate eligibility must be deterministic.

Roles: Student, Parent, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `progress`.

Acceptance:

- All required items completed and attendance of at least 80% of delivered non-cancelled sessions makes student eligible.
- Authorized override requires recorded evidence and reason.

## LRN-009 — Generate completion certificates with immutable identifiers.

Rationale: Completion evidence must be verifiable and controlled.

Roles: Student, Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `certificates`.

Acceptance:

- Certificate contains student's permitted display name, course/version, completion date and unique serial.
- One active issuance per enrolment/version with audited reissue/revoke.

## LRN-010 — Represent course-completion achievement only.

Rationale: Recognition must have a bounded launch design.

Roles: Student, Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `certificates`.

Acceptance:

- Completion achievement is derived from completion/certificate state.
- No points, badges economy or public leaderboard is created.

## CLS-001 — Maintain explicit cohort lifecycle.

Rationale: Delivery needs states independent from curriculum.

Roles: Admin, Parent, Teacher, Student. Priority: REQUIRED FOR LAUNCH. Capability: `cohorts`.

Acceptance:

- Transitions draft → published/open → closed/in_progress → completed or cancelled validate schedule and price prerequisites.
- Cancelled cohort cannot accept enrolments.

## CLS-002 — Store authoritative timezone-aware class sessions.

Rationale: Families need accurate times through daylight-saving changes.

Roles: Admin, Teacher, Parent, Student. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Each session stores UTC start/end plus IANA source timezone.
- Ambiguous/nonexistent local times require explicit resolution before save.

## CLS-003 — Prevent teaching and cohort scheduling conflicts.

Rationale: Sessions must be deliverable.

Roles: Admin, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Overlapping active sessions for the same cohort, assigned teacher or enrolled learner fail transactionally.
- Reschedule validates original and new policy windows.

## CLS-004 — Expand bounded recurring schedule into individual sessions.

Rationale: Recurring classes need manageable exceptions.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Weekly recurrence with finite count/end produces individually identified sessions.
- Editing one instance does not silently alter other sessions.

## CLS-005 — Scope teaching authorization by active assignment relationship.

Rationale: Teaching access must follow assigned duties.

Roles: Admin, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `teacher_assignments`.

Acceptance:

- Teacher assignment references cohort and optional session exception plus validity period.
- Expired/revoked assignments do not authorize data access.

## CLS-006 — Create Zoom meetings for scheduled sessions through a provider port.

Rationale: Each live session needs an external meeting.

Roles: Admin, Teacher, Student. Priority: REQUIRED FOR LAUNCH. Capability: `live_class`.

Acceptance:

- Eligible confirmed session produces one idempotently linked meeting.
- Provider-specific payloads remain inside adapter boundary.

## CLS-007 — Synchronize meeting update and cancellation lifecycle.

Rationale: External live logistics must match domain schedule.

Roles: Admin, Teacher, Student. Priority: REQUIRED FOR LAUNCH. Capability: `live_class`.

Acceptance:

- Outbox event updates/cancels meeting after domain commit.
- Failed sync records actionable status and retries without losing authoritative schedule.

## CLS-008 — Issue authorized time-bounded live start/join actions.

Rationale: Meeting access must respect enrollment and teaching boundaries.

Roles: Teacher, Student. Priority: REQUIRED FOR LAUNCH. Capability: `live_class`.

Acceptance:

- Student and authorized guardian-assisted joins are allowed from 15 minutes before scheduled start until end.
- Teacher starts from 30 minutes before until end.
- Cancelled sessions and revoked users are denied.
- Waiting room is enabled, join-before-host disabled and automatic/local/cloud recording disabled in the launch configuration.

## CLS-009 — Handle live-provider failure explicitly.

Rationale: Class failures need recoverable operations.

Roles: Admin, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `live_class`.

Acceptance:

- Unavailable provider returns retryable delivery status and operational alert.
- Stored secrets are redacted and no unrestricted fallback meeting URL is published.

## CLS-010 — Maintain one attendance record per enrolled student/session.

Rationale: Attendance must be consistent and auditable.

Roles: Teacher, Admin, Student, Parent. Priority: REQUIRED FOR LAUNCH. Capability: `attendance`.

Acceptance:

- Unique session/student record stores present/absent/late/excused and recording actor.
- All amendments preserve prior value/reason in audit.

## CLS-011 — Notify participants and synchronize external systems after schedule changes.

Rationale: Schedule changes must reach affected people.

Roles: Admin, Teacher, Parent, Student. Priority: REQUIRED FOR LAUNCH. Capability: `scheduling`.

Acceptance:

- Committed session revision emits deduplicated notification, Zoom and Calendar intents.
- UI identifies pending provider sync while showing authoritative time.

## ENR-001 — Validate child/cohort eligibility before reservation.

Rationale: Enrolment must respect guardian authority and course suitability.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Active guardian relationship, billing family membership, required consent, age band, enrolment window and capacity are checked server-side.
- Duplicate active child/cohort enrolment is rejected.
- Age must have been confirmed in the preceding 180 days and active sessions must not conflict with the child’s existing enrolments.

## ENR-002 — Reserve a cohort seat during checkout.

Rationale: Concurrent checkout must not oversell delivery.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Seat reservation is transactional and expires after 30 minutes.
- Concurrent successful reservations cannot exceed cohort capacity.

## ENR-003 — Activate enrolment only after verified payment.

Rationale: Learning entitlement must correspond to authoritative commercial state.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Signed provider event/server retrieval matching order amount/currency confirms payment and activates valid reservation once.
- Late success after expired unavailable seat enters paid_exception requiring admin resolution and does not oversell.

## ENR-004 — Track enrolment lifecycle and educational entitlement.

Rationale: Commercial and learning state need clear transitions.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- pending_payment → active → completed or cancelled with expired/paid_exception alternatives is documented.
- Failed checkout does not grant content/live access.

## ENR-005 — Cancel enrolment with accountable reason.

Rationale: Business cancellations need clear records.

Roles: Admin, Parent. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Admin cancellation immediately revokes future class joins and new submissions.
- Completed historical records remain viewable to authorized family for configured retention.

## ENR-006 — Make payment and cancellation conditions explicit before checkout.

Rationale: Parents need informed purchase acceptance.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Order summary identifies child, cohort schedule, fee, terms version and refund/cancellation policy.
- Required acknowledgements are recorded against order.

## ENR-007 — Resolve paid enrolment exceptions without losing financial records.

Rationale: Late/duplicate payment needs safe handling.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `enrolment`.

Acceptance:

- Admin may allocate an available seat or refund recorded payment with reason.
- No silent activation beyond capacity and no payment deletion occur.

## ASM-001 — Define immutable quiz questions and marking rules.

Rationale: Attempts need reproducible scoring.

Roles: Admin, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `quizzes`.

Acceptance:

- Launch questions are single-choice and multiple-choice with exact-match scoring, no negative marks.
- Published answer key is server-only until permitted result release.

## ASM-002 — Manage quiz attempts within configured limits.

Rationale: Attempts need reliable save and submission.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `quizzes`.

Acceptance:

- Quiz allows configured 1–5 attempts with default 3.
- Submit is idempotent, server scored and freezes answers.
- Required quiz completion uses best score meeting default 70% or configured threshold.

## ASM-003 — Release formative quiz results after submission.

Rationale: Learners need timely feedback.

Roles: Student, Parent, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `quizzes`.

Acceptance:

- Submitted attempt returns own score, correctness and approved explanation.
- Answer key from other unsubmitted quizzes is never included.

## ASM-004 — Specify assignment rubric, deadline and revision policy.

Rationale: Work must be assessed against known requirements.

Roles: Admin, Teacher, Student. Priority: REQUIRED FOR LAUNCH. Capability: `assignments`.

Acceptance:

- Assignment pins rubric/version and due instant per cohort.
- Late submissions are accepted and labelled late by default until cohort completion unless explicitly closed.

## ASM-005 — Preserve immutable submission versions.

Rationale: Teacher review needs trustworthy submitted work.

Roles: Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `submissions`.

Acceptance:

- Only student-owned ready files from the expected upload purpose may be submitted.
- Each version records submitted_at and superseded version with no overwrite.

## ASM-006 — Record draft assessment against a specific submission version.

Rationale: Assessment needs stable provenance.

Roles: Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `assessment`.

Acceptance:

- Assessment references immutable submission and rubric version, score/outcome, assessor and timestamp.
- Concurrent updates require version precondition.

## ASM-007 — Release and revise assessment deliberately.

Rationale: Learners must see approved results.

Roles: Teacher, Admin, Student, Parent. Priority: REQUIRED FOR LAUNCH. Capability: `assessment`.

Acceptance:

- Draft result remains educator-only.
- Release exposes result and feedback to learner/guardian.
- Correction creates a new revision and triggers targeted notice.

## ASM-008 — Maintain private-draft and released educational feedback states.

Rationale: Feedback visibility must be intentional.

Roles: Teacher, Admin, Student, Parent. Priority: REQUIRED FOR LAUNCH. Capability: `feedback`.

Acceptance:

- Draft → released → retracted transitions retain authorship and revision history.
- Retraction removes family/student view while audit remains.

## PAY-001 — Use one-time AUD cohort fees at launch.

Rationale: Billing must be simple and definite.

Roles: Admin, Parent, Public. Priority: REQUIRED FOR LAUNCH. Capability: `pricing`.

Acceptance:

- Every payable cohort resolves one integer-cent AUD fee with display total.
- No subscription, instalment, marketplace, coupon or discount path exists.

## PAY-002 — Create server-priced Stripe Checkout payment sessions.

Rationale: Hosted payment reduces card-data handling.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Server resolves immutable order amount, currency, child and cohort.
- Client price or family identifiers cannot change authorized purchase.
- Card details are entered only on Stripe-hosted UI.

## PAY-003 — Maintain immutable order and payment references.

Rationale: Transactions need reconciliation and financial auditability.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Order/payment retain internal UUID, checkout session, payment intent, charge/provider IDs where supplied, amount/currency and status history.
- Provider identifiers are unique where required.

## PAY-004 — Verify Stripe webhook authenticity before processing.

Rationale: Payment events are security-sensitive.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `webhooks`.

Acceptance:

- Raw request signature and freshness are validated.
- Invalid or replayed event cannot change financial/enrolment state.

## PAY-005 — Process payment events idempotently and out of order safely.

Rationale: Providers retry and may reorder notifications.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `webhooks`.

Acceptance:

- Unique provider event is persisted and processed once.
- State transitions use verified current provider state and duplicate delivery has no duplicate effect.

## PAY-006 — Represent checkout, payment and refund status separately.

Rationale: Financial truth must not be collapsed into a browser state.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Created/pending/succeeded/failed/cancelled payment and refund pending/succeeded/failed states map to provider truth.
- Browser redirect is informational only.

## PAY-007 — Issue immutable purchase invoice/receipt representations.

Rationale: Parents and the business need transaction documents.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Verified payment issues a downloadable receipt with provider reference and order snapshot.
- Invoice representation follows approved merchant tax/invoice settings and is versioned rather than overwritten.

## PAY-008 — Perform idempotent full or partial refunds within captured balance.

Rationale: Business remedies require financial controls.

Roles: Admin, Parent. Priority: REQUIRED FOR LAUNCH. Capability: `refunds`.

Acceptance:

- Requested total never exceeds captured amount minus succeeded/pending refunds.
- Refund success is verified from provider and linked to original payment with reason/actor.

## PAY-009 — Reconcile provider transactions to local financial records.

Rationale: Failures must be discoverable and recoverable.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Scheduled reconciliation compares pending/exception payments and refunds to provider identifiers.
- Mismatch creates actionable exception and cannot silently rewrite immutable amounts.

## PAY-010 — Produce launch payment/refund/net financial reports and exports.

Rationale: Operations need useful financial reporting.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `financial_reporting`.

Acceptance:

- Date-bounded report totals integer AUD cents and identifies timezone/status basis.
- CSV formula injection is neutralized and export is audited.

## PAY-011 — Separate financial refund from enrolment entitlement decision.

Rationale: Partial refund must not silently cancel education.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Refund request includes explicit KEEP or CANCEL educational-entitlement disposition authorized to finance admin.
- Cancellation reasons and financial outcome remain separately auditable.

## PAY-012 — Apply approved merchant identity, tax and refund policy settings.

Rationale: Production purchases need human-approved business configuration.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `billing`.

Acceptance:

- Production checkout is blocked until merchant, tax/invoice wording and refund terms gates are approved.
- Architecture uses versioned immutable order snapshots regardless of selected legal/tax settings.

## COM-001 — Send account registration and security emails through a provider port.

Rationale: Accounts need reliable verification and recovery.

Roles: Parent, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- Registration, verification, reset and email-change messages use purpose-bound expiring tokens.
- Sensitive tokens do not enter logs.

## COM-002 — Send enrolment confirmation after authoritative activation.

Rationale: Families need accurate enrolment notice.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- One confirmation is queued per activated enrolment and includes child display name, course/cohort and schedule link.

## COM-003 — Send verified payment/receipt and refund outcome notifications.

Rationale: Families need financial confirmation.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- Only verified successful financial transition queues success message to authorized billing recipients.
- Notification links require authenticated document access.

## COM-004 — Send class reminders and schedule-change notices.

Rationale: Participants need timely logistics.

Roles: Parent, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- Reminder intent is scheduled for 24h and 1h before session, adjusted for newly created sessions.
- Reschedule cancels old reminder intents and queues revised notices.

## COM-005 — Send assignment and released-feedback/result notifications.

Rationale: Learning actions need targeted follow-up.

Roles: Parent, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- New due-work and release events target permitted learner/guardian inboxes.
- Email goes to adult verified contacts and avoids detailed child assessment content.

## COM-006 — Send completion/certificate communication.

Rationale: Completion should reach the learner's family.

Roles: Parent, Student. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- Completion creates learner inbox notification and adult email with authenticated certificate link exactly once per issuance event.

## COM-007 — Provide recipient-scoped in-app notifications.

Rationale: All roles need a consistent operational inbox.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `notifications`.

Acceptance:

- Notification record has audience, kind, safe summary, action link and read timestamp.
- One recipient cannot read/update another recipient's notification.

## COM-008 — Publish role/course/cohort-scoped announcements and events.

Rationale: The business needs safe targeted notices.

Roles: Admin, Parent, Student, Teacher, Public. Priority: REQUIRED FOR LAUNCH. Capability: `announcements`.

Acceptance:

- Audience and publication/expiry time are explicit.
- Private audiences never appear in public listing or feed.

## COM-009 — Deliver noncritical email in background with retry and deduplication.

Rationale: Provider latency must not block ordinary API work.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `communications`.

Acceptance:

- Domain commit writes durable outbox intent.
- Worker uses bounded backoff, dead-letter status and redacted delivery log.
- Repeated intent never knowingly sends duplicate logical message.

## CAL-001 — Create Google Calendar events from authoritative sessions/events.

Rationale: External calendar needs accurate mirrors.

Roles: System, Admin, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `calendar`.

Acceptance:

- Calendar adapter upserts one provider event per domain session/event revision and stores external ID.
- No provider-side edit automatically overwrites domain schedule.

## CAL-002 — Synchronize schedule updates and cancellations.

Rationale: Mirrors must not show obsolete classes.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `calendar`.

Acceptance:

- Reschedule updates same linked event.
- Cancellation marks/deletes provider event and persists sync revision/status.

## CAL-003 — Represent recurrence as individually linked session events.

Rationale: Session exceptions must remain manageable.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `calendar`.

Acceptance:

- Each expanded recurrence occurrence has its own domain and external ID.
- One exception updates only that session event.

## CAL-004 — Offer authorized add-to-calendar exports.

Rationale: Families need convenient personal calendar use.

Roles: Parent, Student, Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `calendar`.

Acceptance:

- Authenticated user can export per-session ICS for owned/assigned schedule.
- Export contains no peer data or teacher host secret and uses stable UID/revision.

## CAL-005 — Recover calendar synchronization failures.

Rationale: External failure must not corrupt the timetable.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `calendar`.

Acceptance:

- Retry is idempotent and dead-letter/operational status is visible.
- Domain session remains authoritative and usable while sync is pending.

## FILE-001 — Store authoritative file metadata and object references.

Rationale: Object storage needs governed ownership.

Roles: Admin, Teacher, Student. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- File record contains owner, purpose, audience, expected MIME/size, checksum, storage key and lifecycle state.
- Database IDs are used in business contracts instead of raw keys.

## FILE-002 — Validate uploaded files before availability.

Rationale: Uploads must not become a security bypass.

Roles: Student, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- Student submission allowlist is PDF, PNG, JPEG, TXT and approved project ZIP, maximum 25 MiB (26,214,400 bytes) per file and 100 MiB (104,857,600 bytes) per submission; executable/script content is rejected and archives are scanned with expansion limits.
- Learning resources permit PDF, PNG, JPEG and TXT up to 50 MiB, MP4 up to 500 MiB or approved HTTPS video references; internal assets permit PDF, PNG, JPEG and TXT up to 25 MiB; generated certificate PDFs are limited to 5 MiB.
- Pending/unscanned files cannot be downloaded or submitted.

## FILE-003 — Use short-lived presigned uploads and authorized downloads.

Rationale: Browsers need secure object transfers.

Roles: Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- Upload grant expires within 10 minutes and is bound to object/purpose/size.
- Download grant expires within 5 minutes after current resource authorization.
- Permanent credentials are never exposed.

## FILE-004 — Quarantine unsafe uploads and make scan status explicit.

Rationale: Unsafe media must not reach children.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- Scanner failure leaves file pending/quarantined and produces operational alert.
- Only ready state assets can be referenced in published content/submissions.

## FILE-005 — Enforce file access through ownership and related-resource scope.

Rationale: Storage possession must not bypass authorization.

Roles: Student, Parent, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- Student own submission, guardian authorized child, assigned educator and explicit admin permission determine access.
- An arbitrary storage key or asset ID cannot grant access.

## FILE-006 — Delete eligible files and clean orphaned uploads safely.

Rationale: Storage must observe lifecycle and minimization.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- Unfinalized objects older than 24h are removed after reference check.
- Deletion tombstones metadata and asynchronously removes object after retention/legal hold checks.

## FILE-007 — Protect object storage and generated documents.

Rationale: Private teaching and child files need confidentiality.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `files`.

Acceptance:

- Buckets are private with encryption and scoped service credentials.
- Certificates/internal documents use same authorization and lifecycle controls as other assets.

## AUTH-001 — Authenticate accounts with secure password/session flows.

Rationale: Every protected surface needs trusted identity.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Passwords use Argon2id.
- Login issues opaque server-side session via HttpOnly Secure SameSite cookie.
- Invalid login returns generic error without account enumeration.

## AUTH-002 — Require MFA for educator and administrator roles.

Rationale: High-impact child/admin access needs stronger authentication.

Roles: Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- TOTP with single-use hashed recovery codes is mandatory for privileged role activation.
- Enrollment/recovery is audited and recovery cannot bypass verified support process.

## AUTH-003 — Rotate and revoke sessions safely.

Rationale: Stolen or stale sessions must be controllable.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Login privilege change and password reset rotate/revoke sessions.
- Idle expiry 30 minutes for staff, 12 hours parent/student with absolute lifetime seven days.
- Logout clears current session.

## AUTH-004 — Recover adult accounts through expiring single-use tokens.

Rationale: Users need safe recovery.

Roles: Parent, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Reset token expires after 30 minutes and is stored hashed.
- Successful reset consumes token and revokes sessions.
- Responses do not reveal email existence.

## AUTH-005 — Reset student credentials through authorized guardian/support action.

Rationale: Children need recovery without required personal email.

Roles: Parent, Student, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `identity`.

Acceptance:

- Verified active guardian or identity_admin resets authorized child's credential with audit.
- Student cannot obtain guardian session or email token.

## AUTH-006 — Authorize using role, relationship, ownership and resource state.

Rationale: Role labels alone cannot protect data.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `authorization`.

Acceptance:

- Every protected application operation evaluates actor capabilities plus resource relationship/state.
- Denied direct-ID and modified-client requests have no side effect.

## AUTH-007 — Enforce guardian/student and billing-family authorization separately.

Rationale: Shared guardianship must not expose unrelated family finances.

Roles: Parent. Priority: REQUIRED FOR LAUNCH. Capability: `authorization`.

Acceptance:

- Child educational read requires active GuardianStudent link.
- Billing requires active FamilyGuardian billing membership.
- Guardian link alone never grants another family's payment records.

## AUTH-008 — Restrict students to own permitted educational data.

Rationale: Student portal must remain a private learning environment.

Roles: Student. Priority: REQUIRED FOR LAUNCH. Capability: `authorization`.

Acceptance:

- Cross-student submission/profile/progress/certificate IDs are denied.
- Billing, administration, peer/private staff and family-management APIs deny Student.

## AUTH-009 — Restrict teachers to current educational assignments and deny finance.

Rationale: Teacher scope must not expand through guessed IDs.

Roles: Teacher. Priority: REQUIRED FOR LAUNCH. Capability: `authorization`.

Acceptance:

- Expired/unassigned cohort/student reads fail in service and query layer.
- All finance repositories and API operations reject teacher capability context.

## AUTH-010 — Use explicit administrative capability groups.

Rationale: Administrative access needs least privilege.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `authorization`.

Acceptance:

- identity_admin, education_admin, finance_admin, operations_admin and audit_admin gates apply per operation.
- No self-grant without identity_admin and audited privilege policy.
- Teacher principals cannot hold admin financial capabilities or gain finance through additive roles; a separate MFA-protected admin principal is required.

## AUTH-011 — Suspend and close accounts without losing required records.

Rationale: Account lifecycle needs safe access removal.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `account`.

Acceptance:

- Suspension revokes sessions and disables new login immediately.
- Closure follows authorized erasure/retention review and does not delete immutable financial/audit records.

## AUTH-012 — Test all role and resource boundaries negatively.

Rationale: Hidden navigation is insufficient protection.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `authorization`.

Acceptance:

- Tests cover Teacher→payment/unassigned learner, Parent→other child/family, Student→other submission/billing and nonprivileged Admin→finance.
- API, service and scoped repository tests prove denial.

## SEC-001 — Minimize child registration data.

Rationale: Children should not surrender unnecessary information.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `privacy`.

Acceptance:

- Name and numeric age are required, school optional, no DOB required.
- Health, address, biometric and identity-document fields are absent from default child schema.

## SEC-002 — Record purpose, visibility and retention for each personal-data field.

Rationale: Data collection needs accountable limits.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `privacy`.

Acceptance:

- DATA_REQUIREMENTS names each collected field, purpose, permitted role projection and retention class.
- Unknown fields fail validation rather than silently storing arbitrary sensitive data.

## SEC-003 — Preserve versioned policy acknowledgements and approval gates.

Rationale: Appropriate service consent needs evidence.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `consent`.

Acceptance:

- Acknowledgement links policy version, scope, actor and time.
- Legal text and child-safety publication are blocked pending recorded human review.

## SEC-004 — Protect production secrets outside source and responses.

Rationale: Provider and infrastructure credentials must remain secret.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `security`.

Acceptance:

- Secret references are injected at runtime from protected environment/store.
- Scanning rejects committed credentials and logs/API redact secret values.

## SEC-005 — Validate inputs and defend web/API boundaries.

Rationale: Untrusted requests must not corrupt data or sessions.

Roles: Public, Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `security`.

Acceptance:

- Typed schemas reject unknown/invalid fields.
- CSRF protects cookie-auth mutations.
- CORS uses explicit origins.
- Rich text is sanitized and query construction is parameterized.

## SEC-006 — Apply abuse limits to authentication, contact, checkout and uploads.

Rationale: Public and financial entry points need abuse resistance.

Roles: Public, Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `security`.

Acceptance:

- Account/IP limits enforce 5 login attempts per minute per identity plus broader IP control, 3 reset requests/hour, 5 contact/hour, 10 checkout/hour/family and configurable upload quota.
- Limits return retry guidance without leaking account existence.

## SEC-007 — Audit privileged and sensitive transitions append-only.

Rationale: Security and financial events need accountability.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `audit`.

Acceptance:

- Role/guardian changes, student access exports, schedule overrides, result corrections, refunds, settings and certificate changes record actor, action, target, timestamp, reason and correlation ID.
- Secrets and full child work content are excluded.

## SEC-008 — Keep logs and diagnostics free of unnecessary child/financial content.

Rationale: Observability must not create a second sensitive database.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `privacy`.

Acceptance:

- Logs use internal opaque IDs and redacted error summaries.
- No passwords, tokens, payment credentials, submission bodies or raw provider webhooks appear.

## SEC-009 — Support verified personal-data access/correction/deletion requests.

Rationale: Operations need a privacy request workflow.

Roles: Parent, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `privacy`.

Acceptance:

- Admin records request, verifies adult authority, exports permitted data and applies correction/retention decision.
- A request cannot expose another guardian's unrelated finances.

## SEC-010 — Enforce retention, archival and legal-hold states.

Rationale: Records need deliberate lifecycle management.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `privacy`.

Acceptance:

- Approved retention matrix drives scheduled purge/anonymization with evidence.
- Held records are not purged and hold changes are audited.

## SEC-011 — Publish child-safety reporting route and restrict child communication.

Rationale: The teaching service needs clear safeguarding boundaries.

Roles: Parent, Student, Teacher, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `child_safety`.

Acceptance:

- Parent/student can locate approved reporting channel.
- No student-peer messaging or teacher-private-chat system is built.
- Live rooms use waiting-room controls and recording is off.

## SEC-012 — Verify webhooks and provider callbacks at trust boundaries.

Rationale: External callbacks must not become privilege bypasses.

Roles: System. Priority: REQUIRED FOR LAUNCH. Capability: `security`.

Acceptance:

- Provider signature/authenticity and event deduplication occur before domain mutation.
- Unsupported/invalid event types are safely rejected or ignored with redacted audit.

## SEC-013 — Secure upload scanning, encrypted transport and private storage.

Rationale: Child work must not be publicly exposed.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `security`.

Acceptance:

- HTTPS is mandatory.
- Objects/backups are encrypted at rest.
- Unsafe file state blocks all audiences and presigned grants expire.

## SEC-014 — Prevent destructive or untraceable financial/admin mutation.

Rationale: High-impact records need controlled changes.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `security`.

Acceptance:

- Money uses integer minor units, optimistic version checks protect concurrent edits and append-only histories preserve financial truth.
- Audit deletion is unavailable through ordinary admin UI.

## OPS-001 — Provide reproducible containerized deployment for OCI-compatible VPS.

Rationale: The business needs operable production hosting.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `deployment`.

Acceptance:

- Documented Docker/Compose stack includes Next.js, FastAPI, worker, PostgreSQL, Redis and Caddy with health/dependency checks.
- Domain code contains no OCI dependency.

## OPS-002 — Terminate HTTPS with Caddy and expose only intended services.

Rationale: Production needs encrypted network boundaries.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `deployment`.

Acceptance:

- Only HTTPS/required HTTP redirect and controlled administration ingress are externally reachable.
- Database/Redis internal ports are not public.

## OPS-003 — Validate environment and integration configuration at startup.

Rationale: Misconfiguration must fail visibly.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `configuration`.

Acceptance:

- Missing/invalid required configuration prevents readiness and identifies safe setting names.
- Secrets are not printed.

## OPS-004 — Manage PostgreSQL schema through reviewed migrations.

Rationale: Data changes need repeatable rollout.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `database`.

Acceptance:

- Every migration has upgrade validation, backup/rollback or forward-fix plan and compatibility review.
- Production does not auto-migrate on every web replica start.

## OPS-005 — Run Redis-backed workers with durable PostgreSQL outbox.

Rationale: Async delivery must survive process failures.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `workers`.

Acceptance:

- Jobs are idempotent, retry bounded and dead-lettered.
- Outbox prevents lost intent after successful database commit and Redis loss can be recovered from durable state.

## OPS-006 — Run CI quality, contract, security and test gates on PRs.

Rationale: Merged work must meet the locked design.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `ci`.

Acceptance:

- CI validates lint/type/build/tests, requirement/chunk coverage, contract consistency and secret/dependency scans.
- Failure blocks review-ready handoff.

## OPS-007 — Use separate development, staging and production environments.

Rationale: Release validation must not expose live children.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `deployment`.

Acceptance:

- Environments isolate credentials, databases, buckets and providers.
- Synthetic staging data is used and production data is not casually copied.

## OPS-008 — Provide liveness/readiness and dependency health visibility.

Rationale: Operations need to distinguish failure modes.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `health`.

Acceptance:

- Liveness avoids sensitive data.
- Readiness checks essential dependencies with bounded timeout.
- Provider degradation is reported without making whole service unnecessarily unavailable.

## OPS-009 — Collect structured logs, metrics, errors and actionable alerts.

Rationale: Incidents need evidence and timely response.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `observability`.

Acceptance:

- Correlation IDs link API/job/provider attempts.
- Alerts cover error rate, payment mismatch, stale jobs, provider sync and backup failure without child-content leakage.

## OPS-010 — Back up PostgreSQL and object storage with retention and encryption.

Rationale: Production data must survive infrastructure loss.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `backups`.

Acceptance:

- Database PITR/WAL target RPO ≤15 minutes plus daily base backup.
- Object storage versioning/daily inventory and encrypted backup policy are documented.

## OPS-011 — Demonstrate complete restore into an isolated environment.

Rationale: A backup is useful only if restoration works.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `backups`.

Acceptance:

- Restore exercise validates DB integrity, object references and protected access within RTO ≤4 hours.
- Evidence records date, duration, exceptions and remediation.

## OPS-012 — Document incident, rollback and provider-failure recovery.

Rationale: Operations need executable runbooks.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `recovery`.

Acceptance:

- Runbooks cover deploy rollback, DB migration failure, credential rotation, queue recovery, provider outages and privacy incident escalation with owner contacts.

## OPS-013 — Scan dependencies, containers and secrets.

Rationale: Production needs a maintained security baseline.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `security_scanning`.

Acceptance:

- CI and scheduled operations produce actionable dependency/container vulnerability reports.
- Unresolved Critical/High exploitable findings block launch.

## OPS-014 — Deploy with versioned artifacts and verified smoke checks.

Rationale: Releases need controlled rollout.

Roles: System, Admin. Priority: REQUIRED FOR LAUNCH. Capability: `deployment`.

Acceptance:

- Deployment records commit/image/config/migration versions and validates health plus critical journeys.
- Rollback uses previously known image and schema-compatible procedure.

## OPS-015 — Pass a formal production launch gate.

Rationale: Merged feature PRs alone do not prove launch readiness.

Roles: Admin. Priority: REQUIRED FOR LAUNCH. Capability: `launch_gate`.

Acceptance:

- All required requirements are implemented and traced, Critical/High findings resolved, integrations/security/restore/accessibility/end-to-end checks evidenced and human business/legal gates approved.

