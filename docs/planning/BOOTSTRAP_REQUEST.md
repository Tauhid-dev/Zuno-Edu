You are the Principal Software Architect, Principal Engineer, Principal Prompt Engineer,
Domain Architect, Security Architect, and Delivery Planner for a new production project:

ZUNO EDU

This is the FIRST repository bootstrap run.

This instruction supersedes any assumption that this project is an MVP.

Zuno Edu is being designed and built as the COMPLETE DEFINED PRODUCT BASELINE required
to launch the business.

The purpose of this run is to:

1. fully define the launch product
2. remove ambiguity from the product scope
3. define the complete object-oriented backend model
4. define the backend interfaces and service responsibilities
5. define the complete API contracts
6. map the frontend exactly onto the backend/domain model
7. define the frontend architecture and reusable component model
8. define security and role boundaries
9. define external integrations
10. establish production/infrastructure architecture
11. create persistent repository memory
12. create reusable Codex skills
13. create deterministic state reconciliation
14. decompose the entire launch product into small implementation chunks
15. create requirement-to-design-to-chunk traceability
16. independently review the entire plan
17. lock the approved implementation scope
18. prepare the repository so future sessions can execute simply:

       next chunk

THIS RUN MUST NOT IMPLEMENT PRODUCT FEATURES.

Planning, repository structure, documentation, schemas/contracts expressed as documentation,
agent instructions, skills, chunk manifests, and development/tooling skeletons are allowed.

Business feature implementation is NOT allowed during this bootstrap run.

======================================================================
A. CORE DEVELOPMENT CONTRACT
======================================================================

This project is NOT exploratory development.

Do not design a small MVP and defer necessary launch functionality.

The goal is to define the complete Zuno Edu launch product now and then implement exactly
that locked product.

The development system must protect against BOTH:

SCOPE CREEP:
adding features that were never approved.

AND

SCOPE EROSION:
silently removing, simplifying, postponing, or replacing approved launch requirements
because they are difficult or because an agent considers them unnecessary for an MVP.

Neither is acceptable.

Once planning is approved and merged, implementation agents must build the locked
launch scope exactly.

Agents must not:

- add speculative functionality
- remove required functionality
- quietly postpone requirements
- substitute partial functionality
- change architecture opportunistically
- broaden permissions
- weaken security
- introduce unnecessary abstractions
- refactor unrelated modules
- implement future considerations
- change agreed domain boundaries
- deviate from the agreed object model without an explicit architecture-change process

If the implementation discovers that the locked design genuinely cannot work, STOP the
affected chunk and document the conflict.

Do not silently redesign the system while implementing a chunk.

======================================================================
B. DESIGN FREEDOM DURING THIS BOOTSTRAP RUN ONLY
======================================================================

The high-level product requirements, role boundaries, technology direction, object-oriented
architecture requirement, Git workflow, scope-control system, remote-master authority,
state reconciliation model, and agent execution model in this prompt are requirements.

However, during THIS INITIAL PLANNING RUN ONLY, you may improve:

- internal folder names
- internal module boundaries
- aggregate boundaries
- class names
- service names
- phase structure
- chunk structure
- package layout
- detailed implementation patterns

when a materially better engineering design exists.

Document every material design decision.

After this planning PR is approved and merged, the resulting architecture becomes the
authoritative implementation blueprint.

Future agents must follow it rather than redesign it.

======================================================================
C. COMPLETE LAUNCH PRODUCT
======================================================================

Zuno Edu is an Australian online education platform for school-age children learning AI
and related technology skills through instructor-led courses.

The launch product contains five user-facing surfaces:

1. Zuno Edu Public Website
2. Zuno Edu Parent Portal
3. Zuno Edu Student LMS
4. Zuno Edu Teacher Portal
5. Zuno Edu Admin Portal

These are NOT five independent systems.

They must operate on:

- one authoritative backend
- one authoritative domain model
- one authorization model
- one PostgreSQL source of truth
- shared reusable application services
- reusable frontend components
- consistent API contracts

Role-specific access must be segregated at the backend.

======================================================================
D. PUBLIC WEBSITE PRODUCT SCOPE
======================================================================

The public website represents the Zuno Edu business and supports customer acquisition.

Plan complete launch functionality for:

- Home
- About Zuno Edu
- Programs/courses
- Course detail pages
- Age-group information
- Curriculum / learning outcomes
- Course duration
- Delivery method
- Upcoming cohorts/classes
- Course schedule/timetable
- Course pricing
- Teacher/public instructor profiles
- How classes work
- Parent information
- FAQs
- Contact
- policies
- privacy information
- terms information
- relevant child-safety information
- enrolment entry point
- parent registration/login entry point

Only explicitly published information may be publicly visible.

No private student, family, class, payment, teacher operational, or administrative
information may be available publicly.

======================================================================
E. PARENT PORTAL PRODUCT SCOPE
======================================================================

The parent/guardian is the primary family account holder.

A parent account can be associated with one or more students.

Plan launch functionality covering:

- parent account creation
- authentication
- profile management
- contact information
- communication preferences
- policy/consent acknowledgements where appropriate
- child/student registration
- multiple children
- course browsing
- course enrolment
- cohort selection where applicable
- enrolment status
- children's schedules
- upcoming classes
- class information
- child's attendance
- child's course progress
- released teacher feedback
- child's assignments/submission status where appropriate
- child's assessments/results where appropriate
- child's certificates/achievements
- relevant events
- notifications/announcements
- own family's billing
- own family's payment history
- own family's invoices/receipts
- payment actions allowed by the billing design
- logout/security/account operations

A parent must NEVER access another family's information.

Parent access must always be constrained by family ownership.

Parents do not receive:

- teacher administration
- unrelated student data
- global course administration
- business financial reporting
- other family billing
- system administration

Parents may VIEW relevant schedules.

Parents must not directly obtain unrestricted global scheduling authority.

Where schedule-change requests are supported by the locked product design, they must be
implemented as appropriately constrained requests rather than administrative scheduling
control.

======================================================================
F. STUDENT REGISTRATION DATA
======================================================================

Apply data minimisation.

Capture information that is genuinely useful to the educational service.

For the initial student profile, the following are REQUIRED:

- student name
- student age

The following must be OPTIONAL:

- school name

During planning, determine whether the student's name should be represented internally as:

- first name
- preferred name where useful
- last name

without making unnecessary fields mandatory.

Age is required by the product.

The planner may choose a robust internal representation for age/date handling, but the
user experience MUST capture the child's age as required information.

If date of birth is proposed internally instead of storing a mutable numeric age,
document the reasoning clearly and ensure the registration UX still satisfies the
requirement to capture age.

Other potentially useful educational fields MAY be offered only when justified and should
normally be optional, for example:

- school year / grade
- learning interests
- previous AI/coding experience
- optional learning notes

Do not make unnecessary child information mandatory.

Do not collect sensitive information merely because it might theoretically be useful.

Document:

- required fields
- optional fields
- purpose of each field
- role allowed to access each field
- retention/security considerations

in the data model and authorization documentation.

======================================================================
G. STUDENT LMS PRODUCT SCOPE
======================================================================

The Student LMS is a focused learning environment supporting live instructor-led courses.

It is NOT intended to become a generic Moodle replacement.

Plan launch functionality covering:

- student login
- student dashboard
- enrolled courses
- course progress
- modules/weeks
- lessons
- lesson content
- downloadable resources
- video resources
- images
- activities
- quizzes
- assignments
- project work
- file submissions
- submission status
- assessment/result visibility
- teacher feedback
- upcoming classes
- live class joining
- attendance visibility
- achievements where defined
- course completion
- certificates
- relevant announcements

Use a consistent learning journey such as:

Learn
→ Attend / Watch
→ Try
→ Build
→ Submit
→ Review / Reflect

Students receive access only to:

- their own profile where appropriate
- their own enrolments
- their own learning data
- released content for courses in which they are enrolled
- their own submissions
- their own feedback
- their own progress
- their own certificates

Students must NEVER receive access to:

- payment information
- invoices
- parent financial information
- family administration
- other students' private information
- internal teacher information
- course administration
- class administration
- pricing administration
- system settings
- business analytics

======================================================================
H. TEACHER PORTAL PRODUCT SCOPE
======================================================================

The Teacher Portal exists exclusively to deliver education.

Teachers may access only the students/classes/resources required to perform their assigned
teaching responsibilities.

Plan launch functionality covering:

- teacher authentication
- teacher dashboard
- assigned courses
- assigned cohorts
- assigned class sessions
- class schedule
- upcoming classes
- lesson plans/resources
- initiating assigned live classes
- permitted class rescheduling
- class/session details
- attendance management
- assigned learners
- learner educational profile required for teaching
- assignments
- submissions from assigned learners
- assessment/marking
- teacher feedback
- learning progress
- teaching resources
- relevant operational notifications

Teacher visibility of student data must be restricted to:

- learners assigned to the teacher's relevant cohort/class
- information genuinely needed to teach those learners

Teachers must have ZERO financial administration access.

Teachers must not access:

- payment records
- Stripe payment information
- invoices
- receipts belonging to families
- payment methods
- refunds
- revenue
- financial analytics
- financial reports
- parent billing history
- administrative pricing controls
- discount/coupon administration

This restriction must exist at:

- API authorization
- service authorization
- repository/query scope where appropriate
- frontend navigation
- frontend route guards
- automated authorization tests

Hiding payment menus is NOT sufficient security.

Teachers may see public-facing course prices in the same way any public visitor can see
them, but this does NOT constitute payment administration access.

======================================================================
I. ADMIN PORTAL PRODUCT SCOPE
======================================================================

The Admin Portal is the business control plane.

Plan complete launch functionality for appropriate authorised administrators covering:

- admin authentication
- dashboard
- parent management
- student management
- teacher management
- role management where appropriate
- courses
- programs
- modules
- lessons
- lesson content
- lesson blocks
- learning resources
- quizzes
- assignments
- assessments
- cohorts
- class sessions
- schedules
- teacher assignments
- student enrolments
- attendance oversight
- progress oversight
- teacher feedback oversight where appropriate
- certificates
- events
- announcements
- notifications
- file/resources management
- prices
- course/cohort fees
- approved discounts if included in the final billing design
- payments
- payment status
- invoices/receipts
- refunds
- financial reporting required to operate the platform
- system/integration settings
- audit visibility
- operational settings

Financial administration is an Admin capability.

Do not give Teacher, Student, or unrelated Parent accounts administrative payment access.

======================================================================
J. LMS DOMAIN MODEL
======================================================================

The content hierarchy must support at minimum:

Program / Offering where justified
    Course
        Module / Week
            Lesson
                LessonBlock

Plan supported LessonBlock/domain types such as:

- Heading
- RichText
- Image
- Video
- DownloadableResource
- Activity
- Quiz reference
- Assignment reference

Also model the complete teaching lifecycle:

Course
Cohort
ClassSession
TeacherAssignment
Enrolment
Attendance
Quiz
QuizQuestion
QuizAttempt
Assignment
Submission
Assessment
TeacherFeedback
StudentProgress
Achievement where included
Certificate

Clearly distinguish:

COURSE
Reusable educational curriculum/content.

COHORT
A scheduled delivery of a Course.

CLASS SESSION
An individual teaching session belonging to a Cohort.

One Course must be reusable across many Cohorts.

Do not duplicate curriculum merely because a new cohort is created.

======================================================================
K. BILLING PRODUCT SCOPE
======================================================================

Design a clear launch billing model.

At minimum plan:

- course/cohort price configuration
- parent checkout
- Stripe Checkout or equivalent approved Stripe flow
- payment records
- payment status
- Stripe webhook processing
- invoice/receipt representation where required
- refund administration
- reconciliation identifiers
- financial auditability
- secure webhook validation
- idempotency

Do not trust browser redirects as evidence of payment success.

Stripe webhook/server verification must be authoritative.

The planning process must explicitly decide and document the launch payment modes rather
than leaving billing ambiguous.

Do not introduce subscriptions, instalments, marketplace payments, or complex billing
models merely because Stripe supports them unless the final locked business requirements
actually include them.

======================================================================
L. LIVE CLASS PRODUCT SCOPE
======================================================================

Use Zoom as the initial external live-class provider unless planning uncovers a material
reason inconsistent with the approved technology direction.

Plan:

- meeting creation
- meeting/update lifecycle
- secure storage of meeting identifiers
- teacher start/initiate experience
- student join experience
- parent visibility where appropriate
- schedule changes
- meeting cancellation
- class-session relationship
- provider failures
- synchronization
- retry/idempotency where required

Keep Zoom behind an abstraction/interface.

Domain/application code must not be tightly coupled directly to Zoom-specific SDK
implementation details.

======================================================================
M. CALENDAR PRODUCT SCOPE
======================================================================

Plan Google Calendar integration for appropriate schedule/event functionality.

The domain scheduling model remains authoritative.

Google Calendar is an integration, not the core domain database.

Plan:

- calendar event creation
- recurring class representation where appropriate
- updates
- cancellations
- relevant reminders
- optional parent add-to-calendar flow
- external event identifiers
- synchronization/error handling

Keep Calendar behind an application port/interface.

======================================================================
N. COMMUNICATION PRODUCT SCOPE
======================================================================

Use Resend or the approved transactional email provider.

Plan transactional communications including appropriate:

- registration confirmation
- enrolment confirmation
- payment confirmation/receipt notification
- class reminders
- schedule-change notifications
- assignment/feedback notifications where needed
- course completion/certificate communication
- password/account flows
- operational notices

Use background processing where appropriate.

Do not make normal API response latency dependent on noncritical email transmission.

Keep email behind an interface.

======================================================================
O. FILE AND OBJECT STORAGE
======================================================================

Use S3-compatible object storage behind an abstraction.

Plan storage for:

- learning resources
- student assignment uploads
- generated certificates
- appropriate internal documents/assets

Prefer secure presigned operations where appropriate.

The database stores authoritative metadata and object references.

Do not expose permanent unrestricted object-storage credentials to browsers.

Plan:

- validation
- file-type rules
- size limits
- ownership
- access control
- expiration
- deletion
- metadata
- orphan cleanup where appropriate

======================================================================
P. SECURITY, PRIVACY, CHILD DATA, AND AUDITABILITY
======================================================================

Security must be designed before implementation rather than added later.

Plan:

- authentication
- password/session/token security
- RBAC
- resource ownership
- family ownership
- teacher assignment constraints
- student ownership
- administrator privileges
- route authorization
- service-level authorization
- query/repository scoping where appropriate
- secret handling
- webhook verification
- input validation
- secure file handling
- audit events
- rate limiting where appropriate
- logging without inappropriate sensitive-data leakage
- account lifecycle
- consent/policy acknowledgement records where required by product design
- data minimisation
- secure production configuration

Because this product involves children, specifically document child/family data boundaries.

Do not invent legal advice.

Where final legal text or jurisdiction-specific compliance decisions require professional
input, create a clearly identified human/legal decision point without weakening the
technical privacy/security architecture.

======================================================================
Q. LAUNCH OPERATIONS
======================================================================

The product is intended to launch as a real business platform.

Planning must therefore cover:

- production configuration
- Docker
- Docker Compose where appropriate
- Caddy
- HTTPS
- PostgreSQL
- Redis
- worker
- object storage
- migrations
- secrets/environment configuration
- CI
- automated tests
- deployment
- health checks
- structured logs
- error reporting
- monitoring
- audit logs
- backups
- restore procedure
- database backup
- object-storage backup/retention considerations
- failure recovery
- dependency/security scanning where appropriate
- staging/testing strategy
- production readiness checks

Initial target deployment is compatible with an OCI/cloud VPS architecture.

Do not make the domain/application architecture depend on OCI.

======================================================================
R. EXPLICIT INITIAL OUT-OF-SCOPE BASELINE
======================================================================

Unless analysis during this bootstrap identifies one of these as absolutely necessary to
satisfy another locked requirement, treat the following as outside the initial launch
baseline:

- native iOS application
- native Android application
- student-to-student social network
- public discussion forum
- unrestricted student messaging
- marketplace for external tutors
- multi-school enterprise tenancy
- full school administration system
- SCORM/xAPI compatibility
- AI autonomous tutor
- generative AI assistant
- AI content generation
- advanced gamification platform
- unrelated CRM
- unrelated marketing automation suite
- microservice architecture
- unnecessary third-party integrations

Create FUTURE_CONSIDERATIONS.md for ideas that are useful but not part of the locked
launch product.

Do not implement FUTURE_CONSIDERATIONS automatically.

======================================================================
S. OBJECT-ORIENTED MODEL REQUIREMENT
======================================================================

The backend MUST follow a well-designed object-oriented/domain model.

This is a binding architectural requirement.

However:

Do not create meaningless classes merely to satisfy an OOP label.

Use OOP where domain identity, behavior, invariants, lifecycle, reuse, interfaces,
polymorphism, composition, and encapsulation justify it.

Prefer:

- domain entities
- value objects
- domain policies
- domain services where appropriate
- application services/use cases
- repository interfaces
- integration ports
- infrastructure adapters
- dependency inversion
- composition
- typed contracts

Avoid:

- procedural business logic scattered across FastAPI endpoints
- massive service classes
- god objects
- active-record style domain coupling when avoidable
- framework-dependent domain entities
- Stripe logic inside domain entities
- Zoom logic inside domain entities
- database queries directly embedded throughout API routes
- duplicated business rules
- duplicated frontend/backend contracts
- unnecessary inheritance

Prefer composition over inheritance unless inheritance represents a genuine domain
relationship and provides clear value.

======================================================================
T. BACKEND MUST BE DESIGNED BEFORE FRONTEND
======================================================================

The planning sequence must be:

PRODUCT REQUIREMENTS
        ↓
DOMAIN MODEL
        ↓
BACKEND OBJECT MODEL
        ↓
APPLICATION USE CASES/SERVICES
        ↓
REPOSITORY/PORT CONTRACTS
        ↓
DATABASE/PERSISTENCE MODEL
        ↓
AUTHORIZATION POLICIES
        ↓
API CONTRACTS
        ↓
EXTERNAL INTEGRATION CONTRACTS
        ↓
FRONTEND INFORMATION ARCHITECTURE
        ↓
FRONTEND OBJECT/COMPONENT MODEL
        ↓
FRONTEND ↔ API ↔ BACKEND MAPPING
        ↓
CHUNKS

Do not independently invent frontend capabilities that do not map to the approved backend
and product requirements.

Do not build backend functionality without identifying which requirement/use case requires it.

======================================================================
U. REQUIRED BACKEND OBJECT CATALOG
======================================================================

Create:

docs/architecture/BACKEND_OBJECT_CATALOG.md

Before implementation, enumerate the planned backend architecture in enough detail that
future implementation agents do not need to redesign it.

For every planned important object/class/interface document:

- name
- type
- module
- responsibility
- invariants
- important attributes
- public methods
- method purpose
- expected inputs
- expected outputs
- errors/domain failures
- authorization considerations
- dependencies
- objects it collaborates with
- persistence relationship
- requirements it satisfies
- chunks expected to implement it

The catalog must cover all launch-domain objects.

Likely domain concepts include, subject to proper aggregate design:

Identity / Accounts:
- User
- Role / role representation
- ParentProfile / Guardian
- StudentProfile
- TeacherProfile
- Administrator representation
- Family
- GuardianStudent relationship
- consent/policy acknowledgement entities where appropriate

Learning:
- Program/Offering if justified
- Course
- CourseModule
- Lesson
- LessonBlock and appropriate block representations
- LearningResource

Delivery:
- Cohort
- ClassSession
- TeacherAssignment
- Enrolment
- AttendanceRecord

Assessment:
- Quiz
- QuizQuestion
- QuizAttempt
- Assignment
- Submission
- Assessment
- TeacherFeedback
- StudentProgress
- Achievement if retained
- Certificate

Commercial:
- Course/Cohort Price or appropriate Money/Pricing representation
- Payment
- Refund
- Invoice/Receipt representation where required
- Discount/Coupon only if accepted in launch billing requirements

Communication/Operations:
- Event/Announcement if appropriate
- Notification
- FileAsset
- AuditRecord/AuditEvent
- ApplicationSetting / integration configuration representation where appropriate

Do not blindly create one database table per noun.

Perform proper aggregate/domain analysis first.

======================================================================
V. REQUIRED BACKEND SERVICE / USE-CASE CATALOG
======================================================================

Create:

docs/architecture/BACKEND_SERVICE_CATALOG.md

Document every planned important application service/use-case object.

Likely capability areas include:

- AuthenticationService
- AuthorizationPolicy / AuthorizationService
- AccountService
- FamilyService
- StudentProfileService
- TeacherService
- CourseService
- CurriculumService
- CohortService
- SchedulingService
- LiveClassService
- EnrolmentService
- AttendanceService
- QuizService
- AssignmentService
- SubmissionService
- AssessmentService
- FeedbackService
- ProgressService
- CertificateService
- BillingService
- RefundService where separated
- NotificationService
- FileService
- CalendarService
- ReportingService
- AuditService

The final design may rename/split/combine these where domain analysis provides a better
boundary.

For each service document planned public operations.

Examples of the LEVEL OF DETAIL required:

EnrolmentService
    enrol_student(...)
    cancel_enrolment(...)
    get_student_enrolments(...)
    get_family_enrolments(...)
    validate_enrolment_access(...)

SchedulingService
    create_class_session(...)
    reschedule_class_session(...)
    cancel_class_session(...)
    list_student_schedule(...)
    list_teacher_schedule(...)
    list_family_schedule(...)

AttendanceService
    record_attendance(...)
    amend_attendance(...)
    list_student_attendance(...)
    list_cohort_attendance(...)

The actual planner must determine the complete operation set.

Do not leave core application behavior undefined for future coding agents to invent.

At the same time, do NOT attempt to pre-specify every trivial private utility/helper
function.

The planning catalog must define all durable:

- domain behavior
- public application operations
- interfaces
- repositories
- integration ports
- API-visible operations

Private implementation helpers may be introduced later when they do not alter architecture,
scope, behavior, or contracts.

======================================================================
W. REQUIRED REPOSITORY AND PORT CATALOG
======================================================================

Create:

docs/architecture/PORTS_AND_REPOSITORIES.md

Document required interfaces such as appropriate:

- UserRepository
- FamilyRepository
- StudentRepository
- TeacherRepository
- CourseRepository
- CohortRepository
- EnrolmentRepository
- AttendanceRepository
- AssessmentRepository
- ProgressRepository
- PaymentRepository
- CertificateRepository
- AuditRepository

And integration ports such as:

- PaymentGateway
- LiveClassProvider
- CalendarProvider
- EmailProvider
- ObjectStorageProvider
- UnitOfWork
- Clock where useful

Do not over-fragment repositories unnecessarily.

Choose aggregate-appropriate boundaries.

Document dependencies and ownership.

======================================================================
X. BACKEND LAYERING
======================================================================

Use an architecture approximately following:

apps/api/src/zuno_edu/

    domain/
        entities/
        value_objects/
        enums/
        policies/
        services/

    application/
        commands/
        queries/
        services/
        dto/
        ports/

    infrastructure/
        persistence/
        integrations/
        messaging/
        configuration/

    interfaces/
        api/
        schemas/
        dependencies/

The exact structure may be refined during this planning run.

The intended dependency direction is:

Interfaces
      ↓
Application
      ↓
Domain

Infrastructure implements ports required by Application/Domain.

Domain must not depend on:

- FastAPI
- SQLAlchemy session mechanics
- Stripe SDK
- Zoom SDK
- Google API SDK
- Resend SDK
- S3 SDK
- Caddy
- OCI

Keep infrastructure replaceable.

======================================================================
Y. DATABASE AND DATA MODEL
======================================================================

Create:

docs/architecture/DATA_MODEL.md
docs/architecture/AGGREGATES.md
docs/architecture/DATABASE_SCHEMA_PLAN.md

Document:

- aggregate boundaries
- entities
- relationships
- ownership
- cardinality
- keys
- important constraints
- uniqueness
- statuses/state machines
- lifecycle rules
- deletion/archive strategy
- timestamps
- auditing
- indexes
- authorization-sensitive relationships
- migration approach

Explicitly model Parent ↔ Student relationships.

Student required registration information:

- name
- age

School:

- optional

Do not accidentally make optional student information a database NOT NULL requirement.

Document the distinction between:

Course
Cohort
ClassSession

very clearly.

======================================================================
Z. AUTHORIZATION MODEL
======================================================================

Create:

docs/architecture/AUTHORIZATION_MODEL.md
docs/architecture/PERMISSION_MATRIX.md
docs/architecture/DATA_ACCESS_BOUNDARIES.md

Authorization must use:

ROLE
+
RESOURCE OWNERSHIP
+
RELATIONSHIP/ASSIGNMENT
+
RESOURCE STATE where relevant

not merely role checks.

Examples:

A Parent may read Student X only if the authenticated Parent is an authorised guardian
of Student X.

A Teacher may read Student X educational information only if Student X belongs to a
cohort/class currently assigned to that Teacher and the information is required for the
teaching operation.

A Student may read Submission X only if it belongs to that Student.

An Admin may access financial administration based on approved admin privileges.

Teacher access to payments must fail even if the Teacher guesses a payment endpoint ID.

Create explicit negative authorization requirements and tests.

======================================================================
AA. API ARCHITECTURE
======================================================================

Create:

docs/architecture/API_ARCHITECTURE.md
docs/architecture/API_CATALOG.md

Plan versioned REST APIs.

Example namespace:

/api/v1/

Potential capability groups:

auth
accounts
families
parents
students
teachers
courses
modules
lessons
resources
cohorts
classes
schedules
enrolments
attendance
quizzes
assignments
submissions
assessments
feedback
progress
certificates
payments
refunds
events
notifications
files
admin

Do not treat this example as mandatory endpoint naming if a better REST structure is
identified.

For every planned API operation document:

- method
- route
- purpose
- role(s)
- ownership rule
- request contract
- response contract
- main application service operation
- main domain objects
- important errors
- requirement IDs
- frontend consumers

This document must become the contract between frontend and backend.

======================================================================
AB. FRONTEND ARCHITECTURE AFTER BACKEND
======================================================================

Only after the backend/domain/API design is complete, create:

docs/architecture/FRONTEND_ARCHITECTURE.md
docs/architecture/FRONTEND_ROUTE_MAP.md
docs/architecture/FRONTEND_COMPONENT_CATALOG.md
docs/architecture/FRONTEND_STATE_AND_API_MODEL.md

Use:

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

Design for:

- component reuse
- clear feature boundaries
- accessibility
- responsiveness
- predictable role navigation
- age-appropriate Student UX
- parent clarity
- teacher efficiency
- admin operational efficiency

Prefer hierarchy:

Route/Page
    ↓
Feature
    ↓
Domain Component
    ↓
Shared UI Component

Separate:

- rendering/presentation
- API clients
- forms
- validation
- state
- domain-specific frontend logic
- reusable visual primitives

Avoid:

- giant page components
- duplicated forms
- duplicated API types
- business rules embedded randomly in JSX
- teacher/admin UI leakage
- financial components being bundled into Teacher modules

======================================================================
AC. FRONTEND COMPONENT CATALOG
======================================================================

Before frontend implementation, document every durable important frontend component/module.

For each, document:

- name
- role/product surface
- responsibility
- props/input
- data requirements
- API operation(s)
- authorization assumptions
- reusable/shared or feature-specific
- state behavior
- requirements served
- chunk implementing it

Examples include categories such as:

Shared:
- AppShell
- RoleNavigation
- PageHeader
- LoadingState
- ErrorState
- EmptyState
- Form controls
- confirmation dialog
- notification presentation
- accessible modal
- file upload control
- schedule/calendar presentation
- reusable data table where appropriate

Parent:
- FamilyDashboard
- StudentSummaryCard
- EnrolmentSummary
- ChildProgressView
- ParentSchedule
- FamilyBillingView

Student:
- StudentDashboard
- CourseProgress
- ModuleNavigation
- LessonRenderer
- LessonBlockRenderer
- QuizExperience
- AssignmentSubmission
- FeedbackView
- StudentSchedule
- CertificateView

Teacher:
- TeacherDashboard
- AssignedClassList
- ClassSessionView
- AttendanceManager
- StudentTeachingProfile
- AssignmentReview
- FeedbackEditor
- TeacherSchedule
- StartClassAction

Admin:
- AdminDashboard
- CourseManager
- CurriculumEditor
- CohortManager
- ScheduleManager
- TeacherAssignmentManager
- EnrolmentManager
- Family/StudentManager
- TeacherManager
- PaymentManager
- RefundManager
- ReportingView
- IntegrationSettings
- AuditView

The actual planning run must determine the complete catalog and avoid needless duplication.

======================================================================
AD. MANDATORY FRONTEND ↔ BACKEND MAPPING
======================================================================

Create one of the most important documents in the repository:

docs/architecture/FRONTEND_BACKEND_MAPPING.md

Every role-facing frontend capability must map explicitly to:

Frontend route
    ↓
Frontend feature/component
    ↓
API operation
    ↓
Application service/use case
    ↓
Domain object/policy
    ↓
Repository / integration port
    ↓
Persistence/external integration where applicable

Example:

Teacher Attendance Page
    ↓
AttendanceManager
    ↓
PUT /api/v1/classes/{id}/attendance
    ↓
AttendanceService.record_attendance()
    ↓
ClassSession + AttendanceRecord + TeacherAssignmentPolicy
    ↓
AttendanceRepository
    ↓
PostgreSQL

Another example:

Parent Payment Page
    ↓
FamilyBillingView
    ↓
GET /api/v1/families/{family_id}/payments
    ↓
BillingService.list_family_payments()
    ↓
FamilyOwnershipPolicy + Payment
    ↓
PaymentRepository
    ↓
PostgreSQL

Teacher must have no corresponding administrative payment route/component/use case.

No frontend functionality may exist without a documented backend mapping.

No backend business use case may exist without a documented requirement/consumer or
administrative purpose.

======================================================================
AE. CODE BLUEPRINT
======================================================================

Create:

docs/architecture/CODE_BLUEPRINT.md

This document is the consolidated implementation map.

It must reference:

- domain objects
- services/use cases
- ports
- repositories
- API operations
- frontend routes
- frontend components
- integrations
- authorization policies
- requirements
- implementation chunks

The objective is that when an implementation agent receives one chunk, it should not need
to redesign the surrounding application.

If implementation reveals that a durable object/function/interface is missing from the
blueprint and adding it would materially alter architecture, the agent must STOP and report
a blueprint conflict instead of silently inventing new architecture.

Trivial private implementation helpers do not require architecture-change approval.

======================================================================
AF. REQUIREMENT IDENTIFIERS
======================================================================

Create stable requirement IDs.

Use logical families such as:

WEB-xxx   Public Website
PAR-xxx   Parent Portal
STU-xxx   Student LMS
TCH-xxx   Teacher Portal
ADM-xxx   Admin Portal
LRN-xxx   Learning/content
CLS-xxx   Classes/scheduling
ENR-xxx   Enrolment
ASM-xxx   Assessment
AUTH-xxx  Identity/authentication/authorization
PAY-xxx   Billing/payments
COM-xxx   Communications
CAL-xxx   Calendar
FILE-xxx  File/object storage
SEC-xxx   Security/privacy
OPS-xxx   Operations/deployment
NFR-xxx   Non-functional requirements

Create:

docs/product/FUNCTIONAL_REQUIREMENTS.md
docs/product/NON_FUNCTIONAL_REQUIREMENTS.md

Every launch requirement needs:

- stable ID
- description
- rationale
- affected role
- priority: REQUIRED FOR LAUNCH
- acceptance criteria or reference
- related domain capability

Avoid ambiguous requirements such as:

"support payments"

Instead describe observable required behavior.

======================================================================
AG. REQUIREMENT TRACEABILITY
======================================================================

Create:

docs/planning/REQUIREMENT_TRACEABILITY.md

Enforce:

Requirement
    ↔
Domain/Object
    ↔
Service/Use Case
    ↔
API
    ↔
Frontend or integration consumer
    ↔
Chunk
    ↔
Tests
    ↔
Verification

Every launch requirement must map to at least one implementation chunk.

Every implementation chunk must map to at least one approved requirement or necessary
architectural/operational requirement.

No orphan requirements.

No orphan implementation chunks.

Before scope lock:

100% of launch requirements must have planned implementation coverage.

======================================================================
AH. PRODUCT DOCUMENTATION
======================================================================

Create at minimum:

docs/product/
    PRODUCT_DEFINITION.md
    LAUNCH_SCOPE.md
    OUT_OF_SCOPE.md
    FUNCTIONAL_REQUIREMENTS.md
    NON_FUNCTIONAL_REQUIREMENTS.md
    ROLE_CAPABILITIES.md
    USER_JOURNEYS.md
    DATA_REQUIREMENTS.md
    LAUNCH_ACCEPTANCE_CRITERIA.md
    FUTURE_CONSIDERATIONS.md
    SCOPE_LOCK.md

LAUNCH_SCOPE.md is authoritative for what must exist before business launch.

OUT_OF_SCOPE.md is authoritative for what must not silently enter implementation.

======================================================================
AI. ARCHITECTURE DOCUMENTATION
======================================================================

Create at minimum:

docs/architecture/
    SYSTEM_ARCHITECTURE.md
    DOMAIN_MODEL.md
    AGGREGATES.md
    BACKEND_ARCHITECTURE.md
    BACKEND_OBJECT_CATALOG.md
    BACKEND_SERVICE_CATALOG.md
    PORTS_AND_REPOSITORIES.md
    DATA_MODEL.md
    DATABASE_SCHEMA_PLAN.md
    AUTHORIZATION_MODEL.md
    PERMISSION_MATRIX.md
    DATA_ACCESS_BOUNDARIES.md
    API_ARCHITECTURE.md
    API_CATALOG.md
    INTEGRATIONS.md
    BILLING_ARCHITECTURE.md
    LIVE_CLASS_ARCHITECTURE.md
    CALENDAR_ARCHITECTURE.md
    COMMUNICATION_ARCHITECTURE.md
    FILE_STORAGE_ARCHITECTURE.md
    FRONTEND_ARCHITECTURE.md
    FRONTEND_ROUTE_MAP.md
    FRONTEND_COMPONENT_CATALOG.md
    FRONTEND_STATE_AND_API_MODEL.md
    FRONTEND_BACKEND_MAPPING.md
    CODE_BLUEPRINT.md
    SECURITY_ARCHITECTURE.md
    DEPLOYMENT_ARCHITECTURE.md
    ADR/

======================================================================
AJ. ENGINEERING STANDARDS
======================================================================

Create:

docs/standards/
    ENGINEERING_STANDARDS.md
    OOP_AND_DOMAIN_STANDARDS.md
    BACKEND_STANDARDS.md
    FRONTEND_STANDARDS.md
    API_STANDARDS.md
    DATABASE_STANDARDS.md
    TESTING_STANDARDS.md
    SECURITY_STANDARDS.md
    ACCESSIBILITY_STANDARDS.md
    UI_DESIGN_SYSTEM.md
    OBSERVABILITY_STANDARDS.md
    DOCUMENTATION_STANDARDS.md

The OOP standard is binding after architecture approval.

======================================================================
AK. REPOSITORY STRUCTURE
======================================================================

Create a professional repository structure approximately:

zuno-edu/
│
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── .editorconfig
│
├── docs/
│   ├── product/
│   ├── architecture/
│   ├── standards/
│   └── planning/
│       ├── MASTER_PLAN.md
│       ├── PHASES.md
│       ├── DEPENDENCY_GRAPH.md
│       ├── REQUIREMENT_TRACEABILITY.md
│       ├── CHUNK_REGISTRY.md
│       └── chunks/
│
├── memory/
│   ├── PROJECT_STATE.md
│   ├── ARCHITECTURE_SNAPSHOT.md
│   ├── DECISIONS.md
│   ├── CONSTRAINTS.md
│   ├── progress.json
│   └── handoffs/
│
├── skills/
│   ├── README.md
│   ├── skill-router.md
│   ├── frontend/
│   ├── backend/
│   ├── security/
│   ├── integrations/
│   ├── infrastructure/
│   └── workflow/
│
├── apps/
│   ├── web/
│   └── api/
│
├── packages/
│   ├── ui/
│   ├── contracts/
│   └── config/
│
├── tests/
├── infra/
└── scripts/

You may improve this structure during bootstrap if justified.

Document changes.

Do not implement business features.

======================================================================
AL. SKILLS SYSTEM
======================================================================

Skills are reusable operational knowledge for Codex.

Create:

skills/skill-router.md

and relevant skills including at minimum:

skills/frontend/
    nextjs.md
    typescript.md
    design-system.md
    component-architecture.md
    accessibility.md
    frontend-api-integration.md
    frontend-testing.md

skills/backend/
    python.md
    fastapi.md
    oop-domain-modeling.md
    application-services.md
    sqlalchemy-alembic.md
    repository-pattern.md
    api-design.md
    validation.md
    backend-testing.md

skills/security/
    authentication.md
    authorization-rbac.md
    resource-ownership.md
    child-family-data-boundaries.md
    secrets-and-integrations.md
    secure-file-handling.md
    webhook-security.md
    security-review.md

skills/integrations/
    stripe.md
    zoom.md
    google-calendar.md
    resend.md
    object-storage.md

skills/infrastructure/
    docker.md
    docker-compose.md
    github-actions.md
    caddy.md
    postgres-operations.md
    redis-workers.md
    deployment.md
    backups-restore.md
    observability.md

skills/workflow/
    chunk-execution.md
    git-workflow.md
    state-reconciliation.md
    scope-control.md
    planning-review.md
    review-agent.md
    memory-maintenance.md
    pr-handoff.md

Each skill should contain:

- when to invoke
- when not to invoke
- required context
- rules
- implementation standards
- verification requirements
- common failure conditions

======================================================================
AM. AUTOMATIC SKILL ROUTING
======================================================================

DO NOT load every skill for every chunk.

Every chunk manifest must declare:

required_skills:
optional_skills:

At the start of a chunk:

1. load the required skills
2. inspect the task
3. load an optional skill only when objectively relevant

If a required reusable engineering rule is missing from an existing skill, the chunk may
update that skill when necessary.

Skill changes must:

- remain generic/reusable
- not encode temporary implementation notes
- not contradict authoritative architecture
- be reviewed as part of the chunk
- not become an excuse to change project scope

Do not create duplicate skills.

The skill router must explain how task type maps to skills.

======================================================================
AN. MEMORY SYSTEM
======================================================================

The repository itself is persistent project memory.

Use:

docs/
    authoritative detailed truth

memory/
    compact operational context

chunk manifests/
    exact task context

Git/
    historical execution evidence

Do NOT use vector embeddings/vector database during initial project development.

Deterministic references are preferred because they are:

- cheaper
- more predictable
- auditable
- less susceptible to irrelevant semantic retrieval
- sufficient at the planned repository size

A future architecture decision may introduce retrieval if deterministic context selection
becomes genuinely inefficient.

Create:

memory/PROJECT_STATE.md
memory/ARCHITECTURE_SNAPSHOT.md
memory/DECISIONS.md
memory/CONSTRAINTS.md
memory/progress.json
memory/handoffs/

PROJECT_STATE.md:
target <= approximately 1,000 words.

ARCHITECTURE_SNAPSHOT.md:
target approximately 500-800 words.

DECISIONS.md:
only durable decisions.

CONSTRAINTS.md:
only binding current constraints.

Do not create a chronological diary.

Do not copy long architecture documents into memory.

======================================================================
AO. REMOTE MASTER IS THE PRIMARY EXECUTION TRUTH
======================================================================

This requirement is CRITICAL.

The human reviews and merges PRs remotely on GitHub.

Therefore:

LOCAL STATE MUST NEVER BE ASSUMED CURRENT.

Before selecting any future chunk:

    git fetch origin
    git checkout master
    git pull --ff-only origin master

Remote master is authoritative.

State evidence priority is:

1. freshly synchronized origin/master repository contents and Git history
2. authoritative chunk completion evidence on master
3. chunk manifests
4. memory/progress.json
5. conversational context

progress.json is a compact routing cache.

It is NOT stronger evidence than current master.

======================================================================
AP. DO NOT MODIFY MASTER DURING STATE RECONCILIATION
======================================================================

State reconciliation on master must be READ-ONLY.

Correct sequence:

1. fetch origin
2. checkout master
3. pull --ff-only origin master
4. inspect/reconcile state without editing master
5. determine effective completed/ready state
6. select exactly one next eligible chunk
7. create a fresh feature branch from synchronized master
8. persist any necessary state reconciliation corrections on the feature branch
9. implement the selected chunk

Never make working-tree modifications directly on master.

Never commit directly to master.

======================================================================
AQ. STATE MODEL
======================================================================

Valid chunk states:

PLANNED
READY
BLOCKED
IN_PROGRESS
PR_OPEN
COMPLETE

Meaning:

PLANNED
defined but not currently executable.

READY
all required prerequisites/dependencies are satisfied according to the plan.

BLOCKED
documented blocker prevents execution.

IN_PROGRESS
currently being implemented on a feature branch.

PR_OPEN
implementation was pushed and submitted for human review but has not yet been confirmed
merged into master.

COMPLETE
implementation is present on synchronized master.

PR_OPEN MUST NOT be treated as COMPLETE merely because code was pushed.

However, after the human merges remotely, the next session may see the manifest still
containing PR_OPEN on master because that was the state committed in the PR.

Therefore the state reconciler must recognize:

PR_OPEN in file
+
chunk implementation/commit now present on synchronized master
=
effective COMPLETE

Persist that reconciliation on the newly created next feature branch.

======================================================================
AR. progress.json
======================================================================

Create a compact machine-readable state model similar to:

{
  "schema_version": 1,
  "project": "zuno-edu",
  "default_branch": "master",
  "scope_version": "1.0",
  "architecture_version": 1,
  "master_sha_at_last_reconciliation": null,
  "current_phase": "P01",
  "last_completed_chunk": null,
  "next_candidate_chunk": null,
  "active_chunk": null,
  "active_pr": null,
  "completed_chunks": [],
  "blocked_chunks": []
}

Do not put verbose history inside progress.json.

next_candidate_chunk is a HINT only.

Never blindly execute it.

Always recompute eligibility after synchronizing master.

======================================================================
AS. CHUNK MANIFEST
======================================================================

Every implementation chunk gets:

docs/planning/chunks/<CHUNK-ID>.md

Include structured metadata similar to:

---
id: ZE-PXX-CXX
title: ...
status: READY
sequence: ...
requirements:
  - ...
dependencies:
  - ...
required_context:
  - ...
required_skills:
  - ...
optional_skills:
  - ...
affected_areas:
  - ...
execution:
  base_master_sha: null
  branch: null
  commit: null
  pr: null
---

Then document:

Objective

In Scope

Explicitly Out of Scope

Requirements Served

Domain Objects

Application Services

API Contracts

Frontend Components where relevant

Authorization Rules

Expected Files/Modules

Acceptance Criteria

Required Tests

Verification

Review Requirements

Completion/Handoff

Every chunk must be self-contained enough that a fresh Codex context can perform it.

======================================================================
AT. CHUNK DECOMPOSITION PRINCIPLE
======================================================================

Break the entire launch product into the smallest reasonably independent coherent chunks.

Optimize for:

- low coupling
- low context requirements
- independent review
- independent tests
- clean PRs
- predictable rollback
- minimum cross-chunk assumptions

Do not optimize for maximum chunk count.

A good chunk has:

- one primary responsibility
- observable output
- clear acceptance criteria
- bounded files/modules
- testable behavior

Before finalizing every proposed chunk ask:

1. Can this be independently implemented?
2. Can this be independently reviewed?
3. Can this be independently tested?
4. Does it unnecessarily mix frontend/backend/infrastructure concerns?
5. Can coupling to unfinished chunks be reduced?
6. Would splitting further create genuine independence or only administrative overhead?
7. Does it have all required architecture already defined?
8. Is anything in it outside the locked product requirements?

Prefer separating backend foundation/API work from frontend consumption when this genuinely
reduces dependency and review complexity.

But do not create artificial tiny chunks that cannot produce meaningful verified progress.

======================================================================
AU. DEPENDENCY GRAPH
======================================================================

Create:

docs/planning/DEPENDENCY_GRAPH.md

Model every chunk dependency.

Where several chunks can safely proceed independently after shared foundations, make that
explicit.

Never make an unnecessary linear sequence.

The planner should deliberately minimize critical-path coupling.

======================================================================
AV. "NEXT CHUNK" PROTOCOL
======================================================================

After the planning PR has been approved and merged, a future fresh Codex session may
receive only:

    next chunk

That must be sufficient.

Execute exactly:

PHASE 1 — INITIALIZE

Read AGENTS.md startup rules.

PHASE 2 — SYNCHRONIZE

git fetch origin
git checkout master
git pull --ff-only origin master

Verify:
- correct repository
- expected remote
- clean master
- no divergence that prevents fast-forward

If synchronization fails:
STOP.

Do not destructively repair Git state.

PHASE 3 — RECONCILE

Read:
- memory/progress.json
- relevant chunk manifests
- Git history where required

Determine:
- current master SHA
- effectively completed chunks
- unresolved PR_OPEN chunks
- blocked chunks
- dependency satisfaction

Do not modify master.

PHASE 4 — SELECT

Eligible chunk:

status/effective state allows READY
AND
all dependencies effectively COMPLETE
AND
no blocker exists.

Select by deterministic sequence/priority.

Do not improvise another task because it looks attractive.

PHASE 5 — LOAD CONTEXT

Read ONLY:

- selected chunk manifest
- required context declared by that chunk
- required skills declared by that chunk
- directly relevant implementation files

Load optional skills/context only if objectively necessary.

Do not read the entire project documentation without need.

PHASE 6 — BRANCH

Create:

feature/<chunk-id-lowercase>-<slug>

from freshly synchronized master.

Record:

base_master_sha

Never branch from the previous feature branch.

Never build dependent work on an unmerged PR.

PHASE 7 — IMPLEMENT

Implement EXACTLY one chunk.

Follow:
- locked architecture
- OOP/domain model
- interfaces
- code blueprint
- frontend/backend mapping
- API contracts
- role boundaries
- skill instructions

No unrelated refactoring.

No next-chunk implementation.

PHASE 8 — VERIFY

Run appropriate:

- unit tests
- domain tests
- service tests
- authorization tests
- API tests
- persistence tests
- integration adapter tests
- frontend tests
- accessibility checks
- type checking
- lint
- build
- relevant regression suite

PHASE 9 — INDEPENDENT REVIEW

Spawn at least one independent reviewer agent.

PHASE 10 — FIX

Resolve all Critical and High findings.

Re-run required checks.

PHASE 11 — MEMORY/STATE

Update only information future chunks need.

Set current chunk to PR_OPEN before handoff.

Do NOT mark it COMPLETE.

PHASE 12 — GIT

commit
push feature branch to origin
open PR targeting master

PHASE 13 — STOP

Do not start another chunk.

Do not merge.

Human reviews and merges remotely.

======================================================================
AW. HANDLING AN UNMERGED PREVIOUS PR
======================================================================

If previous chunk remains PR_OPEN and is absent from master:

It is NOT COMPLETE.

If next chunk depends on it:
do not start the dependent chunk.

If an independent READY chunk exists and deterministic plan permits it:
that independent chunk may proceed.

Never branch dependent work from the unmerged feature branch.

======================================================================
AX. GIT CONVENTIONS
======================================================================

Default branch:

master

Feature branches:

feature/<chunk-id-lowercase>-<slug>

Example:

feature/ze-p04-c03-teacher-scheduling

Commit convention:

feat(ZE-P04-C03): ...
fix(ZE-P04-C03): ...
test(ZE-P04-C03): ...
docs(ZE-P04-C03): ...

Use the chunk ID consistently so Git history can assist state reconciliation.

At handoff:

git push -u origin <branch>

Create PR targeting:

master

Never merge the PR.

======================================================================
AY. INDEPENDENT REVIEW AGENTS
======================================================================

Every implementation chunk must be independently reviewed.

The primary reviewer must read:

- AGENTS.md
- active chunk
- requirements
- relevant architecture
- relevant skills
- branch diff
- tests

Review specifically for:

- exact requirement coverage
- architecture compliance
- OOP/domain compliance
- reuse
- duplicate logic
- improper coupling
- scope creep
- scope erosion
- authorization
- family ownership
- teacher assignment boundaries
- financial information leakage
- security
- data validation
- regression risk
- testing adequacy
- maintainability
- unnecessary complexity

Classify:

Critical
High
Medium
Low

Critical and High findings must be resolved before PR handoff.

Use additional specialist agents when justified.

Examples:

Security-sensitive authorization chunk:
- security reviewer
- backend/domain reviewer

Complex frontend chunk:
- frontend architecture reviewer
- accessibility reviewer

Database migration:
- persistence/data reviewer

Integration:
- integration/security reviewer

Do not spawn unnecessary agents for trivial changes.

======================================================================
AZ. REVIEW AGENT MUST CHECK BLUEPRINT DEVIATION
======================================================================

Every reviewer must explicitly answer:

1. Does implementation match the locked chunk scope?
2. Does implementation match the Code Blueprint?
3. Does implementation preserve the documented object model?
4. Did the agent introduce an undocumented durable class/service/API/component?
5. Did the implementation duplicate reusable behavior?
6. Did it implement functionality belonging to another chunk?
7. Did it remove/defer part of a launch requirement?
8. Did it weaken authorization?
9. Is every acceptance criterion proven?
10. Is the PR safe for human review?

======================================================================
BA. REUSE REQUIREMENT
======================================================================

Code reuse is a core engineering objective.

During planning identify reusable:

- domain policies
- value objects
- application interfaces
- repositories
- integration abstractions
- request/response contracts
- frontend UI primitives
- domain frontend components
- validation
- error handling
- authentication/session plumbing
- authorization helpers
- testing factories/fixtures

Reuse must not create inappropriate coupling.

Do not make a universal abstraction merely to remove two similar lines.

Prefer meaningful domain reuse.

======================================================================
BB. TESTING ARCHITECTURE
======================================================================

Design testing before implementation.

Document:

- domain unit testing
- application service testing
- repository testing
- API integration testing
- authorization negative testing
- database migration testing
- provider adapter testing
- frontend component testing
- user-flow testing
- accessibility testing
- end-to-end critical paths
- regression strategy

Critical authorization tests must include negative cases.

Examples:

Teacher tries to read payment → denied.

Teacher tries to read unrelated student → denied.

Parent tries to read another family's child → denied.

Student tries to read another student's submission → denied.

Student tries to access billing → denied.

Browser/client manipulation must not bypass these rules.

======================================================================
BC. LAUNCH ACCEPTANCE GATE
======================================================================

Create:

docs/product/LAUNCH_ACCEPTANCE_CRITERIA.md

The project is not considered finished merely because every feature PR merged.

Define a final production launch gate requiring appropriate:

- 100% locked launch requirements mapped
- 100% required launch requirements implemented
- no uncovered requirements
- requirement traceability verified
- no unresolved Critical findings
- no unresolved High findings
- security checks
- authorization checks
- frontend/backend mapping consistency
- migrations
- integration validation
- backup/restore validation
- production configuration review
- deployment validation
- smoke testing
- critical end-to-end journeys
- accessibility checks
- operational documentation
- rollback/recovery readiness

======================================================================
BD. SCOPE LOCK
======================================================================

Create:

docs/product/SCOPE_LOCK.md

During planning:

STATUS: DRAFT

Once the bootstrap plan is human-reviewed and merged:

STATUS: LOCKED
SCOPE_VERSION: 1.0

After LOCKED, future implementation agents must not modify launch scope.

A scope change requires explicit human instruction identifying that the scope is being
changed.

Create a formal scope-change process.

Do not infer a scope change from an implementation inconvenience.

======================================================================
BE. AGENTS.md
======================================================================

Create AGENTS.md as the permanent operating constitution.

It must concisely encode:

- authority hierarchy
- scope lock
- remote-master synchronization
- read-only master reconciliation
- deterministic next-chunk selection
- one-chunk-only execution
- OOP architecture enforcement
- Code Blueprint enforcement
- reuse requirement
- automatic skill routing
- authorization rules
- test requirements
- independent review
- state update
- PR-only handoff
- human remote merge
- STOP condition

Authority order should approximately be:

1. SCOPE_LOCK / LAUNCH_SCOPE
2. FUNCTIONAL + NON-FUNCTIONAL requirements
3. accepted architectural decisions
4. CODE_BLUEPRINT
5. architecture documents
6. API/frontend-backend contracts
7. chunk manifest
8. engineering skills/standards
9. existing implementation
10. conversational assumptions

No conversation history should silently override locked repository authority.

======================================================================
BF. INITIAL PLANNING EXECUTION ORDER
======================================================================

During THIS bootstrap run, perform planning in this order:

STAGE 1
Understand launch product.

STAGE 2
Create complete functional and non-functional requirement inventory.

STAGE 3
Create role capabilities and data boundaries.

STAGE 4
Perform requirement-gap analysis.

STAGE 5
Design domain model and aggregates.

STAGE 6
Design backend object catalog.

STAGE 7
Design application service/use-case catalog.

STAGE 8
Design ports/repositories.

STAGE 9
Design persistence/data model.

STAGE 10
Design authorization/security model.

STAGE 11
Design integrations.

STAGE 12
Design complete API catalog.

STAGE 13
Independently review BACKEND design.

Resolve material findings BEFORE proceeding to final frontend architecture.

STAGE 14
Design frontend information architecture.

STAGE 15
Design frontend route/component catalog.

STAGE 16
Produce mandatory frontend-backend mapping.

STAGE 17
Produce consolidated Code Blueprint.

STAGE 18
Design engineering/testing/deployment standards.

STAGE 19
Create skills.

STAGE 20
Create memory/state system.

STAGE 21
Create implementation phases/dependency graph.

STAGE 22
Decompose the ENTIRE launch product into small chunks.

STAGE 23
Map all requirements to chunks.

STAGE 24
Perform chunk-granularity review.

STAGE 25
Perform dependency/coupling review.

STAGE 26
Perform scope-completeness review.

STAGE 27
Perform architecture consistency review.

STAGE 28
Perform authorization/data-boundary review.

STAGE 29
Perform fresh-context simulation:

Pretend conversation history does not exist.

Verify whether an agent receiving only:

    next chunk

can safely:
- synchronize repository
- recover state
- choose correct chunk
- load correct context
- load correct skills
- implement only the task
- verify it
- push PR
- stop

STAGE 30
Resolve all material planning findings.

STAGE 31
Finalise planning documents.

DO NOT implement product functionality.

======================================================================
BG. PLANNING REVIEW AGENTS
======================================================================

Before finalising, use independent reviewers.

At minimum review:

PRODUCT REVIEW
Check whether the complete launch product is represented.

BACKEND/OOP REVIEW
Check domain boundaries, services, reuse, interfaces, coupling, persistence separation.

FRONTEND REVIEW
Check that every screen/feature has backend/API support and reuse is appropriate.

SECURITY/AUTHORIZATION REVIEW
Check Admin, Teacher, Parent, Student boundaries and child/family data.

CHUNK REVIEW
Check granularity, independence, dependency accuracy and complete requirement coverage.

STATE/WORKFLOW REVIEW
Check remote-master synchronization, PR_OPEN/COMPLETE reconciliation and fresh-context
continuation.

Resolve Critical and High planning findings.

Resolve material Medium findings where practical before human review.

======================================================================
BH. PLANNING MUST NOT LEAVE "TBD" IMPLEMENTATION HOLES
======================================================================

Avoid vague architecture placeholders such as:

"Implement suitable service later."

"Decide database model while coding."

"Frontend will call appropriate endpoint."

"Add authorization as needed."

"Use relevant components."

Core product behavior must be designed before scope lock.

Where a genuine external/human business decision remains unavoidable, document it explicitly
as a BLOCKER rather than silently leaving architecture undefined.

======================================================================
BI. INITIAL GIT WORKFLOW
======================================================================

This bootstrap run itself must follow the intended workflow.

First:

git fetch origin
git checkout master
git pull --ff-only origin master

Do not modify master.

Create:

feature/project-bootstrap-planning

Perform all planning/bootstrap work there.

Commit.

Push to origin.

Create PR against master if GitHub tooling/credentials are available.

DO NOT MERGE.

The human will review and merge remotely.

======================================================================
BJ. INITIAL REPOSITORY MEMORY
======================================================================

After planning, initialise compact state.

PROJECT_STATE should contain only:

- project name
- scope status/version
- architecture version
- current phase
- current execution status
- next candidate
- blockers
- critical constraints
- test baseline if applicable

ARCHITECTURE_SNAPSHOT should summarise:

- frontend
- backend
- domain style
- persistence
- integrations
- role model
- deployment

Do not duplicate full architecture.

======================================================================
BK. PR TEMPLATE
======================================================================

Create an implementation PR template containing:

Chunk
Requirements
Objective
Implemented
Explicitly not changed
Authorization impact
Architecture impact
Tests
Verification
Independent review findings
State
Base master SHA
Human action

Human action must say:

Review and merge into master if approved.

Never tell the implementation agent to merge automatically.

======================================================================
BL. FINAL BOOTSTRAP VALIDATION
======================================================================

Before opening the planning PR verify:

- Launch scope is complete.
- Out-of-scope is explicit.
- Parent/Student/Teacher/Admin boundaries are unambiguous.
- Student name and age are required.
- Student school is optional.
- Backend architecture is fully designed before frontend.
- OOP/domain rules are documented.
- Important backend objects are catalogued.
- Important service operations are catalogued.
- Repository/port interfaces are catalogued.
- APIs are mapped.
- Frontend routes are mapped.
- Frontend components are mapped.
- Frontend-to-backend mapping exists.
- Code Blueprint exists.
- Every requirement has a chunk.
- Every chunk has requirements.
- Dependency graph is consistent.
- Chunks are reasonably independent.
- Skills exist.
- Skill routing exists.
- State reconciliation exists.
- Remote master is authoritative.
- Master is never modified by an agent.
- PR_OPEN and COMPLETE are distinguished.
- Fresh-session "next chunk" behavior is viable.
- Human remains the only normal merge authority.
- No product code has been implemented.

======================================================================
BM. FINAL RESPONSE FOR THIS RUN
======================================================================

Do not dump all generated Markdown into the conversation.

Report only:

PLANNING STATUS:
SCOPE STATUS:
SCOPE VERSION:
ARCHITECTURE VERSION:
TOTAL LAUNCH REQUIREMENTS:
PHASE COUNT:
CHUNK COUNT:
REQUIREMENT COVERAGE:
MASTER SHA USED:
BRANCH:
COMMIT:
PR:
BACKEND/OOP REVIEW:
FRONTEND MAPPING REVIEW:
SECURITY REVIEW:
CHUNK REVIEW:
STATE WORKFLOW REVIEW:
CRITICAL FINDINGS REMAINING:
HIGH FINDINGS REMAINING:
BLOCKERS:

Then confirm:

APPLICATION IMPLEMENTATION STARTED: NO

and:

NEXT HUMAN ACTION:
Review the planning/bootstrap PR carefully and merge it into master only if the scope,
architecture, object model, frontend/backend mapping and chunk plan are approved.

After that merge, a completely fresh Codex session must be able to execute:

    next chunk

without requiring previous conversational context.

STOP.