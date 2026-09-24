# Backend object catalog

Status: DRAFT, scope 1.0 / architecture 2. Canonical structured contracts: [backend-catalog.json](backend-catalog.json). These are design contracts, not implemented classes or endpoints. Implementation ownership and requirement traceability are in CODE_BLUEPRINT.md and docs/planning/REQUIREMENT_TRACEABILITY.md.

## Account

- **Type:** aggregate
- **Module:** identity
- **Responsibility:** One principal role; staff MFA; student email nullable; suspended/closed accounts cannot authenticate
- **Attributes:** id:uuid;role:RoleGrant;status:AccountStatus;email:NormalizedEmail?;display_name:string;version:int
- **Invariants:** One principal role; staff MFA; student email nullable; suspended/closed accounts cannot authenticate
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Credential, Session, RoleGrant
- **Collaborators:** Credential, Session, RoleGrant
- **Persistence:** accounts
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011
- **Chunks:** ZE-P02-C01, ZE-P02-C03, ZE-P02-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| activate | Activate | verified_at:Instant | AccountActivated | InvalidState, InvariantViolation, VersionConflict |
| suspend | Suspend | reason:Reason | SessionsRevoked | InvalidState, InvariantViolation, VersionConflict |
| close | Close | decision:RetentionDecision | AccountClosed | InvalidState, InvariantViolation, VersionConflict |

## Credential

- **Type:** entity
- **Module:** identity
- **Responsibility:** Only Argon2id hashes; no plaintext persistence; breached password rejected before hash
- **Attributes:** user_id:uuid;password_hash:string;changed_at:Instant;failed_attempts:int
- **Invariants:** Only Argon2id hashes; no plaintext persistence; breached password rejected before hash
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Account
- **Collaborators:** Account
- **Persistence:** credentials
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| replace | Replace | hash:PasswordHash,now:Instant | CredentialChanged | InvalidState, InvariantViolation, VersionConflict |
| verify_attempt | Verify attempt | outcome:bool,now:Instant | LockoutDecision | InvalidState, InvariantViolation, VersionConflict |

## Session

- **Type:** entity
- **Module:** identity
- **Responsibility:** Opaque rotating token, absolute/idle expiry; revoked cannot be resumed
- **Attributes:** id:uuid;user_id:uuid;token_hash:string;expires_at:Instant;revoked_at:Instant?;mfa_verified_at:Instant?
- **Invariants:** Opaque rotating token, absolute/idle expiry; revoked cannot be resumed
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Account
- **Collaborators:** Account
- **Persistence:** sessions
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| rotate | Rotate | new_hash:TokenHash,now:Instant | SessionRotated | InvalidState, InvariantViolation, VersionConflict |
| revoke | Revoke | now:Instant | None | InvalidState, InvariantViolation, VersionConflict |
| is_active | Is active | now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |

## RoleGrant

- **Type:** value object
- **Module:** identity
- **Responsibility:** Teacher principal cannot also have admin privileges; privileges only approved closed enum
- **Attributes:** role:Role;admin_privileges:frozenset[Privilege]
- **Invariants:** Teacher principal cannot also have admin privileges; privileges only approved closed enum, RoleGrant is owned by Account; RoleGrantView.version is Account.version, never a separate counter.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Account
- **Collaborators:** Account
- **Persistence:** accounts.admin_privileges
- **Requirements:** ADM-006
- **Chunks:** ZE-P02-C01, ZE-P02-C03, ZE-P02-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| allows | Allows | capability:Privilege | bool | InvalidState, InvariantViolation, VersionConflict |
| validate_change | Validate change | actor:Principal,requested:RoleGrant | RoleGrant | InvalidState, InvariantViolation, VersionConflict |

## Guardian

- **Type:** entity
- **Module:** family
- **Responsibility:** Adult contact tied to verified account; no exact birthday collection
- **Attributes:** id:uuid;user_id:uuid;family_id:uuid;first_name:string;last_name:string?;phone:E164?;optional_email:bool
- **Invariants:** Adult contact tied to verified account; no exact birthday collection
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Account, Family
- **Collaborators:** Account, Family
- **Persistence:** guardians
- **Requirements:** AUTH-011, PAR-002, PAR-021, STU-019
- **Chunks:** ZE-P02-C03, ZE-P02-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| update_contact | Update contact | name:Name,phone:E164? | GuardianUpdated | InvalidState, InvariantViolation, VersionConflict |
| set_preferences | Set preferences | optional_email:bool | PreferencesChanged | InvalidState, InvariantViolation, VersionConflict |

## Family

- **Type:** aggregate
- **Module:** family
- **Responsibility:** Family relationship does not imply each guardian can access every sibling; active child needs at least one verified guardian
- **Attributes:** id:uuid;guardians:Guardian[];links:GuardianStudent[];billing_members:BillingMembership[];version:int
- **Invariants:** Family relationship does not imply each guardian can access every sibling; active child needs at least one verified guardian
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Guardian, GuardianStudent, BillingMembership, StudentProfile
- **Collaborators:** Guardian, GuardianStudent, BillingMembership, StudentProfile
- **Persistence:** families
- **Requirements:** PAR-006
- **Chunks:** ZE-P02-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| link_guardian | Link guardian | link:GuardianStudent,evidence:VerificationRef | GuardianLinked | InvalidState, InvariantViolation, VersionConflict |
| revoke_link | Revoke link | guardian_id:uuid,student_id:uuid,reason:Reason | GuardianRevoked | InvalidState, InvariantViolation, VersionConflict |
| grant_billing | Grant billing | member:BillingMembership | BillingGranted | InvalidState, InvariantViolation, VersionConflict |

## GuardianStudent

- **Type:** entity
- **Module:** family
- **Responsibility:** Guardian and child share family; unique active pair; verification required; immediate revocation
- **Attributes:** guardian_id:uuid;student_id:uuid;family_id:uuid;verified_at:Instant;revoked_at:Instant?;verification_reference:string;version:int
- **Invariants:** Guardian and child share family; unique active pair; verification required; immediate revocation
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Guardian, StudentProfile
- **Collaborators:** Guardian, StudentProfile
- **Persistence:** guardian_students
- **Requirements:** PAR-006
- **Chunks:** ZE-P02-C03, ZE-P02-C05, ZE-P08-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| is_active | Is active | now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |
| revoke | Revoke | reason:Reason,now:Instant | GuardianLinkRevoked | InvalidState, InvariantViolation, VersionConflict |

## BillingMembership

- **Type:** entity
- **Module:** family
- **Responsibility:** Explicit financial visibility independent of child guardianship; primary verified parent receives initial membership
- **Attributes:** family_id:uuid;guardian_id:uuid;granted_at:Instant;revoked_at:Instant?;approval_reference:string;version:int
- **Invariants:** Explicit financial visibility independent of child guardianship; primary verified parent receives initial membership
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Family, Guardian
- **Collaborators:** Family, Guardian
- **Persistence:** billing_memberships
- **Requirements:** AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016
- **Chunks:** ZE-P02-C03, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| revoke | Revoke | reason:Reason,now:Instant | BillingAccessRevoked | InvalidState, InvariantViolation, VersionConflict |
| permits | Permits | family_id:uuid | bool | InvalidState, InvariantViolation, VersionConflict |

## StudentProfile

- **Type:** aggregate
- **Module:** family
- **Responsibility:** Name and age required; school/last/preferred names nullable; no diagnoses/DOB/child email required
- **Attributes:** id:uuid;family_id:uuid;first_name:string;preferred_name:string?;last_name:string?;age:AgeSnapshot;school_name:string?;school_year:string?;interests:tuple[str];prior_experience:Experience?;status:StudentStatus
- **Invariants:** Name and age required; school/last/preferred names nullable; no diagnoses/DOB/child email required
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** AgeSnapshot, GuardianStudent
- **Collaborators:** AgeSnapshot, GuardianStudent
- **Persistence:** students
- **Requirements:** ADM-004, PAR-005, TCH-009
- **Chunks:** ZE-P02-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| update_profile | Update profile | changes:StudentProfileChange | StudentUpdated | InvalidState, InvariantViolation, VersionConflict |
| reconfirm_age | Reconfirm age | age:int,as_of:LocalDate | AgeReconfirmed | InvalidState, InvariantViolation, VersionConflict |
| archive | Archive | reason:Reason | StudentArchived | InvalidState, InvariantViolation, VersionConflict |

## AgeSnapshot

- **Type:** value object
- **Module:** family
- **Responsibility:** No inferred DOB; age value valid in technical range; >180 days stale for new checkout
- **Attributes:** years:int;recorded_on:LocalDate
- **Invariants:** No inferred DOB; age value valid in technical range; >180 days stale for new checkout
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** StudentProfile
- **Collaborators:** StudentProfile
- **Persistence:** students.age_years+age_recorded_on
- **Requirements:** ADM-004, PAR-005, TCH-009
- **Chunks:** ZE-P02-C03, ZE-P06-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| requires_reconfirmation | Requires reconfirmation | today:LocalDate | bool | InvalidState, InvariantViolation, VersionConflict |
| meets_band | Meets band | min_age:int,max_age:int | bool | InvalidState, InvariantViolation, VersionConflict |

## TeacherProfile

- **Type:** aggregate
- **Module:** identity
- **Responsibility:** Public publication deliberate; no operational contacts exposed; archive needs no live assignment
- **Attributes:** id:uuid;user_id:uuid;display_name:string;biography:string?;public_photo_asset_id:uuid?;published:bool;status:TeacherStatus
- **Invariants:** Public publication deliberate; no operational contacts exposed; archive needs no live assignment
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Account, TeacherAssignment
- **Collaborators:** Account, TeacherAssignment
- **Persistence:** teacher_profiles
- **Requirements:** ADM-005, WEB-006
- **Chunks:** ZE-P02-C03, ZE-P02-C04, ZE-P03-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| update_public_profile | Update public profile | profile:PublicTeacherDraft | TeacherUpdated | InvalidState, InvariantViolation, VersionConflict |
| publish | Publish | approved:bool | TeacherPublished | InvalidState, InvariantViolation, VersionConflict |
| archive | Archive | no_active_assignments:bool | TeacherArchived | InvalidState, InvariantViolation, VersionConflict |

## PolicyDocument

- **Type:** aggregate
- **Module:** content
- **Responsibility:** Published versions immutable; required acknowledgement only effective approved versions
- **Attributes:** id:uuid;key:PolicyKey;version_label:string;html:SanitizedHtml;effective_at:Instant;approval_reference:string?;published_at:Instant?
- **Invariants:** Published versions immutable; required acknowledgement only effective approved versions
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** PolicyAcknowledgement
- **Collaborators:** PolicyAcknowledgement
- **Persistence:** policy_documents
- **Requirements:** WEB-010
- **Chunks:** ZE-P02-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| publish | Publish | approval:ApprovalReference,now:Instant | PolicyPublished | InvalidState, InvariantViolation, VersionConflict |

## PolicyAcknowledgement

- **Type:** entity
- **Module:** family
- **Responsibility:** Immutable attributable version-specific evidence; scope linked guardian child only
- **Attributes:** id:uuid;policy_id:uuid;guardian_id:uuid;family_id:uuid;student_id:uuid?;acknowledged_at:Instant
- **Invariants:** Immutable attributable version-specific evidence; scope linked guardian child only
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** PolicyDocument, Guardian
- **Collaborators:** PolicyDocument, Guardian
- **Persistence:** policy_acknowledgements
- **Requirements:** PAR-004, SEC-003
- **Chunks:** ZE-P02-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| covers | Covers | policy_id:uuid,student_id:uuid? | bool | InvalidState, InvariantViolation, VersionConflict |

## PublicPage

- **Type:** aggregate
- **Module:** content
- **Responsibility:** Fixed approved page catalog; sanitize content; draft never public
- **Attributes:** slug:PublicPageSlug;title:string;draft:SanitizedHtml;published_revision_id:uuid?
- **Invariants:** Fixed approved page catalog; sanitize content; draft never public
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** PublicationPolicy
- **Collaborators:** PublicationPolicy
- **Persistence:** public_pages+public_page_revisions
- **Requirements:** WEB-001, WEB-002, WEB-007, WEB-008, WEB-012
- **Chunks:** ZE-P03-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| save_draft | Save draft | content:PageDraft | PageDraftSaved | InvalidState, InvariantViolation, VersionConflict |
| publish | Publish | now:Instant | PagePublished | InvalidState, InvariantViolation, VersionConflict |

## ContactEnquiry

- **Type:** aggregate
- **Module:** content
- **Responsibility:** No child linking from untrusted public text; bounded content; restricted operations retention
- **Attributes:** id:uuid;name:string;email:NormalizedEmail;message:string;status:EnquiryStatus
- **Invariants:** No child linking from untrusted public text; bounded content; restricted operations retention
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Notification
- **Collaborators:** Notification
- **Persistence:** contact_enquiries
- **Requirements:** WEB-009
- **Chunks:** ZE-P03-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| mark_handled | Mark handled | now:Instant | EnquiryHandled | InvalidState, InvariantViolation, VersionConflict |

## Program

- **Type:** aggregate
- **Module:** curriculum
- **Responsibility:** Optional course grouping; archive retains referenced courses
- **Attributes:** id:uuid;slug:Slug;title:string;summary:string;status:PublicationStatus
- **Invariants:** Optional course grouping; archive retains referenced courses
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Course
- **Collaborators:** Course
- **Persistence:** programs
- **Requirements:** ADM-007, LRN-001, PAR-007, WEB-003, WEB-004
- **Chunks:** ZE-P03-C01, ZE-P03-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| update | Update | title:string,summary:string | ProgramUpdated | InvalidState, InvariantViolation, VersionConflict |
| publish | Publish | none | ProgramPublished | InvalidState, InvariantViolation, VersionConflict |
| archive | Archive | none | ProgramArchived | InvalidState, InvariantViolation, VersionConflict |

## Course

- **Type:** aggregate
- **Module:** curriculum
- **Responsibility:** Reusable content, no session schedule; public course needs ready published revision
- **Attributes:** id:uuid;program_id:uuid?;slug:Slug;title:string;age_band:AgeBand;duration_weeks:int;current_revision_id:uuid?;status:PublicationStatus
- **Invariants:** Reusable content, no session schedule; public course needs ready published revision
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Program, CurriculumRevision
- **Collaborators:** Program, CurriculumRevision
- **Persistence:** courses
- **Requirements:** ADM-007, LRN-001, PAR-007, WEB-003, WEB-004
- **Chunks:** ZE-P03-C01, ZE-P03-C02, ZE-P06-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| publish | Publish | revision:CurriculumRevision | CoursePublished | InvalidState, InvariantViolation, VersionConflict |
| revise_metadata | Revise metadata | changes:CourseMetadata | CourseUpdated | InvalidState, InvariantViolation, VersionConflict |
| archive | Archive | none | CourseArchived | InvalidState, InvariantViolation, VersionConflict |

## CurriculumRevision

- **Type:** aggregate
- **Module:** curriculum
- **Responsibility:** Published content immutable; stable reference IDs belong to same revision; cohort pin cannot be silently upgraded
- **Attributes:** id:uuid;course_id:uuid;number:int;status:RevisionStatus;modules:CourseModule[];resources:LearningResource[]
- **Invariants:** Published content immutable; stable reference IDs belong to same revision; cohort pin cannot be silently upgraded
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** CourseModule, Lesson, LessonBlock, LearningResource, Quiz, Assignment
- **Collaborators:** CourseModule, Lesson, LessonBlock, LearningResource, Quiz, Assignment
- **Persistence:** curriculum_revisions
- **Requirements:** ADM-008, ADM-011, ASM-004, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003
- **Chunks:** ZE-P03-C02, ZE-P03-C03, ZE-P03-C04, ZE-P05-C01, ZE-P07-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| add_module | Add module | module:CourseModule | ModuleAdded | InvalidState, InvariantViolation, VersionConflict |
| reorder | Reorder | ids:tuple[uuid] | RevisionReordered | InvalidState, InvariantViolation, VersionConflict |
| publish | Publish | report:PublicationReport | RevisionPublished | InvalidState, InvariantViolation, VersionConflict |
| clone | Clone | new_id:uuid | CurriculumRevision | InvalidState, InvariantViolation, VersionConflict |

## CourseModule

- **Type:** entity
- **Module:** curriculum
- **Responsibility:** Position unique in revision; module release offset nonnegative; mutates through draft revision
- **Attributes:** id:uuid;revision_id:uuid;title:string;position:int;release_offset_days:int;lessons:Lesson[]
- **Invariants:** Position unique in revision; module release offset nonnegative; mutates through draft revision
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** CurriculumRevision, Lesson
- **Collaborators:** CurriculumRevision, Lesson
- **Persistence:** course_modules
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003
- **Chunks:** ZE-P03-C03, ZE-P03-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| rename | Rename | title:string | None | InvalidState, InvariantViolation, VersionConflict |
| move | Move | position:int | None | InvalidState, InvariantViolation, VersionConflict |
| add_lesson | Add lesson | lesson:Lesson | None | InvalidState, InvariantViolation, VersionConflict |

## Lesson

- **Type:** entity
- **Module:** curriculum
- **Responsibility:** Ordered within module; release >= module gate; mutation through draft revision
- **Attributes:** id:uuid;module_id:uuid;title:string;position:int;release_offset_days:int;required_for_completion:bool;blocks:LessonBlock[]
- **Invariants:** Ordered within module; release >= module gate; mutation through draft revision
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** LessonBlock, CourseModule
- **Collaborators:** LessonBlock, CourseModule
- **Persistence:** lessons
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003
- **Chunks:** ZE-P03-C03, ZE-P03-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| replace_blocks | Replace blocks | blocks:tuple[LessonBlock] | None | InvalidState, InvariantViolation, VersionConflict |
| set_release | Set release | offset:int | None | InvalidState, InvariantViolation, VersionConflict |

## LessonBlock

- **Type:** discriminated value composition
- **Module:** curriculum
- **Responsibility:** Exactly typed payload per kind; sanitize rich text; accessible image/video; references same revision
- **Attributes:** id:uuid;lesson_id:uuid;position:int;kind:BlockKind;content:BlockContent;required_for_completion:bool
- **Invariants:** Exactly typed payload per kind; sanitize rich text; accessible image/video; references same revision
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Lesson, LearningResource, Quiz, Assignment
- **Collaborators:** Lesson, LearningResource, Quiz, Assignment
- **Persistence:** lesson_blocks
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003
- **Chunks:** ZE-P03-C03, ZE-P03-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| validate | Validate | context:RevisionReferences | ValidationResult | InvalidState, InvariantViolation, VersionConflict |
| referenced_assets | Referenced assets | none | frozenset[uuid] | InvalidState, InvariantViolation, VersionConflict |

## LearningResource

- **Type:** entity
- **Module:** curriculum
- **Responsibility:** Exactly one scanned asset or approved HTTPS resource; immutable after revision published
- **Attributes:** id:uuid;revision_id:uuid;title:string;kind:ResourceKind;asset_id:uuid?;external_url:ApprovedUrl?;status:ResourceStatus
- **Invariants:** Exactly one scanned asset or approved HTTPS resource; immutable after revision published
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** FileAsset, CurriculumRevision
- **Collaborators:** FileAsset, CurriculumRevision
- **Persistence:** learning_resources
- **Requirements:** ADM-009, LRN-005, STU-005
- **Chunks:** ZE-P03-C03, ZE-P03-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| replace_source | Replace source | source:ResourceSource | None | InvalidState, InvariantViolation, VersionConflict |
| validate_ready | Validate ready | asset:FileAsset? | ValidationResult | InvalidState, InvariantViolation, VersionConflict |

## Cohort

- **Type:** aggregate
- **Module:** delivery
- **Responsibility:** Scheduled delivery of one published pinned revision; cannot reduce seats below holds+active; fees external
- **Attributes:** id:uuid;course_id:uuid;revision_id:uuid;capacity:int;status:CohortStatus;timezone:IanaZone;starts_at:Instant;ends_at:Instant;enrolment_window:TimeRange
- **Invariants:** Scheduled delivery of one published pinned revision; cannot reduce seats below holds+active; fees external
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Course, CurriculumRevision, ClassSession, Enrolment
- **Collaborators:** Course, CurriculumRevision, ClassSession, Enrolment
- **Persistence:** cohorts
- **Requirements:** ADM-013, ADM-015, ADM-016, ADM-017, ADM-018, ADM-019, AUTH-010, CLS-001, CLS-005, NFR-012
- **Chunks:** ZE-P03-C01, ZE-P05-C01, ZE-P05-C02, ZE-P06-C01, ZE-P06-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| open | Open | ready:LaunchReadiness | CohortOpened | InvalidState, InvariantViolation, VersionConflict |
| change_capacity | Change capacity | capacity:int,committed:int | CapacityChanged | InvalidState, InvariantViolation, VersionConflict |
| transition | Transition | status:CohortStatus | CohortChanged | InvalidState, InvariantViolation, VersionConflict |
| cancel | Cancel | reason:Reason | CohortCancelled | InvalidState, InvariantViolation, VersionConflict |

## ClassSession

- **Type:** aggregate
- **Module:** delivery
- **Responsibility:** One occurrence; UTC end>start; no independent external calendar authority; cancelled cannot join
- **Attributes:** id:uuid;cohort_id:uuid;lesson_id:uuid?;starts_at:Instant;ends_at:Instant;timezone:IanaZone;local_start:LocalDateTime;utc_offset_minutes:int;status:SessionStatus;version:int
- **Invariants:** One occurrence; UTC end>start; no independent external calendar authority; cancelled cannot join
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Cohort, TeacherAssignment, IntegrationBinding
- **Collaborators:** Cohort, TeacherAssignment, IntegrationBinding
- **Persistence:** class_sessions
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011, PAR-009, STU-013, TCH-005, TCH-006, WEB-005
- **Chunks:** ZE-P05-C02, ZE-P05-C03, ZE-P05-C04, ZE-P05-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| reschedule | Reschedule | slot:TimeSlot,permit:SchedulePermit | SessionRescheduled | InvalidState, InvariantViolation, VersionConflict |
| cancel | Cancel | reason:Reason | SessionCancelled | InvalidState, InvariantViolation, VersionConflict |
| complete | Complete | now:Instant | SessionCompleted | InvalidState, InvariantViolation, VersionConflict |

## TeacherAssignment

- **Type:** entity
- **Module:** delivery
- **Responsibility:** Session belongs to cohort; teacher active; grants education only; revocation immediate
- **Attributes:** id:uuid;teacher_id:uuid;cohort_id:uuid;session_id:uuid?;role:TeachingRole;active_from:Instant;active_until:Instant?
- **Invariants:** Session belongs to cohort; teacher active; grants education only; revocation immediate
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** TeacherProfile, Cohort, ClassSession
- **Collaborators:** TeacherProfile, Cohort, ClassSession
- **Persistence:** teacher_assignments
- **Requirements:** ADM-015, CLS-005
- **Chunks:** ZE-P02-C04, ZE-P05-C01, ZE-P05-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| covers | Covers | session:ClassSession,now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |
| revoke | Revoke | now:Instant,reason:Reason | AssignmentRevoked | InvalidState, InvariantViolation, VersionConflict |

## Enrolment

- **Type:** aggregate
- **Module:** enrolment
- **Responsibility:** One active/held child-cohort pair; hold30m; only authoritative verified payment activates; late no-seat payment becomes exception
- **Attributes:** id:uuid;student_id:uuid;cohort_id:uuid;status:EnrolmentStatus;hold_expires_at:Instant?;access_ends_at:Instant?;version:int
- **Invariants:** One active/held child-cohort pair; hold30m; only authoritative verified payment activates; late no-seat payment becomes exception PAID_EXCEPTION allocation/refund is explicit serialized admin resolution; no automatically competing refund.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** StudentProfile, Cohort, Payment
- **Collaborators:** StudentProfile, Cohort, Payment
- **Persistence:** enrolments
- **Requirements:** ADM-016, ADM-017, ADM-018, ADM-019, AUTH-010, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, LRN-007, LRN-008, NFR-012, PAR-008
- **Chunks:** ZE-P06-C01, ZE-P06-C02, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P07-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| reserve | Reserve | expires:Instant | SeatHeld | InvalidState, InvariantViolation, VersionConflict |
| activate | Activate | proof:VerifiedPayment,seat:CapacityPermit | EnrolmentActivated | InvalidState, InvariantViolation, VersionConflict |
| expire | Expire | now:Instant | HoldExpired | InvalidState, InvariantViolation, VersionConflict |
| cancel | Cancel | reason:Reason,access_end:Instant? | EnrolmentCancelled | InvalidState, InvariantViolation, VersionConflict |
| complete | Complete | evidence:CompletionEvidence | EnrolmentCompleted | InvalidState, InvariantViolation, VersionConflict |

## AttendanceRecord

- **Type:** aggregate
- **Module:** delivery
- **Responsibility:** One row per enrolled student/session; status valid; change reason audit; no sensitive note storage
- **Attributes:** id:uuid;session_id:uuid;student_id:uuid;status:AttendanceStatus;minutes_attended:int?;recorded_by:uuid;version:int
- **Invariants:** One row per enrolled student/session; status valid; change reason audit; no sensitive note storage, First record uses conditional absence under UNIQUE(session_id,student_id), then version 1; amendments compare positive current version. Reads never create rows or manufacture versions.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** ClassSession, Enrolment
- **Collaborators:** ClassSession, Enrolment
- **Persistence:** attendance_records
- **Requirements:** ADM-017, CLS-010, PAR-010, STU-015, TCH-007, TCH-008
- **Chunks:** ZE-P05-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| record | Record | status:AttendanceStatus,minutes:int?,actor:uuid | AttendanceRecorded | InvalidState, InvariantViolation, VersionConflict |
| amend | Amend | status:AttendanceStatus,reason:Reason | AttendanceAmended | InvalidState, InvariantViolation, VersionConflict |

## Quiz

- **Type:** entity
- **Module:** assessment
- **Responsibility:** Revision immutable when published; pass0–100; attempts1–5 default3; default pass70
- **Attributes:** id:uuid;lesson_id:uuid;title:string;pass_percent:int;max_attempts:int;questions:QuizQuestion[]
- **Invariants:** Revision immutable when published; pass0–100; attempts1–5 default3; default pass70
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** QuizQuestion, CurriculumRevision
- **Collaborators:** QuizQuestion, CurriculumRevision
- **Persistence:** quizzes
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003, STU-007
- **Chunks:** ZE-P07-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| replace_questions | Replace questions | questions:tuple[QuizQuestion] | None | InvalidState, InvariantViolation, VersionConflict |
| snapshot | Snapshot | none | QuizSnapshot | InvalidState, InvariantViolation, VersionConflict |

## QuizQuestion

- **Type:** entity
- **Module:** assessment
- **Responsibility:** Single/multiple choice; correct IDs are in own options; at least2 options; keys never learner projected
- **Attributes:** id:uuid;quiz_id:uuid;prompt:string;kind:QuestionKind;options:QuizOption[];correct_ids:frozenset[uuid];points:int;explanation:string
- **Invariants:** Answer key valid within own question; approved explanation required before publication; release feedback only on own submitted attempt.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Quiz
- **Collaborators:** Quiz
- **Persistence:** quiz_questions+quiz_options
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003, STU-007
- **Chunks:** ZE-P07-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| score | Score | selection:frozenset[uuid] | int | InvalidState, InvariantViolation, VersionConflict |

## QuizAttempt

- **Type:** aggregate
- **Module:** assessment
- **Responsibility:** One in-progress attempt per quiz/enrolment; attempt count locked; submitted immutable; formative score released automatically
- **Attributes:** id:uuid;quiz_id:uuid;student_id:uuid;enrolment_id:uuid;attempt_number:int;snapshot:QuizSnapshot;answers:tuple[QuizAnswer];status:AttemptStatus;result:QuizScore?
- **Invariants:** One in-progress attempt per quiz/enrolment; attempt count locked; submitted immutable; formative score released automatically
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Quiz, Enrolment
- **Collaborators:** Quiz, Enrolment
- **Persistence:** quiz_attempts+quiz_answers
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003, STU-007
- **Chunks:** ZE-P07-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| save_answers | Save answers | answers:tuple[QuizAnswer] | AttemptSaved | InvalidState, InvariantViolation, VersionConflict |
| submit | Submit | now:Instant | QuizAttemptSubmitted | InvalidState, InvariantViolation, VersionConflict |
| release | Release | none | QuizResultReleased | InvalidState, InvariantViolation, VersionConflict |

## Assignment

- **Type:** entity
- **Module:** assessment
- **Responsibility:** Curriculum-owned immutable definition; cohort closure is separate delivery rule; late accepted until cohort complete/closed
- **Attributes:** id:uuid;lesson_id:uuid;kind:AssignmentKind;instructions:string;rubric:string;max_score:int;passing_score:int;due_offset_days:int?;allow_resubmission:bool
- **Invariants:** Curriculum-owned immutable definition; cohort closure is separate delivery rule; late accepted until cohort complete/closed
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Submission, CurriculumRevision
- **Collaborators:** Submission, CurriculumRevision, AssignmentDeliveryRule
- **Persistence:** assignments
- **Requirements:** ADM-011, ASM-004, STU-008, TCH-010
- **Chunks:** ZE-P07-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| validate_submission_window | Validate submission window | cohort:Cohort,now:Instant,closed:bool | SubmissionWindow | InvalidState, InvariantViolation, VersionConflict |

## Submission

- **Type:** aggregate
- **Module:** assessment
- **Responsibility:** Submitted work immutable; file ready+own; one current draft; returned work creates new attempt preserving chain
- **Attributes:** id:uuid;assignment_id:uuid;student_id:uuid;enrolment_id:uuid;attempt_number:int;body:string?;asset_ids:tuple[uuid];status:SubmissionStatus;late:bool
- **Invariants:** Submitted work immutable; file ready+own; one current draft; returned work creates new attempt preserving chain
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Assignment, FileAsset, Assessment
- **Collaborators:** Assignment, FileAsset, Assessment
- **Persistence:** submissions+submission_assets
- **Requirements:** ASM-005, STU-009, STU-010
- **Chunks:** ZE-P07-C03, ZE-P07-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| save_draft | Save draft | body:string?,assets:tuple[ReadyFileRef] | SubmissionSaved | InvalidState, InvariantViolation, VersionConflict |
| submit | Submit | window:SubmissionWindow | SubmissionSubmitted | InvalidState, InvariantViolation, VersionConflict |
| return_for_revision | Return for revision | reason:Reason | SubmissionReturned | InvalidState, InvariantViolation, VersionConflict |

## Assessment

- **Type:** aggregate
- **Module:** assessment
- **Responsibility:** Score bounded; ties specific submitted version; release deliberate; corrections preserve history and recompute completion
- **Attributes:** id:uuid;submission_id:uuid;assessor_id:uuid;score:int?;max_score:int;rubric_comment:string?;status:AssessmentStatus;released_at:Instant?;version:int
- **Invariants:** Score bounded; ties specific submitted version; release deliberate; corrections preserve history and recompute completion, One assessment per frozen submission; first save requires absent-resource conditional, later writes compare current assessment version. Read returns explicit nullable state and never creates a row.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Submission, ReleasePolicy
- **Collaborators:** Submission, ReleasePolicy
- **Persistence:** assessments+assessment_revisions
- **Requirements:** ADM-012, ASM-006, ASM-007, PAR-013, STU-011, TCH-011, TCH-012
- **Chunks:** ZE-P07-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| mark | Mark | score:int,comment:string | AssessmentSaved | InvalidState, InvariantViolation, VersionConflict |
| release | Release | now:Instant | AssessmentReleased | InvalidState, InvariantViolation, VersionConflict |
| withdraw | Withdraw | reason:Reason | AssessmentWithdrawn | InvalidState, InvariantViolation, VersionConflict |

## TeacherFeedback

- **Type:** aggregate
- **Module:** assessment
- **Responsibility:** Draft private; release only current teaching/admin education authority; no finance or private messaging channel
- **Attributes:** id:uuid;student_id:uuid;cohort_id:uuid;submission_id:uuid?;message:string;author_id:uuid;status:FeedbackStatus
- **Invariants:** Draft private; release only current teaching/admin education authority; no finance or private messaging channel
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** TeachingAccessPolicy, ReleasePolicy
- **Collaborators:** TeachingAccessPolicy, ReleasePolicy
- **Persistence:** teacher_feedback+feedback_revisions
- **Requirements:** ADM-019, ASM-008, PAR-012, STU-012, TCH-013
- **Chunks:** ZE-P07-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| revise | Revise | message:string | FeedbackSaved | InvalidState, InvariantViolation, VersionConflict |
| release | Release | now:Instant | FeedbackReleased | InvalidState, InvariantViolation, VersionConflict |
| withdraw | Withdraw | reason:Reason | FeedbackWithdrawn | InvalidState, InvariantViolation, VersionConflict |

## ActivityCompletion

- **Type:** entity
- **Module:** learning
- **Responsibility:** Own released lesson/activity; one row per completion key; no graded score
- **Attributes:** enrolment_id:uuid;lesson_id:uuid;block_id:uuid?;completed:bool;reflection:string?;completed_at:Instant?
- **Invariants:** Own released lesson/activity; one row per completion key; no graded score
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** StudentProgress, Lesson
- **Collaborators:** StudentProgress, Lesson
- **Persistence:** activity_completions
- **Requirements:** LRN-006, STU-006
- **Chunks:** ZE-P07-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| record | Record | completed:bool,reflection:string?,now:Instant | ActivityCompleted | InvalidState, InvariantViolation, VersionConflict |

## StudentProgress

- **Type:** projection aggregate
- **Module:** learning
- **Responsibility:** Derived from authoritative evidence; no arbitrary percentage setter; ignore cancelled sessions; >=80% delivered attendance and all required items
- **Attributes:** enrolment_id:uuid;required_counts:RequiredItemCounts;completed_counts:RequiredItemCounts;attendance:AttendanceCounts;status:ProgressStatus;source_version:int;completion_basis:CompletionBasis;active_override_id:uuid?;overrides:tuple[CompletionOverride];version:int
- **Invariants:** Derived counts and percentage cannot be manually rewritten. Standard evidence or explicit active evidenced completion override determines certificate eligibility., Initialize version 1 with an active enrolment; every recompute and override change increments this single aggregate version. CompletionReviewView exposes it only as progress_version. Lock progress before override so grant/revoke and source recomputation serialize.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** ActivityCompletion, Assessment, QuizAttempt, AttendanceRecord, CompletionPolicy, CompletionOverride
- **Collaborators:** ActivityCompletion, Assessment, QuizAttempt, AttendanceRecord, CompletionPolicy, CompletionOverride
- **Persistence:** student_progress
- **Requirements:** ADM-018, AUTH-010, LRN-007, LRN-008, NFR-012, PAR-011, STU-016, TCH-014
- **Chunks:** ZE-P07-C05, ZE-P07-C06

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| recompute | Recompute | evidence:ProgressEvidence,policy:CompletionPolicy | ProgressRecomputed | InvalidState, InvariantViolation, VersionConflict |
| is_complete | Is complete | none | bool | InvalidState, InvariantViolation, VersionConflict |
| grant_override | Add owned evidenced exceptional decision without changing source counts | Validated CompletionOverride from education-admin decision | CompletionEligibilityChanged | EvidenceRequired, InvalidState |
| revoke_override | Revoke owned exceptional decision; recompute derived eligibility | Override ID and reason | CompletionEligibilityChanged | InvalidState |

## Certificate

- **Type:** aggregate
- **Module:** learning
- **Responsibility:** One current certificate per enrolment; issue only eligible; immutable display snapshot; revoked retained; no public child lookup
- **Attributes:** id:uuid;student_id:uuid;enrolment_id:uuid;verification_code:string;name_snapshot:string;course_title_snapshot:string;status:CertificateStatus;asset_id:uuid?;replaces_id:uuid?
- **Invariants:** One current certificate per enrolment; issue only eligible; immutable display snapshot; revoked retained; no public child lookup
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** StudentProgress, FileAsset
- **Collaborators:** StudentProgress, FileAsset
- **Persistence:** certificates
- **Requirements:** ADM-020, LRN-009, LRN-010, PAR-014, STU-017
- **Chunks:** ZE-P07-C06

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| issue | Issue | eligibility:CompletionEvidence | CertificateRequested | InvalidState, InvariantViolation, VersionConflict |
| attach_render | Attach render | asset:ReadyFileRef | CertificateIssued | InvalidState, InvariantViolation, VersionConflict |
| revoke | Revoke | reason:Reason | CertificateRevoked | InvalidState, InvariantViolation, VersionConflict |

## Money

- **Type:** value object
- **Module:** billing
- **Responsibility:** AUD only at launch; integer minor units >=0; addition same currency
- **Attributes:** amount_minor:int;currency:Currency
- **Invariants:** AUD only at launch; integer minor units >=0; addition same currency
- **Authorization:** Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied.
- **Dependencies:** Price, Payment, Refund
- **Collaborators:** Price, Payment, Refund
- **Persistence:** amount_minor+currency columns
- **Requirements:** ADM-024, PAY-001
- **Chunks:** ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| add | Add | other:Money | Money | InvalidState, InvariantViolation, VersionConflict |
| subtract | Subtract | other:Money | Money | InvalidState, InvariantViolation, VersionConflict |
| covers | Covers | other:Money | bool | InvalidState, InvariantViolation, VersionConflict |

## Price

- **Type:** aggregate
- **Module:** billing
- **Responsibility:** No overlapping active fee range for same target; cohort override wins; old purchases immutable
- **Attributes:** id:uuid;course_id:uuid;cohort_id:uuid?;money:Money;tax_treatment:TaxTreatment;tax_rate_basis_points:int;effective_range:TimeRange
- **Invariants:** No overlapping active fee range for same target; cohort override wins; old purchases immutable
- **Authorization:** Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied.
- **Dependencies:** Money, Course, Cohort
- **Collaborators:** Money, Course, Cohort
- **Persistence:** prices
- **Requirements:** ADM-024, PAY-001
- **Chunks:** ZE-P03-C01, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| snapshot | Snapshot | approved_tax:TaxConfiguration | PriceSnapshot | InvalidState, InvariantViolation, VersionConflict |
| retire | Retire | at:Instant | PriceRetired | InvalidState, InvariantViolation, VersionConflict |

## Payment

- **Type:** aggregate
- **Module:** billing
- **Responsibility:** Financial truth append-only event history; unique provider IDs; success server verified; ambiguous outcome does not retry new payment blindly
- **Attributes:** id:uuid;family_id:uuid;enrolment_id:uuid;price_snapshot:PriceSnapshot;provider_checkout_id:string?;provider_payment_id:string?;status:PaymentStatus;refunded_minor:int;version:int
- **Invariants:** Financial truth append-only event history; unique provider IDs; success server verified; ambiguous outcome does not retry new payment blindly
- **Authorization:** Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied.
- **Dependencies:** Enrolment, Money, Refund, Receipt
- **Collaborators:** Enrolment, Money, Refund, Receipt
- **Persistence:** payments+payment_events
- **Requirements:** ADM-025, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Chunks:** ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| bind_checkout | Bind checkout | reference:CheckoutRef | CheckoutBound | InvalidState, InvariantViolation, VersionConflict |
| record_verified_state | Record verified state | state:VerifiedProviderPayment | PaymentUpdated | InvalidState, InvariantViolation, VersionConflict |
| flag_exception | Flag exception | code:PaymentException | PaymentExceptionRaised | InvalidState, InvariantViolation, VersionConflict |

## Refund

- **Type:** entity
- **Module:** billing
- **Responsibility:** Pending+successful refunds <= captured; provider outcome ambiguity reconciled before retry; finance privilege only
- **Attributes:** id:uuid;payment_id:uuid;amount:Money;provider_refund_id:string?;idempotency_key:uuid;access_disposition:AccessDisposition;status:RefundStatus
- **Invariants:** Pending+successful refunds <= captured; provider outcome ambiguity reconciled before retry; finance privilege only Educational disposition is KEEP or CANCEL; no date-based refund mode.
- **Authorization:** Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied.
- **Dependencies:** Payment, Enrolment
- **Collaborators:** Payment, Enrolment
- **Persistence:** refunds
- **Requirements:** ADM-026, PAY-008
- **Chunks:** ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| request | Request | available:Money | RefundRequested | InvalidState, InvariantViolation, VersionConflict |
| confirm | Confirm | provider:VerifiedRefund | RefundSucceeded | InvalidState, InvariantViolation, VersionConflict |
| fail | Fail | code:ProviderFailure | RefundFailed | InvalidState, InvariantViolation, VersionConflict |

## Receipt

- **Type:** entity
- **Module:** billing
- **Responsibility:** Immutable merchant/tax/purchase snapshot; legal content approval gate; no editing paid document
- **Attributes:** id:uuid;payment_id:uuid;type:DocumentType;number:string;merchant_snapshot:MerchantIdentity;purchaser_snapshot:string;amount:Money;tax:Money;asset_id:uuid?
- **Invariants:** Immutable merchant/tax/purchase snapshot; legal content approval gate; no editing paid document
- **Authorization:** Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied.
- **Dependencies:** Payment, FileAsset
- **Collaborators:** Payment, FileAsset
- **Persistence:** purchase_documents
- **Requirements:** ADM-025, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Chunks:** ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| issue | Issue | verified_payment:Payment,merchant:MerchantIdentity | ReceiptIssued | InvalidState, InvariantViolation, VersionConflict |
| attach_asset | Attach asset | asset:ReadyFileRef | None | InvalidState, InvariantViolation, VersionConflict |

## Event

- **Type:** aggregate
- **Module:** communication
- **Responsibility:** Explicit audience; public events contain no learner names; domain schedule authoritative
- **Attributes:** id:uuid;title:string;description:string;time:TimeSlot;audience:Audience;status:EventStatus
- **Invariants:** Explicit audience; public events contain no learner names; domain schedule authoritative
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** AudiencePolicy, IntegrationBinding
- **Collaborators:** AudiencePolicy, IntegrationBinding
- **Persistence:** events
- **Requirements:** ADM-021, PAR-015
- **Chunks:** ZE-P05-C04, ZE-P08-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| publish | Publish | none | EventPublished | InvalidState, InvariantViolation, VersionConflict |
| reschedule | Reschedule | slot:TimeSlot | EventRescheduled | InvalidState, InvariantViolation, VersionConflict |
| cancel | Cancel | reason:Reason | EventCancelled | InvalidState, InvariantViolation, VersionConflict |

## Announcement

- **Type:** aggregate
- **Module:** communication
- **Responsibility:** Publish audience resolved from current relations; withdrawn unreadable; no messaging threads
- **Attributes:** id:uuid;title:string;body:string;audience:Audience;status:AnnouncementStatus;published_at:Instant?
- **Invariants:** Publish audience resolved from current relations; withdrawn unreadable; no messaging threads
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** AudiencePolicy, Notification
- **Collaborators:** AudiencePolicy, Notification
- **Persistence:** announcements
- **Requirements:** COM-008, STU-018
- **Chunks:** ZE-P08-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| publish | Publish | now:Instant | AnnouncementPublished | InvalidState, InvariantViolation, VersionConflict |
| revise_draft | Revise draft | body:string | AnnouncementSaved | InvalidState, InvariantViolation, VersionConflict |
| withdraw | Withdraw | reason:Reason | AnnouncementWithdrawn | InvalidState, InvariantViolation, VersionConflict |

## Notification

- **Type:** aggregate
- **Module:** communication
- **Responsibility:** Unique recipient/source/kind; role-filtered allowed deep link; actor owns read state
- **Attributes:** id:uuid;recipient_id:uuid;kind:NotificationKind;source_event_id:uuid;title:string;body:string;read_at:Instant?;portal_path:PortalPath
- **Invariants:** Unique recipient/source/kind; role-filtered allowed deep link; actor owns read state
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** NotificationDelivery, Account
- **Collaborators:** NotificationDelivery, Account
- **Persistence:** notifications
- **Requirements:** ADM-022, COM-007, PAR-016, TCH-015
- **Chunks:** ZE-P08-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| mark_read | Mark read | read:bool,now:Instant | NotificationReadChanged | InvalidState, InvariantViolation, VersionConflict |

## NotificationDelivery

- **Type:** entity
- **Module:** communication
- **Responsibility:** Durable dedupe beyond provider24h; optional prefs cannot suppress security/payment essentials
- **Attributes:** id:uuid;notification_id:uuid;channel:DeliveryChannel;status:DeliveryStatus;attempts:int;provider_message_id:string?;dedupe_key:string
- **Invariants:** Durable dedupe beyond provider24h; optional prefs cannot suppress security/payment essentials
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Notification
- **Collaborators:** Notification
- **Persistence:** notification_deliveries
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, PAR-003, PAR-015, STU-018
- **Chunks:** ZE-P08-C01

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| claim | Claim | lease:Lease | DeliveryClaimed | InvalidState, InvariantViolation, VersionConflict |
| record_sent | Record sent | provider_id:string,now:Instant | DeliverySent | InvalidState, InvariantViolation, VersionConflict |
| fail | Fail | code:ProviderFailure,retry_at:Instant? | DeliveryFailed | InvalidState, InvariantViolation, VersionConflict |

## FileAsset

- **Type:** aggregate
- **Module:** files
- **Responsibility:** Quarantine unavailable; immutable promotion only after successful actual-type/checksum/malware validation; key never public; hold prevents purge
- **Attributes:** id:uuid;owner_id:uuid;purpose:FilePurpose;context_id:uuid;staging_key:string;immutable_key:string?;mime:string;size:int;checksum:string;status:FileStatus;hold:bool;version:int
- **Invariants:** Quarantine unavailable; immutable promotion only after successful actual-type/checksum/malware validation; key never public; hold prevents purge, Generated financial_document/financial_export purposes require BillingScope/FinanceScope and cannot pass generic teaching/learning file routes., purpose, context_id and owner_id are immutable after reservation; internal/public_asset context_id equals owning operations-admin account ID; upload alone never makes public.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** FileAccessPolicy
- **Collaborators:** FileAccessPolicy
- **Persistence:** file_assets
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Chunks:** ZE-P02-C05, ZE-P04-C01, ZE-P04-C02, ZE-P07-C03, ZE-P08-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| begin_scan | Begin scan | none | ScanStarted | InvalidState, InvariantViolation, VersionConflict |
| promote | Promote | result:CleanScan,key:ImmutableObjectKey | AssetReady | InvalidState, InvariantViolation, VersionConflict |
| reject | Reject | reason:ScanFailure | AssetRejected | InvalidState, InvariantViolation, VersionConflict |
| mark_deleted | Mark deleted | decision:RetentionDecision | AssetDeleted | InvalidState, InvariantViolation, VersionConflict |
| register_generated | Accept trusted bounded renderer/exporter artifact after provider integrity proof | Trusted internal generation proof with exact MIME,size,hash,purpose,intent and stored key | AssetReady | IntegrityMismatch, InvalidGeneratedPurpose, ArtifactTooLarge |

## AuditRecord

- **Type:** immutable record
- **Module:** operations
- **Responsibility:** Append-only; secrets/raw PII excluded; separate DB writer privilege; no application delete
- **Attributes:** id:uuid;actor_id:uuid?;action:string;resource_type:string;resource_id:uuid?;occurred_at:Instant;request_id:uuid;outcome:AuditOutcome;reason:string?
- **Invariants:** Append-only; secrets/raw PII excluded; separate DB writer privilege; no application delete
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Account
- **Collaborators:** Account
- **Persistence:** audit_records
- **Requirements:** ADM-029, SEC-007
- **Chunks:** ZE-P02-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| redacted_view | Redacted view | scope:AuditScope | AuditSummary | InvalidState, InvariantViolation, VersionConflict |

## ApplicationSetting

- **Type:** aggregate
- **Module:** operations
- **Responsibility:** Closed typed key catalog; secrets are external references; sensitive values need approval; settings not generic arbitrary JSON behavior
- **Attributes:** key:SettingKey;typed_value:SettingValue;approved:bool;approval_reference:string?;version:int
- **Invariants:** Closed typed key catalog; secrets are external references; sensitive values need approval; settings not generic arbitrary JSON behavior
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** RoleGrant
- **Collaborators:** RoleGrant
- **Persistence:** application_settings
- **Requirements:** ADM-028
- **Chunks:** ZE-P01-C02, ZE-P08-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| change | Change | value:SettingValue,approval:ApprovalReference? | SettingChanged | InvalidState, InvariantViolation, VersionConflict |
| approve | Approve | reference:ApprovalReference | SettingApproved | InvalidState, InvariantViolation, VersionConflict |

## IntegrationBinding

- **Type:** aggregate
- **Module:** operations
- **Responsibility:** Unique provider/resource; latest desired domain version wins; encrypted identifiers; host URL never persisted
- **Attributes:** id:uuid;provider:Provider;resource_type:MirrorResourceType;resource_id:uuid;provider_id_ciphertext:bytes;desired_version:int;applied_version:int;status:SyncStatus
- **Invariants:** Unique provider/resource; latest desired domain version wins; encrypted identifiers; host URL never persisted
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** ClassSession, Event
- **Collaborators:** ClassSession, Event
- **Persistence:** integration_bindings
- **Requirements:** OPS-003
- **Chunks:** ZE-P01-C02, ZE-P05-C03, ZE-P05-C04, ZE-P08-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| schedule_sync | Schedule sync | version:int | SyncRequested | InvalidState, InvariantViolation, VersionConflict |
| mark_applied | Mark applied | version:int | SyncApplied | InvalidState, InvariantViolation, VersionConflict |
| record_failure | Record failure | code:ProviderFailure | SyncFailed | InvalidState, InvariantViolation, VersionConflict |

## WebhookInbox

- **Type:** immutable processing record
- **Module:** operations
- **Responsibility:** Verify before processing; unique provider/event; unsupported signed event ignored safely; bounded encrypted retention
- **Attributes:** id:uuid;provider:Provider;provider_event_id:string;received_at:Instant;verified:bool;payload_reference:EncryptedReference;status:InboxStatus
- **Invariants:** Verify before processing; unique provider/event; unsupported signed event ignored safely; bounded encrypted retention
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Payment
- **Collaborators:** Payment
- **Persistence:** webhook_inbox
- **Requirements:** PAY-004, PAY-005
- **Chunks:** ZE-P01-C02, ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05, ZE-P08-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| claim | Claim | lease:Lease | InboxClaimed | InvalidState, InvariantViolation, VersionConflict |
| complete | Complete | outcome:ProcessingOutcome | InboxProcessed | InvalidState, InvariantViolation, VersionConflict |

## OutboxEvent

- **Type:** immutable delivery record
- **Module:** operations
- **Responsibility:** Created in same transaction as business mutation; opaque IDs only; at-least-once dispatch and deduped consumption
- **Attributes:** id:uuid;aggregate_type:string;aggregate_id:uuid;aggregate_version:int;event_type:string;payload:MinimalEventPayload;occurred_at:Instant;published_at:Instant?
- **Invariants:** Created in same transaction as business mutation; opaque IDs only; at-least-once dispatch and deduped consumption
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** BackgroundJob
- **Collaborators:** BackgroundJob
- **Persistence:** outbox_events
- **Requirements:** OPS-005
- **Chunks:** ZE-P01-C02, ZE-P08-C01, ZE-P08-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| claim | Claim | lease:Lease | OutboxClaimed | InvalidState, InvariantViolation, VersionConflict |
| mark_published | Mark published | now:Instant | None | InvalidState, InvariantViolation, VersionConflict |

## BackgroundJob

- **Type:** aggregate
- **Module:** operations
- **Responsibility:** Unique job kind/dedupe key; bounded exponential retry max8 attempts/24h; stale leases recover; immutable payload
- **Attributes:** id:uuid;kind:JobKind;source_event_id:uuid?;dedupe_key:string;status:JobStatus;attempt_count:int;lease_until:Instant?;next_attempt_at:Instant?
- **Invariants:** Unique job kind/dedupe key; bounded exponential retry max8 attempts/24h; stale leases recover; immutable payload
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** OutboxEvent
- **Collaborators:** OutboxEvent
- **Persistence:** background_jobs
- **Requirements:** OPS-005
- **Chunks:** ZE-P01-C02, ZE-P08-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| claim | Claim | now:Instant,lease_until:Instant | JobClaimed | InvalidState, InvariantViolation, VersionConflict |
| succeed | Succeed | none | JobSucceeded | InvalidState, InvariantViolation, VersionConflict |
| retry | Retry | code:Failure,next_at:Instant | JobRetryScheduled | InvalidState, InvariantViolation, VersionConflict |
| dead_letter | Dead letter | code:Failure | JobDeadLettered | InvalidState, InvariantViolation, VersionConflict |

## PrivacyRequest

- **Type:** aggregate
- **Module:** family
- **Responsibility:** Verified adult authority and explicit retention decision precede export/purge; holds respected; do not orphan child guardianship
- **Attributes:** id:uuid;family_id:uuid;requester_id:uuid;student_id:uuid?;kind:PrivacyRequestKind;status:PrivacyStatus;verification_reference:string?;decision_reason:string?
- **Invariants:** Verified adult authority and explicit retention decision precede export/purge; holds respected; do not orphan child guardianship
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Family, GuardianStudent, FileAsset
- **Collaborators:** Family, GuardianStudent, FileAsset
- **Persistence:** privacy_requests+retention_holds
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Chunks:** ZE-P02-C05, ZE-P08-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| verify | Verify | evidence:VerificationRef | PrivacyVerified | InvalidState, InvariantViolation, VersionConflict |
| approve | Approve | decision:RetentionDecision | PrivacyApproved | InvalidState, InvariantViolation, VersionConflict |
| complete | Complete | result:PrivacyOutcome | PrivacyCompleted | InvalidState, InvariantViolation, VersionConflict |
| reject | Reject | reason:Reason | PrivacyRejected | InvalidState, InvariantViolation, VersionConflict |

## FamilyOwnershipPolicy

- **Type:** domain policy
- **Module:** family
- **Responsibility:** Require active explicit link for child and separate active family financial membership; no names/email matching
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** Require active explicit link for child and separate active family financial membership; no names/email matching
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Family, GuardianStudent, BillingMembership
- **Collaborators:** Family, GuardianStudent, BillingMembership
- **Persistence:** none; pure policy
- **Requirements:** AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016
- **Chunks:** ZE-P02-C03, ZE-P06-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| authorize_student | Authorize student | principal:Principal,links:GuardianLinks,student:StudentProfile | FamilyScope | InvalidState, InvariantViolation, VersionConflict |
| authorize_billing | Authorize billing | principal:Principal,memberships:BillingMemberships,family_id:uuid | BillingScope | InvalidState, InvariantViolation, VersionConflict |

## TeachingAccessPolicy

- **Type:** domain policy
- **Module:** delivery
- **Responsibility:** Teacher role plus active relevant assignment plus enrolled learner; financial actions denied before repository read
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** Teacher role plus active relevant assignment plus enrolled learner; financial actions denied before repository read
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** TeacherAssignment, Enrolment
- **Collaborators:** TeacherAssignment, Enrolment
- **Persistence:** none; pure policy
- **Requirements:** AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016
- **Chunks:** ZE-P02-C04, ZE-P05-C03, ZE-P05-C05, ZE-P07-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| authorize | Authorize | principal:Principal,assignment:TeacherAssignment,enrolment:Enrolment,action:TeachingAction | TeachingScope | InvalidState, InvariantViolation, VersionConflict |

## PublicationPolicy

- **Type:** domain policy
- **Module:** curriculum
- **Responsibility:** All referenced objects same revision; accessible content and safe assets; no unresolved required settings
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** All referenced objects same revision; accessible content and safe assets; no unresolved required settings
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** CurriculumRevision, LessonBlock, FileAsset
- **Collaborators:** CurriculumRevision, LessonBlock, FileAsset
- **Persistence:** none; pure policy
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003
- **Chunks:** ZE-P03-C01, ZE-P03-C02, ZE-P03-C03, ZE-P03-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| validate | Validate | revision:CurriculumRevision,assets:ReadyAssets,settings:ApprovedSettings | PublicationReport | InvalidState, InvariantViolation, VersionConflict |

## ReleasePolicy

- **Type:** domain policy
- **Module:** learning
- **Responsibility:** Pinned revision membership and active/completed entitlement and release time; draft marks never visible
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** Pinned revision membership and active/completed entitlement and release time; draft marks never visible
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Enrolment, CurriculumRevision, Assessment, TeacherFeedback
- **Collaborators:** Enrolment, CurriculumRevision, Assessment, TeacherFeedback
- **Persistence:** none; pure policy
- **Requirements:** AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016
- **Chunks:** ZE-P07-C01, ZE-P07-C02, ZE-P07-C03, ZE-P07-C04

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| can_read | Can read | principal:Principal,enrolment:Enrolment,resource:LearningResourceState,now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |

## SchedulePolicy

- **Type:** domain policy
- **Module:** delivery
- **Responsibility:** Teacher assigned future session at least24h; administrator reason for shorter notice; no conflict; valid DST resolution
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** Teacher assigned future session at least24h; administrator reason for shorter notice; no conflict; valid DST resolution
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** ClassSession, TeacherAssignment, Cohort
- **Collaborators:** ClassSession, TeacherAssignment, Cohort
- **Persistence:** none; pure policy
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011, PAR-009, STU-013, TCH-005, TCH-006, WEB-005
- **Chunks:** ZE-P05-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| authorize_change | Authorize change | principal:Principal,session:ClassSession,new_slot:TimeSlot,conflicts:ScheduleConflicts,now:Instant | SchedulePermit | InvalidState, InvariantViolation, VersionConflict |

## CapacityPolicy

- **Type:** domain policy
- **Module:** enrolment
- **Responsibility:** Run under cohort row lock; active+unexpired holds <= capacity; verified late payment never oversells
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** Run under cohort row lock; active+unexpired holds <= capacity; verified late payment never oversells
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** Cohort, Enrolment
- **Collaborators:** Cohort, Enrolment
- **Persistence:** none; pure policy
- **Requirements:** ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008
- **Chunks:** ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| reserve | Reserve | capacity:int,active:int,unexpired_holds:int,now:Instant | CapacityPermit | InvalidState, InvariantViolation, VersionConflict |

## CompletionPolicy

- **Type:** domain policy
- **Module:** learning
- **Responsibility:** All required learning items satisfied and >=80% delivered attendance; no arbitrary progress edit; no zero-delivery completion
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** All required items plus >=80% delivered attendance make standard completion eligible. An active education_admin completion override with reason and verified evidence can independently confer eligibility without changing source records.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** ActivityCompletion, QuizAttempt, Assessment, AttendanceRecord
- **Collaborators:** ActivityCompletion, QuizAttempt, Assessment, AttendanceRecord
- **Persistence:** none; pure policy
- **Requirements:** ADM-018, LRN-007, LRN-008, PAR-011, STU-016, TCH-014
- **Chunks:** ZE-P07-C05, ZE-P07-C06

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| evaluate | Evaluate | evidence:ProgressEvidence | CompletionEvidence | InvalidState, InvariantViolation, VersionConflict |

## AudiencePolicy

- **Type:** domain policy
- **Module:** communication
- **Responsibility:** Only current intended audience; no cohort roster disclosure; relevant parent/student/teacher notices only
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** Target kind public/role/course/cohort plus explicit recipient role filter; course resolves eligible enrolments across its cohorts and current teachers; parent requires active child link; no recipient roster exposed.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** GuardianStudent, TeacherAssignment, Enrolment
- **Collaborators:** GuardianStudent, TeacherAssignment, Enrolment
- **Persistence:** none; pure policy
- **Requirements:** COM-008, STU-018
- **Chunks:** ZE-P08-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| resolve | Resolve | audience:Audience,relationships:AudienceRelationships | frozenset[RecipientId] | InvalidState, InvariantViolation, VersionConflict |
| permits | Permits | principal:Principal,audience:Audience | bool | InvalidState, InvariantViolation, VersionConflict |

## FileAccessPolicy

- **Type:** domain policy
- **Module:** files
- **Responsibility:** Ready state for download; owner draft for upload; release/guardian/assignment context; internal purpose excluded from learners
- **Attributes:** no mutable attributes; explicit evaluation context
- **Invariants:** Ready state for download; owner draft for upload; release/guardian/assignment context; internal purpose excluded from learners, Reject financial_document and financial_export on generic /files endpoints; financial-specific document/export services recheck billing membership or finance_admin before signed grant., submission -> Submission.id from owned draft submission create/detail, same authenticated student and eligible enrolment; resource -> CurriculumRevision.id from education-admin revision list/detail, must still be writable draft; internal/public_asset -> authenticated SessionView.user_id (the same Account.id as principal), current admin:operations_admin only. No caller-selected other account/context; certificate/financial_document/financial_export are server-generated and forbidden here.
- **Authorization:** Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing.
- **Dependencies:** FileAsset, Enrolment, GuardianStudent, TeacherAssignment
- **Collaborators:** FileAsset, Enrolment, GuardianStudent, TeacherAssignment
- **Persistence:** none; pure policy
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Chunks:** ZE-P04-C01, ZE-P04-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| authorize | Authorize | principal:Principal,asset:FileAsset,context:FileContext,action:FileAction | FileScope | InvalidState, InvariantViolation, VersionConflict |

## CompletionOverride

- **Type:** entity
- **Module:** learning
- **Responsibility:** Evidence-backed administrative completion decision preserving source learning/attendance truth.
- **Attributes:** id:uuid;enrolment_id:uuid;actor_id:uuid;reason:string;evidence_references:tuple[string];granted_at:Instant;revoked_at:Instant?;version:int
- **Invariants:** Education-admin with recent MFA only; nonempty reason and verified evidence references mandatory; never changes grades or attendance.
- **Authorization:** education_admin plus explicit evidence and reason; teacher cannot grant.
- **Dependencies:** StudentProgress
- **Collaborators:** StudentProgress, Certificate
- **Persistence:** completion_overrides
- **Requirements:** ADM-018, AUTH-010, LRN-007, LRN-008, NFR-012, SEC-007
- **Chunks:** ZE-P07-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| grant | Grant audited exceptional completion eligibility | Education-admin actor, reason, verified evidence references | CompletionOverrideGranted | EvidenceRequired, Forbidden, InvalidState |
| revoke | Revoke invalid exceptional decision and recompute certificate eligibility | Reason and current instant | CompletionOverrideRevoked | InvalidState |

## MfaFactor

- **Type:** aggregate
- **Module:** identity
- **Responsibility:** Durable replay-resistant mandatory staff second-factor lifecycle.
- **Attributes:** id:uuid;account_id:uuid;secret_reference:EncryptedSecretRef;status:FactorStatus;last_accepted_step:int?;activated_at:Instant?;version:int
- **Invariants:** Secret seed encrypted with versioned managed key; recovery codes hashed; challenge/setup tokens hashed, purpose/browser-bound and expiring; last TOTP timestep locked and monotonic; no full staff privileges before completion.
- **Authorization:** Own staff account limited setup or authenticated challenge; secret material never API-returned except one-time provisioning URI.
- **Dependencies:** Account, Session
- **Collaborators:** Account, Session
- **Persistence:** mfa_factors
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, TCH-001, ADM-001, SEC-004
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| activate | Activate only after first valid proof | proof:VerifiedTotpProof,now:Instant | MfaActivated | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |
| accept_step | Reject replay if step<=last accepted step | step:int | TotpAccepted | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |
| revoke | Revoke compromised factor and dependent sessions | reason:Reason | MfaRevoked | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |

## RecoveryCode

- **Type:** entity
- **Module:** identity
- **Responsibility:** Durable replay-resistant mandatory staff second-factor lifecycle.
- **Attributes:** id:uuid;factor_id:uuid;code_hash:bytes;consumed_at:Instant?
- **Invariants:** Secret seed encrypted with versioned managed key; recovery codes hashed; challenge/setup tokens hashed, purpose/browser-bound and expiring; last TOTP timestep locked and monotonic; no full staff privileges before completion.
- **Authorization:** Own staff account limited setup or authenticated challenge; secret material never API-returned except one-time provisioning URI.
- **Dependencies:** Account, Session
- **Collaborators:** Account, Session
- **Persistence:** mfa_recovery_codes
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, TCH-001, ADM-001, SEC-004
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| consume | Consume matching hashed recovery code once under row lock | proof:VerifiedRecoveryProof,now:Instant | RecoveryCodeConsumed | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |

## MfaChallenge

- **Type:** entity
- **Module:** identity
- **Responsibility:** Durable replay-resistant mandatory staff second-factor lifecycle.
- **Attributes:** id:uuid;account_id:uuid;token_hash:bytes;purpose:ChallengePurpose;expires_at:Instant;attempts:int;consumed_at:Instant?;browser_binding_hash:bytes
- **Invariants:** Secret seed encrypted with versioned managed key; recovery codes hashed; challenge/setup tokens hashed, purpose/browser-bound and expiring; last TOTP timestep locked and monotonic; no full staff privileges before completion.
- **Authorization:** Own staff account limited setup or authenticated challenge; secret material never API-returned except one-time provisioning URI.
- **Dependencies:** Account, Session
- **Collaborators:** Account, Session
- **Persistence:** mfa_challenges
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, TCH-001, ADM-001, SEC-004
- **Chunks:** ZE-P02-C01, ZE-P02-C03

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| consume | Require correct purpose/browser/expiry and proof, consume once | proof:VerifiedSecondFactor,now:Instant | ChallengeConsumed | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |
| reject_attempt | Bound attempts and revoke challenge after5 failures | now:Instant | ChallengeAttemptRejected | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |

## ReconciliationException

- **Type:** aggregate
- **Module:** billing
- **Responsibility:** Preserve provider financial truth when local purchase association is missing or inconsistent.
- **Attributes:** id:uuid;provider_transaction_id:string;amount:Money;provider_status:string;payment_id:uuid?;status:ReconciliationStatus;first_seen_at:Instant;last_checked_at:Instant;reason_code:string;version:int
- **Invariants:** No inferred child/family ownership; resolve only verified immutable-reference/amount/currency match or verified provider reversal; unresolved evidence remains visible.
- **Authorization:** finance_admin or SystemBillingScope only; excluded from teacher/student and parent scopes until valid own purchase link exists.
- **Dependencies:** Payment, Money
- **Collaborators:** Payment
- **Persistence:** reconciliation_exceptions
- **Requirements:** PAY-009, ADM-025, ENR-007
- **Chunks:** ZE-P06-C01, ZE-P06-C03, ZE-P06-C04, ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| reconcile | Resolve only proved local association or provider reversal | Verified provider transaction and optional verified purchase match | ReconciliationChecked | ReferenceMismatch, AmountMismatch, UnknownOutcome |

## FinancialExport

- **Type:** aggregate
- **Module:** billing
- **Responsibility:** Track private finance report request, immutable date range, generation job, protected artifact and expiry.
- **Attributes:** id:uuid;requested_by:uuid;from_date:LocalDate;to_date:LocalDate;job_id:uuid;status:ExportStatus;asset_id:uuid?;expires_at:Instant?;version:int;failure_code:ExportFailureCode?
- **Invariants:** finance_admin only; range<=366days; ready requires verified generated financial_export asset; immutable request range and requester; downloads authorized again; signed URL<=60s and export expires24h after ready., Status requested/processing/ready/failed/expired. Exhausted bounded retries set failed with sanitized failure_code; no usable URL. Authorized operations job retry transitions failed to processing and clears failure; requester may create a new export with a new idempotency key.
- **Authorization:** finance_admin requesting/overseeing export only; parent/teacher/student denied; worker generation requires SystemFinanceScope.
- **Dependencies:** FileAsset, BackgroundJob
- **Collaborators:** Payment, Refund, FileAsset, BackgroundJob
- **Persistence:** privacy_exports with purpose=financial_export
- **Requirements:** ADM-027, PAY-010, FILE-007
- **Chunks:** ZE-P06-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| complete | Attach verified private CSV and set24h expiry | Ready financial_export asset and instant | FinancialExportReady | InvalidState, InvalidGeneratedPurpose |
| expire | Expire download authority and schedule artifact cleanup | Current instant | FinancialExportExpired | InvalidState |
| start_generation | Start or explicitly retry an authorized generation job | Matching current job ID | ExportProcessing | InvalidState, VersionConflict |
| fail | Persist bounded-retry exhaustion without leaking provider details | GENERATION_FAILED, LIMIT_EXCEEDED or STORAGE_UNAVAILABLE | ExportFailed | InvalidState, VersionConflict |

## RetentionHold

- **Type:** aggregate
- **Module:** privacy
- **Responsibility:** Audited legal retention decision for one typed resource, with a version independent of that resource.
- **Attributes:** id:uuid;resource_type:RetentionResourceType;resource_id:uuid;held:bool;reason:Reason;approval_reference:string;actor_id:uuid;version:int
- **Invariants:** Unique (resource_type,resource_id); verify target existence under identity-purpose scope before changes., No row is represented read-only as version 0; first write must compare against absence and inserts version 1. Persisted versions are positive; released rows are retained, never reset to absence., Every hold mutation and resource purge acquires the same transaction-scoped typed-resource lock, including applicable family/student ancestor hold locks in deterministic order. Purge rechecks all holds before deletion; concurrent hold changes cannot be bypassed.
- **Authorization:** Active administrator with identity_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Explicit identity-purpose projection only.
- **Dependencies:** See Code Blueprint implementation ownership
- **Collaborators:** See Code Blueprint implementation ownership
- **Persistence:** retention_holds
- **Requirements:** AUTH-010, NFR-012, SEC-002, SEC-008, SEC-009, SEC-010
- **Chunks:** ZE-P02-C05

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| set_state | Validate evidence and change held state with audit | held:bool,reason:Reason,approval:ApprovalReference,actor:Principal | RetentionHoldChanged | InvalidState, InvariantViolation, VersionConflict |

## AssignmentDeliveryRule

- **Type:** aggregate
- **Module:** assessment
- **Responsibility:** Per-cohort assignment submission closure and resolved due time, independently versioned from published assignment definition.
- **Attributes:** assignment_id:uuid;cohort_id:uuid;due_at:Instant?;closed:bool;reason:Reason?;version:int
- **Invariants:** Assignment must belong to cohort pinned revision; definition remains immutable., No row means default open delivery rule and derived due time, never a fabricated positive version. First explicit change requires conditional absence; later changes compare current delivery rule version., Closure and submission finalization lock the same cohort/assignment delivery key so work cannot finalize after a concurrent closure. Cohort completion/closure still blocks submissions independently.
- **Authorization:** Active administrator with education_admin and recent MFA; deny every other privilege-only principal, teacher, parent and student. Cohort-scoped educational projection only.
- **Dependencies:** Assignment, Cohort
- **Collaborators:** Assignment, Cohort
- **Persistence:** assignment_delivery_rules
- **Requirements:** ADM-011, ASM-004
- **Chunks:** ZE-P07-C02

| Public method | Purpose | Inputs | Output | Domain failures |
|---|---|---|---|---|
| set_closed | Change one delivery submission window with audited reason | closed:bool,reason:Reason | AssignmentDeliveryClosureChanged | InvalidState, InvariantViolation, VersionConflict |
