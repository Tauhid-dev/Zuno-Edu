# API operation catalog

Status: DRAFT, scope 1.0 / architecture 1. Canonical structured contracts: [backend-catalog.json](backend-catalog.json). These are design contracts, not implemented classes or endpoints. Implementation ownership and requirement traceability are in CODE_BLUEPRINT.md and docs/planning/REQUIREMENT_TRACEABILITY.md.

All HTTP paths are versioned under `/api/v1`. WORKER entries are internal consumers and expose no HTTP route. Field-by-field request/response definitions are in [API_SCHEMA_CATALOG.md](API_SCHEMA_CATALOG.md); every operation refers to a concrete named schema, including path/query inputs. Transport conventions and status codes are in API_ARCHITECTURE.md.

## API-AUTH-REGISTER

- **Method/route:** POST /api/v1/auth/parents
- **Purpose:** Register guardian and create family
- **Roles:** public
- **Ownership / assignment / state:** Email uniqueness; accepted current required policy versions; rate-limit by address/network.
- **Request:** API_AUTH_REGISTERRequest
- **Response:** AccountView
- **Application operation:** AuthenticationService.register_parent
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-AUTH-VERIFY

- **Method/route:** POST /api/v1/auth/email-verifications
- **Purpose:** Consume single-use email verification
- **Roles:** public
- **Ownership / assignment / state:** Hashed token bound to account and purpose; 24h expiry.
- **Request:** API_AUTH_VERIFYRequest
- **Response:** Empty
- **Application operation:** AuthenticationService.verify_email
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-AUTH-RESEND

- **Method/route:** POST /api/v1/auth/email-verifications/resend
- **Purpose:** Resend verification without account enumeration
- **Roles:** public
- **Ownership / assignment / state:** Uniform response and throttled per identifier.
- **Request:** API_AUTH_RESENDRequest
- **Response:** Empty
- **Application operation:** AuthenticationService.resend_verification
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-AUTH-LOGIN

- **Method/route:** POST /api/v1/auth/sessions
- **Purpose:** Authenticate parent/staff/student
- **Roles:** public
- **Ownership / assignment / state:** Credential and account status; staff MFA challenge before privileged session.
- **Request:** API_AUTH_LOGINRequest
- **Response:** AuthOutcomeView
- **Application operation:** AuthenticationService.login
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE, INVALID_CREDENTIALS, ACCOUNT_SUSPENDED
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-AUTH-MFA

- **Method/route:** POST /api/v1/auth/mfa/verifications
- **Purpose:** Complete staff MFA challenge
- **Roles:** public
- **Ownership / assignment / state:** Short-lived challenge bound to browser, user and purpose.
- **Request:** API_AUTH_MFARequest
- **Response:** SessionView
- **Application operation:** AuthenticationService.verify_mfa
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE, INVALID_CREDENTIALS, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-AUTH-MFA-ENROL

- **Method/route:** POST /api/v1/account/mfa/enrolment
- **Purpose:** Create pending TOTP enrolment
- **Roles:** teacher, admin
- **Ownership / assignment / state:** Full staff session with recent password reauthentication OR unexpired staff-invitation MFA setup token; setup context permits only MFA setup operations.
- **Request:** API_AUTH_MFA_ENROLRequest
- **Response:** MfaSetupView
- **Application operation:** AuthenticationService.enrol_mfa
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, TCH-001
- **Consumers:** teacher, admin

## API-AUTH-MFA-CONFIRM

- **Method/route:** POST /api/v1/account/mfa/confirmation
- **Purpose:** Activate TOTP and issue recovery codes once
- **Roles:** teacher, admin
- **Ownership / assignment / state:** Purpose-bound setup token plus valid first TOTP proof; consume setup token, activate staff account and full MFA session atomically.
- **Request:** API_AUTH_MFA_CONFIRMRequest
- **Response:** MfaActivationView
- **Application operation:** AuthenticationService.confirm_mfa
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, TCH-001
- **Consumers:** teacher, admin

## API-AUTH-RESET-REQUEST

- **Method/route:** POST /api/v1/auth/password-reset-requests
- **Purpose:** Request account recovery
- **Roles:** public
- **Ownership / assignment / state:** Uniform response; adult verified email only; student recovery managed by guardian.
- **Request:** API_AUTH_RESET_REQUESTRequest
- **Response:** Empty
- **Application operation:** AuthenticationService.request_password_reset
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-AUTH-RESET

- **Method/route:** POST /api/v1/auth/password-resets
- **Purpose:** Reset adult password and revoke sessions
- **Roles:** public
- **Ownership / assignment / state:** One-time hashed token, 30-minute lifetime; revocation transactional.
- **Request:** API_AUTH_RESETRequest
- **Response:** Empty
- **Application operation:** AuthenticationService.reset_password
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-AUTH-ME

- **Method/route:** GET /api/v1/account/session
- **Purpose:** Get safe authenticated session identity
- **Roles:** parent, student, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_AUTH_MERequest
- **Response:** SessionView
- **Application operation:** AuthenticationService.get_session
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001
- **Consumers:** parent, student, teacher, admin

## API-AUTH-LOGOUT

- **Method/route:** DELETE /api/v1/auth/sessions/current
- **Purpose:** Revoke current session
- **Roles:** parent, student, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_AUTH_LOGOUTRequest
- **Response:** Empty
- **Application operation:** AuthenticationService.logout
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001
- **Consumers:** parent, student, teacher, admin

## API-ACCOUNT-PASSWORD

- **Method/route:** PUT /api/v1/account/password
- **Purpose:** Change own adult/staff password and revoke other sessions
- **Roles:** parent, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_ACCOUNT_PASSWORDRequest
- **Response:** Empty
- **Application operation:** AccountService.change_password
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021
- **Consumers:** parent, teacher, admin

## API-ACCOUNT-SESSIONS

- **Method/route:** GET /api/v1/account/sessions
- **Purpose:** List own devices
- **Roles:** parent, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_ACCOUNT_SESSIONSRequest
- **Response:** DeviceSessionViewPage
- **Application operation:** AccountService.list_sessions
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021
- **Consumers:** parent, teacher, admin

## API-ACCOUNT-REVOKE

- **Method/route:** DELETE /api/v1/account/sessions/{session_id}
- **Purpose:** Revoke selected own device
- **Roles:** parent, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_ACCOUNT_REVOKERequest
- **Response:** Empty
- **Application operation:** AccountService.revoke_session
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021
- **Consumers:** parent, teacher, admin

## API-ACCOUNT-PROFILE

- **Method/route:** GET /api/v1/account
- **Purpose:** Read own profile
- **Roles:** parent, student, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_ACCOUNT_PROFILERequest
- **Response:** AccountView
- **Application operation:** AccountService.get_account
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021, STU-019
- **Consumers:** parent, student, teacher, admin

## API-FAMILY-GET

- **Method/route:** GET /api/v1/parent/family
- **Purpose:** Read own family and linked students
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child.
- **Request:** API_FAMILY_GETRequest
- **Response:** FamilyView
- **Application operation:** FamilyService.get_family
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-006
- **Consumers:** parent

## API-PARENT-PROFILE

- **Method/route:** GET /api/v1/parent/profile
- **Purpose:** Read guardian contact/preferences
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_PARENT_PROFILERequest
- **Response:** GuardianView
- **Application operation:** AccountService.get_guardian_profile
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** AUTH-011, PAR-002, PAR-021
- **Consumers:** parent

## API-PARENT-UPDATE

- **Method/route:** PATCH /api/v1/parent/profile
- **Purpose:** Update guardian contact/preferences
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_PARENT_UPDATERequest
- **Response:** GuardianView
- **Application operation:** AccountService.update_guardian_profile
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-011, PAR-002, PAR-021
- **Consumers:** parent

## API-PARENT-EMAIL-CHANGE

- **Method/route:** POST /api/v1/parent/email-change
- **Purpose:** Begin verified contact email change
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. Reauthentication; new address never takes effect until verification.
- **Request:** API_PARENT_EMAIL_CHANGERequest
- **Response:** Empty
- **Application operation:** AccountService.request_email_change
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-011, PAR-002, PAR-021
- **Consumers:** parent

## API-PARENT-EMAIL-CONFIRM

- **Method/route:** POST /api/v1/parent/email-change/confirmation
- **Purpose:** Confirm new email and notify old address
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_PARENT_EMAIL_CONFIRMRequest
- **Response:** GuardianView
- **Application operation:** AccountService.confirm_email_change
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-011, PAR-002, PAR-021
- **Consumers:** parent

## API-STUDENT-CREATE

- **Method/route:** POST /api/v1/parent/students
- **Purpose:** Register child with required name and age
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. Create StudentProfile and verified GuardianStudent link to requesting parent atomically in same family; no pre-existing child required.
- **Request:** API_STUDENT_CREATERequest
- **Response:** StudentProfileView
- **Application operation:** StudentProfileService.create_student
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-005
- **Consumers:** parent

## API-STUDENT-GET

- **Method/route:** GET /api/v1/parent/students/{student_id}
- **Purpose:** Read linked child profile
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_STUDENT_GETRequest
- **Response:** StudentProfileView
- **Application operation:** StudentProfileService.get_student
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-005
- **Consumers:** parent

## API-STUDENT-UPDATE

- **Method/route:** PATCH /api/v1/parent/students/{student_id}
- **Purpose:** Update optional child information
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_STUDENT_UPDATERequest
- **Response:** StudentProfileView
- **Application operation:** StudentProfileService.update_student
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-005
- **Consumers:** parent

## API-STUDENT-AGE

- **Method/route:** PUT /api/v1/parent/students/{student_id}/age
- **Purpose:** Reconfirm required age
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_STUDENT_AGERequest
- **Response:** StudentProfileView
- **Application operation:** StudentProfileService.reconfirm_age
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-005
- **Consumers:** parent

## API-STUDENT-CREDENTIALS

- **Method/route:** POST /api/v1/parent/students/{student_id}/credentials
- **Purpose:** Provision or rotate child login
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Guardian password reauthentication; revoke prior student sessions.
- **Request:** API_STUDENT_CREDENTIALSRequest
- **Response:** StudentCredentialsView
- **Application operation:** StudentProfileService.provision_credentials
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-005
- **Consumers:** parent

## API-STUDENT-SELF

- **Method/route:** GET /api/v1/student/profile
- **Purpose:** Read own limited profile
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_SELFRequest
- **Response:** StudentSelfProfileView
- **Application operation:** StudentProfileService.get_student_self
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-004, PAR-005, TCH-009
- **Consumers:** student

## API-STUDENT-PREFERRED

- **Method/route:** PATCH /api/v1/student/profile
- **Purpose:** Update own preferred name and optional interests/experience
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_PREFERREDRequest
- **Response:** StudentSelfProfileView
- **Application operation:** StudentProfileService.update_preferred_name
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-004, PAR-005, TCH-009
- **Consumers:** student

## API-POLICY-LIST

- **Method/route:** GET /api/v1/public/policies
- **Purpose:** Read published policy versions
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_POLICY_LISTRequest
- **Response:** PolicyViewPage
- **Application operation:** ConsentService.list_policies
- **Domain objects:** PolicyDocument, PolicyAcknowledgement
- **Repository / ports:** ContentRepository, FamilyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** SEC-003
- **Consumers:** public

## API-CONSENT-LIST

- **Method/route:** GET /api/v1/parent/acknowledgements
- **Purpose:** Read family acknowledgement evidence
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link.
- **Request:** API_CONSENT_LISTRequest
- **Response:** AcknowledgementViewPage
- **Application operation:** ConsentService.list_acknowledgements
- **Domain objects:** PolicyDocument, PolicyAcknowledgement
- **Repository / ports:** ContentRepository, FamilyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-004, SEC-003
- **Consumers:** parent

## API-CONSENT-ACK

- **Method/route:** POST /api/v1/parent/acknowledgements
- **Purpose:** Record current policy acknowledgement
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_CONSENT_ACKRequest
- **Response:** AcknowledgementView
- **Application operation:** ConsentService.acknowledge
- **Domain objects:** PolicyDocument, PolicyAcknowledgement
- **Repository / ports:** ContentRepository, FamilyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, POLICY_VERSION_STALE
- **Requirements:** PAR-004, SEC-003
- **Consumers:** parent

## API-PUBLIC-PAGE

- **Method/route:** GET /api/v1/public/pages/{slug}
- **Purpose:** Read get page
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_PUBLIC_PAGERequest
- **Response:** PublicPageView
- **Application operation:** PublicContentService.get_page
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Consumers:** public

## API-PUBLIC-PROGRAMS

- **Method/route:** GET /api/v1/public/programs
- **Purpose:** Read list programs
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_PUBLIC_PROGRAMSRequest
- **Response:** PublicProgramViewPage
- **Application operation:** PublicContentService.list_programs
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Consumers:** public

## API-PUBLIC-COURSES

- **Method/route:** GET /api/v1/public/courses
- **Purpose:** Read list courses
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_PUBLIC_COURSESRequest
- **Response:** PublicCourseViewPage
- **Application operation:** PublicContentService.list_courses
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Consumers:** public

## API-PUBLIC-COURSE

- **Method/route:** GET /api/v1/public/courses/{slug}
- **Purpose:** Read get course
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_PUBLIC_COURSERequest
- **Response:** PublicCourseView
- **Application operation:** PublicContentService.get_course
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Consumers:** public

## API-PUBLIC-COHORTS

- **Method/route:** GET /api/v1/public/courses/{course_id}/cohorts
- **Purpose:** Read list public cohorts
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_PUBLIC_COHORTSRequest
- **Response:** PublicCohortViewPage
- **Application operation:** PublicContentService.list_public_cohorts
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Consumers:** public

## API-PUBLIC-TEACHERS

- **Method/route:** GET /api/v1/public/instructors
- **Purpose:** Read list public teachers
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_PUBLIC_TEACHERSRequest
- **Response:** PublicTeacherViewPage
- **Application operation:** PublicContentService.list_public_teachers
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Consumers:** public

## API-PUBLIC-CONTACT

- **Method/route:** POST /api/v1/public/contact
- **Purpose:** Submit contact enquiry to operations queue
- **Roles:** public
- **Ownership / assignment / state:** Rate limit; honeypot; no attachments, child profile matching or marketing subscription.
- **Request:** API_PUBLIC_CONTACTRequest
- **Response:** ContactReceipt
- **Application operation:** PublicContentService.submit_contact
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012
- **Consumers:** public

## API-ADMIN-PROGRAM-LIST

- **Method/route:** GET /api/v1/admin/programs
- **Purpose:** List draft and published programs
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PROGRAM_LISTRequest
- **Response:** ProgramViewPage
- **Application operation:** CourseService.list_programs
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-PROGRAM-CREATE

- **Method/route:** POST /api/v1/admin/programs
- **Purpose:** Create offering grouping
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PROGRAM_CREATERequest
- **Response:** ProgramView
- **Application operation:** CourseService.create_program
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-PROGRAM-UPDATE

- **Method/route:** PATCH /api/v1/admin/programs/{program_id}
- **Purpose:** Edit offering grouping
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PROGRAM_UPDATERequest
- **Response:** ProgramView
- **Application operation:** CourseService.update_program
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-PROGRAM-STATUS

- **Method/route:** PUT /api/v1/admin/programs/{program_id}/publication
- **Purpose:** Publish or archive program
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PROGRAM_STATUSRequest
- **Response:** ProgramView
- **Application operation:** CourseService.set_program_publication
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-COURSES

- **Method/route:** GET /api/v1/admin/courses
- **Purpose:** List all curriculum courses
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COURSESRequest
- **Response:** CourseViewPage
- **Application operation:** CourseService.list_courses
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-COURSE

- **Method/route:** GET /api/v1/admin/courses/{course_id}
- **Purpose:** Read administrative course details
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COURSERequest
- **Response:** CourseView
- **Application operation:** CourseService.get_course
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-COURSE-CREATE

- **Method/route:** POST /api/v1/admin/courses
- **Purpose:** Create reusable course
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COURSE_CREATERequest
- **Response:** CourseView
- **Application operation:** CourseService.create_course
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-COURSE-UPDATE

- **Method/route:** PATCH /api/v1/admin/courses/{course_id}
- **Purpose:** Edit course marketing metadata
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COURSE_UPDATERequest
- **Response:** CourseView
- **Application operation:** CourseService.update_course
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-COURSE-PUBLISH

- **Method/route:** POST /api/v1/admin/courses/{course_id}/publication
- **Purpose:** Publish approved course with ready revision
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COURSE_PUBLISHRequest
- **Response:** CourseView
- **Application operation:** CourseService.publish_course
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PUBLISH_VALIDATION_FAILED, LAUNCH_CONFIGURATION_REQUIRED
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-COURSE-ARCHIVE

- **Method/route:** POST /api/v1/admin/courses/{course_id}/archive
- **Purpose:** Archive course acquisition; preserve existing learning access
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COURSE_ARCHIVERequest
- **Response:** CourseView
- **Application operation:** CourseService.archive_course
- **Domain objects:** Program, Course, CurriculumRevision, PublicationPolicy
- **Repository / ports:** CourseRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-REVISION-LIST

- **Method/route:** GET /api/v1/admin/courses/{course_id}/revisions
- **Purpose:** List curriculum revisions
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REVISION_LISTRequest
- **Response:** CurriculumRevisionViewPage
- **Application operation:** CurriculumService.list_revisions
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-REVISION-CREATE

- **Method/route:** POST /api/v1/admin/courses/{course_id}/revisions
- **Purpose:** Create draft revision optionally copied from same course
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REVISION_CREATERequest
- **Response:** CurriculumRevisionView
- **Application operation:** CurriculumService.create_revision
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-REVISION-GET

- **Method/route:** GET /api/v1/admin/revisions/{revision_id}
- **Purpose:** Read full authoring hierarchy
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REVISION_GETRequest
- **Response:** CurriculumRevisionView
- **Application operation:** CurriculumService.get_revision
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-REVISION-PUBLISH

- **Method/route:** POST /api/v1/admin/revisions/{revision_id}/publication
- **Purpose:** Freeze validated curriculum revision
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REVISION_PUBLISHRequest
- **Response:** CurriculumRevisionView
- **Application operation:** CurriculumService.publish_revision
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PUBLISH_VALIDATION_FAILED, ASSET_NOT_READY
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-MODULE-CREATE

- **Method/route:** POST /api/v1/admin/revisions/{revision_id}/modules
- **Purpose:** Create draft module
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_MODULE_CREATERequest
- **Response:** ModuleView
- **Application operation:** CurriculumService.create_module
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-MODULE-UPDATE

- **Method/route:** PATCH /api/v1/admin/modules/{module_id}
- **Purpose:** Edit draft module
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_MODULE_UPDATERequest
- **Response:** ModuleView
- **Application operation:** CurriculumService.update_module
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-MODULE-DELETE

- **Method/route:** DELETE /api/v1/admin/modules/{module_id}
- **Purpose:** Remove unreferenced draft module
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references.
- **Request:** API_ADMIN_MODULE_DELETERequest
- **Response:** Empty
- **Application operation:** CurriculumService.delete_module
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-LESSON-CREATE

- **Method/route:** POST /api/v1/admin/modules/{module_id}/lessons
- **Purpose:** Create draft lesson
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_LESSON_CREATERequest
- **Response:** LessonView
- **Application operation:** CurriculumService.create_lesson
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-LESSON-UPDATE

- **Method/route:** PATCH /api/v1/admin/lessons/{lesson_id}
- **Purpose:** Edit draft lesson
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_LESSON_UPDATERequest
- **Response:** LessonView
- **Application operation:** CurriculumService.update_lesson
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-LESSON-DELETE

- **Method/route:** DELETE /api/v1/admin/lessons/{lesson_id}
- **Purpose:** Remove unreferenced draft lesson
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references.
- **Request:** API_ADMIN_LESSON_DELETERequest
- **Response:** Empty
- **Application operation:** CurriculumService.delete_lesson
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-BLOCK-CREATE

- **Method/route:** POST /api/v1/admin/lessons/{lesson_id}/blocks
- **Purpose:** Create draft block
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_BLOCK_CREATERequest
- **Response:** LessonBlockView
- **Application operation:** CurriculumService.create_block
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-BLOCK-UPDATE

- **Method/route:** PATCH /api/v1/admin/blocks/{block_id}
- **Purpose:** Edit draft block
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_BLOCK_UPDATERequest
- **Response:** LessonBlockView
- **Application operation:** CurriculumService.update_block
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-BLOCK-DELETE

- **Method/route:** DELETE /api/v1/admin/blocks/{block_id}
- **Purpose:** Remove unreferenced draft block
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references.
- **Request:** API_ADMIN_BLOCK_DELETERequest
- **Response:** Empty
- **Application operation:** CurriculumService.delete_block
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-RESOURCE-CREATE

- **Method/route:** POST /api/v1/admin/revisions/{revision_id}/resources
- **Purpose:** Create draft resource
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_RESOURCE_CREATERequest
- **Response:** ResourceView
- **Application operation:** CurriculumService.create_resource
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-RESOURCE-UPDATE

- **Method/route:** PATCH /api/v1/admin/resources/{resource_id}
- **Purpose:** Edit draft resource
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only.
- **Request:** API_ADMIN_RESOURCE_UPDATERequest
- **Response:** ResourceView
- **Application operation:** CurriculumService.update_resource
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-RESOURCE-DELETE

- **Method/route:** DELETE /api/v1/admin/resources/{resource_id}
- **Purpose:** Remove unreferenced draft resource
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references.
- **Request:** API_ADMIN_RESOURCE_DELETERequest
- **Response:** Empty
- **Application operation:** CurriculumService.delete_resource
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-RESOURCE-LIST

- **Method/route:** GET /api/v1/admin/revisions/{revision_id}/resources
- **Purpose:** List teaching assets in revision
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_RESOURCE_LISTRequest
- **Response:** ResourceViewPage
- **Application operation:** CurriculumService.list_resources
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-ADMIN-LESSON-GET

- **Method/route:** GET /api/v1/admin/lessons/{lesson_id}
- **Purpose:** Read authoring lesson and all block fields
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_LESSON_GETRequest
- **Response:** LessonView
- **Application operation:** CurriculumService.get_authoring_lesson
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-008, LRN-002, LRN-003, LRN-004
- **Consumers:** admin

## API-STUDENT-ENROLMENTS

- **Method/route:** GET /api/v1/student/enrolments
- **Purpose:** List own enrolled courses
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ENROLMENTSRequest
- **Response:** EnrolmentViewPage
- **Application operation:** EnrolmentService.list_student_enrolments
- **Domain objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007
- **Consumers:** student

## API-PARENT-ENROLMENTS

- **Method/route:** GET /api/v1/parent/students/{student_id}/enrolments
- **Purpose:** List linked child enrolment status
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_ENROLMENTSRequest
- **Response:** EnrolmentViewPage
- **Application operation:** EnrolmentService.list_child_enrolments
- **Domain objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008
- **Consumers:** parent

## API-STUDENT-CURRICULUM

- **Method/route:** GET /api/v1/student/enrolments/{enrolment_id}/curriculum
- **Purpose:** Read released modules of pinned revision
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_CURRICULUMRequest
- **Response:** CurriculumRevisionView
- **Application operation:** CurriculumService.get_learning_curriculum
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-002, LRN-003, LRN-004, STU-003, STU-004
- **Consumers:** student

## API-STUDENT-LESSON

- **Method/route:** GET /api/v1/student/enrolments/{enrolment_id}/lessons/{lesson_id}
- **Purpose:** Read released lesson and safe blocks
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_LESSONRequest
- **Response:** LessonView
- **Application operation:** CurriculumService.get_learning_lesson
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, CONTENT_UNRELEASED
- **Requirements:** LRN-002, LRN-003, LRN-004, STU-003, STU-004
- **Consumers:** student

## API-STUDENT-RESOURCE

- **Method/route:** GET /api/v1/student/enrolments/{enrolment_id}/resources
- **Purpose:** List released learning resources
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_RESOURCERequest
- **Response:** ResourceViewPage
- **Application operation:** CurriculumService.list_learning_resources
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-002, LRN-003, LRN-004, STU-003, STU-004
- **Consumers:** student

## API-TEACHER-COURSES

- **Method/route:** GET /api/v1/teacher/courses
- **Purpose:** List assigned courses
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_COURSESRequest
- **Response:** CourseViewPage
- **Application operation:** TeacherService.list_assigned_courses
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-005
- **Consumers:** teacher

## API-TEACHER-COHORTS

- **Method/route:** GET /api/v1/teacher/cohorts
- **Purpose:** List assigned cohorts
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_COHORTSRequest
- **Response:** CohortViewPage
- **Application operation:** CohortService.list_assigned_cohorts
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-001, CLS-005
- **Consumers:** teacher

## API-TEACHER-CURRICULUM

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/curriculum
- **Purpose:** Read pinned teaching curriculum including planned lessons
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_CURRICULUMRequest
- **Response:** CurriculumRevisionView
- **Application operation:** CurriculumService.get_teaching_curriculum
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-002, LRN-003, LRN-004, TCH-003
- **Consumers:** teacher

## API-TEACHER-LESSON

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/lessons/{lesson_id}
- **Purpose:** Read assigned teaching lesson plan
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_LESSONRequest
- **Response:** LessonView
- **Application operation:** CurriculumService.get_teaching_lesson
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-002, LRN-003, LRN-004, TCH-003
- **Consumers:** teacher

## API-TEACHER-RESOURCES

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/resources
- **Purpose:** Read assigned teaching resources
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_RESOURCESRequest
- **Response:** ResourceViewPage
- **Application operation:** CurriculumService.list_teaching_resources
- **Domain objects:** CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy
- **Repository / ports:** CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-002, LRN-003, LRN-004, TCH-003
- **Consumers:** teacher

## API-TEACHER-STUDENTS

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/students
- **Purpose:** Read assigned roster educational fields
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_STUDENTSRequest
- **Response:** TeachingStudentViewPage
- **Application operation:** TeacherService.list_assigned_students
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-005
- **Consumers:** teacher

## API-TEACHER-STUDENT

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/students/{student_id}
- **Purpose:** Read assigned learner educational profile
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_STUDENTRequest
- **Response:** TeachingStudentView
- **Application operation:** TeacherService.get_teaching_student
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-005
- **Consumers:** teacher

## API-ADMIN-PARENTS

- **Method/route:** GET /api/v1/admin/parents
- **Purpose:** Read authorized list parents
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PARENTSRequest
- **Response:** GuardianViewPage
- **Application operation:** FamilyService.list_parents_admin
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-006
- **Consumers:** admin

## API-ADMIN-FAMILY

- **Method/route:** GET /api/v1/admin/families/{family_id}
- **Purpose:** Read authorized get family
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FAMILYRequest
- **Response:** FamilyView
- **Application operation:** FamilyService.get_family_admin
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-006
- **Consumers:** admin

## API-ADMIN-STUDENTS

- **Method/route:** GET /api/v1/admin/students
- **Purpose:** Read authorized list students
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_STUDENTSRequest
- **Response:** StudentProfileViewPage
- **Application operation:** StudentProfileService.list_students_admin
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-004
- **Consumers:** admin

## API-ADMIN-STUDENT

- **Method/route:** GET /api/v1/admin/students/{student_id}
- **Purpose:** Read authorized get student
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_STUDENTRequest
- **Response:** StudentProfileView
- **Application operation:** StudentProfileService.get_student_admin
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-004
- **Consumers:** admin

## API-ADMIN-TEACHERS

- **Method/route:** GET /api/v1/admin/teachers
- **Purpose:** Read authorized list teachers
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_TEACHERSRequest
- **Response:** TeacherViewPage
- **Application operation:** TeacherService.list_teachers_admin
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-005, ADM-015, CLS-005
- **Consumers:** admin

## API-ADMIN-TEACHER

- **Method/route:** GET /api/v1/admin/teachers/{teacher_id}
- **Purpose:** Read authorized get teacher
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_TEACHERRequest
- **Response:** TeacherView
- **Application operation:** TeacherService.get_teacher_admin
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-005, ADM-015, CLS-005
- **Consumers:** admin

## API-ADMIN-GUARDIAN-LINK

- **Method/route:** POST /api/v1/admin/students/{student_id}/guardians
- **Purpose:** Link verified guardian to same family child
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Verification evidence reference mandatory; no cross-family transfer implicit.
- **Request:** API_ADMIN_GUARDIAN_LINKRequest
- **Response:** FamilyView
- **Application operation:** FamilyService.create_guardian_link
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-006
- **Consumers:** admin

## API-ADMIN-GUARDIAN-REVOKE

- **Method/route:** DELETE /api/v1/admin/students/{student_id}/guardians/{guardian_id}
- **Purpose:** Revoke guardian child access
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. At least one verified active guardian remains or safeguarding override is documented.
- **Request:** API_ADMIN_GUARDIAN_REVOKERequest
- **Response:** FamilyView
- **Application operation:** FamilyService.revoke_guardian_link
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-006
- **Consumers:** admin

## API-ADMIN-STUDENT-UPDATE

- **Method/route:** PATCH /api/v1/admin/students/{student_id}
- **Purpose:** Correct student data with reason
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_STUDENT_UPDATERequest
- **Response:** StudentProfileView
- **Application operation:** StudentProfileService.correct_student
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-004
- **Consumers:** admin

## API-ADMIN-STUDENT-ARCHIVE

- **Method/route:** POST /api/v1/admin/students/{student_id}/archive
- **Purpose:** Archive child after active obligations resolved
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_STUDENT_ARCHIVERequest
- **Response:** StudentProfileView
- **Application operation:** StudentProfileService.archive_student
- **Domain objects:** StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ACTIVE_ENROLMENT_EXISTS
- **Requirements:** ADM-004
- **Consumers:** admin

## API-ADMIN-INVITE

- **Method/route:** POST /api/v1/admin/staff-invitations
- **Purpose:** Invite teacher or constrained admin principal
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate admin principal required for teacher-to-admin duties.
- **Request:** API_ADMIN_INVITERequest
- **Response:** AccountView
- **Application operation:** AccountService.create_staff_invitation
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, INCOMPATIBLE_ROLE
- **Requirements:** ADM-003, ADM-006, AUTH-011
- **Consumers:** admin

## API-AUTH-INVITE-ACCEPT

- **Method/route:** POST /api/v1/auth/staff-invitations/accept
- **Purpose:** Accept staff invitation and require MFA setup
- **Roles:** public
- **Ownership / assignment / state:** Single-use invitation token; no privilege upgrades from request.
- **Request:** API_AUTH_INVITE_ACCEPTRequest
- **Response:** StaffSetupSessionView
- **Application operation:** AuthenticationService.accept_staff_invitation
- **Domain objects:** Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge
- **Repository / ports:** UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011
- **Consumers:** public

## API-ADMIN-ROLE

- **Method/route:** GET /api/v1/admin/accounts/{account_id}/roles
- **Purpose:** Read constrained role grants
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ROLERequest
- **Response:** RoleGrantView
- **Application operation:** AccountService.get_role_grants
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-003, ADM-006, AUTH-011
- **Consumers:** admin

## API-ADMIN-ROLE-UPDATE

- **Method/route:** PUT /api/v1/admin/accounts/{account_id}/roles
- **Purpose:** Change admin privileges with audit and session revocation
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Cannot self-escalate; no last identity-admin removal; teacher/admin principal incompatibility.
- **Request:** API_ADMIN_ROLE_UPDATERequest
- **Response:** RoleGrantView
- **Application operation:** AccountService.set_role_grants
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, INCOMPATIBLE_ROLE, LAST_ADMIN
- **Requirements:** ADM-003, ADM-006, AUTH-011
- **Consumers:** admin

## API-ADMIN-ACCOUNT-STATUS

- **Method/route:** PUT /api/v1/admin/accounts/{account_id}/status
- **Purpose:** Suspend or reactivate account and revoke affected sessions
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ACCOUNT_STATUSRequest
- **Response:** AccountView
- **Application operation:** AccountService.set_account_status
- **Domain objects:** Account, Guardian, TeacherProfile, RoleGrant
- **Repository / ports:** UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-003, ADM-006, AUTH-011
- **Consumers:** admin

## API-ADMIN-TEACHER-UPDATE

- **Method/route:** PATCH /api/v1/admin/teachers/{teacher_id}
- **Purpose:** Edit teacher public biography/profile
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_TEACHER_UPDATERequest
- **Response:** TeacherView
- **Application operation:** TeacherService.update_teacher
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-005, ADM-015, CLS-005
- **Consumers:** admin

## API-ADMIN-TEACHER-PUBLISH

- **Method/route:** PUT /api/v1/admin/teachers/{teacher_id}/publication
- **Purpose:** Publish or withdraw explicitly approved instructor profile
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_TEACHER_PUBLISHRequest
- **Response:** TeacherView
- **Application operation:** TeacherService.publish_teacher
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-005, ADM-015, CLS-005
- **Consumers:** admin

## API-ADMIN-TEACHER-ARCHIVE

- **Method/route:** POST /api/v1/admin/teachers/{teacher_id}/archive
- **Purpose:** Archive teacher after assignment reassignment
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_TEACHER_ARCHIVERequest
- **Response:** TeacherView
- **Application operation:** TeacherService.archive_teacher
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ACTIVE_ASSIGNMENT_EXISTS
- **Requirements:** ADM-005, ADM-015, CLS-005
- **Consumers:** admin

## API-TEACHER-PROFILE

- **Method/route:** GET /api/v1/teacher/profile
- **Purpose:** Read own teacher profile
- **Roles:** teacher
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_TEACHER_PROFILERequest
- **Response:** TeacherView
- **Application operation:** TeacherService.get_own_teacher_profile
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-005
- **Consumers:** teacher

## API-ADMIN-COHORTS

- **Method/route:** GET /api/v1/admin/cohorts
- **Purpose:** List operational cohorts
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COHORTSRequest
- **Response:** CohortViewPage
- **Application operation:** CohortService.list_cohorts
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-COHORT

- **Method/route:** GET /api/v1/admin/cohorts/{cohort_id}
- **Purpose:** Read cohort operational details
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COHORTRequest
- **Response:** CohortView
- **Application operation:** CohortService.get_cohort
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-COHORT-CREATE

- **Method/route:** POST /api/v1/admin/cohorts
- **Purpose:** Create course delivery pinned to published revision
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COHORT_CREATERequest
- **Response:** CohortView
- **Application operation:** CohortService.create_cohort
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-COHORT-UPDATE

- **Method/route:** PATCH /api/v1/admin/cohorts/{cohort_id}
- **Purpose:** Edit future cohort metadata and safe capacity
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COHORT_UPDATERequest
- **Response:** CohortView
- **Application operation:** CohortService.update_cohort
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, CAPACITY_BELOW_COMMITMENTS
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-COHORT-STATUS

- **Method/route:** PUT /api/v1/admin/cohorts/{cohort_id}/status
- **Purpose:** Open, close, start or complete delivery
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_COHORT_STATUSRequest
- **Response:** CohortView
- **Application operation:** CohortService.transition_cohort
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, LAUNCH_CONFIGURATION_REQUIRED
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-COHORT-CANCEL

- **Method/route:** POST /api/v1/admin/cohorts/{cohort_id}/cancellation
- **Purpose:** Cancel delivery and create refund review tasks
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Education can cancel delivery but cannot execute refund.
- **Request:** API_ADMIN_COHORT_CANCELRequest
- **Response:** Accepted
- **Application operation:** CohortService.cancel_cohort
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 202
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-ASSIGNMENTS

- **Method/route:** GET /api/v1/admin/cohorts/{cohort_id}/teacher-assignments
- **Purpose:** List cohort teaching grants
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSIGNMENTSRequest
- **Response:** TeacherAssignmentViewPage
- **Application operation:** CohortService.list_teacher_assignments
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-ASSIGNMENT-CREATE

- **Method/route:** POST /api/v1/admin/cohorts/{cohort_id}/teacher-assignments
- **Purpose:** Assign active teacher to cohort/session
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSIGNMENT_CREATERequest
- **Response:** TeacherAssignmentView
- **Application operation:** CohortService.create_teacher_assignment
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-ASSIGNMENT-REVOKE

- **Method/route:** DELETE /api/v1/admin/teacher-assignments/{assignment_id}
- **Purpose:** Revoke teaching access immediately
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSIGNMENT_REVOKERequest
- **Response:** Empty
- **Application operation:** CohortService.revoke_teacher_assignment
- **Domain objects:** Cohort, TeacherAssignment, CurriculumRevision
- **Repository / ports:** DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-013, ADM-015, CLS-001, CLS-005
- **Consumers:** admin

## API-ADMIN-SESSIONS

- **Method/route:** GET /api/v1/admin/cohorts/{cohort_id}/sessions
- **Purpose:** List all delivery sessions
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SESSIONSRequest
- **Response:** ClassSessionViewPage
- **Application operation:** SchedulingService.list_cohort_sessions
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011
- **Consumers:** admin

## API-ADMIN-SESSION-CREATE

- **Method/route:** POST /api/v1/admin/cohorts/{cohort_id}/sessions
- **Purpose:** Schedule one class occurrence
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SESSION_CREATERequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.create_class_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, DST_AMBIGUOUS
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011
- **Consumers:** admin

## API-ADMIN-RECURRENCE

- **Method/route:** POST /api/v1/admin/cohorts/{cohort_id}/session-series
- **Purpose:** Materialize bounded weekly occurrences transactionally
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_RECURRENCERequest
- **Response:** ClassSessionViewPage
- **Application operation:** SchedulingService.create_session_series
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, DST_AMBIGUOUS
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011
- **Consumers:** admin

## API-ADMIN-SESSION-UPDATE

- **Method/route:** PATCH /api/v1/admin/sessions/{session_id}
- **Purpose:** Edit session title/lesson without rescheduling
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SESSION_UPDATERequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.update_class_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011
- **Consumers:** admin

## API-PARENT-SCHEDULE

- **Method/route:** GET /api/v1/parent/schedule
- **Purpose:** List parent authorized upcoming classes
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_SCHEDULERequest
- **Response:** ClassSessionViewPage
- **Application operation:** SchedulingService.list_parent_schedule
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-011, PAR-009
- **Consumers:** parent

## API-PARENT-SESSION

- **Method/route:** GET /api/v1/parent/sessions/{session_id}
- **Purpose:** Read authorized class session details
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_SESSIONRequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.get_parent_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-011, PAR-009
- **Consumers:** parent

## API-STUDENT-SCHEDULE

- **Method/route:** GET /api/v1/student/schedule
- **Purpose:** List student authorized upcoming classes
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_SCHEDULERequest
- **Response:** ClassSessionViewPage
- **Application operation:** SchedulingService.list_student_schedule
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-011, STU-013
- **Consumers:** student

## API-STUDENT-SESSION

- **Method/route:** GET /api/v1/student/sessions/{session_id}
- **Purpose:** Read authorized class session details
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_SESSIONRequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.get_student_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-011, STU-013
- **Consumers:** student

## API-TEACHER-SCHEDULE

- **Method/route:** GET /api/v1/teacher/schedule
- **Purpose:** List teacher authorized upcoming classes
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_SCHEDULERequest
- **Response:** ClassSessionViewPage
- **Application operation:** SchedulingService.list_teacher_schedule
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-011, TCH-005, TCH-006
- **Consumers:** teacher

## API-TEACHER-SESSION

- **Method/route:** GET /api/v1/teacher/sessions/{session_id}
- **Purpose:** Read authorized class session details
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_SESSIONRequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.get_teacher_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-011, TCH-005, TCH-006
- **Consumers:** teacher

## API-TEACHER-RESCHEDULE

- **Method/route:** POST /api/v1/teacher/sessions/{session_id}/reschedule
- **Purpose:** Reschedule authorized session and queue provider updates
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Start >= now+24h; future assigned session only; no overlap for teacher/learner.
- **Request:** API_TEACHER_RESCHEDULERequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.reschedule_teacher_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, RESCHEDULE_WINDOW_CLOSED, DST_AMBIGUOUS
- **Requirements:** CLS-002, CLS-003, CLS-004, CLS-011, TCH-005, TCH-006
- **Consumers:** teacher

## API-ADMIN-RESCHEDULE

- **Method/route:** POST /api/v1/admin/sessions/{session_id}/reschedule
- **Purpose:** Reschedule authorized session and queue provider updates
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Override short notice requires reason; overlaps still rejected.
- **Request:** API_ADMIN_RESCHEDULERequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.reschedule_admin_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, RESCHEDULE_WINDOW_CLOSED, DST_AMBIGUOUS
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011
- **Consumers:** admin

## API-ADMIN-SESSION-CANCEL

- **Method/route:** POST /api/v1/admin/sessions/{session_id}/cancellation
- **Purpose:** Cancel class and queue Zoom/calendar cancellation and notices
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SESSION_CANCELRequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.cancel_class_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011
- **Consumers:** admin

## API-ADMIN-SESSION-COMPLETE

- **Method/route:** POST /api/v1/admin/sessions/{session_id}/completion
- **Purpose:** Complete past session after attendance review
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SESSION_COMPLETERequest
- **Response:** ClassSessionView
- **Application operation:** SchedulingService.complete_class_session
- **Domain objects:** ClassSession, SchedulePolicy, TeacherAssignment, Cohort
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-014, CLS-002, CLS-003, CLS-004, CLS-011
- **Consumers:** admin

## API-TEACHER-START

- **Method/route:** POST /api/v1/teacher/sessions/{session_id}/start
- **Purpose:** Fetch fresh authorized Zoom host handoff
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Assigned authorized host; now within start-30m through scheduled end.
- **Request:** API_TEACHER_STARTRequest
- **Response:** JoinLinkView
- **Application operation:** LiveClassService.start_assigned_class
- **Domain objects:** ClassSession, IntegrationBinding, TeachingAccessPolicy
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009, TCH-004
- **Consumers:** teacher

## API-STUDENT-JOIN

- **Method/route:** POST /api/v1/student/sessions/{session_id}/join
- **Purpose:** Fetch eligible learner Zoom join handoff
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Active enrolment; now within start-15m through scheduled end; no host URL.
- **Request:** API_STUDENT_JOINRequest
- **Response:** JoinLinkView
- **Application operation:** LiveClassService.join_student_class
- **Domain objects:** ClassSession, IntegrationBinding, TeachingAccessPolicy
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009, STU-014
- **Consumers:** student

## API-PARENT-JOIN

- **Method/route:** POST /api/v1/parent/sessions/{session_id}/join
- **Purpose:** Fetch eligible learner Zoom join handoff
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Active enrolment; now within start-15m through scheduled end; no host URL.
- **Request:** API_PARENT_JOINRequest
- **Response:** JoinLinkView
- **Application operation:** LiveClassService.join_parent_class
- **Domain objects:** ClassSession, IntegrationBinding, TeachingAccessPolicy
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009
- **Consumers:** parent

## API-ADMIN-ENROLMENTS

- **Method/route:** GET /api/v1/admin/enrolments
- **Purpose:** List delivery enrolments without financial fields
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ENROLMENTSRequest
- **Response:** EnrolmentViewPage
- **Application operation:** EnrolmentService.list_enrolments
- **Domain objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007
- **Consumers:** admin

## API-ADMIN-ENROLMENT

- **Method/route:** GET /api/v1/admin/enrolments/{enrolment_id}
- **Purpose:** Read educational enrolment status
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ENROLMENTRequest
- **Response:** EnrolmentView
- **Application operation:** EnrolmentService.get_enrolment
- **Domain objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007
- **Consumers:** admin

## API-ADMIN-ENROLMENT-CANCEL

- **Method/route:** POST /api/v1/admin/enrolments/{enrolment_id}/cancellation
- **Purpose:** Cancel educational access with auditable reason
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Any money movement requires finance workflow.
- **Request:** API_ADMIN_ENROLMENT_CANCELRequest
- **Response:** EnrolmentView
- **Application operation:** EnrolmentService.cancel_enrolment
- **Domain objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007
- **Consumers:** admin

## API-PARENT-CHECKOUT-CANCEL

- **Method/route:** POST /api/v1/parent/enrolments/{enrolment_id}/hold-cancellation
- **Purpose:** Release own unpaid hold
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Held/pending payment only; provider expiry reconciled.
- **Request:** API_PARENT_CHECKOUT_CANCELRequest
- **Response:** EnrolmentView
- **Application operation:** EnrolmentService.cancel_hold
- **Domain objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008
- **Consumers:** parent

## API-TEACHER-ATTENDANCE

- **Method/route:** GET /api/v1/teacher/sessions/{session_id}/attendance
- **Purpose:** Read authorized session attendance roster
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_ATTENDANCERequest
- **Response:** AttendanceViewPage
- **Application operation:** AttendanceService.list_teacher_attendance
- **Domain objects:** AttendanceRecord, ClassSession, TeachingAccessPolicy
- **Repository / ports:** AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-010, TCH-007, TCH-008
- **Consumers:** teacher

## API-TEACHER-ATTENDANCE-RECORD

- **Method/route:** PUT /api/v1/teacher/sessions/{session_id}/students/{student_id}/attendance
- **Purpose:** Record or amend attendance
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Student enrolled in this session cohort.
- **Request:** API_TEACHER_ATTENDANCE_RECORDRequest
- **Response:** AttendanceView
- **Application operation:** AttendanceService.record_teacher_attendance
- **Domain objects:** AttendanceRecord, ClassSession, TeachingAccessPolicy
- **Repository / ports:** AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** CLS-010, TCH-007, TCH-008
- **Consumers:** teacher

## API-ADMIN-ATTENDANCE

- **Method/route:** GET /api/v1/admin/sessions/{session_id}/attendance
- **Purpose:** Read authorized session attendance roster
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ATTENDANCERequest
- **Response:** AttendanceViewPage
- **Application operation:** AttendanceService.list_admin_attendance
- **Domain objects:** AttendanceRecord, ClassSession, TeachingAccessPolicy
- **Repository / ports:** AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-017, CLS-010
- **Consumers:** admin

## API-ADMIN-ATTENDANCE-RECORD

- **Method/route:** PUT /api/v1/admin/sessions/{session_id}/students/{student_id}/attendance
- **Purpose:** Record or amend attendance
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Student enrolled in this session cohort.
- **Request:** API_ADMIN_ATTENDANCE_RECORDRequest
- **Response:** AttendanceView
- **Application operation:** AttendanceService.record_admin_attendance
- **Domain objects:** AttendanceRecord, ClassSession, TeachingAccessPolicy
- **Repository / ports:** AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-017, CLS-010
- **Consumers:** admin

## API-PARENT-ATTENDANCE

- **Method/route:** GET /api/v1/parent/students/{student_id}/attendance
- **Purpose:** Read own or linked child attendance
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_ATTENDANCERequest
- **Response:** AttendanceViewPage
- **Application operation:** AttendanceService.list_parent_attendance
- **Domain objects:** AttendanceRecord, ClassSession, TeachingAccessPolicy
- **Repository / ports:** AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-010, PAR-010
- **Consumers:** parent

## API-STUDENT-ATTENDANCE

- **Method/route:** GET /api/v1/student/attendance
- **Purpose:** Read own or linked child attendance
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ATTENDANCERequest
- **Response:** AttendanceViewPage
- **Application operation:** AttendanceService.list_student_attendance
- **Domain objects:** AttendanceRecord, ClassSession, TeachingAccessPolicy
- **Repository / ports:** AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-010, STU-015
- **Consumers:** student

## API-ADMIN-QUIZZES

- **Method/route:** GET /api/v1/admin/revisions/{revision_id}/quizzes
- **Purpose:** List quiz authoring definitions
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_QUIZZESRequest
- **Response:** QuizViewPage
- **Application operation:** QuizService.list_quizzes
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003
- **Consumers:** admin

## API-ADMIN-QUIZ

- **Method/route:** GET /api/v1/admin/quizzes/{quiz_id}
- **Purpose:** Read quiz questions and grading keys
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_QUIZRequest
- **Response:** QuizView
- **Application operation:** QuizService.get_quiz
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003
- **Consumers:** admin

## API-ADMIN-QUIZ-CREATE

- **Method/route:** POST /api/v1/admin/lessons/{lesson_id}/quizzes
- **Purpose:** Create draft formative quiz
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only.
- **Request:** API_ADMIN_QUIZ_CREATERequest
- **Response:** QuizView
- **Application operation:** QuizService.create_quiz
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003
- **Consumers:** admin

## API-ADMIN-QUIZ-UPDATE

- **Method/route:** PATCH /api/v1/admin/quizzes/{quiz_id}
- **Purpose:** Edit draft quiz rules
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only.
- **Request:** API_ADMIN_QUIZ_UPDATERequest
- **Response:** QuizView
- **Application operation:** QuizService.update_quiz
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003
- **Consumers:** admin

## API-ADMIN-QUESTION-PUT

- **Method/route:** PUT /api/v1/admin/quizzes/{quiz_id}/questions
- **Purpose:** Replace ordered draft questions atomically
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft only; complete validated answer key; positions unique.
- **Request:** API_ADMIN_QUESTION_PUTRequest
- **Response:** QuizView
- **Application operation:** QuizService.replace_questions
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003
- **Consumers:** admin

## API-ADMIN-QUIZ-DELETE

- **Method/route:** DELETE /api/v1/admin/quizzes/{quiz_id}
- **Purpose:** Delete unreferenced draft quiz
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_QUIZ_DELETERequest
- **Response:** Empty
- **Application operation:** QuizService.delete_quiz
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003
- **Consumers:** admin

## API-STUDENT-QUIZ

- **Method/route:** GET /api/v1/student/enrolments/{enrolment_id}/quizzes/{quiz_id}
- **Purpose:** Read released quiz without answer key
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_QUIZRequest
- **Response:** LearnerQuizView
- **Application operation:** QuizService.get_learner_quiz
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-001, ASM-002, ASM-003, STU-007
- **Consumers:** student

## API-STUDENT-ATTEMPTS

- **Method/route:** GET /api/v1/student/quizzes/{quiz_id}/attempts
- **Purpose:** Read own attempt history
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ATTEMPTSRequest
- **Response:** QuizAttemptViewPage
- **Application operation:** QuizService.list_attempts
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-001, ASM-002, ASM-003, STU-007
- **Consumers:** student

## API-STUDENT-ATTEMPT-CREATE

- **Method/route:** POST /api/v1/student/enrolments/{enrolment_id}/quizzes/{quiz_id}/attempts
- **Purpose:** Start attempt with immutable quiz snapshot
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ATTEMPT_CREATERequest
- **Response:** QuizAttemptView
- **Application operation:** QuizService.start_attempt
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ATTEMPT_LIMIT_REACHED
- **Requirements:** ASM-001, ASM-002, ASM-003, STU-007
- **Consumers:** student

## API-STUDENT-ATTEMPT-SAVE

- **Method/route:** PUT /api/v1/student/quiz-attempts/{attempt_id}/answers
- **Purpose:** Save selections on own in-progress attempt
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ATTEMPT_SAVERequest
- **Response:** QuizAttemptView
- **Application operation:** QuizService.save_answers
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-001, ASM-002, ASM-003, STU-007
- **Consumers:** student

## API-STUDENT-ATTEMPT-SUBMIT

- **Method/route:** POST /api/v1/student/quiz-attempts/{attempt_id}/submission
- **Purpose:** Submit once and release formative score
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ATTEMPT_SUBMITRequest
- **Response:** QuizAttemptView
- **Application operation:** QuizService.submit_attempt
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ATTEMPT_ALREADY_SUBMITTED
- **Requirements:** ASM-001, ASM-002, ASM-003, STU-007
- **Consumers:** student

## API-TEACHER-QUIZ-RESULTS

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/quiz-attempts
- **Purpose:** Read assigned learners submitted quiz scores
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_QUIZ_RESULTSRequest
- **Response:** QuizAttemptViewPage
- **Application operation:** QuizService.list_teaching_attempts
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-001, ASM-002, ASM-003
- **Consumers:** teacher

## API-ADMIN-QUIZ-RESULTS

- **Method/route:** GET /api/v1/admin/cohorts/{cohort_id}/quiz-attempts
- **Purpose:** Oversee submitted quiz outcomes
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_QUIZ_RESULTSRequest
- **Response:** QuizAttemptViewPage
- **Application operation:** QuizService.list_admin_attempts
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-010, ASM-001, ASM-002, ASM-003
- **Consumers:** admin

## API-PARENT-QUIZ-RESULTS

- **Method/route:** GET /api/v1/parent/students/{student_id}/quiz-results
- **Purpose:** Read released child quiz results
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_QUIZ_RESULTSRequest
- **Response:** ChildQuizResultViewPage
- **Application operation:** QuizService.list_child_quiz_results
- **Domain objects:** Quiz, QuizQuestion, QuizAttempt, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-001, ASM-002, ASM-003
- **Consumers:** parent

## API-ADMIN-ASSIGNMENTS-LIST

- **Method/route:** GET /api/v1/admin/revisions/{revision_id}/assignments
- **Purpose:** List assignment/project authoring definitions
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSIGNMENTS_LISTRequest
- **Response:** AssignmentViewPage
- **Application operation:** AssignmentService.list_assignments
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-011, ASM-004
- **Consumers:** admin

## API-ADMIN-ASSIGNMENT-GET

- **Method/route:** GET /api/v1/admin/assignments/{assignment_id}
- **Purpose:** Read assignment authoring detail
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSIGNMENT_GETRequest
- **Response:** AssignmentView
- **Application operation:** AssignmentService.get_assignment
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-011, ASM-004
- **Consumers:** admin

## API-ADMIN-ASSIGNMENT-DEFINE

- **Method/route:** POST /api/v1/admin/lessons/{lesson_id}/assignments
- **Purpose:** Create assignment or project definition
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only.
- **Request:** API_ADMIN_ASSIGNMENT_DEFINERequest
- **Response:** AssignmentView
- **Application operation:** AssignmentService.create_assignment
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-011, ASM-004
- **Consumers:** admin

## API-ADMIN-ASSIGNMENT-EDIT

- **Method/route:** PATCH /api/v1/admin/assignments/{assignment_id}
- **Purpose:** Edit draft assignment definition
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only.
- **Request:** API_ADMIN_ASSIGNMENT_EDITRequest
- **Response:** AssignmentView
- **Application operation:** AssignmentService.update_assignment
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-011, ASM-004
- **Consumers:** admin

## API-ADMIN-ASSIGNMENT-DELETE

- **Method/route:** DELETE /api/v1/admin/assignments/{assignment_id}
- **Purpose:** Delete unreferenced draft assignment
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSIGNMENT_DELETERequest
- **Response:** Empty
- **Application operation:** AssignmentService.delete_assignment
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE
- **Requirements:** ADM-011, ASM-004
- **Consumers:** admin

## API-STUDENT-ASSIGNMENTS

- **Method/route:** GET /api/v1/student/enrolments/{enrolment_id}/assignments
- **Purpose:** Read permitted assignment and project work
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ASSIGNMENTSRequest
- **Response:** AssignmentViewPage
- **Application operation:** AssignmentService.list_student_assignments
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-004, STU-008
- **Consumers:** student

## API-PARENT-ASSIGNMENTS

- **Method/route:** GET /api/v1/parent/students/{student_id}/assignments
- **Purpose:** Read permitted assignment and project work
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_ASSIGNMENTSRequest
- **Response:** AssignmentViewPage
- **Application operation:** AssignmentService.list_parent_assignments
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-004
- **Consumers:** parent

## API-TEACHER-ASSIGNMENTS

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/assignments
- **Purpose:** Read permitted assignment and project work
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_ASSIGNMENTSRequest
- **Response:** AssignmentViewPage
- **Application operation:** AssignmentService.list_teacher_assignments
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-004, TCH-010
- **Consumers:** teacher

## API-STUDENT-SUBMISSIONS

- **Method/route:** GET /api/v1/student/assignments/{assignment_id}/submissions
- **Purpose:** Read own immutable submission history
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_SUBMISSIONSRequest
- **Response:** SubmissionViewPage
- **Application operation:** SubmissionService.list_own_submissions
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-005, STU-009, STU-010
- **Consumers:** student

## API-STUDENT-SUBMISSION-CREATE

- **Method/route:** POST /api/v1/student/enrolments/{enrolment_id}/assignments/{assignment_id}/submissions
- **Purpose:** Start own assignment submission/revision
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. New attempt only if policy permits or prior attempt returned.
- **Request:** API_STUDENT_SUBMISSION_CREATERequest
- **Response:** SubmissionView
- **Application operation:** SubmissionService.create_submission
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-005, STU-009, STU-010
- **Consumers:** student

## API-STUDENT-SUBMISSION-SAVE

- **Method/route:** PUT /api/v1/student/submissions/{submission_id}
- **Purpose:** Save own draft work and ready scanned file links
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_SUBMISSION_SAVERequest
- **Response:** SubmissionView
- **Application operation:** SubmissionService.save_submission
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSET_NOT_READY
- **Requirements:** ASM-005, STU-009, STU-010
- **Consumers:** student

## API-STUDENT-SUBMISSION-SEND

- **Method/route:** POST /api/v1/student/submissions/{submission_id}/submission
- **Purpose:** Freeze own work and enqueue assessment notice
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Late work accepted and labelled until cohort complete or explicitly closed.
- **Request:** API_STUDENT_SUBMISSION_SENDRequest
- **Response:** SubmissionView
- **Application operation:** SubmissionService.submit_work
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSIGNMENT_CLOSED, ASSET_NOT_READY
- **Requirements:** ASM-005, STU-009, STU-010
- **Consumers:** student

## API-STUDENT-SUBMISSION-DELETE

- **Method/route:** DELETE /api/v1/student/submissions/{submission_id}
- **Purpose:** Discard own unsubmitted draft
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_SUBMISSION_DELETERequest
- **Response:** Empty
- **Application operation:** SubmissionService.delete_draft
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-005, STU-009, STU-010
- **Consumers:** student

## API-PARENT-SUBMISSIONS

- **Method/route:** GET /api/v1/parent/students/{student_id}/submissions
- **Purpose:** Read child submission status/history
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_SUBMISSIONSRequest
- **Response:** ChildSubmissionStatusViewPage
- **Application operation:** SubmissionService.list_child_submissions
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-005
- **Consumers:** parent

## API-TEACHER-SUBMISSIONS

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/submissions
- **Purpose:** Read authorized submitted work review queue
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_SUBMISSIONSRequest
- **Response:** SubmissionViewPage
- **Application operation:** SubmissionService.list_teacher_submissions
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-005
- **Consumers:** teacher

## API-TEACHER-SUBMISSION

- **Method/route:** GET /api/v1/teacher/submissions/{submission_id}
- **Purpose:** Read authorized frozen work version
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_SUBMISSIONRequest
- **Response:** SubmissionView
- **Application operation:** SubmissionService.get_teacher_submission
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-005
- **Consumers:** teacher

## API-TEACHER-RETURN

- **Method/route:** POST /api/v1/teacher/submissions/{submission_id}/return
- **Purpose:** Return work for a new immutable revision
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_RETURNRequest
- **Response:** SubmissionView
- **Application operation:** AssessmentService.return_teacher_submission
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-006, ASM-007, TCH-011, TCH-012
- **Consumers:** teacher

## API-TEACHER-ASSESSMENT

- **Method/route:** PUT /api/v1/teacher/submissions/{submission_id}/assessment
- **Purpose:** Save draft marking against frozen submission
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_ASSESSMENTRequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.save_teacher_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-006, ASM-007, TCH-011, TCH-012
- **Consumers:** teacher

## API-TEACHER-ASSESSMENT-GET

- **Method/route:** GET /api/v1/teacher/submissions/{submission_id}/assessment
- **Purpose:** Read permitted draft/released marking
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_ASSESSMENT_GETRequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.get_teacher_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-006, ASM-007, TCH-011, TCH-012
- **Consumers:** teacher

## API-TEACHER-ASSESSMENT-RELEASE

- **Method/route:** POST /api/v1/teacher/assessments/{assessment_id}/release
- **Purpose:** Release validated assessment to learner and guardian
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_ASSESSMENT_RELEASERequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.release_teacher_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-006, ASM-007, TCH-011, TCH-012
- **Consumers:** teacher

## API-TEACHER-ASSESSMENT-WITHDRAW

- **Method/route:** POST /api/v1/teacher/assessments/{assessment_id}/withdrawal
- **Purpose:** Withdraw erroneous release and preserve correction history
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_ASSESSMENT_WITHDRAWRequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.withdraw_teacher_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-006, ASM-007, TCH-011, TCH-012
- **Consumers:** teacher

## API-TEACHER-FEEDBACK-LIST

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/feedback
- **Purpose:** Read permitted feedback drafts/releases
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_FEEDBACK_LISTRequest
- **Response:** FeedbackViewPage
- **Application operation:** FeedbackService.list_teacher_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-008, TCH-013
- **Consumers:** teacher

## API-TEACHER-FEEDBACK-CREATE

- **Method/route:** POST /api/v1/teacher/cohorts/{cohort_id}/feedback
- **Purpose:** Create draft educational feedback
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_FEEDBACK_CREATERequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.create_teacher_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-008, TCH-013
- **Consumers:** teacher

## API-TEACHER-FEEDBACK-UPDATE

- **Method/route:** PATCH /api/v1/teacher/feedback/{feedback_id}
- **Purpose:** Revise draft feedback; released content requires withdrawal first
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_FEEDBACK_UPDATERequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.update_teacher_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-008, TCH-013
- **Consumers:** teacher

## API-TEACHER-FEEDBACK-RELEASE

- **Method/route:** POST /api/v1/teacher/feedback/{feedback_id}/release
- **Purpose:** Release educational feedback and notify
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_FEEDBACK_RELEASERequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.release_teacher_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-008, TCH-013
- **Consumers:** teacher

## API-TEACHER-FEEDBACK-WITHDRAW

- **Method/route:** POST /api/v1/teacher/feedback/{feedback_id}/withdrawal
- **Purpose:** Withdraw mistaken feedback release with reason
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_FEEDBACK_WITHDRAWRequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.withdraw_teacher_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ASM-008, TCH-013
- **Consumers:** teacher

## API-TEACHER-PROGRESS

- **Method/route:** GET /api/v1/teacher/cohorts/{cohort_id}/progress
- **Purpose:** Read permitted learner completion evidence
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_PROGRESSRequest
- **Response:** ProgressViewPage
- **Application operation:** ProgressService.list_teacher_progress
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-007, LRN-008, TCH-014
- **Consumers:** teacher

## API-ADMIN-SUBMISSIONS

- **Method/route:** GET /api/v1/admin/cohorts/{cohort_id}/submissions
- **Purpose:** Read authorized submitted work review queue
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SUBMISSIONSRequest
- **Response:** SubmissionViewPage
- **Application operation:** SubmissionService.list_admin_submissions
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-005
- **Consumers:** admin

## API-ADMIN-SUBMISSION

- **Method/route:** GET /api/v1/admin/submissions/{submission_id}
- **Purpose:** Read authorized frozen work version
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SUBMISSIONRequest
- **Response:** SubmissionView
- **Application operation:** SubmissionService.get_admin_submission
- **Domain objects:** Submission, FileAsset, ReleasePolicy
- **Repository / ports:** AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-005
- **Consumers:** admin

## API-ADMIN-RETURN

- **Method/route:** POST /api/v1/admin/submissions/{submission_id}/return
- **Purpose:** Return work for a new immutable revision
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_RETURNRequest
- **Response:** SubmissionView
- **Application operation:** AssessmentService.return_admin_submission
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-012, ASM-006, ASM-007
- **Consumers:** admin

## API-ADMIN-ASSESSMENT

- **Method/route:** PUT /api/v1/admin/submissions/{submission_id}/assessment
- **Purpose:** Save draft marking against frozen submission
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSESSMENTRequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.save_admin_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-012, ASM-006, ASM-007
- **Consumers:** admin

## API-ADMIN-ASSESSMENT-GET

- **Method/route:** GET /api/v1/admin/submissions/{submission_id}/assessment
- **Purpose:** Read permitted draft/released marking
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSESSMENT_GETRequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.get_admin_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-012, ASM-006, ASM-007
- **Consumers:** admin

## API-ADMIN-ASSESSMENT-RELEASE

- **Method/route:** POST /api/v1/admin/assessments/{assessment_id}/release
- **Purpose:** Release validated assessment to learner and guardian
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSESSMENT_RELEASERequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.release_admin_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-012, ASM-006, ASM-007
- **Consumers:** admin

## API-ADMIN-ASSESSMENT-WITHDRAW

- **Method/route:** POST /api/v1/admin/assessments/{assessment_id}/withdrawal
- **Purpose:** Withdraw erroneous release and preserve correction history
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSESSMENT_WITHDRAWRequest
- **Response:** AssessmentView
- **Application operation:** AssessmentService.withdraw_admin_assessment
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-012, ASM-006, ASM-007
- **Consumers:** admin

## API-ADMIN-FEEDBACK-LIST

- **Method/route:** GET /api/v1/admin/cohorts/{cohort_id}/feedback
- **Purpose:** Read permitted feedback drafts/releases
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FEEDBACK_LISTRequest
- **Response:** FeedbackViewPage
- **Application operation:** FeedbackService.list_admin_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-019, ASM-008
- **Consumers:** admin

## API-ADMIN-FEEDBACK-CREATE

- **Method/route:** POST /api/v1/admin/cohorts/{cohort_id}/feedback
- **Purpose:** Create draft educational feedback
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FEEDBACK_CREATERequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.create_admin_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-019, ASM-008
- **Consumers:** admin

## API-ADMIN-FEEDBACK-UPDATE

- **Method/route:** PATCH /api/v1/admin/feedback/{feedback_id}
- **Purpose:** Revise draft feedback; released content requires withdrawal first
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FEEDBACK_UPDATERequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.update_admin_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-019, ASM-008
- **Consumers:** admin

## API-ADMIN-FEEDBACK-RELEASE

- **Method/route:** POST /api/v1/admin/feedback/{feedback_id}/release
- **Purpose:** Release educational feedback and notify
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FEEDBACK_RELEASERequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.release_admin_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-019, ASM-008
- **Consumers:** admin

## API-ADMIN-FEEDBACK-WITHDRAW

- **Method/route:** POST /api/v1/admin/feedback/{feedback_id}/withdrawal
- **Purpose:** Withdraw mistaken feedback release with reason
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FEEDBACK_WITHDRAWRequest
- **Response:** FeedbackView
- **Application operation:** FeedbackService.withdraw_admin_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-019, ASM-008
- **Consumers:** admin

## API-ADMIN-PROGRESS

- **Method/route:** GET /api/v1/admin/cohorts/{cohort_id}/progress
- **Purpose:** Read permitted learner completion evidence
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PROGRESSRequest
- **Response:** ProgressViewPage
- **Application operation:** ProgressService.list_admin_progress
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-018, LRN-007, LRN-008
- **Consumers:** admin

## API-STUDENT-ASSESSMENTS

- **Method/route:** GET /api/v1/student/assessments
- **Purpose:** Read own/linked child released assessments
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only.
- **Request:** API_STUDENT_ASSESSMENTSRequest
- **Response:** AssessmentViewPage
- **Application operation:** AssessmentService.list_student_assessments
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-006, ASM-007, STU-011
- **Consumers:** student

## API-STUDENT-FEEDBACK

- **Method/route:** GET /api/v1/student/feedback
- **Purpose:** Read own/linked child released feedback
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only.
- **Request:** API_STUDENT_FEEDBACKRequest
- **Response:** FeedbackViewPage
- **Application operation:** FeedbackService.list_student_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-008, STU-012
- **Consumers:** student

## API-STUDENT-PROGRESS

- **Method/route:** GET /api/v1/student/progress
- **Purpose:** Read own/linked child released progress
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only.
- **Request:** API_STUDENT_PROGRESSRequest
- **Response:** ProgressViewPage
- **Application operation:** ProgressService.list_student_progress
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-007, LRN-008, STU-016
- **Consumers:** student

## API-STUDENT-CERTIFICATES

- **Method/route:** GET /api/v1/student/certificates
- **Purpose:** Read own/linked child released certificates
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only.
- **Request:** API_STUDENT_CERTIFICATESRequest
- **Response:** CertificateViewPage
- **Application operation:** CertificateService.list_student_certificates
- **Domain objects:** Certificate, CompletionPolicy, StudentProgress
- **Repository / ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-009, LRN-010, STU-017
- **Consumers:** student

## API-PARENT-ASSESSMENTS

- **Method/route:** GET /api/v1/parent/students/{student_id}/assessments
- **Purpose:** Read own/linked child released assessments
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only.
- **Request:** API_PARENT_ASSESSMENTSRequest
- **Response:** AssessmentViewPage
- **Application operation:** AssessmentService.list_parent_assessments
- **Domain objects:** Assessment, Submission, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-006, ASM-007, PAR-013
- **Consumers:** parent

## API-PARENT-FEEDBACK

- **Method/route:** GET /api/v1/parent/students/{student_id}/feedback
- **Purpose:** Read own/linked child released feedback
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only.
- **Request:** API_PARENT_FEEDBACKRequest
- **Response:** FeedbackViewPage
- **Application operation:** FeedbackService.list_parent_feedback
- **Domain objects:** TeacherFeedback, ReleasePolicy, TeachingAccessPolicy
- **Repository / ports:** AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ASM-008, PAR-012
- **Consumers:** parent

## API-PARENT-PROGRESS

- **Method/route:** GET /api/v1/parent/students/{student_id}/progress
- **Purpose:** Read own/linked child released progress
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only.
- **Request:** API_PARENT_PROGRESSRequest
- **Response:** ProgressViewPage
- **Application operation:** ProgressService.list_parent_progress
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-007, LRN-008, PAR-011
- **Consumers:** parent

## API-PARENT-CERTIFICATES

- **Method/route:** GET /api/v1/parent/students/{student_id}/certificates
- **Purpose:** Read own/linked child released certificates
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only.
- **Request:** API_PARENT_CERTIFICATESRequest
- **Response:** CertificateViewPage
- **Application operation:** CertificateService.list_parent_certificates
- **Domain objects:** Certificate, CompletionPolicy, StudentProgress
- **Repository / ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-009, LRN-010, PAR-014
- **Consumers:** parent

## API-STUDENT-ACTIVITY-GET

- **Method/route:** GET /api/v1/student/enrolments/{enrolment_id}/activities
- **Purpose:** Read own activity/reflection status
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ACTIVITY_GETRequest
- **Response:** ActivityCompletionViewPage
- **Application operation:** ProgressService.list_activities
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-007, LRN-008, STU-016
- **Consumers:** student

## API-STUDENT-ACTIVITY

- **Method/route:** PUT /api/v1/student/enrolments/{enrolment_id}/lessons/{lesson_id}/activities/{block_id}
- **Purpose:** Record own non-graded activity and reflection
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_ACTIVITYRequest
- **Response:** ActivityCompletionView
- **Application operation:** ProgressService.record_activity
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** LRN-007, LRN-008, STU-016
- **Consumers:** student

## API-STUDENT-LESSON-COMPLETE

- **Method/route:** PUT /api/v1/student/enrolments/{enrolment_id}/lessons/{lesson_id}/completion
- **Purpose:** Record own lesson acknowledgement
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_LESSON_COMPLETERequest
- **Response:** ActivityCompletionView
- **Application operation:** ProgressService.complete_lesson
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** LRN-007, LRN-008, STU-016
- **Consumers:** student

## API-ADMIN-COMPLETION-REVIEW

- **Method/route:** POST /api/v1/admin/enrolments/{enrolment_id}/completion-review
- **Purpose:** Record standard or evidenced exceptional course completion decision
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. education_admin may recompute standard eligibility, grant override with verified evidence and reason, or revoke prior override. Source learning records and attendance remain immutable.
- **Request:** API_ADMIN_COMPLETION_REVIEWRequest
- **Response:** ProgressView
- **Application operation:** ProgressService.review_completion
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED
- **Requirements:** ADM-018, LRN-007, LRN-008
- **Consumers:** admin

## API-ADMIN-CERTIFICATES

- **Method/route:** GET /api/v1/admin/certificates
- **Purpose:** List certificate issue/revocation state
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_CERTIFICATESRequest
- **Response:** CertificateViewPage
- **Application operation:** CertificateService.list_certificates
- **Domain objects:** Certificate, CompletionPolicy, StudentProgress
- **Repository / ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-020, LRN-009, LRN-010
- **Consumers:** admin

## API-ADMIN-CERTIFICATE-ISSUE

- **Method/route:** POST /api/v1/admin/enrolments/{enrolment_id}/certificates
- **Purpose:** Issue completion certificate once from eligible progress
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_CERTIFICATE_ISSUERequest
- **Response:** CertificateView
- **Application operation:** CertificateService.issue_certificate
- **Domain objects:** Certificate, CompletionPolicy, StudentProgress
- **Repository / ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COMPLETION_NOT_ELIGIBLE
- **Requirements:** ADM-020, LRN-009, LRN-010
- **Consumers:** admin

## API-ADMIN-CERTIFICATE-REVOKE

- **Method/route:** POST /api/v1/admin/certificates/{certificate_id}/revocation
- **Purpose:** Revoke incorrect certificate with reason
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_CERTIFICATE_REVOKERequest
- **Response:** CertificateView
- **Application operation:** CertificateService.revoke_certificate
- **Domain objects:** Certificate, CompletionPolicy, StudentProgress
- **Repository / ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-020, LRN-009, LRN-010
- **Consumers:** admin

## API-ADMIN-CERTIFICATE-REISSUE

- **Method/route:** POST /api/v1/admin/certificates/{certificate_id}/reissue
- **Purpose:** Issue replacement linked to revoked certificate
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_CERTIFICATE_REISSUERequest
- **Response:** CertificateView
- **Application operation:** CertificateService.reissue_certificate
- **Domain objects:** Certificate, CompletionPolicy, StudentProgress
- **Repository / ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-020, LRN-009, LRN-010
- **Consumers:** admin

## API-PARENT-CHECKOUT

- **Method/route:** POST /api/v1/parent/students/{student_id}/checkout
- **Purpose:** Reserve seat and create server-priced hosted checkout
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. Verified email; age reconfirmed within180d; current required consents.
- **Request:** API_PARENT_CHECKOUTRequest
- **Response:** CheckoutSessionView
- **Application operation:** BillingService.create_checkout
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, AGE_RECONFIRMATION_REQUIRED, AGE_INELIGIBLE, ALREADY_ENROLLED, LAUNCH_CONFIGURATION_REQUIRED, PROVIDER_UNAVAILABLE
- **Requirements:** PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** parent

## API-PARENT-CHECKOUT-RETRY

- **Method/route:** POST /api/v1/parent/payments/{payment_id}/checkout
- **Purpose:** Retry failed/expired checkout with fresh eligibility and seat check
- **Roles:** parent
- **Ownership / assignment / state:** Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout.
- **Request:** API_PARENT_CHECKOUT_RETRYRequest
- **Response:** CheckoutSessionView
- **Application operation:** BillingService.retry_checkout
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, PROVIDER_UNAVAILABLE
- **Requirements:** PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** parent

## API-PARENT-PAYMENTS

- **Method/route:** GET /api/v1/parent/payments
- **Purpose:** Read own family payment history
- **Roles:** parent
- **Ownership / assignment / state:** Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout.
- **Request:** API_PARENT_PAYMENTSRequest
- **Response:** PaymentViewPage
- **Application operation:** BillingService.list_family_payments
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** parent

## API-PARENT-PAYMENT

- **Method/route:** GET /api/v1/parent/payments/{payment_id}
- **Purpose:** Read authoritative payment/checkout state
- **Roles:** parent
- **Ownership / assignment / state:** Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout.
- **Request:** API_PARENT_PAYMENTRequest
- **Response:** PaymentView
- **Application operation:** BillingService.get_family_payment
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** parent

## API-PARENT-RECEIPTS

- **Method/route:** GET /api/v1/parent/payments/{payment_id}/documents
- **Purpose:** Read own immutable invoice/receipt documents
- **Roles:** parent
- **Ownership / assignment / state:** Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout.
- **Request:** API_PARENT_RECEIPTSRequest
- **Response:** ReceiptViewPage
- **Application operation:** BillingService.list_family_documents
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** parent

## API-PARENT-REFUNDS

- **Method/route:** GET /api/v1/parent/payments/{payment_id}/refunds
- **Purpose:** Read own refund outcome
- **Roles:** parent
- **Ownership / assignment / state:** Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout.
- **Request:** API_PARENT_REFUNDSRequest
- **Response:** RefundViewPage
- **Application operation:** RefundService.list_family_refunds
- **Domain objects:** Refund, Payment, Enrolment, Money
- **Repository / ports:** PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAY-008
- **Consumers:** parent

## API-ADMIN-PRICES

- **Method/route:** GET /api/v1/admin/prices
- **Purpose:** List current and historic fees
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PRICESRequest
- **Response:** PriceConfigViewPage
- **Application operation:** BillingService.list_prices
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-024, PAY-001
- **Consumers:** admin

## API-ADMIN-PRICE-CREATE

- **Method/route:** POST /api/v1/admin/prices
- **Purpose:** Create effective dated course default/cohort override fee
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PRICE_CREATERequest
- **Response:** PriceConfigView
- **Application operation:** BillingService.create_price
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, OVERLAPPING_PRICE_WINDOW
- **Requirements:** ADM-024, PAY-001
- **Consumers:** admin

## API-ADMIN-PRICE-RETIRE

- **Method/route:** POST /api/v1/admin/prices/{price_id}/retirement
- **Purpose:** End future pricing without changing purchase snapshots
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PRICE_RETIRERequest
- **Response:** PriceConfigView
- **Application operation:** BillingService.retire_price
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-024, PAY-001
- **Consumers:** admin

## API-ADMIN-PAYMENTS

- **Method/route:** GET /api/v1/admin/payments
- **Purpose:** Inspect financial transactions and exceptions
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PAYMENTSRequest
- **Response:** AdminPaymentViewPage
- **Application operation:** BillingService.list_payments
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** admin

## API-ADMIN-PAYMENT

- **Method/route:** GET /api/v1/admin/payments/{payment_id}
- **Purpose:** Read payment reconciliation references
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PAYMENTRequest
- **Response:** AdminPaymentView
- **Application operation:** BillingService.get_payment
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** admin

## API-ADMIN-PAYMENT-RECONCILE

- **Method/route:** POST /api/v1/admin/payments/{payment_id}/reconciliation
- **Purpose:** Queue server-to-server reconciliation
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PAYMENT_RECONCILERequest
- **Response:** Accepted
- **Application operation:** BillingService.request_reconciliation
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 202
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** admin

## API-ADMIN-DOCUMENTS

- **Method/route:** GET /api/v1/admin/payments/{payment_id}/documents
- **Purpose:** Inspect immutable invoices/receipts
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_DOCUMENTSRequest
- **Response:** ReceiptViewPage
- **Application operation:** BillingService.list_documents
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** admin

## API-ADMIN-REFUNDS

- **Method/route:** GET /api/v1/admin/payments/{payment_id}/refunds
- **Purpose:** Inspect refund ledger
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REFUNDSRequest
- **Response:** RefundViewPage
- **Application operation:** RefundService.list_refunds
- **Domain objects:** Refund, Payment, Enrolment, Money
- **Repository / ports:** PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-026, PAY-008
- **Consumers:** admin

## API-ADMIN-REFUND-CREATE

- **Method/route:** POST /api/v1/admin/payments/{payment_id}/refunds
- **Purpose:** Request full/partial refund with explicit entitlement disposition
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REFUND_CREATERequest
- **Response:** RefundView
- **Application operation:** RefundService.create_refund
- **Domain objects:** Refund, Payment, Enrolment, Money
- **Repository / ports:** PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, REFUND_EXCEEDS_BALANCE
- **Requirements:** ADM-026, PAY-008
- **Consumers:** admin

## API-ADMIN-REFUND-RETRY

- **Method/route:** POST /api/v1/admin/refunds/{refund_id}/retry
- **Purpose:** Retry confirmed failed refund under same provider idempotency key
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REFUND_RETRYRequest
- **Response:** RefundView
- **Application operation:** RefundService.retry_refund
- **Domain objects:** Refund, Payment, Enrolment, Money
- **Repository / ports:** PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PROVIDER_OUTCOME_UNKNOWN
- **Requirements:** ADM-026, PAY-008
- **Consumers:** admin

## API-ADMIN-REPORT

- **Method/route:** GET /api/v1/admin/reports/finance
- **Purpose:** Read bounded AUD gross/refund/net report
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REPORTRequest
- **Response:** FinanceReportView
- **Application operation:** ReportingService.get_finance_report
- **Domain objects:** Payment, Refund, Receipt, FinancialExport
- **Repository / ports:** PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-027, PAY-010
- **Consumers:** admin

## API-ADMIN-REPORT-EXPORT

- **Method/route:** POST /api/v1/admin/reports/finance/exports
- **Purpose:** Generate bounded finance CSV export
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_REPORT_EXPORTRequest
- **Response:** ExportView
- **Application operation:** ReportingService.create_finance_export
- **Domain objects:** Payment, Refund, Receipt, FinancialExport
- **Repository / ports:** PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-027, PAY-010
- **Consumers:** admin

## API-ADMIN-PAGES

- **Method/route:** GET /api/v1/admin/pages
- **Purpose:** Read public page drafts
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PAGESRequest
- **Response:** PublicPageViewPage
- **Application operation:** PublicContentService.list_page_drafts
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-PAGE-UPDATE

- **Method/route:** PUT /api/v1/admin/pages/{slug}
- **Purpose:** Save allowlisted public-page draft
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PAGE_UPDATERequest
- **Response:** PublicPageView
- **Application operation:** PublicContentService.save_page
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-PAGE-PUBLISH

- **Method/route:** POST /api/v1/admin/pages/{slug}/publication
- **Purpose:** Publish reviewed public page
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PAGE_PUBLISHRequest
- **Response:** PublicPageView
- **Application operation:** PublicContentService.publish_page
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-007, LRN-001
- **Consumers:** admin

## API-ADMIN-POLICIES

- **Method/route:** GET /api/v1/admin/policies
- **Purpose:** Read draft and published legal policies
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_POLICIESRequest
- **Response:** PolicyViewPage
- **Application operation:** ConsentService.list_policy_drafts
- **Domain objects:** PolicyDocument, PolicyAcknowledgement
- **Repository / ports:** ContentRepository, FamilyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** SEC-003
- **Consumers:** admin

## API-ADMIN-POLICY-CREATE

- **Method/route:** POST /api/v1/admin/policies
- **Purpose:** Create immutable policy-version draft
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_POLICY_CREATERequest
- **Response:** PolicyView
- **Application operation:** ConsentService.create_policy
- **Domain objects:** PolicyDocument, PolicyAcknowledgement
- **Repository / ports:** ContentRepository, FamilyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** SEC-003
- **Consumers:** admin

## API-ADMIN-POLICY-PUBLISH

- **Method/route:** POST /api/v1/admin/policies/{policy_id}/publication
- **Purpose:** Publish policy with human/legal approval evidence
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_POLICY_PUBLISHRequest
- **Response:** PolicyView
- **Application operation:** ConsentService.publish_policy
- **Domain objects:** PolicyDocument, PolicyAcknowledgement
- **Repository / ports:** ContentRepository, FamilyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED
- **Requirements:** SEC-003
- **Consumers:** admin

## API-ADMIN-EVENT-LIST

- **Method/route:** GET /api/v1/admin/events
- **Purpose:** List event drafts and releases
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_EVENT_LISTRequest
- **Response:** EventViewPage
- **Application operation:** CommunicationService.list_events
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-EVENT-CREATE

- **Method/route:** POST /api/v1/admin/events
- **Purpose:** Create audience-scoped event
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_EVENT_CREATERequest
- **Response:** EventView
- **Application operation:** CommunicationService.create_event
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-EVENT-UPDATE

- **Method/route:** PUT /api/v1/admin/events/{event_id}
- **Purpose:** Revise draft event
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_EVENT_UPDATERequest
- **Response:** EventView
- **Application operation:** CommunicationService.update_event
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-EVENT-PUBLISH

- **Method/route:** POST /api/v1/admin/events/{event_id}/publication
- **Purpose:** Publish event and resolve recipients
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_EVENT_PUBLISHRequest
- **Response:** EventView
- **Application operation:** CommunicationService.publish_event
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-EVENT-WITHDRAW

- **Method/route:** POST /api/v1/admin/events/{event_id}/withdrawal
- **Purpose:** Cancel or withdraw event and notify affected audience
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_EVENT_WITHDRAWRequest
- **Response:** EventView
- **Application operation:** CommunicationService.withdraw_event
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-PARENT-EVENTS

- **Method/route:** GET /api/v1/parent/events
- **Purpose:** Read relevant published events
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read.
- **Request:** API_PARENT_EVENTSRequest
- **Response:** EventViewPage
- **Application operation:** CommunicationService.list_parent_events
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, PAR-003, PAR-015
- **Consumers:** parent

## API-STUDENT-EVENTS

- **Method/route:** GET /api/v1/student/events
- **Purpose:** Read relevant published events
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read.
- **Request:** API_STUDENT_EVENTSRequest
- **Response:** EventViewPage
- **Application operation:** CommunicationService.list_student_events
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, STU-018
- **Consumers:** student

## API-TEACHER-EVENTS

- **Method/route:** GET /api/v1/teacher/events
- **Purpose:** Read relevant published events
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read.
- **Request:** API_TEACHER_EVENTSRequest
- **Response:** EventViewPage
- **Application operation:** CommunicationService.list_teacher_events
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** teacher

## API-ADMIN-ANNOUNCEMENT-LIST

- **Method/route:** GET /api/v1/admin/announcements
- **Purpose:** List announcement drafts and releases
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ANNOUNCEMENT_LISTRequest
- **Response:** AnnouncementViewPage
- **Application operation:** CommunicationService.list_announcements
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-ANNOUNCEMENT-CREATE

- **Method/route:** POST /api/v1/admin/announcements
- **Purpose:** Create audience-scoped announcement
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ANNOUNCEMENT_CREATERequest
- **Response:** AnnouncementView
- **Application operation:** CommunicationService.create_announcement
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-ANNOUNCEMENT-UPDATE

- **Method/route:** PUT /api/v1/admin/announcements/{announcement_id}
- **Purpose:** Revise draft announcement
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ANNOUNCEMENT_UPDATERequest
- **Response:** AnnouncementView
- **Application operation:** CommunicationService.update_announcement
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-ANNOUNCEMENT-PUBLISH

- **Method/route:** POST /api/v1/admin/announcements/{announcement_id}/publication
- **Purpose:** Publish announcement and resolve recipients
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ANNOUNCEMENT_PUBLISHRequest
- **Response:** AnnouncementView
- **Application operation:** CommunicationService.publish_announcement
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-ADMIN-ANNOUNCEMENT-WITHDRAW

- **Method/route:** POST /api/v1/admin/announcements/{announcement_id}/withdrawal
- **Purpose:** Cancel or withdraw announcement and notify affected audience
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ANNOUNCEMENT_WITHDRAWRequest
- **Response:** AnnouncementView
- **Application operation:** CommunicationService.withdraw_announcement
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** admin

## API-PARENT-ANNOUNCEMENTS

- **Method/route:** GET /api/v1/parent/announcements
- **Purpose:** Read relevant published announcements
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read.
- **Request:** API_PARENT_ANNOUNCEMENTSRequest
- **Response:** AnnouncementViewPage
- **Application operation:** CommunicationService.list_parent_announcements
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, PAR-003, PAR-015
- **Consumers:** parent

## API-STUDENT-ANNOUNCEMENTS

- **Method/route:** GET /api/v1/student/announcements
- **Purpose:** Read relevant published announcements
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read.
- **Request:** API_STUDENT_ANNOUNCEMENTSRequest
- **Response:** AnnouncementViewPage
- **Application operation:** CommunicationService.list_student_announcements
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, STU-018
- **Consumers:** student

## API-TEACHER-ANNOUNCEMENTS

- **Method/route:** GET /api/v1/teacher/announcements
- **Purpose:** Read relevant published announcements
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read.
- **Request:** API_TEACHER_ANNOUNCEMENTSRequest
- **Response:** AnnouncementViewPage
- **Application operation:** CommunicationService.list_teacher_announcements
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** teacher

## API-PUBLIC-EVENTS

- **Method/route:** GET /api/v1/public/events
- **Purpose:** Read explicitly public upcoming events
- **Roles:** public
- **Ownership / assignment / state:** Only explicitly published projection; no private child, roster, billing or operational data.
- **Request:** API_PUBLIC_EVENTSRequest
- **Response:** EventViewPage
- **Application operation:** CommunicationService.list_public_events
- **Domain objects:** Event, Announcement, AudiencePolicy
- **Repository / ports:** CommunicationRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** public

## API-NOTIFICATIONS

- **Method/route:** GET /api/v1/notifications
- **Purpose:** Read own recipient-scoped inbox
- **Roles:** parent, student, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_NOTIFICATIONSRequest
- **Response:** NotificationViewPage
- **Application operation:** NotificationService.list_notifications
- **Domain objects:** Notification, NotificationDelivery, OutboxEvent
- **Repository / ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-022, COM-007, PAR-016, TCH-015
- **Consumers:** parent, student, teacher, admin

## API-NOTIFICATION-READ

- **Method/route:** PUT /api/v1/notifications/{notification_id}/read
- **Purpose:** Mark own notification read
- **Roles:** parent, student, teacher, admin
- **Ownership / assignment / state:** Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role.
- **Request:** API_NOTIFICATION_READRequest
- **Response:** NotificationView
- **Application operation:** NotificationService.mark_read
- **Domain objects:** Notification, NotificationDelivery, OutboxEvent
- **Repository / ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-022, COM-007, PAR-016, TCH-015
- **Consumers:** parent, student, teacher, admin

## API-ADMIN-DELIVERIES

- **Method/route:** GET /api/v1/admin/notification-deliveries
- **Purpose:** Inspect redacted delivery errors
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_DELIVERIESRequest
- **Response:** DeliveryViewPage
- **Application operation:** NotificationService.list_deliveries
- **Domain objects:** Notification, NotificationDelivery, OutboxEvent
- **Repository / ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-022, COM-007
- **Consumers:** admin

## API-ADMIN-DELIVERY-RETRY

- **Method/route:** POST /api/v1/admin/notification-deliveries/{delivery_id}/retry
- **Purpose:** Retry failed authorized delivery with deduplication
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_DELIVERY_RETRYRequest
- **Response:** Accepted
- **Application operation:** NotificationService.retry_delivery
- **Domain objects:** Notification, NotificationDelivery, OutboxEvent
- **Repository / ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Success status:** 202
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-022, COM-007
- **Consumers:** admin

## API-PARENT-DASHBOARD

- **Method/route:** GET /api/v1/parent/dashboard
- **Purpose:** Read purpose-filtered dashboard counts and next actions
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child.
- **Request:** API_PARENT_DASHBOARDRequest
- **Response:** DashboardView
- **Application operation:** FamilyService.get_parent_dashboard
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAR-006
- **Consumers:** parent

## API-STUDENT-DASHBOARD

- **Method/route:** GET /api/v1/student/dashboard
- **Purpose:** Read purpose-filtered dashboard counts and next actions
- **Roles:** student
- **Ownership / assignment / state:** Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances.
- **Request:** API_STUDENT_DASHBOARDRequest
- **Response:** DashboardView
- **Application operation:** ProgressService.get_student_dashboard
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** LRN-007, LRN-008, STU-016
- **Consumers:** student

## API-TEACHER-DASHBOARD

- **Method/route:** GET /api/v1/teacher/dashboard
- **Purpose:** Read purpose-filtered dashboard counts and next actions
- **Roles:** teacher
- **Ownership / assignment / state:** Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance.
- **Request:** API_TEACHER_DASHBOARDRequest
- **Response:** DashboardView
- **Application operation:** TeacherService.get_teacher_dashboard
- **Domain objects:** TeacherProfile, TeacherAssignment, TeachingAccessPolicy
- **Repository / ports:** UserRepository, DeliveryRepository, UnitOfWork
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CLS-005
- **Consumers:** teacher

## API-ADMIN-DASHBOARD

- **Method/route:** GET /api/v1/admin/dashboard
- **Purpose:** Read purpose-filtered dashboard counts and next actions
- **Roles:** admin:education_admin, admin:finance_admin, admin:identity_admin, admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_DASHBOARDRequest
- **Response:** DashboardView
- **Application operation:** OperationsService.get_admin_dashboard
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-FILE-UPLOAD

- **Method/route:** POST /api/v1/files/uploads
- **Purpose:** Reserve validated private upload ticket
- **Roles:** student, admin:education_admin, admin:operations_admin
- **Ownership / assignment / state:** Student own draft submission only; admin matching purpose privilege. No parent upload feature.
- **Request:** API_FILE_UPLOADRequest
- **Response:** UploadTicketView
- **Application operation:** FileService.create_upload
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, FILE_TYPE_DENIED, FILE_TOO_LARGE
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** student, admin

## API-FILE-CONFIRM

- **Method/route:** POST /api/v1/files/{asset_id}/upload-confirmation
- **Purpose:** Confirm upload and queue independent scanning
- **Roles:** student, admin:education_admin, admin:operations_admin
- **Ownership / assignment / state:** Upload owner and same original scope; uploaded object metadata/checksum must match ticket.
- **Request:** API_FILE_CONFIRMRequest
- **Response:** FileAssetView
- **Application operation:** FileService.confirm_upload
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, UPLOAD_MISMATCH
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** student, admin

## API-FILE-GET

- **Method/route:** GET /api/v1/files/{asset_id}
- **Purpose:** Read authorized file scan/metadata state
- **Roles:** parent, student, teacher, admin:education_admin, admin:operations_admin
- **Ownership / assignment / state:** FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required.
- **Request:** API_FILE_GETRequest
- **Response:** FileAssetView
- **Application operation:** FileService.get_asset
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** parent, student, teacher, admin

## API-FILE-DOWNLOAD

- **Method/route:** POST /api/v1/files/{asset_id}/download
- **Purpose:** Issue ready-file short-lived download
- **Roles:** parent, student, teacher, admin:education_admin, admin:operations_admin
- **Ownership / assignment / state:** FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required.
- **Request:** API_FILE_DOWNLOADRequest
- **Response:** DownloadTicketView
- **Application operation:** FileService.create_download
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSET_NOT_READY
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** parent, student, teacher, admin

## API-FILE-DELETE

- **Method/route:** DELETE /api/v1/files/{asset_id}
- **Purpose:** Delete eligible unreferenced owned draft asset
- **Roles:** student, admin:education_admin, admin:operations_admin
- **Ownership / assignment / state:** No referenced submitted work/published resource/certificate deletion; retention and legal hold apply. Reject financial_document/financial_export purposes on this generic endpoint even for a parent; financial-specific BillingService/ReportingService grants are required.
- **Request:** API_FILE_DELETERequest
- **Response:** Empty
- **Application operation:** FileService.delete_asset
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE, LEGAL_HOLD
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** student, admin

## API-ADMIN-FILES

- **Method/route:** GET /api/v1/admin/files
- **Purpose:** Browse assets by permitted educational/operations purpose
- **Roles:** admin:education_admin, admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FILESRequest
- **Response:** FileAssetViewPage
- **Application operation:** FileService.list_assets
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** admin

## API-PARENT-CALENDAR

- **Method/route:** GET /api/v1/parent/calendar.ics
- **Purpose:** Export authorized family schedule with portal deep links
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs.
- **Request:** API_PARENT_CALENDARRequest
- **Response:** CalendarExport
- **Application operation:** CalendarService.export_family_calendar
- **Domain objects:** ClassSession, Event, IntegrationBinding
- **Repository / ports:** DeliveryRepository, CommunicationRepository, IntegrationRepository, CalendarProvider, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** CAL-001, CAL-002, CAL-003, CAL-004, CAL-005
- **Consumers:** parent

## API-ADMIN-SETTINGS

- **Method/route:** GET /api/v1/admin/settings
- **Purpose:** Read allowlisted non-secret operational settings
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SETTINGSRequest
- **Response:** SettingViewPage
- **Application operation:** OperationsService.list_settings
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-SETTING-PUT

- **Method/route:** PUT /api/v1/admin/settings/{key}
- **Purpose:** Set validated key with approval evidence for launch-sensitive values
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_SETTING_PUTRequest
- **Response:** SettingView
- **Application operation:** OperationsService.set_setting
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-FINANCE-SETTINGS

- **Method/route:** GET /api/v1/admin/billing-settings
- **Purpose:** Read merchant identity/tax configuration
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FINANCE_SETTINGSRequest
- **Response:** SettingViewPage
- **Application operation:** BillingService.list_billing_settings
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** admin

## API-ADMIN-FINANCE-SETTING-PUT

- **Method/route:** PUT /api/v1/admin/billing-settings/{key}
- **Purpose:** Set approved merchant/tax/refund policy value
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_FINANCE_SETTING_PUTRequest
- **Response:** SettingView
- **Application operation:** BillingService.set_billing_setting
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED
- **Requirements:** ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** admin

## API-ADMIN-INTEGRATIONS

- **Method/route:** GET /api/v1/admin/integrations
- **Purpose:** Read masked provider configuration and synchronization health
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_INTEGRATIONSRequest
- **Response:** IntegrationStatusViewPage
- **Application operation:** OperationsService.list_integrations
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-INTEGRATION-UPDATE

- **Method/route:** PUT /api/v1/admin/integrations/{provider}
- **Purpose:** Enable/disable provider using managed secret reference
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe credential/configuration additionally requires finance privilege.
- **Request:** API_ADMIN_INTEGRATION_UPDATERequest
- **Response:** IntegrationStatusView
- **Application operation:** OperationsService.configure_integration
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-INTEGRATION-CHECK

- **Method/route:** POST /api/v1/admin/integrations/{provider}/check
- **Purpose:** Queue bounded provider connectivity check
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_INTEGRATION_CHECKRequest
- **Response:** Accepted
- **Application operation:** OperationsService.check_integration
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 202
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-INTEGRATION-RESYNC

- **Method/route:** POST /api/v1/admin/integrations/{provider}/resync
- **Purpose:** Queue provider mirror reconciliation
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe resync requires finance privilege.
- **Request:** API_ADMIN_INTEGRATION_RESYNCRequest
- **Response:** Accepted
- **Application operation:** OperationsService.request_provider_resync
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 202
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-JOBS

- **Method/route:** GET /api/v1/admin/jobs
- **Purpose:** Read redacted job processing state
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_JOBSRequest
- **Response:** JobViewPage
- **Application operation:** OperationsService.list_jobs
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-JOB

- **Method/route:** GET /api/v1/admin/jobs/{job_id}
- **Purpose:** Read authorized background operation status
- **Roles:** admin:operations_admin, admin:finance_admin, admin:education_admin
- **Ownership / assignment / state:** Match job capability and initiating admin purpose; arbitrary job IDs denied.
- **Request:** API_ADMIN_JOBRequest
- **Response:** JobView
- **Application operation:** OperationsService.get_job
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-JOB-RETRY

- **Method/route:** POST /api/v1/admin/jobs/{job_id}/retry
- **Purpose:** Retry dead-letter job after cause correction
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Finance jobs additionally require finance privilege; immutable original payload.
- **Request:** API_ADMIN_JOB_RETRYRequest
- **Response:** Accepted
- **Application operation:** OperationsService.retry_job
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 202
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-OPERATIONS

- **Method/route:** GET /api/v1/admin/operations
- **Purpose:** Read actionable operational summary
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_OPERATIONSRequest
- **Response:** OperationsSummaryView
- **Application operation:** OperationsService.get_operations_summary
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-028, OPS-003, OPS-005, OPS-008
- **Consumers:** admin

## API-ADMIN-AUDIT

- **Method/route:** GET /api/v1/admin/audit
- **Purpose:** Read filtered redacted audit history
- **Roles:** admin:audit_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_AUDITRequest
- **Response:** AuditViewPage
- **Application operation:** AuditService.list_audit
- **Domain objects:** AuditRecord
- **Repository / ports:** AuditRepository, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** ADM-029, SEC-007
- **Consumers:** admin

## API-PARENT-PRIVACY-REQUEST

- **Method/route:** POST /api/v1/parent/privacy-requests
- **Purpose:** Request family data access/correction/deletion or account closure
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link.
- **Request:** API_PARENT_PRIVACY_REQUESTRequest
- **Response:** PrivacyRequestView
- **Application operation:** PrivacyService.create_privacy_request
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** parent

## API-PARENT-PRIVACY-LIST

- **Method/route:** GET /api/v1/parent/privacy-requests
- **Purpose:** Read own privacy request state
- **Roles:** parent
- **Ownership / assignment / state:** Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link.
- **Request:** API_PARENT_PRIVACY_LISTRequest
- **Response:** PrivacyRequestViewPage
- **Application operation:** PrivacyService.list_own_requests
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** parent

## API-ADMIN-PRIVACY-LIST

- **Method/route:** GET /api/v1/admin/privacy-requests
- **Purpose:** Read restricted privacy work queue
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_PRIVACY_LISTRequest
- **Response:** PrivacyRequestViewPage
- **Application operation:** PrivacyService.list_privacy_requests
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** admin

## API-ADMIN-PRIVACY-DECIDE

- **Method/route:** POST /api/v1/admin/privacy-requests/{request_id}/decision
- **Purpose:** Record verified authority and retention-aware decision
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Never orphan active children or erase required finance records.
- **Request:** API_ADMIN_PRIVACY_DECIDERequest
- **Response:** PrivacyRequestView
- **Application operation:** PrivacyService.decide_request
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, LEGAL_HOLD, ACTIVE_GUARDIAN_REQUIRED
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** admin

## API-PARENT-PRIVACY-EXPORT

- **Method/route:** POST /api/v1/parent/privacy-requests/{request_id}/download
- **Purpose:** Get ready verified family export
- **Roles:** parent
- **Ownership / assignment / state:** Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Approved access request only; exclude unrelated guardian finances.
- **Request:** API_PARENT_PRIVACY_EXPORTRequest
- **Response:** DownloadTicketView
- **Application operation:** PrivacyService.download_export
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** parent

## API-ADMIN-LEGAL-HOLD

- **Method/route:** PUT /api/v1/admin/privacy/holds/{resource_id}
- **Purpose:** Set or release audited retention hold
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_LEGAL_HOLDRequest
- **Response:** Empty
- **Application operation:** PrivacyService.set_legal_hold
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** admin

## API-STRIPE-WEBHOOK

- **Method/route:** POST /api/v1/webhooks/stripe
- **Purpose:** Validate raw signature and persist deduplicated provider event
- **Roles:** system
- **Ownership / assignment / state:** Stripe signature on original bytes; signed does not imply relevant event; dedupe provider+event ID before any financial mutation.
- **Request:** API_STRIPE_WEBHOOKRequest
- **Response:** Empty
- **Application operation:** BillingService.receive_stripe_webhook
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-004, PAY-005
- **Consumers:** stripe

## JOB-PAYMENT-PROCESS

- **Method/route:** WORKER worker:process_payment_event
- **Purpose:** Retrieve authoritative provider state and activate paid seat safely
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_PAYMENT_PROCESSRequest
- **Response:** JobView
- **Application operation:** BillingService.process_payment_event
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-004, PAY-005
- **Consumers:** worker

## JOB-PAYMENT-RECONCILE

- **Method/route:** WORKER worker:reconcile_payment
- **Purpose:** Compare Stripe state with immutable local ledger
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_PAYMENT_RECONCILERequest
- **Response:** JobView
- **Application operation:** BillingService.reconcile_payment
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** worker

## JOB-HOLD-EXPIRE

- **Method/route:** WORKER worker:expire_holds
- **Purpose:** Expire elapsed holds under row lock; release capacity
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_HOLD_EXPIRERequest
- **Response:** JobView
- **Application operation:** EnrolmentService.expire_holds
- **Domain objects:** Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy
- **Repository / ports:** EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007
- **Consumers:** worker

## JOB-REFUND-PROCESS

- **Method/route:** WORKER worker:process_refund
- **Purpose:** Execute idempotent requested refund and apply explicit access disposition
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_REFUND_PROCESSRequest
- **Response:** JobView
- **Application operation:** RefundService.process_refund
- **Domain objects:** Refund, Payment, Enrolment, Money
- **Repository / ports:** PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-008
- **Consumers:** worker

## JOB-DOCUMENT-GENERATE

- **Method/route:** WORKER worker:generate_purchase_documents
- **Purpose:** Generate immutable receipt/invoice after verified payment
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_DOCUMENT_GENERATERequest
- **Response:** JobView
- **Application operation:** BillingService.generate_purchase_documents
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** worker

## JOB-LIVE-CREATE

- **Method/route:** WORKER worker:provision_meeting
- **Purpose:** Create provider meeting from authoritative session version
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_LIVE_CREATERequest
- **Response:** JobView
- **Application operation:** LiveClassService.provision_meeting
- **Domain objects:** ClassSession, IntegrationBinding, TeachingAccessPolicy
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009
- **Consumers:** worker

## JOB-LIVE-UPDATE

- **Method/route:** WORKER worker:synchronize_meeting
- **Purpose:** Update/cancel meeting from latest authoritative session state
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_LIVE_UPDATERequest
- **Response:** JobView
- **Application operation:** LiveClassService.synchronize_meeting
- **Domain objects:** ClassSession, IntegrationBinding, TeachingAccessPolicy
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009
- **Consumers:** worker

## JOB-LIVE-RECONCILE

- **Method/route:** WORKER worker:reconcile_meetings
- **Purpose:** Resolve provider drift without overwriting domain schedule
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_LIVE_RECONCILERequest
- **Response:** JobView
- **Application operation:** LiveClassService.reconcile_meetings
- **Domain objects:** ClassSession, IntegrationBinding, TeachingAccessPolicy
- **Repository / ports:** DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** CLS-006, CLS-007, CLS-008, CLS-009
- **Consumers:** worker

## JOB-CALENDAR-SYNC

- **Method/route:** WORKER worker:synchronize_event
- **Purpose:** Upsert/cancel individual business calendar mirror event
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_CALENDAR_SYNCRequest
- **Response:** JobView
- **Application operation:** CalendarService.synchronize_event
- **Domain objects:** ClassSession, Event, IntegrationBinding
- **Repository / ports:** DeliveryRepository, CommunicationRepository, IntegrationRepository, CalendarProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** CAL-001, CAL-002, CAL-003, CAL-004, CAL-005
- **Consumers:** worker

## JOB-CALENDAR-RESYNC

- **Method/route:** WORKER worker:reconcile_calendar
- **Purpose:** Recover invalid sync token with full mirror reconciliation
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_CALENDAR_RESYNCRequest
- **Response:** JobView
- **Application operation:** CalendarService.reconcile_calendar
- **Domain objects:** ClassSession, Event, IntegrationBinding
- **Repository / ports:** DeliveryRepository, CommunicationRepository, IntegrationRepository, CalendarProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** CAL-001, CAL-002, CAL-003, CAL-004, CAL-005
- **Consumers:** worker

## JOB-NOTIFICATION-PREPARE

- **Method/route:** WORKER worker:prepare_notifications
- **Purpose:** Resolve outbox recipients and create deduplicated notices
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_NOTIFICATION_PREPARERequest
- **Response:** JobView
- **Application operation:** NotificationService.prepare_notifications
- **Domain objects:** Notification, NotificationDelivery, OutboxEvent
- **Repository / ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** worker

## JOB-EMAIL-SEND

- **Method/route:** WORKER worker:deliver_email
- **Purpose:** Deliver transactional email with durable local deduplication
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_EMAIL_SENDRequest
- **Response:** JobView
- **Application operation:** NotificationService.deliver_email
- **Domain objects:** Notification, NotificationDelivery, OutboxEvent
- **Repository / ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** worker

## JOB-REMINDER-SCHEDULE

- **Method/route:** WORKER worker:schedule_reminders
- **Purpose:** Queue class reminders once per current session version
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_REMINDER_SCHEDULERequest
- **Response:** JobView
- **Application operation:** NotificationService.schedule_reminders
- **Domain objects:** Notification, NotificationDelivery, OutboxEvent
- **Repository / ports:** NotificationRepository, EmailProvider, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009
- **Consumers:** worker

## JOB-FILE-SCAN

- **Method/route:** WORKER worker:scan_and_promote
- **Purpose:** Verify metadata/MIME/archive limits/malware and promote immutable object
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_FILE_SCANRequest
- **Response:** JobView
- **Application operation:** FileService.scan_and_promote
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** worker

## JOB-FILE-CLEAN

- **Method/route:** WORKER worker:clean_orphaned_uploads
- **Purpose:** Delete expired unreferenced staging objects after retention/hold checks
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_FILE_CLEANRequest
- **Response:** JobView
- **Application operation:** FileService.clean_orphaned_uploads
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** worker

## JOB-FILE-DELETE

- **Method/route:** WORKER worker:purge_asset
- **Purpose:** Delete eligible private object/version per approved retention decision
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_FILE_DELETERequest
- **Response:** JobView
- **Application operation:** FileService.purge_asset
- **Domain objects:** FileAsset, FileAccessPolicy
- **Repository / ports:** FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007
- **Consumers:** worker

## JOB-PROGRESS-RECOMPUTE

- **Method/route:** WORKER worker:recompute_progress
- **Purpose:** Recalculate completion from latest released work and attendance evidence
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_PROGRESS_RECOMPUTERequest
- **Response:** ProgressView
- **Application operation:** ProgressService.recompute_progress
- **Domain objects:** StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride
- **Repository / ports:** ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** LRN-007, LRN-008
- **Consumers:** worker

## JOB-CERTIFICATE-RENDER

- **Method/route:** WORKER worker:render_certificate
- **Purpose:** Render immutable certificate artifact and mark issued after ready storage
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_CERTIFICATE_RENDERRequest
- **Response:** CertificateView
- **Application operation:** CertificateService.render_certificate
- **Domain objects:** Certificate, CompletionPolicy, StudentProgress
- **Repository / ports:** CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** LRN-009, LRN-010
- **Consumers:** worker

## JOB-PRIVACY-PROCESS

- **Method/route:** WORKER worker:process_request
- **Purpose:** Generate protected export or execute approved retention-aware deletion/closure
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_PRIVACY_PROCESSRequest
- **Response:** JobView
- **Application operation:** PrivacyService.process_request
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** worker

## JOB-RETENTION

- **Method/route:** WORKER worker:apply_retention
- **Purpose:** Purge/anonymize only eligible unheld records from approved matrix
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_RETENTIONRequest
- **Response:** JobView
- **Application operation:** PrivacyService.apply_retention
- **Domain objects:** PrivacyRequest, GuardianStudent, FileAsset
- **Repository / ports:** FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** SEC-001, SEC-002, SEC-008, SEC-009, SEC-010
- **Consumers:** worker

## JOB-OUTBOX-DISPATCH

- **Method/route:** WORKER worker:dispatch_outbox
- **Purpose:** Publish durable intent to queue and recover expired leases
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_OUTBOX_DISPATCHRequest
- **Response:** JobView
- **Application operation:** OperationsService.dispatch_outbox
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** OPS-005
- **Consumers:** worker

## JOB-INTEGRATION-CHECK

- **Method/route:** WORKER worker:probe_integration
- **Purpose:** Check configured provider and persist masked operational state
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_INTEGRATION_CHECKRequest
- **Response:** IntegrationStatusView
- **Application operation:** OperationsService.probe_integration
- **Domain objects:** ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent
- **Repository / ports:** SettingsRepository, IntegrationRepository, UnitOfWork, Clock
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** OPS-003
- **Consumers:** worker

## JOB-FINANCE-EXPORT

- **Method/route:** WORKER worker:generate_finance_export
- **Purpose:** Write formula-injection-safe CSV to private export storage
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_FINANCE_EXPORTRequest
- **Response:** ExportView
- **Application operation:** ReportingService.generate_finance_export
- **Domain objects:** Payment, Refund, Receipt, FinancialExport
- **Repository / ports:** PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. After bounded retries exhaust, atomically set failed and sanitized failure_code. Explicit authorized job retry sets processing and clears failure; never return a download for failed state.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-010
- **Consumers:** worker

## API-ADMIN-ASSIGNMENT-CLOSE

- **Method/route:** PUT /api/v1/admin/cohorts/{cohort_id}/assignments/{assignment_id}/closure
- **Purpose:** Close/reopen assignment submissions for a delivery
- **Roles:** admin:education_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ASSIGNMENT_CLOSERequest
- **Response:** AssignmentView
- **Application operation:** AssignmentService.set_delivery_closure
- **Domain objects:** Assignment, CurriculumRevision, ReleasePolicy
- **Repository / ports:** AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** ADM-011, ASM-004
- **Consumers:** admin

## API-ADMIN-BILLING-MEMBER

- **Method/route:** POST /api/v1/admin/families/{family_id}/billing-members
- **Purpose:** Grant verified adult family billing visibility separately from child links
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate finance approval reference required; no teacher principal.
- **Request:** API_ADMIN_BILLING_MEMBERRequest
- **Response:** FamilyView
- **Application operation:** FamilyService.create_billing_membership
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-006
- **Consumers:** admin

## API-ADMIN-BILLING-MEMBER-REVOKE

- **Method/route:** DELETE /api/v1/admin/families/{family_id}/billing-members/{guardian_id}
- **Purpose:** Revoke adult family financial membership
- **Roles:** admin:identity_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_BILLING_MEMBER_REVOKERequest
- **Response:** Empty
- **Application operation:** FamilyService.revoke_billing_membership
- **Domain objects:** Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership
- **Repository / ports:** FamilyRepository, StudentRepository, UnitOfWork, Clock
- **Success status:** 204
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAR-006
- **Consumers:** admin

## API-ADMIN-ENQUIRIES

- **Method/route:** GET /api/v1/admin/contact-enquiries
- **Purpose:** Read inbound enquiries to support customers
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ENQUIRIESRequest
- **Response:** ContactEnquiryViewPage
- **Application operation:** PublicContentService.list_contact_enquiries
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** WEB-009
- **Consumers:** admin

## API-ADMIN-ENQUIRY-STATUS

- **Method/route:** PUT /api/v1/admin/contact-enquiries/{enquiry_id}/status
- **Purpose:** Mark enquiry handled without sending unauthorized messages
- **Roles:** admin:operations_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_ENQUIRY_STATUSRequest
- **Response:** ContactEnquiryView
- **Application operation:** PublicContentService.set_enquiry_status
- **Domain objects:** PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry, Cohort, Price
- **Repository / ports:** ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork, DeliveryRepository, PaymentRepository
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** WEB-009
- **Consumers:** admin

## API-ADMIN-PAID-EXCEPTION

- **Method/route:** POST /api/v1/admin/payments/{payment_id}/exception-resolution
- **Purpose:** Resolve late paid no-seat exception exactly once by allocation or refund
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Lock Payment+Enrolment+Cohort; ALLOCATE requires available seat and no pending refund; REFUND reserves refundable balance and prevents activation.
- **Request:** API_ADMIN_PAID_EXCEPTIONRequest
- **Response:** AdminPaymentView
- **Application operation:** BillingService.resolve_paid_exception
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, REFUND_PENDING, EXCEPTION_ALREADY_RESOLVED
- **Requirements:** ADM-025, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012
- **Consumers:** admin

## JOB-PAYMENT-DISCOVERY

- **Method/route:** WORKER worker:discover_provider_transactions
- **Purpose:** Discover provider-side payments/refunds and reconcile missing local references
- **Roles:** system
- **Ownership / assignment / state:** Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege.
- **Request:** JOB_PAYMENT_DISCOVERYRequest
- **Response:** JobView
- **Application operation:** BillingService.discover_provider_transactions
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** None
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-009, PAY-005, ADM-025
- **Consumers:** worker

## API-ADMIN-REPORT-EXPORT-STATUS

- **Method/route:** GET /api/v1/admin/reports/finance/exports/{export_id}
- **Purpose:** Read own authorized financial report export status
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Authenticated finance_admin with active account and recent MFA, requesting the export or explicitly authorized finance oversight; status read permits every defined ExportView state and never requires a ready asset. Deny parent, student, teacher and non-finance admin.
- **Request:** API_ADMIN_REPORT_EXPORT_STATUSRequest
- **Response:** ExportView
- **Application operation:** ReportingService.get_finance_export
- **Domain objects:** Payment, Refund, Receipt, FinancialExport
- **Repository / ports:** PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAY-010, ADM-027
- **Consumers:** admin

## API-ADMIN-REPORT-EXPORT-DOWNLOAD

- **Method/route:** POST /api/v1/admin/reports/finance/exports/{export_id}/download
- **Purpose:** Download ready private financial report export under finance scope
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Ready generated financial_export; initiated by this principal or explicitly privileged finance oversight; no generic teaching file grant.
- **Request:** API_ADMIN_REPORT_EXPORT_DOWNLOADRequest
- **Response:** DownloadTicketView
- **Application operation:** ReportingService.download_finance_export
- **Domain objects:** Payment, Refund, Receipt, FinancialExport
- **Repository / ports:** PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider
- **Success status:** 200
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, EXPORT_NOT_READY, EXPORT_EXPIRED
- **Requirements:** PAY-010, ADM-027
- **Consumers:** admin

## API-ADMIN-RECONCILIATION-EXCEPTIONS

- **Method/route:** GET /api/v1/admin/reconciliation-exceptions
- **Purpose:** Inspect provider transactions unmatched to local financial records
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection.
- **Request:** API_ADMIN_RECONCILIATION_EXCEPTIONSRequest
- **Response:** ReconciliationExceptionViewPage
- **Application operation:** BillingService.list_reconciliation_exceptions
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 200
- **Transaction:** Read-only scoped projection
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR
- **Requirements:** PAY-009, ADM-025, ENR-007
- **Consumers:** admin

## API-ADMIN-RECONCILIATION-EXCEPTION-RETRY

- **Method/route:** POST /api/v1/admin/reconciliation-exceptions/{exception_id}/reconciliation
- **Purpose:** Recheck provider truth and resolve only verified matching or reversed transaction
- **Roles:** admin:finance_admin
- **Ownership / assignment / state:** Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No manual invented payment ownership; unresolved cases remain open for documented operational repair.
- **Request:** API_ADMIN_RECONCILIATION_EXCEPTION_RETRYRequest
- **Response:** Accepted
- **Application operation:** BillingService.retry_reconciliation_exception
- **Domain objects:** Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt, ReconciliationException
- **Repository / ports:** PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider, DocumentRenderer
- **Success status:** 202
- **Transaction:** Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks.
- **Implementation chunk:** Pending final chunk binding
- **Errors:** UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE
- **Requirements:** PAY-009, ADM-025
- **Consumers:** admin
