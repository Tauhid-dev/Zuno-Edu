# Backend object catalog

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

Important objects below encapsulate identity, lifecycle or reusable policy. Small private helpers do not need a durable object entry; introducing a public domain concept does. Type annotations here are documentation contracts, not implementation. Value/reference types named inside attributes use the constrained primitive schemas and domain definitions; framework-independent dataclasses/enums are permitted only within these named boundaries.

## Account

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / identity |
| Responsibility | One principal role; staff MFA; student email nullable; suspended/closed accounts cannot authenticate |
| Attributes | id:uuid;role:RoleGrant;status:AccountStatus;email:NormalizedEmail?;display_name:string;version:int |
| Invariants | One principal role; staff MFA; student email nullable; suspended/closed accounts cannot authenticate |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Credential, Session, RoleGrant |
| Persistence | accounts |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| activate(verified_at:Instant)->AccountActivated | Activate | verified_at:Instant | AccountActivated | InvalidState, InvariantViolation, VersionConflict |
| suspend(reason:Reason)->SessionsRevoked | Suspend | reason:Reason | SessionsRevoked | InvalidState, InvariantViolation, VersionConflict |
| close(decision:RetentionDecision)->AccountClosed | Close | decision:RetentionDecision | AccountClosed | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACCOUNT_SUSPENDED, FORBIDDEN, INCOMPATIBLE_ROLE, INVALID_CREDENTIALS, INVALID_STATE, InvalidState, InvariantViolation, LAST_ADMIN, MFA_ATTEMPTS_EXCEEDED, MFA_CHALLENGE_EXPIRED, MFA_REPLAY, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Credential

| Metadata | Contract |
| --- | --- |
| Type / module | entity / identity |
| Responsibility | Only Argon2id hashes; no plaintext persistence; breached password rejected before hash |
| Attributes | user_id:uuid;password_hash:string;changed_at:Instant;failed_attempts:int |
| Invariants | Only Argon2id hashes; no plaintext persistence; breached password rejected before hash |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Account |
| Persistence | credentials |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| replace(hash:PasswordHash,now:Instant)->CredentialChanged | Replace | hash:PasswordHash,now:Instant | CredentialChanged | InvalidState, InvariantViolation, VersionConflict |
| verify_attempt(outcome:bool,now:Instant)->LockoutDecision | Verify attempt | outcome:bool,now:Instant | LockoutDecision | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACCOUNT_SUSPENDED, FORBIDDEN, INVALID_CREDENTIALS, INVALID_STATE, InvalidState, InvariantViolation, MFA_ATTEMPTS_EXCEEDED, MFA_CHALLENGE_EXPIRED, MFA_REPLAY, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Session

| Metadata | Contract |
| --- | --- |
| Type / module | entity / identity |
| Responsibility | Opaque rotating token, absolute/idle expiry; revoked cannot be resumed |
| Attributes | id:uuid;user_id:uuid;token_hash:string;expires_at:Instant;revoked_at:Instant?;mfa_verified_at:Instant? |
| Invariants | Opaque rotating token, absolute/idle expiry; revoked cannot be resumed |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Account |
| Persistence | sessions |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| rotate(new_hash:TokenHash,now:Instant)->SessionRotated | Rotate | new_hash:TokenHash,now:Instant | SessionRotated | InvalidState, InvariantViolation, VersionConflict |
| revoke(now:Instant)->None | Revoke | now:Instant | None | InvalidState, InvariantViolation, VersionConflict |
| is_active(now:Instant)->bool | Is active | now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACCOUNT_SUSPENDED, FORBIDDEN, INVALID_CREDENTIALS, INVALID_STATE, InvalidState, InvariantViolation, MFA_ATTEMPTS_EXCEEDED, MFA_CHALLENGE_EXPIRED, MFA_REPLAY, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## RoleGrant

| Metadata | Contract |
| --- | --- |
| Type / module | value object / identity |
| Responsibility | Teacher principal cannot also have admin privileges; privileges only approved closed enum |
| Attributes | role:Role;admin_privileges:frozenset[Privilege] |
| Invariants | Teacher principal cannot also have admin privileges; privileges only approved closed enum |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Account |
| Persistence | accounts.admin_privileges |
| Requirements | ADM-006 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| allows(capability:Privilege)->bool | Allows | capability:Privilege | bool | InvalidState, InvariantViolation, VersionConflict |
| validate_change(actor:Principal,requested:RoleGrant)->RoleGrant | Validate change | actor:Principal,requested:RoleGrant | RoleGrant | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACCOUNT_SUSPENDED, FORBIDDEN, INCOMPATIBLE_ROLE, INVALID_CREDENTIALS, INVALID_STATE, InvalidState, InvariantViolation, LAST_ADMIN, MFA_ATTEMPTS_EXCEEDED, MFA_CHALLENGE_EXPIRED, MFA_REPLAY, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Guardian

| Metadata | Contract |
| --- | --- |
| Type / module | entity / family |
| Responsibility | Adult contact tied to verified account; no exact birthday collection |
| Attributes | id:uuid;user_id:uuid;family_id:uuid;first_name:string;last_name:string?;phone:E164?;optional_email:bool |
| Invariants | Adult contact tied to verified account; no exact birthday collection |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Account, Family |
| Persistence | guardians |
| Requirements | AUTH-011, PAR-002, PAR-021, STU-019 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| update_contact(name:Name,phone:E164?)->GuardianUpdated | Update contact | name:Name,phone:E164? | GuardianUpdated | InvalidState, InvariantViolation, VersionConflict |
| set_preferences(optional_email:bool)->PreferencesChanged | Set preferences | optional_email:bool | PreferencesChanged | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INCOMPATIBLE_ROLE, INVALID_STATE, InvalidState, InvariantViolation, LAST_ADMIN, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Family

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / family |
| Responsibility | Family relationship does not imply each guardian can access every sibling; active child needs at least one verified guardian |
| Attributes | id:uuid;guardians:Guardian[];links:GuardianStudent[];billing_members:BillingMembership[];version:int |
| Invariants | Family relationship does not imply each guardian can access every sibling; active child needs at least one verified guardian |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Guardian, GuardianStudent, BillingMembership, StudentProfile |
| Persistence | families |
| Requirements | PAR-006 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| link_guardian(link:GuardianStudent,evidence:VerificationRef)->GuardianLinked | Link guardian | link:GuardianStudent,evidence:VerificationRef | GuardianLinked | InvalidState, InvariantViolation, VersionConflict |
| revoke_link(link_id:uuid,reason:Reason)->GuardianRevoked | Revoke link | link_id:uuid,reason:Reason | GuardianRevoked | InvalidState, InvariantViolation, VersionConflict |
| grant_billing(member:BillingMembership)->BillingGranted | Grant billing | member:BillingMembership | BillingGranted | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## GuardianStudent

| Metadata | Contract |
| --- | --- |
| Type / module | entity / family |
| Responsibility | Guardian and child share family; unique active pair; verification required; immediate revocation |
| Attributes | guardian_id:uuid;student_id:uuid;family_id:uuid;verified_at:Instant;revoked_at:Instant?;verification_reference:string |
| Invariants | Guardian and child share family; unique active pair; verification required; immediate revocation |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Guardian, StudentProfile |
| Persistence | guardian_students |
| Requirements | PAR-006 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| is_active(now:Instant)->bool | Is active | now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |
| revoke(reason:Reason,now:Instant)->GuardianLinkRevoked | Revoke | reason:Reason,now:Instant | GuardianLinkRevoked | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_ENROLMENT_EXISTS, ACTIVE_GUARDIAN_REQUIRED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LEGAL_HOLD, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## BillingMembership

| Metadata | Contract |
| --- | --- |
| Type / module | entity / family |
| Responsibility | Explicit financial visibility independent of child guardianship; primary verified parent receives initial membership |
| Attributes | family_id:uuid;guardian_id:uuid;granted_at:Instant;revoked_at:Instant?;approval_reference:string |
| Invariants | Explicit financial visibility independent of child guardianship; primary verified parent receives initial membership |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Family, Guardian |
| Persistence | billing_memberships |
| Requirements | AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| revoke(reason:Reason,now:Instant)->BillingAccessRevoked | Revoke | reason:Reason,now:Instant | BillingAccessRevoked | InvalidState, InvariantViolation, VersionConflict |
| permits(family_id:uuid)->bool | Permits | family_id:uuid | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_UNAVAILABLE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## StudentProfile

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / family |
| Responsibility | Name and age required; school/last/preferred names nullable; no diagnoses/DOB/child email required |
| Attributes | id:uuid;family_id:uuid;first_name:string;preferred_name:string?;last_name:string?;age:AgeSnapshot;school_name:string?;school_year:string?;interests:tuple[str];prior_experience:Experience?;status:StudentStatus |
| Invariants | Name and age required; school/last/preferred names nullable; no diagnoses/DOB/child email required |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | AgeSnapshot, GuardianStudent |
| Persistence | students |
| Requirements | ADM-004, PAR-005, TCH-009 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| update_profile(changes:StudentProfileChange)->StudentUpdated | Update profile | changes:StudentProfileChange | StudentUpdated | InvalidState, InvariantViolation, VersionConflict |
| reconfirm_age(age:int,as_of:LocalDate)->AgeReconfirmed | Reconfirm age | age:int,as_of:LocalDate | AgeReconfirmed | InvalidState, InvariantViolation, VersionConflict |
| archive(reason:Reason)->StudentArchived | Archive | reason:Reason | StudentArchived | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_ENROLMENT_EXISTS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## AgeSnapshot

| Metadata | Contract |
| --- | --- |
| Type / module | value object / family |
| Responsibility | No inferred DOB; age value valid in technical range; >180 days stale for new checkout |
| Attributes | years:int;recorded_on:LocalDate |
| Invariants | No inferred DOB; age value valid in technical range; >180 days stale for new checkout |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | StudentProfile |
| Persistence | students.age_years+age_recorded_on |
| Requirements | ADM-004, PAR-005, TCH-009 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| requires_reconfirmation(today:LocalDate)->bool | Requires reconfirmation | today:LocalDate | bool | InvalidState, InvariantViolation, VersionConflict |
| meets_band(min_age:int,max_age:int)->bool | Meets band | min_age:int,max_age:int | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_ENROLMENT_EXISTS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## TeacherProfile

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / identity |
| Responsibility | Public publication deliberate; no operational contacts exposed; archive needs no live assignment |
| Attributes | id:uuid;user_id:uuid;display_name:string;biography:string?;public_photo_asset_id:uuid?;published:bool;status:TeacherStatus |
| Invariants | Public publication deliberate; no operational contacts exposed; archive needs no live assignment |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Account, TeacherAssignment |
| Persistence | teacher_profiles |
| Requirements | ADM-005, WEB-006 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| update_public_profile(profile:PublicTeacherDraft)->TeacherUpdated | Update public profile | profile:PublicTeacherDraft | TeacherUpdated | InvalidState, InvariantViolation, VersionConflict |
| publish(approved:bool)->TeacherPublished | Publish | approved:bool | TeacherPublished | InvalidState, InvariantViolation, VersionConflict |
| archive(no_active_assignments:bool)->TeacherArchived | Archive | no_active_assignments:bool | TeacherArchived | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_ASSIGNMENT_EXISTS, FORBIDDEN, INCOMPATIBLE_ROLE, INVALID_STATE, InvalidState, InvariantViolation, LAST_ADMIN, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## PolicyDocument

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / content |
| Responsibility | Published versions immutable; required acknowledgement only effective approved versions |
| Attributes | id:uuid;key:PolicyKey;version_label:string;html:SanitizedHtml;effective_at:Instant;approval_reference:string?;published_at:Instant? |
| Invariants | Published versions immutable; required acknowledgement only effective approved versions |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | PolicyAcknowledgement |
| Persistence | policy_documents |
| Requirements | WEB-010 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| publish(approval:ApprovalReference,now:Instant)->PolicyPublished | Publish | approval:ApprovalReference,now:Instant | PolicyPublished | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, POLICY_VERSION_STALE, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## PolicyAcknowledgement

| Metadata | Contract |
| --- | --- |
| Type / module | entity / family |
| Responsibility | Immutable attributable version-specific evidence; scope linked guardian child only |
| Attributes | id:uuid;policy_id:uuid;guardian_id:uuid;family_id:uuid;student_id:uuid?;acknowledged_at:Instant |
| Invariants | Immutable attributable version-specific evidence; scope linked guardian child only |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | PolicyDocument, Guardian |
| Persistence | policy_acknowledgements |
| Requirements | PAR-004, SEC-003 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| covers(policy_id:uuid,student_id:uuid?)->bool | Covers | policy_id:uuid,student_id:uuid? | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, POLICY_VERSION_STALE, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## PublicPage

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / content |
| Responsibility | Fixed approved page catalog; sanitize content; draft never public |
| Attributes | slug:PublicPageSlug;title:string;draft:SanitizedHtml;published_revision_id:uuid? |
| Invariants | Fixed approved page catalog; sanitize content; draft never public |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | PublicationPolicy |
| Persistence | public_pages+public_page_revisions |
| Requirements | WEB-001, WEB-002, WEB-007, WEB-008, WEB-012 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| save_draft(content:PageDraft)->PageDraftSaved | Save draft | content:PageDraft | PageDraftSaved | InvalidState, InvariantViolation, VersionConflict |
| publish(now:Instant)->PagePublished | Publish | now:Instant | PagePublished | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## ContactEnquiry

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / content |
| Responsibility | No child linking from untrusted public text; bounded content; restricted operations retention |
| Attributes | id:uuid;name:string;email:NormalizedEmail;message:string;status:EnquiryStatus |
| Invariants | No child linking from untrusted public text; bounded content; restricted operations retention |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Notification |
| Persistence | contact_enquiries |
| Requirements | WEB-009 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| mark_handled(now:Instant)->EnquiryHandled | Mark handled | now:Instant | EnquiryHandled | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Program

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / curriculum |
| Responsibility | Optional course grouping; archive retains referenced courses |
| Attributes | id:uuid;slug:Slug;title:string;summary:string;status:PublicationStatus |
| Invariants | Optional course grouping; archive retains referenced courses |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Course |
| Persistence | programs |
| Requirements | ADM-007, LRN-001, PAR-007, WEB-003, WEB-004 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| update(title:string,summary:string)->ProgramUpdated | Update | title:string,summary:string | ProgramUpdated | InvalidState, InvariantViolation, VersionConflict |
| publish()->ProgramPublished | Publish | none | ProgramPublished | InvalidState, InvariantViolation, VersionConflict |
| archive()->ProgramArchived | Archive | none | ProgramArchived | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Course

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / curriculum |
| Responsibility | Reusable content, no session schedule; public course needs ready published revision |
| Attributes | id:uuid;program_id:uuid?;slug:Slug;title:string;age_band:AgeBand;duration_weeks:int;current_revision_id:uuid?;status:PublicationStatus |
| Invariants | Reusable content, no session schedule; public course needs ready published revision |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Program, CurriculumRevision |
| Persistence | courses |
| Requirements | ADM-007, LRN-001, PAR-007, WEB-003, WEB-004 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| publish(revision:CurriculumRevision)->CoursePublished | Publish | revision:CurriculumRevision | CoursePublished | InvalidState, InvariantViolation, VersionConflict |
| revise_metadata(changes:CourseMetadata)->CourseUpdated | Revise metadata | changes:CourseMetadata | CourseUpdated | InvalidState, InvariantViolation, VersionConflict |
| archive()->CourseArchived | Archive | none | CourseArchived | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## CurriculumRevision

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / curriculum |
| Responsibility | Published content immutable; stable reference IDs belong to same revision; cohort pin cannot be silently upgraded |
| Attributes | id:uuid;course_id:uuid;number:int;status:RevisionStatus;modules:CourseModule[];resources:LearningResource[] |
| Invariants | Published content immutable; stable reference IDs belong to same revision; cohort pin cannot be silently upgraded |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | CourseModule, Lesson, LessonBlock, LearningResource, Quiz, Assignment |
| Persistence | curriculum_revisions |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| add_module(module:CourseModule)->ModuleAdded | Add module | module:CourseModule | ModuleAdded | InvalidState, InvariantViolation, VersionConflict |
| reorder(ids:tuple[uuid])->RevisionReordered | Reorder | ids:tuple[uuid] | RevisionReordered | InvalidState, InvariantViolation, VersionConflict |
| publish(report:PublicationReport)->RevisionPublished | Publish | report:PublicationReport | RevisionPublished | InvalidState, InvariantViolation, VersionConflict |
| clone(new_id:uuid)->CurriculumRevision | Clone | new_id:uuid | CurriculumRevision | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, CAPACITY_BELOW_COMMITMENTS, CONTENT_UNRELEASED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RESOURCE_IN_USE, SCHEDULE_CONFLICT, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## CourseModule

| Metadata | Contract |
| --- | --- |
| Type / module | entity / curriculum |
| Responsibility | Position unique in revision; module release offset nonnegative; mutates through draft revision |
| Attributes | id:uuid;revision_id:uuid;title:string;position:int;release_offset_days:int;lessons:Lesson[] |
| Invariants | Position unique in revision; module release offset nonnegative; mutates through draft revision |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | CurriculumRevision, Lesson |
| Persistence | course_modules |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| rename(title:string)->None | Rename | title:string | None | InvalidState, InvariantViolation, VersionConflict |
| move(position:int)->None | Move | position:int | None | InvalidState, InvariantViolation, VersionConflict |
| add_lesson(lesson:Lesson)->None | Add lesson | lesson:Lesson | None | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, CONTENT_UNRELEASED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Lesson

| Metadata | Contract |
| --- | --- |
| Type / module | entity / curriculum |
| Responsibility | Ordered within module; release >= module gate; mutation through draft revision |
| Attributes | id:uuid;module_id:uuid;title:string;position:int;release_offset_days:int;required_for_completion:bool;blocks:LessonBlock[] |
| Invariants | Ordered within module; release >= module gate; mutation through draft revision |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | LessonBlock, CourseModule |
| Persistence | lessons |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| replace_blocks(blocks:tuple[LessonBlock])->None | Replace blocks | blocks:tuple[LessonBlock] | None | InvalidState, InvariantViolation, VersionConflict |
| set_release(offset:int)->None | Set release | offset:int | None | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, CONTENT_UNRELEASED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## LessonBlock

| Metadata | Contract |
| --- | --- |
| Type / module | discriminated value composition / curriculum |
| Responsibility | Exactly typed payload per kind; sanitize rich text; accessible image/video; references same revision |
| Attributes | id:uuid;lesson_id:uuid;position:int;kind:BlockKind;content:BlockContent;required_for_completion:bool |
| Invariants | Exactly typed payload per kind; sanitize rich text; accessible image/video; references same revision |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Lesson, LearningResource, Quiz, Assignment |
| Persistence | lesson_blocks |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| validate(context:RevisionReferences)->ValidationResult | Validate | context:RevisionReferences | ValidationResult | InvalidState, InvariantViolation, VersionConflict |
| referenced_assets()->frozenset[uuid] | Referenced assets | none | frozenset[uuid] | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, CONTENT_UNRELEASED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## LearningResource

| Metadata | Contract |
| --- | --- |
| Type / module | entity / curriculum |
| Responsibility | Exactly one scanned asset or approved HTTPS resource; immutable after revision published |
| Attributes | id:uuid;revision_id:uuid;title:string;kind:ResourceKind;asset_id:uuid?;external_url:ApprovedUrl?;status:ResourceStatus |
| Invariants | Exactly one scanned asset or approved HTTPS resource; immutable after revision published |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | FileAsset, CurriculumRevision |
| Persistence | learning_resources |
| Requirements | ADM-009, LRN-005, STU-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| replace_source(source:ResourceSource)->None | Replace source | source:ResourceSource | None | InvalidState, InvariantViolation, VersionConflict |
| validate_ready(asset:FileAsset?)->ValidationResult | Validate ready | asset:FileAsset? | ValidationResult | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, CONTENT_UNRELEASED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Cohort

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / delivery |
| Responsibility | Scheduled delivery of one published pinned revision; cannot reduce seats below holds+active; fees external |
| Attributes | id:uuid;course_id:uuid;revision_id:uuid;capacity:int;status:CohortStatus;timezone:IanaZone;starts_at:Instant;ends_at:Instant;enrolment_window:TimeRange |
| Invariants | Scheduled delivery of one published pinned revision; cannot reduce seats below holds+active; fees external |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Course, CurriculumRevision, ClassSession, Enrolment |
| Persistence | cohorts |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| open(ready:LaunchReadiness)->CohortOpened | Open | ready:LaunchReadiness | CohortOpened | InvalidState, InvariantViolation, VersionConflict |
| change_capacity(capacity:int,committed:int)->CapacityChanged | Change capacity | capacity:int,committed:int | CapacityChanged | InvalidState, InvariantViolation, VersionConflict |
| transition(status:CohortStatus)->CohortChanged | Transition | status:CohortStatus | CohortChanged | InvalidState, InvariantViolation, VersionConflict |
| cancel(reason:Reason)->CohortCancelled | Cancel | reason:Reason | CohortCancelled | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: CAPACITY_BELOW_COMMITMENTS, DST_AMBIGUOUS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, RESCHEDULE_WINDOW_CLOSED, SCHEDULE_CONFLICT, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## ClassSession

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / delivery |
| Responsibility | One occurrence; UTC end>start; no independent external calendar authority; cancelled cannot join |
| Attributes | id:uuid;cohort_id:uuid;lesson_id:uuid?;starts_at:Instant;ends_at:Instant;timezone:IanaZone;local_start:LocalDateTime;utc_offset_minutes:int;status:SessionStatus;version:int |
| Invariants | One occurrence; UTC end>start; no independent external calendar authority; cancelled cannot join |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Cohort, TeacherAssignment, IntegrationBinding |
| Persistence | class_sessions |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011, PAR-009, STU-013, TCH-005, TCH-006, WEB-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| reschedule(slot:TimeSlot,permit:SchedulePermit)->SessionRescheduled | Reschedule | slot:TimeSlot,permit:SchedulePermit | SessionRescheduled | InvalidState, InvariantViolation, VersionConflict |
| cancel(reason:Reason)->SessionCancelled | Cancel | reason:Reason | SessionCancelled | InvalidState, InvariantViolation, VersionConflict |
| complete(now:Instant)->SessionCompleted | Complete | now:Instant | SessionCompleted | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: DST_AMBIGUOUS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, JOIN_WINDOW_CLOSED, NOT_FOUND, PROVIDER_UNAVAILABLE, RESCHEDULE_WINDOW_CLOSED, SCHEDULE_CONFLICT, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## TeacherAssignment

| Metadata | Contract |
| --- | --- |
| Type / module | entity / delivery |
| Responsibility | Session belongs to cohort; teacher active; grants education only; revocation immediate |
| Attributes | id:uuid;teacher_id:uuid;cohort_id:uuid;session_id:uuid?;role:TeachingRole;active_from:Instant;active_until:Instant? |
| Invariants | Session belongs to cohort; teacher active; grants education only; revocation immediate |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | TeacherProfile, Cohort, ClassSession |
| Persistence | teacher_assignments |
| Requirements | ADM-015, CLS-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| covers(session:ClassSession,now:Instant)->bool | Covers | session:ClassSession,now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |
| revoke(now:Instant,reason:Reason)->AssignmentRevoked | Revoke | now:Instant,reason:Reason | AssignmentRevoked | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_ASSIGNMENT_EXISTS, CAPACITY_BELOW_COMMITMENTS, DST_AMBIGUOUS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, RESCHEDULE_WINDOW_CLOSED, SCHEDULE_CONFLICT, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Enrolment

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / enrolment |
| Responsibility | One active/held child-cohort pair; hold30m; only authoritative verified payment activates; late no-seat payment becomes exception |
| Attributes | id:uuid;student_id:uuid;cohort_id:uuid;status:EnrolmentStatus;hold_expires_at:Instant?;access_ends_at:Instant?;version:int |
| Invariants | One active/held child-cohort pair; hold30m; only authoritative verified payment activates; late no-seat payment becomes exception PAID_EXCEPTION allocation/refund is explicit serialized admin resolution; no automatically competing refund. |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | StudentProfile, Cohort, Payment |
| Persistence | enrolments |
| Requirements | ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| reserve(expires:Instant)->SeatHeld | Reserve | expires:Instant | SeatHeld | InvalidState, InvariantViolation, VersionConflict |
| activate(proof:VerifiedPayment,seat:CapacityPermit)->EnrolmentActivated | Activate | proof:VerifiedPayment,seat:CapacityPermit | EnrolmentActivated | InvalidState, InvariantViolation, VersionConflict |
| expire(now:Instant)->HoldExpired | Expire | now:Instant | HoldExpired | InvalidState, InvariantViolation, VersionConflict |
| cancel(reason:Reason,access_end:Instant?)->EnrolmentCancelled | Cancel | reason:Reason,access_end:Instant? | EnrolmentCancelled | InvalidState, InvariantViolation, VersionConflict |
| complete(evidence:CompletionEvidence)->EnrolmentCompleted | Complete | evidence:CompletionEvidence | EnrolmentCompleted | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_OUTCOME_UNKNOWN, PROVIDER_UNAVAILABLE, REFUND_EXCEEDS_BALANCE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## AttendanceRecord

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / delivery |
| Responsibility | One row per enrolled student/session; status valid; change reason audit; no sensitive note storage |
| Attributes | id:uuid;session_id:uuid;student_id:uuid;status:AttendanceStatus;minutes_attended:int?;recorded_by:uuid;version:int |
| Invariants | One row per enrolled student/session; status valid; change reason audit; no sensitive note storage |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | ClassSession, Enrolment |
| Persistence | attendance_records |
| Requirements | ADM-017, CLS-010, PAR-010, STU-015, TCH-007, TCH-008 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| record(status:AttendanceStatus,minutes:int?,actor:uuid)->AttendanceRecorded | Record | status:AttendanceStatus,minutes:int?,actor:uuid | AttendanceRecorded | InvalidState, InvariantViolation, VersionConflict |
| amend(status:AttendanceStatus,reason:Reason)->AttendanceAmended | Amend | status:AttendanceStatus,reason:Reason | AttendanceAmended | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Quiz

| Metadata | Contract |
| --- | --- |
| Type / module | entity / assessment |
| Responsibility | Revision immutable when published; pass0–100; attempts1–5 default3; default pass70 |
| Attributes | id:uuid;lesson_id:uuid;title:string;pass_percent:int;max_attempts:int;questions:QuizQuestion[] |
| Invariants | Revision immutable when published; pass0–100; attempts1–5 default3; default pass70 |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | QuizQuestion, CurriculumRevision |
| Persistence | quizzes |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003, STU-007 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| replace_questions(questions:tuple[QuizQuestion])->None | Replace questions | questions:tuple[QuizQuestion] | None | InvalidState, InvariantViolation, VersionConflict |
| snapshot()->QuizSnapshot | Snapshot | none | QuizSnapshot | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ATTEMPT_ALREADY_SUBMITTED, ATTEMPT_LIMIT_REACHED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## QuizQuestion

| Metadata | Contract |
| --- | --- |
| Type / module | entity / assessment |
| Responsibility | Single/multiple choice; correct IDs are in own options; at least2 options; keys never learner projected |
| Attributes | id:uuid;quiz_id:uuid;prompt:string;kind:QuestionKind;options:QuizOption[];correct_ids:frozenset[uuid];points:int;explanation:string |
| Invariants | Answer key valid within own question; approved explanation required before publication; release feedback only on own submitted attempt. |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Quiz |
| Persistence | quiz_questions+quiz_options |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003, STU-007 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| score(selection:frozenset[uuid])->int | Score | selection:frozenset[uuid] | int | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ATTEMPT_ALREADY_SUBMITTED, ATTEMPT_LIMIT_REACHED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## QuizAttempt

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / assessment |
| Responsibility | One in-progress attempt per quiz/enrolment; attempt count locked; submitted immutable; formative score released automatically |
| Attributes | id:uuid;quiz_id:uuid;student_id:uuid;enrolment_id:uuid;attempt_number:int;snapshot:QuizSnapshot;answers:tuple[QuizAnswer];status:AttemptStatus;result:QuizScore? |
| Invariants | One in-progress attempt per quiz/enrolment; attempt count locked; submitted immutable; formative score released automatically |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Quiz, Enrolment |
| Persistence | quiz_attempts+quiz_answers |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003, STU-007 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| save_answers(answers:tuple[QuizAnswer])->AttemptSaved | Save answers | answers:tuple[QuizAnswer] | AttemptSaved | InvalidState, InvariantViolation, VersionConflict |
| submit(now:Instant)->QuizAttemptSubmitted | Submit | now:Instant | QuizAttemptSubmitted | InvalidState, InvariantViolation, VersionConflict |
| release()->QuizResultReleased | Release | none | QuizResultReleased | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ATTEMPT_ALREADY_SUBMITTED, ATTEMPT_LIMIT_REACHED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Assignment

| Metadata | Contract |
| --- | --- |
| Type / module | entity / assessment |
| Responsibility | Curriculum-owned immutable definition; cohort closure is separate delivery rule; late accepted until cohort complete/closed |
| Attributes | id:uuid;lesson_id:uuid;kind:AssignmentKind;instructions:string;rubric:string;max_score:int;passing_score:int;due_offset_days:int?;allow_resubmission:bool |
| Invariants | Curriculum-owned immutable definition; cohort closure is separate delivery rule; late accepted until cohort complete/closed |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Submission, CurriculumRevision |
| Persistence | assignments+assignment_delivery_rules |
| Requirements | ADM-011, ASM-004, STU-008, TCH-010 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| validate_submission_window(cohort:Cohort,now:Instant,closed:bool)->SubmissionWindow | Validate submission window | cohort:Cohort,now:Instant,closed:bool | SubmissionWindow | InvalidState, InvariantViolation, VersionConflict |
| mark_delivery_closed(cohort_id:uuid,reason:Reason)->AssignmentClosed | Mark delivery closed | cohort_id:uuid,reason:Reason | AssignmentClosed | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Submission

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / assessment |
| Responsibility | Submitted work immutable; file ready+own; one current draft; returned work creates new attempt preserving chain |
| Attributes | id:uuid;assignment_id:uuid;student_id:uuid;enrolment_id:uuid;attempt_number:int;body:string?;asset_ids:tuple[uuid];status:SubmissionStatus;late:bool |
| Invariants | Submitted work immutable; file ready+own; one current draft; returned work creates new attempt preserving chain |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Assignment, FileAsset, Assessment |
| Persistence | submissions+submission_assets |
| Requirements | ASM-005, STU-009, STU-010 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| save_draft(body:string?,assets:tuple[ReadyFileRef])->SubmissionSaved | Save draft | body:string?,assets:tuple[ReadyFileRef] | SubmissionSaved | InvalidState, InvariantViolation, VersionConflict |
| submit(window:SubmissionWindow)->SubmissionSubmitted | Submit | window:SubmissionWindow | SubmissionSubmitted | InvalidState, InvariantViolation, VersionConflict |
| return_for_revision(reason:Reason)->SubmissionReturned | Return for revision | reason:Reason | SubmissionReturned | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, ASSIGNMENT_CLOSED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Assessment

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / assessment |
| Responsibility | Score bounded; ties specific submitted version; release deliberate; corrections preserve history and recompute completion |
| Attributes | id:uuid;submission_id:uuid;assessor_id:uuid;score:int?;max_score:int;rubric_comment:string?;status:AssessmentStatus;released_at:Instant? |
| Invariants | Score bounded; ties specific submitted version; release deliberate; corrections preserve history and recompute completion |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Submission, ReleasePolicy |
| Persistence | assessments+assessment_revisions |
| Requirements | ADM-012, ASM-006, ASM-007, PAR-013, STU-011, TCH-011, TCH-012 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| mark(score:int,comment:string)->AssessmentSaved | Mark | score:int,comment:string | AssessmentSaved | InvalidState, InvariantViolation, VersionConflict |
| release(now:Instant)->AssessmentReleased | Release | now:Instant | AssessmentReleased | InvalidState, InvariantViolation, VersionConflict |
| withdraw(reason:Reason)->AssessmentWithdrawn | Withdraw | reason:Reason | AssessmentWithdrawn | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## TeacherFeedback

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / assessment |
| Responsibility | Draft private; release only current teaching/admin education authority; no finance or private messaging channel |
| Attributes | id:uuid;student_id:uuid;cohort_id:uuid;submission_id:uuid?;message:string;author_id:uuid;status:FeedbackStatus |
| Invariants | Draft private; release only current teaching/admin education authority; no finance or private messaging channel |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | TeachingAccessPolicy, ReleasePolicy |
| Persistence | teacher_feedback+feedback_revisions |
| Requirements | ADM-019, ASM-008, PAR-012, STU-012, TCH-013 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| revise(message:string)->FeedbackSaved | Revise | message:string | FeedbackSaved | InvalidState, InvariantViolation, VersionConflict |
| release(now:Instant)->FeedbackReleased | Release | now:Instant | FeedbackReleased | InvalidState, InvariantViolation, VersionConflict |
| withdraw(reason:Reason)->FeedbackWithdrawn | Withdraw | reason:Reason | FeedbackWithdrawn | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## ActivityCompletion

| Metadata | Contract |
| --- | --- |
| Type / module | entity / learning |
| Responsibility | Own released lesson/activity; one row per completion key; no graded score |
| Attributes | enrolment_id:uuid;lesson_id:uuid;block_id:uuid?;completed:bool;reflection:string?;completed_at:Instant? |
| Invariants | Own released lesson/activity; one row per completion key; no graded score |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | StudentProgress, Lesson |
| Persistence | activity_completions |
| Requirements | LRN-006, STU-006 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| record(completed:bool,reflection:string?,now:Instant)->ActivityCompleted | Record | completed:bool,reflection:string?,now:Instant | ActivityCompleted | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## StudentProgress

| Metadata | Contract |
| --- | --- |
| Type / module | projection aggregate / learning |
| Responsibility | Derived from authoritative evidence; no arbitrary percentage setter; ignore cancelled sessions; >=80% delivered attendance and all required items |
| Attributes | enrolment_id:uuid;required_counts:RequiredItemCounts;completed_counts:RequiredItemCounts;attendance:AttendanceCounts;status:ProgressStatus;source_version:int;completion_basis:CompletionBasis;active_override_id:uuid? |
| Invariants | Derived counts and percentage cannot be manually rewritten. Standard evidence or explicit active evidenced completion override determines certificate eligibility. |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | ActivityCompletion, Assessment, QuizAttempt, AttendanceRecord, CompletionPolicy, CompletionOverride |
| Persistence | student_progress |
| Requirements | ADM-018, LRN-007, LRN-008, PAR-011, STU-016, TCH-014 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| recompute(evidence:ProgressEvidence,policy:CompletionPolicy)->ProgressRecomputed | Recompute | evidence:ProgressEvidence,policy:CompletionPolicy | ProgressRecomputed | InvalidState, InvariantViolation, VersionConflict |
| is_complete()->bool | Is complete | none | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Certificate

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / learning |
| Responsibility | One current certificate per enrolment; issue only eligible; immutable display snapshot; revoked retained; no public child lookup |
| Attributes | id:uuid;student_id:uuid;enrolment_id:uuid;verification_code:string;name_snapshot:string;course_title_snapshot:string;status:CertificateStatus;asset_id:uuid?;replaces_id:uuid? |
| Invariants | One current certificate per enrolment; issue only eligible; immutable display snapshot; revoked retained; no public child lookup |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | StudentProgress, FileAsset |
| Persistence | certificates |
| Requirements | ADM-020, LRN-009, LRN-010, PAR-014, STU-017 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| issue(eligibility:CompletionEvidence)->CertificateRequested | Issue | eligibility:CompletionEvidence | CertificateRequested | InvalidState, InvariantViolation, VersionConflict |
| attach_render(asset:ReadyFileRef)->CertificateIssued | Attach render | asset:ReadyFileRef | CertificateIssued | InvalidState, InvariantViolation, VersionConflict |
| revoke(reason:Reason)->CertificateRevoked | Revoke | reason:Reason | CertificateRevoked | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: COMPLETION_NOT_ELIGIBLE, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Money

| Metadata | Contract |
| --- | --- |
| Type / module | value object / billing |
| Responsibility | AUD only at launch; integer minor units >=0; addition same currency |
| Attributes | amount_minor:int;currency:Currency |
| Invariants | AUD only at launch; integer minor units >=0; addition same currency |
| Authorization | Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied. |
| Dependencies / collaborators | Price, Payment, Refund |
| Persistence | amount_minor+currency columns |
| Requirements | ADM-024, PAY-001 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| add(other:Money)->Money | Add | other:Money | Money | InvalidState, InvariantViolation, VersionConflict |
| subtract(other:Money)->Money | Subtract | other:Money | Money | InvalidState, InvariantViolation, VersionConflict |
| covers(other:Money)->bool | Covers | other:Money | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_OUTCOME_UNKNOWN, PROVIDER_UNAVAILABLE, REFUND_EXCEEDS_BALANCE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Price

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / billing |
| Responsibility | No overlapping active fee range for same target; cohort override wins; old purchases immutable |
| Attributes | id:uuid;course_id:uuid;cohort_id:uuid?;money:Money;tax_treatment:TaxTreatment;tax_rate_basis_points:int;effective_range:TimeRange |
| Invariants | No overlapping active fee range for same target; cohort override wins; old purchases immutable |
| Authorization | Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied. |
| Dependencies / collaborators | Money, Course, Cohort |
| Persistence | prices |
| Requirements | ADM-024, PAY-001 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| snapshot(approved_tax:TaxConfiguration)->PriceSnapshot | Snapshot | approved_tax:TaxConfiguration | PriceSnapshot | InvalidState, InvariantViolation, VersionConflict |
| retire(at:Instant)->PriceRetired | Retire | at:Instant | PriceRetired | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_UNAVAILABLE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Payment

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / billing |
| Responsibility | Financial truth append-only event history; unique provider IDs; success server verified; ambiguous outcome does not retry new payment blindly |
| Attributes | id:uuid;family_id:uuid;enrolment_id:uuid;price_snapshot:PriceSnapshot;provider_checkout_id:string?;provider_payment_id:string?;status:PaymentStatus;refunded_minor:int;version:int |
| Invariants | Financial truth append-only event history; unique provider IDs; success server verified; ambiguous outcome does not retry new payment blindly |
| Authorization | Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied. |
| Dependencies / collaborators | Enrolment, Money, Refund, Receipt |
| Persistence | payments+payment_events |
| Requirements | ADM-025, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| bind_checkout(reference:CheckoutRef)->CheckoutBound | Bind checkout | reference:CheckoutRef | CheckoutBound | InvalidState, InvariantViolation, VersionConflict |
| record_verified_state(state:VerifiedProviderPayment)->PaymentUpdated | Record verified state | state:VerifiedProviderPayment | PaymentUpdated | InvalidState, InvariantViolation, VersionConflict |
| flag_exception(code:PaymentException)->PaymentExceptionRaised | Flag exception | code:PaymentException | PaymentExceptionRaised | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_OUTCOME_UNKNOWN, PROVIDER_UNAVAILABLE, REFUND_EXCEEDS_BALANCE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Refund

| Metadata | Contract |
| --- | --- |
| Type / module | entity / billing |
| Responsibility | Pending+successful refunds <= captured; provider outcome ambiguity reconciled before retry; finance privilege only |
| Attributes | id:uuid;payment_id:uuid;amount:Money;provider_refund_id:string?;idempotency_key:uuid;access_disposition:AccessDisposition;status:RefundStatus |
| Invariants | Pending+successful refunds <= captured; provider outcome ambiguity reconciled before retry; finance privilege only Educational disposition is KEEP or CANCEL; no date-based refund mode. |
| Authorization | Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied. |
| Dependencies / collaborators | Payment, Enrolment |
| Persistence | refunds |
| Requirements | ADM-026, PAY-008 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| request(available:Money)->RefundRequested | Request | available:Money | RefundRequested | InvalidState, InvariantViolation, VersionConflict |
| confirm(provider:VerifiedRefund)->RefundSucceeded | Confirm | provider:VerifiedRefund | RefundSucceeded | InvalidState, InvariantViolation, VersionConflict |
| fail(code:ProviderFailure)->RefundFailed | Fail | code:ProviderFailure | RefundFailed | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, PROVIDER_OUTCOME_UNKNOWN, REFUND_EXCEEDS_BALANCE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Receipt

| Metadata | Contract |
| --- | --- |
| Type / module | entity / billing |
| Responsibility | Immutable merchant/tax/purchase snapshot; legal content approval gate; no editing paid document |
| Attributes | id:uuid;payment_id:uuid;type:DocumentType;number:string;merchant_snapshot:MerchantIdentity;purchaser_snapshot:string;amount:Money;tax:Money;asset_id:uuid? |
| Invariants | Immutable merchant/tax/purchase snapshot; legal content approval gate; no editing paid document |
| Authorization | Authorize at application boundary before invoking behavior; Finance scope only; teacher/student denied. |
| Dependencies / collaborators | Payment, FileAsset |
| Persistence | purchase_documents |
| Requirements | ADM-025, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| issue(verified_payment:Payment,merchant:MerchantIdentity)->ReceiptIssued | Issue | verified_payment:Payment,merchant:MerchantIdentity | ReceiptIssued | InvalidState, InvariantViolation, VersionConflict |
| attach_asset(asset:ReadyFileRef)->None | Attach asset | asset:ReadyFileRef | None | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_UNAVAILABLE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Event

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / communication |
| Responsibility | Explicit audience; public events contain no learner names; domain schedule authoritative |
| Attributes | id:uuid;title:string;description:string;time:TimeSlot;audience:Audience;status:EventStatus |
| Invariants | Explicit audience; public events contain no learner names; domain schedule authoritative |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | AudiencePolicy, IntegrationBinding |
| Persistence | events |
| Requirements | ADM-021, PAR-015 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| publish()->EventPublished | Publish | none | EventPublished | InvalidState, InvariantViolation, VersionConflict |
| reschedule(slot:TimeSlot)->EventRescheduled | Reschedule | slot:TimeSlot | EventRescheduled | InvalidState, InvariantViolation, VersionConflict |
| cancel(reason:Reason)->EventCancelled | Cancel | reason:Reason | EventCancelled | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Announcement

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / communication |
| Responsibility | Publish audience resolved from current relations; withdrawn unreadable; no messaging threads |
| Attributes | id:uuid;title:string;body:string;audience:Audience;status:AnnouncementStatus;published_at:Instant? |
| Invariants | Publish audience resolved from current relations; withdrawn unreadable; no messaging threads |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | AudiencePolicy, Notification |
| Persistence | announcements |
| Requirements | COM-008, STU-018 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| publish(now:Instant)->AnnouncementPublished | Publish | now:Instant | AnnouncementPublished | InvalidState, InvariantViolation, VersionConflict |
| revise_draft(body:string)->AnnouncementSaved | Revise draft | body:string | AnnouncementSaved | InvalidState, InvariantViolation, VersionConflict |
| withdraw(reason:Reason)->AnnouncementWithdrawn | Withdraw | reason:Reason | AnnouncementWithdrawn | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## Notification

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / communication |
| Responsibility | Unique recipient/source/kind; role-filtered allowed deep link; actor owns read state |
| Attributes | id:uuid;recipient_id:uuid;kind:NotificationKind;source_event_id:uuid;title:string;body:string;read_at:Instant?;portal_path:PortalPath |
| Invariants | Unique recipient/source/kind; role-filtered allowed deep link; actor owns read state |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | NotificationDelivery, Account |
| Persistence | notifications |
| Requirements | ADM-022, COM-007, PAR-016, TCH-015 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| mark_read(read:bool,now:Instant)->NotificationReadChanged | Mark read | read:bool,now:Instant | NotificationReadChanged | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## NotificationDelivery

| Metadata | Contract |
| --- | --- |
| Type / module | entity / communication |
| Responsibility | Durable dedupe beyond provider24h; optional prefs cannot suppress security/payment essentials |
| Attributes | id:uuid;notification_id:uuid;channel:DeliveryChannel;status:DeliveryStatus;attempts:int;provider_message_id:string?;dedupe_key:string |
| Invariants | Durable dedupe beyond provider24h; optional prefs cannot suppress security/payment essentials |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Notification |
| Persistence | notification_deliveries |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, PAR-003, PAR-015, STU-018 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| claim(lease:Lease)->DeliveryClaimed | Claim | lease:Lease | DeliveryClaimed | InvalidState, InvariantViolation, VersionConflict |
| record_sent(provider_id:string,now:Instant)->DeliverySent | Record sent | provider_id:string,now:Instant | DeliverySent | InvalidState, InvariantViolation, VersionConflict |
| fail(code:ProviderFailure,retry_at:Instant?)->DeliveryFailed | Fail | code:ProviderFailure,retry_at:Instant? | DeliveryFailed | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## FileAsset

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / files |
| Responsibility | Quarantine unavailable; immutable promotion only after successful actual-type/checksum/malware validation; key never public; hold prevents purge |
| Attributes | id:uuid;owner_id:uuid;purpose:FilePurpose;context_id:uuid;staging_key:string;immutable_key:string?;mime:string;size:int;checksum:string;status:FileStatus;hold:bool |
| Invariants | Quarantine unavailable; immutable promotion only after successful actual-type/checksum/malware validation; key never public; hold prevents purge |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | FileAccessPolicy |
| Persistence | file_assets |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| begin_scan()->ScanStarted | Begin scan | none | ScanStarted | InvalidState, InvariantViolation, VersionConflict |
| promote(result:CleanScan,key:ImmutableObjectKey)->AssetReady | Promote | result:CleanScan,key:ImmutableObjectKey | AssetReady | InvalidState, InvariantViolation, VersionConflict |
| reject(reason:ScanFailure)->AssetRejected | Reject | reason:ScanFailure | AssetRejected | InvalidState, InvariantViolation, VersionConflict |
| mark_deleted(decision:RetentionDecision)->AssetDeleted | Mark deleted | decision:RetentionDecision | AssetDeleted | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_GUARDIAN_REQUIRED, ASSET_NOT_READY, ASSIGNMENT_CLOSED, FILE_TOO_LARGE, FILE_TYPE_DENIED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LEGAL_HOLD, NOT_FOUND, RESOURCE_IN_USE, UNAUTHENTICATED, UPLOAD_MISMATCH, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## AuditRecord

| Metadata | Contract |
| --- | --- |
| Type / module | immutable record / operations |
| Responsibility | Append-only; secrets/raw PII excluded; separate DB writer privilege; no application delete |
| Attributes | id:uuid;actor_id:uuid?;action:string;resource_type:string;resource_id:uuid?;occurred_at:Instant;request_id:uuid;outcome:AuditOutcome;reason:string? |
| Invariants | Append-only; secrets/raw PII excluded; separate DB writer privilege; no application delete |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Account |
| Persistence | audit_records |
| Requirements | ADM-029, SEC-007 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| redacted_view(scope:AuditScope)->AuditSummary | Redacted view | scope:AuditScope | AuditSummary | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VersionConflict.

## ApplicationSetting

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / operations |
| Responsibility | Closed typed key catalog; secrets are external references; sensitive values need approval; settings not generic arbitrary JSON behavior |
| Attributes | key:SettingKey;typed_value:SettingValue;approved:bool;approval_reference:string?;version:int |
| Invariants | Closed typed key catalog; secrets are external references; sensitive values need approval; settings not generic arbitrary JSON behavior |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | RoleGrant |
| Persistence | application_settings |
| Requirements | ADM-028 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| change(value:SettingValue,approval:ApprovalReference?)->SettingChanged | Change | value:SettingValue,approval:ApprovalReference? | SettingChanged | InvalidState, InvariantViolation, VersionConflict |
| approve(reference:ApprovalReference)->SettingApproved | Approve | reference:ApprovalReference | SettingApproved | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## IntegrationBinding

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / operations |
| Responsibility | Unique provider/resource; latest desired domain version wins; encrypted identifiers; host URL never persisted |
| Attributes | id:uuid;provider:Provider;resource_type:MirrorResourceType;resource_id:uuid;provider_id_ciphertext:bytes;desired_version:int;applied_version:int;status:SyncStatus |
| Invariants | Unique provider/resource; latest desired domain version wins; encrypted identifiers; host URL never persisted |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | ClassSession, Event |
| Persistence | integration_bindings |
| Requirements | OPS-003 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| schedule_sync(version:int)->SyncRequested | Schedule sync | version:int | SyncRequested | InvalidState, InvariantViolation, VersionConflict |
| mark_applied(version:int)->SyncApplied | Mark applied | version:int | SyncApplied | InvalidState, InvariantViolation, VersionConflict |
| record_failure(code:ProviderFailure)->SyncFailed | Record failure | code:ProviderFailure | SyncFailed | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, JOIN_WINDOW_CLOSED, NOT_FOUND, PROVIDER_UNAVAILABLE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## WebhookInbox

| Metadata | Contract |
| --- | --- |
| Type / module | immutable processing record / operations |
| Responsibility | Verify before processing; unique provider/event; unsupported signed event ignored safely; bounded encrypted retention |
| Attributes | id:uuid;provider:Provider;provider_event_id:string;received_at:Instant;verified:bool;payload_reference:EncryptedReference;status:InboxStatus |
| Invariants | Verify before processing; unique provider/event; unsupported signed event ignored safely; bounded encrypted retention |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Payment |
| Persistence | webhook_inbox |
| Requirements | PAY-004, PAY-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| claim(lease:Lease)->InboxClaimed | Claim | lease:Lease | InboxClaimed | InvalidState, InvariantViolation, VersionConflict |
| complete(outcome:ProcessingOutcome)->InboxProcessed | Complete | outcome:ProcessingOutcome | InboxProcessed | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_UNAVAILABLE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## OutboxEvent

| Metadata | Contract |
| --- | --- |
| Type / module | immutable delivery record / operations |
| Responsibility | Created in same transaction as business mutation; opaque IDs only; at-least-once dispatch and deduped consumption |
| Attributes | id:uuid;aggregate_type:string;aggregate_id:uuid;aggregate_version:int;event_type:string;payload:MinimalEventPayload;occurred_at:Instant;published_at:Instant? |
| Invariants | Created in same transaction as business mutation; opaque IDs only; at-least-once dispatch and deduped consumption |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | BackgroundJob |
| Persistence | outbox_events |
| Requirements | OPS-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| claim(lease:Lease)->OutboxClaimed | Claim | lease:Lease | OutboxClaimed | InvalidState, InvariantViolation, VersionConflict |
| mark_published(now:Instant)->None | Mark published | now:Instant | None | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## BackgroundJob

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / operations |
| Responsibility | Unique job kind/dedupe key; bounded exponential retry max8 attempts/24h; stale leases recover; immutable payload |
| Attributes | id:uuid;kind:JobKind;source_event_id:uuid?;dedupe_key:string;status:JobStatus;attempt_count:int;lease_until:Instant?;next_attempt_at:Instant? |
| Invariants | Unique job kind/dedupe key; bounded exponential retry max8 attempts/24h; stale leases recover; immutable payload |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | OutboxEvent |
| Persistence | background_jobs |
| Requirements | OPS-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| claim(now:Instant,lease_until:Instant)->JobClaimed | Claim | now:Instant,lease_until:Instant | JobClaimed | InvalidState, InvariantViolation, VersionConflict |
| succeed()->JobSucceeded | Succeed | none | JobSucceeded | InvalidState, InvariantViolation, VersionConflict |
| retry(code:Failure,next_at:Instant)->JobRetryScheduled | Retry | code:Failure,next_at:Instant | JobRetryScheduled | InvalidState, InvariantViolation, VersionConflict |
| dead_letter(code:Failure)->JobDeadLettered | Dead letter | code:Failure | JobDeadLettered | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## PrivacyRequest

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / family |
| Responsibility | Verified adult authority and explicit retention decision precede export/purge; holds respected; do not orphan child guardianship |
| Attributes | id:uuid;family_id:uuid;requester_id:uuid;student_id:uuid?;kind:PrivacyRequestKind;status:PrivacyStatus;verification_reference:string?;decision_reason:string? |
| Invariants | Verified adult authority and explicit retention decision precede export/purge; holds respected; do not orphan child guardianship |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Family, GuardianStudent, FileAsset |
| Persistence | privacy_requests+retention_holds |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| verify(evidence:VerificationRef)->PrivacyVerified | Verify | evidence:VerificationRef | PrivacyVerified | InvalidState, InvariantViolation, VersionConflict |
| approve(decision:RetentionDecision)->PrivacyApproved | Approve | decision:RetentionDecision | PrivacyApproved | InvalidState, InvariantViolation, VersionConflict |
| complete(result:PrivacyOutcome)->PrivacyCompleted | Complete | result:PrivacyOutcome | PrivacyCompleted | InvalidState, InvariantViolation, VersionConflict |
| reject(reason:Reason)->PrivacyRejected | Reject | reason:Reason | PrivacyRejected | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_GUARDIAN_REQUIRED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LEGAL_HOLD, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## FamilyOwnershipPolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / family |
| Responsibility | Require active explicit link for child and separate active family financial membership; no names/email matching |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | Require active explicit link for child and separate active family financial membership; no names/email matching |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Family, GuardianStudent, BillingMembership |
| Persistence | none; pure policy |
| Requirements | AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| authorize_student(principal:Principal,links:GuardianLinks,student:StudentProfile)->FamilyScope | Authorize student | principal:Principal,links:GuardianLinks,student:StudentProfile | FamilyScope | InvalidState, InvariantViolation, VersionConflict |
| authorize_billing(principal:Principal,memberships:BillingMemberships,family_id:uuid)->BillingScope | Authorize billing | principal:Principal,memberships:BillingMemberships,family_id:uuid | BillingScope | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_ENROLMENT_EXISTS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## TeachingAccessPolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / delivery |
| Responsibility | Teacher role plus active relevant assignment plus enrolled learner; financial actions denied before repository read |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | Teacher role plus active relevant assignment plus enrolled learner; financial actions denied before repository read |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | TeacherAssignment, Enrolment |
| Persistence | none; pure policy |
| Requirements | AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| authorize(principal:Principal,assignment:TeacherAssignment,enrolment:Enrolment,action:TeachingAction)->TeachingScope | Authorize | principal:Principal,assignment:TeacherAssignment,enrolment:Enrolment,action:TeachingAction | TeachingScope | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ACTIVE_ASSIGNMENT_EXISTS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, JOIN_WINDOW_CLOSED, NOT_FOUND, PROVIDER_UNAVAILABLE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## PublicationPolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / curriculum |
| Responsibility | All referenced objects same revision; accessible content and safe assets; no unresolved required settings |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | All referenced objects same revision; accessible content and safe assets; no unresolved required settings |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | CurriculumRevision, LessonBlock, FileAsset |
| Persistence | none; pure policy |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| validate(revision:CurriculumRevision,assets:ReadyAssets,settings:ApprovedSettings)->PublicationReport | Validate | revision:CurriculumRevision,assets:ReadyAssets,settings:ApprovedSettings | PublicationReport | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, CONTENT_UNRELEASED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, PUBLISH_VALIDATION_FAILED, RATE_LIMITED, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## ReleasePolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / learning |
| Responsibility | Pinned revision membership and active/completed entitlement and release time; draft marks never visible |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | Pinned revision membership and active/completed entitlement and release time; draft marks never visible |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Enrolment, CurriculumRevision, Assessment, TeacherFeedback |
| Persistence | none; pure policy |
| Requirements | AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-012, TCH-016 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| can_read(principal:Principal,enrolment:Enrolment,resource:LearningResourceState,now:Instant)->bool | Can read | principal:Principal,enrolment:Enrolment,resource:LearningResourceState,now:Instant | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, ASSIGNMENT_CLOSED, ATTEMPT_ALREADY_SUBMITTED, ATTEMPT_LIMIT_REACHED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RESOURCE_IN_USE, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## SchedulePolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / delivery |
| Responsibility | Teacher assigned future session at least24h; administrator reason for shorter notice; no conflict; valid DST resolution |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | Teacher assigned future session at least24h; administrator reason for shorter notice; no conflict; valid DST resolution |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | ClassSession, TeacherAssignment, Cohort |
| Persistence | none; pure policy |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011, PAR-009, STU-013, TCH-005, TCH-006, WEB-005 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| authorize_change(principal:Principal,session:ClassSession,new_slot:TimeSlot,conflicts:ScheduleConflicts,now:Instant)->SchedulePermit | Authorize change | principal:Principal,session:ClassSession,new_slot:TimeSlot,conflicts:ScheduleConflicts,now:Instant | SchedulePermit | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: DST_AMBIGUOUS, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RESCHEDULE_WINDOW_CLOSED, SCHEDULE_CONFLICT, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## CapacityPolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / enrolment |
| Responsibility | Run under cohort row lock; active+unexpired holds <= capacity; verified late payment never oversells |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | Run under cohort row lock; active+unexpired holds <= capacity; verified late payment never oversells |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | Cohort, Enrolment |
| Persistence | none; pure policy |
| Requirements | ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| reserve(capacity:int,active:int,unexpired_holds:int,now:Instant)->CapacityPermit | Reserve | capacity:int,active:int,unexpired_holds:int,now:Instant | CapacityPermit | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: AGE_INELIGIBLE, AGE_RECONFIRMATION_REQUIRED, ALREADY_ENROLLED, COHORT_FULL, EXCEPTION_ALREADY_RESOLVED, FORBIDDEN, HUMAN_APPROVAL_REQUIRED, INVALID_STATE, InvalidState, InvariantViolation, LAUNCH_CONFIGURATION_REQUIRED, NOT_FOUND, OVERLAPPING_PRICE_WINDOW, PROVIDER_UNAVAILABLE, REFUND_PENDING, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## CompletionPolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / learning |
| Responsibility | All required learning items satisfied and >=80% delivered attendance; no arbitrary progress edit; no zero-delivery completion |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | All required items plus >=80% delivered attendance make standard completion eligible. An active education_admin completion override with reason and verified evidence can independently confer eligibility without changing source records. |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | ActivityCompletion, QuizAttempt, Assessment, AttendanceRecord |
| Persistence | none; pure policy |
| Requirements | ADM-018, LRN-007, LRN-008, PAR-011, STU-016, TCH-014 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| evaluate(evidence:ProgressEvidence)->CompletionEvidence | Evaluate | evidence:ProgressEvidence | CompletionEvidence | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## AudiencePolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / communication |
| Responsibility | Only current intended audience; no cohort roster disclosure; relevant parent/student/teacher notices only |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | Target kind public/role/course/cohort plus explicit recipient role filter; course resolves eligible enrolments across its cohorts and current teachers; parent requires active child link; no recipient roster exposed. |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | GuardianStudent, TeacherAssignment, Enrolment |
| Persistence | none; pure policy |
| Requirements | COM-008, STU-018 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| resolve(audience:Audience,relationships:AudienceRelationships)->frozenset[RecipientId] | Resolve | audience:Audience,relationships:AudienceRelationships | frozenset[RecipientId] | InvalidState, InvariantViolation, VersionConflict |
| permits(principal:Principal,audience:Audience)->bool | Permits | principal:Principal,audience:Audience | bool | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## FileAccessPolicy

| Metadata | Contract |
| --- | --- |
| Type / module | domain policy / files |
| Responsibility | Ready state for download; owner draft for upload; release/guardian/assignment context; internal purpose excluded from learners |
| Attributes | no mutable attributes; explicit evaluation context |
| Invariants | Ready state for download; owner draft for upload; release/guardian/assignment context; internal purpose excluded from learners |
| Authorization | Authorize at application boundary before invoking behavior; Use scoped relationships and purpose-specific projections; object IDs alone grant nothing. |
| Dependencies / collaborators | FileAsset, Enrolment, GuardianStudent, TeacherAssignment |
| Persistence | none; pure policy |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| authorize(principal:Principal,asset:FileAsset,context:FileContext,action:FileAction)->FileScope | Authorize | principal:Principal,asset:FileAsset,context:FileContext,action:FileAction | FileScope | InvalidState, InvariantViolation, VersionConflict |

Domain failures additionally include: ASSET_NOT_READY, FILE_TOO_LARGE, FILE_TYPE_DENIED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, LEGAL_HOLD, NOT_FOUND, RESOURCE_IN_USE, UNAUTHENTICATED, UPLOAD_MISMATCH, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## CompletionOverride

| Metadata | Contract |
| --- | --- |
| Type / module | entity / learning |
| Responsibility | Evidence-backed administrative completion decision preserving source learning/attendance truth. |
| Attributes | id:uuid;enrolment_id:uuid;actor_id:uuid;reason:string;evidence_references:tuple[string];granted_at:Instant;revoked_at:Instant?;version:int |
| Invariants | Education-admin with recent MFA only; nonempty reason and verified evidence references mandatory; never changes grades or attendance. |
| Authorization | education_admin plus explicit evidence and reason; teacher cannot grant. |
| Dependencies / collaborators | StudentProgress, Certificate |
| Persistence | completion_overrides |
| Requirements | ADM-018, LRN-008, SEC-007 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| grant(actor:Principal,reason:Reason,evidence:tuple[VerifiedEvidence])->CompletionOverrideGranted | Grant audited exceptional completion eligibility | Education-admin actor, reason, verified evidence references | CompletionOverrideGranted | EvidenceRequired, Forbidden, InvalidState |
| revoke(reason:Reason,now:Instant)->CompletionOverrideRevoked | Revoke invalid exceptional decision and recompute certificate eligibility | Reason and current instant | CompletionOverrideRevoked | InvalidState |

Domain failures additionally include: COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED, FORBIDDEN, INVALID_STATE, InvalidState, InvariantViolation, NOT_FOUND, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## MfaFactor

| Metadata | Contract |
| --- | --- |
| Type / module | aggregate / identity |
| Responsibility | Durable replay-resistant mandatory staff second-factor lifecycle. |
| Attributes | id:uuid;account_id:uuid;secret_reference:EncryptedSecretRef;status:FactorStatus;last_accepted_step:int?;activated_at:Instant?;version:int |
| Invariants | Secret seed encrypted with versioned managed key; recovery codes hashed; challenge/setup tokens hashed, purpose/browser-bound and expiring; last TOTP timestep locked and monotonic; no full staff privileges before completion. |
| Authorization | Own staff account limited setup or authenticated challenge; secret material never API-returned except one-time provisioning URI. |
| Dependencies / collaborators | Account, Session |
| Persistence | mfa_factors |
| Requirements | AUTH-001, AUTH-002, AUTH-003, TCH-001, ADM-001, SEC-004 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| activate(proof:VerifiedTotpProof,now:Instant)->MfaActivated | Activate only after first valid proof | proof:VerifiedTotpProof,now:Instant | MfaActivated | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |
| accept_step(step:int)->TotpAccepted | Reject replay if step<=last accepted step | step:int | TotpAccepted | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |
| revoke(reason:Reason)->MfaRevoked | Revoke compromised factor and dependent sessions | reason:Reason | MfaRevoked | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |

Domain failures additionally include: ACCOUNT_SUSPENDED, FORBIDDEN, INVALID_CREDENTIALS, INVALID_STATE, InvalidState, InvariantViolation, MFA_ATTEMPTS_EXCEEDED, MFA_CHALLENGE_EXPIRED, MFA_REPLAY, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## RecoveryCode

| Metadata | Contract |
| --- | --- |
| Type / module | entity / identity |
| Responsibility | Durable replay-resistant mandatory staff second-factor lifecycle. |
| Attributes | id:uuid;factor_id:uuid;code_hash:bytes;consumed_at:Instant? |
| Invariants | Secret seed encrypted with versioned managed key; recovery codes hashed; challenge/setup tokens hashed, purpose/browser-bound and expiring; last TOTP timestep locked and monotonic; no full staff privileges before completion. |
| Authorization | Own staff account limited setup or authenticated challenge; secret material never API-returned except one-time provisioning URI. |
| Dependencies / collaborators | Account, Session |
| Persistence | mfa_recovery_codes |
| Requirements | AUTH-001, AUTH-002, AUTH-003, TCH-001, ADM-001, SEC-004 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| consume(proof:VerifiedRecoveryProof,now:Instant)->RecoveryCodeConsumed | Consume matching hashed recovery code once under row lock | proof:VerifiedRecoveryProof,now:Instant | RecoveryCodeConsumed | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |

Domain failures additionally include: ACCOUNT_SUSPENDED, FORBIDDEN, INVALID_CREDENTIALS, INVALID_STATE, InvalidState, InvariantViolation, MFA_ATTEMPTS_EXCEEDED, MFA_CHALLENGE_EXPIRED, MFA_REPLAY, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.

## MfaChallenge

| Metadata | Contract |
| --- | --- |
| Type / module | entity / identity |
| Responsibility | Durable replay-resistant mandatory staff second-factor lifecycle. |
| Attributes | id:uuid;account_id:uuid;token_hash:bytes;purpose:ChallengePurpose;expires_at:Instant;attempts:int;consumed_at:Instant?;browser_binding_hash:bytes |
| Invariants | Secret seed encrypted with versioned managed key; recovery codes hashed; challenge/setup tokens hashed, purpose/browser-bound and expiring; last TOTP timestep locked and monotonic; no full staff privileges before completion. |
| Authorization | Own staff account limited setup or authenticated challenge; secret material never API-returned except one-time provisioning URI. |
| Dependencies / collaborators | Account, Session |
| Persistence | mfa_challenges |
| Requirements | AUTH-001, AUTH-002, AUTH-003, TCH-001, ADM-001, SEC-004 |
| Implementation chunks | Resolve object name through CODE_BLUEPRINT and requirement-to-chunk mapping; lock requires nonempty assignment. |

| Public method | Purpose | Inputs | Output | Failures |
| --- | --- | --- | --- | --- |
| consume(proof:VerifiedSecondFactor,now:Instant)->ChallengeConsumed | Require correct purpose/browser/expiry and proof, consume once | proof:VerifiedSecondFactor,now:Instant | ChallengeConsumed | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |
| reject_attempt(now:Instant)->ChallengeAttemptRejected | Bound attempts and revoke challenge after5 failures | now:Instant | ChallengeAttemptRejected | InvalidMfaProof, MfaReplay, MfaChallengeExpired, MfaAttemptsExceeded |

Domain failures additionally include: ACCOUNT_SUSPENDED, FORBIDDEN, INVALID_CREDENTIALS, INVALID_STATE, InvalidState, InvariantViolation, MFA_ATTEMPTS_EXCEEDED, MFA_CHALLENGE_EXPIRED, MFA_REPLAY, NOT_FOUND, RATE_LIMITED, UNAUTHENTICATED, VALIDATION_ERROR, VERSION_CONFLICT, VersionConflict.
