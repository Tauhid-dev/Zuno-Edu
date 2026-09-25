"""Internal request context and explicit authentication projections."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from zuno_edu.modules.identity.domain import Account, Role


@dataclass(frozen=True, repr=False)
class RequestContext:
    browser_token: str
    csrf_token: str
    origin: str
    network: str
    session_token: str | None = None


@dataclass(frozen=True)
class SessionView:
    user_id: UUID
    role: Role
    privileges: tuple[str, ...]
    display_name: str
    expires_at: datetime
    csrf_token: str = field(repr=False)
    mfa_required: bool = False


@dataclass(frozen=True)
class AuthOutcomeView:
    status: str
    session: SessionView | None
    challenge_token: str | None = field(repr=False)
    setup_token: str | None = field(repr=False)
    expires_at: datetime


@dataclass(frozen=True)
class AccountView:
    id: UUID
    role: Role
    display_name: str
    email: str | None
    status: str
    mfa_enabled: bool
    version: int

    @classmethod
    def from_account(cls, account: Account) -> AccountView:
        return cls(
            account.id,
            account.role.role,
            account.display_name,
            account.email,
            account.status.value,
            account.mfa_enabled,
            account.version,
        )


@dataclass(frozen=True)
class StaffSetupSessionView:
    account: AccountView
    setup_token: str = field(repr=False)
    expires_at: datetime


@dataclass(frozen=True)
class MfaSetupView:
    setup_token: str = field(repr=False)
    otpauth_uri: str = field(repr=False)
    expires_at: datetime


@dataclass(frozen=True)
class MfaActivationView:
    session: SessionView
    recovery_codes: tuple[str, ...] = field(repr=False)
