"""Strict authentication transport with request-local services and secure cookies."""

from collections.abc import Callable
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Request, Response
from pydantic import Field, StringConstraints, model_validator

from zuno_edu.modules.identity.application.contracts import (
    AuthOutcomeView,
    MfaActivationView,
    MfaSetupView,
    RequestContext,
    SessionView,
    StaffSetupSessionView,
)
from zuno_edu.modules.identity.application.service import AuthenticationService
from zuno_edu.presentation.http.models import TransportModel

SESSION_COOKIE = "__Host-zuno-session"
BROWSER_COOKIE = "__Host-zuno-browser"
CSRF_COOKIE = "__Host-zuno-csrf"
SETUP_COOKIE = "__Host-zuno-setup"
type ServiceFactory = Callable[[Callable[[str | None], None]], AuthenticationService]
Password = Annotated[str, StringConstraints(min_length=12, max_length=128)]
Token = Annotated[str, StringConstraints(min_length=1, max_length=512)]
Code = Annotated[str, StringConstraints(pattern=r"^(?:[0-9]{6}|[A-Z2-7]{26})$")]


class LoginRequest(TransportModel):
    identifier: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=254)
    ]
    password: Password = Field(repr=False)


class TokenRequest(TransportModel):
    token: Token = Field(repr=False)


class EmailRequest(TransportModel):
    email: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, max_length=254, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        ),
    ]


class ResetRequest(TokenRequest):
    new_password: Password = Field(repr=False)


class InvitationRequest(TokenRequest):
    password: Password = Field(repr=False)


class MfaRequest(TransportModel):
    challenge_token: Token = Field(repr=False)
    code: Code = Field(repr=False)


class ConfirmRequest(TransportModel):
    setup_token: Token = Field(repr=False)
    code: Annotated[str, StringConstraints(pattern=r"^[0-9]{6}$")] = Field(repr=False)


class EnrolRequest(TransportModel):
    password: Password = Field(repr=False)
    setup_token: Token | None = Field(default=None, repr=False)

    @model_validator(mode="after")
    def nonnullable_optional(self) -> EnrolRequest:
        if "setup_token" in self.model_fields_set and self.setup_token is None:
            raise ValueError("setup_token must be omitted or supplied")
        return self


def set_cookie(response: Response, name: str, value: str | None, max_age: int) -> None:
    if value is None:
        response.delete_cookie(name, path="/", secure=True, httponly=True, samesite="lax")
    else:
        response.set_cookie(
            name, value, max_age=max_age, path="/", secure=True, httponly=True, samesite="lax"
        )


def create_identity_router(factory: ServiceFactory) -> APIRouter:
    router = APIRouter()

    def service(response: Response) -> AuthenticationService:
        def cookie(value: str | None) -> None:
            set_cookie(response, SESSION_COOKIE, value, 7 * 24 * 3600)
            if value:
                set_cookie(response, SETUP_COOKIE, None, 0)

        return factory(cookie)

    def context(request: Request) -> RequestContext:
        return RequestContext(
            request.cookies.get(BROWSER_COOKIE, ""),
            request.headers.get("X-CSRF-Token", ""),
            request.headers.get("Origin", ""),
            request.client.host if request.client else "unknown",
            request.cookies.get(SESSION_COOKIE),
        )

    @router.post("/auth/sessions", response_model=AuthOutcomeView)
    def login(
        body: LoginRequest,
        response: Response,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> AuthOutcomeView:
        result = auth.login(principal, body.model_dump())
        set_cookie(response, SETUP_COOKIE, result.setup_token, 600)
        return result

    @router.get("/account/session", response_model=SessionView)
    def current(
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> SessionView:
        return auth.get_session(principal, {})

    @router.delete("/auth/sessions/current", status_code=204)
    def logout(
        request: Request,
        response: Response,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> None:
        token = request.cookies.get(SETUP_COOKIE)
        auth.logout(principal, {"setup_token": token} if token else {})
        set_cookie(response, SETUP_COOKIE, None, 0)

    @router.post("/auth/mfa/verifications", response_model=SessionView)
    def verify_mfa(
        body: MfaRequest,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> SessionView:
        return auth.verify_mfa(principal, body.model_dump())

    @router.post("/account/mfa/enrolment", response_model=MfaSetupView)
    def enrol(
        body: EnrolRequest,
        response: Response,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
        key: Annotated[UUID, Header(alias="Idempotency-Key")],
    ) -> MfaSetupView:
        result = auth.enrol_mfa(
            principal,
            {
                **body.model_dump(exclude_unset=True),
                "Idempotency-Key": str(key),
            },
        )
        set_cookie(response, SETUP_COOKIE, result.setup_token, 600)
        return result

    @router.post("/account/mfa/confirmation", response_model=MfaActivationView)
    def confirm(
        body: ConfirmRequest,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> MfaActivationView:
        return auth.confirm_mfa(principal, body.model_dump())

    @router.post("/auth/email-verifications", status_code=204)
    def verify_email(
        body: TokenRequest,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> None:
        auth.verify_email(principal, body.model_dump())

    @router.post("/auth/email-verifications/resend", status_code=204)
    def resend(
        body: EmailRequest,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> None:
        auth.resend_verification(principal, body.model_dump())

    @router.post("/auth/password-reset-requests", status_code=204)
    def request_reset(
        body: EmailRequest,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> None:
        auth.request_password_reset(principal, body.model_dump())

    @router.post("/auth/password-resets", status_code=204)
    def reset(
        body: ResetRequest,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> None:
        auth.reset_password(principal, body.model_dump())

    @router.post("/auth/staff-invitations/accept", response_model=StaffSetupSessionView)
    def accept(
        body: InvitationRequest,
        response: Response,
        principal: Annotated[RequestContext, Depends(context)],
        auth: Annotated[AuthenticationService, Depends(service)],
    ) -> StaffSetupSessionView:
        result = auth.accept_staff_invitation(principal, body.model_dump())
        set_cookie(response, SETUP_COOKIE, result.setup_token, 600)
        return result

    return router
