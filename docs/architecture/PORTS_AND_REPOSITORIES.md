# Ports and repositories

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

Repositories follow aggregate boundaries, not one repository per table. Query projections may join modules through explicit ports; they must not expose an unrestricted `get(id)` to user-driven services. Scope types are immutable evidence resolved by the authorization context, carrying principal, role, family or student identity, assignment and purpose. They are not accepted from JSON. Unscoped worker methods exist only where named and require internal capability identity. Repositories never silently remove ownership filters to accommodate an admin caller; an explicit restricted admin scope is required.

## UserRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / identity |
| Responsibility | Aggregate persistence and purpose-scoped projection of Account,Credential,RoleGrant,TeacherProfile |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | accounts,credentials,teacher_profiles |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | AuthenticationService, AccountService, StudentProfileService, TeacherService, PublicContentService, CohortService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-001, ADM-005, ADM-006, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-006, WEB-011 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| find_login(identifier:NormalizedIdentifier)->AccountCredentials? | identifier:NormalizedIdentifier | AccountCredentials? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_scoped(id:uuid,scope:IdentityScope)->Account? | id:uuid,scope:IdentityScope | Account? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_staff(scope:IdentityScope,filter:StaffFilter,page:Page)->Page[TeacherProfile] | scope:IdentityScope,filter:StaffFilter,page:Page | Page[TeacherProfile] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(account:Account,expected_version:int)->None | account:Account,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## SessionRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / identity |
| Responsibility | Aggregate persistence and purpose-scoped projection of Session |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | sessions,one_time_tokens |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | AuthenticationService, AccountService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| find_active(token_hash:TokenHash,now:Instant)->Session? | token_hash:TokenHash,now:Instant | Session? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_owned(user_id:uuid,scope:SelfScope)->tuple[Session] | user_id:uuid,scope:SelfScope | tuple[Session] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| revoke_all(user_id:uuid)->int | user_id:uuid | int | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(session:Session)->None | session:Session | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| consume_token(hash:TokenHash,purpose:TokenPurpose,now:Instant)->TokenSubject | hash:TokenHash,purpose:TokenPurpose,now:Instant | TokenSubject | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## FamilyRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / family |
| Responsibility | Aggregate persistence and purpose-scoped projection of Family,Guardian,GuardianStudent,BillingMembership,PolicyAcknowledgement |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | families,guardians,guardian_students,billing_memberships,policy_acknowledgements |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | AuthenticationService, AccountService, FamilyService, StudentProfileService, ConsentService, EnrolmentService, BillingService, FileService, PrivacyService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-011, AUTH-012, PAR-002, PAR-004, PAR-006, PAR-021, SEC-003, STU-019, TCH-016 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(id:uuid,scope:FamilyScope)->Family? | id:uuid,scope:FamilyScope | Family? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| resolve_guardian_scope(principal:Principal,student_id:uuid)->FamilyScope? | principal:Principal,student_id:uuid | FamilyScope? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| resolve_billing_scope(principal:Principal,family_id:uuid)->BillingScope? | principal:Principal,family_id:uuid | BillingScope? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(family:Family,expected_version:int)->None | family:Family,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_acknowledgements(scope:FamilyScope,page:Page)->Page[PolicyAcknowledgement] | scope:FamilyScope,page:Page | Page[PolicyAcknowledgement] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## StudentRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / family |
| Responsibility | Aggregate persistence and purpose-scoped projection of StudentProfile |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | students |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | FamilyService, StudentProfileService, EnrolmentService, PrivacyService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-004, PAR-005, TCH-009 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(id:uuid,scope:StudentReadScope)->StudentProfile? | id:uuid,scope:StudentReadScope | StudentProfile? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_linked(scope:FamilyScope,page:Page)->Page[StudentProfile] | scope:FamilyScope,page:Page | Page[StudentProfile] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_teaching(scope:TeachingScope,page:Page)->Page[TeachingStudentProjection] | scope:TeachingScope,page:Page | Page[TeachingStudentProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(student:StudentProfile,expected_version:int)->None | student:StudentProfile,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## ContentRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / content |
| Responsibility | Aggregate persistence and purpose-scoped projection of PublicPage,PolicyDocument,ContactEnquiry |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | public_pages,public_page_revisions,policy_documents,contact_enquiries |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | ConsentService, PublicContentService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | WEB-001, WEB-002, WEB-007, WEB-008, WEB-009, WEB-010, WEB-012 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_published_page(slug:PublicPageSlug)->PublicPage? | slug:PublicPageSlug | PublicPage? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_policies(scope:PublicationScope,page:Page)->Page[PolicyDocument] | scope:PublicationScope,page:Page | Page[PolicyDocument] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_draft(id:uuid,scope:OperationsScope)->ContentAggregate? | id:uuid,scope:OperationsScope | ContentAggregate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(content:ContentAggregate,expected_version:int)->None | content:ContentAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_enquiries(scope:OperationsScope,page:Page)->Page[ContactEnquiry] | scope:OperationsScope,page:Page | Page[ContactEnquiry] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## CourseRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / curriculum |
| Responsibility | Aggregate persistence and purpose-scoped projection of Program,Course,CurriculumRevision,CourseModule,Lesson,LessonBlock,LearningResource |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | programs,courses,curriculum_revisions,course_modules,lessons,lesson_blocks,learning_resources |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | PublicContentService, CourseService, CurriculumService, CohortService, QuizService, AssignmentService, ProgressService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-007, ADM-008, ADM-009, LRN-001, LRN-002, LRN-003, LRN-004, LRN-005, PAR-007, STU-003, STU-004, STU-005, TCH-003, WEB-003, WEB-004 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_course(id:uuid,scope:CourseScope)->Course? | id:uuid,scope:CourseScope | Course? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_revision(id:uuid,scope:CurriculumScope)->CurriculumRevision? | id:uuid,scope:CurriculumScope | CurriculumRevision? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_courses(scope:CourseScope,filter:CourseFilter,page:Page)->Page[Course] | scope:CourseScope,filter:CourseFilter,page:Page | Page[Course] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_revision(revision:CurriculumRevision,expected_version:int)->None | revision:CurriculumRevision,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_course(course:Course,expected_version:int)->None | course:Course,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_program(program:Program,expected_version:int)->None | program:Program,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## DeliveryRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / delivery |
| Responsibility | Aggregate persistence and purpose-scoped projection of Cohort,ClassSession,TeacherAssignment |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | cohorts,class_sessions,teacher_assignments |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | TeacherService, CurriculumService, CohortService, SchedulingService, LiveClassService, EnrolmentService, AttendanceService, AssignmentService, SubmissionService, AssessmentService, FeedbackService, BillingService, CommunicationService, FileService, CalendarService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-013, ADM-014, ADM-015, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-011, PAR-009, STU-013, TCH-005, TCH-006, WEB-005 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_cohort(id:uuid,scope:DeliveryScope,for_update:bool)->Cohort? | id:uuid,scope:DeliveryScope,for_update:bool | Cohort? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_session(id:uuid,scope:DeliveryScope)->ClassSession? | id:uuid,scope:DeliveryScope | ClassSession? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| resolve_teaching_scope(principal:Principal,cohort_id:uuid,session_id:uuid?)->TeachingScope? | principal:Principal,cohort_id:uuid,session_id:uuid? | TeachingScope? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_schedule(scope:ScheduleScope,range:TimeRange,page:Page)->Page[ClassSession] | scope:ScheduleScope,range:TimeRange,page:Page | Page[ClassSession] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| find_conflicts(slot:TimeSlot,participants:ParticipantIds,exclude_session_id:uuid?)->ScheduleConflicts | slot:TimeSlot,participants:ParticipantIds,exclude_session_id:uuid? | ScheduleConflicts | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(aggregate:DeliveryAggregate,expected_version:int)->None | aggregate:DeliveryAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## EnrolmentRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / enrolment |
| Responsibility | Aggregate persistence and purpose-scoped projection of Enrolment |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | enrolments |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | CurriculumService, SchedulingService, LiveClassService, EnrolmentService, AttendanceService, QuizService, AssignmentService, SubmissionService, AssessmentService, FeedbackService, ProgressService, CertificateService, BillingService, RefundService, FileService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(id:uuid,scope:EnrolmentScope,for_update:bool)->Enrolment? | id:uuid,scope:EnrolmentScope,for_update:bool | Enrolment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:EnrolmentScope,filter:EnrolmentFilter,page:Page)->Page[Enrolment] | scope:EnrolmentScope,filter:EnrolmentFilter,page:Page | Page[Enrolment] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| count_committed(cohort_id:uuid,now:Instant)->SeatCounts | cohort_id:uuid,now:Instant | SeatCounts | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_child_cohort(student_id:uuid,cohort_id:uuid,scope:EnrolmentScope)->Enrolment? | student_id:uuid,cohort_id:uuid,scope:EnrolmentScope | Enrolment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| lock_expired_holds(cutoff:Instant,batch_size:int)->tuple[Enrolment] | cutoff:Instant,batch_size:int | tuple[Enrolment] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(enrolment:Enrolment,expected_version:int)->None | enrolment:Enrolment,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## AttendanceRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / delivery |
| Responsibility | Aggregate persistence and purpose-scoped projection of AttendanceRecord |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | attendance_records |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | AttendanceService, ProgressService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-017, CLS-010, PAR-010, STU-015, TCH-007, TCH-008 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| list_scoped(scope:AttendanceScope,filter:AttendanceFilter,page:Page)->Page[AttendanceRecord] | scope:AttendanceScope,filter:AttendanceFilter,page:Page | Page[AttendanceRecord] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_for_update(session_id:uuid,student_id:uuid,scope:TeachingScope)->AttendanceRecord? | session_id:uuid,student_id:uuid,scope:TeachingScope | AttendanceRecord? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| summarize(enrolment_id:uuid,scope:ProgressScope)->AttendanceCounts | enrolment_id:uuid,scope:ProgressScope | AttendanceCounts | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(record:AttendanceRecord,expected_version:int)->None | record:AttendanceRecord,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## AssessmentRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / assessment |
| Responsibility | Aggregate persistence and purpose-scoped projection of Quiz,QuizQuestion,QuizAttempt,Assignment,Submission,Assessment,TeacherFeedback |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | quizzes,quiz_questions,quiz_options,quiz_attempts,quiz_answers,assignments,assignment_delivery_rules,submissions,submission_assets,assessments,assessment_revisions,teacher_feedback,feedback_revisions |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | CurriculumService, QuizService, AssignmentService, SubmissionService, AssessmentService, FeedbackService, ProgressService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-010, ADM-011, ADM-012, ADM-019, ASM-001, ASM-002, ASM-003, ASM-004, ASM-005, ASM-006, ASM-007, ASM-008, PAR-012, PAR-013, STU-007, STU-008, STU-009, STU-010, STU-011, STU-012, TCH-010, TCH-011, TCH-012, TCH-013 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_definition(id:uuid,scope:CurriculumScope)->AssessmentDefinition? | id:uuid,scope:CurriculumScope | AssessmentDefinition? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_definitions(scope:CurriculumScope,filter:DefinitionFilter,page:Page)->Page[AssessmentDefinition] | scope:CurriculumScope,filter:DefinitionFilter,page:Page | Page[AssessmentDefinition] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_work(id:uuid,scope:WorkScope,for_update:bool)->AssessmentAggregate? | id:uuid,scope:WorkScope,for_update:bool | AssessmentAggregate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_work(scope:WorkScope,filter:WorkFilter,page:Page)->Page[WorkProjection] | scope:WorkScope,filter:WorkFilter,page:Page | Page[WorkProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| count_attempts(quiz_id:uuid,enrolment_id:uuid,locked:bool)->AttemptCount | quiz_id:uuid,enrolment_id:uuid,locked:bool | AttemptCount | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_definition(definition:AssessmentDefinition,revision_version:int)->None | definition:AssessmentDefinition,revision_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_work(work:AssessmentAggregate,expected_version:int)->None | work:AssessmentAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## ProgressRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / learning |
| Responsibility | Aggregate persistence and purpose-scoped projection of StudentProgress,ActivityCompletion |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | student_progress,activity_completions |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | ProgressService, CertificateService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-018, LRN-006, LRN-007, LRN-008, PAR-011, STU-006, STU-016, TCH-014 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(enrolment_id:uuid,scope:ProgressScope)->StudentProgress? | enrolment_id:uuid,scope:ProgressScope | StudentProgress? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:ProgressScope,page:Page)->Page[StudentProgress] | scope:ProgressScope,page:Page | Page[StudentProgress] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_activities(enrolment_id:uuid,scope:StudentScope)->tuple[ActivityCompletion] | enrolment_id:uuid,scope:StudentScope | tuple[ActivityCompletion] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_activity(record:ActivityCompletion,expected_version:int)->None | record:ActivityCompletion,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_progress(progress:StudentProgress,expected_version:int)->None | progress:StudentProgress,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## CertificateRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / learning |
| Responsibility | Aggregate persistence and purpose-scoped projection of Certificate |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | certificates |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | CertificateService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-020, LRN-009, LRN-010, PAR-014, STU-017 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(id:uuid,scope:CertificateScope)->Certificate? | id:uuid,scope:CertificateScope | Certificate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:CertificateScope,filter:CertificateFilter,page:Page)->Page[Certificate] | scope:CertificateScope,filter:CertificateFilter,page:Page | Page[Certificate] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_current_for_update(enrolment_id:uuid)->Certificate? | enrolment_id:uuid | Certificate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(certificate:Certificate,expected_version:int)->None | certificate:Certificate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## PaymentRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / billing |
| Responsibility | Aggregate persistence and purpose-scoped projection of Price,Payment,Refund,Receipt |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | prices,payments,payment_events,refunds,purchase_documents |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | BillingService, RefundService, ReportingService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-024, ADM-025, ADM-026, PAR-017, PAR-018, PAR-019, PAR-020, PAY-001, PAY-002, PAY-003, PAY-006, PAY-007, PAY-008, PAY-009, PAY-011, PAY-012 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| resolve_price(course_id:uuid,cohort_id:uuid,at:Instant)->PriceSnapshot | course_id:uuid,cohort_id:uuid,at:Instant | PriceSnapshot | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_payment(id:uuid,scope:BillingScope,for_update:bool)->Payment? | id:uuid,scope:BillingScope,for_update:bool | Payment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_payments(scope:BillingScope,filter:PaymentFilter,page:Page)->Page[Payment] | scope:BillingScope,filter:PaymentFilter,page:Page | Page[Payment] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| find_by_provider(reference:ProviderPaymentRef,scope:SystemBillingScope)->Payment? | reference:ProviderPaymentRef,scope:SystemBillingScope | Payment? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| lock_refundable_balance(payment_id:uuid)->RefundBalance | payment_id:uuid | RefundBalance | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_refunds(payment_id:uuid,scope:BillingScope)->tuple[Refund] | payment_id:uuid,scope:BillingScope | tuple[Refund] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| report(scope:FinanceScope,range:DateRange)->FinanceReport | scope:FinanceScope,range:DateRange | FinanceReport | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(aggregate:BillingAggregate,expected_version:int)->None | aggregate:BillingAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## CommunicationRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / communication |
| Responsibility | Aggregate persistence and purpose-scoped projection of Event,Announcement |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | events,announcements |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | CommunicationService, CalendarService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-021, COM-008, PAR-015, STU-018 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(id:uuid,scope:AudienceScope)->CommunicationAggregate? | id:uuid,scope:AudienceScope | CommunicationAggregate? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:AudienceScope,filter:CommunicationFilter,page:Page)->Page[CommunicationProjection] | scope:AudienceScope,filter:CommunicationFilter,page:Page | Page[CommunicationProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(aggregate:CommunicationAggregate,expected_version:int)->None | aggregate:CommunicationAggregate,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## NotificationRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / communication |
| Responsibility | Aggregate persistence and purpose-scoped projection of Notification,NotificationDelivery |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | notifications,notification_deliveries |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | AuthenticationService, PublicContentService, NotificationService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-021, ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-003, PAR-015, PAR-016, STU-018, TCH-015 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| list_owned(scope:SelfScope,filter:NotificationFilter,page:Page)->Page[Notification] | scope:SelfScope,filter:NotificationFilter,page:Page | Page[Notification] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_owned(id:uuid,scope:SelfScope)->Notification? | id:uuid,scope:SelfScope | Notification? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| insert_deduplicated(notification:Notification)->InsertOutcome | notification:Notification | InsertOutcome | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| claim_delivery(id:uuid,scope:SystemNotificationScope,lease:Lease)->NotificationDelivery? | id:uuid,scope:SystemNotificationScope,lease:Lease | NotificationDelivery? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save_delivery(delivery:NotificationDelivery,expected_version:int)->None | delivery:NotificationDelivery,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_deliveries(scope:OperationsScope,filter:DeliveryFilter,page:Page)->Page[DeliveryProjection] | scope:OperationsScope,filter:DeliveryFilter,page:Page | Page[DeliveryProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## FileRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / files |
| Responsibility | Aggregate persistence and purpose-scoped projection of FileAsset |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | file_assets,asset_links |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | CurriculumService, SubmissionService, CertificateService, BillingService, ReportingService, FileService, PrivacyService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(id:uuid,scope:FileScope)->FileAsset? | id:uuid,scope:FileScope | FileAsset? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_scan_target(id:uuid,scope:SystemFileScope,for_update:bool)->FileAsset? | id:uuid,scope:SystemFileScope,for_update:bool | FileAsset? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:FileScope,filter:FileFilter,page:Page)->Page[FileAsset] | scope:FileScope,filter:FileFilter,page:Page | Page[FileAsset] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| reference_count(id:uuid)->int | id:uuid | int | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| lock_orphans(cutoff:Instant,batch_size:int)->tuple[FileAsset] | cutoff:Instant,batch_size:int | tuple[FileAsset] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(asset:FileAsset,expected_version:int)->None | asset:FileAsset,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## IntegrationRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / operations |
| Responsibility | Aggregate persistence and purpose-scoped projection of IntegrationBinding,WebhookInbox,OutboxEvent,BackgroundJob |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | integration_bindings,webhook_inbox,outbox_events,background_jobs,idempotency_records |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | LiveClassService, BillingService, CalendarService, OperationsService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | OPS-003, OPS-005, PAY-004, PAY-005 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| insert_inbox_unique(event:VerifiedWebhook)->InboxInsertOutcome | event:VerifiedWebhook | InboxInsertOutcome | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| get_binding(resource:MirrorResource,provider:Provider)->IntegrationBinding? | resource:MirrorResource,provider:Provider | IntegrationBinding? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| claim_outbox(batch_size:int,lease:Lease)->tuple[OutboxEvent] | batch_size:int,lease:Lease | tuple[OutboxEvent] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| claim_job(id:uuid,scope:JobScope,lease:Lease)->BackgroundJob? | id:uuid,scope:JobScope,lease:Lease | BackgroundJob? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_jobs(scope:JobScope,filter:JobFilter,page:Page)->Page[JobProjection] | scope:JobScope,filter:JobFilter,page:Page | Page[JobProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(record:IntegrationRecord,expected_version:int)->None | record:IntegrationRecord,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| reserve_idempotency(key:IdempotencyScope,body_hash:string)->IdempotencyResult | key:IdempotencyScope,body_hash:string | IdempotencyResult | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## SettingsRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / operations |
| Responsibility | Aggregate persistence and purpose-scoped projection of ApplicationSetting |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | application_settings |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | BillingService, OperationsService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-028 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_typed(key:SettingKey,scope:SettingsScope)->ApplicationSetting? | key:SettingKey,scope:SettingsScope | ApplicationSetting? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_allowed(scope:SettingsScope)->tuple[ApplicationSetting] | scope:SettingsScope | tuple[ApplicationSetting] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(setting:ApplicationSetting,expected_version:int)->None | setting:ApplicationSetting,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| launch_readiness()->LaunchReadiness |  | LaunchReadiness | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## AuditRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / operations |
| Responsibility | Aggregate persistence and purpose-scoped projection of AuditRecord |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | audit_records |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | AuditService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-029, SEC-007 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| append(record:AuditRecord)->None | record:AuditRecord | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_redacted(scope:AuditScope,filter:AuditFilter,page:Page)->Page[AuditProjection] | scope:AuditScope,filter:AuditFilter,page:Page | Page[AuditProjection] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## PrivacyRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / family |
| Responsibility | Aggregate persistence and purpose-scoped projection of PrivacyRequest |
| Adapter | SQLAlchemy data-mapper adapter; PostgreSQL |
| Data ownership | privacy_requests,retention_holds,privacy_exports,retention_decisions |
| Invariants | Every user read requires typed scope resolved from principal relationships; never optional unrestricted filter., Writes participate in UnitOfWork; domain objects have no ORM imports. |
| Consumers | PrivacyService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_scoped(id:uuid,scope:PrivacyScope,for_update:bool)->PrivacyRequest? | id:uuid,scope:PrivacyScope,for_update:bool | PrivacyRequest? | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| list_scoped(scope:PrivacyScope,filter:PrivacyFilter,page:Page)->Page[PrivacyRequest] | scope:PrivacyScope,filter:PrivacyFilter,page:Page | Page[PrivacyRequest] | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| has_hold(resource:RetentionResource)->bool | resource:RetentionResource | bool | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| save(request:PrivacyRequest,expected_version:int)->None | request:PrivacyRequest,expected_version:int | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |
| record_retention_decision(decision:RetentionDecision)->None | decision:RetentionDecision | None | RepositoryConflict, NotFoundWithinScope, PersistenceUnavailable |

## PaymentGateway

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / billing |
| Responsibility | Signature verification requires original bytes; authoritative server state; timeout unknown outcome reconciled; raw secrets never domain |
| Adapter | Stripe adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Signature verification requires original bytes; authoritative server state; timeout unknown outcome reconciled; raw secrets never domain |
| Consumers | BillingService, RefundService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-024, ADM-025, ADM-026, PAR-017, PAR-018, PAR-019, PAR-020, PAY-001, PAY-002, PAY-003, PAY-004, PAY-005, PAY-006, PAY-007, PAY-008, PAY-009, PAY-011, PAY-012 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| create_checkout(order:CheckoutOrder,key:IdempotencyKey)->CheckoutRef | order:CheckoutOrder,key:IdempotencyKey | CheckoutRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| expire_checkout(reference:CheckoutRef,key:IdempotencyKey)->CheckoutState | reference:CheckoutRef,key:IdempotencyKey | CheckoutState | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| verify_webhook(raw:bytes,signature:string,now:Instant)->VerifiedWebhook | raw:bytes,signature:string,now:Instant | VerifiedWebhook | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| retrieve_payment(reference:ProviderPaymentRef)->VerifiedProviderPayment | reference:ProviderPaymentRef | VerifiedProviderPayment | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| create_refund(request:RefundOrder,key:IdempotencyKey)->VerifiedRefund | request:RefundOrder,key:IdempotencyKey | VerifiedRefund | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| retrieve_refund(reference:ProviderRefundRef)->VerifiedRefund | reference:ProviderRefundRef | VerifiedRefund | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## LiveClassProvider

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / delivery |
| Responsibility | Waiting room true; join-before-host false; no recording; host start URL retrieved fresh, never stored |
| Adapter | Zoom Server-to-Server OAuth adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Waiting room true; join-before-host false; no recording; host start URL retrieved fresh, never stored |
| Consumers | LiveClassService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | CLS-006, CLS-007, CLS-008, CLS-009, STU-014, TCH-004 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| create_meeting(request:MeetingSpec,key:IdempotencyKey)->MeetingRef | request:MeetingSpec,key:IdempotencyKey | MeetingRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| update_meeting(reference:MeetingRef,spec:MeetingSpec,key:IdempotencyKey)->MeetingRef | reference:MeetingRef,spec:MeetingSpec,key:IdempotencyKey | MeetingRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| cancel_meeting(reference:MeetingRef,key:IdempotencyKey)->None | reference:MeetingRef,key:IdempotencyKey | None | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| get_host_handoff(reference:MeetingRef,host:AuthorizedHost)->ExpiringUrl | reference:MeetingRef,host:AuthorizedHost | ExpiringUrl | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| get_join_handoff(reference:MeetingRef,learner:AuthorizedLearner)->ExpiringUrl | reference:MeetingRef,learner:AuthorizedLearner | ExpiringUrl | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| retrieve_meeting(reference:MeetingRef)->MeetingState | reference:MeetingRef | MeetingState | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## CalendarProvider

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / delivery |
| Responsibility | Dedicated business calendar; domain schedule authoritative; no child roster or meeting credentials; invalid token triggers full mirror reconcile |
| Adapter | Google Calendar adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Dedicated business calendar; domain schedule authoritative; no child roster or meeting credentials; invalid token triggers full mirror reconcile |
| Consumers | CalendarService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | CAL-001, CAL-002, CAL-003, CAL-004, CAL-005 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| upsert_event(reference:CalendarRef?,event:CalendarEventSpec,key:IdempotencyKey)->CalendarRef | reference:CalendarRef?,event:CalendarEventSpec,key:IdempotencyKey | CalendarRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| cancel_event(reference:CalendarRef,key:IdempotencyKey)->None | reference:CalendarRef,key:IdempotencyKey | None | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| list_changed(sync_token:SyncToken?)->CalendarDelta | sync_token:SyncToken? | CalendarDelta | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## EmailProvider

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / communication |
| Responsibility | Approved template ID and recipient; only needed variables; retry unknown outcome under same local delivery key; local dedupe beyond24h |
| Adapter | Resend adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Approved template ID and recipient; only needed variables; retry unknown outcome under same local delivery key; local dedupe beyond24h |
| Consumers | NotificationService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-016, TCH-015 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| send(message:TransactionalEmail,key:IdempotencyKey)->MessageRef | message:TransactionalEmail,key:IdempotencyKey | MessageRef | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## ObjectStorageProvider

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / files |
| Responsibility | Private buckets; unique staging+final keys; short-lived grants; no execution of child archives; metadata validated independently |
| Adapter | S3-compatible adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Private buckets; unique staging+final keys; short-lived grants; no execution of child archives; metadata validated independently |
| Consumers | CertificateService, BillingService, ReportingService, FileService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| presign_upload(spec:StagingUpload,ttl:Duration)->PresignedUpload | spec:StagingUpload,ttl:Duration | PresignedUpload | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| head(key:ObjectKey)->ObjectMetadata | key:ObjectKey | ObjectMetadata | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| open_quarantined(key:ObjectKey,max_bytes:int)->BinaryStream | key:ObjectKey,max_bytes:int | BinaryStream | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| promote(source:StagingKey,target:ImmutableKey,checksum:Sha256)->StoredObject | source:StagingKey,target:ImmutableKey,checksum:Sha256 | StoredObject | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| presign_download(key:ImmutableKey,ttl:Duration,filename:SafeFilename)->ExpiringUrl | key:ImmutableKey,ttl:Duration,filename:SafeFilename | ExpiringUrl | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| delete_versions(key:ObjectKey,decision:RetentionDecision)->DeleteResult | key:ObjectKey,decision:RetentionDecision | DeleteResult | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## MalwareScanner

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / files |
| Responsibility | Fail closed on unavailable/stale scanner; archive expansion size<=250MiB, ratio<=20, entries<=1000, nesting<=2; reject encrypted/path traversal archives |
| Adapter | Sandboxed ClamAV scanner adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Fail closed on unavailable/stale scanner; archive expansion size<=250MiB, ratio<=20, entries<=1000, nesting<=2; reject encrypted/path traversal archives |
| Consumers | FileService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| scan(stream:BinaryStream,limits:ScanLimits)->ScanResult | stream:BinaryStream,limits:ScanLimits | ScanResult | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## PasswordHasher

| Metadata | Contract |
| --- | --- |
| Kind/module | application port / identity |
| Responsibility | Salt per credential; benchmark memory/time parameters; never log inputs; constant-time library verifier |
| Adapter | Argon2id adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Salt per credential; benchmark memory/time parameters; never log inputs; constant-time library verifier |
| Consumers | AuthenticationService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| hash(password:SecretString)->PasswordHash | password:SecretString | PasswordHash | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| verify(password:SecretString,hash:PasswordHash)->bool | password:SecretString,hash:PasswordHash | bool | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| needs_rehash(hash:PasswordHash)->bool | hash:PasswordHash | bool | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## TokenIssuer

| Metadata | Contract |
| --- | --- |
| Kind/module | application port / identity |
| Responsibility | At least256-bit entropy; hashed persistence; purpose-bound single-use tokens |
| Adapter | CSPRNG/HMAC adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | At least256-bit entropy; hashed persistence; purpose-bound single-use tokens |
| Consumers | AuthenticationService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| issue(purpose:TokenPurpose,subject:uuid,ttl:Duration)->IssuedToken | purpose:TokenPurpose,subject:uuid,ttl:Duration | IssuedToken | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| digest(token:SecretString)->TokenHash | token:SecretString | TokenHash | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| verify_digest(token:SecretString,hash:TokenHash)->bool | token:SecretString,hash:TokenHash | bool | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## CertificateRenderer

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / learning |
| Responsibility | Static approved template, no network fetch or script execution; immutable learner/course/issue snapshots |
| Adapter | Sandboxed PDF renderer adapter |
| Data ownership | External adapter; authoritative references in PostgreSQL |
| Invariants | Static approved template, no network fetch or script execution; immutable learner/course/issue snapshots |
| Consumers | CertificateService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-020, LRN-009, LRN-010, PAR-014, STU-017 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| render(snapshot:CertificateSnapshot)->RenderedPdf | snapshot:CertificateSnapshot | RenderedPdf | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## Clock

| Metadata | Contract |
| --- | --- |
| Kind/module | application port / shared |
| Responsibility | No server-local timezone assumptions; injectable deterministic time |
| Adapter | UTC system clock; frozen test clock |
| Data ownership | none |
| Invariants | No server-local timezone assumptions; injectable deterministic time |
| Consumers | AuthenticationService, AccountService, FamilyService, StudentProfileService, ConsentService, CourseService, CurriculumService, CohortService, SchedulingService, LiveClassService, EnrolmentService, AttendanceService, QuizService, SubmissionService, AssessmentService, FeedbackService, ProgressService, CertificateService, BillingService, RefundService, ReportingService, CommunicationService, NotificationService, FileService, CalendarService, OperationsService, AuditService, PrivacyService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-001, ADM-003, ADM-004, ADM-006, ADM-007, ADM-008, ADM-010, ADM-012, ADM-013, ADM-014, ADM-015, ADM-016, ADM-017, ADM-018, ADM-019, ADM-020, ADM-021, ADM-022, ADM-023, ADM-024, ADM-025, ADM-026, ADM-027, ADM-028, ADM-029, ASM-001, ASM-002, ASM-003, ASM-005, ASM-006, ASM-007, ASM-008, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-011, CAL-001, CAL-002, CAL-003, CAL-004, CAL-005, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-006, CLS-007, CLS-008, CLS-009, CLS-010, CLS-011, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-001, LRN-002, LRN-003, LRN-004, LRN-007, LRN-008, LRN-009, LRN-010, OPS-003, OPS-005, OPS-008, PAR-001, PAR-002, PAR-003, PAR-004, PAR-005, PAR-006, PAR-008, PAR-009, PAR-010, PAR-011, PAR-012, PAR-013, PAR-014, PAR-015, PAR-016, PAR-017, PAR-018, PAR-019, PAR-020, PAR-021, PAY-001, PAY-002, PAY-003, PAY-004, PAY-005, PAY-006, PAY-007, PAY-008, PAY-009, PAY-010, PAY-011, PAY-012, SEC-001, SEC-002, SEC-003, SEC-007, SEC-008, SEC-009, SEC-010, STU-001, STU-003, STU-004, STU-007, STU-009, STU-010, STU-011, STU-012, STU-013, STU-014, STU-015, STU-016, STU-017, STU-018, STU-019, TCH-001, TCH-003, TCH-004, TCH-005, TCH-006, TCH-007, TCH-008, TCH-009, TCH-011, TCH-012, TCH-013, TCH-014, TCH-015, WEB-011 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| now()->Instant |  | Instant | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| today(zone:IanaZone)->LocalDate | zone:IanaZone | LocalDate | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## UnitOfWork

| Metadata | Contract |
| --- | --- |
| Kind/module | application port / shared |
| Responsibility | Atomic aggregate writes+audit+outbox; connection/session lifecycle outside domain; no network call inside lock-held transaction |
| Adapter | SQLAlchemy transaction adapter |
| Data ownership | Transaction infrastructure |
| Invariants | Atomic aggregate writes+audit+outbox; connection/session lifecycle outside domain; no network call inside lock-held transaction |
| Consumers | AuthenticationService, AccountService, FamilyService, StudentProfileService, TeacherService, ConsentService, PublicContentService, CourseService, CurriculumService, CohortService, SchedulingService, LiveClassService, EnrolmentService, AttendanceService, QuizService, AssignmentService, SubmissionService, AssessmentService, FeedbackService, ProgressService, CertificateService, BillingService, RefundService, ReportingService, CommunicationService, NotificationService, FileService, CalendarService, OperationsService, PrivacyService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | ADM-001, ADM-003, ADM-004, ADM-005, ADM-006, ADM-007, ADM-008, ADM-010, ADM-011, ADM-012, ADM-013, ADM-014, ADM-015, ADM-016, ADM-017, ADM-018, ADM-019, ADM-020, ADM-021, ADM-022, ADM-023, ADM-024, ADM-025, ADM-026, ADM-027, ADM-028, ASM-001, ASM-002, ASM-003, ASM-004, ASM-005, ASM-006, ASM-007, ASM-008, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-011, CAL-001, CAL-002, CAL-003, CAL-004, CAL-005, CLS-001, CLS-002, CLS-003, CLS-004, CLS-005, CLS-006, CLS-007, CLS-008, CLS-009, CLS-010, CLS-011, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007, LRN-001, LRN-002, LRN-003, LRN-004, LRN-007, LRN-008, LRN-009, LRN-010, OPS-003, OPS-005, OPS-008, PAR-001, PAR-002, PAR-003, PAR-004, PAR-005, PAR-006, PAR-008, PAR-009, PAR-010, PAR-011, PAR-012, PAR-013, PAR-014, PAR-015, PAR-016, PAR-017, PAR-018, PAR-019, PAR-020, PAR-021, PAY-001, PAY-002, PAY-003, PAY-004, PAY-005, PAY-006, PAY-007, PAY-008, PAY-009, PAY-010, PAY-011, PAY-012, SEC-001, SEC-002, SEC-003, SEC-008, SEC-009, SEC-010, STU-001, STU-003, STU-004, STU-007, STU-008, STU-009, STU-010, STU-011, STU-012, STU-013, STU-014, STU-015, STU-016, STU-017, STU-018, STU-019, TCH-001, TCH-003, TCH-004, TCH-005, TCH-006, TCH-007, TCH-008, TCH-009, TCH-010, TCH-011, TCH-012, TCH-013, TCH-014, TCH-015, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-011, WEB-012 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| begin()->Transaction |  | Transaction | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| commit(events:tuple[DomainEvent],audit:tuple[AuditRecord])->CommitResult | events:tuple[DomainEvent],audit:tuple[AuditRecord] | CommitResult | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |
| rollback()->None |  | None | ProviderUnavailable, ProviderRejected, UnknownOutcome, InvalidProviderResponse |

## MfaRepository

| Metadata | Contract |
| --- | --- |
| Kind/module | repository interface / identity |
| Responsibility | Lock and persist encrypted-factor references, hashed recovery codes, challenge/setup state and replay counter. |
| Adapter | SQLAlchemy data-mapper; PostgreSQL; encrypted secret column handled by secret adapter |
| Data ownership | mfa_factors,mfa_recovery_codes,mfa_challenges |
| Invariants | Challenge consume, recovery code consume, timestep update and full-session issuance commit atomically. |
| Consumers | AuthenticationService |
| Dependencies | UnitOfWork |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | AUTH-001, AUTH-002, AUTH-003, SEC-004 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| get_factor_for_update(account_id:uuid,scope:SelfAuthScope)->MfaFactor? | account_id:uuid,scope:SelfAuthScope | MfaFactor? | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| get_challenge_for_update(token_hash:bytes,browser_hash:bytes)->MfaChallenge? | token_hash:bytes,browser_hash:bytes | MfaChallenge? | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| find_recovery_for_update(factor_id:uuid,code_hash:bytes)->RecoveryCode? | factor_id:uuid,code_hash:bytes | RecoveryCode? | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| save_factor(factor:MfaFactor,expected_version:int)->None | factor:MfaFactor,expected_version:int | None | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| save_challenge(challenge:MfaChallenge)->None | challenge:MfaChallenge | None | MfaReplay, RepositoryConflict, PersistenceUnavailable |
| consume_recovery(code:RecoveryCode)->None | code:RecoveryCode | None | MfaReplay, RepositoryConflict, PersistenceUnavailable |

## MfaVerifier

| Metadata | Contract |
| --- | --- |
| Kind/module | integration port / identity |
| Responsibility | Generate/encrypt TOTP seed, verify RFC6238 proof and hash high-entropy recovery codes without exposing seed to domain. |
| Adapter | Audited TOTP library plus managed key-encryption adapter |
| Data ownership | Managed encryption key outside database; ciphertext/reference persisted in mfa_factors |
| Invariants | TOTP30-second step,6 digits,SHA1 for authenticator compatibility, +/-1-step clock tolerance; server enforces returned accepted step>last step. Secret seed>=160 bits; recoverycodes>=128-bit entropy. |
| Consumers | AuthenticationService |
| Dependencies | Pure supporting contract; requirements inherited from named consumers. |
| Authorization | Typed explicit scope mandatory for all user-driven reads; worker identity is constructed only in trusted worker entrypoint. |
| Requirements | AUTH-002, SEC-004 |
| Implementation chunks | Resolve port name in Code Blueprint; adapter and interface chunks remain distinct where dependency requires. |

| Signature | Input | Output | Failures |
| --- | --- | --- | --- |
| generate_setup(account_label:string)->EncryptedMfaSetup | account_label:string | EncryptedMfaSetup | InvalidMfaProof, SecretUnavailable |
| verify_totp(secret_reference:EncryptedSecretRef,code:string,now:Instant)->VerifiedTotpProof | secret_reference:EncryptedSecretRef,code:string,now:Instant | VerifiedTotpProof | InvalidMfaProof, SecretUnavailable |
| issue_recovery_codes(count:int)->RecoveryCodeSet | count:int | RecoveryCodeSet | InvalidMfaProof, SecretUnavailable |
| hash_recovery_code(code:SecretString)->bytes | code:SecretString | bytes | InvalidMfaProof, SecretUnavailable |
