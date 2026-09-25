"""Identity aggregates, with no transport or persistence dependencies."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum
from uuid import UUID

from zuno_edu.shared.persistence import require_instant


class AuthError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class Role(StrEnum):
    PARENT = "parent"
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class AccountStatus(StrEnum):
    INVITED = "invited"
    PENDING = "pending_verification"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


PRIVILEGES = frozenset(
    {"identity_admin", "education_admin", "finance_admin", "operations_admin", "audit_admin"}
)


@dataclass(frozen=True)
class RoleGrant:
    role: Role
    admin_privileges: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not isinstance(self.role, Role) or not self.admin_privileges <= PRIVILEGES:
            raise AuthError("INCOMPATIBLE_ROLE")
        if (self.role == Role.ADMIN) != bool(self.admin_privileges):
            raise AuthError("INCOMPATIBLE_ROLE")

    def allows(self, capability: str) -> bool:
        return self.role == Role.ADMIN and capability in self.admin_privileges


@dataclass
class Account:
    id: UUID
    role: RoleGrant
    status: AccountStatus
    email: str | None
    display_name: str
    mfa_enabled: bool = False
    version: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.status, AccountStatus) or self.version < 1:
            raise AuthError("INVALID_STATE")
        if not self.display_name.strip() or len(self.display_name) > 200:
            raise AuthError("INVALID_STATE")
        if self.role.role != Role.STUDENT and not self.email:
            raise AuthError("INVALID_STATE")

    @property
    def staff(self) -> bool:
        return self.role.role in {Role.TEACHER, Role.ADMIN}

    def require_login(self) -> None:
        if self.status not in {AccountStatus.PENDING, AccountStatus.ACTIVE}:
            raise AuthError("INVALID_CREDENTIALS")

    def activate(self, verified_at: datetime) -> None:
        require_instant(verified_at)
        if self.status not in {AccountStatus.PENDING, AccountStatus.INVITED}:
            raise AuthError("INVALID_STATE")
        if self.staff and not self.mfa_enabled:
            raise AuthError("INVALID_STATE")
        self.status = AccountStatus.ACTIVE
        self.version += 1

    def suspend(self, reason: str) -> None:
        if not reason.strip() or self.status == AccountStatus.CLOSED:
            raise AuthError("INVALID_STATE")
        self.status = AccountStatus.SUSPENDED
        self.version += 1


@dataclass
class Credential:
    user_id: UUID
    password_hash: str = field(repr=False)
    changed_at: datetime
    failed_attempts: int = 0
    locked_until: datetime | None = None

    def __post_init__(self) -> None:
        if not self.password_hash.startswith("$argon2id$") or self.failed_attempts < 0:
            raise AuthError("INVALID_STATE")
        require_instant(self.changed_at)

    def replace(self, password_hash: str, now: datetime) -> None:
        if not password_hash.startswith("$argon2id$"):
            raise AuthError("VALIDATION_ERROR")
        self.password_hash = password_hash
        self.changed_at = require_instant(now)
        self.failed_attempts = 0
        self.locked_until = None

    def verify_attempt(self, outcome: bool, now: datetime) -> bool:
        now = require_instant(now)
        if self.locked_until is not None and now < self.locked_until:
            return True
        if self.locked_until is not None:
            self.failed_attempts = 0
            self.locked_until = None
        self.failed_attempts = 0 if outcome else self.failed_attempts + 1
        if self.failed_attempts >= 5:
            self.locked_until = now + timedelta(minutes=1)
        return self.locked_until is not None


@dataclass
class Session:
    id: UUID
    user_id: UUID
    token_hash: bytes = field(repr=False)
    created_at: datetime
    last_seen_at: datetime
    expires_at: datetime
    staff: bool
    revoked_at: datetime | None = None
    mfa_verified_at: datetime | None = None
    device_label: str = ""

    def __post_init__(self) -> None:
        for instant in (self.created_at, self.last_seen_at, self.expires_at):
            require_instant(instant)
        if not self.created_at < self.expires_at <= self.created_at + timedelta(days=7):
            raise AuthError("INVALID_STATE")

    def is_active(self, now: datetime) -> bool:
        now = require_instant(now)
        idle = timedelta(minutes=30) if self.staff else timedelta(hours=12)
        return (
            self.revoked_at is None
            and self.created_at <= now < min(self.expires_at, self.last_seen_at + idle)
            and (not self.staff or self.mfa_verified_at is not None)
        )

    def revoke(self, now: datetime) -> None:
        if self.revoked_at is None:
            self.revoked_at = require_instant(now)

    def rotate(self, new_hash: bytes, now: datetime) -> None:
        if not self.is_active(now) or len(new_hash) < 32:
            raise AuthError("UNAUTHENTICATED")
        self.token_hash = new_hash
        self.last_seen_at = require_instant(now)


@dataclass(frozen=True)
class VerifiedTotpProof:
    factor_id: UUID
    step: int


@dataclass(frozen=True)
class VerifiedSecondFactor:
    account_id: UUID
    factor_id: UUID
    browser_hash: bytes = field(repr=False)
    purpose: str


@dataclass(frozen=True)
class VerifiedRecoveryProof:
    factor_id: UUID
    code_hash: bytes = field(repr=False)


@dataclass
class MfaChallenge:
    id: UUID
    account_id: UUID
    token_hash: bytes = field(repr=False)
    purpose: str
    expires_at: datetime
    browser_binding_hash: bytes = field(repr=False)
    factor_id: UUID | None = None
    attempts: int = 0
    consumed_at: datetime | None = None

    def __post_init__(self) -> None:
        require_instant(self.expires_at)
        if self.purpose not in {"challenge", "setup"} or not 0 <= self.attempts <= 5:
            raise AuthError("INVALID_STATE")

    def check(self, purpose: str, browser_hash: bytes, now: datetime) -> None:
        if self.purpose != purpose or self.browser_binding_hash != browser_hash:
            raise AuthError("UNAUTHENTICATED")
        if self.consumed_at is not None:
            raise AuthError("MFA_REPLAY")
        if require_instant(now) >= self.expires_at:
            raise AuthError("MFA_CHALLENGE_EXPIRED")
        if self.attempts >= 5:
            raise AuthError("MFA_ATTEMPTS_EXCEEDED")

    def consume(self, proof: VerifiedSecondFactor, now: datetime) -> None:
        self.check(proof.purpose, proof.browser_hash, now)
        if proof.account_id != self.account_id or proof.factor_id != self.factor_id:
            raise AuthError("UNAUTHENTICATED")
        self.consumed_at = require_instant(now)

    def reject_attempt(self, now: datetime) -> None:
        self.check(self.purpose, self.browser_binding_hash, now)
        self.attempts += 1


@dataclass
class MfaFactor:
    id: UUID
    account_id: UUID
    secret_reference: bytes = field(repr=False)
    encryption_key_version: str
    status: str = "pending"
    last_accepted_step: int | None = None
    activated_at: datetime | None = None
    revoked_at: datetime | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if self.status not in {"pending", "active", "revoked"} or self.version < 1:
            raise AuthError("INVALID_STATE")

    def accept_step(self, step: int) -> None:
        if self.status == "revoked" or step < 0:
            raise AuthError("INVALID_STATE")
        if self.last_accepted_step is not None and step <= self.last_accepted_step:
            raise AuthError("MFA_REPLAY")
        self.last_accepted_step = step
        self.version += 1

    def activate(self, proof: VerifiedTotpProof, now: datetime) -> None:
        if self.status != "pending" or proof.factor_id != self.id:
            raise AuthError("INVALID_STATE")
        self.accept_step(proof.step)
        self.status = "active"
        self.activated_at = require_instant(now)

    def revoke(self, reason: str) -> None:
        if not reason.strip():
            raise AuthError("VALIDATION_ERROR")
        self.status = "revoked"
        self.version += 1


@dataclass
class RecoveryCode:
    id: UUID
    factor_id: UUID
    code_hash: bytes = field(repr=False)
    consumed_at: datetime | None = None

    def consume(self, proof: VerifiedRecoveryProof, now: datetime) -> None:
        if proof.factor_id != self.factor_id or proof.code_hash != self.code_hash:
            raise AuthError("UNAUTHENTICATED")
        if self.consumed_at is not None:
            raise AuthError("MFA_REPLAY")
        self.consumed_at = require_instant(now)
