"""HTTP response DTOs adapt framework-independent authentication projections."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import ConfigDict, Field

from zuno_edu.modules.identity.domain import AccountStatus, Role
from zuno_edu.presentation.http.models import TransportModel


class IdentityResponse(TransportModel):
    model_config = ConfigDict(from_attributes=True)


class SessionView(IdentityResponse):
    user_id: UUID
    role: Role
    privileges: tuple[str, ...]
    display_name: str
    expires_at: datetime
    csrf_token: str = Field(repr=False)
    mfa_required: bool


class AuthOutcomeView(IdentityResponse):
    status: Literal["authenticated", "mfa_challenge", "mfa_setup_required"]
    session: SessionView | None
    challenge_token: str | None = Field(repr=False)
    setup_token: str | None = Field(repr=False)
    expires_at: datetime


class AccountView(IdentityResponse):
    id: UUID
    role: Role
    display_name: str
    email: str | None
    status: AccountStatus
    mfa_enabled: bool
    version: int


class StaffSetupSessionView(IdentityResponse):
    account: AccountView
    setup_token: str = Field(repr=False)
    expires_at: datetime


class MfaSetupView(IdentityResponse):
    setup_token: str = Field(repr=False)
    otpauth_uri: str = Field(repr=False)
    expires_at: datetime


class MfaActivationView(IdentityResponse):
    session: SessionView
    recovery_codes: tuple[str, ...] = Field(repr=False)
