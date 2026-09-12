# Versioned API and worker catalog

Status: DRAFT. Architecture version1.0. This is a complete proposed launch blueprint for human review. No application code is implemented. Canonical machine-readable details: [backend-catalog.json](backend-catalog.json). Requirement authority: [requirements.json](../product/requirements.json). Implementing chunk IDs are assigned by the consolidated Code Blueprint and requirement-to-chunk traceability; no catalog entry may be implemented without that assignment.

307 explicit operations, of which 23 are internal worker entrypoints. The remaining operations are REST/provider ingress contracts. Every schema below declares fields, type, required/optional presence, nullability, validation and request location. All unlisted JSON fields are rejected. Null and omission are different: omission in PATCH means unchanged; explicit null clears a nullable field. A property marked required and nullable must be present with value or null. Path/header fields never repeat in JSON body. `PageMeta` contains an opaque cursor; no unbounded list response is allowed.

## Error contract

| Code | HTTP status | Meaning |
| --- | --- | --- |
| ACCOUNT_SUSPENDED | 403 | Account suspended. Return safe actionable message; never infer unrelated resource existence. |
| ACTIVE_ASSIGNMENT_EXISTS | 409 | Active assignment exists. Return safe actionable message; never infer unrelated resource existence. |
| ACTIVE_ENROLMENT_EXISTS | 409 | Active enrolment exists. Return safe actionable message; never infer unrelated resource existence. |
| ACTIVE_GUARDIAN_REQUIRED | 409 | Active guardian required. Return safe actionable message; never infer unrelated resource existence. |
| AGE_INELIGIBLE | 409 | Age ineligible. Return safe actionable message; never infer unrelated resource existence. |
| AGE_RECONFIRMATION_REQUIRED | 409 | Age reconfirmation required. Return safe actionable message; never infer unrelated resource existence. |
| ALREADY_ENROLLED | 409 | Already enrolled. Return safe actionable message; never infer unrelated resource existence. |
| ASSET_NOT_READY | 409 | Asset not ready. Return safe actionable message; never infer unrelated resource existence. |
| ASSIGNMENT_CLOSED | 409 | Assignment closed. Return safe actionable message; never infer unrelated resource existence. |
| ATTEMPT_ALREADY_SUBMITTED | 409 | Attempt already submitted. Return safe actionable message; never infer unrelated resource existence. |
| ATTEMPT_LIMIT_REACHED | 409 | Attempt limit reached. Return safe actionable message; never infer unrelated resource existence. |
| CAPACITY_BELOW_COMMITMENTS | 409 | Capacity below commitments. Return safe actionable message; never infer unrelated resource existence. |
| COHORT_FULL | 409 | Cohort full. Return safe actionable message; never infer unrelated resource existence. |
| COMPLETION_NOT_ELIGIBLE | 409 | Completion not eligible. Return safe actionable message; never infer unrelated resource existence. |
| CONTENT_UNRELEASED | 409 | Content unreleased. Return safe actionable message; never infer unrelated resource existence. |
| DST_AMBIGUOUS | 409 | Dst ambiguous. Return safe actionable message; never infer unrelated resource existence. |
| EVIDENCE_REQUIRED | 409 | Evidence required. Return safe actionable message; never infer unrelated resource existence. |
| EXCEPTION_ALREADY_RESOLVED | 409 | Exception already resolved. Return safe actionable message; never infer unrelated resource existence. |
| FILE_TOO_LARGE | 409 | File too large. Return safe actionable message; never infer unrelated resource existence. |
| FILE_TYPE_DENIED | 409 | File type denied. Return safe actionable message; never infer unrelated resource existence. |
| FORBIDDEN | 403 | Forbidden. Return safe actionable message; never infer unrelated resource existence. |
| HUMAN_APPROVAL_REQUIRED | 409 | Human approval required. Return safe actionable message; never infer unrelated resource existence. |
| INCOMPATIBLE_ROLE | 409 | Incompatible role. Return safe actionable message; never infer unrelated resource existence. |
| INVALID_CREDENTIALS | 401 | Invalid credentials. Return safe actionable message; never infer unrelated resource existence. |
| INVALID_STATE | 409 | Invalid state. Return safe actionable message; never infer unrelated resource existence. |
| JOIN_WINDOW_CLOSED | 409 | Join window closed. Return safe actionable message; never infer unrelated resource existence. |
| LAST_ADMIN | 409 | Last admin. Return safe actionable message; never infer unrelated resource existence. |
| LAUNCH_CONFIGURATION_REQUIRED | 409 | Launch configuration required. Return safe actionable message; never infer unrelated resource existence. |
| LEGAL_HOLD | 409 | Legal hold. Return safe actionable message; never infer unrelated resource existence. |
| MFA_ATTEMPTS_EXCEEDED | 409 | Mfa attempts exceeded. Return safe actionable message; never infer unrelated resource existence. |
| MFA_CHALLENGE_EXPIRED | 409 | Mfa challenge expired. Return safe actionable message; never infer unrelated resource existence. |
| MFA_REPLAY | 409 | Mfa replay. Return safe actionable message; never infer unrelated resource existence. |
| NOT_FOUND | 404 | Not found. Return safe actionable message; never infer unrelated resource existence. |
| OVERLAPPING_PRICE_WINDOW | 409 | Overlapping price window. Return safe actionable message; never infer unrelated resource existence. |
| POLICY_VERSION_STALE | 409 | Policy version stale. Return safe actionable message; never infer unrelated resource existence. |
| PROVIDER_OUTCOME_UNKNOWN | 409 | Provider outcome unknown. Return safe actionable message; never infer unrelated resource existence. |
| PROVIDER_UNAVAILABLE | 503 | Provider unavailable. Return safe actionable message; never infer unrelated resource existence. |
| PUBLISH_VALIDATION_FAILED | 409 | Publish validation failed. Return safe actionable message; never infer unrelated resource existence. |
| RATE_LIMITED | 429 | Rate limited. Return safe actionable message; never infer unrelated resource existence. |
| REFUND_EXCEEDS_BALANCE | 409 | Refund exceeds balance. Return safe actionable message; never infer unrelated resource existence. |
| REFUND_PENDING | 409 | Refund pending. Return safe actionable message; never infer unrelated resource existence. |
| RESCHEDULE_WINDOW_CLOSED | 409 | Reschedule window closed. Return safe actionable message; never infer unrelated resource existence. |
| RESOURCE_IN_USE | 409 | Resource in use. Return safe actionable message; never infer unrelated resource existence. |
| SCHEDULE_CONFLICT | 409 | Schedule conflict. Return safe actionable message; never infer unrelated resource existence. |
| UNAUTHENTICATED | 401 | Unauthenticated. Return safe actionable message; never infer unrelated resource existence. |
| UPLOAD_MISMATCH | 409 | Upload mismatch. Return safe actionable message; never infer unrelated resource existence. |
| VALIDATION_ERROR | 422 | Validation error. Return safe actionable message; never infer unrelated resource existence. |
| VERSION_CONFLICT | 409 | Version conflict. Return safe actionable message; never infer unrelated resource existence. |

## Operations

### API-AUTH-REGISTER — Register guardian and create family

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/parents |
| Roles | public |
| Ownership / assignment / state | Email uniqueness; accepted current required policy versions; rate-limit by address/network. |
| Request | API_AUTH_REGISTERRequest |
| Response / success | AccountView / 200 |
| Application operation | AuthenticationService.register_parent |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-AUTH-VERIFY — Consume single-use email verification

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/email-verifications |
| Roles | public |
| Ownership / assignment / state | Hashed token bound to account and purpose; 24h expiry. |
| Request | API_AUTH_VERIFYRequest |
| Response / success | Empty / 204 |
| Application operation | AuthenticationService.verify_email |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-AUTH-RESEND — Resend verification without account enumeration

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/email-verifications/resend |
| Roles | public |
| Ownership / assignment / state | Uniform response and throttled per identifier. |
| Request | API_AUTH_RESENDRequest |
| Response / success | Empty / 204 |
| Application operation | AuthenticationService.resend_verification |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-AUTH-LOGIN — Authenticate parent/staff/student

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/sessions |
| Roles | public |
| Ownership / assignment / state | Credential and account status; staff MFA challenge before privileged session. |
| Request | API_AUTH_LOGINRequest |
| Response / success | AuthOutcomeView / 200 |
| Application operation | AuthenticationService.login |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE, INVALID_CREDENTIALS, ACCOUNT_SUSPENDED |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-AUTH-MFA — Complete staff MFA challenge

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/mfa/verifications |
| Roles | public |
| Ownership / assignment / state | Short-lived challenge bound to browser, user and purpose. |
| Request | API_AUTH_MFARequest |
| Response / success | SessionView / 200 |
| Application operation | AuthenticationService.verify_mfa |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE, INVALID_CREDENTIALS, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-AUTH-MFA-ENROL — Create pending TOTP enrolment

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/account/mfa/enrolment |
| Roles | teacher, admin |
| Ownership / assignment / state | Full staff session with recent password reauthentication OR unexpired staff-invitation MFA setup token; setup context permits only MFA setup operations. |
| Request | API_AUTH_MFA_ENROLRequest |
| Response / success | MfaSetupView / 200 |
| Application operation | AuthenticationService.enrol_mfa |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, TCH-001 |
| Consumers | teacher, admin |

### API-AUTH-MFA-CONFIRM — Activate TOTP and issue recovery codes once

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/account/mfa/confirmation |
| Roles | teacher, admin |
| Ownership / assignment / state | Purpose-bound setup token plus valid first TOTP proof; consume setup token, activate staff account and full MFA session atomically. |
| Request | API_AUTH_MFA_CONFIRMRequest |
| Response / success | MfaActivationView / 200 |
| Application operation | AuthenticationService.confirm_mfa |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, MFA_REPLAY, MFA_CHALLENGE_EXPIRED, MFA_ATTEMPTS_EXCEEDED |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, TCH-001 |
| Consumers | teacher, admin |

### API-AUTH-RESET-REQUEST — Request account recovery

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/password-reset-requests |
| Roles | public |
| Ownership / assignment / state | Uniform response; adult verified email only; student recovery managed by guardian. |
| Request | API_AUTH_RESET_REQUESTRequest |
| Response / success | Empty / 204 |
| Application operation | AuthenticationService.request_password_reset |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-AUTH-RESET — Reset adult password and revoke sessions

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/password-resets |
| Roles | public |
| Ownership / assignment / state | One-time hashed token, 30-minute lifetime; revocation transactional. |
| Request | API_AUTH_RESETRequest |
| Response / success | Empty / 204 |
| Application operation | AuthenticationService.reset_password |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-AUTH-ME — Get safe authenticated session identity

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/account/session |
| Roles | parent, student, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_AUTH_MERequest |
| Response / success | SessionView / 200 |
| Application operation | AuthenticationService.get_session |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001 |
| Consumers | parent, student, teacher, admin |

### API-AUTH-LOGOUT — Revoke current session

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/auth/sessions/current |
| Roles | parent, student, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_AUTH_LOGOUTRequest |
| Response / success | Empty / 204 |
| Application operation | AuthenticationService.logout |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-001, AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, PAR-001, STU-001, TCH-001 |
| Consumers | parent, student, teacher, admin |

### API-ACCOUNT-PASSWORD — Change own adult/staff password and revoke other sessions

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/account/password |
| Roles | parent, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_ACCOUNT_PASSWORDRequest |
| Response / success | Empty / 204 |
| Application operation | AccountService.change_password |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021 |
| Consumers | parent, teacher, admin |

### API-ACCOUNT-SESSIONS — List own devices

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/account/sessions |
| Roles | parent, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_ACCOUNT_SESSIONSRequest |
| Response / success | DeviceSessionViewPage / 200 |
| Application operation | AccountService.list_sessions |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021 |
| Consumers | parent, teacher, admin |

### API-ACCOUNT-REVOKE — Revoke selected own device

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/account/sessions/{session_id} |
| Roles | parent, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_ACCOUNT_REVOKERequest |
| Response / success | Empty / 204 |
| Application operation | AccountService.revoke_session |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021 |
| Consumers | parent, teacher, admin |

### API-ACCOUNT-PROFILE — Read own profile

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/account |
| Roles | parent, student, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_ACCOUNT_PROFILERequest |
| Response / success | AccountView / 200 |
| Application operation | AccountService.get_account |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-003, ADM-006, AUTH-011, PAR-002, PAR-021, STU-019 |
| Consumers | parent, student, teacher, admin |

### API-FAMILY-GET — Read own family and linked students

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/family |
| Roles | parent |
| Ownership / assignment / state | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. |
| Request | API_FAMILY_GETRequest |
| Response / success | FamilyView / 200 |
| Application operation | FamilyService.get_family |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-006 |
| Consumers | parent |

### API-PARENT-PROFILE — Read guardian contact/preferences

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/profile |
| Roles | parent |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_PARENT_PROFILERequest |
| Response / success | GuardianView / 200 |
| Application operation | AccountService.get_guardian_profile |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | AUTH-011, PAR-002, PAR-021 |
| Consumers | parent |

### API-PARENT-UPDATE — Update guardian contact/preferences

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/parent/profile |
| Roles | parent |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_PARENT_UPDATERequest |
| Response / success | GuardianView / 200 |
| Application operation | AccountService.update_guardian_profile |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-011, PAR-002, PAR-021 |
| Consumers | parent |

### API-PARENT-EMAIL-CHANGE — Begin verified contact email change

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/email-change |
| Roles | parent |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. Reauthentication; new address never takes effect until verification. |
| Request | API_PARENT_EMAIL_CHANGERequest |
| Response / success | Empty / 204 |
| Application operation | AccountService.request_email_change |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-011, PAR-002, PAR-021 |
| Consumers | parent |

### API-PARENT-EMAIL-CONFIRM — Confirm new email and notify old address

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/email-change/confirmation |
| Roles | parent |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_PARENT_EMAIL_CONFIRMRequest |
| Response / success | GuardianView / 200 |
| Application operation | AccountService.confirm_email_change |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-011, PAR-002, PAR-021 |
| Consumers | parent |

### API-STUDENT-CREATE — Register child with required name and age

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/students |
| Roles | parent |
| Ownership / assignment / state | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. Create StudentProfile and verified GuardianStudent link to requesting parent atomically in same family; no pre-existing child required. |
| Request | API_STUDENT_CREATERequest |
| Response / success | StudentProfileView / 200 |
| Application operation | StudentProfileService.create_student |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-005 |
| Consumers | parent |

### API-STUDENT-GET — Read linked child profile

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id} |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_STUDENT_GETRequest |
| Response / success | StudentProfileView / 200 |
| Application operation | StudentProfileService.get_student |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-005 |
| Consumers | parent |

### API-STUDENT-UPDATE — Update optional child information

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/parent/students/{student_id} |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_STUDENT_UPDATERequest |
| Response / success | StudentProfileView / 200 |
| Application operation | StudentProfileService.update_student |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-005 |
| Consumers | parent |

### API-STUDENT-AGE — Reconfirm required age

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/parent/students/{student_id}/age |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_STUDENT_AGERequest |
| Response / success | StudentProfileView / 200 |
| Application operation | StudentProfileService.reconfirm_age |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-005 |
| Consumers | parent |

### API-STUDENT-CREDENTIALS — Provision or rotate child login

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/students/{student_id}/credentials |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Guardian password reauthentication; revoke prior student sessions. |
| Request | API_STUDENT_CREDENTIALSRequest |
| Response / success | StudentCredentialsView / 200 |
| Application operation | StudentProfileService.provision_credentials |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-005 |
| Consumers | parent |

### API-STUDENT-SELF — Read own limited profile

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/profile |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_SELFRequest |
| Response / success | TeachingStudentView / 200 |
| Application operation | StudentProfileService.get_student_self |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-004, PAR-005, TCH-009 |
| Consumers | student |

### API-STUDENT-PREFERRED — Update own preferred name and optional interests/experience

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/student/profile |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_PREFERREDRequest |
| Response / success | TeachingStudentView / 200 |
| Application operation | StudentProfileService.update_preferred_name |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-004, PAR-005, TCH-009 |
| Consumers | student |

### API-POLICY-LIST — Read published policy versions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/policies |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_POLICY_LISTRequest |
| Response / success | PolicyViewPage / 200 |
| Application operation | ConsentService.list_policies |
| Domain objects | PolicyDocument, PolicyAcknowledgement |
| Ports / repositories | ContentRepository, FamilyRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | SEC-003 |
| Consumers | public |

### API-CONSENT-LIST — Read family acknowledgement evidence

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/acknowledgements |
| Roles | parent |
| Ownership / assignment / state | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. |
| Request | API_CONSENT_LISTRequest |
| Response / success | AcknowledgementViewPage / 200 |
| Application operation | ConsentService.list_acknowledgements |
| Domain objects | PolicyDocument, PolicyAcknowledgement |
| Ports / repositories | ContentRepository, FamilyRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-004, SEC-003 |
| Consumers | parent |

### API-CONSENT-ACK — Record current policy acknowledgement

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/acknowledgements |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_CONSENT_ACKRequest |
| Response / success | AcknowledgementView / 200 |
| Application operation | ConsentService.acknowledge |
| Domain objects | PolicyDocument, PolicyAcknowledgement |
| Ports / repositories | ContentRepository, FamilyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, POLICY_VERSION_STALE |
| Requirements | PAR-004, SEC-003 |
| Consumers | parent |

### API-PUBLIC-PAGE — Read get page

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/pages/{slug} |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_PUBLIC_PAGERequest |
| Response / success | PublicPageView / 200 |
| Application operation | PublicContentService.get_page |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012 |
| Consumers | public |

### API-PUBLIC-PROGRAMS — Read list programs

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/programs |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_PUBLIC_PROGRAMSRequest |
| Response / success | PublicProgramViewPage / 200 |
| Application operation | PublicContentService.list_programs |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012 |
| Consumers | public |

### API-PUBLIC-COURSES — Read list courses

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/courses |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_PUBLIC_COURSESRequest |
| Response / success | PublicCourseViewPage / 200 |
| Application operation | PublicContentService.list_courses |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012 |
| Consumers | public |

### API-PUBLIC-COURSE — Read get course

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/courses/{slug} |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_PUBLIC_COURSERequest |
| Response / success | PublicCourseView / 200 |
| Application operation | PublicContentService.get_course |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012 |
| Consumers | public |

### API-PUBLIC-COHORTS — Read list public cohorts

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/courses/{course_id}/cohorts |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_PUBLIC_COHORTSRequest |
| Response / success | PublicCohortViewPage / 200 |
| Application operation | PublicContentService.list_public_cohorts |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012 |
| Consumers | public |

### API-PUBLIC-TEACHERS — Read list public teachers

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/instructors |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_PUBLIC_TEACHERSRequest |
| Response / success | PublicTeacherViewPage / 200 |
| Application operation | PublicContentService.list_public_teachers |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012 |
| Consumers | public |

### API-PUBLIC-CONTACT — Submit contact enquiry to operations queue

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/public/contact |
| Roles | public |
| Ownership / assignment / state | Rate limit; honeypot; no attachments, child profile matching or marketing subscription. |
| Request | API_PUBLIC_CONTACTRequest |
| Response / success | ContactReceipt / 200 |
| Application operation | PublicContentService.submit_contact |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE |
| Requirements | LRN-001, WEB-001, WEB-002, WEB-003, WEB-004, WEB-007, WEB-008, WEB-009, WEB-012 |
| Consumers | public |

### API-ADMIN-PROGRAM-LIST — List draft and published programs

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/programs |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PROGRAM_LISTRequest |
| Response / success | ProgramViewPage / 200 |
| Application operation | CourseService.list_programs |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-PROGRAM-CREATE — Create offering grouping

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/programs |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PROGRAM_CREATERequest |
| Response / success | ProgramView / 200 |
| Application operation | CourseService.create_program |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-PROGRAM-UPDATE — Edit offering grouping

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/programs/{program_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PROGRAM_UPDATERequest |
| Response / success | ProgramView / 200 |
| Application operation | CourseService.update_program |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-PROGRAM-STATUS — Publish or archive program

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/programs/{program_id}/publication |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PROGRAM_STATUSRequest |
| Response / success | ProgramView / 200 |
| Application operation | CourseService.set_program_publication |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-COURSES — List all curriculum courses

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/courses |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COURSESRequest |
| Response / success | CourseViewPage / 200 |
| Application operation | CourseService.list_courses |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-COURSE — Read administrative course details

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/courses/{course_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COURSERequest |
| Response / success | CourseView / 200 |
| Application operation | CourseService.get_course |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-COURSE-CREATE — Create reusable course

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/courses |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COURSE_CREATERequest |
| Response / success | CourseView / 200 |
| Application operation | CourseService.create_course |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-COURSE-UPDATE — Edit course marketing metadata

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/courses/{course_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COURSE_UPDATERequest |
| Response / success | CourseView / 200 |
| Application operation | CourseService.update_course |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-COURSE-PUBLISH — Publish approved course with ready revision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/courses/{course_id}/publication |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COURSE_PUBLISHRequest |
| Response / success | CourseView / 200 |
| Application operation | CourseService.publish_course |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PUBLISH_VALIDATION_FAILED, LAUNCH_CONFIGURATION_REQUIRED |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-COURSE-ARCHIVE — Archive course acquisition; preserve existing learning access

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/courses/{course_id}/archive |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COURSE_ARCHIVERequest |
| Response / success | CourseView / 200 |
| Application operation | CourseService.archive_course |
| Domain objects | Program, Course, CurriculumRevision, PublicationPolicy |
| Ports / repositories | CourseRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-REVISION-LIST — List curriculum revisions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/courses/{course_id}/revisions |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REVISION_LISTRequest |
| Response / success | CurriculumRevisionViewPage / 200 |
| Application operation | CurriculumService.list_revisions |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-REVISION-CREATE — Create draft revision optionally copied from same course

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/courses/{course_id}/revisions |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REVISION_CREATERequest |
| Response / success | CurriculumRevisionView / 200 |
| Application operation | CurriculumService.create_revision |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-REVISION-GET — Read full authoring hierarchy

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/revisions/{revision_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REVISION_GETRequest |
| Response / success | CurriculumRevisionView / 200 |
| Application operation | CurriculumService.get_revision |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-REVISION-PUBLISH — Freeze validated curriculum revision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/revisions/{revision_id}/publication |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REVISION_PUBLISHRequest |
| Response / success | CurriculumRevisionView / 200 |
| Application operation | CurriculumService.publish_revision |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PUBLISH_VALIDATION_FAILED, ASSET_NOT_READY |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-MODULE-CREATE — Create draft module

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/revisions/{revision_id}/modules |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_MODULE_CREATERequest |
| Response / success | ModuleView / 200 |
| Application operation | CurriculumService.create_module |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-MODULE-UPDATE — Edit draft module

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/modules/{module_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_MODULE_UPDATERequest |
| Response / success | ModuleView / 200 |
| Application operation | CurriculumService.update_module |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-MODULE-DELETE — Remove unreferenced draft module

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/modules/{module_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| Request | API_ADMIN_MODULE_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | CurriculumService.delete_module |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-LESSON-CREATE — Create draft lesson

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/modules/{module_id}/lessons |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_LESSON_CREATERequest |
| Response / success | LessonView / 200 |
| Application operation | CurriculumService.create_lesson |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-LESSON-UPDATE — Edit draft lesson

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/lessons/{lesson_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_LESSON_UPDATERequest |
| Response / success | LessonView / 200 |
| Application operation | CurriculumService.update_lesson |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-LESSON-DELETE — Remove unreferenced draft lesson

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/lessons/{lesson_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| Request | API_ADMIN_LESSON_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | CurriculumService.delete_lesson |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-BLOCK-CREATE — Create draft block

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/lessons/{lesson_id}/blocks |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_BLOCK_CREATERequest |
| Response / success | LessonBlockView / 200 |
| Application operation | CurriculumService.create_block |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-BLOCK-UPDATE — Edit draft block

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/blocks/{block_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_BLOCK_UPDATERequest |
| Response / success | LessonBlockView / 200 |
| Application operation | CurriculumService.update_block |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-BLOCK-DELETE — Remove unreferenced draft block

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/blocks/{block_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| Request | API_ADMIN_BLOCK_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | CurriculumService.delete_block |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-RESOURCE-CREATE — Create draft resource

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/revisions/{revision_id}/resources |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_RESOURCE_CREATERequest |
| Response / success | ResourceView / 200 |
| Application operation | CurriculumService.create_resource |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-RESOURCE-UPDATE — Edit draft resource

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/resources/{resource_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Mutable draft revision only. |
| Request | API_ADMIN_RESOURCE_UPDATERequest |
| Response / success | ResourceView / 200 |
| Application operation | CurriculumService.update_resource |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-RESOURCE-DELETE — Remove unreferenced draft resource

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/resources/{resource_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. No published revision or active external references. |
| Request | API_ADMIN_RESOURCE_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | CurriculumService.delete_resource |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-RESOURCE-LIST — List teaching assets in revision

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/revisions/{revision_id}/resources |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_RESOURCE_LISTRequest |
| Response / success | ResourceViewPage / 200 |
| Application operation | CurriculumService.list_resources |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-ADMIN-LESSON-GET — Read authoring lesson and all block fields

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/lessons/{lesson_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_LESSON_GETRequest |
| Response / success | LessonView / 200 |
| Application operation | CurriculumService.get_authoring_lesson |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-008, LRN-002, LRN-003, LRN-004 |
| Consumers | admin |

### API-STUDENT-ENROLMENTS — List own enrolled courses

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/enrolments |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ENROLMENTSRequest |
| Response / success | EnrolmentViewPage / 200 |
| Application operation | EnrolmentService.list_student_enrolments |
| Domain objects | Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007 |
| Consumers | student |

### API-PARENT-ENROLMENTS — List linked child enrolment status

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/enrolments |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_ENROLMENTSRequest |
| Response / success | EnrolmentViewPage / 200 |
| Application operation | EnrolmentService.list_child_enrolments |
| Domain objects | Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008 |
| Consumers | parent |

### API-STUDENT-CURRICULUM — Read released modules of pinned revision

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/enrolments/{enrolment_id}/curriculum |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_CURRICULUMRequest |
| Response / success | CurriculumRevisionView / 200 |
| Application operation | CurriculumService.get_learning_curriculum |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-002, LRN-003, LRN-004, STU-003, STU-004 |
| Consumers | student |

### API-STUDENT-LESSON — Read released lesson and safe blocks

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/enrolments/{enrolment_id}/lessons/{lesson_id} |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_LESSONRequest |
| Response / success | LessonView / 200 |
| Application operation | CurriculumService.get_learning_lesson |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, CONTENT_UNRELEASED |
| Requirements | LRN-002, LRN-003, LRN-004, STU-003, STU-004 |
| Consumers | student |

### API-STUDENT-RESOURCE — List released learning resources

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/enrolments/{enrolment_id}/resources |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_RESOURCERequest |
| Response / success | ResourceViewPage / 200 |
| Application operation | CurriculumService.list_learning_resources |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-002, LRN-003, LRN-004, STU-003, STU-004 |
| Consumers | student |

### API-TEACHER-COURSES — List assigned courses

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/courses |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_COURSESRequest |
| Response / success | CourseViewPage / 200 |
| Application operation | TeacherService.list_assigned_courses |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-005 |
| Consumers | teacher |

### API-TEACHER-COHORTS — List assigned cohorts

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_COHORTSRequest |
| Response / success | CohortViewPage / 200 |
| Application operation | CohortService.list_assigned_cohorts |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-001, CLS-005 |
| Consumers | teacher |

### API-TEACHER-CURRICULUM — Read pinned teaching curriculum including planned lessons

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/curriculum |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_CURRICULUMRequest |
| Response / success | CurriculumRevisionView / 200 |
| Application operation | CurriculumService.get_teaching_curriculum |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-002, LRN-003, LRN-004, TCH-003 |
| Consumers | teacher |

### API-TEACHER-LESSON — Read assigned teaching lesson plan

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/lessons/{lesson_id} |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_LESSONRequest |
| Response / success | LessonView / 200 |
| Application operation | CurriculumService.get_teaching_lesson |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-002, LRN-003, LRN-004, TCH-003 |
| Consumers | teacher |

### API-TEACHER-RESOURCES — Read assigned teaching resources

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/resources |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_RESOURCESRequest |
| Response / success | ResourceViewPage / 200 |
| Application operation | CurriculumService.list_teaching_resources |
| Domain objects | CurriculumRevision, CourseModule, Lesson, LessonBlock, LearningResource, PublicationPolicy |
| Ports / repositories | CourseRepository, FileRepository, AssessmentRepository, UnitOfWork, Clock, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-002, LRN-003, LRN-004, TCH-003 |
| Consumers | teacher |

### API-TEACHER-STUDENTS — Read assigned roster educational fields

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/students |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_STUDENTSRequest |
| Response / success | TeachingStudentViewPage / 200 |
| Application operation | TeacherService.list_assigned_students |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-005 |
| Consumers | teacher |

### API-TEACHER-STUDENT — Read assigned learner educational profile

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/students/{student_id} |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_STUDENTRequest |
| Response / success | TeachingStudentView / 200 |
| Application operation | TeacherService.get_teaching_student |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-005 |
| Consumers | teacher |

### API-ADMIN-PARENTS — Read authorized list parents

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/parents |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PARENTSRequest |
| Response / success | GuardianViewPage / 200 |
| Application operation | FamilyService.list_parents_admin |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-006 |
| Consumers | admin |

### API-ADMIN-FAMILY — Read authorized get family

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/families/{family_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FAMILYRequest |
| Response / success | FamilyView / 200 |
| Application operation | FamilyService.get_family_admin |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-006 |
| Consumers | admin |

### API-ADMIN-STUDENTS — Read authorized list students

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/students |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_STUDENTSRequest |
| Response / success | StudentProfileViewPage / 200 |
| Application operation | StudentProfileService.list_students_admin |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-004 |
| Consumers | admin |

### API-ADMIN-STUDENT — Read authorized get student

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/students/{student_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_STUDENTRequest |
| Response / success | StudentProfileView / 200 |
| Application operation | StudentProfileService.get_student_admin |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-004 |
| Consumers | admin |

### API-ADMIN-TEACHERS — Read authorized list teachers

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/teachers |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_TEACHERSRequest |
| Response / success | TeacherViewPage / 200 |
| Application operation | TeacherService.list_teachers_admin |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-005, ADM-015, CLS-005 |
| Consumers | admin |

### API-ADMIN-TEACHER — Read authorized get teacher

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/teachers/{teacher_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_TEACHERRequest |
| Response / success | TeacherView / 200 |
| Application operation | TeacherService.get_teacher_admin |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-005, ADM-015, CLS-005 |
| Consumers | admin |

### API-ADMIN-GUARDIAN-LINK — Link verified guardian to same family child

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/students/{student_id}/guardians |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Verification evidence reference mandatory; no cross-family transfer implicit. |
| Request | API_ADMIN_GUARDIAN_LINKRequest |
| Response / success | FamilyView / 200 |
| Application operation | FamilyService.create_guardian_link |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-006 |
| Consumers | admin |

### API-ADMIN-GUARDIAN-REVOKE — Revoke guardian child access

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/students/{student_id}/guardians/{guardian_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. At least one verified active guardian remains or safeguarding override is documented. |
| Request | API_ADMIN_GUARDIAN_REVOKERequest |
| Response / success | FamilyView / 200 |
| Application operation | FamilyService.revoke_guardian_link |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-006 |
| Consumers | admin |

### API-ADMIN-STUDENT-UPDATE — Correct student data with reason

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/students/{student_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_STUDENT_UPDATERequest |
| Response / success | StudentProfileView / 200 |
| Application operation | StudentProfileService.correct_student |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-004 |
| Consumers | admin |

### API-ADMIN-STUDENT-ARCHIVE — Archive child after active obligations resolved

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/students/{student_id}/archive |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_STUDENT_ARCHIVERequest |
| Response / success | StudentProfileView / 200 |
| Application operation | StudentProfileService.archive_student |
| Domain objects | StudentProfile, GuardianStudent, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | StudentRepository, FamilyRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ACTIVE_ENROLMENT_EXISTS |
| Requirements | ADM-004 |
| Consumers | admin |

### API-ADMIN-INVITE — Invite teacher or constrained admin principal

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/staff-invitations |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate admin principal required for teacher-to-admin duties. |
| Request | API_ADMIN_INVITERequest |
| Response / success | AccountView / 200 |
| Application operation | AccountService.create_staff_invitation |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, INCOMPATIBLE_ROLE |
| Requirements | ADM-003, ADM-006, AUTH-011 |
| Consumers | admin |

### API-AUTH-INVITE-ACCEPT — Accept staff invitation and require MFA setup

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/auth/staff-invitations/accept |
| Roles | public |
| Ownership / assignment / state | Single-use invitation token; no privilege upgrades from request. |
| Request | API_AUTH_INVITE_ACCEPTRequest |
| Response / success | StaffSetupSessionView / 200 |
| Application operation | AuthenticationService.accept_staff_invitation |
| Domain objects | Account, Session, Credential, RoleGrant, MfaFactor, RecoveryCode, MfaChallenge |
| Ports / repositories | UserRepository, SessionRepository, PasswordHasher, TokenIssuer, UnitOfWork, Clock, FamilyRepository, NotificationRepository, MfaRepository, MfaVerifier |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED, VERSION_CONFLICT, INVALID_STATE |
| Requirements | AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, WEB-011 |
| Consumers | public |

### API-ADMIN-ROLE — Read constrained role grants

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/accounts/{account_id}/roles |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ROLERequest |
| Response / success | RoleGrantView / 200 |
| Application operation | AccountService.get_role_grants |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-003, ADM-006, AUTH-011 |
| Consumers | admin |

### API-ADMIN-ROLE-UPDATE — Change admin privileges with audit and session revocation

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/accounts/{account_id}/roles |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Cannot self-escalate; no last identity-admin removal; teacher/admin principal incompatibility. |
| Request | API_ADMIN_ROLE_UPDATERequest |
| Response / success | RoleGrantView / 200 |
| Application operation | AccountService.set_role_grants |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, INCOMPATIBLE_ROLE, LAST_ADMIN |
| Requirements | ADM-003, ADM-006, AUTH-011 |
| Consumers | admin |

### API-ADMIN-ACCOUNT-STATUS — Suspend or reactivate account and revoke affected sessions

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/accounts/{account_id}/status |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ACCOUNT_STATUSRequest |
| Response / success | AccountView / 200 |
| Application operation | AccountService.set_account_status |
| Domain objects | Account, Guardian, TeacherProfile, RoleGrant |
| Ports / repositories | UserRepository, FamilyRepository, SessionRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-003, ADM-006, AUTH-011 |
| Consumers | admin |

### API-ADMIN-TEACHER-UPDATE — Edit teacher public biography/profile

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/teachers/{teacher_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_TEACHER_UPDATERequest |
| Response / success | TeacherView / 200 |
| Application operation | TeacherService.update_teacher |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-005, ADM-015, CLS-005 |
| Consumers | admin |

### API-ADMIN-TEACHER-PUBLISH — Publish or withdraw explicitly approved instructor profile

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/teachers/{teacher_id}/publication |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_TEACHER_PUBLISHRequest |
| Response / success | TeacherView / 200 |
| Application operation | TeacherService.publish_teacher |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-005, ADM-015, CLS-005 |
| Consumers | admin |

### API-ADMIN-TEACHER-ARCHIVE — Archive teacher after assignment reassignment

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/teachers/{teacher_id}/archive |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_TEACHER_ARCHIVERequest |
| Response / success | TeacherView / 200 |
| Application operation | TeacherService.archive_teacher |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ACTIVE_ASSIGNMENT_EXISTS |
| Requirements | ADM-005, ADM-015, CLS-005 |
| Consumers | admin |

### API-TEACHER-PROFILE — Read own teacher profile

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/profile |
| Roles | teacher |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_TEACHER_PROFILERequest |
| Response / success | TeacherView / 200 |
| Application operation | TeacherService.get_own_teacher_profile |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-005 |
| Consumers | teacher |

### API-ADMIN-COHORTS — List operational cohorts

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COHORTSRequest |
| Response / success | CohortViewPage / 200 |
| Application operation | CohortService.list_cohorts |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-COHORT — Read cohort operational details

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts/{cohort_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COHORTRequest |
| Response / success | CohortView / 200 |
| Application operation | CohortService.get_cohort |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-COHORT-CREATE — Create course delivery pinned to published revision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/cohorts |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COHORT_CREATERequest |
| Response / success | CohortView / 200 |
| Application operation | CohortService.create_cohort |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-COHORT-UPDATE — Edit future cohort metadata and safe capacity

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/cohorts/{cohort_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COHORT_UPDATERequest |
| Response / success | CohortView / 200 |
| Application operation | CohortService.update_cohort |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, CAPACITY_BELOW_COMMITMENTS |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-COHORT-STATUS — Open, close, start or complete delivery

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/cohorts/{cohort_id}/status |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_COHORT_STATUSRequest |
| Response / success | CohortView / 200 |
| Application operation | CohortService.transition_cohort |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, LAUNCH_CONFIGURATION_REQUIRED |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-COHORT-CANCEL — Cancel delivery and create refund review tasks

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/cohorts/{cohort_id}/cancellation |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Education can cancel delivery but cannot execute refund. |
| Request | API_ADMIN_COHORT_CANCELRequest |
| Response / success | Accepted / 202 |
| Application operation | CohortService.cancel_cohort |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-ASSIGNMENTS — List cohort teaching grants

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts/{cohort_id}/teacher-assignments |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSIGNMENTSRequest |
| Response / success | TeacherAssignmentViewPage / 200 |
| Application operation | CohortService.list_teacher_assignments |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-ASSIGNMENT-CREATE — Assign active teacher to cohort/session

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/cohorts/{cohort_id}/teacher-assignments |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSIGNMENT_CREATERequest |
| Response / success | TeacherAssignmentView / 200 |
| Application operation | CohortService.create_teacher_assignment |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-ASSIGNMENT-REVOKE — Revoke teaching access immediately

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/teacher-assignments/{assignment_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSIGNMENT_REVOKERequest |
| Response / success | Empty / 204 |
| Application operation | CohortService.revoke_teacher_assignment |
| Domain objects | Cohort, TeacherAssignment, CurriculumRevision |
| Ports / repositories | DeliveryRepository, CourseRepository, UserRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-013, ADM-015, CLS-001, CLS-005 |
| Consumers | admin |

### API-ADMIN-SESSIONS — List all delivery sessions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts/{cohort_id}/sessions |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SESSIONSRequest |
| Response / success | ClassSessionViewPage / 200 |
| Application operation | SchedulingService.list_cohort_sessions |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011 |
| Consumers | admin |

### API-ADMIN-SESSION-CREATE — Schedule one class occurrence

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/cohorts/{cohort_id}/sessions |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SESSION_CREATERequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.create_class_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, DST_AMBIGUOUS |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011 |
| Consumers | admin |

### API-ADMIN-RECURRENCE — Materialize bounded weekly occurrences transactionally

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/cohorts/{cohort_id}/session-series |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_RECURRENCERequest |
| Response / success | ClassSessionViewPage / 200 |
| Application operation | SchedulingService.create_session_series |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, DST_AMBIGUOUS |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011 |
| Consumers | admin |

### API-ADMIN-SESSION-UPDATE — Edit session title/lesson without rescheduling

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/sessions/{session_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SESSION_UPDATERequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.update_class_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011 |
| Consumers | admin |

### API-PARENT-SCHEDULE — List parent authorized upcoming classes

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/schedule |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_SCHEDULERequest |
| Response / success | ClassSessionViewPage / 200 |
| Application operation | SchedulingService.list_parent_schedule |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-002, CLS-003, CLS-004, CLS-011, PAR-009 |
| Consumers | parent |

### API-PARENT-SESSION — Read authorized class session details

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/sessions/{session_id} |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_SESSIONRequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.get_parent_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-002, CLS-003, CLS-004, CLS-011, PAR-009 |
| Consumers | parent |

### API-STUDENT-SCHEDULE — List student authorized upcoming classes

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/schedule |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_SCHEDULERequest |
| Response / success | ClassSessionViewPage / 200 |
| Application operation | SchedulingService.list_student_schedule |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-002, CLS-003, CLS-004, CLS-011, STU-013 |
| Consumers | student |

### API-STUDENT-SESSION — Read authorized class session details

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/sessions/{session_id} |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_SESSIONRequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.get_student_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-002, CLS-003, CLS-004, CLS-011, STU-013 |
| Consumers | student |

### API-TEACHER-SCHEDULE — List teacher authorized upcoming classes

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/schedule |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_SCHEDULERequest |
| Response / success | ClassSessionViewPage / 200 |
| Application operation | SchedulingService.list_teacher_schedule |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-002, CLS-003, CLS-004, CLS-011, TCH-005, TCH-006 |
| Consumers | teacher |

### API-TEACHER-SESSION — Read authorized class session details

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/sessions/{session_id} |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_SESSIONRequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.get_teacher_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-002, CLS-003, CLS-004, CLS-011, TCH-005, TCH-006 |
| Consumers | teacher |

### API-TEACHER-RESCHEDULE — Reschedule authorized session and queue provider updates

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/sessions/{session_id}/reschedule |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Start >= now+24h; future assigned session only; no overlap for teacher/learner. |
| Request | API_TEACHER_RESCHEDULERequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.reschedule_teacher_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, RESCHEDULE_WINDOW_CLOSED, DST_AMBIGUOUS |
| Requirements | CLS-002, CLS-003, CLS-004, CLS-011, TCH-005, TCH-006 |
| Consumers | teacher |

### API-ADMIN-RESCHEDULE — Reschedule authorized session and queue provider updates

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/sessions/{session_id}/reschedule |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Override short notice requires reason; overlaps still rejected. |
| Request | API_ADMIN_RESCHEDULERequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.reschedule_admin_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, SCHEDULE_CONFLICT, RESCHEDULE_WINDOW_CLOSED, DST_AMBIGUOUS |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011 |
| Consumers | admin |

### API-ADMIN-SESSION-CANCEL — Cancel class and queue Zoom/calendar cancellation and notices

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/sessions/{session_id}/cancellation |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SESSION_CANCELRequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.cancel_class_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011 |
| Consumers | admin |

### API-ADMIN-SESSION-COMPLETE — Complete past session after attendance review

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/sessions/{session_id}/completion |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SESSION_COMPLETERequest |
| Response / success | ClassSessionView / 200 |
| Application operation | SchedulingService.complete_class_session |
| Domain objects | ClassSession, SchedulePolicy, TeacherAssignment, Cohort |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-014, CLS-002, CLS-003, CLS-004, CLS-011 |
| Consumers | admin |

### API-TEACHER-START — Fetch fresh authorized Zoom host handoff

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/sessions/{session_id}/start |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Assigned authorized host; now within start-30m through scheduled end. |
| Request | API_TEACHER_STARTRequest |
| Response / success | JoinLinkView / 200 |
| Application operation | LiveClassService.start_assigned_class |
| Domain objects | ClassSession, IntegrationBinding, TeachingAccessPolicy |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE |
| Requirements | CLS-006, CLS-007, CLS-008, CLS-009, TCH-004 |
| Consumers | teacher |

### API-STUDENT-JOIN — Fetch eligible learner Zoom join handoff

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/student/sessions/{session_id}/join |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Active enrolment; now within start-15m through scheduled end; no host URL. |
| Request | API_STUDENT_JOINRequest |
| Response / success | JoinLinkView / 200 |
| Application operation | LiveClassService.join_student_class |
| Domain objects | ClassSession, IntegrationBinding, TeachingAccessPolicy |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE |
| Requirements | CLS-006, CLS-007, CLS-008, CLS-009, STU-014 |
| Consumers | student |

### API-PARENT-JOIN — Fetch eligible learner Zoom join handoff

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/sessions/{session_id}/join |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Active enrolment; now within start-15m through scheduled end; no host URL. |
| Request | API_PARENT_JOINRequest |
| Response / success | JoinLinkView / 200 |
| Application operation | LiveClassService.join_parent_class |
| Domain objects | ClassSession, IntegrationBinding, TeachingAccessPolicy |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, JOIN_WINDOW_CLOSED, PROVIDER_UNAVAILABLE |
| Requirements | CLS-006, CLS-007, CLS-008, CLS-009 |
| Consumers | parent |

### API-ADMIN-ENROLMENTS — List delivery enrolments without financial fields

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/enrolments |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ENROLMENTSRequest |
| Response / success | EnrolmentViewPage / 200 |
| Application operation | EnrolmentService.list_enrolments |
| Domain objects | Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007 |
| Consumers | admin |

### API-ADMIN-ENROLMENT — Read educational enrolment status

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/enrolments/{enrolment_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ENROLMENTRequest |
| Response / success | EnrolmentView / 200 |
| Application operation | EnrolmentService.get_enrolment |
| Domain objects | Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007 |
| Consumers | admin |

### API-ADMIN-ENROLMENT-CANCEL — Cancel educational access with auditable reason

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/enrolments/{enrolment_id}/cancellation |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Any money movement requires finance workflow. |
| Request | API_ADMIN_ENROLMENT_CANCELRequest |
| Response / success | EnrolmentView / 200 |
| Application operation | EnrolmentService.cancel_enrolment |
| Domain objects | Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-016, ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007 |
| Consumers | admin |

### API-PARENT-CHECKOUT-CANCEL — Release own unpaid hold

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/enrolments/{enrolment_id}/hold-cancellation |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Held/pending payment only; provider expiry reconciled. |
| Request | API_PARENT_CHECKOUT_CANCELRequest |
| Response / success | EnrolmentView / 200 |
| Application operation | EnrolmentService.cancel_hold |
| Domain objects | Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007, PAR-008 |
| Consumers | parent |

### API-TEACHER-ATTENDANCE — Read authorized session attendance roster

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/sessions/{session_id}/attendance |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_ATTENDANCERequest |
| Response / success | AttendanceViewPage / 200 |
| Application operation | AttendanceService.list_teacher_attendance |
| Domain objects | AttendanceRecord, ClassSession, TeachingAccessPolicy |
| Ports / repositories | AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-010, TCH-007, TCH-008 |
| Consumers | teacher |

### API-TEACHER-ATTENDANCE-RECORD — Record or amend attendance

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/teacher/sessions/{session_id}/students/{student_id}/attendance |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Student enrolled in this session cohort. |
| Request | API_TEACHER_ATTENDANCE_RECORDRequest |
| Response / success | AttendanceView / 200 |
| Application operation | AttendanceService.record_teacher_attendance |
| Domain objects | AttendanceRecord, ClassSession, TeachingAccessPolicy |
| Ports / repositories | AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | CLS-010, TCH-007, TCH-008 |
| Consumers | teacher |

### API-ADMIN-ATTENDANCE — Read authorized session attendance roster

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/sessions/{session_id}/attendance |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ATTENDANCERequest |
| Response / success | AttendanceViewPage / 200 |
| Application operation | AttendanceService.list_admin_attendance |
| Domain objects | AttendanceRecord, ClassSession, TeachingAccessPolicy |
| Ports / repositories | AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-017, CLS-010 |
| Consumers | admin |

### API-ADMIN-ATTENDANCE-RECORD — Record or amend attendance

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/sessions/{session_id}/students/{student_id}/attendance |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Student enrolled in this session cohort. |
| Request | API_ADMIN_ATTENDANCE_RECORDRequest |
| Response / success | AttendanceView / 200 |
| Application operation | AttendanceService.record_admin_attendance |
| Domain objects | AttendanceRecord, ClassSession, TeachingAccessPolicy |
| Ports / repositories | AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-017, CLS-010 |
| Consumers | admin |

### API-PARENT-ATTENDANCE — Read own or linked child attendance

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/attendance |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_ATTENDANCERequest |
| Response / success | AttendanceViewPage / 200 |
| Application operation | AttendanceService.list_parent_attendance |
| Domain objects | AttendanceRecord, ClassSession, TeachingAccessPolicy |
| Ports / repositories | AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-010, PAR-010 |
| Consumers | parent |

### API-STUDENT-ATTENDANCE — Read own or linked child attendance

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/attendance |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ATTENDANCERequest |
| Response / success | AttendanceViewPage / 200 |
| Application operation | AttendanceService.list_student_attendance |
| Domain objects | AttendanceRecord, ClassSession, TeachingAccessPolicy |
| Ports / repositories | AttendanceRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-010, STU-015 |
| Consumers | student |

### API-ADMIN-QUIZZES — List quiz authoring definitions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/revisions/{revision_id}/quizzes |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_QUIZZESRequest |
| Response / success | QuizViewPage / 200 |
| Application operation | QuizService.list_quizzes |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003 |
| Consumers | admin |

### API-ADMIN-QUIZ — Read quiz questions and grading keys

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/quizzes/{quiz_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_QUIZRequest |
| Response / success | QuizView / 200 |
| Application operation | QuizService.get_quiz |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003 |
| Consumers | admin |

### API-ADMIN-QUIZ-CREATE — Create draft formative quiz

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/lessons/{lesson_id}/quizzes |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| Request | API_ADMIN_QUIZ_CREATERequest |
| Response / success | QuizView / 200 |
| Application operation | QuizService.create_quiz |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003 |
| Consumers | admin |

### API-ADMIN-QUIZ-UPDATE — Edit draft quiz rules

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/quizzes/{quiz_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| Request | API_ADMIN_QUIZ_UPDATERequest |
| Response / success | QuizView / 200 |
| Application operation | QuizService.update_quiz |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003 |
| Consumers | admin |

### API-ADMIN-QUESTION-PUT — Replace ordered draft questions atomically

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/quizzes/{quiz_id}/questions |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft only; complete validated answer key; positions unique. |
| Request | API_ADMIN_QUESTION_PUTRequest |
| Response / success | QuizView / 200 |
| Application operation | QuizService.replace_questions |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003 |
| Consumers | admin |

### API-ADMIN-QUIZ-DELETE — Delete unreferenced draft quiz

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/quizzes/{quiz_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_QUIZ_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | QuizService.delete_quiz |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003 |
| Consumers | admin |

### API-STUDENT-QUIZ — Read released quiz without answer key

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/enrolments/{enrolment_id}/quizzes/{quiz_id} |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_QUIZRequest |
| Response / success | LearnerQuizView / 200 |
| Application operation | QuizService.get_learner_quiz |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-001, ASM-002, ASM-003, STU-007 |
| Consumers | student |

### API-STUDENT-ATTEMPTS — Read own attempt history

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/quizzes/{quiz_id}/attempts |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ATTEMPTSRequest |
| Response / success | QuizAttemptViewPage / 200 |
| Application operation | QuizService.list_attempts |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-001, ASM-002, ASM-003, STU-007 |
| Consumers | student |

### API-STUDENT-ATTEMPT-CREATE — Start attempt with immutable quiz snapshot

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/student/enrolments/{enrolment_id}/quizzes/{quiz_id}/attempts |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ATTEMPT_CREATERequest |
| Response / success | QuizAttemptView / 200 |
| Application operation | QuizService.start_attempt |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ATTEMPT_LIMIT_REACHED |
| Requirements | ASM-001, ASM-002, ASM-003, STU-007 |
| Consumers | student |

### API-STUDENT-ATTEMPT-SAVE — Save selections on own in-progress attempt

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/student/quiz-attempts/{attempt_id}/answers |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ATTEMPT_SAVERequest |
| Response / success | QuizAttemptView / 200 |
| Application operation | QuizService.save_answers |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-001, ASM-002, ASM-003, STU-007 |
| Consumers | student |

### API-STUDENT-ATTEMPT-SUBMIT — Submit once and release formative score

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/student/quiz-attempts/{attempt_id}/submission |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ATTEMPT_SUBMITRequest |
| Response / success | QuizAttemptView / 200 |
| Application operation | QuizService.submit_attempt |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ATTEMPT_ALREADY_SUBMITTED |
| Requirements | ASM-001, ASM-002, ASM-003, STU-007 |
| Consumers | student |

### API-TEACHER-QUIZ-RESULTS — Read assigned learners submitted quiz scores

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/quiz-attempts |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_QUIZ_RESULTSRequest |
| Response / success | QuizAttemptViewPage / 200 |
| Application operation | QuizService.list_teaching_attempts |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-001, ASM-002, ASM-003 |
| Consumers | teacher |

### API-ADMIN-QUIZ-RESULTS — Oversee submitted quiz outcomes

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts/{cohort_id}/quiz-attempts |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_QUIZ_RESULTSRequest |
| Response / success | QuizAttemptViewPage / 200 |
| Application operation | QuizService.list_admin_attempts |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-010, ASM-001, ASM-002, ASM-003 |
| Consumers | admin |

### API-PARENT-QUIZ-RESULTS — Read released child quiz results

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/quiz-results |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_QUIZ_RESULTSRequest |
| Response / success | ChildQuizResultViewPage / 200 |
| Application operation | QuizService.list_child_quiz_results |
| Domain objects | Quiz, QuizQuestion, QuizAttempt, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-001, ASM-002, ASM-003 |
| Consumers | parent |

### API-ADMIN-ASSIGNMENTS-LIST — List assignment/project authoring definitions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/revisions/{revision_id}/assignments |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSIGNMENTS_LISTRequest |
| Response / success | AssignmentViewPage / 200 |
| Application operation | AssignmentService.list_assignments |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-011, ASM-004 |
| Consumers | admin |

### API-ADMIN-ASSIGNMENT-GET — Read assignment authoring detail

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/assignments/{assignment_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSIGNMENT_GETRequest |
| Response / success | AssignmentView / 200 |
| Application operation | AssignmentService.get_assignment |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-011, ASM-004 |
| Consumers | admin |

### API-ADMIN-ASSIGNMENT-DEFINE — Create assignment or project definition

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/lessons/{lesson_id}/assignments |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| Request | API_ADMIN_ASSIGNMENT_DEFINERequest |
| Response / success | AssignmentView / 200 |
| Application operation | AssignmentService.create_assignment |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-011, ASM-004 |
| Consumers | admin |

### API-ADMIN-ASSIGNMENT-EDIT — Edit draft assignment definition

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/assignments/{assignment_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Draft revision only. |
| Request | API_ADMIN_ASSIGNMENT_EDITRequest |
| Response / success | AssignmentView / 200 |
| Application operation | AssignmentService.update_assignment |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-011, ASM-004 |
| Consumers | admin |

### API-ADMIN-ASSIGNMENT-DELETE — Delete unreferenced draft assignment

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/assignments/{assignment_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSIGNMENT_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | AssignmentService.delete_assignment |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE |
| Requirements | ADM-011, ASM-004 |
| Consumers | admin |

### API-STUDENT-ASSIGNMENTS — Read permitted assignment and project work

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/enrolments/{enrolment_id}/assignments |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ASSIGNMENTSRequest |
| Response / success | AssignmentViewPage / 200 |
| Application operation | AssignmentService.list_student_assignments |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-004, STU-008 |
| Consumers | student |

### API-PARENT-ASSIGNMENTS — Read permitted assignment and project work

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/assignments |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_ASSIGNMENTSRequest |
| Response / success | AssignmentViewPage / 200 |
| Application operation | AssignmentService.list_parent_assignments |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-004 |
| Consumers | parent |

### API-TEACHER-ASSIGNMENTS — Read permitted assignment and project work

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/assignments |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_ASSIGNMENTSRequest |
| Response / success | AssignmentViewPage / 200 |
| Application operation | AssignmentService.list_teacher_assignments |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-004, TCH-010 |
| Consumers | teacher |

### API-STUDENT-SUBMISSIONS — Read own immutable submission history

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/assignments/{assignment_id}/submissions |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_SUBMISSIONSRequest |
| Response / success | SubmissionViewPage / 200 |
| Application operation | SubmissionService.list_own_submissions |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-005, STU-009, STU-010 |
| Consumers | student |

### API-STUDENT-SUBMISSION-CREATE — Start own assignment submission/revision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/student/enrolments/{enrolment_id}/assignments/{assignment_id}/submissions |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. New attempt only if policy permits or prior attempt returned. |
| Request | API_STUDENT_SUBMISSION_CREATERequest |
| Response / success | SubmissionView / 200 |
| Application operation | SubmissionService.create_submission |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-005, STU-009, STU-010 |
| Consumers | student |

### API-STUDENT-SUBMISSION-SAVE — Save own draft work and ready scanned file links

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/student/submissions/{submission_id} |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_SUBMISSION_SAVERequest |
| Response / success | SubmissionView / 200 |
| Application operation | SubmissionService.save_submission |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSET_NOT_READY |
| Requirements | ASM-005, STU-009, STU-010 |
| Consumers | student |

### API-STUDENT-SUBMISSION-SEND — Freeze own work and enqueue assessment notice

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/student/submissions/{submission_id}/submission |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Late work accepted and labelled until cohort complete or explicitly closed. |
| Request | API_STUDENT_SUBMISSION_SENDRequest |
| Response / success | SubmissionView / 200 |
| Application operation | SubmissionService.submit_work |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSIGNMENT_CLOSED, ASSET_NOT_READY |
| Requirements | ASM-005, STU-009, STU-010 |
| Consumers | student |

### API-STUDENT-SUBMISSION-DELETE — Discard own unsubmitted draft

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/student/submissions/{submission_id} |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_SUBMISSION_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | SubmissionService.delete_draft |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-005, STU-009, STU-010 |
| Consumers | student |

### API-PARENT-SUBMISSIONS — Read child submission status/history

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/submissions |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_SUBMISSIONSRequest |
| Response / success | ChildSubmissionStatusViewPage / 200 |
| Application operation | SubmissionService.list_child_submissions |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-005 |
| Consumers | parent |

### API-TEACHER-SUBMISSIONS — Read authorized submitted work review queue

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/submissions |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_SUBMISSIONSRequest |
| Response / success | SubmissionViewPage / 200 |
| Application operation | SubmissionService.list_teacher_submissions |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-005 |
| Consumers | teacher |

### API-TEACHER-SUBMISSION — Read authorized frozen work version

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/submissions/{submission_id} |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_SUBMISSIONRequest |
| Response / success | SubmissionView / 200 |
| Application operation | SubmissionService.get_teacher_submission |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-005 |
| Consumers | teacher |

### API-TEACHER-RETURN — Return work for a new immutable revision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/submissions/{submission_id}/return |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_RETURNRequest |
| Response / success | SubmissionView / 200 |
| Application operation | AssessmentService.return_teacher_submission |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-006, ASM-007, TCH-011, TCH-012 |
| Consumers | teacher |

### API-TEACHER-ASSESSMENT — Save draft marking against frozen submission

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/teacher/submissions/{submission_id}/assessment |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_ASSESSMENTRequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.save_teacher_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-006, ASM-007, TCH-011, TCH-012 |
| Consumers | teacher |

### API-TEACHER-ASSESSMENT-GET — Read permitted draft/released marking

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/submissions/{submission_id}/assessment |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_ASSESSMENT_GETRequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.get_teacher_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-006, ASM-007, TCH-011, TCH-012 |
| Consumers | teacher |

### API-TEACHER-ASSESSMENT-RELEASE — Release validated assessment to learner and guardian

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/assessments/{assessment_id}/release |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_ASSESSMENT_RELEASERequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.release_teacher_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-006, ASM-007, TCH-011, TCH-012 |
| Consumers | teacher |

### API-TEACHER-ASSESSMENT-WITHDRAW — Withdraw erroneous release and preserve correction history

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/assessments/{assessment_id}/withdrawal |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_ASSESSMENT_WITHDRAWRequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.withdraw_teacher_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-006, ASM-007, TCH-011, TCH-012 |
| Consumers | teacher |

### API-TEACHER-FEEDBACK-LIST — Read permitted feedback drafts/releases

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/feedback |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_FEEDBACK_LISTRequest |
| Response / success | FeedbackViewPage / 200 |
| Application operation | FeedbackService.list_teacher_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-008, TCH-013 |
| Consumers | teacher |

### API-TEACHER-FEEDBACK-CREATE — Create draft educational feedback

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/cohorts/{cohort_id}/feedback |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_FEEDBACK_CREATERequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.create_teacher_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-008, TCH-013 |
| Consumers | teacher |

### API-TEACHER-FEEDBACK-UPDATE — Revise draft feedback; released content requires withdrawal first

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/teacher/feedback/{feedback_id} |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_FEEDBACK_UPDATERequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.update_teacher_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-008, TCH-013 |
| Consumers | teacher |

### API-TEACHER-FEEDBACK-RELEASE — Release educational feedback and notify

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/feedback/{feedback_id}/release |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_FEEDBACK_RELEASERequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.release_teacher_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-008, TCH-013 |
| Consumers | teacher |

### API-TEACHER-FEEDBACK-WITHDRAW — Withdraw mistaken feedback release with reason

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/teacher/feedback/{feedback_id}/withdrawal |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_FEEDBACK_WITHDRAWRequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.withdraw_teacher_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ASM-008, TCH-013 |
| Consumers | teacher |

### API-TEACHER-PROGRESS — Read permitted learner completion evidence

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/cohorts/{cohort_id}/progress |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_PROGRESSRequest |
| Response / success | ProgressViewPage / 200 |
| Application operation | ProgressService.list_teacher_progress |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-007, LRN-008, TCH-014 |
| Consumers | teacher |

### API-ADMIN-SUBMISSIONS — Read authorized submitted work review queue

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts/{cohort_id}/submissions |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SUBMISSIONSRequest |
| Response / success | SubmissionViewPage / 200 |
| Application operation | SubmissionService.list_admin_submissions |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-005 |
| Consumers | admin |

### API-ADMIN-SUBMISSION — Read authorized frozen work version

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/submissions/{submission_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SUBMISSIONRequest |
| Response / success | SubmissionView / 200 |
| Application operation | SubmissionService.get_admin_submission |
| Domain objects | Submission, FileAsset, ReleasePolicy |
| Ports / repositories | AssessmentRepository, FileRepository, EnrolmentRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-005 |
| Consumers | admin |

### API-ADMIN-RETURN — Return work for a new immutable revision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/submissions/{submission_id}/return |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_RETURNRequest |
| Response / success | SubmissionView / 200 |
| Application operation | AssessmentService.return_admin_submission |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-012, ASM-006, ASM-007 |
| Consumers | admin |

### API-ADMIN-ASSESSMENT — Save draft marking against frozen submission

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/submissions/{submission_id}/assessment |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSESSMENTRequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.save_admin_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-012, ASM-006, ASM-007 |
| Consumers | admin |

### API-ADMIN-ASSESSMENT-GET — Read permitted draft/released marking

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/submissions/{submission_id}/assessment |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSESSMENT_GETRequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.get_admin_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-012, ASM-006, ASM-007 |
| Consumers | admin |

### API-ADMIN-ASSESSMENT-RELEASE — Release validated assessment to learner and guardian

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/assessments/{assessment_id}/release |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSESSMENT_RELEASERequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.release_admin_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-012, ASM-006, ASM-007 |
| Consumers | admin |

### API-ADMIN-ASSESSMENT-WITHDRAW — Withdraw erroneous release and preserve correction history

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/assessments/{assessment_id}/withdrawal |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSESSMENT_WITHDRAWRequest |
| Response / success | AssessmentView / 200 |
| Application operation | AssessmentService.withdraw_admin_assessment |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-012, ASM-006, ASM-007 |
| Consumers | admin |

### API-ADMIN-FEEDBACK-LIST — Read permitted feedback drafts/releases

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts/{cohort_id}/feedback |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FEEDBACK_LISTRequest |
| Response / success | FeedbackViewPage / 200 |
| Application operation | FeedbackService.list_admin_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-019, ASM-008 |
| Consumers | admin |

### API-ADMIN-FEEDBACK-CREATE — Create draft educational feedback

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/cohorts/{cohort_id}/feedback |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FEEDBACK_CREATERequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.create_admin_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-019, ASM-008 |
| Consumers | admin |

### API-ADMIN-FEEDBACK-UPDATE — Revise draft feedback; released content requires withdrawal first

| Contract | Definition |
| --- | --- |
| Method / route | PATCH /api/v1/admin/feedback/{feedback_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FEEDBACK_UPDATERequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.update_admin_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-019, ASM-008 |
| Consumers | admin |

### API-ADMIN-FEEDBACK-RELEASE — Release educational feedback and notify

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/feedback/{feedback_id}/release |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FEEDBACK_RELEASERequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.release_admin_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-019, ASM-008 |
| Consumers | admin |

### API-ADMIN-FEEDBACK-WITHDRAW — Withdraw mistaken feedback release with reason

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/feedback/{feedback_id}/withdrawal |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FEEDBACK_WITHDRAWRequest |
| Response / success | FeedbackView / 200 |
| Application operation | FeedbackService.withdraw_admin_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-019, ASM-008 |
| Consumers | admin |

### API-ADMIN-PROGRESS — Read permitted learner completion evidence

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/cohorts/{cohort_id}/progress |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PROGRESSRequest |
| Response / success | ProgressViewPage / 200 |
| Application operation | ProgressService.list_admin_progress |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-018, LRN-007, LRN-008 |
| Consumers | admin |

### API-STUDENT-ASSESSMENTS — Read own/linked child released assessments

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/assessments |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |
| Request | API_STUDENT_ASSESSMENTSRequest |
| Response / success | AssessmentViewPage / 200 |
| Application operation | AssessmentService.list_student_assessments |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-006, ASM-007, STU-011 |
| Consumers | student |

### API-STUDENT-FEEDBACK — Read own/linked child released feedback

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/feedback |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |
| Request | API_STUDENT_FEEDBACKRequest |
| Response / success | FeedbackViewPage / 200 |
| Application operation | FeedbackService.list_student_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-008, STU-012 |
| Consumers | student |

### API-STUDENT-PROGRESS — Read own/linked child released progress

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/progress |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |
| Request | API_STUDENT_PROGRESSRequest |
| Response / success | ProgressViewPage / 200 |
| Application operation | ProgressService.list_student_progress |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-007, LRN-008, STU-016 |
| Consumers | student |

### API-STUDENT-CERTIFICATES — Read own/linked child released certificates

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/certificates |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Released records only. |
| Request | API_STUDENT_CERTIFICATESRequest |
| Response / success | CertificateViewPage / 200 |
| Application operation | CertificateService.list_student_certificates |
| Domain objects | Certificate, CompletionPolicy, StudentProgress |
| Ports / repositories | CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-009, LRN-010, STU-017 |
| Consumers | student |

### API-PARENT-ASSESSMENTS — Read own/linked child released assessments

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/assessments |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |
| Request | API_PARENT_ASSESSMENTSRequest |
| Response / success | AssessmentViewPage / 200 |
| Application operation | AssessmentService.list_parent_assessments |
| Domain objects | Assessment, Submission, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-006, ASM-007, PAR-013 |
| Consumers | parent |

### API-PARENT-FEEDBACK — Read own/linked child released feedback

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/feedback |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |
| Request | API_PARENT_FEEDBACKRequest |
| Response / success | FeedbackViewPage / 200 |
| Application operation | FeedbackService.list_parent_feedback |
| Domain objects | TeacherFeedback, ReleasePolicy, TeachingAccessPolicy |
| Ports / repositories | AssessmentRepository, DeliveryRepository, EnrolmentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ASM-008, PAR-012 |
| Consumers | parent |

### API-PARENT-PROGRESS — Read own/linked child released progress

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/progress |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |
| Request | API_PARENT_PROGRESSRequest |
| Response / success | ProgressViewPage / 200 |
| Application operation | ProgressService.list_parent_progress |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-007, LRN-008, PAR-011 |
| Consumers | parent |

### API-PARENT-CERTIFICATES — Read own/linked child released certificates

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/students/{student_id}/certificates |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Released records only. |
| Request | API_PARENT_CERTIFICATESRequest |
| Response / success | CertificateViewPage / 200 |
| Application operation | CertificateService.list_parent_certificates |
| Domain objects | Certificate, CompletionPolicy, StudentProgress |
| Ports / repositories | CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-009, LRN-010, PAR-014 |
| Consumers | parent |

### API-STUDENT-ACTIVITY-GET — Read own activity/reflection status

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/enrolments/{enrolment_id}/activities |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ACTIVITY_GETRequest |
| Response / success | ActivityCompletionViewPage / 200 |
| Application operation | ProgressService.list_activities |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-007, LRN-008, STU-016 |
| Consumers | student |

### API-STUDENT-ACTIVITY — Record own non-graded activity and reflection

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/student/enrolments/{enrolment_id}/lessons/{lesson_id}/activities/{block_id} |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_ACTIVITYRequest |
| Response / success | ActivityCompletionView / 200 |
| Application operation | ProgressService.record_activity |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | LRN-007, LRN-008, STU-016 |
| Consumers | student |

### API-STUDENT-LESSON-COMPLETE — Record own lesson acknowledgement

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/student/enrolments/{enrolment_id}/lessons/{lesson_id}/completion |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_LESSON_COMPLETERequest |
| Response / success | ActivityCompletionView / 200 |
| Application operation | ProgressService.complete_lesson |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | LRN-007, LRN-008, STU-016 |
| Consumers | student |

### API-ADMIN-COMPLETION-REVIEW — Record standard or evidenced exceptional course completion decision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/enrolments/{enrolment_id}/completion-review |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. education_admin may recompute standard eligibility, grant override with verified evidence and reason, or revoke prior override. Source learning records and attendance remain immutable. |
| Request | API_ADMIN_COMPLETION_REVIEWRequest |
| Response / success | ProgressView / 200 |
| Application operation | ProgressService.review_completion |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COMPLETION_NOT_ELIGIBLE, EVIDENCE_REQUIRED |
| Requirements | ADM-018, LRN-007, LRN-008 |
| Consumers | admin |

### API-ADMIN-CERTIFICATES — List certificate issue/revocation state

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/certificates |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_CERTIFICATESRequest |
| Response / success | CertificateViewPage / 200 |
| Application operation | CertificateService.list_certificates |
| Domain objects | Certificate, CompletionPolicy, StudentProgress |
| Ports / repositories | CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-020, LRN-009, LRN-010 |
| Consumers | admin |

### API-ADMIN-CERTIFICATE-ISSUE — Issue completion certificate once from eligible progress

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/enrolments/{enrolment_id}/certificates |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_CERTIFICATE_ISSUERequest |
| Response / success | CertificateView / 200 |
| Application operation | CertificateService.issue_certificate |
| Domain objects | Certificate, CompletionPolicy, StudentProgress |
| Ports / repositories | CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COMPLETION_NOT_ELIGIBLE |
| Requirements | ADM-020, LRN-009, LRN-010 |
| Consumers | admin |

### API-ADMIN-CERTIFICATE-REVOKE — Revoke incorrect certificate with reason

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/certificates/{certificate_id}/revocation |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_CERTIFICATE_REVOKERequest |
| Response / success | CertificateView / 200 |
| Application operation | CertificateService.revoke_certificate |
| Domain objects | Certificate, CompletionPolicy, StudentProgress |
| Ports / repositories | CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-020, LRN-009, LRN-010 |
| Consumers | admin |

### API-ADMIN-CERTIFICATE-REISSUE — Issue replacement linked to revoked certificate

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/certificates/{certificate_id}/reissue |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_CERTIFICATE_REISSUERequest |
| Response / success | CertificateView / 200 |
| Application operation | CertificateService.reissue_certificate |
| Domain objects | Certificate, CompletionPolicy, StudentProgress |
| Ports / repositories | CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-020, LRN-009, LRN-010 |
| Consumers | admin |

### API-PARENT-CHECKOUT — Reserve seat and create server-priced hosted checkout

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/students/{student_id}/checkout |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. Verified email; age reconfirmed within180d; current required consents. |
| Request | API_PARENT_CHECKOUTRequest |
| Response / success | CheckoutSessionView / 200 |
| Application operation | BillingService.create_checkout |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, AGE_RECONFIRMATION_REQUIRED, AGE_INELIGIBLE, ALREADY_ENROLLED, LAUNCH_CONFIGURATION_REQUIRED, PROVIDER_UNAVAILABLE |
| Requirements | PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | parent |

### API-PARENT-CHECKOUT-RETRY — Retry failed/expired checkout with fresh eligibility and seat check

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/payments/{payment_id}/checkout |
| Roles | parent |
| Ownership / assignment / state | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| Request | API_PARENT_CHECKOUT_RETRYRequest |
| Response / success | CheckoutSessionView / 200 |
| Application operation | BillingService.retry_checkout |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, PROVIDER_UNAVAILABLE |
| Requirements | PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | parent |

### API-PARENT-PAYMENTS — Read own family payment history

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/payments |
| Roles | parent |
| Ownership / assignment / state | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| Request | API_PARENT_PAYMENTSRequest |
| Response / success | PaymentViewPage / 200 |
| Application operation | BillingService.list_family_payments |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | parent |

### API-PARENT-PAYMENT — Read authoritative payment/checkout state

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/payments/{payment_id} |
| Roles | parent |
| Ownership / assignment / state | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| Request | API_PARENT_PAYMENTRequest |
| Response / success | PaymentView / 200 |
| Application operation | BillingService.get_family_payment |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | parent |

### API-PARENT-RECEIPTS — Read own immutable invoice/receipt documents

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/payments/{payment_id}/documents |
| Roles | parent |
| Ownership / assignment / state | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| Request | API_PARENT_RECEIPTSRequest |
| Response / success | ReceiptViewPage / 200 |
| Application operation | BillingService.list_family_documents |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | parent |

### API-PARENT-REFUNDS — Read own refund outcome

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/payments/{payment_id}/refunds |
| Roles | parent |
| Ownership / assignment / state | Parent principal has active billing membership in payment family; child link alone grants no billing rights; child eligibility additionally checked for checkout. |
| Request | API_PARENT_REFUNDSRequest |
| Response / success | RefundViewPage / 200 |
| Application operation | RefundService.list_family_refunds |
| Domain objects | Refund, Payment, Enrolment, Money |
| Ports / repositories | PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAY-008 |
| Consumers | parent |

### API-ADMIN-PRICES — List current and historic fees

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/prices |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PRICESRequest |
| Response / success | PriceConfigViewPage / 200 |
| Application operation | BillingService.list_prices |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-024, PAY-001 |
| Consumers | admin |

### API-ADMIN-PRICE-CREATE — Create effective dated course default/cohort override fee

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/prices |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PRICE_CREATERequest |
| Response / success | PriceConfigView / 200 |
| Application operation | BillingService.create_price |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, OVERLAPPING_PRICE_WINDOW |
| Requirements | ADM-024, PAY-001 |
| Consumers | admin |

### API-ADMIN-PRICE-RETIRE — End future pricing without changing purchase snapshots

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/prices/{price_id}/retirement |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PRICE_RETIRERequest |
| Response / success | PriceConfigView / 200 |
| Application operation | BillingService.retire_price |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-024, PAY-001 |
| Consumers | admin |

### API-ADMIN-PAYMENTS — Inspect financial transactions and exceptions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/payments |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PAYMENTSRequest |
| Response / success | AdminPaymentViewPage / 200 |
| Application operation | BillingService.list_payments |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | admin |

### API-ADMIN-PAYMENT — Read payment reconciliation references

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/payments/{payment_id} |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PAYMENTRequest |
| Response / success | AdminPaymentView / 200 |
| Application operation | BillingService.get_payment |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | admin |

### API-ADMIN-PAYMENT-RECONCILE — Queue server-to-server reconciliation

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/payments/{payment_id}/reconciliation |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PAYMENT_RECONCILERequest |
| Response / success | Accepted / 202 |
| Application operation | BillingService.request_reconciliation |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | admin |

### API-ADMIN-DOCUMENTS — Inspect immutable invoices/receipts

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/payments/{payment_id}/documents |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_DOCUMENTSRequest |
| Response / success | ReceiptViewPage / 200 |
| Application operation | BillingService.list_documents |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | admin |

### API-ADMIN-REFUNDS — Inspect refund ledger

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/payments/{payment_id}/refunds |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REFUNDSRequest |
| Response / success | RefundViewPage / 200 |
| Application operation | RefundService.list_refunds |
| Domain objects | Refund, Payment, Enrolment, Money |
| Ports / repositories | PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-026, PAY-008 |
| Consumers | admin |

### API-ADMIN-REFUND-CREATE — Request full/partial refund with explicit entitlement disposition

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/payments/{payment_id}/refunds |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REFUND_CREATERequest |
| Response / success | RefundView / 200 |
| Application operation | RefundService.create_refund |
| Domain objects | Refund, Payment, Enrolment, Money |
| Ports / repositories | PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, REFUND_EXCEEDS_BALANCE |
| Requirements | ADM-026, PAY-008 |
| Consumers | admin |

### API-ADMIN-REFUND-RETRY — Retry confirmed failed refund under same provider idempotency key

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/refunds/{refund_id}/retry |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REFUND_RETRYRequest |
| Response / success | RefundView / 200 |
| Application operation | RefundService.retry_refund |
| Domain objects | Refund, Payment, Enrolment, Money |
| Ports / repositories | PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, PROVIDER_OUTCOME_UNKNOWN |
| Requirements | ADM-026, PAY-008 |
| Consumers | admin |

### API-ADMIN-REPORT — Read bounded AUD gross/refund/net report

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/reports/finance |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REPORTRequest |
| Response / success | FinanceReportView / 200 |
| Application operation | ReportingService.get_finance_report |
| Domain objects | Payment, Refund, Receipt |
| Ports / repositories | PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-027, PAY-010 |
| Consumers | admin |

### API-ADMIN-REPORT-EXPORT — Generate bounded finance CSV export

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/reports/finance/exports |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_REPORT_EXPORTRequest |
| Response / success | ExportView / 200 |
| Application operation | ReportingService.create_finance_export |
| Domain objects | Payment, Refund, Receipt |
| Ports / repositories | PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-027, PAY-010 |
| Consumers | admin |

### API-ADMIN-PAGES — Read public page drafts

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/pages |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PAGESRequest |
| Response / success | PublicPageViewPage / 200 |
| Application operation | PublicContentService.list_page_drafts |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-PAGE-UPDATE — Save allowlisted public-page draft

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/pages/{slug} |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PAGE_UPDATERequest |
| Response / success | PublicPageView / 200 |
| Application operation | PublicContentService.save_page |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-PAGE-PUBLISH — Publish reviewed public page

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/pages/{slug}/publication |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PAGE_PUBLISHRequest |
| Response / success | PublicPageView / 200 |
| Application operation | PublicContentService.publish_page |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-007, LRN-001 |
| Consumers | admin |

### API-ADMIN-POLICIES — Read draft and published legal policies

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/policies |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_POLICIESRequest |
| Response / success | PolicyViewPage / 200 |
| Application operation | ConsentService.list_policy_drafts |
| Domain objects | PolicyDocument, PolicyAcknowledgement |
| Ports / repositories | ContentRepository, FamilyRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | SEC-003 |
| Consumers | admin |

### API-ADMIN-POLICY-CREATE — Create immutable policy-version draft

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/policies |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_POLICY_CREATERequest |
| Response / success | PolicyView / 200 |
| Application operation | ConsentService.create_policy |
| Domain objects | PolicyDocument, PolicyAcknowledgement |
| Ports / repositories | ContentRepository, FamilyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | SEC-003 |
| Consumers | admin |

### API-ADMIN-POLICY-PUBLISH — Publish policy with human/legal approval evidence

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/policies/{policy_id}/publication |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_POLICY_PUBLISHRequest |
| Response / success | PolicyView / 200 |
| Application operation | ConsentService.publish_policy |
| Domain objects | PolicyDocument, PolicyAcknowledgement |
| Ports / repositories | ContentRepository, FamilyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED |
| Requirements | SEC-003 |
| Consumers | admin |

### API-ADMIN-EVENT-LIST — List event drafts and releases

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/events |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_EVENT_LISTRequest |
| Response / success | EventViewPage / 200 |
| Application operation | CommunicationService.list_events |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-EVENT-CREATE — Create audience-scoped event

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/events |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_EVENT_CREATERequest |
| Response / success | EventView / 200 |
| Application operation | CommunicationService.create_event |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-EVENT-UPDATE — Revise draft event

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/events/{event_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_EVENT_UPDATERequest |
| Response / success | EventView / 200 |
| Application operation | CommunicationService.update_event |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-EVENT-PUBLISH — Publish event and resolve recipients

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/events/{event_id}/publication |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_EVENT_PUBLISHRequest |
| Response / success | EventView / 200 |
| Application operation | CommunicationService.publish_event |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-EVENT-WITHDRAW — Cancel or withdraw event and notify affected audience

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/events/{event_id}/withdrawal |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_EVENT_WITHDRAWRequest |
| Response / success | EventView / 200 |
| Application operation | CommunicationService.withdraw_event |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-PARENT-EVENTS — Read relevant published events

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/events |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read. |
| Request | API_PARENT_EVENTSRequest |
| Response / success | EventViewPage / 200 |
| Application operation | CommunicationService.list_parent_events |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, PAR-003, PAR-015 |
| Consumers | parent |

### API-STUDENT-EVENTS — Read relevant published events

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/events |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read. |
| Request | API_STUDENT_EVENTSRequest |
| Response / success | EventViewPage / 200 |
| Application operation | CommunicationService.list_student_events |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, STU-018 |
| Consumers | student |

### API-TEACHER-EVENTS — Read relevant published events

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/events |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read. |
| Request | API_TEACHER_EVENTSRequest |
| Response / success | EventViewPage / 200 |
| Application operation | CommunicationService.list_teacher_events |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | teacher |

### API-ADMIN-ANNOUNCEMENT-LIST — List announcement drafts and releases

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/announcements |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ANNOUNCEMENT_LISTRequest |
| Response / success | AnnouncementViewPage / 200 |
| Application operation | CommunicationService.list_announcements |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-ANNOUNCEMENT-CREATE — Create audience-scoped announcement

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/announcements |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ANNOUNCEMENT_CREATERequest |
| Response / success | AnnouncementView / 200 |
| Application operation | CommunicationService.create_announcement |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-ANNOUNCEMENT-UPDATE — Revise draft announcement

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/announcements/{announcement_id} |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ANNOUNCEMENT_UPDATERequest |
| Response / success | AnnouncementView / 200 |
| Application operation | CommunicationService.update_announcement |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-ANNOUNCEMENT-PUBLISH — Publish announcement and resolve recipients

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/announcements/{announcement_id}/publication |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ANNOUNCEMENT_PUBLISHRequest |
| Response / success | AnnouncementView / 200 |
| Application operation | CommunicationService.publish_announcement |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-ADMIN-ANNOUNCEMENT-WITHDRAW — Cancel or withdraw announcement and notify affected audience

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/announcements/{announcement_id}/withdrawal |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ANNOUNCEMENT_WITHDRAWRequest |
| Response / success | AnnouncementView / 200 |
| Application operation | CommunicationService.withdraw_announcement |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-021, COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | admin |

### API-PARENT-ANNOUNCEMENTS — Read relevant published announcements

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/announcements |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Audience membership rechecked at read. |
| Request | API_PARENT_ANNOUNCEMENTSRequest |
| Response / success | AnnouncementViewPage / 200 |
| Application operation | CommunicationService.list_parent_announcements |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, PAR-003, PAR-015 |
| Consumers | parent |

### API-STUDENT-ANNOUNCEMENTS — Read relevant published announcements

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/announcements |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. Audience membership rechecked at read. |
| Request | API_STUDENT_ANNOUNCEMENTSRequest |
| Response / success | AnnouncementViewPage / 200 |
| Application operation | CommunicationService.list_student_announcements |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009, STU-018 |
| Consumers | student |

### API-TEACHER-ANNOUNCEMENTS — Read relevant published announcements

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/announcements |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. Audience membership rechecked at read. |
| Request | API_TEACHER_ANNOUNCEMENTSRequest |
| Response / success | AnnouncementViewPage / 200 |
| Application operation | CommunicationService.list_teacher_announcements |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | teacher |

### API-PUBLIC-EVENTS — Read explicitly public upcoming events

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/public/events |
| Roles | public |
| Ownership / assignment / state | Only explicitly published projection; no private child, roster, billing or operational data. |
| Request | API_PUBLIC_EVENTSRequest |
| Response / success | EventViewPage / 200 |
| Application operation | CommunicationService.list_public_events |
| Domain objects | Event, Announcement, AudiencePolicy |
| Ports / repositories | CommunicationRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | NOT_FOUND, VALIDATION_ERROR, RATE_LIMITED |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | public |

### API-NOTIFICATIONS — Read own recipient-scoped inbox

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/notifications |
| Roles | parent, student, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_NOTIFICATIONSRequest |
| Response / success | NotificationViewPage / 200 |
| Application operation | NotificationService.list_notifications |
| Domain objects | Notification, NotificationDelivery, OutboxEvent |
| Ports / repositories | NotificationRepository, EmailProvider, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-022, COM-007, PAR-016, TCH-015 |
| Consumers | parent, student, teacher, admin |

### API-NOTIFICATION-READ — Mark own notification read

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/notifications/{notification_id}/read |
| Roles | parent, student, teacher, admin |
| Ownership / assignment / state | Authenticated principal owns this account/session/notification; server resolves subject, never trusts requested role. |
| Request | API_NOTIFICATION_READRequest |
| Response / success | NotificationView / 200 |
| Application operation | NotificationService.mark_read |
| Domain objects | Notification, NotificationDelivery, OutboxEvent |
| Ports / repositories | NotificationRepository, EmailProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-022, COM-007, PAR-016, TCH-015 |
| Consumers | parent, student, teacher, admin |

### API-ADMIN-DELIVERIES — Inspect redacted delivery errors

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/notification-deliveries |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_DELIVERIESRequest |
| Response / success | DeliveryViewPage / 200 |
| Application operation | NotificationService.list_deliveries |
| Domain objects | Notification, NotificationDelivery, OutboxEvent |
| Ports / repositories | NotificationRepository, EmailProvider, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-022, COM-007 |
| Consumers | admin |

### API-ADMIN-DELIVERY-RETRY — Retry failed authorized delivery with deduplication

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/notification-deliveries/{delivery_id}/retry |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_DELIVERY_RETRYRequest |
| Response / success | Accepted / 202 |
| Application operation | NotificationService.retry_delivery |
| Domain objects | Notification, NotificationDelivery, OutboxEvent |
| Ports / repositories | NotificationRepository, EmailProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-022, COM-007 |
| Consumers | admin |

### API-PARENT-DASHBOARD — Read purpose-filtered dashboard counts and next actions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/dashboard |
| Roles | parent |
| Ownership / assignment / state | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. |
| Request | API_PARENT_DASHBOARDRequest |
| Response / success | DashboardView / 200 |
| Application operation | FamilyService.get_parent_dashboard |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | PAR-006 |
| Consumers | parent |

### API-STUDENT-DASHBOARD — Read purpose-filtered dashboard counts and next actions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/student/dashboard |
| Roles | student |
| Ownership / assignment / state | Student principal identity equals resource student_id; active/completed eligible enrolment and released pinned curriculum; no finances. |
| Request | API_STUDENT_DASHBOARDRequest |
| Response / success | DashboardView / 200 |
| Application operation | ProgressService.get_student_dashboard |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | LRN-007, LRN-008, STU-016 |
| Consumers | student |

### API-TEACHER-DASHBOARD — Read purpose-filtered dashboard counts and next actions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/teacher/dashboard |
| Roles | teacher |
| Ownership / assignment / state | Active teacher assignment covers cohort/session and requested learner enrolment; purpose-limited educational projection; never finance. |
| Request | API_TEACHER_DASHBOARDRequest |
| Response / success | DashboardView / 200 |
| Application operation | TeacherService.get_teacher_dashboard |
| Domain objects | TeacherProfile, TeacherAssignment, TeachingAccessPolicy |
| Ports / repositories | UserRepository, DeliveryRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CLS-005 |
| Consumers | teacher |

### API-ADMIN-DASHBOARD — Read purpose-filtered dashboard counts and next actions

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/dashboard |
| Roles | admin:education_admin, admin:finance_admin, admin:identity_admin, admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_DASHBOARDRequest |
| Response / success | DashboardView / 200 |
| Application operation | OperationsService.get_admin_dashboard |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-FILE-UPLOAD — Reserve validated private upload ticket

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/files/uploads |
| Roles | student, admin:education_admin, admin:operations_admin |
| Ownership / assignment / state | Student own draft submission only; admin matching purpose privilege. No parent upload feature. |
| Request | API_FILE_UPLOADRequest |
| Response / success | UploadTicketView / 200 |
| Application operation | FileService.create_upload |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, FILE_TYPE_DENIED, FILE_TOO_LARGE |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | student, admin |

### API-FILE-CONFIRM — Confirm upload and queue independent scanning

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/files/{asset_id}/upload-confirmation |
| Roles | student, admin:education_admin, admin:operations_admin |
| Ownership / assignment / state | Upload owner and same original scope; uploaded object metadata/checksum must match ticket. |
| Request | API_FILE_CONFIRMRequest |
| Response / success | FileAssetView / 200 |
| Application operation | FileService.confirm_upload |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, UPLOAD_MISMATCH |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | student, admin |

### API-FILE-GET — Read authorized file scan/metadata state

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/files/{asset_id} |
| Roles | parent, student, teacher, admin:education_admin, admin:operations_admin |
| Ownership / assignment / state | FileAccessPolicy derives released curriculum, own submission, guardian link, teaching assignment or scoped admin purpose. |
| Request | API_FILE_GETRequest |
| Response / success | FileAssetView / 200 |
| Application operation | FileService.get_asset |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | parent, student, teacher, admin |

### API-FILE-DOWNLOAD — Issue ready-file short-lived download

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/files/{asset_id}/download |
| Roles | parent, student, teacher, admin:education_admin, admin:operations_admin |
| Ownership / assignment / state | FileAccessPolicy validates ready state and linked resource scope; submission parents read only authorized child; internal files never learner-readable. |
| Request | API_FILE_DOWNLOADRequest |
| Response / success | DownloadTicketView / 200 |
| Application operation | FileService.create_download |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, ASSET_NOT_READY |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | parent, student, teacher, admin |

### API-FILE-DELETE — Delete eligible unreferenced owned draft asset

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/files/{asset_id} |
| Roles | student, admin:education_admin, admin:operations_admin |
| Ownership / assignment / state | No referenced submitted work/published resource/certificate deletion; retention and legal hold apply. |
| Request | API_FILE_DELETERequest |
| Response / success | Empty / 204 |
| Application operation | FileService.delete_asset |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, RESOURCE_IN_USE, LEGAL_HOLD |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | student, admin |

### API-ADMIN-FILES — Browse assets by permitted educational/operations purpose

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/files |
| Roles | admin:education_admin, admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FILESRequest |
| Response / success | FileAssetViewPage / 200 |
| Application operation | FileService.list_assets |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-023, FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | admin |

### API-PARENT-CALENDAR — Export authorized family schedule with portal deep links

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/calendar.ics |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. |
| Request | API_PARENT_CALENDARRequest |
| Response / success | CalendarExport / 200 |
| Application operation | CalendarService.export_family_calendar |
| Domain objects | ClassSession, Event, IntegrationBinding |
| Ports / repositories | DeliveryRepository, CommunicationRepository, IntegrationRepository, CalendarProvider, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | CAL-001, CAL-002, CAL-003, CAL-004, CAL-005 |
| Consumers | parent |

### API-ADMIN-SETTINGS — Read allowlisted non-secret operational settings

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/settings |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SETTINGSRequest |
| Response / success | SettingViewPage / 200 |
| Application operation | OperationsService.list_settings |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-SETTING-PUT — Set validated key with approval evidence for launch-sensitive values

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/settings/{key} |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_SETTING_PUTRequest |
| Response / success | SettingView / 200 |
| Application operation | OperationsService.set_setting |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-FINANCE-SETTINGS — Read merchant identity/tax configuration

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/billing-settings |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FINANCE_SETTINGSRequest |
| Response / success | SettingViewPage / 200 |
| Application operation | BillingService.list_billing_settings |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | admin |

### API-ADMIN-FINANCE-SETTING-PUT — Set approved merchant/tax/refund policy value

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/billing-settings/{key} |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_FINANCE_SETTING_PUTRequest |
| Response / success | SettingView / 200 |
| Application operation | BillingService.set_billing_setting |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, HUMAN_APPROVAL_REQUIRED |
| Requirements | ADM-025, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | admin |

### API-ADMIN-INTEGRATIONS — Read masked provider configuration and synchronization health

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/integrations |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_INTEGRATIONSRequest |
| Response / success | IntegrationStatusViewPage / 200 |
| Application operation | OperationsService.list_integrations |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-INTEGRATION-UPDATE — Enable/disable provider using managed secret reference

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/integrations/{provider} |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe credential/configuration additionally requires finance privilege. |
| Request | API_ADMIN_INTEGRATION_UPDATERequest |
| Response / success | IntegrationStatusView / 200 |
| Application operation | OperationsService.configure_integration |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-INTEGRATION-CHECK — Queue bounded provider connectivity check

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/integrations/{provider}/check |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_INTEGRATION_CHECKRequest |
| Response / success | Accepted / 202 |
| Application operation | OperationsService.check_integration |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-INTEGRATION-RESYNC — Queue provider mirror reconciliation

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/integrations/{provider}/resync |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Stripe resync requires finance privilege. |
| Request | API_ADMIN_INTEGRATION_RESYNCRequest |
| Response / success | Accepted / 202 |
| Application operation | OperationsService.request_provider_resync |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-JOBS — Read redacted job processing state

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/jobs |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_JOBSRequest |
| Response / success | JobViewPage / 200 |
| Application operation | OperationsService.list_jobs |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-JOB — Read authorized background operation status

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/jobs/{job_id} |
| Roles | admin:operations_admin, admin:finance_admin, admin:education_admin |
| Ownership / assignment / state | Match job capability and initiating admin purpose; arbitrary job IDs denied. |
| Request | API_ADMIN_JOBRequest |
| Response / success | JobView / 200 |
| Application operation | OperationsService.get_job |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-JOB-RETRY — Retry dead-letter job after cause correction

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/jobs/{job_id}/retry |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Finance jobs additionally require finance privilege; immutable original payload. |
| Request | API_ADMIN_JOB_RETRYRequest |
| Response / success | Accepted / 202 |
| Application operation | OperationsService.retry_job |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-OPERATIONS — Read actionable operational summary

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/operations |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_OPERATIONSRequest |
| Response / success | OperationsSummaryView / 200 |
| Application operation | OperationsService.get_operations_summary |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-028, OPS-003, OPS-005, OPS-008 |
| Consumers | admin |

### API-ADMIN-AUDIT — Read filtered redacted audit history

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/audit |
| Roles | admin:audit_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_AUDITRequest |
| Response / success | AuditViewPage / 200 |
| Application operation | AuditService.list_audit |
| Domain objects | AuditRecord |
| Ports / repositories | AuditRepository, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | ADM-029, SEC-007 |
| Consumers | admin |

### API-PARENT-PRIVACY-REQUEST — Request family data access/correction/deletion or account closure

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/privacy-requests |
| Roles | parent |
| Ownership / assignment / state | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. |
| Request | API_PARENT_PRIVACY_REQUESTRequest |
| Response / success | PrivacyRequestView / 200 |
| Application operation | PrivacyService.create_privacy_request |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | parent |

### API-PARENT-PRIVACY-LIST — Read own privacy request state

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/parent/privacy-requests |
| Roles | parent |
| Ownership / assignment / state | Authenticated verified parent owns an active family membership. Child list is filtered to active GuardianStudent links; an empty family is valid and does not require an existing child. If student_id is supplied, additionally require active explicit child link. |
| Request | API_PARENT_PRIVACY_LISTRequest |
| Response / success | PrivacyRequestViewPage / 200 |
| Application operation | PrivacyService.list_own_requests |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | parent |

### API-ADMIN-PRIVACY-LIST — Read restricted privacy work queue

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/privacy-requests |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_PRIVACY_LISTRequest |
| Response / success | PrivacyRequestViewPage / 200 |
| Application operation | PrivacyService.list_privacy_requests |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | admin |

### API-ADMIN-PRIVACY-DECIDE — Record verified authority and retention-aware decision

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/privacy-requests/{request_id}/decision |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Never orphan active children or erase required finance records. |
| Request | API_ADMIN_PRIVACY_DECIDERequest |
| Response / success | PrivacyRequestView / 200 |
| Application operation | PrivacyService.decide_request |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, LEGAL_HOLD, ACTIVE_GUARDIAN_REQUIRED |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | admin |

### API-PARENT-PRIVACY-EXPORT — Get ready verified family export

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/parent/privacy-requests/{request_id}/download |
| Roles | parent |
| Ownership / assignment / state | Active verified GuardianStudent link for requested student within principal family; deny revoked links and unrelated family IDs. Approved access request only; exclude unrelated guardian finances. |
| Request | API_PARENT_PRIVACY_EXPORTRequest |
| Response / success | DownloadTicketView / 200 |
| Application operation | PrivacyService.download_export |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | parent |

### API-ADMIN-LEGAL-HOLD — Set or release audited retention hold

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/privacy/holds/{resource_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_LEGAL_HOLDRequest |
| Response / success | Empty / 204 |
| Application operation | PrivacyService.set_legal_hold |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | admin |

### API-STRIPE-WEBHOOK — Validate raw signature and persist deduplicated provider event

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/webhooks/stripe |
| Roles | system |
| Ownership / assignment / state | Stripe signature on original bytes; signed does not imply relevant event; dedupe provider+event ID before any financial mutation. |
| Request | API_STRIPE_WEBHOOKRequest |
| Response / success | Empty / 204 |
| Application operation | BillingService.receive_stripe_webhook |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAY-004, PAY-005 |
| Consumers | stripe |

### JOB-PAYMENT-PROCESS — Retrieve authoritative provider state and activate paid seat safely

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:process_payment_event |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_PAYMENT_PROCESSRequest |
| Response / success | JobView / worker completion |
| Application operation | BillingService.process_payment_event |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAY-004, PAY-005 |
| Consumers | worker |

### JOB-PAYMENT-RECONCILE — Compare Stripe state with immutable local ledger

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:reconcile_payment |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_PAYMENT_RECONCILERequest |
| Response / success | JobView / worker completion |
| Application operation | BillingService.reconcile_payment |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | worker |

### JOB-HOLD-EXPIRE — Expire elapsed holds under row lock; release capacity

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:expire_holds |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_HOLD_EXPIRERequest |
| Response / success | JobView / worker completion |
| Application operation | EnrolmentService.expire_holds |
| Domain objects | Enrolment, Cohort, AgeSnapshot, FamilyOwnershipPolicy |
| Ports / repositories | EnrolmentRepository, StudentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ENR-001, ENR-002, ENR-003, ENR-004, ENR-005, ENR-006, ENR-007 |
| Consumers | worker |

### JOB-REFUND-PROCESS — Execute idempotent requested refund and apply explicit access disposition

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:process_refund |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_REFUND_PROCESSRequest |
| Response / success | JobView / worker completion |
| Application operation | RefundService.process_refund |
| Domain objects | Refund, Payment, Enrolment, Money |
| Ports / repositories | PaymentRepository, EnrolmentRepository, PaymentGateway, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAY-008 |
| Consumers | worker |

### JOB-DOCUMENT-GENERATE — Generate immutable receipt/invoice after verified payment

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:generate_purchase_documents |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_DOCUMENT_GENERATERequest |
| Response / success | JobView / worker completion |
| Application operation | BillingService.generate_purchase_documents |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | worker |

### JOB-LIVE-CREATE — Create provider meeting from authoritative session version

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:provision_meeting |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_LIVE_CREATERequest |
| Response / success | JobView / worker completion |
| Application operation | LiveClassService.provision_meeting |
| Domain objects | ClassSession, IntegrationBinding, TeachingAccessPolicy |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | CLS-006, CLS-007, CLS-008, CLS-009 |
| Consumers | worker |

### JOB-LIVE-UPDATE — Update/cancel meeting from latest authoritative session state

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:synchronize_meeting |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_LIVE_UPDATERequest |
| Response / success | JobView / worker completion |
| Application operation | LiveClassService.synchronize_meeting |
| Domain objects | ClassSession, IntegrationBinding, TeachingAccessPolicy |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | CLS-006, CLS-007, CLS-008, CLS-009 |
| Consumers | worker |

### JOB-LIVE-RECONCILE — Resolve provider drift without overwriting domain schedule

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:reconcile_meetings |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_LIVE_RECONCILERequest |
| Response / success | JobView / worker completion |
| Application operation | LiveClassService.reconcile_meetings |
| Domain objects | ClassSession, IntegrationBinding, TeachingAccessPolicy |
| Ports / repositories | DeliveryRepository, EnrolmentRepository, IntegrationRepository, LiveClassProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | CLS-006, CLS-007, CLS-008, CLS-009 |
| Consumers | worker |

### JOB-CALENDAR-SYNC — Upsert/cancel individual business calendar mirror event

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:synchronize_event |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_CALENDAR_SYNCRequest |
| Response / success | JobView / worker completion |
| Application operation | CalendarService.synchronize_event |
| Domain objects | ClassSession, Event, IntegrationBinding |
| Ports / repositories | DeliveryRepository, CommunicationRepository, IntegrationRepository, CalendarProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | CAL-001, CAL-002, CAL-003, CAL-004, CAL-005 |
| Consumers | worker |

### JOB-CALENDAR-RESYNC — Recover invalid sync token with full mirror reconciliation

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:reconcile_calendar |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_CALENDAR_RESYNCRequest |
| Response / success | JobView / worker completion |
| Application operation | CalendarService.reconcile_calendar |
| Domain objects | ClassSession, Event, IntegrationBinding |
| Ports / repositories | DeliveryRepository, CommunicationRepository, IntegrationRepository, CalendarProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | CAL-001, CAL-002, CAL-003, CAL-004, CAL-005 |
| Consumers | worker |

### JOB-NOTIFICATION-PREPARE — Resolve outbox recipients and create deduplicated notices

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:prepare_notifications |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_NOTIFICATION_PREPARERequest |
| Response / success | JobView / worker completion |
| Application operation | NotificationService.prepare_notifications |
| Domain objects | Notification, NotificationDelivery, OutboxEvent |
| Ports / repositories | NotificationRepository, EmailProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | worker |

### JOB-EMAIL-SEND — Deliver transactional email with durable local deduplication

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:deliver_email |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_EMAIL_SENDRequest |
| Response / success | JobView / worker completion |
| Application operation | NotificationService.deliver_email |
| Domain objects | Notification, NotificationDelivery, OutboxEvent |
| Ports / repositories | NotificationRepository, EmailProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | worker |

### JOB-REMINDER-SCHEDULE — Queue class reminders once per current session version

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:schedule_reminders |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_REMINDER_SCHEDULERequest |
| Response / success | JobView / worker completion |
| Application operation | NotificationService.schedule_reminders |
| Domain objects | Notification, NotificationDelivery, OutboxEvent |
| Ports / repositories | NotificationRepository, EmailProvider, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | COM-001, COM-002, COM-003, COM-004, COM-005, COM-006, COM-008, COM-009 |
| Consumers | worker |

### JOB-FILE-SCAN — Verify metadata/MIME/archive limits/malware and promote immutable object

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:scan_and_promote |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_FILE_SCANRequest |
| Response / success | JobView / worker completion |
| Application operation | FileService.scan_and_promote |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | worker |

### JOB-FILE-CLEAN — Delete expired unreferenced staging objects after retention/hold checks

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:clean_orphaned_uploads |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_FILE_CLEANRequest |
| Response / success | JobView / worker completion |
| Application operation | FileService.clean_orphaned_uploads |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | worker |

### JOB-FILE-DELETE — Delete eligible private object/version per approved retention decision

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:purge_asset |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_FILE_DELETERequest |
| Response / success | JobView / worker completion |
| Application operation | FileService.purge_asset |
| Domain objects | FileAsset, FileAccessPolicy |
| Ports / repositories | FileRepository, ObjectStorageProvider, MalwareScanner, EnrolmentRepository, FamilyRepository, DeliveryRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | FILE-001, FILE-002, FILE-003, FILE-004, FILE-005, FILE-006, FILE-007 |
| Consumers | worker |

### JOB-PROGRESS-RECOMPUTE — Recalculate completion from latest released work and attendance evidence

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:recompute_progress |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_PROGRESS_RECOMPUTERequest |
| Response / success | ProgressView / worker completion |
| Application operation | ProgressService.recompute_progress |
| Domain objects | StudentProgress, CompletionPolicy, Enrolment, ActivityCompletion, CompletionOverride |
| Ports / repositories | ProgressRepository, AssessmentRepository, CourseRepository, EnrolmentRepository, UnitOfWork, Clock, AttendanceRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | LRN-007, LRN-008 |
| Consumers | worker |

### JOB-CERTIFICATE-RENDER — Render immutable certificate artifact and mark issued after ready storage

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:render_certificate |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_CERTIFICATE_RENDERRequest |
| Response / success | CertificateView / worker completion |
| Application operation | CertificateService.render_certificate |
| Domain objects | Certificate, CompletionPolicy, StudentProgress |
| Ports / repositories | CertificateRepository, ProgressRepository, EnrolmentRepository, FileRepository, CertificateRenderer, UnitOfWork, Clock, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | LRN-009, LRN-010 |
| Consumers | worker |

### JOB-PRIVACY-PROCESS — Generate protected export or execute approved retention-aware deletion/closure

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:process_request |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_PRIVACY_PROCESSRequest |
| Response / success | JobView / worker completion |
| Application operation | PrivacyService.process_request |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | worker |

### JOB-RETENTION — Purge/anonymize only eligible unheld records from approved matrix

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:apply_retention |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_RETENTIONRequest |
| Response / success | JobView / worker completion |
| Application operation | PrivacyService.apply_retention |
| Domain objects | PrivacyRequest, GuardianStudent, FileAsset |
| Ports / repositories | FamilyRepository, StudentRepository, FileRepository, PrivacyRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | SEC-001, SEC-002, SEC-008, SEC-009, SEC-010 |
| Consumers | worker |

### JOB-OUTBOX-DISPATCH — Publish durable intent to queue and recover expired leases

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:dispatch_outbox |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_OUTBOX_DISPATCHRequest |
| Response / success | JobView / worker completion |
| Application operation | OperationsService.dispatch_outbox |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | OPS-005 |
| Consumers | worker |

### JOB-INTEGRATION-CHECK — Check configured provider and persist masked operational state

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:probe_integration |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_INTEGRATION_CHECKRequest |
| Response / success | IntegrationStatusView / worker completion |
| Application operation | OperationsService.probe_integration |
| Domain objects | ApplicationSetting, IntegrationBinding, BackgroundJob, WebhookInbox, OutboxEvent |
| Ports / repositories | SettingsRepository, IntegrationRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | OPS-003 |
| Consumers | worker |

### JOB-FINANCE-EXPORT — Write formula-injection-safe CSV to private export storage

| Contract | Definition |
| --- | --- |
| Method / route | WORKER worker:generate_finance_export |
| Roles | system |
| Ownership / assignment / state | Internal service identity; validated durable job/event origin; no browser route and no user-provided worker privilege. |
| Request | JOB_FINANCE_EXPORTRequest |
| Response / success | ExportView / worker completion |
| Application operation | ReportingService.generate_finance_export |
| Domain objects | Payment, Refund, Receipt |
| Ports / repositories | PaymentRepository, UnitOfWork, Clock, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAY-010 |
| Consumers | worker |

### API-ADMIN-ASSIGNMENT-CLOSE — Close/reopen assignment submissions for a delivery

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/cohorts/{cohort_id}/assignments/{assignment_id}/closure |
| Roles | admin:education_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ASSIGNMENT_CLOSERequest |
| Response / success | AssignmentView / 200 |
| Application operation | AssignmentService.set_delivery_closure |
| Domain objects | Assignment, CurriculumRevision, ReleasePolicy |
| Ports / repositories | AssessmentRepository, CourseRepository, UnitOfWork, EnrolmentRepository, DeliveryRepository |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | ADM-011, ASM-004 |
| Consumers | admin |

### API-ADMIN-BILLING-MEMBER — Grant verified adult family billing visibility separately from child links

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/families/{family_id}/billing-members |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Separate finance approval reference required; no teacher principal. |
| Request | API_ADMIN_BILLING_MEMBERRequest |
| Response / success | FamilyView / 200 |
| Application operation | FamilyService.create_billing_membership |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-006 |
| Consumers | admin |

### API-ADMIN-BILLING-MEMBER-REVOKE — Revoke adult family financial membership

| Contract | Definition |
| --- | --- |
| Method / route | DELETE /api/v1/admin/families/{family_id}/billing-members/{guardian_id} |
| Roles | admin:identity_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_BILLING_MEMBER_REVOKERequest |
| Response / success | Empty / 204 |
| Application operation | FamilyService.revoke_billing_membership |
| Domain objects | Family, Guardian, GuardianStudent, FamilyOwnershipPolicy, BillingMembership |
| Ports / repositories | FamilyRepository, StudentRepository, UnitOfWork, Clock |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | PAR-006 |
| Consumers | admin |

### API-ADMIN-ENQUIRIES — Read inbound enquiries to support customers

| Contract | Definition |
| --- | --- |
| Method / route | GET /api/v1/admin/contact-enquiries |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ENQUIRIESRequest |
| Response / success | ContactEnquiryViewPage / 200 |
| Application operation | PublicContentService.list_contact_enquiries |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Read-only scoped projection |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR |
| Requirements | WEB-009 |
| Consumers | admin |

### API-ADMIN-ENQUIRY-STATUS — Mark enquiry handled without sending unauthorized messages

| Contract | Definition |
| --- | --- |
| Method / route | PUT /api/v1/admin/contact-enquiries/{enquiry_id}/status |
| Roles | admin:operations_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. |
| Request | API_ADMIN_ENQUIRY_STATUSRequest |
| Response / success | ContactEnquiryView / 200 |
| Application operation | PublicContentService.set_enquiry_status |
| Domain objects | PublicPage, Program, Course, TeacherProfile, PublicationPolicy, ContactEnquiry |
| Ports / repositories | ContentRepository, CourseRepository, UserRepository, NotificationRepository, UnitOfWork |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE |
| Requirements | WEB-009 |
| Consumers | admin |

### API-ADMIN-PAID-EXCEPTION — Resolve late paid no-seat exception exactly once by allocation or refund

| Contract | Definition |
| --- | --- |
| Method / route | POST /api/v1/admin/payments/{payment_id}/exception-resolution |
| Roles | admin:finance_admin |
| Ownership / assignment / state | Admin privilege stated in roles plus active account and recent MFA; no teacher principal, no cross-purpose projection. Lock Payment+Enrolment+Cohort; ALLOCATE requires available seat and no pending refund; REFUND reserves refundable balance and prevents activation. |
| Request | API_ADMIN_PAID_EXCEPTIONRequest |
| Response / success | AdminPaymentView / 200 |
| Application operation | BillingService.resolve_paid_exception |
| Domain objects | Payment, Price, Money, Enrolment, WebhookInbox, CapacityPolicy, BillingMembership, Receipt |
| Ports / repositories | PaymentRepository, EnrolmentRepository, DeliveryRepository, FamilyRepository, PaymentGateway, UnitOfWork, Clock, SettingsRepository, IntegrationRepository, FileRepository, ObjectStorageProvider |
| Transaction | Authorize, reserve idempotency where required, lock affected aggregate/version, invoke domain behavior, commit audit+outbox; provider calls outside held locks. |
| Errors | UNAUTHENTICATED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, VERSION_CONFLICT, INVALID_STATE, COHORT_FULL, REFUND_PENDING, EXCEPTION_ALREADY_RESOLVED |
| Requirements | ADM-025, PAR-017, PAR-018, PAR-019, PAR-020, PAY-002, PAY-003, PAY-006, PAY-007, PAY-009, PAY-011, PAY-012 |
| Consumers | admin |


## Field-level reusable schema catalog

### Empty

No JSON body; successful deletion is HTTP 204.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### Accepted

HTTP 202 durable operation accepted; poll authorized job.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| job_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(queued\|running) | True | False | body | Closed enum; reject unknown values |
| status_url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |

### Error

RFC9457-style JSON problem body; HTTP status specified in error catalog.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| code | string | True | False | body | Stable documented error code |
| message | string | True | False | body | Safe actionable text without resource existence leaks |
| request_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| field_errors | FieldError[] | False | False | body | Validate referenced schema recursively |
| retry_after_seconds | integer | False | False | body | 1–3600 |

### FieldError

FieldError

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| field | string | True | False | body | Known input field path |
| code | string | True | False | body | Validation code |
| message | string | True | False | body | Safe validation message |

### PageMeta

Opaque signed cursor binds principal, query, order and expiry.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| next_cursor | token | True | True | body | opaque cryptographic token; max 512 characters; never logged |
| has_more | boolean | True | False | body | strict JSON boolean |

### SessionView

No bearer session secret in JSON; HttpOnly cookie set separately.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| privileges | string[] | True | False | body | Closed identifiers: identity_admin,education_admin,finance_admin,operations_admin,audit_admin |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| csrf_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| mfa_required | boolean | True | False | body | strict JSON boolean |

### AccountView

Child identity may have no email; staff privileges only in authorized admin projection.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | True | body | normalized verified deliverable address; max 254 characters |
| status | enum(invited\|pending_verification\|active\|suspended\|closed) | True | False | body | Closed enum; reject unknown values |
| mfa_enabled | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

### DeviceSessionView

No IP address or raw credential exposed.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| last_seen_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| device_label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| current | boolean | True | False | body | strict JSON boolean |

### GuardianView

GuardianView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| phone | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| essential_contact | enum(email) | True | False | body | Closed enum; reject unknown values |
| optional_email | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

### FamilyView

Parent projection includes only actively linked students, not every family sibling. Billing membership never inferred from list membership.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| guardians | GuardianSummary[] | True | False | body | Validate referenced schema recursively |
| students | StudentSummary[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |

### GuardianSummary

GuardianSummary

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| relationship | enum(primary\|verified_guardian) | True | False | body | Closed enum; reject unknown values |
| status | enum(active\|revoked) | True | False | body | Closed enum; reject unknown values |

### StudentSummary

StudentSummary

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 proposed technical input; approved launch bands enforced separately |
| age_recorded_on | date | True | False | body | ISO8601 calendar date |
| status | enum(active\|archived) | True | False | body | Closed enum; reject unknown values |

### StudentProfileView

StudentProfileView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 |
| age_recorded_on | date | True | False | body | ISO8601 calendar date |
| school_name | string | True | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | True | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | True | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | True | True | body | Optional closed educational-experience enum |
| status | enum(active\|archived) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

### TeachingStudentView

Purpose-limited teaching projection: excludes family ID, school name, last name, email, phone, billing and credentials.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | True | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 |
| age_recorded_on | date | True | False | body | ISO8601 calendar date |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | True | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | True | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | True | True | body | Optional closed educational-experience enum |

### StudentCredentialsView

Returned only once to authorized guardian after step-up; no child email required.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| username | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| one_time_secret | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### TeacherView

TeacherView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| biography | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| public_photo_asset_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(invited\|active\|suspended\|archived) | True | False | body | Closed enum; reject unknown values |
| public_profile_published | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

### PublicTeacherView

Explicitly published teacher profile only.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| biography | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| photo_url | url | True | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |

### RoleGrantView

RoleGrantView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| user_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| admin_privileges | string[] | True | False | body | Closed identifiers: identity_admin,education_admin,finance_admin,operations_admin,audit_admin |
| version | version | True | False | body | positive integer optimistic concurrency token |

### PolicyView

PolicyView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| key | enum(privacy\|terms\|child_safety\|consent) | True | False | body | Closed enum; reject unknown values |
| version_label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| requires_acknowledgement | boolean | True | False | body | strict JSON boolean |
| effective_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### AcknowledgementView

Immutable evidence, not an editable boolean.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| policy_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| policy_version | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| guardian_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| acknowledged_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### PublicPageView

PublicPageView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| slug | string | True | False | body | home,about,how-classes-work,parents,faq,contact,age-groups only |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### ContactReceipt

No contact payload echoed; submission becomes restricted operational notice.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| reference | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| accepted_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### ProgramView

ProgramView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(draft\|published\|archived) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

### PublicProgramView

PublicProgramView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |

### CourseView

CourseView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| program_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | True | False | body | Validate referenced schema recursively |
| min_age | integer | True | False | body | 4–18 |
| max_age | integer | True | False | body | 4–18 and >= min_age |
| duration_weeks | integer | True | False | body | 1–52 |
| delivery_method | enum(live_online) | True | False | body | Closed enum; reject unknown values |
| status | enum(draft\|published\|archived) | True | False | body | Closed enum; reject unknown values |
| current_revision_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| version | version | True | False | body | positive integer optimistic concurrency token |

### PublicCourseView

Published marketing projection. Does not expose lesson drafts, content URLs, answers or internal settings.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| program_title | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| slug | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | True | False | body | Validate referenced schema recursively |
| min_age | integer | True | False | body | strict integer |
| max_age | integer | True | False | body | strict integer |
| duration_weeks | integer | True | False | body | strict integer |
| delivery_method | enum(live_online) | True | False | body | Closed enum; reject unknown values |
| display_price | PriceView | True | True | body | Type validation; no unknown fields |
| curriculum_outline | OutlineModule[] | True | False | body | Validate referenced schema recursively |

### OutlineModule

Only explicitly publishable outline titles.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| lesson_titles | string[] | True | False | body | Validate referenced schema recursively |

### CurriculumRevisionView

CurriculumRevisionView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_number | integer | True | False | body | >=1 |
| status | enum(draft\|published\|retired) | True | False | body | Closed enum; reject unknown values |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| modules | ModuleView[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |

### ModuleView

ModuleView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | >=0 |
| release_offset_days | integer | True | False | body | 0–365 |
| lessons | LessonSummary[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |

### LessonSummary

Learner responses omit unreleased lessons entirely; administrative summaries may include released false.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | strict integer |
| released | boolean | True | False | body | strict JSON boolean |

### LessonView

LessonView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| module_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | strict integer |
| release_offset_days | integer | True | False | body | 0–365 |
| blocks | LessonBlockView[] | True | False | body | Validate referenced schema recursively |
| version | version | True | False | body | positive integer optimistic concurrency token |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

### LessonBlockView

Discriminated union described below; no arbitrary HTML, embeds or scripts.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | enum(heading\|rich_text\|image\|video\|download\|activity\|quiz\|assignment) | True | False | body | Closed enum; reject unknown values |
| position | integer | True | False | body | strict integer |
| content | LessonBlockContent | True | False | body | Type validation; no unknown fields |
| version | version | True | False | body | positive integer optimistic concurrency token |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

### LessonBlockContent

Exactly branch fields allowed by kind: heading=heading; rich_text=sanitized_html; image=asset_id+alt_text; video=asset_id XOR approved video_url; download=asset_id; activity=instructions; quiz=quiz_id; assignment=assignment_id. All other fields forbidden; no answer fields. Video additionally requires captions_asset_id or transcript before publication; image alt text mandatory. Resource video equivalent accessibility metadata required.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| heading | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| asset_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| alt_text | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| video_url | url | False | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| instructions | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| quiz_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| captions_asset_id | uuid | False | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| transcript | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |

### ResourceView

Exactly one ready asset or approved HTTPS external URL; learner read additionally release-gated.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| asset_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| external_url | url | True | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| kind | enum(document\|image\|video\|project) | True | False | body | Closed enum; reject unknown values |
| status | enum(draft\|ready\|archived) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

### CohortView

CohortView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| capacity | integer | True | False | body | 1–100 |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| status | enum(draft\|open\|closed\|in_progress\|completed\|cancelled) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | <=starts_at |

### PublicCohortView

No roster, meeting reference, capacity counters or teacher operational data.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| availability | enum(available\|full\|closed) | True | False | body | Closed enum; reject unknown values |
| price | PriceView | True | False | body | Type validation; no unknown fields |
| sessions | PublicSessionView[] | True | False | body | Validate referenced schema recursively |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### PublicSessionView

Published timetable only.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |

### ClassSessionView

No stored host URL or meeting credential; actions separately authorized. Learner projection hides provider failure detail.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| status | enum(scheduled\|cancelled\|completed) | True | False | body | Closed enum; reject unknown values |
| lesson_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| can_join | boolean | True | False | body | strict JSON boolean |
| can_start | boolean | True | False | body | strict JSON boolean |
| integration_status | enum(pending\|ready\|failed) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |
| teacher_display_names | string[] | True | False | body | Validate referenced schema recursively |
| student_ids | uuid[] | False | False | body | Parent response only, linked children only; forbidden in public/student/teacher details |

### TeacherAssignmentView

TeacherAssignmentView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| teacher_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| session_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(lead\|assistant) | True | False | body | Closed enum; reject unknown values |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### JoinLinkView

Sensitive short-lived handoff; Cache-Control no-store, referrer policy no-referrer; never analytics logged.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### EnrolmentView

Learner projection never includes Payment or Price.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(held\|pending_payment\|active\|cancelled\|completed\|expired\|payment_exception) | True | False | body | Closed enum; reject unknown values |
| hold_expires_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| access_ends_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### AttendanceView

No internal attendance notes are exposed to parents or students.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(present\|absent\|late\|excused\|unrecorded) | True | False | body | Closed enum; reject unknown values |
| minutes_attended | integer | True | True | body | strict integer |
| recorded_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### QuizView

Authoring quiz definition; correct keys and approved explanation included only to authorized curriculum/teaching scope. LearnerQuizView excludes both until own attempt submitted.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lesson_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| pass_percent | integer | True | False | body | 0–100 |
| max_attempts | integer | True | False | body | 1–5; default3 |
| questions | QuizQuestionView[] | True | False | body | Validate referenced schema recursively |
| status | enum(draft\|ready) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

### QuizQuestionView

Never included in learner schema.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| prompt | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| position | integer | True | False | body | strict integer |
| kind | enum(single_choice\|multiple_choice) | True | False | body | Closed enum; reject unknown values |
| options | QuizOption[] | True | False | body | Validate referenced schema recursively |
| correct_option_ids | uuid[] | True | False | body | Validate referenced schema recursively |
| points | integer | True | False | body | 1–100 |
| explanation | text | True | False | body | Approved explanation shown after learner submission; immutable with published quiz |

### QuizOption

QuizOption

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| text | string | True | False | body | 1–500 |

### LearnerQuizView

Correct-answer identifiers and grading rules omitted.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| max_attempts | integer | True | False | body | strict integer |
| attempts_remaining | integer | True | False | body | strict integer |
| questions | LearnerQuestionView[] | True | False | body | Validate referenced schema recursively |

### LearnerQuestionView

LearnerQuestionView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| prompt | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| position | integer | True | False | body | strict integer |
| kind | enum(single_choice\|multiple_choice) | True | False | body | Closed enum; reject unknown values |
| options | QuizOption[] | True | False | body | Validate referenced schema recursively |

### QuizAnswer

QuizAnswer

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| question_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| selected_option_ids | uuid[] | True | False | body | IDs in attempt snapshot; unique; one for single choice; up to all options for multiple choice |

### QuizAttemptView

Result null until release; answers only own selections, never correct-answer key.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(in_progress\|submitted\|released) | True | False | body | Closed enum; reject unknown values |
| answers | QuizAnswer[] | True | False | body | Validate referenced schema recursively |
| submitted_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| result | ReleasedQuizResult | True | True | body | Type validation; no unknown fields |
| version | version | True | False | body | positive integer optimistic concurrency token |

### ReleasedQuizResult

Immediate formative result for submitted own attempt: score plus per-question correctness and approved explanation. Never an unsubmitted quiz answer-key endpoint.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| score | integer | True | False | body | max possible score |
| max_score | integer | True | False | body | strict integer |
| passed | boolean | True | False | body | strict JSON boolean |
| released_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| questions | ReleasedQuestionFeedback[] | True | False | body | Validate referenced schema recursively |

### AssignmentView

AssignmentView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lesson_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| kind | enum(assignment\|project) | True | False | body | Closed enum; reject unknown values |
| due_offset_days | integer | True | True | body | 0–365 |
| max_score | integer | True | False | body | 1–1000 |
| max_files | integer | True | False | body | 1–5 |
| status | enum(draft\|ready) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |
| rubric | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| passing_score | integer | True | False | body | 0–max_score |
| allow_resubmission | boolean | True | False | body | strict JSON boolean |
| closed | boolean | True | False | body | strict JSON boolean |
| due_at | datetime | True | True | body | Resolved cohort-relative due time in learner context |

### SubmissionView

Immutable submitted version; returning permits new attempt linked to previous, not overwriting evidence.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| attempt_number | integer | True | False | body | >=1 |
| body | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| files | FileAssetView[] | True | False | body | Validate referenced schema recursively |
| status | enum(draft\|submitted\|returned\|assessed) | True | False | body | Closed enum; reject unknown values |
| submitted_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |
| late | boolean | True | False | body | strict JSON boolean |

### AssessmentView

Learner endpoint returns only released record; withdrawn becomes unavailable, retaining audit.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| score | integer | True | True | body | strict integer |
| max_score | integer | True | False | body | strict integer |
| rubric_comment | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(draft\|released\|withdrawn) | True | False | body | Closed enum; reject unknown values |
| released_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### FeedbackView

FeedbackView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(draft\|released\|withdrawn) | True | False | body | Closed enum; reject unknown values |
| released_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### ProgressView

Derived source counts remain unchanged. Eligibility is standard policy OR active evidenced education-admin override; private override evidence is never learner/parent projected.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lessons_completed | integer | True | False | body | strict integer |
| lessons_required | integer | True | False | body | strict integer |
| assignments_passed | integer | True | False | body | strict integer |
| assignments_required | integer | True | False | body | strict integer |
| quizzes_passed | integer | True | False | body | strict integer |
| quizzes_required | integer | True | False | body | strict integer |
| completion_percent | integer | True | False | body | 0–100 |
| status | enum(not_started\|in_progress\|complete) | True | False | body | Closed enum; reject unknown values |
| updated_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| delivered_sessions | integer | True | False | body | strict integer |
| attended_sessions | integer | True | False | body | strict integer |
| attendance_percent | integer | True | False | body | 0–100 |
| completion_eligible | boolean | True | False | body | strict JSON boolean |
| completion_basis | enum(incomplete\|standard\|admin_override) | True | False | body | Closed enum; reject unknown values |

### CertificateView

No public directory or searchable child names. Download separately authorized.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| issued_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| status | enum(pending\|issued\|revoked) | True | False | body | Closed enum; reject unknown values |
| verification_code | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| asset_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### PriceView

Admin-approved tax configuration required before checkout. Snapshot immutable on Payment.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| tax_treatment | enum(inclusive\|exclusive\|exempt) | True | False | body | Closed enum; reject unknown values |
| tax_rate_basis_points | integer | True | False | body | 0–10000 |
| label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### PriceConfigView

PriceConfigView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| price | PriceView | True | False | body | Validate referenced schema recursively |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### CheckoutSessionView

Server-generated Stripe hosted checkout URL; redirect does not activate enrolment.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| checkout_url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| price | PriceView | True | False | body | Validate referenced schema recursively |

### PaymentView

Parent-safe projection; excludes Stripe customer/payment-method metadata and integration raw payload.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| status | enum(pending\|succeeded\|failed\|expired\|partially_refunded\|refunded\|exception) | True | False | body | Closed enum; reject unknown values |
| paid_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| refunded_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| receipt_available | boolean | True | False | body | strict JSON boolean |

### AdminPaymentView

Finance privilege only; no card data or sensitive webhook raw payload.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment | PaymentView | True | False | body | Validate referenced schema recursively |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| provider_payment_id | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| provider_checkout_id | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reconciliation_status | enum(unreconciled\|matched\|exception) | True | False | body | Closed enum; reject unknown values |
| exception_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| version | version | True | False | body | positive integer optimistic concurrency token |

### ReceiptView

Legal content approved before billing live; short-lived authorized document URL.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| document_type | enum(receipt\|invoice) | True | False | body | Closed enum; reject unknown values |
| number | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| issued_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| seller_legal_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| seller_abn | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| purchaser_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| line_description | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| tax_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| download_url | url | True | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |

### RefundView

RefundView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| amount_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| access_disposition | enum(KEEP\|CANCEL) | True | False | body | Closed enum; reject unknown values |
| status | enum(requested\|processing\|succeeded\|failed) | True | False | body | Closed enum; reject unknown values |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### FinanceReportView

Bounded 366-day range; cash ledger reporting, not unapproved accounting/tax engine.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| from | date | True | False | body | ISO8601 calendar date |
| to | date | True | False | body | ISO8601 calendar date |
| currency | enum(AUD) | True | False | body | Closed enum; reject unknown values |
| gross_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| refund_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| net_minor | money | True | False | body | integer minor units, nonnegative AUD; no floating point |
| succeeded_count | integer | True | False | body | strict integer |
| exception_count | integer | True | False | body | strict integer |

### EventView

EventView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| description | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | True | False | body | valid IANA timezone |
| audience | Audience | True | False | body | Type validation; no unknown fields |
| status | enum(draft\|published\|cancelled) | True | False | body | Closed enum; reject unknown values |
| version | version | True | False | body | positive integer optimistic concurrency token |

### Audience

Discriminated target: public has empty roles and null IDs; role has nonempty role allowlist and null IDs; course has course_id only; cohort has cohort_id only. Course/cohort recipients must have current educational relation and be in role filter. Global student role announcements permitted only approved operational education notice, never marketing. Public announcements contain no private relations.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| kind | enum(public\|role\|course\|cohort) | True | False | body | Closed enum; reject unknown values |
| roles | enum(parent\|student\|teacher)[] | True | False | body | Nonempty except public; optional audience roles are explicit inclusion filter |
| course_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### AnnouncementView

AnnouncementView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| status | enum(draft\|published\|withdrawn) | True | False | body | Closed enum; reject unknown values |
| published_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### NotificationView

Only principal-owned recipient; no teacher payment notification.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | enum(account\|enrolment\|payment\|class\|assignment\|feedback\|certificate\|operations) | True | False | body | Closed enum; reject unknown values |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| portal_path | string | True | False | body | Allowlisted same-origin route |
| read_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### FileAssetView

Object keys and bucket credentials never returned.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| filename | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| media_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| size_bytes | integer | True | False | body | strict integer |
| purpose | enum(resource\|submission\|certificate\|internal\|public_asset) | True | False | body | Closed enum; reject unknown values |
| status | enum(quarantined\|scanning\|ready\|rejected\|deleted) | True | False | body | Closed enum; reject unknown values |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### UploadTicketView

Unique staging key; presigned 5-minute validity; cannot overwrite final key.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| asset_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| upload_url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| method | enum(PUT) | True | False | body | Closed enum; reject unknown values |
| required_headers | UploadHeaders | True | False | body | Type validation; no unknown fields |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| max_size_bytes | integer | True | False | body | strict integer |

### UploadHeaders

UploadHeaders

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| content_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| checksum_sha256 | string | True | False | body | base64 SHA256 checksum; provider-independent required-header names serialized by API |

### DownloadTicketView

Presigned GET valid <=60 seconds; permission rechecked each issuance.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| url | url | True | False | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| filename | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| media_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### SettingView

Never returns credential value; public config uses separate schema.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| key | enum(child_age_min\|child_age_max\|approved_child_interests\|support_email\|safeguarding_email\|business_phone\|policy_privacy_id\|policy_terms_id\|policy_child_safety_id\|required_consent_policy_ids\|retention_matrix_version\|retention_child_months\|retention_contact_days\|retention_delivery_days\|retention_finance_years\|retention_certificate_years\|merchant_legal_name\|merchant_abn\|merchant_address\|tax_treatment\|tax_rate_basis_points\|refund_policy_id\|zoom_host_assignments\|google_calendar_id\|email_from_address\|approved_video_hosts\|enrolment_enabled\|public_publication_enabled\|retention_purge_enabled) | True | False | body | Closed key catalog in SETTINGS_CATALOG |
| value | SettingValue | True | False | body | Type validation; no unknown fields |
| approved | boolean | True | False | body | strict JSON boolean |
| version | version | True | False | body | positive integer optimistic concurrency token |

### SettingValue

Exactly one value field according to approved key schema; no arbitrary secrets.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| text | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| number | integer | False | False | body | strict integer |
| flag | boolean | False | False | body | strict JSON boolean |
| items | string[] | False | False | body | Validate referenced schema recursively |

### IntegrationStatusView

Masked reference only; configuration cannot accept executable endpoint URLs.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| provider | enum(stripe\|zoom\|calendar\|resend\|storage) | True | False | body | Closed enum; reject unknown values |
| configured | boolean | True | False | body | strict JSON boolean |
| enabled | boolean | True | False | body | strict JSON boolean |
| last_success_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| failure_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| secret_version_label | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### JobView

Safe error codes; no payload or PII.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| status | enum(queued\|running\|succeeded\|failed\|dead_letter) | True | False | body | Closed enum; reject unknown values |
| attempts | integer | True | False | body | strict integer |
| last_error_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| next_attempt_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |

### AuditView

Redacted purpose-bound audit view; no passwords, tokens, secret URLs or full child content.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| actor_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| action | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| resource_type | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| resource_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| occurred_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| outcome | enum(allowed\|denied\|failed) | True | False | body | Closed enum; reject unknown values |
| request_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| reason | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### DashboardView

Role-specific safe counts. Admin uses privilege-specific dashboard parts, never all-data dump.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| upcoming_count | integer | True | False | body | strict integer |
| unread_notifications | integer | True | False | body | strict integer |
| pending_actions | DashboardAction[] | True | False | body | Validate referenced schema recursively |

### DashboardAction

Allowed kinds filtered by role; teacher/student cannot receive payment.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| kind | enum(class\|assignment\|payment\|review\|operations) | True | False | body | Closed enum; reject unknown values |
| count | integer | True | False | body | strict integer |
| portal_path | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### OperationsSummaryView

Operations-admin only; no finance sums.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| failed_jobs | integer | True | False | body | strict integer |
| unsynced_sessions | integer | True | False | body | strict integer |
| quarantined_files | integer | True | False | body | strict integer |
| unconfigured_launch_settings | integer | True | False | body | strict integer |

### DeliveryView

Operations-admin; recipient email masked.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| notification_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| channel | enum(in_app\|email) | True | False | body | Closed enum; reject unknown values |
| status | enum(queued\|sent\|failed\|suppressed) | True | False | body | Closed enum; reject unknown values |
| attempt_count | integer | True | False | body | strict integer |
| sent_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| last_error_code | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### ExportView

Family privacy export excludes third-party and staff-private content; generated file separately protected.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(requested\|processing\|ready\|expired) | True | False | body | Closed enum; reject unknown values |
| expires_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |

### API_AUTH_REGISTERRequest

Register guardian and create family input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| policy_ids | uuid[] | True | False | body | All required current policy versions |

### API_AUTH_VERIFYRequest

Consume single-use email verification input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |

### API_AUTH_RESENDRequest

Resend verification without account enumeration input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |

### API_AUTH_LOGINRequest

Authenticate parent/staff/student input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| identifier | string | True | False | body | Email for adult/staff or opaque student username |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

### API_AUTH_MFARequest

Complete staff MFA challenge input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| challenge_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| code | string | True | False | body | 6-digit TOTP or unused recovery code |

### MfaSetupView

MfaSetupView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| setup_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| otpauth_uri | string | True | False | body | TOTP provisioning URI shown once over HTTPS |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### API_AUTH_MFA_ENROLRequest

Create pending TOTP enrolment input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| setup_token | token | False | False | body | Required for limited invited staff setup context; forbidden with unrelated full session |

### RecoveryCodeView

RecoveryCodeView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| recovery_codes | string[] | True | False | body | 10 cryptographically random single-use codes shown once |

### API_AUTH_MFA_CONFIRMRequest

Activate TOTP and issue recovery codes once input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| setup_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| code | string | True | False | body | 6 digits |

### API_AUTH_RESET_REQUESTRequest

Request account recovery input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |

### API_AUTH_RESETRequest

Reset adult password and revoke sessions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| new_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

### API_AUTH_MERequest

Get safe authenticated session identity input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_AUTH_LOGOUTRequest

Revoke current session input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_ACCOUNT_PASSWORDRequest

Change own adult/staff password and revoke other sessions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| current_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| new_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ACCOUNT_SESSIONSRequest

List own devices input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### DeviceSessionViewPage

DeviceSessionViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | DeviceSessionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ACCOUNT_REVOKERequest

Revoke selected own device input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ACCOUNT_PROFILERequest

Read own profile input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_FAMILY_GETRequest

Read own family and linked students input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_PARENT_PROFILERequest

Read guardian contact/preferences input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_PARENT_UPDATERequest

Update guardian contact/preferences input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| first_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| phone | string | False | True | body | E164, nullable |
| optional_email | boolean | False | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_PARENT_EMAIL_CHANGERequest

Begin verified contact email change input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| new_email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

### API_PARENT_EMAIL_CONFIRMRequest

Confirm new email and notify old address input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |

### API_STUDENT_CREATERequest

Register child with required name and age input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| first_name | string | True | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | True | False | body | 4–18 |
| preferred_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| school_name | string | False | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | False | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | False | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | False | True | body | Optional closed educational-experience enum |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_STUDENT_GETRequest

Read linked child profile input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_STUDENT_UPDATERequest

Update optional child information input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| first_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| school_name | string | False | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| school_year | enum(foundation\|year_1\|year_2\|year_3\|year_4\|year_5\|year_6\|year_7\|year_8\|year_9\|year_10\|year_11\|year_12\|other\|not_specified) | False | True | body | Closed school-year catalog; nullable and optional at registration |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | False | False | body | 0–10 unique approved topics; closed catalog; optional at registration |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | False | True | body | Optional closed educational-experience enum |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STUDENT_AGERequest

Reconfirm required age input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| age_years | integer | True | False | body | 4–18;recorded date set by server |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STUDENT_CREDENTIALSRequest

Provision or rotate child login input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| guardian_password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_STUDENT_SELFRequest

Read own limited profile input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_STUDENT_PREFERREDRequest

Change own preferred display name input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| preferred_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| interests | enum(artificial_intelligence\|coding\|robotics\|creative_design\|games\|data\|online_safety)[] | False | False | body | 0–10 unique |
| prior_experience | enum(none\|some\|experienced\|prefer-not-to-say) | False | True | body | Closed enum; reject unknown values |

### API_POLICY_LISTRequest

Read published policy versions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PolicyViewPage

PolicyViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PolicyView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_CONSENT_LISTRequest

Read family acknowledgement evidence input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### AcknowledgementViewPage

AcknowledgementViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | AcknowledgementView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_CONSENT_ACKRequest

Record current policy acknowledgement input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| policy_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | False | True | body | Linked child scope where policy requires |

### API_PUBLIC_PAGERequest

Read get page input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| slug | string | True | False | path | Known allowlisted key |

### API_PUBLIC_PROGRAMSRequest

Read list programs input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PublicProgramViewPage

PublicProgramViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PublicProgramView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PUBLIC_COURSESRequest

Read list courses input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PublicCourseViewPage

PublicCourseViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PublicCourseView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PUBLIC_COURSERequest

Read get course input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| slug | string | True | False | path | Known allowlisted key |

### API_PUBLIC_COHORTSRequest

Read list public cohorts input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PublicCohortViewPage

PublicCohortViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PublicCohortView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PUBLIC_TEACHERSRequest

Read list public teachers input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PublicTeacherViewPage

PublicTeacherViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PublicTeacherView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PUBLIC_CONTACTRequest

Submit contact enquiry to operations queue input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| message | text | True | False | body | 20–2000 |
| captcha_token | token | False | False | body | opaque cryptographic token; max 512 characters; never logged |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_PROGRAM_LISTRequest

List draft and published programs input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ProgramViewPage

ProgramViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ProgramView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_PROGRAM_CREATERequest

Create offering grouping input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| slug | string | True | False | body | lowercase URL slug 3–80, unique |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_PROGRAM_UPDATERequest

Edit offering grouping input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| program_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_PROGRAM_STATUSRequest

Publish or archive program input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| program_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(published\|archived) | True | False | body | Closed enum; reject unknown values |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_COURSESRequest

List all curriculum courses input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(draft\|published\|archived) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### CourseViewPage

CourseViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | CourseView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_COURSERequest

Read administrative course details input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_COURSE_CREATERequest

Create reusable course input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| program_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| slug | string | True | False | body | unique lowercase slug 3–80 |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | True | False | body | 1–30 |
| min_age | integer | True | False | body | 4–18 |
| max_age | integer | True | False | body | >= min_age, <=18 |
| duration_weeks | integer | True | False | body | 1–52 |
| delivery_method | enum(live_online) | True | False | body | Closed enum; reject unknown values |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_COURSE_UPDATERequest

Edit course marketing metadata input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| program_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| summary | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| learning_outcomes | string[] | False | False | body | Validate referenced schema recursively |
| min_age | integer | False | False | body | 4–18 |
| max_age | integer | False | False | body | >= min_age, <=18 |
| duration_weeks | integer | False | False | body | 1–52 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_COURSE_PUBLISHRequest

Publish approved course with ready revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_COURSE_ARCHIVERequest

Archive course acquisition; preserve existing learning access input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_REVISION_LISTRequest

List curriculum revisions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### CurriculumRevisionViewPage

CurriculumRevisionViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | CurriculumRevisionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_REVISION_CREATERequest

Create draft revision optionally copied from same course input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| source_revision_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_REVISION_GETRequest

Read full authoring hierarchy input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_REVISION_PUBLISHRequest

Freeze validated curriculum revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_MODULE_CREATERequest

Create draft module input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | >=0 |
| release_offset_days | integer | True | False | body | 0–365 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_MODULE_UPDATERequest

Edit draft module input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| module_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | False | False | body | >=0 |
| release_offset_days | integer | False | False | body | 0–365 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_MODULE_DELETERequest

Remove unreferenced draft module input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| module_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_LESSON_CREATERequest

Create draft lesson input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| module_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | True | False | body | >=0 |
| release_offset_days | integer | True | False | body | 0–365 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

### API_ADMIN_LESSON_UPDATERequest

Edit draft lesson input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| position | integer | False | False | body | >=0 |
| release_offset_days | integer | False | False | body | 0–365 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| required_for_completion | boolean | False | False | body | strict JSON boolean |

### API_ADMIN_LESSON_DELETERequest

Remove unreferenced draft lesson input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_BLOCK_CREATERequest

Create draft block input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| kind | enum(heading\|rich_text\|image\|video\|download\|activity\|quiz\|assignment) | True | False | body | Closed enum; reject unknown values |
| position | integer | True | False | body | >=0 |
| content | LessonBlockContent | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| required_for_completion | boolean | True | False | body | strict JSON boolean |

### API_ADMIN_BLOCK_UPDATERequest

Edit draft block input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| block_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| position | integer | False | False | body | >=0 |
| content | LessonBlockContent | False | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| required_for_completion | boolean | False | False | body | strict JSON boolean |

### API_ADMIN_BLOCK_DELETERequest

Remove unreferenced draft block input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| block_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_RESOURCE_CREATERequest

Create draft resource input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| kind | enum(document\|image\|video\|project) | True | False | body | Closed enum; reject unknown values |
| asset_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| external_url | url | False | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_RESOURCE_UPDATERequest

Edit draft resource input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| resource_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| asset_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| external_url | url | False | True | body | HTTPS URL; approved provider/storage host allowlist; no credentials |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_RESOURCE_DELETERequest

Remove unreferenced draft resource input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| resource_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_RESOURCE_LISTRequest

List teaching assets in revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ResourceViewPage

ResourceViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ResourceView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_LESSON_GETRequest

Read authoring lesson and all block fields input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_STUDENT_ENROLMENTSRequest

List own enrolled courses input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### EnrolmentViewPage

EnrolmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | EnrolmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PARENT_ENROLMENTSRequest

List linked child enrolment status input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_CURRICULUMRequest

Read released modules of pinned revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_STUDENT_LESSONRequest

Read released lesson and safe blocks input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_STUDENT_RESOURCERequest

List released learning resources input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_COURSESRequest

List assigned courses input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_COHORTSRequest

List assigned cohorts input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### CohortViewPage

CohortViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | CohortView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_TEACHER_CURRICULUMRequest

Read pinned teaching curriculum including planned lessons input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_TEACHER_LESSONRequest

Read assigned teaching lesson plan input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_TEACHER_RESOURCESRequest

Read assigned teaching resources input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_STUDENTSRequest

Read assigned roster educational fields input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### TeachingStudentViewPage

TeachingStudentViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | TeachingStudentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_TEACHER_STUDENTRequest

Read assigned learner educational profile input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_PARENTSRequest

Read authorized list parents input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| query | string | False | False | query | 1–100 exact/limited contact search |
| status | enum(active\|suspended\|closed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### GuardianViewPage

GuardianViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | GuardianView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_FAMILYRequest

Read authorized get family input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| family_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_STUDENTSRequest

Read authorized list students input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| family_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| query | string | False | False | query | 1–100 |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### StudentProfileViewPage

StudentProfileViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | StudentProfileView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_STUDENTRequest

Read authorized get student input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_TEACHERSRequest

Read authorized list teachers input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(invited\|active\|suspended\|archived) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### TeacherViewPage

TeacherViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | TeacherView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_TEACHERRequest

Read authorized get teacher input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_GUARDIAN_LINKRequest

Link verified guardian to same family child input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| guardian_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| verification_reference | string | True | False | body | Audited external evidence ID, no sensitive document body |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_GUARDIAN_REVOKERequest

Revoke guardian child access input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| guardian_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_STUDENT_UPDATERequest

Correct student data with reason input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| first_name | string | False | False | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| preferred_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| last_name | string | False | True | body | Trimmed Unicode1–80 characters; optional blank normalizes null; no markup |
| age_years | integer | False | False | body | 4–18 |
| school_name | string | False | True | body | Optional trimmed Unicode1–160 characters; blank normalizes null; never required |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_STUDENT_ARCHIVERequest

Archive child after active obligations resolved input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_INVITERequest

Invite teacher or constrained admin principal input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| display_name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| role | enum(teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| admin_privileges | string[] | False | False | body | Closed list identity_admin,education_admin,finance_admin,operations_admin,audit_admin; incompatible teacher grants forbidden |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_AUTH_INVITE_ACCEPTRequest

Accept staff invitation and require MFA setup input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |

### API_ADMIN_ROLERequest

Read constrained role grants input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| account_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_ROLE_UPDATERequest

Change admin privileges with audit and session revocation input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| account_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| role | enum(parent\|student\|teacher\|admin) | True | False | body | Closed enum; reject unknown values |
| admin_privileges | string[] | True | False | body | Closed list identity_admin,education_admin,finance_admin,operations_admin,audit_admin; incompatible teacher grants forbidden |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ACCOUNT_STATUSRequest

Suspend or reactivate account and revoke affected sessions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| account_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(active\|suspended) | True | False | body | Closed enum; reject unknown values |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_TEACHER_UPDATERequest

Edit teacher public biography/profile input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| display_name | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| biography | text | False | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| public_photo_asset_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_TEACHER_PUBLISHRequest

Publish or withdraw explicitly approved instructor profile input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| published | boolean | True | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_TEACHER_ARCHIVERequest

Archive teacher after assignment reassignment input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| teacher_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_PROFILERequest

Read own teacher profile input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_ADMIN_COHORTSRequest

List operational cohorts input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(draft\|open\|closed\|in_progress\|completed\|cancelled) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_COHORTRequest

Read cohort operational details input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_COHORT_CREATERequest

Create course delivery pinned to published revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| revision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| capacity | integer | True | False | body | 1–100 |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | > starts_at |
| timezone | timezone | True | False | body | valid IANA timezone |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | >opens and <=starts |

### API_ADMIN_COHORT_UPDATERequest

Edit future cohort metadata and safe capacity input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| capacity | integer | False | False | body | >= active enrolments plus live holds |
| starts_at | datetime | False | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | False | False | body | RFC3339 timezone-aware instant, UTC persisted |
| timezone | timezone | False | False | body | valid IANA timezone |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| enrolment_opens_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| enrolment_closes_at | datetime | True | False | body | >opens and <=starts |

### API_ADMIN_COHORT_STATUSRequest

Open, close, start or complete delivery input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(open\|closed\|in_progress\|completed) | True | False | body | Closed enum; reject unknown values |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_COHORT_CANCELRequest

Cancel delivery and create refund review tasks input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ASSIGNMENTSRequest

List cohort teaching grants input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### TeacherAssignmentViewPage

TeacherAssignmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | TeacherAssignmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_ASSIGNMENT_CREATERequest

Assign active teacher to cohort/session input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| teacher_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| session_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| role | enum(lead\|assistant) | True | False | body | Closed enum; reject unknown values |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | False | True | body | RFC3339 timezone-aware instant, UTC persisted |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_ASSIGNMENT_REVOKERequest

Revoke teaching access immediately input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_SESSIONSRequest

List all delivery sessions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ClassSessionViewPage

ClassSessionViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ClassSessionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_SESSION_CREATERequest

Schedule one class occurrence input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | Must resolve chosen DST occurrence |
| duration_minutes | integer | True | False | body | 15–240 |
| lesson_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_RECURRENCERequest

Materialize bounded weekly occurrences transactionally input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| first_local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | strict integer |
| duration_minutes | integer | True | False | body | 15–240 |
| occurrences | integer | True | False | body | 1–52 |
| interval_weeks | integer | True | False | body | 1–4 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_SESSION_UPDATERequest

Edit session title/lesson without rescheduling input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| lesson_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_PARENT_SCHEDULERequest

List parent authorized upcoming classes input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | > from, <=93 day range |
| student_id | uuid | False | False | query | parent only; forbidden for student/teacher |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_PARENT_SESSIONRequest

Read authorized class session details input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_STUDENT_SCHEDULERequest

List student authorized upcoming classes input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | > from, <=93 day range |
| student_id | uuid | False | False | query | parent only; forbidden for student/teacher |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_SESSIONRequest

Read authorized class session details input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_TEACHER_SCHEDULERequest

List teacher authorized upcoming classes input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | > from, <=93 day range |
| student_id | uuid | False | False | query | parent only; forbidden for student/teacher |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_SESSIONRequest

Read authorized class session details input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_TEACHER_RESCHEDULERequest

Reschedule authorized session and queue provider updates input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | strict integer |
| duration_minutes | integer | True | False | body | 15–240 |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_RESCHEDULERequest

Reschedule authorized session and queue provider updates input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| local_start | string | True | False | body | ISO local datetime |
| timezone | timezone | True | False | body | valid IANA timezone |
| utc_offset_minutes | integer | True | False | body | strict integer |
| duration_minutes | integer | True | False | body | 15–240 |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_SESSION_CANCELRequest

Cancel class and queue Zoom/calendar cancellation and notices input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_SESSION_COMPLETERequest

Complete past session after attendance review input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_STARTRequest

Fetch fresh authorized Zoom host handoff input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_STUDENT_JOINRequest

Fetch eligible learner Zoom join handoff input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_PARENT_JOINRequest

Fetch eligible learner Zoom join handoff input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### API_ADMIN_ENROLMENTSRequest

List delivery enrolments without financial fields input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(held\|pending_payment\|active\|cancelled\|completed\|expired\|payment_exception) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_ENROLMENTRequest

Read educational enrolment status input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_ENROLMENT_CANCELRequest

Cancel educational access with auditable reason input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| access_ends_at | datetime | False | True | body | RFC3339 timezone-aware instant, UTC persisted |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_PARENT_CHECKOUT_CANCELRequest

Release own unpaid hold input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_ATTENDANCERequest

Read authorized session attendance roster input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### AttendanceViewPage

AttendanceViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | AttendanceView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_TEACHER_ATTENDANCE_RECORDRequest

Record or amend attendance input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(present\|absent\|late\|excused) | True | False | body | Closed enum; reject unknown values |
| minutes_attended | integer | False | True | body | 0–240 |
| reason | string | True | False | body | Required change reason; no diagnoses or sensitive notes |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ATTENDANCERequest

Read authorized session attendance roster input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_ATTENDANCE_RECORDRequest

Record or amend attendance input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| session_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(present\|absent\|late\|excused) | True | False | body | Closed enum; reject unknown values |
| minutes_attended | integer | False | True | body | 0–240 |
| reason | string | True | False | body | Required change reason; no diagnoses or sensitive notes |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_PARENT_ATTENDANCERequest

Read own or linked child attendance input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_ATTENDANCERequest

Read own or linked child attendance input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_QUIZZESRequest

List quiz authoring definitions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### QuizViewPage

QuizViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | QuizView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_QUIZRequest

Read quiz questions and grading keys input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_QUIZ_CREATERequest

Create draft formative quiz input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| pass_percent | integer | True | False | body | 0–100, default70 |
| max_attempts | integer | True | False | body | 1–5, default3 |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_QUIZ_UPDATERequest

Edit draft quiz rules input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| pass_percent | integer | False | False | body | 0–100 |
| max_attempts | integer | False | False | body | 1–5 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_QUESTION_PUTRequest

Replace ordered draft questions atomically input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| questions | QuizQuestionView[] | True | False | body | 1–100; all correct option IDs reference that question; unique IDs and positions |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_QUIZ_DELETERequest

Delete unreferenced draft quiz input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STUDENT_QUIZRequest

Read released quiz without answer key input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_STUDENT_ATTEMPTSRequest

Read own attempt history input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### QuizAttemptViewPage

QuizAttemptViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | QuizAttemptView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_STUDENT_ATTEMPT_CREATERequest

Start attempt with immutable quiz snapshot input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| quiz_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_STUDENT_ATTEMPT_SAVERequest

Save selections on own in-progress attempt input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| attempt_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| answers | QuizAnswer[] | True | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STUDENT_ATTEMPT_SUBMITRequest

Submit once and release formative score input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| attempt_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| answers | QuizAnswer[] | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_TEACHER_QUIZ_RESULTSRequest

Read assigned learners submitted quiz scores input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_QUIZ_RESULTSRequest

Oversee submitted quiz outcomes input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_PARENT_QUIZ_RESULTSRequest

Read released child quiz results input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_ASSIGNMENTS_LISTRequest

List assignment/project authoring definitions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| revision_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### AssignmentViewPage

AssignmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | AssignmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_ASSIGNMENT_GETRequest

Read assignment authoring detail input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_ASSIGNMENT_DEFINERequest

Create assignment or project definition input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| kind | enum(assignment\|project) | True | False | body | Closed enum; reject unknown values |
| due_offset_days | integer | False | True | body | 0–365 |
| max_score | integer | True | False | body | 1–1000 |
| max_files | integer | True | False | body | 1–5 |
| rubric | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| passing_score | integer | True | False | body | 0–max_score |
| allow_resubmission | boolean | True | False | body | strict JSON boolean |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_ASSIGNMENT_EDITRequest

Edit draft assignment definition input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | False | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| instructions | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| due_offset_days | integer | False | True | body | 0–365 |
| max_score | integer | False | False | body | 1–1000 |
| rubric | text | False | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| passing_score | integer | False | False | body | 0–max_score |
| allow_resubmission | boolean | False | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ASSIGNMENT_DELETERequest

Delete unreferenced draft assignment input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STUDENT_ASSIGNMENTSRequest

Read permitted assignment and project work input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_PARENT_ASSIGNMENTSRequest

Read permitted assignment and project work input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_ASSIGNMENTSRequest

Read permitted assignment and project work input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_SUBMISSIONSRequest

Read own immutable submission history input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### SubmissionViewPage

SubmissionViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | SubmissionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_STUDENT_SUBMISSION_CREATERequest

Start own assignment submission/revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| previous_submission_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_STUDENT_SUBMISSION_SAVERequest

Save own draft work and ready scanned file links input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| body | text | False | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| asset_ids | uuid[] | True | False | body | 0–5; own ready submission-purpose assets only |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STUDENT_SUBMISSION_SENDRequest

Freeze own work and enqueue assessment notice input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_STUDENT_SUBMISSION_DELETERequest

Discard own unsubmitted draft input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_PARENT_SUBMISSIONSRequest

Read child submission status/history input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| assignment_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_SUBMISSIONSRequest

Read authorized submitted work review queue input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(submitted\|returned\|assessed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_SUBMISSIONRequest

Read authorized frozen work version input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_TEACHER_RETURNRequest

Return work for a new immutable revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | text | True | False | body | 1–2000 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_ASSESSMENTRequest

Save draft marking against frozen submission input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| score | integer | True | False | body | 0–assignment max_score |
| rubric_comment | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_ASSESSMENT_GETRequest

Read permitted draft/released marking input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_TEACHER_ASSESSMENT_RELEASERequest

Release validated assessment to learner and guardian input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_ASSESSMENT_WITHDRAWRequest

Withdraw erroneous release and preserve correction history input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_FEEDBACK_LISTRequest

Read permitted feedback drafts/releases input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### FeedbackViewPage

FeedbackViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | FeedbackView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_TEACHER_FEEDBACK_CREATERequest

Create draft educational feedback input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_TEACHER_FEEDBACK_UPDATERequest

Revise draft feedback; released content requires withdrawal first input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_FEEDBACK_RELEASERequest

Release educational feedback and notify input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_FEEDBACK_WITHDRAWRequest

Withdraw mistaken feedback release with reason input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_TEACHER_PROGRESSRequest

Read permitted learner completion evidence input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ProgressViewPage

ProgressViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ProgressView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_SUBMISSIONSRequest

Read authorized submitted work review queue input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(submitted\|returned\|assessed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_SUBMISSIONRequest

Read authorized frozen work version input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_RETURNRequest

Return work for a new immutable revision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | text | True | False | body | 1–2000 |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ASSESSMENTRequest

Save draft marking against frozen submission input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| score | integer | True | False | body | 0–assignment max_score |
| rubric_comment | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ASSESSMENT_GETRequest

Read permitted draft/released marking input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| submission_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_ASSESSMENT_RELEASERequest

Release validated assessment to learner and guardian input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ASSESSMENT_WITHDRAWRequest

Withdraw erroneous release and preserve correction history input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assessment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_FEEDBACK_LISTRequest

Read permitted feedback drafts/releases input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_FEEDBACK_CREATERequest

Create draft educational feedback input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| submission_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_FEEDBACK_UPDATERequest

Revise draft feedback; released content requires withdrawal first input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_FEEDBACK_RELEASERequest

Release educational feedback and notify input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_FEEDBACK_WITHDRAWRequest

Withdraw mistaken feedback release with reason input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| feedback_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_PROGRESSRequest

Read permitted learner completion evidence input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_ASSESSMENTSRequest

Read own/linked child released assessments input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### AssessmentViewPage

AssessmentViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | AssessmentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_STUDENT_FEEDBACKRequest

Read own/linked child released feedback input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_PROGRESSRequest

Read own/linked child released progress input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_CERTIFICATESRequest

Read own/linked child released certificates input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### CertificateViewPage

CertificateViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | CertificateView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PARENT_ASSESSMENTSRequest

Read own/linked child released assessments input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_PARENT_FEEDBACKRequest

Read own/linked child released feedback input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_PARENT_PROGRESSRequest

Read own/linked child released progress input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_PARENT_CERTIFICATESRequest

Read own/linked child released certificates input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ActivityCompletionView

ActivityCompletionView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| lesson_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| block_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| completed | boolean | True | False | body | strict JSON boolean |
| reflection | text | True | True | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| completed_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### API_STUDENT_ACTIVITY_GETRequest

Read own activity/reflection status input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| lesson_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ActivityCompletionViewPage

ActivityCompletionViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ActivityCompletionView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_STUDENT_ACTIVITYRequest

Record own non-graded activity and reflection input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| block_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| completed | boolean | True | False | body | strict JSON boolean |
| reflection | text | False | True | body | max2000, optional; no sensitive data prompts |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STUDENT_LESSON_COMPLETERequest

Record own lesson acknowledgement input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| lesson_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| completed | boolean | True | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_COMPLETION_REVIEWRequest

Recompute and record completion decision from evidence input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| decision | enum(RECOMPUTE\|GRANT_OVERRIDE\|REVOKE_OVERRIDE) | True | False | body | Closed enum; reject unknown values |
| evidence_references | string[] | False | False | body | 1–10 nonempty verified evidence references required iff GRANT_OVERRIDE; forbidden for RECOMPUTE |
| override_id | uuid | False | False | body | Required iff REVOKE_OVERRIDE |

### API_ADMIN_CERTIFICATESRequest

List certificate issue/revocation state input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_CERTIFICATE_ISSUERequest

Issue completion certificate once from eligible progress input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_CERTIFICATE_REVOKERequest

Revoke incorrect certificate with reason input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| certificate_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_CERTIFICATE_REISSUERequest

Issue replacement linked to revoked certificate input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| certificate_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_PARENT_CHECKOUTRequest

Reserve seat and create server-priced hosted checkout input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| student_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| accepted_policy_ids | uuid[] | True | False | body | Current payment/cancellation policies |
| return_path | string | True | False | body | Allowlisted same-origin path; no arbitrary redirect |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_PARENT_CHECKOUT_RETRYRequest

Retry failed/expired checkout with fresh eligibility and seat check input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| return_path | string | True | False | body | Allowlisted same-origin |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_PARENT_PAYMENTSRequest

Read own family payment history input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(pending\|succeeded\|failed\|expired\|partially_refunded\|refunded\|exception) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PaymentViewPage

PaymentViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PaymentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PARENT_PAYMENTRequest

Read authoritative payment/checkout state input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_PARENT_RECEIPTSRequest

Read own immutable invoice/receipt documents input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ReceiptViewPage

ReceiptViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ReceiptView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_PARENT_REFUNDSRequest

Read own refund outcome input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### RefundViewPage

RefundViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | RefundView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_PRICESRequest

List current and historic fees input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PriceConfigViewPage

PriceConfigViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PriceConfigView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_PRICE_CREATERequest

Create effective dated course default/cohort override fee input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| course_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| cohort_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| price | PriceView | True | False | body | Validate referenced schema recursively |
| active_from | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| active_until | datetime | False | True | body | RFC3339 timezone-aware instant, UTC persisted |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_PRICE_RETIRERequest

End future pricing without changing purchase snapshots input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| price_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| active_until | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### API_ADMIN_PAYMENTSRequest

Inspect financial transactions and exceptions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| family_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(pending\|succeeded\|failed\|expired\|partially_refunded\|refunded\|exception) | False | False | query | Closed enum; reject unknown values |
| from | date | False | False | query | ISO8601 calendar date |
| to | date | False | False | query | ISO8601 calendar date |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### AdminPaymentViewPage

AdminPaymentViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | AdminPaymentView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_PAYMENTRequest

Read payment reconciliation references input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_PAYMENT_RECONCILERequest

Queue server-to-server reconciliation input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### API_ADMIN_DOCUMENTSRequest

Inspect immutable invoices/receipts input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_REFUNDSRequest

Inspect refund ledger input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_REFUND_CREATERequest

Request full/partial refund with explicit entitlement disposition input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| amount_minor | money | True | False | body | >0 and <= captured minus successful/pending refunds |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| access_disposition | enum(KEEP\|CANCEL) | True | False | body | Closed enum; reject unknown values |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_REFUND_RETRYRequest

Retry confirmed failed refund under same provider idempotency key input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| refund_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_REPORTRequest

Read bounded AUD gross/refund/net report input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| from | date | True | False | query | ISO8601 calendar date |
| to | date | True | False | query | <=366 days; >=from |

### API_ADMIN_REPORT_EXPORTRequest

Generate bounded finance CSV export input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| from | date | True | False | body | ISO8601 calendar date |
| to | date | True | False | body | <=366 days |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_PAGESRequest

Read public page drafts input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PublicPageViewPage

PublicPageViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PublicPageView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_PAGE_UPDATERequest

Save allowlisted public-page draft input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| slug | string | True | False | path | Known allowlisted key |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | Sanitize allowlisted semantic tags; scripts/styles/iframes forbidden |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_PAGE_PUBLISHRequest

Publish reviewed public page input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| slug | string | True | False | path | Known allowlisted key |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_POLICIESRequest

Read draft and published legal policies input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_POLICY_CREATERequest

Create immutable policy-version draft input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| key | enum(privacy\|terms\|child_safety\|consent) | True | False | body | Closed enum; reject unknown values |
| version_label | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| sanitized_html | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| requires_acknowledgement | boolean | True | False | body | strict JSON boolean |
| effective_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_POLICY_PUBLISHRequest

Publish policy with human/legal approval evidence input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| policy_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| approval_reference | string | True | False | body | Recorded human approval evidence |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_EVENT_LISTRequest

List event drafts and releases input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### EventViewPage

EventViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | EventView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_EVENT_CREATERequest

Create audience-scoped event input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| description | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | >starts_at |
| timezone | timezone | True | False | body | valid IANA timezone |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_EVENT_UPDATERequest

Revise draft event input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| event_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| description | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| starts_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| ends_at | datetime | True | False | body | >starts_at |
| timezone | timezone | True | False | body | valid IANA timezone |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_EVENT_PUBLISHRequest

Publish event and resolve recipients input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| event_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_EVENT_WITHDRAWRequest

Cancel or withdraw event and notify affected audience input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| event_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_PARENT_EVENTSRequest

Read relevant published events input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_EVENTSRequest

Read relevant published events input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_EVENTSRequest

Read relevant published events input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_ANNOUNCEMENT_LISTRequest

List announcement drafts and releases input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### AnnouncementViewPage

AnnouncementViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | AnnouncementView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_ANNOUNCEMENT_CREATERequest

Create audience-scoped announcement input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_ANNOUNCEMENT_UPDATERequest

Revise draft announcement input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| announcement_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| title | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| body | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| audience | Audience | True | False | body | Validate referenced schema recursively |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ANNOUNCEMENT_PUBLISHRequest

Publish announcement and resolve recipients input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| announcement_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_ANNOUNCEMENT_WITHDRAWRequest

Cancel or withdraw announcement and notify affected audience input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| announcement_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_PARENT_ANNOUNCEMENTSRequest

Read relevant published announcements input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_STUDENT_ANNOUNCEMENTSRequest

Read relevant published announcements input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_TEACHER_ANNOUNCEMENTSRequest

Read relevant published announcements input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_PUBLIC_EVENTSRequest

Read explicitly public upcoming events input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_NOTIFICATIONSRequest

Read own recipient-scoped inbox input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| unread_only | boolean | False | False | query | strict JSON boolean |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### NotificationViewPage

NotificationViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | NotificationView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_NOTIFICATION_READRequest

Mark own notification read input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| notification_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| read | boolean | True | False | body | strict JSON boolean |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_DELIVERIESRequest

Inspect redacted delivery errors input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(queued\|sent\|failed\|suppressed) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### DeliveryViewPage

DeliveryViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | DeliveryView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_DELIVERY_RETRYRequest

Retry failed authorized delivery with deduplication input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| delivery_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_PARENT_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_STUDENT_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_TEACHER_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_ADMIN_DASHBOARDRequest

Read purpose-filtered dashboard counts and next actions input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_FILE_UPLOADRequest

Reserve validated private upload ticket input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| filename | string | True | False | body | basename only,1–200 |
| media_type | string | True | False | body | Allowlisted actual MIME expectation |
| size_bytes | integer | True | False | body | student <=25MiB, staff documents <=50MiB, MP4 <=500MiB |
| checksum_sha256 | string | True | False | body | base64 SHA256 |
| purpose | enum(resource\|submission\|internal\|public_asset) | True | False | body | Closed enum; reject unknown values |
| context_id | uuid | True | False | body | Owning submission or curriculum revision |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_FILE_CONFIRMRequest

Confirm upload and queue independent scanning input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_FILE_GETRequest

Read authorized file scan/metadata state input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_FILE_DOWNLOADRequest

Issue ready-file short-lived download input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_FILE_DELETERequest

Delete eligible unreferenced owned draft asset input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| asset_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_FILESRequest

Browse assets by permitted educational/operations purpose input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| purpose | enum(resource\|submission\|certificate\|internal\|public_asset) | False | False | query | Closed enum; reject unknown values |
| status | enum(quarantined\|scanning\|ready\|rejected\|deleted) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### FileAssetViewPage

FileAssetViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | FileAssetView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### CalendarExport

CalendarExport

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| content | string | True | False | body | RFC5545 text/calendar; UID stable; portal links only, no student name/host URL |
| content_type | enum(text/calendar) | True | False | body | Closed enum; reject unknown values |

### API_PARENT_CALENDARRequest

Export authorized family schedule with portal deep links input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| from | date | True | False | query | ISO8601 calendar date |
| to | date | True | False | query | <=93-day range |
| student_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |

### API_ADMIN_SETTINGSRequest

Read allowlisted non-secret operational settings input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### SettingViewPage

SettingViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | SettingView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_SETTING_PUTRequest

Set validated key with approval evidence for launch-sensitive values input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| key | enum(child_age_min\|child_age_max\|approved_child_interests\|support_email\|safeguarding_email\|business_phone\|policy_privacy_id\|policy_terms_id\|policy_child_safety_id\|required_consent_policy_ids\|retention_matrix_version\|retention_child_months\|retention_contact_days\|retention_delivery_days\|retention_certificate_years\|zoom_host_assignments\|google_calendar_id\|email_from_address\|approved_video_hosts\|enrolment_enabled\|public_publication_enabled\|retention_purge_enabled) | True | False | path | Closed key enum; key-specific type, value bounds and approval gate in SETTINGS_CATALOG |
| value | SettingValue | True | False | body | Validate referenced schema recursively |
| approval_reference | string | False | True | body | Required for age bands, policies, retention |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_FINANCE_SETTINGSRequest

Read merchant identity/tax configuration input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_FINANCE_SETTING_PUTRequest

Set approved merchant/tax/refund policy value input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| key | enum(retention_finance_years\|merchant_legal_name\|merchant_abn\|merchant_address\|tax_treatment\|tax_rate_basis_points\|refund_policy_id) | True | False | path | Closed key enum; key-specific type, value bounds and approval gate in SETTINGS_CATALOG |
| value | SettingValue | True | False | body | Validate referenced schema recursively |
| approval_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_INTEGRATIONSRequest

Read masked provider configuration and synchronization health input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### IntegrationStatusViewPage

IntegrationStatusViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | IntegrationStatusView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_INTEGRATION_UPDATERequest

Enable/disable provider using managed secret reference input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| provider | string | True | False | path | Known allowlisted key |
| enabled | boolean | True | False | body | strict JSON boolean |
| secret_reference | string | True | False | body | Approved secret-manager reference only, not credential bytes |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_INTEGRATION_CHECKRequest

Queue bounded provider connectivity check input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| provider | string | True | False | path | Known allowlisted key |

### API_ADMIN_INTEGRATION_RESYNCRequest

Queue provider mirror reconciliation input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| provider | string | True | False | path | Known allowlisted key |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### API_ADMIN_JOBSRequest

Read redacted job processing state input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(queued\|running\|succeeded\|failed\|dead_letter) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### JobViewPage

JobViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | JobView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_JOBRequest

Read authorized background operation status input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| job_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_JOB_RETRYRequest

Retry dead-letter job after cause correction input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| job_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_OPERATIONSRequest

Read actionable operational summary input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |

### API_ADMIN_AUDITRequest

Read filtered redacted audit history input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| actor_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| resource_id | uuid | False | False | query | UUID v4/v7; opaque identifier; ownership checked after parse |
| action | string | False | False | query | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| from | datetime | True | False | query | RFC3339 timezone-aware instant, UTC persisted |
| to | datetime | True | False | query | <=31-day range |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### AuditViewPage

AuditViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | AuditView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### PrivacyRequestView

PrivacyRequestView

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| family_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| kind | enum(access\|correction\|deletion\|closure) | True | False | body | Closed enum; reject unknown values |
| student_id | uuid | True | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| status | enum(requested\|verified\|processing\|completed\|rejected) | True | False | body | Closed enum; reject unknown values |
| decision_reason | string | True | True | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### API_PARENT_PRIVACY_REQUESTRequest

Request family data access/correction/deletion or account closure input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| kind | enum(access\|correction\|deletion\|closure) | True | False | body | Closed enum; reject unknown values |
| student_id | uuid | False | True | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| details | text | True | False | body | 1–2000 |
| password | password | True | False | body | 12–128 characters; breached-password screening; no silent truncation |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_PARENT_PRIVACY_LISTRequest

Read own privacy request state input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### PrivacyRequestViewPage

PrivacyRequestViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | PrivacyRequestView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_PRIVACY_LISTRequest

Read restricted privacy work queue input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(requested\|verified\|processing\|completed\|rejected) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### API_ADMIN_PRIVACY_DECIDERequest

Record verified authority and retention-aware decision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| request_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| decision | enum(approve\|reject) | True | False | body | Closed enum; reject unknown values |
| verification_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |

### API_PARENT_PRIVACY_EXPORTRequest

Get ready verified family export input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| request_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |

### API_ADMIN_LEGAL_HOLDRequest

Set or release audited retention hold input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| resource_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| resource_type | enum(family\|student\|payment\|file) | True | False | body | Closed enum; reject unknown values |
| held | boolean | True | False | body | strict JSON boolean |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| approval_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_STRIPE_WEBHOOKRequest

Validate raw signature and persist deduplicated provider event input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| raw_body | string | True | False | body | Original bytes, <=1MiB |
| stripe_signature | string | True | False | body | Header HMAC timestamp within300s; no JSON reserialization |

### JOB_PAYMENT_PROCESSRequest

Retrieve authoritative provider state and activate paid seat safely input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| inbox_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_PAYMENT_RECONCILERequest

Compare Stripe state with immutable local ledger input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_HOLD_EXPIRERequest

Expire elapsed holds under row lock; release capacity input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cutoff | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### JOB_REFUND_PROCESSRequest

Execute idempotent requested refund and apply explicit access disposition input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| refund_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_DOCUMENT_GENERATERequest

Generate immutable receipt/invoice after verified payment input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_LIVE_CREATERequest

Create provider meeting from authoritative session version input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| expected_version | version | True | False | body | positive integer optimistic concurrency token |

### JOB_LIVE_UPDATERequest

Update/cancel meeting from latest authoritative session state input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| expected_version | version | True | False | body | positive integer optimistic concurrency token |

### JOB_LIVE_RECONCILERequest

Resolve provider drift without overwriting domain schedule input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| binding_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_CALENDAR_SYNCRequest

Upsert/cancel individual business calendar mirror event input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| resource_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| resource_type | enum(session\|event) | True | False | body | Closed enum; reject unknown values |
| expected_version | version | True | False | body | positive integer optimistic concurrency token |

### JOB_CALENDAR_RESYNCRequest

Recover invalid sync token with full mirror reconciliation input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| integration_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_NOTIFICATION_PREPARERequest

Resolve outbox recipients and create deduplicated notices input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| outbox_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_EMAIL_SENDRequest

Deliver transactional email with durable local deduplication input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| delivery_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_REMINDER_SCHEDULERequest

Queue class reminders once per current session version input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| window_start | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| window_end | datetime | True | False | body | <=24h |

### JOB_FILE_SCANRequest

Verify metadata/MIME/archive limits/malware and promote immutable object input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| asset_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_FILE_CLEANRequest

Delete expired unreferenced staging objects after retention/hold checks input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| cutoff | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### JOB_FILE_DELETERequest

Delete eligible private object/version per approved retention decision input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| asset_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| retention_decision_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_PROGRESS_RECOMPUTERequest

Recalculate completion from latest released work and attendance evidence input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enrolment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_CERTIFICATE_RENDERRequest

Render immutable certificate artifact and mark issued after ready storage input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| certificate_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_PRIVACY_PROCESSRequest

Generate protected export or execute approved retention-aware deletion/closure input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| request_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### JOB_RETENTIONRequest

Purge/anonymize only eligible unheld records from approved matrix input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| policy_version | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| cutoff | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### JOB_OUTBOX_DISPATCHRequest

Publish durable intent to queue and recover expired leases input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| batch_size | integer | True | False | body | 1–100 |

### JOB_INTEGRATION_CHECKRequest

Check configured provider and persist masked operational state input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| provider | enum(stripe\|zoom\|calendar\|resend\|storage) | True | False | body | Closed enum; reject unknown values |

### JOB_FINANCE_EXPORTRequest

Write formula-injection-safe CSV to private export storage input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| export_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |

### ChildSubmissionStatusView

Parent support projection; no draft work body or files.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| assignment_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| attempt_number | integer | True | False | body | strict integer |
| status | enum(draft\|submitted\|returned\|assessed) | True | False | body | Closed enum; reject unknown values |
| submitted_at | datetime | True | True | body | RFC3339 timezone-aware instant, UTC persisted |
| late | boolean | True | False | body | strict JSON boolean |

### ChildQuizResultView

Parent only released result; no child draft answers.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| attempt_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| quiz_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| student_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| result | ReleasedQuizResult | True | False | body | Validate referenced schema recursively |

### ChildQuizResultViewPage

ChildQuizResultViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ChildQuizResultView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### ChildSubmissionStatusViewPage

ChildSubmissionStatusViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ChildSubmissionStatusView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_ASSIGNMENT_CLOSERequest

Close/reopen assignment submissions for a delivery input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| assignment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| cohort_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| closed | boolean | True | False | body | strict JSON boolean |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_BILLING_MEMBERRequest

Grant verified adult family billing visibility separately from child links input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| family_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| guardian_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| finance_approval_reference | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| Idempotency-Key | uuid | True | False | header | Principal + operation + key; same body replays result, different body 409 IDEMPOTENCY_CONFLICT; retention 7 days, billing 90 days |

### API_ADMIN_BILLING_MEMBER_REVOKERequest

Revoke adult family financial membership input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| guardian_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| family_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### ContactEnquiryView

Operations only; no child association inferred from enquiry.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| name | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| email | email | True | False | body | normalized verified deliverable address; max 254 characters |
| message | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
| status | enum(new\|handled) | True | False | body | Closed enum; reject unknown values |
| created_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |
| version | version | True | False | body | positive integer optimistic concurrency token |

### API_ADMIN_ENQUIRIESRequest

Read inbound enquiries to support customers input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(new\|handled) | False | False | query | Closed enum; reject unknown values |
| cursor | token | False | False | query | opaque cryptographic token; max 512 characters; never logged |
| limit | integer | False | False | query | 1–100; default 25 |

### ContactEnquiryViewPage

ContactEnquiryViewPage

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| items | ContactEnquiryView[] | True | False | body | Validate referenced schema recursively |
| page | PageMeta | True | False | body | Validate referenced schema recursively |

### API_ADMIN_ENQUIRY_STATUSRequest

Mark enquiry handled without sending unauthorized messages input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| enquiry_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| status | enum(new\|handled) | True | False | body | Closed enum; reject unknown values |
| If-Match | version | True | False | header | Expected aggregate version; mismatch 409 VERSION_CONFLICT |

### API_ADMIN_PAID_EXCEPTIONRequest

Resolve late paid no-seat exception exactly once by allocation or refund input

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| payment_id | uuid | True | False | path | Opaque UUID; authorization scoped lookup |
| decision | enum(ALLOCATE\|REFUND) | True | False | body | Closed enum; reject unknown values |
| reason | string | True | False | body | UTF-8, trimmed, 1–200 characters unless otherwise specified |
| If-Match | version | True | False | header | Expected Payment aggregate version |
| Idempotency-Key | uuid | True | False | header | Payment+decision request dedupe;90d retention; body mismatch409 |

### AuthOutcomeView

Discriminated outcome: authenticated has session and null challenge/setup; mfa_challenge has one purpose-bound 5-minute challenge_token and null session/setup; mfa_setup_required has a 10-minute limited setup_token and null session/challenge. Partial authentication grants no teaching/admin API access.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| status | enum(authenticated\|mfa_challenge\|mfa_setup_required) | True | False | body | Closed enum; reject unknown values |
| session | SessionView | True | True | body | Validate referenced schema recursively |
| challenge_token | token | True | True | body | opaque cryptographic token; max 512 characters; never logged |
| setup_token | token | True | True | body | opaque cryptographic token; max 512 characters; never logged |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### StaffSetupSessionView

Invitation establishes limited 10-minute MFA setup session only. Permitted operations are enrol MFA, confirm MFA, logout; no role data APIs.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| account | AccountView | True | False | body | Validate referenced schema recursively |
| setup_token | token | True | False | body | opaque cryptographic token; max 512 characters; never logged |
| expires_at | datetime | True | False | body | RFC3339 timezone-aware instant, UTC persisted |

### MfaActivationView

Successful TOTP proof activates staff role session; setup credentials revoked atomically.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| session | SessionView | True | False | body | Validate referenced schema recursively |
| recovery_codes | string[] | True | False | body | 10 single-use high-entropy codes shown once |

### ReleasedQuestionFeedback

Own submitted attempt only; explanation is immutable approved quiz-version text. No cross-quiz key or hidden correct_option_ids returned.

| Field | Type | Required | Nullable | Location | Validation |
| --- | --- | --- | --- | --- | --- |
| question_id | uuid | True | False | body | UUID v4/v7; opaque identifier; ownership checked after parse |
| correct | boolean | True | False | body | strict JSON boolean |
| awarded_points | integer | True | False | body | strict integer |
| max_points | integer | True | False | body | strict integer |
| explanation | text | True | False | body | UTF-8, max 10000 characters; plain text unless explicitly sanitized rich text |
