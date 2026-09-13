# Backend application services

Status: DRAFT, scope 1.0 / architecture 1. Canonical structured contracts: [backend-catalog.json](backend-catalog.json). These are design contracts, not implemented classes or endpoints. Implementation ownership and requirement traceability are in CODE_BLUEPRINT.md and docs/planning/REQUIREMENT_TRACEABILITY.md.

## AuthenticationService

- **Module:** identity
- **Responsibility:** authentication
- **Objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001, WEB-011
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| register_parent | API_AUTH_REGISTERRequest → AccountView | Register guardian and create family | Email uniqueness; accepted current required policy versions; rate-limit by address/network. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE | API-AUTH-REGISTER |
| verify_email | API_AUTH_VERIFYRequest → Empty | Consume single-use email verification | Hashed token bound to account and purpose; 24h expiry. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE | API-AUTH-VERIFY |
| resend_verification | API_AUTH_RESENDRequest → Empty | Resend verification without account enumeration | Uniform response and throttled per identifier. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE | API-AUTH-RESEND |
| login | API_AUTH_LOGINRequest → AuthOutcomeView | Authenticate parent/staff/student | Credential and account status; staff MFA challenge before privileged session. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE, INVALID_CREDENTIALS, ACCOUNT_SUSPENDED | API-AUTH-LOGIN |
| verify_mfa | API_AUTH_MFARequest → SessionView | Complete staff MFA challenge | Short-lived challenge bound to browser, user and purpose. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE, INVALID_CREDENTIALS, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED | API-AUTH-MFA |
| enrol_mfa | API_AUTH_MFA_ENROLRequest → MfaSetupView | Create pending TOTP enrolment | Full staff session with recent password reauthentication OR unexpired staff-invitation MFA setup token; setup context permits only MFA setup operations. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED | API-AUTH-MFA-ENROL |
| confirm_mfa | API_AUTH_MFA_CONFIRMRequest → MfaActivationView | Activate TOTP and issue recovery codes once | Purpose-bound setup token plus valid first TOTP proof; consume setup token, activate staff account and full MFA session atomically. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED | API-AUTH-MFA-CONFIRM |
| request_password_reset | API_AUTH_RESET_REQUESTRequest → Empty | Request account recovery | Uniform response; adult verified email only; student recovery managed by guardian. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE | API-AUTH-RESET-REQUEST |
| reset_password | API_AUTH_RESETRequest → Empty | Reset adult password and revoke sessions | One-time hashed token, 30-minute lifetime; revocation transactional. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE | API-AUTH-RESET |
| get_session | API_AUTH_MERequest → SessionView | Get safe authenticated session identity | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-AUTH-ME |
| logout | API_AUTH_LOGOUTRequest → Empty | Revoke current session | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-AUTH-LOGOUT |
| accept_staff_invitation | API_AUTH_INVITE_ACCEPTRequest → StaffSetupSessionView | Accept staff invitation and require MFA setup | Single-use invitation token; no privilege upgrades from request. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE | API-AUTH-INVITE-ACCEPT |

## AccountService

- **Module:** identity
- **Responsibility:** accounts
- **Objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021, STU-019
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| change_password | API_ACCOUNT_PASSWORDRequest → Empty | Change own adult/staff password and revoke other sessions | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ACCOUNT-PASSWORD |
| list_sessions | API_ACCOUNT_SESSIONSRequest → DeviceSessionViewPage | List own devices | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ACCOUNT-SESSIONS |
| revoke_session | API_ACCOUNT_REVOKERequest → Empty | Revoke selected own device | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ACCOUNT-REVOKE |
| get_account | API_ACCOUNT_PROFILERequest → AccountView | Read own profile | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ACCOUNT-PROFILE |
| get_guardian_profile | API_PARENT_PROFILERequest → GuardianView | Read guardian contact/preferences | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-PROFILE |
| update_guardian_profile | API_PARENT_UPDATERequest → GuardianView | Update guardian contact/preferences | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-PARENT-UPDATE |
| request_email_change | API_PARENT_EMAIL_CHANGERequest → Empty | Begin verified contact email change | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. Reauthentication; new address never takes effect until verification. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-PARENT-EMAIL-CHANGE |
| confirm_email_change | API_PARENT_EMAIL_CONFIRMRequest → GuardianView | Confirm new email and notify old address | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-PARENT-EMAIL-CONFIRM |
| create_staff_invitation | API_ADMIN_INVITERequest → AccountView | Invite teacher or constrained admin principal | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate admin principal required for teacher-to-admin duties. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, INCOMPATIBLE_ROLE | API-ADMIN-INVITE |
| get_role_grants | API_ADMIN_ROLERequest → RoleGrantView | Read constrained role grants | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ROLE |
| set_role_grants | API_ADMIN_ROLE_UPDATERequest → RoleGrantView | Change admin privileges with audit and session revocation | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Cannot self-escalate; no last identity-admin removal; teacher/admin principal incompatibility. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, INCOMPATIBLE_ROLE, LAST_ADMIN | API-ADMIN-ROLE-UPDATE |
| set_account_status | API_ADMIN_ACCOUNT_STATUSRequest → AccountView | Suspend or reactivate account and revoke affected sessions | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ACCOUNT-STATUS |

## FamilyService

- **Module:** family
- **Responsibility:** family
- **Objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** PAR-006
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| get_family | API_FAMILY_GETRequest → FamilyView | Read own family and linked students | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-FAMILY-GET |
| list_parents_admin | API_ADMIN_PARENTSRequest → GuardianViewPage | Read authorized list parents | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PARENTS |
| get_family_admin | API_ADMIN_FAMILYRequest → FamilyView | Read authorized get family | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-FAMILY |
| create_guardian_link | API_ADMIN_GUARDIAN_LINKRequest → FamilyView | Link verified guardian to same family child | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Verification evidence reference mandatory; no cross-family transfer implicit. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-GUARDIAN-LINK |
| revoke_guardian_link | API_ADMIN_GUARDIAN_REVOKERequest → FamilyView | Revoke guardian child access | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. At least one verified active guardian remains or safeguarding override is documented. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-GUARDIAN-REVOKE |
| get_parent_dashboard | API_PARENT_DASHBOARDRequest → DashboardView | Read purpose-filtered dashboard counts and next actions | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-DASHBOARD |
| create_billing_membership | API_ADMIN_BILLING_MEMBERRequest → FamilyView | Grant verified adult family billing visibility separately from child links | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate finance approval reference required; no teacher principal. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-BILLING-MEMBER |
| revoke_billing_membership | API_ADMIN_BILLING_MEMBER_REVOKERequest → Empty | Revoke adult family financial membership | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-BILLING-MEMBER-REVOKE |

## StudentProfileService

- **Module:** family
- **Responsibility:** student_profile
- **Objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-004, PAR-005, TCH-009
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| create_student | API_STUDENT_CREATERequest → StudentProfileView | Register child with required name and age | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. Create StudentProfile and verified GuardianStudent link to requesting parent atomically in same family; no pre-existing child required. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-CREATE |
| get_student | API_STUDENT_GETRequest → StudentProfileView | Read linked child profile | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-GET |
| update_student | API_STUDENT_UPDATERequest → StudentProfileView | Update optional child information | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-UPDATE |
| reconfirm_age | API_STUDENT_AGERequest → StudentProfileView | Reconfirm required age | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-AGE |
| provision_credentials | API_STUDENT_CREDENTIALSRequest → StudentCredentialsView | Provision or rotate child login | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Guardian password reauthentication; revoke prior student sessions. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-CREDENTIALS |
| get_student_self | API_STUDENT_SELFRequest → StudentSelfProfileView | Read own limited profile | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-SELF |
| update_preferred_name | API_STUDENT_PREFERREDRequest → StudentSelfProfileView | Change own preferred display name | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-PREFERRED |
| list_students_admin | API_ADMIN_STUDENTSRequest → StudentProfileViewPage | Read authorized list students | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-STUDENTS |
| get_student_admin | API_ADMIN_STUDENTRequest → StudentProfileView | Read authorized get student | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-STUDENT |
| correct_student | API_ADMIN_STUDENT_UPDATERequest → StudentProfileView | Correct student data with reason | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-STUDENT-UPDATE |
| archive_student | API_ADMIN_STUDENT_ARCHIVERequest → StudentProfileView | Archive child after active obligations resolved | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ACTIVE_ENROLMENT_EXISTS | API-ADMIN-STUDENT-ARCHIVE |

## TeacherService

- **Module:** identity
- **Responsibility:** teachers
- **Objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-005, ADM-015, CLS-005
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_assigned_courses | API_TEACHER_COURSESRequest → CourseViewPage | List assigned courses | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-COURSES |
| list_assigned_students | API_TEACHER_STUDENTSRequest → TeachingStudentViewPage | Read assigned roster educational fields | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-STUDENTS |
| get_teaching_student | API_TEACHER_STUDENTRequest → TeachingStudentView | Read assigned learner educational profile | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-STUDENT |
| list_teachers_admin | API_ADMIN_TEACHERSRequest → TeacherViewPage | Read authorized list teachers | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-TEACHERS |
| get_teacher_admin | API_ADMIN_TEACHERRequest → TeacherView | Read authorized get teacher | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-TEACHER |
| update_teacher | API_ADMIN_TEACHER_UPDATERequest → TeacherView | Edit teacher public biography/profile | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-TEACHER-UPDATE |
| publish_teacher | API_ADMIN_TEACHER_PUBLISHRequest → TeacherView | Publish or withdraw explicitly approved instructor profile | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-TEACHER-PUBLISH |
| archive_teacher | API_ADMIN_TEACHER_ARCHIVERequest → TeacherView | Archive teacher after assignment reassignment | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ACTIVE_ASSIGNMENT_EXISTS | API-ADMIN-TEACHER-ARCHIVE |
| get_own_teacher_profile | API_TEACHER_PROFILERequest → TeacherView | Read own teacher profile | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-PROFILE |
| get_teacher_dashboard | API_TEACHER_DASHBOARDRequest → DashboardView | Read purpose-filtered dashboard counts and next actions | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-DASHBOARD |

## ConsentService

- **Module:** family
- **Responsibility:** consent
- **Objects:** PolicyDocument, PolicyAcknowledgement
- **Ports:** ContentRepository, FamilyRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** PAR-004, SEC-003
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_policies | API_POLICY_LISTRequest → PolicyViewPage | Read published policy versions | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-POLICY-LIST |
| list_acknowledgements | API_CONSENT_LISTRequest → AcknowledgementViewPage | Read family acknowledgement evidence | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-CONSENT-LIST |
| acknowledge | API_CONSENT_ACKRequest → AcknowledgementView | Record current policy acknowledgement | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, POLICY_VERSION_STALE | API-CONSENT-ACK |
| list_policy_drafts | API_ADMIN_POLICIESRequest → PolicyViewPage | Read draft and published legal policies | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-POLICIES |
| create_policy | API_ADMIN_POLICY_CREATERequest → PolicyView | Create immutable policy-version draft | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-POLICY-CREATE |
| publish_policy | API_ADMIN_POLICY_PUBLISHRequest → PolicyView | Publish policy with human/legal approval evidence | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED | API-ADMIN-POLICY-PUBLISH |

## PublicContentService

- **Module:** content
- **Responsibility:** public
- **Objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-007, LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| get_page | API_PUBLIC_PAGERequest → PublicPageView | Read get page | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-PUBLIC-PAGE |
| list_programs | API_PUBLIC_PROGRAMSRequest → PublicProgramViewPage | Read list programs | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-PUBLIC-PROGRAMS |
| list_courses | API_PUBLIC_COURSESRequest → PublicCourseViewPage | Read list courses | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-PUBLIC-COURSES |
| get_course | API_PUBLIC_COURSERequest → PublicCourseView | Read get course | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-PUBLIC-COURSE |
| list_public_cohorts | API_PUBLIC_COHORTSRequest → PublicCohortViewPage | Read list public cohorts | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-PUBLIC-COHORTS |
| list_public_teachers | API_PUBLIC_TEACHERSRequest → PublicTeacherViewPage | Read list public teachers | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-PUBLIC-TEACHERS |
| submit_contact | API_PUBLIC_CONTACTRequest → ContactReceipt | Submit contact enquiry to operations queue | Rate limit; honeypot; no attachments, child profile matching or marketing subscription. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE | API-PUBLIC-CONTACT |
| list_page_drafts | API_ADMIN_PAGESRequest → PublicPageViewPage | Read public page drafts | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PAGES |
| save_page | API_ADMIN_PAGE_UPDATERequest → PublicPageView | Save allowlisted public-page draft | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-PAGE-UPDATE |
| publish_page | API_ADMIN_PAGE_PUBLISHRequest → PublicPageView | Publish reviewed public page | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-PAGE-PUBLISH |
| list_contact_enquiries | API_ADMIN_ENQUIRIESRequest → ContactEnquiryViewPage | Read inbound enquiries to support customers | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ENQUIRIES |
| set_enquiry_status | API_ADMIN_ENQUIRY_STATUSRequest → ContactEnquiryView | Mark enquiry handled without sending unauthorized messages | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ENQUIRY-STATUS |

## CourseService

- **Module:** curriculum
- **Responsibility:** courses
- **Objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Ports:** CourseRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-007, LRN-001
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_programs | API_ADMIN_PROGRAM_LISTRequest → ProgramViewPage | List draft and published programs | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PROGRAM-LIST |
| create_program | API_ADMIN_PROGRAM_CREATERequest → ProgramView | Create offering grouping | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-PROGRAM-CREATE |
| update_program | API_ADMIN_PROGRAM_UPDATERequest → ProgramView | Edit offering grouping | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-PROGRAM-UPDATE |
| set_program_publication | API_ADMIN_PROGRAM_STATUSRequest → ProgramView | Publish or archive program | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-PROGRAM-STATUS |
| list_courses | API_ADMIN_COURSESRequest → CourseViewPage | List all curriculum courses | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-COURSES |
| get_course | API_ADMIN_COURSERequest → CourseView | Read administrative course details | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-COURSE |
| create_course | API_ADMIN_COURSE_CREATERequest → CourseView | Create reusable course | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-COURSE-CREATE |
| update_course | API_ADMIN_COURSE_UPDATERequest → CourseView | Edit course marketing metadata | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-COURSE-UPDATE |
| publish_course | API_ADMIN_COURSE_PUBLISHRequest → CourseView | Publish approved course with ready revision | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PUBLISH_VALIDATION_FAILED, LAUNCH_CONFIGURATION_REQUIRED | API-ADMIN-COURSE-PUBLISH |
| archive_course | API_ADMIN_COURSE_ARCHIVERequest → CourseView | Archive course acquisition; preserve existing learning access | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-COURSE-ARCHIVE |

## CurriculumService

- **Module:** curriculum
- **Responsibility:** curriculum
- **Objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004, STU-003, STU-004, TCH-003
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_revisions | API_ADMIN_REVISION_LISTRequest → CurriculumRevisionViewPage | List curriculum revisions | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-REVISION-LIST |
| create_revision | API_ADMIN_REVISION_CREATERequest → CurriculumRevisionView | Create draft revision optionally copied from same course | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-REVISION-CREATE |
| get_revision | API_ADMIN_REVISION_GETRequest → CurriculumRevisionView | Read full authoring hierarchy | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-REVISION-GET |
| publish_revision | API_ADMIN_REVISION_PUBLISHRequest → CurriculumRevisionView | Freeze validated curriculum revision | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PUBLISH_VALIDATION_FAILED, ASSET_NOT_READY | API-ADMIN-REVISION-PUBLISH |
| create_module | API_ADMIN_MODULE_CREATERequest → ModuleView | Create draft module | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-MODULE-CREATE |
| update_module | API_ADMIN_MODULE_UPDATERequest → ModuleView | Edit draft module | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-MODULE-UPDATE |
| delete_module | API_ADMIN_MODULE_DELETERequest → Empty | Remove unreferenced draft module | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE | API-ADMIN-MODULE-DELETE |
| create_lesson | API_ADMIN_LESSON_CREATERequest → LessonView | Create draft lesson | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-LESSON-CREATE |
| update_lesson | API_ADMIN_LESSON_UPDATERequest → LessonView | Edit draft lesson | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-LESSON-UPDATE |
| delete_lesson | API_ADMIN_LESSON_DELETERequest → Empty | Remove unreferenced draft lesson | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE | API-ADMIN-LESSON-DELETE |
| create_block | API_ADMIN_BLOCK_CREATERequest → LessonBlockView | Create draft block | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-BLOCK-CREATE |
| update_block | API_ADMIN_BLOCK_UPDATERequest → LessonBlockView | Edit draft block | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-BLOCK-UPDATE |
| delete_block | API_ADMIN_BLOCK_DELETERequest → Empty | Remove unreferenced draft block | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE | API-ADMIN-BLOCK-DELETE |
| create_resource | API_ADMIN_RESOURCE_CREATERequest → ResourceView | Create draft resource | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-RESOURCE-CREATE |
| update_resource | API_ADMIN_RESOURCE_UPDATERequest → ResourceView | Edit draft resource | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-RESOURCE-UPDATE |
| delete_resource | API_ADMIN_RESOURCE_DELETERequest → Empty | Remove unreferenced draft resource | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE | API-ADMIN-RESOURCE-DELETE |
| list_resources | API_ADMIN_RESOURCE_LISTRequest → ResourceViewPage | List teaching assets in revision | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-RESOURCE-LIST |
| get_authoring_lesson | API_ADMIN_LESSON_GETRequest → LessonView | Read authoring lesson and all block fields | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-LESSON-GET |
| get_learning_curriculum | API_STUDENT_CURRICULUMRequest → CurriculumRevisionView | Read released modules of pinned revision | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-CURRICULUM |
| get_learning_lesson | API_STUDENT_LESSONRequest → LessonView | Read released lesson and safe blocks | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, CONTENT_UNRELEASED | API-STUDENT-LESSON |
| list_learning_resources | API_STUDENT_RESOURCERequest → ResourceViewPage | List released learning resources | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-RESOURCE |
| get_teaching_curriculum | API_TEACHER_CURRICULUMRequest → CurriculumRevisionView | Read pinned teaching curriculum including planned lessons | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-CURRICULUM |
| get_teaching_lesson | API_TEACHER_LESSONRequest → LessonView | Read assigned teaching lesson plan | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-LESSON |
| list_teaching_resources | API_TEACHER_RESOURCESRequest → ResourceViewPage | Read assigned teaching resources | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-RESOURCES |

## CohortService

- **Module:** delivery
- **Responsibility:** cohorts
- **Objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_assigned_cohorts | API_TEACHER_COHORTSRequest → CohortViewPage | List assigned cohorts | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-COHORTS |
| list_cohorts | API_ADMIN_COHORTSRequest → CohortViewPage | List operational cohorts | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-COHORTS |
| get_cohort | API_ADMIN_COHORTRequest → CohortView | Read cohort operational details | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-COHORT |
| create_cohort | API_ADMIN_COHORT_CREATERequest → CohortView | Create course delivery pinned to published revision | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-COHORT-CREATE |
| update_cohort | API_ADMIN_COHORT_UPDATERequest → CohortView | Edit future cohort metadata and safe capacity | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, CAPACITY_BELOW_COMMITMENTS | API-ADMIN-COHORT-UPDATE |
| transition_cohort | API_ADMIN_COHORT_STATUSRequest → CohortView | Open, close, start or complete delivery | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, LAUNCH_CONFIGURATION_REQUIRED | API-ADMIN-COHORT-STATUS |
| cancel_cohort | API_ADMIN_COHORT_CANCELRequest → Accepted | Cancel delivery and create refund review tasks | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Education can cancel delivery but cannot execute refund. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-COHORT-CANCEL |
| list_teacher_assignments | API_ADMIN_ASSIGNMENTSRequest → TeacherAssignmentViewPage | List cohort teaching grants | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ASSIGNMENTS |
| create_teacher_assignment | API_ADMIN_ASSIGNMENT_CREATERequest → TeacherAssignmentView | Assign active teacher to cohort/session | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT | API-ADMIN-ASSIGNMENT-CREATE |
| revoke_teacher_assignment | API_ADMIN_ASSIGNMENT_REVOKERequest → Empty | Revoke teaching access immediately | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ASSIGNMENT-REVOKE |

## SchedulingService

- **Module:** delivery
- **Responsibility:** scheduling
- **Objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011, PAR-009, STU-013, TCH-005, TCH-006
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_cohort_sessions | API_ADMIN_SESSIONSRequest → ClassSessionViewPage | List all delivery sessions | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-SESSIONS |
| create_class_session | API_ADMIN_SESSION_CREATERequest → ClassSessionView | Schedule one class occurrence | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, DST_AMBIGUOUS | API-ADMIN-SESSION-CREATE |
| create_session_series | API_ADMIN_RECURRENCERequest → ClassSessionViewPage | Materialize bounded weekly occurrences transactionally | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, DST_AMBIGUOUS | API-ADMIN-RECURRENCE |
| update_class_session | API_ADMIN_SESSION_UPDATERequest → ClassSessionView | Edit session title/lesson without rescheduling | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-SESSION-UPDATE |
| list_parent_schedule | API_PARENT_SCHEDULERequest → ClassSessionViewPage | List parent authorized upcoming classes | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-SCHEDULE |
| get_parent_session | API_PARENT_SESSIONRequest → ClassSessionView | Read authorized class session details | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-SESSION |
| list_student_schedule | API_STUDENT_SCHEDULERequest → ClassSessionViewPage | List student authorized upcoming classes | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-SCHEDULE |
| get_student_session | API_STUDENT_SESSIONRequest → ClassSessionView | Read authorized class session details | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-SESSION |
| list_teacher_schedule | API_TEACHER_SCHEDULERequest → ClassSessionViewPage | List teacher authorized upcoming classes | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-SCHEDULE |
| get_teacher_session | API_TEACHER_SESSIONRequest → ClassSessionView | Read authorized class session details | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-SESSION |
| reschedule_teacher_session | API_TEACHER_RESCHEDULERequest → ClassSessionView | Reschedule authorized session and queue provider updates | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Start >= now+24h; future assigned session only; no overlap for teacher/learner. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, RESCHEDULE_WINDOW_CLOSED, DST_AMBIGUOUS | API-TEACHER-RESCHEDULE |
| reschedule_admin_session | API_ADMIN_RESCHEDULERequest → ClassSessionView | Reschedule authorized session and queue provider updates | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Override short notice requires reason; overlaps still rejected. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, RESCHEDULE_WINDOW_CLOSED, DST_AMBIGUOUS | API-ADMIN-RESCHEDULE |
| cancel_class_session | API_ADMIN_SESSION_CANCELRequest → ClassSessionView | Cancel class and queue Zoom/calendar cancellation and notices | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-SESSION-CANCEL |
| complete_class_session | API_ADMIN_SESSION_COMPLETERequest → ClassSessionView | Complete past session after attendance review | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-SESSION-COMPLETE |

## LiveClassService

- **Module:** delivery
- **Responsibility:** live
- **Objects:** ClassSession, IntegrationBinding, TeachingAccessPolicy
- **Ports:** DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009, STU-014, TCH-004
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| start_assigned_class | API_TEACHER_STARTRequest → JoinLinkView | Fetch fresh authorized Zoom host handoff | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Assigned authorized host; now within start-30m through scheduled end. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE | API-TEACHER-START |
| join_student_class | API_STUDENT_JOINRequest → JoinLinkView | Fetch eligible learner Zoom join handoff | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Active enrolment; now within start-15m through scheduled end; no host URL. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE | API-STUDENT-JOIN |
| join_parent_class | API_PARENT_JOINRequest → JoinLinkView | Fetch eligible learner Zoom join handoff | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Active enrolment; now within start-15m through scheduled end; no host URL. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE | API-PARENT-JOIN |
| provision_meeting | JOB_LIVE_CREATERequest → JobView | Create provider meeting from authoritative session version | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-LIVE-CREATE |
| synchronize_meeting | JOB_LIVE_UPDATERequest → JobView | Update/cancel meeting from latest authoritative session state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-LIVE-UPDATE |
| reconcile_meetings | JOB_LIVE_RECONCILERequest → JobView | Resolve provider drift without overwriting domain schedule | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-LIVE-RECONCILE |

## EnrolmentService

- **Module:** enrolment
- **Responsibility:** enrolments
- **Objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_student_enrolments | API_STUDENT_ENROLMENTSRequest → EnrolmentViewPage | List own enrolled courses | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-ENROLMENTS |
| list_child_enrolments | API_PARENT_ENROLMENTSRequest → EnrolmentViewPage | List linked child enrolment status | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-ENROLMENTS |
| list_enrolments | API_ADMIN_ENROLMENTSRequest → EnrolmentViewPage | List delivery enrolments without financial fields | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ENROLMENTS |
| get_enrolment | API_ADMIN_ENROLMENTRequest → EnrolmentView | Read educational enrolment status | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ENROLMENT |
| cancel_enrolment | API_ADMIN_ENROLMENT_CANCELRequest → EnrolmentView | Cancel educational access with auditable reason | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Any money movement requires finance workflow. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ENROLMENT-CANCEL |
| cancel_hold | API_PARENT_CHECKOUT_CANCELRequest → EnrolmentView | Release own unpaid hold | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Held/pending payment only; provider expiry reconciled. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-PARENT-CHECKOUT-CANCEL |
| expire_holds | JOB_HOLD_EXPIRERequest → JobView | Expire elapsed holds under row lock; release capacity | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-HOLD-EXPIRE |

## AttendanceService

- **Module:** delivery
- **Responsibility:** attendance
- **Objects:** AttendanceRecord, ClassSession, TeachingAccessPolicy
- **Ports:** AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-017, CLS-010, PAR-010, STU-015, TCH-007, TCH-008
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_teacher_attendance | API_TEACHER_ATTENDANCERequest → AttendanceViewPage | Read authorized session attendance roster | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-ATTENDANCE |
| record_teacher_attendance | API_TEACHER_ATTENDANCE_RECORDRequest → AttendanceView | Record or amend attendance | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Student enrolled in this session cohort. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-ATTENDANCE-RECORD |
| list_admin_attendance | API_ADMIN_ATTENDANCERequest → AttendanceViewPage | Read authorized session attendance roster | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ATTENDANCE |
| record_admin_attendance | API_ADMIN_ATTENDANCE_RECORDRequest → AttendanceView | Record or amend attendance | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Student enrolled in this session cohort. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ATTENDANCE-RECORD |
| list_parent_attendance | API_PARENT_ATTENDANCERequest → AttendanceViewPage | Read own or linked child attendance | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-ATTENDANCE |
| list_student_attendance | API_STUDENT_ATTENDANCERequest → AttendanceViewPage | Read own or linked child attendance | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-ATTENDANCE |

## QuizService

- **Module:** assessment
- **Responsibility:** quizzes
- **Objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003, STU-007
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_quizzes | API_ADMIN_QUIZZESRequest → QuizViewPage | List quiz authoring definitions | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-QUIZZES |
| get_quiz | API_ADMIN_QUIZRequest → QuizView | Read quiz questions and grading keys | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-QUIZ |
| create_quiz | API_ADMIN_QUIZ_CREATERequest → QuizView | Create draft formative quiz | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-QUIZ-CREATE |
| update_quiz | API_ADMIN_QUIZ_UPDATERequest → QuizView | Edit draft quiz rules | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-QUIZ-UPDATE |
| replace_questions | API_ADMIN_QUESTION_PUTRequest → QuizView | Replace ordered draft questions atomically | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft only; complete validated answer key; positions unique. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-QUESTION-PUT |
| delete_quiz | API_ADMIN_QUIZ_DELETERequest → Empty | Delete unreferenced draft quiz | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE | API-ADMIN-QUIZ-DELETE |
| get_learner_quiz | API_STUDENT_QUIZRequest → LearnerQuizView | Read released quiz without answer key | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-QUIZ |
| list_attempts | API_STUDENT_ATTEMPTSRequest → QuizAttemptViewPage | Read own attempt history | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-ATTEMPTS |
| start_attempt | API_STUDENT_ATTEMPT_CREATERequest → QuizAttemptView | Start attempt with immutable quiz snapshot | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ATTEMPT_LIMIT_REACHED | API-STUDENT-ATTEMPT-CREATE |
| save_answers | API_STUDENT_ATTEMPT_SAVERequest → QuizAttemptView | Save selections on own in-progress attempt | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-ATTEMPT-SAVE |
| submit_attempt | API_STUDENT_ATTEMPT_SUBMITRequest → QuizAttemptView | Submit once and release formative score | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ATTEMPT_ALREADY_SUBMITTED | API-STUDENT-ATTEMPT-SUBMIT |
| list_teaching_attempts | API_TEACHER_QUIZ_RESULTSRequest → QuizAttemptViewPage | Read assigned learners submitted quiz scores | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-QUIZ-RESULTS |
| list_admin_attempts | API_ADMIN_QUIZ_RESULTSRequest → QuizAttemptViewPage | Oversee submitted quiz outcomes | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-QUIZ-RESULTS |
| list_child_quiz_results | API_PARENT_QUIZ_RESULTSRequest → ChildQuizResultViewPage | Read released child quiz results | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-QUIZ-RESULTS |

## AssignmentService

- **Module:** assessment
- **Responsibility:** assignments
- **Objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-011, ASM-004, STU-008, TCH-010
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_assignments | API_ADMIN_ASSIGNMENTS_LISTRequest → AssignmentViewPage | List assignment/project authoring definitions | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ASSIGNMENTS-LIST |
| get_assignment | API_ADMIN_ASSIGNMENT_GETRequest → AssignmentView | Read assignment authoring detail | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ASSIGNMENT-GET |
| create_assignment | API_ADMIN_ASSIGNMENT_DEFINERequest → AssignmentView | Create assignment or project definition | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ASSIGNMENT-DEFINE |
| update_assignment | API_ADMIN_ASSIGNMENT_EDITRequest → AssignmentView | Edit draft assignment definition | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ASSIGNMENT-EDIT |
| delete_assignment | API_ADMIN_ASSIGNMENT_DELETERequest → Empty | Delete unreferenced draft assignment | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE | API-ADMIN-ASSIGNMENT-DELETE |
| list_student_assignments | API_STUDENT_ASSIGNMENTSRequest → AssignmentViewPage | Read permitted assignment and project work | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-ASSIGNMENTS |
| list_parent_assignments | API_PARENT_ASSIGNMENTSRequest → AssignmentViewPage | Read permitted assignment and project work | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-ASSIGNMENTS |
| list_teacher_assignments | API_TEACHER_ASSIGNMENTSRequest → AssignmentViewPage | Read permitted assignment and project work | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-ASSIGNMENTS |
| set_delivery_closure | API_ADMIN_ASSIGNMENT_CLOSERequest → AssignmentView | Close/reopen assignment submissions for a delivery | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ASSIGNMENT-CLOSE |

## SubmissionService

- **Module:** assessment
- **Responsibility:** submissions
- **Objects:** Submission, FileAsset, ReleasePolicy
- **Ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ASM-005, STU-009, STU-010
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_own_submissions | API_STUDENT_SUBMISSIONSRequest → SubmissionViewPage | Read own immutable submission history | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-SUBMISSIONS |
| create_submission | API_STUDENT_SUBMISSION_CREATERequest → SubmissionView | Start own assignment submission/revision | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. New attempt only if policy permits or prior attempt returned. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-SUBMISSION-CREATE |
| save_submission | API_STUDENT_SUBMISSION_SAVERequest → SubmissionView | Save own draft work and ready scanned file links | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSET_NOT_READY | API-STUDENT-SUBMISSION-SAVE |
| submit_work | API_STUDENT_SUBMISSION_SENDRequest → SubmissionView | Freeze own work and enqueue assessment notice | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Late work accepted and labelled until cohort complete or explicitly closed. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSIGNMENT_CLOSED, ASSET_NOT_READY | API-STUDENT-SUBMISSION-SEND |
| delete_draft | API_STUDENT_SUBMISSION_DELETERequest → Empty | Discard own unsubmitted draft | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-SUBMISSION-DELETE |
| list_child_submissions | API_PARENT_SUBMISSIONSRequest → ChildSubmissionStatusViewPage | Read child submission status/history | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-SUBMISSIONS |
| list_teacher_submissions | API_TEACHER_SUBMISSIONSRequest → SubmissionViewPage | Read authorized submitted work review queue | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-SUBMISSIONS |
| get_teacher_submission | API_TEACHER_SUBMISSIONRequest → SubmissionView | Read authorized frozen work version | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-SUBMISSION |
| list_admin_submissions | API_ADMIN_SUBMISSIONSRequest → SubmissionViewPage | Read authorized submitted work review queue | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-SUBMISSIONS |
| get_admin_submission | API_ADMIN_SUBMISSIONRequest → SubmissionView | Read authorized frozen work version | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-SUBMISSION |

## AssessmentService

- **Module:** assessment
- **Responsibility:** assessments
- **Objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-012, ASM-006, ASM-007, PAR-013, STU-011, TCH-011, TCH-012
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| return_teacher_submission | API_TEACHER_RETURNRequest → SubmissionView | Return work for a new immutable revision | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-RETURN |
| save_teacher_assessment | API_TEACHER_ASSESSMENTRequest → AssessmentView | Save draft marking against frozen submission | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-ASSESSMENT |
| get_teacher_assessment | API_TEACHER_ASSESSMENT_GETRequest → AssessmentView | Read permitted draft/released marking | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-ASSESSMENT-GET |
| release_teacher_assessment | API_TEACHER_ASSESSMENT_RELEASERequest → AssessmentView | Release validated assessment to learner and guardian | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-ASSESSMENT-RELEASE |
| withdraw_teacher_assessment | API_TEACHER_ASSESSMENT_WITHDRAWRequest → AssessmentView | Withdraw erroneous release and preserve correction history | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-ASSESSMENT-WITHDRAW |
| return_admin_submission | API_ADMIN_RETURNRequest → SubmissionView | Return work for a new immutable revision | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-RETURN |
| save_admin_assessment | API_ADMIN_ASSESSMENTRequest → AssessmentView | Save draft marking against frozen submission | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ASSESSMENT |
| get_admin_assessment | API_ADMIN_ASSESSMENT_GETRequest → AssessmentView | Read permitted draft/released marking | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ASSESSMENT-GET |
| release_admin_assessment | API_ADMIN_ASSESSMENT_RELEASERequest → AssessmentView | Release validated assessment to learner and guardian | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ASSESSMENT-RELEASE |
| withdraw_admin_assessment | API_ADMIN_ASSESSMENT_WITHDRAWRequest → AssessmentView | Withdraw erroneous release and preserve correction history | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ASSESSMENT-WITHDRAW |
| list_student_assessments | API_STUDENT_ASSESSMENTSRequest → AssessmentViewPage | Read own/linked child released assessments | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-ASSESSMENTS |
| list_parent_assessments | API_PARENT_ASSESSMENTSRequest → AssessmentViewPage | Read own/linked child released assessments | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-ASSESSMENTS |

## FeedbackService

- **Module:** assessment
- **Responsibility:** feedback
- **Objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-019, ASM-008, PAR-012, STU-012, TCH-013
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_teacher_feedback | API_TEACHER_FEEDBACK_LISTRequest → FeedbackViewPage | Read permitted feedback drafts/releases | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-FEEDBACK-LIST |
| create_teacher_feedback | API_TEACHER_FEEDBACK_CREATERequest → FeedbackView | Create draft educational feedback | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-FEEDBACK-CREATE |
| update_teacher_feedback | API_TEACHER_FEEDBACK_UPDATERequest → FeedbackView | Revise draft feedback; released content requires withdrawal first | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-FEEDBACK-UPDATE |
| release_teacher_feedback | API_TEACHER_FEEDBACK_RELEASERequest → FeedbackView | Release educational feedback and notify | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-FEEDBACK-RELEASE |
| withdraw_teacher_feedback | API_TEACHER_FEEDBACK_WITHDRAWRequest → FeedbackView | Withdraw mistaken feedback release with reason | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-TEACHER-FEEDBACK-WITHDRAW |
| list_admin_feedback | API_ADMIN_FEEDBACK_LISTRequest → FeedbackViewPage | Read permitted feedback drafts/releases | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-FEEDBACK-LIST |
| create_admin_feedback | API_ADMIN_FEEDBACK_CREATERequest → FeedbackView | Create draft educational feedback | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-FEEDBACK-CREATE |
| update_admin_feedback | API_ADMIN_FEEDBACK_UPDATERequest → FeedbackView | Revise draft feedback; released content requires withdrawal first | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-FEEDBACK-UPDATE |
| release_admin_feedback | API_ADMIN_FEEDBACK_RELEASERequest → FeedbackView | Release educational feedback and notify | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-FEEDBACK-RELEASE |
| withdraw_admin_feedback | API_ADMIN_FEEDBACK_WITHDRAWRequest → FeedbackView | Withdraw mistaken feedback release with reason | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-FEEDBACK-WITHDRAW |
| list_student_feedback | API_STUDENT_FEEDBACKRequest → FeedbackViewPage | Read own/linked child released feedback | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-FEEDBACK |
| list_parent_feedback | API_PARENT_FEEDBACKRequest → FeedbackViewPage | Read own/linked child released feedback | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-FEEDBACK |

## ProgressService

- **Module:** learning
- **Responsibility:** progress
- **Objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-018, LRN-007, LRN-008, PAR-011, STU-016, TCH-014
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_teacher_progress | API_TEACHER_PROGRESSRequest → ProgressViewPage | Read permitted learner completion evidence | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-PROGRESS |
| list_admin_progress | API_ADMIN_PROGRESSRequest → ProgressViewPage | Read permitted learner completion evidence | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PROGRESS |
| list_student_progress | API_STUDENT_PROGRESSRequest → ProgressViewPage | Read own/linked child released progress | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-PROGRESS |
| list_parent_progress | API_PARENT_PROGRESSRequest → ProgressViewPage | Read own/linked child released progress | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-PROGRESS |
| list_activities | API_STUDENT_ACTIVITY_GETRequest → ActivityCompletionViewPage | Read own activity/reflection status | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-ACTIVITY-GET |
| record_activity | API_STUDENT_ACTIVITYRequest → ActivityCompletionView | Record own non-graded activity and reflection | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-ACTIVITY |
| complete_lesson | API_STUDENT_LESSON_COMPLETERequest → ActivityCompletionView | Record own lesson acknowledgement | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STUDENT-LESSON-COMPLETE |
| review_completion | API_ADMIN_COMPLETION_REVIEWRequest → ProgressView | Recompute and record completion decision from evidence | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. education_admin may recompute standard eligibility, grant override with verified evidence and reason, or revoke prior override. Source learning records and attendance remain immutable. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED | API-ADMIN-COMPLETION-REVIEW |
| get_student_dashboard | API_STUDENT_DASHBOARDRequest → DashboardView | Read purpose-filtered dashboard counts and next actions | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-DASHBOARD |
| recompute_progress | JOB_PROGRESS_RECOMPUTERequest → ProgressView | Recalculate completion from latest released work and attendance evidence | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-PROGRESS-RECOMPUTE |

## CertificateService

- **Module:** learning
- **Responsibility:** certificates
- **Objects:** Certificate, CompletionPolicy, StudentProgress
- **Ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-020, LRN-009, LRN-010, PAR-014, STU-017
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_student_certificates | API_STUDENT_CERTIFICATESRequest → CertificateViewPage | Read own/linked child released certificates | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-CERTIFICATES |
| list_parent_certificates | API_PARENT_CERTIFICATESRequest → CertificateViewPage | Read own/linked child released certificates | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-CERTIFICATES |
| list_certificates | API_ADMIN_CERTIFICATESRequest → CertificateViewPage | List certificate issue/revocation state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-CERTIFICATES |
| issue_certificate | API_ADMIN_CERTIFICATE_ISSUERequest → CertificateView | Issue completion certificate once from eligible progress | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COMPLETION_NOT_ELIGIBLE | API-ADMIN-CERTIFICATE-ISSUE |
| revoke_certificate | API_ADMIN_CERTIFICATE_REVOKERequest → CertificateView | Revoke incorrect certificate with reason | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-CERTIFICATE-REVOKE |
| reissue_certificate | API_ADMIN_CERTIFICATE_REISSUERequest → CertificateView | Issue replacement linked to revoked certificate | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-CERTIFICATE-REISSUE |
| render_certificate | JOB_CERTIFICATE_RENDERRequest → CertificateView | Render immutable certificate artifact and mark issued after ready storage | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-CERTIFICATE-RENDER |

## BillingService

- **Module:** billing
- **Responsibility:** billing
- **Objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Never accepted from teacher/student principal.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-024, ADM-025, ENR-007, PAR-017, PAR-018, PAR-019, PAR-020, PAY-001, PAY-002, PAY-003, PAY-004, PAY-005, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| create_checkout | API_PARENT_CHECKOUTRequest → CheckoutSessionView | Reserve seat and create server-priced hosted checkout | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. Verified email; age reconfirmed within180d; current required consents. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, AGE_RECONFIRMATION_REQUIRED, AGE_INELIGIBLE, ALREADY_ENROLLED, LAUNCH_CONFIGURATION_REQUIRED, PROVIDER_UNAVAILABLE | API-PARENT-CHECKOUT |
| retry_checkout | API_PARENT_CHECKOUT_RETRYRequest → CheckoutSessionView | Retry failed/expired checkout with fresh eligibility and seat check | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, PROVIDER_UNAVAILABLE | API-PARENT-CHECKOUT-RETRY |
| list_family_payments | API_PARENT_PAYMENTSRequest → PaymentViewPage | Read own family payment history | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-PAYMENTS |
| get_family_payment | API_PARENT_PAYMENTRequest → PaymentView | Read authoritative payment/checkout state | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-PAYMENT |
| list_family_documents | API_PARENT_RECEIPTSRequest → ReceiptViewPage | Read own immutable invoice/receipt documents | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-RECEIPTS |
| list_prices | API_ADMIN_PRICESRequest → PriceConfigViewPage | List current and historic fees | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PRICES |
| create_price | API_ADMIN_PRICE_CREATERequest → PriceConfigView | Create effective dated course default/cohort override fee | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, OVERLAPPING_PRICE_WINDOW | API-ADMIN-PRICE-CREATE |
| retire_price | API_ADMIN_PRICE_RETIRERequest → PriceConfigView | End future pricing without changing purchase snapshots | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-PRICE-RETIRE |
| list_payments | API_ADMIN_PAYMENTSRequest → AdminPaymentViewPage | Inspect financial transactions and exceptions | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PAYMENTS |
| get_payment | API_ADMIN_PAYMENTRequest → AdminPaymentView | Read payment reconciliation references | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PAYMENT |
| request_reconciliation | API_ADMIN_PAYMENT_RECONCILERequest → Accepted | Queue server-to-server reconciliation | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-PAYMENT-RECONCILE |
| list_documents | API_ADMIN_DOCUMENTSRequest → ReceiptViewPage | Inspect immutable invoices/receipts | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-DOCUMENTS |
| list_billing_settings | API_ADMIN_FINANCE_SETTINGSRequest → SettingViewPage | Read merchant identity/tax configuration | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-FINANCE-SETTINGS |
| set_billing_setting | API_ADMIN_FINANCE_SETTING_PUTRequest → SettingView | Set approved merchant/tax/refund policy value | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED | API-ADMIN-FINANCE-SETTING-PUT |
| receive_stripe_webhook | API_STRIPE_WEBHOOKRequest → Empty | Validate raw signature and persist deduplicated provider event | Stripe signature on original bytes; signed does not imply relevant event; dedupe provider+event ID before any financial mutation. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-STRIPE-WEBHOOK |
| process_payment_event | JOB_PAYMENT_PROCESSRequest → JobView | Retrieve authoritative provider state and activate paid seat safely | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-PAYMENT-PROCESS |
| reconcile_payment | JOB_PAYMENT_RECONCILERequest → JobView | Compare Stripe state with immutable local ledger | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-PAYMENT-RECONCILE |
| generate_purchase_documents | JOB_DOCUMENT_GENERATERequest → JobView | Generate immutable receipt/invoice after verified payment | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-DOCUMENT-GENERATE |
| resolve_paid_exception | API_ADMIN_PAID_EXCEPTIONRequest → AdminPaymentView | Resolve late paid no-seat exception exactly once by allocation or refund | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Lock Payment+Enrolment+Cohort; ALLOCATE requires available seat and no pending refund; REFUND reserves refundable balance and prevents activation. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, REFUND_PENDING, EXCEPTION_ALREADY_RESOLVED | API-ADMIN-PAID-EXCEPTION |
| discover_provider_transactions | JOB_PAYMENT_DISCOVERYRequest → JobView | Discover provider-side payments/refunds and reconcile missing local references | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-PAYMENT-DISCOVERY |
| list_reconciliation_exceptions | API_ADMIN_RECONCILIATION_EXCEPTIONSRequest → ReconciliationExceptionViewPage | Inspect provider transactions unmatched to local financial records | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-RECONCILIATION-EXCEPTIONS |
| retry_reconciliation_exception | API_ADMIN_RECONCILIATION_EXCEPTION_RETRYRequest → Accepted | Recheck provider truth and resolve only verified matching or reversed transaction | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No manual invented payment ownership; unresolved cases remain open for documented operational repair. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-RECONCILIATION-EXCEPTION-RETRY |

## RefundService

- **Module:** billing
- **Responsibility:** refunds
- **Objects:** Refund, Payment, Enrolment, Money
- **Ports:** PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Never accepted from teacher/student principal.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-026, PAY-008
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_family_refunds | API_PARENT_REFUNDSRequest → RefundViewPage | Read own refund outcome | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-REFUNDS |
| list_refunds | API_ADMIN_REFUNDSRequest → RefundViewPage | Inspect refund ledger | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-REFUNDS |
| create_refund | API_ADMIN_REFUND_CREATERequest → RefundView | Request full/partial refund with explicit entitlement disposition | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, REFUND_EXCEEDS_BALANCE | API-ADMIN-REFUND-CREATE |
| retry_refund | API_ADMIN_REFUND_RETRYRequest → RefundView | Retry confirmed failed refund under same provider idempotency key | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PROVIDER_OUTCOME_UNKNOWN | API-ADMIN-REFUND-RETRY |
| process_refund | JOB_REFUND_PROCESSRequest → JobView | Execute idempotent requested refund and apply explicit access disposition | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-REFUND-PROCESS |

## ReportingService

- **Module:** billing
- **Responsibility:** reporting
- **Objects:** Payment, Refund, Receipt, FinancialExport
- **Ports:** PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Never accepted from teacher/student principal.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-027, PAY-010
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| get_finance_report | API_ADMIN_REPORTRequest → FinanceReportView | Read bounded AUD gross/refund/net report | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-REPORT |
| create_finance_export | API_ADMIN_REPORT_EXPORTRequest → ExportView | Generate bounded finance CSV export | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-REPORT-EXPORT |
| generate_finance_export | JOB_FINANCE_EXPORTRequest → ExportView | Write formula-injection-safe CSV to private export storage | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-FINANCE-EXPORT |
| get_finance_export | API_ADMIN_REPORT_EXPORT_STATUSRequest → ExportView | Read own authorized financial report export status | Authenticated finance_admin with active account and recent MFA, requesting the export or explicitly authorized finance oversight; status read permits every defined ExportView state and never requires a ready asset. Deny parent, student, teacher and non-finance admin. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-REPORT-EXPORT-STATUS |
| download_finance_export | API_ADMIN_REPORT_EXPORT_DOWNLOADRequest → DownloadTicketView | Download ready private financial report export under finance scope | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Ready generated financial_export; initiated by this principal or explicitly privileged finance oversight; no generic teaching file grant. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, EXPORT_NOT_READY, EXPORT_EXPIRED | API-ADMIN-REPORT-EXPORT-DOWNLOAD |

## CommunicationService

- **Module:** communication
- **Responsibility:** communications
- **Objects:** Event, Announcement, AudiencePolicy
- **Ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, PAR-003, PAR-015, STU-018
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_events | API_ADMIN_EVENT_LISTRequest → EventViewPage | List event drafts and releases | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-EVENT-LIST |
| create_event | API_ADMIN_EVENT_CREATERequest → EventView | Create audience-scoped event | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-EVENT-CREATE |
| update_event | API_ADMIN_EVENT_UPDATERequest → EventView | Revise draft event | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-EVENT-UPDATE |
| publish_event | API_ADMIN_EVENT_PUBLISHRequest → EventView | Publish event and resolve recipients | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-EVENT-PUBLISH |
| withdraw_event | API_ADMIN_EVENT_WITHDRAWRequest → EventView | Cancel or withdraw event and notify affected audience | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-EVENT-WITHDRAW |
| list_parent_events | API_PARENT_EVENTSRequest → EventViewPage | Read relevant published events | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-EVENTS |
| list_student_events | API_STUDENT_EVENTSRequest → EventViewPage | Read relevant published events | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-EVENTS |
| list_teacher_events | API_TEACHER_EVENTSRequest → EventViewPage | Read relevant published events | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-EVENTS |
| list_announcements | API_ADMIN_ANNOUNCEMENT_LISTRequest → AnnouncementViewPage | List announcement drafts and releases | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-ANNOUNCEMENT-LIST |
| create_announcement | API_ADMIN_ANNOUNCEMENT_CREATERequest → AnnouncementView | Create audience-scoped announcement | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ANNOUNCEMENT-CREATE |
| update_announcement | API_ADMIN_ANNOUNCEMENT_UPDATERequest → AnnouncementView | Revise draft announcement | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ANNOUNCEMENT-UPDATE |
| publish_announcement | API_ADMIN_ANNOUNCEMENT_PUBLISHRequest → AnnouncementView | Publish announcement and resolve recipients | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ANNOUNCEMENT-PUBLISH |
| withdraw_announcement | API_ADMIN_ANNOUNCEMENT_WITHDRAWRequest → AnnouncementView | Cancel or withdraw announcement and notify affected audience | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-ANNOUNCEMENT-WITHDRAW |
| list_parent_announcements | API_PARENT_ANNOUNCEMENTSRequest → AnnouncementViewPage | Read relevant published announcements | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-ANNOUNCEMENTS |
| list_student_announcements | API_STUDENT_ANNOUNCEMENTSRequest → AnnouncementViewPage | Read relevant published announcements | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-STUDENT-ANNOUNCEMENTS |
| list_teacher_announcements | API_TEACHER_ANNOUNCEMENTSRequest → AnnouncementViewPage | Read relevant published announcements | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-TEACHER-ANNOUNCEMENTS |
| list_public_events | API_PUBLIC_EVENTSRequest → EventViewPage | Read explicitly public upcoming events | Only explicitly published projection; no private child, roster, billing or operational data. | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED | API-PUBLIC-EVENTS |

## NotificationService

- **Module:** communication
- **Responsibility:** notifications
- **Objects:** Notification, NotificationDelivery, OutboxEvent
- **Ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-022, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-007, COM-008, COM-009, PAR-016, TCH-015
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_notifications | API_NOTIFICATIONSRequest → NotificationViewPage | Read own recipient-scoped inbox | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-NOTIFICATIONS |
| mark_read | API_NOTIFICATION_READRequest → NotificationView | Mark own notification read | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-NOTIFICATION-READ |
| list_deliveries | API_ADMIN_DELIVERIESRequest → DeliveryViewPage | Inspect redacted delivery errors | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-DELIVERIES |
| retry_delivery | API_ADMIN_DELIVERY_RETRYRequest → Accepted | Retry failed authorized delivery with deduplication | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-DELIVERY-RETRY |
| prepare_notifications | JOB_NOTIFICATION_PREPARERequest → JobView | Resolve outbox recipients and create deduplicated notices | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-NOTIFICATION-PREPARE |
| deliver_email | JOB_EMAIL_SENDRequest → JobView | Deliver transactional email with durable local deduplication | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-EMAIL-SEND |
| schedule_reminders | JOB_REMINDER_SCHEDULERequest → JobView | Queue class reminders once per current session version | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-REMINDER-SCHEDULE |

## FileService

- **Module:** files
- **Responsibility:** files
- **Objects:** FileAsset, FileAccessPolicy
- **Ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| create_upload | API_FILE_UPLOADRequest → UploadTicketView | Reserve validated private upload ticket | Student own draft submission only; admin matching purpose privilege. No parent upload feature. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, FILE_TYPE_DENIED, FILE_TOO_LARGE | API-FILE-UPLOAD |
| confirm_upload | API_FILE_CONFIRMRequest → FileAssetView | Confirm upload and queue independent scanning | Upload owner and same original scope; uploaded object metadata/checksum must match ticket. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, UPLOAD_MISMATCH | API-FILE-CONFIRM |
| get_asset | API_FILE_GETRequest → FileAssetView | Read authorized file scan/metadata state | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-FILE-GET |
| create_download | API_FILE_DOWNLOADRequest → DownloadTicketView | Issue ready-file short-lived download | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSET_NOT_READY | API-FILE-DOWNLOAD |
| delete_asset | API_FILE_DELETERequest → Empty | Delete eligible unreferenced owned draft asset | No referenced submitted work/published resource/certificate deletion; retention and legal hold apply. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE, LEGAL_HOLD | API-FILE-DELETE |
| list_assets | API_ADMIN_FILESRequest → FileAssetViewPage | Browse assets by permitted educational/operations purpose | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-FILES |
| scan_and_promote | JOB_FILE_SCANRequest → JobView | Verify metadata/MIME/archive limits/malware and promote immutable object | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-FILE-SCAN |
| clean_orphaned_uploads | JOB_FILE_CLEANRequest → JobView | Delete expired unreferenced staging objects after retention/hold checks | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-FILE-CLEAN |
| purge_asset | JOB_FILE_DELETERequest → JobView | Delete eligible private object/version per approved retention decision | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-FILE-DELETE |

## CalendarService

- **Module:** delivery
- **Responsibility:** calendar
- **Objects:** ClassSession, Event, IntegrationBinding
- **Ports:** DeliveryRepository, CommunicationRepository, IntegrationRepository, CalendarProvider, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** CAL-001, CAL-002, CAL-003, CAL-004, CAL-005
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| export_family_calendar | API_PARENT_CALENDARRequest → CalendarExport | Export authorized family schedule with portal deep links | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-CALENDAR |
| synchronize_event | JOB_CALENDAR_SYNCRequest → JobView | Upsert/cancel individual business calendar mirror event | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-CALENDAR-SYNC |
| reconcile_calendar | JOB_CALENDAR_RESYNCRequest → JobView | Recover invalid sync token with full mirror reconciliation | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-CALENDAR-RESYNC |

## OperationsService

- **Module:** operations
- **Responsibility:** operations
- **Objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| get_admin_dashboard | API_ADMIN_DASHBOARDRequest → DashboardView | Read purpose-filtered dashboard counts and next actions | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-DASHBOARD |
| list_settings | API_ADMIN_SETTINGSRequest → SettingViewPage | Read allowlisted non-secret operational settings | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-SETTINGS |
| set_setting | API_ADMIN_SETTING_PUTRequest → SettingView | Set validated key with approval evidence for launch-sensitive values | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED | API-ADMIN-SETTING-PUT |
| list_integrations | API_ADMIN_INTEGRATIONSRequest → IntegrationStatusViewPage | Read masked provider configuration and synchronization health | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-INTEGRATIONS |
| configure_integration | API_ADMIN_INTEGRATION_UPDATERequest → IntegrationStatusView | Enable/disable provider using managed secret reference | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe credential/configuration additionally requires finance privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-INTEGRATION-UPDATE |
| check_integration | API_ADMIN_INTEGRATION_CHECKRequest → Accepted | Queue bounded provider connectivity check | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-INTEGRATION-CHECK |
| request_provider_resync | API_ADMIN_INTEGRATION_RESYNCRequest → Accepted | Queue provider mirror reconciliation | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe resync requires finance privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-INTEGRATION-RESYNC |
| list_jobs | API_ADMIN_JOBSRequest → JobViewPage | Read redacted job processing state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-JOBS |
| get_job | API_ADMIN_JOBRequest → JobView | Read authorized background operation status | Match job capability and initiating admin purpose; arbitrary job IDs denied. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-JOB |
| retry_job | API_ADMIN_JOB_RETRYRequest → Accepted | Retry dead-letter job after cause correction | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Finance jobs additionally require finance privilege; immutable original payload. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-JOB-RETRY |
| get_operations_summary | API_ADMIN_OPERATIONSRequest → OperationsSummaryView | Read actionable operational summary | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-OPERATIONS |
| dispatch_outbox | JOB_OUTBOX_DISPATCHRequest → JobView | Publish durable intent to queue and recover expired leases | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-OUTBOX-DISPATCH |
| probe_integration | JOB_INTEGRATION_CHECKRequest → IntegrationStatusView | Check configured provider and persist masked operational state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-INTEGRATION-CHECK |

## AuditService

- **Module:** operations
- **Responsibility:** audit
- **Objects:** AuditRecord
- **Ports:** AuditRepository, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** ADM-029, SEC-007
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| list_audit | API_ADMIN_AUDITRequest → AuditViewPage | Read filtered redacted audit history | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-AUDIT |

## PrivacyService

- **Module:** family
- **Responsibility:** privacy
- **Objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Invariants:** Application operation checks role, explicit resource scope and state before aggregate mutation; no route-level business rules; no direct provider SDK. Return purpose-specific DTO only.
- **Persistence:** UnitOfWork commits aggregate change, audit and outbox atomically. Read DTO projections remain repository-scoped. Integration calls execute outside row locks with durable intent/result reconciliation.
- **Authorization:** Each public method has its own explicit authorization contract below; all callers, including internal adapters, use it.
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Chunks:** See Code Blueprint implementation ownership

| Operation | Input → output | Purpose | Authorization | Errors | API/worker |
|---|---|---|---|---|---|
| create_privacy_request | API_PARENT_PRIVACY_REQUESTRequest → PrivacyRequestView | Request family data access/correction/deletion or account closure | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-PARENT-PRIVACY-REQUEST |
| list_own_requests | API_PARENT_PRIVACY_LISTRequest → PrivacyRequestViewPage | Read own privacy request state | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-PARENT-PRIVACY-LIST |
| list_privacy_requests | API_ADMIN_PRIVACY_LISTRequest → PrivacyRequestViewPage | Read restricted privacy work queue | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR | API-ADMIN-PRIVACY-LIST |
| decide_request | API_ADMIN_PRIVACY_DECIDERequest → PrivacyRequestView | Record verified authority and retention-aware decision | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Never orphan active children or erase required finance records. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, LEGAL_HOLD, ACTIVE_GUARDIAN_REQUIRED | API-ADMIN-PRIVACY-DECIDE |
| download_export | API_PARENT_PRIVACY_EXPORTRequest → DownloadTicketView | Get ready verified family export | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Approved access request only; exclude unrelated guardian finances. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-PARENT-PRIVACY-EXPORT |
| set_legal_hold | API_ADMIN_LEGAL_HOLDRequest → Empty | Set or release audited retention hold | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | API-ADMIN-LEGAL-HOLD |
| process_request | JOB_PRIVACY_PROCESSRequest → JobView | Generate protected export or execute approved retention-aware deletion/closure | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-PRIVACY-PROCESS |
| apply_retention | JOB_RETENTIONRequest → JobView | Purge/anonymize only eligible unheld records from approved matrix | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE | JOB-RETENTION |
