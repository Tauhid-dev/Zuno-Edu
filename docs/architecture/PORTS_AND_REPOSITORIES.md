# Ports and aggregate repositories

Status: DRAFT, scope 1.0 / architecture 2. Canonical structured contracts: [backend-catalog.json](backend-catalog.json). These are design contracts, not implemented classes or endpoints. Implementation ownership and requirement traceability are in CODE_BLUEPRINT.md and docs/planning/REQUIREMENT_TRACEABILITY.md.

Repositories return domain roots or named scoped projections, never an unscoped ORM session. Every application write uses UnitOfWork. Provider calls execute through durable intent outside database locks; each adapter maps provider errors to the named port failures.

## UserRepository

- **Type:** repository interface
- **Module:** identity
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Account,Credential,RoleGrant,TeacherProfile
- **Objects:** Account, Credential, RoleGrant, TeacherProfile
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** accounts,credentials,teacher_profiles
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports., list_accounts requires IdentityAdminScope and projects only AccountView from accounts; get_scoped for admin detail requires the same purpose. Account.version is used for account-status preconditions; RoleGrantView.version is not substituted. No credential/session/MFA-secret join for these selectors.
- **Requirements:** ADM-001, ADM-003, ADM-005, ADM-006, ADM-015, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-010, AUTH-011, CLS-005, NFR-012, PAR-001, STU-001, TCH-001, WEB-006, WEB-011
- **Chunks:** ZE-P02-C01, ZE-P02-C03, ZE-P02-C04, ZE-P03-C01, ZE-P05-C01

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| find_login(identifier:NormalizedIdentifier)->AccountCredentials? | find login | identifier:NormalizedIdentifier | AccountCredentials? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_scoped(id:uuid,scope:IdentityScope)->Account? | get scoped | id:uuid,scope:IdentityScope | Account? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_staff(scope:IdentityScope,filter:StaffFilter,page:Page)->Page[TeacherProfile] | list staff | scope:IdentityScope,filter:StaffFilter,page:Page | Page[TeacherProfile] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(account:Account,expected_version:int)->None | save | account:Account,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_assignment_candidates(scope:EducationScope,query:DisplayNameQuery,page:Page)->Page[TeachingCandidateView] | Select only active approved teacher accounts/profiles before paging, projecting id and display_name only; never reuse the identity-admin full staff directory | Trusted education-admin scope, bounded name query and actor-bound page | Page[TeachingCandidateView] | NotFoundWithinScope, PersistenceUnavailable |
| list_accounts(scope:IdentityAdminScope,filter:AccountDirectoryFilter,page:Page)->Page[AccountView] | Select account lifecycle targets by approved display/email search without loading credentials,session/MFA secrets or unrelated family/finance data | IdentityAdminScope from active administrator/current MFA; validated AccountDirectoryFilter(q,role,status); bounded Page(cursor,limit) | Page[AccountView], including current Account.version; whitelist only id,role,display_name,email,status,mfa_enabled,version | NotFoundWithinScope, PersistenceUnavailable |
| lock_identity_admin_membership(scope:IdentityAdminScope)->tuple[Account] | Acquire a transaction-scoped singleton membership lock and return current active identity-admin candidates; every role/status write takes this lock before Account row locks, so concurrent mutations cannot remove/suspend the last active identity admin. | scope:IdentityAdminScope | tuple[Account] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## SessionRepository

- **Type:** repository interface
- **Module:** identity
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Session
- **Objects:** Session
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** sessions,one_time_tokens
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011
- **Chunks:** ZE-P02-C01, ZE-P02-C03, ZE-P02-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| find_active(token_hash:TokenHash,now:Instant)->Session? | find active | token_hash:TokenHash,now:Instant | Session? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_owned(user_id:uuid,scope:SelfScope)->tuple[Session] | list owned | user_id:uuid,scope:SelfScope | tuple[Session] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| revoke_all(user_id:uuid)->int | revoke all | user_id:uuid | int | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(session:Session)->None | save | session:Session | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| consume_token(hash:TokenHash,purpose:TokenPurpose,now:Instant)->TokenSubject | consume token | hash:TokenHash,purpose:TokenPurpose,now:Instant | TokenSubject | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## FamilyRepository

- **Type:** repository interface
- **Module:** family
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Family,Guardian,GuardianStudent,BillingMembership,PolicyAcknowledgement
- **Objects:** Family, Guardian, GuardianStudent, BillingMembership, PolicyAcknowledgement
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** families,guardians,guardian_students,billing_memberships,policy_acknowledgements
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports., Relationship mutations lock Family then exact relationship row. Creation compares Family.version; revocation compares GuardianStudent.version or BillingMembership.version. Every relationship change increments both the changed row and Family.version; parent projections remain filtered.
- **Requirements:** AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-011, AUTH-012, PAR-002, PAR-004, PAR-006, PAR-021, SEC-003, STU-019, TCH-016
- **Chunks:** ZE-P02-C01, ZE-P02-C03, ZE-P02-C04, ZE-P02-C05, ZE-P04-C01, ZE-P04-C02, ZE-P06-C01, ZE-P06-C02, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P08-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(id:uuid,scope:FamilyScope)->Family? | get scoped | id:uuid,scope:FamilyScope | Family? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| resolve_guardian_scope(principal:Principal,student_id:uuid)->FamilyScope? | resolve guardian scope | principal:Principal,student_id:uuid | FamilyScope? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| resolve_billing_scope(principal:Principal,family_id:uuid)->BillingScope? | resolve billing scope | principal:Principal,family_id:uuid | BillingScope? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(family:Family,expected_version:int)->None | save | family:Family,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_acknowledgements(scope:FamilyScope,page:Page)->Page[PolicyAcknowledgement] | list acknowledgements | scope:FamilyScope,page:Page | Page[PolicyAcknowledgement] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_admin_relationships(family_id:uuid,scope:IdentityAdminScope)->AdminFamilyRelationshipsView? | Read same-snapshot explicit family, named existing guardians/students, guardian-child links and independent billing memberships with their own current row versions; never return payment records. | family_id:uuid,scope:IdentityAdminScope | AdminFamilyRelationshipsView? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| lock_relationships(family_id:uuid,scope:IdentityAdminScope)->Family? | Lock Family before relationship rows, hydrate current GuardianStudent and BillingMembership versions, preserve last-guardian checks, and commit row versions plus family version in one UnitOfWork. | family_id:uuid,scope:IdentityAdminScope | Family? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## StudentRepository

- **Type:** repository interface
- **Module:** family
- **Responsibility:** Aggregate persistence and purpose-scoped projection of StudentProfile
- **Objects:** StudentProfile
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** students
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-004, PAR-005, TCH-009
- **Chunks:** ZE-P02-C03, ZE-P02-C05, ZE-P06-C02, ZE-P08-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(id:uuid,scope:StudentReadScope)->StudentProfile? | get scoped | id:uuid,scope:StudentReadScope | StudentProfile? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_linked(scope:FamilyScope,page:Page)->Page[StudentProfile] | list linked | scope:FamilyScope,page:Page | Page[StudentProfile] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_teaching(scope:TeachingScope,page:Page)->Page[TeachingStudentProjection] | list teaching | scope:TeachingScope,page:Page | Page[TeachingStudentProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(student:StudentProfile,expected_version:int)->None | save | student:StudentProfile,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## ContentRepository

- **Type:** repository interface
- **Module:** content
- **Responsibility:** Aggregate persistence and purpose-scoped projection of PublicPage,PolicyDocument,ContactEnquiry
- **Objects:** PublicPage, PolicyDocument, ContactEnquiry
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** public_pages,public_page_revisions,policy_documents,contact_enquiries
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** WEB-001, WEB-002, WEB-007, WEB-008, WEB-009, WEB-010, WEB-012
- **Chunks:** ZE-P02-C05, ZE-P03-C01

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_published_page(slug:PublicPageSlug)->PublicPage? | get published page | slug:PublicPageSlug | PublicPage? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_policies(scope:PublicationScope,page:Page)->Page[PolicyDocument] | list policies | scope:PublicationScope,page:Page | Page[PolicyDocument] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_draft(id:uuid,scope:OperationsScope)->ContentAggregate? | get draft | id:uuid,scope:OperationsScope | ContentAggregate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(content:ContentAggregate,expected_version:int)->None | save | content:ContentAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_enquiries(scope:OperationsScope,page:Page)->Page[ContactEnquiry] | list enquiries | scope:OperationsScope,page:Page | Page[ContactEnquiry] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## CourseRepository

- **Type:** repository interface
- **Module:** curriculum
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Program,Course,CurriculumRevision,CourseModule,Lesson,LessonBlock,LearningResource
- **Objects:** Program, Course, CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** programs,courses,curriculum_revisions,course_modules,lessons,lesson_blocks,learning_resources
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-007, ADM-008, ADM-009, ADM-011, ASM-004, LRN-001, LRN-002, LRN-003, LRN-004, LRN-005, PAR-007, STU-003, STU-004, STU-005, TCH-003, WEB-003, WEB-004
- **Chunks:** ZE-P03-C01, ZE-P03-C02, ZE-P03-C03, ZE-P03-C04, ZE-P05-C01, ZE-P07-C01, ZE-P07-C02, ZE-P07-C05

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_course(id:uuid,scope:CourseScope)->Course? | get course | id:uuid,scope:CourseScope | Course? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_revision(id:uuid,scope:CurriculumScope)->CurriculumRevision? | get revision | id:uuid,scope:CurriculumScope | CurriculumRevision? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_courses(scope:CourseScope,filter:CourseFilter,page:Page)->Page[Course] | list courses | scope:CourseScope,filter:CourseFilter,page:Page | Page[Course] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_revision(revision:CurriculumRevision,expected_version:int)->None | save revision | revision:CurriculumRevision,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_course(course:Course,expected_version:int)->None | save course | course:Course,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_program(program:Program,expected_version:int)->None | save program | program:Program,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## DeliveryRepository

- **Type:** repository interface
- **Module:** delivery
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Cohort,ClassSession,TeacherAssignment
- **Objects:** Cohort, ClassSession, TeacherAssignment
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** cohorts,class_sessions,teacher_assignments
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-011, ADM-013, ADM-014, ADM-015, ADM-016, ADM-017, ADM-018, ADM-019, ASM-004, AUTH-010, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-011, NFR-012, PAR-009, STU-013, TCH-005, TCH-006, WEB-005
- **Chunks:** ZE-P02-C04, ZE-P03-C01, ZE-P03-C03, ZE-P03-C04, ZE-P04-C01, ZE-P04-C02, ZE-P05-C01, ZE-P05-C02, ZE-P05-C03, ZE-P05-C04, ZE-P05-C05, ZE-P06-C01, ZE-P06-C02, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P07-C02, ZE-P07-C03, ZE-P07-C04, ZE-P08-C02

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_cohort(id:uuid,scope:DeliveryScope,for_update:bool)->Cohort? | get cohort | id:uuid,scope:DeliveryScope,for_update:bool | Cohort? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_session(id:uuid,scope:DeliveryScope)->ClassSession? | get session | id:uuid,scope:DeliveryScope | ClassSession? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| resolve_teaching_scope(principal:Principal,cohort_id:uuid,session_id:uuid?)->TeachingScope? | resolve teaching scope | principal:Principal,cohort_id:uuid,session_id:uuid? | TeachingScope? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_schedule(scope:ScheduleScope,range:TimeRange,page:Page)->Page[ClassSession] | list schedule | scope:ScheduleScope,range:TimeRange,page:Page | Page[ClassSession] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| find_conflicts(slot:TimeSlot,participants:ParticipantIds,exclude_session_id:uuid?)->ScheduleConflicts | find conflicts | slot:TimeSlot,participants:ParticipantIds,exclude_session_id:uuid? | ScheduleConflicts | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(aggregate:DeliveryAggregate,expected_version:int)->None | save | aggregate:DeliveryAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## EnrolmentRepository

- **Type:** repository interface
- **Module:** enrolment
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Enrolment
- **Objects:** Enrolment
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** enrolments; read-only cohort learner projection joins students.id/first_name/preferred_name only
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-016, ADM-017, ADM-018, ADM-019, AUTH-010, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, LRN-007, LRN-008, NFR-012, PAR-008
- **Chunks:** ZE-P03-C03, ZE-P03-C04, ZE-P04-C01, ZE-P04-C02, ZE-P05-C02, ZE-P05-C03, ZE-P05-C05, ZE-P06-C01, ZE-P06-C02, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P07-C01, ZE-P07-C02, ZE-P07-C03, ZE-P07-C04, ZE-P07-C05, ZE-P07-C06

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(id:uuid,scope:EnrolmentScope,for_update:bool)->Enrolment? | get scoped | id:uuid,scope:EnrolmentScope,for_update:bool | Enrolment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:EnrolmentScope,filter:EnrolmentFilter,page:Page)->Page[Enrolment] | list scoped | scope:EnrolmentScope,filter:EnrolmentFilter,page:Page | Page[Enrolment] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| count_committed(cohort_id:uuid,now:Instant)->SeatCounts | count committed | cohort_id:uuid,now:Instant | SeatCounts | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_child_cohort(student_id:uuid,cohort_id:uuid,scope:EnrolmentScope)->Enrolment? | get child cohort | student_id:uuid,cohort_id:uuid,scope:EnrolmentScope | Enrolment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| lock_expired_holds(cutoff:Instant,batch_size:int)->tuple[Enrolment] | lock expired holds | cutoff:Instant,batch_size:int | tuple[Enrolment] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(enrolment:Enrolment,expected_version:int)->None | save | enrolment:Enrolment,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_education_learners(cohort_id:uuid,scope:EducationAdminScope,query:DisplayNameQuery,page:Page)->Page[EducationLearnerView] | Join enrolments to students for first/preferred display name only after verifying explicit cohort education scope; never hydrate StudentProfile/Account/Family or payment records; scope before paging. | cohort_id:uuid,scope:EducationAdminScope,query:DisplayNameQuery,page:Page | Page[EducationLearnerView] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## AttendanceRepository

- **Type:** repository interface
- **Module:** delivery
- **Responsibility:** Aggregate persistence and purpose-scoped projection of AttendanceRecord
- **Objects:** AttendanceRecord
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** attendance_records
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-017, CLS-010, PAR-010, STU-015, TCH-007, TCH-008
- **Chunks:** ZE-P05-C05, ZE-P07-C05

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| list_scoped(scope:AttendanceScope,filter:AttendanceFilter,page:Page)->Page[AttendanceRecord] | list scoped | scope:AttendanceScope,filter:AttendanceFilter,page:Page | Page[AttendanceRecord] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_for_update(session_id:uuid,student_id:uuid,scope:AttendanceWriteScope)->AttendanceRecord? | Read/lock exact current attendance row under active teaching or education-admin scope; absence is explicit and never creates data. | session_id:uuid,student_id:uuid,scope:AttendanceWriteScope | AttendanceRecord? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| summarize(enrolment_id:uuid,scope:ProgressScope)->AttendanceCounts | summarize | enrolment_id:uuid,scope:ProgressScope | AttendanceCounts | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(record:AttendanceRecord,expected_version:int)->None | save | record:AttendanceRecord,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_conditional(record:AttendanceRecord,scope:AttendanceWriteScope,expected_version:int?)->None | Scope is active assigned teacher or education admin; expected_version None means require row absence for exact(session_id,student_id), otherwise require current positive version. Serialize with session/cohort and unique key; conflict never overwrites another marker. | record:AttendanceRecord,scope:AttendanceWriteScope,expected_version:int? | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## AssessmentRepository

- **Type:** repository interface
- **Module:** assessment
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Quiz,QuizQuestion,QuizAttempt,Assignment,Submission,Assessment,TeacherFeedback
- **Objects:** Quiz, QuizQuestion, QuizAttempt, Assignment, Submission, Assessment, TeacherFeedback, AssignmentDeliveryRule
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** quizzes,quiz_questions,quiz_options,quiz_attempts,quiz_answers,assignments,assignment_delivery_rules,submissions,submission_assets,assessments,assessment_revisions,teacher_feedback,feedback_revisions; assignment_delivery_rules
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-010, ADM-011, ADM-012, ADM-019, ASM-001, ASM-002, ASM-003, ASM-004, ASM-005, ASM-006, ASM-007, ASM-008, PAR-012, PAR-013, STU-007, STU-008, STU-009, STU-010, STU-011, STU-012, TCH-010, TCH-011, TCH-012, TCH-013
- **Chunks:** ZE-P03-C03, ZE-P03-C04, ZE-P07-C01, ZE-P07-C02, ZE-P07-C03, ZE-P07-C04, ZE-P07-C05

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_definition(id:uuid,scope:CurriculumScope)->AssessmentDefinition? | get definition | id:uuid,scope:CurriculumScope | AssessmentDefinition? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_definitions(scope:CurriculumScope,filter:DefinitionFilter,page:Page)->Page[AssessmentDefinition] | list definitions | scope:CurriculumScope,filter:DefinitionFilter,page:Page | Page[AssessmentDefinition] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_work(id:uuid,scope:WorkScope,for_update:bool)->AssessmentAggregate? | get work | id:uuid,scope:WorkScope,for_update:bool | AssessmentAggregate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_work(scope:WorkScope,filter:WorkFilter,page:Page)->Page[WorkProjection] | list work | scope:WorkScope,filter:WorkFilter,page:Page | Page[WorkProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| count_attempts(quiz_id:uuid,enrolment_id:uuid,locked:bool)->AttemptCount | count attempts | quiz_id:uuid,enrolment_id:uuid,locked:bool | AttemptCount | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_definition(definition:AssessmentDefinition,revision_version:int)->None | save definition | definition:AssessmentDefinition,revision_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_work(work:AssessmentAggregate,expected_version:int)->None | save work | work:AssessmentAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_assessment_state(submission_id:uuid,scope:MarkingScope)->AssessmentStateView? | Validate accessible frozen submission under active assigned teacher or education-admin scope, then return nullable current assessment; missing/inaccessible submission returns None. Read-only, no guessed initial version. | submission_id:uuid,scope:MarkingScope | AssessmentStateView? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_assessment_conditional(assessment:Assessment,scope:MarkingScope,expected_version:int?)->None | Lock frozen submission then assessment; None means require absence, positive value means require matching current assessment version; unique submission constraint plus row lock prevents concurrent first-save overwrite. Preserve immutable assessment revision/audit. | assessment:Assessment,scope:MarkingScope,expected_version:int? | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_delivery_closure(assignment_id:uuid,cohort_id:uuid,scope:EducationAdminScope)->AssignmentClosureView? | Validate assignment in cohort pinned revision; return existing delivery rule or explicit absence/default values without persisting a row. Never reuse immutable definition version. | assignment_id:uuid,cohort_id:uuid,scope:EducationAdminScope | AssignmentClosureView? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_delivery_rule_conditional(rule:AssignmentDeliveryRule,scope:EducationAdminScope,expected_version:int?)->None | Lock cohort/assignment delivery key shared with submission finalization; None requires exact pair absent, positive requires same rule current version; insert/increment version atomically with closure audit. | rule:AssignmentDeliveryRule,scope:EducationAdminScope,expected_version:int? | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## ProgressRepository

- **Type:** repository interface
- **Module:** learning
- **Responsibility:** Aggregate persistence and purpose-scoped projection of StudentProgress,ActivityCompletion
- **Objects:** StudentProgress, ActivityCompletion, CompletionOverride
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** student_progress,activity_completions,completion_overrides
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-018, AUTH-010, LRN-006, LRN-007, LRN-008, NFR-012, PAR-011, STU-006, STU-016, TCH-014
- **Chunks:** ZE-P07-C05, ZE-P07-C06

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(enrolment_id:uuid,scope:ProgressScope)->StudentProgress? | get scoped | enrolment_id:uuid,scope:ProgressScope | StudentProgress? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:ProgressScope,page:Page)->Page[StudentProgress] | list scoped | scope:ProgressScope,page:Page | Page[StudentProgress] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_activities(enrolment_id:uuid,scope:StudentScope)->tuple[ActivityCompletion] | list activities | enrolment_id:uuid,scope:StudentScope | tuple[ActivityCompletion] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_activity(record:ActivityCompletion,expected_version:int)->None | save activity | record:ActivityCompletion,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_progress(progress:StudentProgress,expected_version:int)->None | save progress | progress:StudentProgress,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_override_for_update(enrolment_id:uuid,scope:EducationAdminScope)->CompletionOverride? | Load current exceptional decision under enrolment lock | enrolment_id:uuid,scope:EducationAdminScope | CompletionOverride? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_override_history(enrolment_id:uuid,scope:EducationAdminScope)->tuple[CompletionOverride] | Read evidence history for authorized education oversight only | enrolment_id:uuid,scope:EducationAdminScope | tuple[CompletionOverride] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_override(override:CompletionOverride,scope:EducationAdminScope,expected_version:int)->None | Persist evidenced grant plus progress eligibility audit/outbox in same UnitOfWork | override:CompletionOverride,scope:EducationAdminScope,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| revoke_override(override_id:uuid,reason:Reason,scope:EducationAdminScope,expected_version:int)->None | Record audited revocation and enqueue progress/certificate eligibility review | override_id:uuid,reason:Reason,scope:EducationAdminScope,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_completion_review(enrolment_id:uuid,scope:EducationAdminScope)->CompletionReviewView? | Read current progress version and same-enrolment active/history overrides in one snapshot; private history never included in parent/student/teacher projections. | enrolment_id:uuid,scope:EducationAdminScope | CompletionReviewView? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_progress_for_update(enrolment_id:uuid,scope:ProgressMutationScope)->StudentProgress? | Acquire progress row lock before override rows for every recompute/grant/revoke. Scope is education-admin or trusted progress-worker only, never client supplied. | enrolment_id:uuid,scope:ProgressMutationScope | StudentProgress? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| initialize_for_enrolment(enrolment_id:uuid,scope:SystemProgressScope)->None | Idempotently insert StudentProgress version 1 with empty counts and no override when the enrolment activates; unique enrolment key prevents duplicates. Activation event persists atomically, and progress initialization must finish before completion review becomes available; later recomputations increment version. | enrolment_id:uuid,scope:SystemProgressScope | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## CertificateRepository

- **Type:** repository interface
- **Module:** learning
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Certificate
- **Objects:** Certificate
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** certificates
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-020, LRN-009, LRN-010, PAR-014, STU-017
- **Chunks:** ZE-P07-C06

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(id:uuid,scope:CertificateScope)->Certificate? | get scoped | id:uuid,scope:CertificateScope | Certificate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:CertificateScope,filter:CertificateFilter,page:Page)->Page[Certificate] | list scoped | scope:CertificateScope,filter:CertificateFilter,page:Page | Page[Certificate] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_current_for_update(enrolment_id:uuid)->Certificate? | get current for update | enrolment_id:uuid | Certificate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(certificate:Certificate,expected_version:int)->None | save | certificate:Certificate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## PaymentRepository

- **Type:** repository interface
- **Module:** billing
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Price,Payment,Refund,Receipt
- **Objects:** Price, Payment, Refund, Receipt, ReconciliationException, FinancialExport
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** prices,payments,payment_events,refunds,purchase_documents,reconciliation_exceptions,privacy_exports(financial_export purpose); courses/cohorts read-only identity/title/status projection for finance price targets; curriculum/delivery mutation ownership remains in their modules
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports., list_price_targets is FinanceScope only; read-only columns from courses/cohorts are IDs,titles,status,course association. It never requires a Price row/publication and never returns curriculum,rosters,staff data or sessions; this projection grants no education read/mutation rights.
- **Requirements:** ADM-024, ADM-025, ADM-026, AUTH-010, NFR-012, PAR-017, PAR-018, PAR-019, PAR-020, PAY-001, PAY-002, PAY-003, PAY-006, PAY-007, PAY-008, PAY-009, PAY-011, PAY-012
- **Chunks:** ZE-P03-C01, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| resolve_price(course_id:uuid,cohort_id:uuid,at:Instant)->PriceSnapshot | resolve price | course_id:uuid,cohort_id:uuid,at:Instant | PriceSnapshot | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_payment(id:uuid,scope:BillingScope,for_update:bool)->Payment? | get payment | id:uuid,scope:BillingScope,for_update:bool | Payment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_payments(scope:BillingScope,filter:PaymentFilter,page:Page)->Page[Payment] | list payments | scope:BillingScope,filter:PaymentFilter,page:Page | Page[Payment] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| find_by_provider(reference:ProviderPaymentRef,scope:SystemBillingScope)->Payment? | find by provider | reference:ProviderPaymentRef,scope:SystemBillingScope | Payment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| lock_refundable_balance(payment_id:uuid)->RefundBalance | lock refundable balance | payment_id:uuid | RefundBalance | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_refunds(payment_id:uuid,scope:BillingScope)->tuple[Refund] | list refunds | payment_id:uuid,scope:BillingScope | tuple[Refund] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| report(scope:FinanceScope,range:DateRange)->FinanceReport | report | scope:FinanceScope,range:DateRange | FinanceReport | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(aggregate:BillingAggregate,expected_version:int)->None | save | aggregate:BillingAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_receipt(id:uuid,scope:BillingScope)->Receipt? | Read immutable purchase document under financial scope | id:uuid,scope:BillingScope | Receipt? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_receipts(payment_id:uuid,scope:BillingScope)->tuple[Receipt] | List only authorized purchase documents | payment_id:uuid,scope:BillingScope | tuple[Receipt] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_receipt(receipt:Receipt,scope:SystemBillingScope)->None | Persist immutable receipt and generated financial-document asset reference | receipt:Receipt,scope:SystemBillingScope | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_prices(filter:PriceFilter,scope:FinanceScope,page:Page)->Page[Price] | Read effective dated fee configuration | filter:PriceFilter,scope:FinanceScope,page:Page | Page[Price] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_price_for_update(id:uuid,scope:FinanceScope)->Price? | Load fee for versioned retirement | id:uuid,scope:FinanceScope | Price? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_price(price:Price,scope:FinanceScope,expected_version:int)->None | Persist fee and exclusion-constraint validation | price:Price,scope:FinanceScope,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| record_provider_exception(reference:VerifiedProviderPayment,reason:ReconciliationException)->ReconciliationExceptionId | Persist provider transaction lacking a local purchase for finance investigation; never invent child/family ownership | reference:VerifiedProviderPayment,reason:ReconciliationException | ReconciliationExceptionId | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_reconciliation_exceptions(scope:FinanceScope,filter:ExceptionFilter,page:Page)->Page[ReconciliationException] | Return unmatched provider financial evidence to finance administrators | scope:FinanceScope,filter:ExceptionFilter,page:Page | Page[ReconciliationException] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_reconciliation_exception_for_update(id:uuid,scope:FinanceScope)->ReconciliationException? | Lock exception before verified resolution | id:uuid,scope:FinanceScope | ReconciliationException? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_reconciliation_exception(exception:ReconciliationException,expected_version:int)->None | Persist verified matched/reversed outcome; never fabricate ownership | exception:ReconciliationException,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| create_finance_export(export:FinancialExport,scope:FinanceScope)->None | Persist immutable requester/date-range/job identity together with generation outbox | export:FinancialExport,scope:FinanceScope | None | RepositoryConflict, NotFoundWithinScope, ExportLimitExceeded, PersistenceUnavailable |
| get_finance_export(id:uuid,scope:FinanceScope,for_update:bool)->FinancialExport? | Load status/asset only for requesting finance admin or explicit finance oversight | id:uuid,scope:FinanceScope,for_update:bool | FinancialExport? | RepositoryConflict, NotFoundWithinScope, ExportLimitExceeded, PersistenceUnavailable |
| save_finance_export(export:FinancialExport,scope:SystemFinanceScope,expected_version:int)->None | Store ready/expired state and verified private asset association | export:FinancialExport,scope:SystemFinanceScope,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, ExportLimitExceeded, PersistenceUnavailable |
| iter_finance_rows(range:DateRange,scope:SystemFinanceScope,batch_size:int)->Iterator[FinanceReportRow] | Read bounded immutable financial snapshot rows; batches<=1000, report<=100000rows/100MiB, formula-safe formatting in report application use case | range:DateRange,scope:SystemFinanceScope,batch_size:int | Iterator[FinanceReportRow] | RepositoryConflict, NotFoundWithinScope, ExportLimitExceeded, PersistenceUnavailable |
| list_price_targets(scope:FinanceScope,filter:PriceTargetFilter,page:Page)->Page[PriceTargetView] | Provide minimal named targets for first-time and future fee configuration, including draft/unpublished/unpriced targets without requiring education privileges | FinanceScope from active finance administrator/current MFA; validated PriceTargetFilter(kind,course_id,q); bounded Page(cursor,limit) | Page[PriceTargetView] with strict course/cohort discriminator, current titles/status and nullable cohort fields; no Price or education entity dump | NotFoundWithinScope, PersistenceUnavailable |

## CommunicationRepository

- **Type:** repository interface
- **Module:** communication
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Event,Announcement
- **Objects:** Event, Announcement
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** events,announcements
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-021, COM-008, PAR-015, STU-018
- **Chunks:** ZE-P05-C04, ZE-P08-C02

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(id:uuid,scope:AudienceScope)->CommunicationAggregate? | get scoped | id:uuid,scope:AudienceScope | CommunicationAggregate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:AudienceScope,filter:CommunicationFilter,page:Page)->Page[CommunicationProjection] | list scoped | scope:AudienceScope,filter:CommunicationFilter,page:Page | Page[CommunicationProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(aggregate:CommunicationAggregate,expected_version:int)->None | save | aggregate:CommunicationAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## NotificationRepository

- **Type:** repository interface
- **Module:** communication
- **Responsibility:** Aggregate persistence and purpose-scoped projection of Notification,NotificationDelivery
- **Objects:** Notification, NotificationDelivery
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** notifications,notification_deliveries
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-021, ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-003, PAR-015, PAR-016, STU-018, TCH-015
- **Chunks:** ZE-P02-C01, ZE-P02-C03, ZE-P03-C01, ZE-P08-C01

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| list_owned(scope:SelfScope,filter:NotificationFilter,page:Page)->Page[Notification] | list owned | scope:SelfScope,filter:NotificationFilter,page:Page | Page[Notification] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_owned(id:uuid,scope:SelfScope)->Notification? | get owned | id:uuid,scope:SelfScope | Notification? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| insert_deduplicated(notification:Notification)->InsertOutcome | insert deduplicated | notification:Notification | InsertOutcome | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| claim_delivery(id:uuid,scope:SystemNotificationScope,lease:Lease)->NotificationDelivery? | claim delivery | id:uuid,scope:SystemNotificationScope,lease:Lease | NotificationDelivery? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_delivery(delivery:NotificationDelivery,expected_version:int)->None | save delivery | delivery:NotificationDelivery,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_deliveries(scope:OperationsScope,filter:DeliveryFilter,page:Page)->Page[DeliveryProjection] | list deliveries | scope:OperationsScope,filter:DeliveryFilter,page:Page | Page[DeliveryProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## FileRepository

- **Type:** repository interface
- **Module:** files
- **Responsibility:** Aggregate persistence and purpose-scoped projection of FileAsset
- **Objects:** FileAsset
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** file_assets,asset_links; purpose-scoped upload-context reads/locks over submissions,enrolments,curriculum_revisions,accounts only
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports., Generated financial_document/export metadata and private storage references remain financial scope only; no teaching/public scope grants., Upload context is closed by purpose: owned draft submission, writable educational revision, or own operations-admin account asset collection. Source rows and current privilege are rechecked; no arbitrary UUID/other account accepted. Only explicit public-content linkage makes ready public_asset public.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Chunks:** ZE-P02-C05, ZE-P03-C03, ZE-P03-C04, ZE-P04-C01, ZE-P04-C02, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P07-C03, ZE-P07-C06, ZE-P08-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(id:uuid,scope:FileScope)->FileAsset? | get scoped | id:uuid,scope:FileScope | FileAsset? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_scan_target(id:uuid,scope:SystemFileScope,for_update:bool)->FileAsset? | get scan target | id:uuid,scope:SystemFileScope,for_update:bool | FileAsset? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:FileScope,filter:FileFilter,page:Page)->Page[FileAsset] | list scoped | scope:FileScope,filter:FileFilter,page:Page | Page[FileAsset] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| reference_count(id:uuid)->int | reference count | id:uuid | int | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| lock_orphans(cutoff:Instant,batch_size:int)->tuple[FileAsset] | lock orphans | cutoff:Instant,batch_size:int | tuple[FileAsset] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(asset:FileAsset,expected_version:int)->None | save | asset:FileAsset,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_generated_asset(asset:FileAsset,proof:GeneratedArtifactProof,scope:SystemGeneratedFileScope,expected_version:int)->None | Persist generated ready metadata only after immutable object existence,size and SHA256 verified; atomic link to owning receipt/certificate/export | asset:FileAsset,proof:GeneratedArtifactProof,scope:SystemGeneratedFileScope,expected_version:int | None | RepositoryConflict, IntegrityMismatch, PersistenceUnavailable |
| resolve_upload_context(purpose:UploadPurpose,context_id:uuid,scope:UploadActorScope,for_update:bool)->FileUploadContext? | Closed tagged context: own draft Submission with eligible enrolment; education-admin writable draft CurriculumRevision; or operations-admin own Account asset collection for internal/public_asset. Resolve exact source row/current status and MIME/size policy; return no context for mismatched kind, owner, revoked role or arbitrary ID. Confirmation/deletion locks the owning context to serialize with publication/submission finalization. | purpose:UploadPurpose,context_id:uuid,scope:UploadActorScope,for_update:bool | FileUploadContext? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## IntegrationRepository

- **Type:** repository interface
- **Module:** operations
- **Responsibility:** Aggregate persistence and purpose-scoped projection of IntegrationBinding,WebhookInbox,OutboxEvent,BackgroundJob
- **Objects:** IntegrationBinding, WebhookInbox, OutboxEvent, BackgroundJob
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** integration_bindings,webhook_inbox,outbox_events,background_jobs,idempotency_records
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** OPS-003, OPS-005, PAY-004, PAY-005
- **Chunks:** ZE-P01-C02, ZE-P05-C03, ZE-P05-C04, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P08-C03

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| insert_inbox_unique(event:VerifiedWebhook)->InboxInsertOutcome | insert inbox unique | event:VerifiedWebhook | InboxInsertOutcome | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_binding(resource:MirrorResource,provider:Provider)->IntegrationBinding? | get binding | resource:MirrorResource,provider:Provider | IntegrationBinding? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| claim_outbox(batch_size:int,lease:Lease)->tuple[OutboxEvent] | claim outbox | batch_size:int,lease:Lease | tuple[OutboxEvent] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| claim_job(id:uuid,scope:JobScope,lease:Lease)->BackgroundJob? | claim job | id:uuid,scope:JobScope,lease:Lease | BackgroundJob? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_jobs(scope:JobScope,filter:JobFilter,page:Page)->Page[JobProjection] | list jobs | scope:JobScope,filter:JobFilter,page:Page | Page[JobProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(record:IntegrationRecord,expected_version:int)->None | save | record:IntegrationRecord,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| reserve_idempotency(key:IdempotencyScope,body_hash:string)->IdempotencyResult | reserve idempotency | key:IdempotencyScope,body_hash:string | IdempotencyResult | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## SettingsRepository

- **Type:** repository interface
- **Module:** operations
- **Responsibility:** Aggregate persistence and purpose-scoped projection of ApplicationSetting
- **Objects:** ApplicationSetting
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** application_settings
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-028
- **Chunks:** ZE-P01-C02, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P08-C03

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_typed(key:SettingKey,scope:SettingsScope)->ApplicationSetting? | get typed | key:SettingKey,scope:SettingsScope | ApplicationSetting? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_allowed(scope:SettingsScope)->tuple[ApplicationSetting] | list allowed | scope:SettingsScope | tuple[ApplicationSetting] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(setting:ApplicationSetting,expected_version:int)->None | save | setting:ApplicationSetting,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| launch_readiness()->LaunchReadiness | launch readiness |  | LaunchReadiness | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## AuditRepository

- **Type:** repository interface
- **Module:** operations
- **Responsibility:** Aggregate persistence and purpose-scoped projection of AuditRecord
- **Objects:** AuditRecord
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** audit_records
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** ADM-029, SEC-007
- **Chunks:** ZE-P02-C02

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| append(record:AuditRecord)->None | append | record:AuditRecord | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_redacted(scope:AuditScope,filter:AuditFilter,page:Page)->Page[AuditProjection] | list redacted | scope:AuditScope,filter:AuditFilter,page:Page | Page[AuditProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## PrivacyRepository

- **Type:** repository interface
- **Module:** family
- **Responsibility:** Aggregate persistence and purpose-scoped projection of PrivacyRequest
- **Objects:** PrivacyRequest, RetentionHold
- **Adapter:** SQLAlchemy data-mapper adapter; PostgreSQL
- **Persistence:** privacy_requests,retention_holds,privacy_exports,retention_decisions; minimal target identity projection over families,students,payments,file_assets and explicit ownership links only
- **Invariants:** Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports.
- **Requirements:** AUTH-010, NFR-012, SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Chunks:** ZE-P02-C05, ZE-P08-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_scoped(id:uuid,scope:PrivacyScope,for_update:bool)->PrivacyRequest? | get scoped | id:uuid,scope:PrivacyScope,for_update:bool | PrivacyRequest? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:PrivacyScope,filter:PrivacyFilter,page:Page)->Page[PrivacyRequest] | list scoped | scope:PrivacyScope,filter:PrivacyFilter,page:Page | Page[PrivacyRequest] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| has_hold(resource:RetentionResource)->bool | has hold | resource:RetentionResource | bool | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(request:PrivacyRequest,expected_version:int)->None | save | request:PrivacyRequest,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| record_retention_decision(decision:RetentionDecision)->None | record retention decision | decision:RetentionDecision | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_hold_targets(scope:IdentityAdminScope,resource_type:RetentionResourceType,family_id:uuid?,page:Page)->Page[LegalHoldTargetView] | Project only typed target IDs, display references and existing family/student ownership links; include targets without hold rows; no financial/file content, keys or URLs. | scope:IdentityAdminScope,resource_type:RetentionResourceType,family_id:uuid?,page:Page | Page[LegalHoldTargetView] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_hold_state(resource_type:RetentionResourceType,resource_id:uuid,scope:IdentityAdminScope)->LegalHoldStateView? | Read typed target existence and independent hold state; absent hold row maps to hold_version 0 without creating data; missing target returns None. | resource_type:RetentionResourceType,resource_id:uuid,scope:IdentityAdminScope | LegalHoldStateView? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| set_hold(hold:RetentionHold,scope:IdentityAdminScope,expected_hold_version:int)->None | Shared target/ancestor purge lock then exact CAS; expected 0 inserts only if absent; positive updates only matching current hold version; preserve released row and audit atomically. | hold:RetentionHold,scope:IdentityAdminScope,expected_hold_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## PaymentGateway

- **Type:** integration port
- **Module:** billing
- **Responsibility:** Signature verification requires original bytes; authoritative server state; timeout unknown outcome reconciled; raw secrets never domain
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** Stripe adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Signature verification requires original bytes; authoritative server state; timeout unknown outcome reconciled; raw secrets never domain
- **Requirements:** ADM-024, ADM-025, ADM-026, PAR-017, PAR-018, PAR-019, PAR-020, PAY-001, PAY-002, PAY-003, PAY-004, PAY-005, PAY-006, PAY-007, PAY-008, PAY-009, PAY-011, PAY-012
- **Chunks:** ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| create_checkout(order:CheckoutOrder,key:IdempotencyKey)->CheckoutRef | create checkout | order:CheckoutOrder,key:IdempotencyKey | CheckoutRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| expire_checkout(reference:CheckoutRef,key:IdempotencyKey)->CheckoutState | expire checkout | reference:CheckoutRef,key:IdempotencyKey | CheckoutState | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| verify_webhook(raw:bytes,signature:string,now:Instant)->VerifiedWebhook | verify webhook | raw:bytes,signature:string,now:Instant | VerifiedWebhook | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| retrieve_payment(reference:ProviderPaymentRef)->VerifiedProviderPayment | retrieve payment | reference:ProviderPaymentRef | VerifiedProviderPayment | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| create_refund(request:RefundOrder,key:IdempotencyKey)->VerifiedRefund | create refund | request:RefundOrder,key:IdempotencyKey | VerifiedRefund | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| retrieve_refund(reference:ProviderRefundRef)->VerifiedRefund | retrieve refund | reference:ProviderRefundRef | VerifiedRefund | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| list_transactions(range:TimeRange,cursor:ProviderCursor?)->ProviderTransactionPage | Discover provider payments/refunds missing from local state; normalized items have provider ID,created_at,amount,currency,status,checkout/order references and next cursor | range:TimeRange,cursor:ProviderCursor? | ProviderTransactionPage | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## LiveClassProvider

- **Type:** integration port
- **Module:** delivery
- **Responsibility:** Waiting room true; join-before-host false; no recording; host start URL retrieved fresh, never stored
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** Zoom Server-to-Server OAuth adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Waiting room true; join-before-host false; no recording; host start URL retrieved fresh, never stored
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009, STU-014, TCH-004
- **Chunks:** ZE-P05-C03

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| create_meeting(request:MeetingSpec,key:IdempotencyKey)->MeetingRef | create meeting | request:MeetingSpec,key:IdempotencyKey | MeetingRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| update_meeting(reference:MeetingRef,spec:MeetingSpec,key:IdempotencyKey)->MeetingRef | update meeting | reference:MeetingRef,spec:MeetingSpec,key:IdempotencyKey | MeetingRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| cancel_meeting(reference:MeetingRef,key:IdempotencyKey)->None | cancel meeting | reference:MeetingRef,key:IdempotencyKey | None | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| get_host_handoff(reference:MeetingRef,host:AuthorizedHost)->ExpiringUrl | get host handoff | reference:MeetingRef,host:AuthorizedHost | ExpiringUrl | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| get_join_handoff(reference:MeetingRef,learner:AuthorizedLearner)->ExpiringUrl | get join handoff | reference:MeetingRef,learner:AuthorizedLearner | ExpiringUrl | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| retrieve_meeting(reference:MeetingRef)->MeetingState | retrieve meeting | reference:MeetingRef | MeetingState | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## CalendarProvider

- **Type:** integration port
- **Module:** delivery
- **Responsibility:** Dedicated business calendar; domain schedule authoritative; no child roster or meeting credentials; invalid token triggers full mirror reconcile
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** Google Calendar adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Dedicated business calendar; domain schedule authoritative; no child roster or meeting credentials; invalid token triggers full mirror reconcile
- **Requirements:** CAL-001, CAL-002, CAL-003, CAL-004, CAL-005
- **Chunks:** ZE-P05-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| upsert_event(reference:CalendarRef?,event:CalendarEventSpec,key:IdempotencyKey)->CalendarRef | upsert event | reference:CalendarRef?,event:CalendarEventSpec,key:IdempotencyKey | CalendarRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| cancel_event(reference:CalendarRef,key:IdempotencyKey)->None | cancel event | reference:CalendarRef,key:IdempotencyKey | None | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| list_changed(sync_token:SyncToken?)->CalendarDelta | list changed | sync_token:SyncToken? | CalendarDelta | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## EmailProvider

- **Type:** integration port
- **Module:** communication
- **Responsibility:** Approved template ID and recipient; only needed variables; retry unknown outcome under same local delivery key; local dedupe beyond24h
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** Resend adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Approved template ID and recipient; only needed variables; retry unknown outcome under same local delivery key; local dedupe beyond24h
- **Requirements:** ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-016, TCH-015
- **Chunks:** ZE-P08-C01

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| send(message:TransactionalEmail,key:IdempotencyKey)->MessageRef | send | message:TransactionalEmail,key:IdempotencyKey | MessageRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## ObjectStorageProvider

- **Type:** integration port
- **Module:** files
- **Responsibility:** Private buckets; unique staging+final keys; short-lived grants; no execution of child archives; metadata validated independently
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** S3-compatible adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Private buckets; unique staging+final keys; short-lived grants; no execution of child archives; metadata validated independently, Generated financial_document/export metadata and private storage references remain financial scope only; no teaching/public scope grants., Generated artifact spec contains purpose,media_type,size_bytes,sha256,content_disposition,metadata and creation intent ID. Only SystemGeneratedFileScope may write certificate/financial_document/financial_export. PDF<=10MiB; CSV<=100MiB; no browser-authorized generated writes. Verify HEAD/checksum after unknown outcome; cleanup uses recorded orphan intent and reference/retention checks, never bulk bucket deletion.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Chunks:** ZE-P04-C01, ZE-P04-C02, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P07-C06

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| presign_upload(spec:StagingUpload,ttl:Duration)->PresignedUpload | presign upload | spec:StagingUpload,ttl:Duration | PresignedUpload | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| head(key:ObjectKey)->ObjectMetadata | head | key:ObjectKey | ObjectMetadata | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| open_quarantined(key:ObjectKey,max_bytes:int)->BinaryStream | open quarantined | key:ObjectKey,max_bytes:int | BinaryStream | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| promote(source:StagingKey,target:ImmutableKey,checksum:Sha256)->StoredObject | promote | source:StagingKey,target:ImmutableKey,checksum:Sha256 | StoredObject | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| presign_download(key:ImmutableKey,ttl:Duration,filename:SafeFilename)->ExpiringUrl | presign download | key:ImmutableKey,ttl:Duration,filename:SafeFilename | ExpiringUrl | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| delete_versions(key:ObjectKey,decision:RetentionDecision)->DeleteResult | delete versions | key:ObjectKey,decision:RetentionDecision | DeleteResult | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| write_generated(source:BinaryStream,spec:GeneratedArtifactSpec,key:ImmutableObjectKey)->StoredObject | Trusted worker writes bounded PDF/CSV bytes to a unique immutable key; validates actual size and SHA256 against spec; conditional create forbids overwrite; same key+checksum retry reuses identical result; mismatch fails. Orphan intent is recorded before write and cleaned if final DB association never commits | source:BinaryStream,spec:GeneratedArtifactSpec,key:ImmutableObjectKey | StoredObject | ProviderUnavailable, IntegrityMismatch, ImmutableKeyConflict, ArtifactTooLarge, UnknownOutcome |

## MalwareScanner

- **Type:** integration port
- **Module:** files
- **Responsibility:** Fail closed on unavailable/stale scanner; archive expansion size<=100MiB, ratio<=20, entries<=100; nested archives forbidden; reject encrypted/path traversal archives
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** Sandboxed ClamAV scanner adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Fail closed on unavailable/stale scanner; archive expansion size<=100MiB, ratio<=20, entries<=100; nested archives forbidden; reject encrypted/path traversal archives
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Chunks:** ZE-P04-C01, ZE-P04-C02

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| scan(stream:BinaryStream,limits:ScanLimits)->ScanResult | scan | stream:BinaryStream,limits:ScanLimits | ScanResult | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## PasswordHasher

- **Type:** application port
- **Module:** identity
- **Responsibility:** Salt per credential; benchmark memory/time parameters; never log inputs; constant-time library verifier
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** Argon2id adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Salt per credential; benchmark memory/time parameters; never log inputs; constant-time library verifier
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| hash(password:SecretString)->PasswordHash | hash | password:SecretString | PasswordHash | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| verify(password:SecretString,hash:PasswordHash)->bool | verify | password:SecretString,hash:PasswordHash | bool | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| needs_rehash(hash:PasswordHash)->bool | needs rehash | hash:PasswordHash | bool | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## TokenIssuer

- **Type:** application port
- **Module:** identity
- **Responsibility:** At least256-bit entropy; hashed persistence; purpose-bound single-use tokens
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** CSPRNG/HMAC adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** At least256-bit entropy; hashed persistence; purpose-bound single-use tokens
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| issue(purpose:TokenPurpose,subject:uuid,ttl:Duration)->IssuedToken | issue | purpose:TokenPurpose,subject:uuid,ttl:Duration | IssuedToken | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| digest(token:SecretString)->TokenHash | digest | token:SecretString | TokenHash | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| verify_digest(token:SecretString,hash:TokenHash)->bool | verify digest | token:SecretString,hash:TokenHash | bool | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## CertificateRenderer

- **Type:** integration port
- **Module:** learning
- **Responsibility:** Static approved template, no network fetch or script execution; immutable learner/course/issue snapshots
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** Sandboxed PDF renderer adapter
- **Persistence:** External adapter; authoritative references in PostgreSQL
- **Invariants:** Static approved template, no network fetch or script execution; immutable learner/course/issue snapshots
- **Requirements:** ADM-020, LRN-009, LRN-010, PAR-014, STU-017
- **Chunks:** ZE-P07-C06

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| render(snapshot:CertificateSnapshot)->RenderedPdf | render | snapshot:CertificateSnapshot | RenderedPdf | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## Clock

- **Type:** application port
- **Module:** shared
- **Responsibility:** No server-local timezone assumptions; injectable deterministic time
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** UTC system clock; frozen test clock
- **Persistence:** none
- **Invariants:** No server-local timezone assumptions; injectable deterministic time
- **Requirements:** ADM-001, ADM-003, ADM-004, ADM-006, ADM-007, ADM-008, ADM-010, ADM-012, ADM-013, ADM-014, ADM-015, ADM-016, ADM-017, ADM-018, ADM-019, ADM-020, ADM-021, ADM-022, ADM-023, ADM-024, ADM-025, ADM-026, ADM-027, ADM-028, ADM-029, ASM-001, ASM-002, ASM-003, ASM-005, ASM-006, ASM-007, ASM-008, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-011, CAL-001, CAL-002, CAL-003, CAL-004, CAL-005, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-006, CLS-007, CLS-008, CLS-009, CLS-010, CLS-011, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-001, LRN-002, LRN-003, LRN-004, LRN-007, LRN-008, LRN-009, LRN-010, OPS-003, OPS-005, OPS-008, PAR-001, PAR-002, PAR-003, PAR-004, PAR-005, PAR-006, PAR-008, PAR-009, PAR-010, PAR-011, PAR-012, PAR-013, PAR-014, PAR-015, PAR-016, PAR-017, PAR-018, PAR-019, PAR-020, PAR-021, PAY-001, PAY-002, PAY-003, PAY-004, PAY-005, PAY-006, PAY-007, PAY-008, PAY-009, PAY-010, PAY-011, PAY-012, SEC-001, SEC-002, SEC-003, SEC-007, SEC-008, SEC-009, SEC-010, STU-001, STU-003, STU-004, STU-007, STU-009, STU-010, STU-011, STU-012, STU-013, STU-014, STU-015, STU-016, STU-017, STU-018, STU-019, TCH-001, TCH-003, TCH-004, TCH-005, TCH-006, TCH-007, TCH-008, TCH-009, TCH-011, TCH-012, TCH-013, TCH-014, TCH-015, WEB-011
- **Chunks:** ZE-P01-C02, ZE-P02-C01, ZE-P02-C02, ZE-P02-C03, ZE-P02-C04, ZE-P02-C05, ZE-P03-C02, ZE-P03-C03, ZE-P03-C04, ZE-P04-C01, ZE-P04-C02, ZE-P05-C01, ZE-P05-C02, ZE-P05-C03, ZE-P05-C04, ZE-P05-C05, ZE-P06-C01, ZE-P06-C02, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P07-C01, ZE-P07-C03, ZE-P07-C04, ZE-P07-C05, ZE-P07-C06, ZE-P08-C01, ZE-P08-C02, ZE-P08-C03, ZE-P08-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| now()->Instant | now |  | Instant | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| today(zone:IanaZone)->LocalDate | today | zone:IanaZone | LocalDate | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## UnitOfWork

- **Type:** application port
- **Module:** shared
- **Responsibility:** Atomic aggregate writes+audit+outbox; connection/session lifecycle outside domain; no network call inside lock-held transaction
- **Objects:** See Code Blueprint implementation ownership
- **Adapter:** SQLAlchemy transaction adapter
- **Persistence:** Transaction infrastructure
- **Invariants:** Atomic aggregate writes+audit+outbox; connection/session lifecycle outside domain; no network call inside lock-held transaction
- **Requirements:** ADM-001, ADM-003, ADM-004, ADM-005, ADM-006, ADM-007, ADM-008, ADM-010, ADM-011, ADM-012, ADM-013, ADM-014, ADM-015, ADM-016, ADM-017, ADM-018, ADM-019, ADM-020, ADM-021, ADM-022, ADM-023, ADM-024, ADM-025, ADM-026, ADM-027, ADM-028, ASM-001, ASM-002, ASM-003, ASM-004, ASM-005, ASM-006, ASM-007, ASM-008, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-010, AUTH-011, CAL-001, CAL-002, CAL-003, CAL-004, CAL-005, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-006, CLS-007, CLS-008, CLS-009, CLS-010, CLS-011, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-001, LRN-002, LRN-003, LRN-004, LRN-007, LRN-008, LRN-009, LRN-010, NFR-012, OPS-003, OPS-005, OPS-008, PAR-001, PAR-002, PAR-003, PAR-004, PAR-005, PAR-006, PAR-008, PAR-009, PAR-010, PAR-011, PAR-012, PAR-013, PAR-014, PAR-015, PAR-016, PAR-017, PAR-018, PAR-019, PAR-020, PAR-021, PAY-001, PAY-002, PAY-003, PAY-004, PAY-005, PAY-006, PAY-007, PAY-008, PAY-009, PAY-010, PAY-011, PAY-012, SEC-001, SEC-002, SEC-003, SEC-008, SEC-009, SEC-010, STU-001, STU-003, STU-004, STU-007, STU-008, STU-009, STU-010, STU-011, STU-012, STU-013, STU-014, STU-015, STU-016, STU-017, STU-018, STU-019, TCH-001, TCH-003, TCH-004, TCH-005, TCH-006, TCH-007, TCH-008, TCH-009, TCH-010, TCH-011, TCH-012, TCH-013, TCH-014, TCH-015, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-011, WEB-012
- **Chunks:** ZE-P01-C02, ZE-P02-C01, ZE-P02-C03, ZE-P02-C04, ZE-P02-C05, ZE-P03-C01, ZE-P03-C02, ZE-P03-C03, ZE-P03-C04, ZE-P04-C01, ZE-P04-C02, ZE-P05-C01, ZE-P05-C02, ZE-P05-C03, ZE-P05-C04, ZE-P05-C05, ZE-P06-C01, ZE-P06-C02, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P07-C01, ZE-P07-C02, ZE-P07-C03, ZE-P07-C04, ZE-P07-C05, ZE-P07-C06, ZE-P08-C01, ZE-P08-C02, ZE-P08-C03, ZE-P08-C04

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| begin()->Transaction | begin |  | Transaction | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| commit(events:tuple[DomainEvent],audit:tuple[AuditRecord])->CommitResult | commit | events:tuple[DomainEvent],audit:tuple[AuditRecord] | CommitResult | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| rollback()->None | rollback |  | None | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## MfaRepository

- **Type:** repository interface
- **Module:** identity
- **Responsibility:** Lock and persist encrypted-factor references, hashed recovery codes, challenge/setup state and replay counter.
- **Objects:** MfaFactor, RecoveryCode, MfaChallenge
- **Adapter:** SQLAlchemy data-mapper; PostgreSQL; encrypted secret column handled by secret adapter
- **Persistence:** mfa_factors,mfa_recovery_codes,mfa_challenges
- **Invariants:** Challenge consume, recovery code consume, timestep update and full-session issuance commit atomically., ADR 0004: acquire the shared Account row lock before factor/challenge locks even when no factor exists; revalidate trusted authorization and current lifecycle inside the transaction before idempotency outcome or mutation. Status/role writes retain membership-lock-before-Account order; MFA paths do not acquire the membership lock.
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, SEC-004
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| get_factor_for_update(account_id:uuid,scope:SelfAuthScope)->MfaFactor? | Lock and return only the active factor for the scoped account; never choose a pending or latest factor | account_id:uuid,scope:SelfAuthScope | MfaFactor? | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| get_pending_factor_for_update(account_id:uuid,setup_token_hash:bytes,browser_hash:bytes,scope:SelfAuthScope)->MfaFactor? | Under the shared Account lock, validate the exact hashed setup challenge against scoped account/browser, setup purpose, expiry, attempts and nonconsumption; follow its factor_id to lock that pending factor. Never select latest-by-account or an active factor. | account_id:uuid,setup_token_hash:bytes,browser_hash:bytes,scope:SelfAuthScope | MfaFactor? | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| invalidate_pending_setup(account_id:uuid,scope:SelfAuthScope)->int | Under the shared Account lock, revoke all pending factors and consume every dependent pending setup credential for the scoped account; return count of invalidated pending factors. Preserve active factors and recovery codes. | account_id:uuid,scope:SelfAuthScope | int | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| get_challenge_for_update(token_hash:bytes,browser_hash:bytes)->MfaChallenge? | get challenge for update | token_hash:bytes,browser_hash:bytes | MfaChallenge? | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| find_recovery_for_update(factor_id:uuid,code_hash:bytes)->RecoveryCode? | find recovery for update | factor_id:uuid,code_hash:bytes | RecoveryCode? | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| save_factor(factor:MfaFactor,expected_version:int)->None | save factor | factor:MfaFactor,expected_version:int | None | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| save_challenge(challenge:MfaChallenge)->None | save challenge | challenge:MfaChallenge | None | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| consume_recovery(code:RecoveryCode)->None | consume recovery | code:RecoveryCode | None | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| save_recovery_codes(factor_id:uuid,codes:HashedRecoveryCodeSet,scope:SelfAuthScope)->None | Persist complete newly issued hashed recovery code set under factor lock; plaintext codes never persist | factor_id:uuid,codes:HashedRecoveryCodeSet,scope:SelfAuthScope | None | RepositoryConflict, PersistenceUnavailable |
| revoke_recovery_codes(factor_id:uuid,scope:SelfAuthScope)->int | Invalidate previous set atomically when factor rotates | factor_id:uuid,scope:SelfAuthScope | int | RepositoryConflict, PersistenceUnavailable |

## MfaVerifier

- **Type:** integration port
- **Module:** identity
- **Responsibility:** Generate/encrypt TOTP seed, verify RFC6238 proof and hash high-entropy recovery codes without exposing seed to domain.
- **Objects:** MfaFactor
- **Adapter:** Audited TOTP library plus managed key-encryption adapter
- **Persistence:** Managed encryption key outside database; ciphertext/reference persisted in mfa_factors
- **Invariants:** TOTP30-second step,6 digits,SHA1 for authenticator compatibility, +/-1-step clock tolerance; server enforces returned accepted step>last step. Secret seed>=160 bits; recoverycodes>=128-bit entropy.
- **Requirements:** AUTH-002, SEC-004
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| generate_setup(account_label:string)->EncryptedMfaSetup | generate setup | account_label:string | EncryptedMfaSetup | InvalidMfaProof, SecretUnavailable |
| verify_totp(secret_reference:EncryptedSecretRef,code:string,now:Instant)->VerifiedTotpProof | verify totp | secret_reference:EncryptedSecretRef,code:string,now:Instant | VerifiedTotpProof | InvalidMfaProof, SecretUnavailable |
| issue_recovery_codes(count:int)->RecoveryCodeSet | issue recovery codes | count:int | RecoveryCodeSet | InvalidMfaProof, SecretUnavailable |
| hash_recovery_code(code:SecretString)->bytes | hash recovery code | code:SecretString | bytes | InvalidMfaProof, SecretUnavailable |

## DocumentRenderer

- **Type:** integration port
- **Module:** billing
- **Responsibility:** Render approved immutable invoice/receipt PDF from purchase snapshot without external network or executable content.
- **Objects:** Receipt
- **Adapter:** Sandboxed PDF renderer adapter with static approved merchant/tax template
- **Persistence:** Returned PDF becomes generated financial_document FileAsset in private object storage
- **Invariants:** Only approved immutable ReceiptSnapshot input; deterministic document serial/content hash; no external resources, scripts or child work.
- **Requirements:** PAY-007, PAY-012, PAR-018
- **Chunks:** ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Interface signature | Purpose | Inputs | Output | Failures |
|---|---|---|---|---|
| render_purchase_document(snapshot:ReceiptSnapshot)->RenderedPdf | Generate immutable legal purchase artifact | ReceiptSnapshot: document ID/type/number/issued_at,merchant legal name/ABN/address,purchaser name,description,AUD amount/tax | RenderedPdf: bytes,media_type application/pdf,sha256,size_bytes<=10MiB | RenderFailed, InvalidReceiptSnapshot |
