"""Internal request context and explicit authentication projections."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Literal
from uuid import UUID

from pydantic import ConfigDict

from zuno_edu.modules.identity.domain import Account, AccountStatus, Role


@dataclass(frozen=True, repr=False)
class RequestContext:
    browser_token: str
    csrf_token: str
    origin: str
    network: str
    session_token: str | None = None


@dataclass(frozen=True)
class SessionView:
    __pydantic_config__: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

    user_id: UUID
    role: Role
    privileges: tuple[str, ...]
    display_name: str
    expires_at: datetime
    csrf_token: str = field(repr=False)
    mfa_required: bool


@dataclass(frozen=True)
class AuthOutcomeView:
    __pydantic_config__: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

    status: Literal["authenticated", "mfa_challenge", "mfa_setup_required"]
    session: SessionView | None
    challenge_token: str | None = field(repr=False)
    setup_token: str | None = field(repr=False)
    expires_at: datetime


@dataclass(frozen=True)
class AccountView:
    __pydantic_config__: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

    id: UUID
    role: Role
    display_name: str
    email: str | None
    status: AccountStatus
    mfa_enabled: bool
    version: int

    @classmethod
    def from_account(cls, account: Account) -> AccountView:
        return cls(
            account.id,
            account.role.role,
            account.display_name,
            account.email,
            account.status,
            account.mfa_enabled,
            account.version,
        )


@dataclass(frozen=True)
class StaffSetupSessionView:
    __pydantic_config__: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

    account: AccountView
    setup_token: str = field(repr=False)
    expires_at: datetime


@dataclass(frozen=True)
class MfaSetupView:
    __pydantic_config__: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

    setup_token: str = field(repr=False)
    otpauth_uri: str = field(repr=False)
    expires_at: datetime


@dataclass(frozen=True)
class MfaActivationView:
    __pydantic_config__: ClassVar[ConfigDict] = ConfigDict(extra="forbid")

    session: SessionView
    recovery_codes: tuple[str, ...] = field(repr=False)
