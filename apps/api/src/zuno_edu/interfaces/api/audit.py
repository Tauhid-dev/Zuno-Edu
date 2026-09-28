"""Audit transport: server session context, strict filters, explicit response fields."""

from collections.abc import Callable
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from pydantic import AwareDatetime, ConfigDict, Field, StringConstraints, model_validator
from pydantic.json_schema import SkipJsonSchema

from zuno_edu.modules.identity.application.contracts import RequestContext
from zuno_edu.modules.operations.application.audit import AuditFilter, AuditService
from zuno_edu.modules.operations.application.audit import AuditViewPage as Result
from zuno_edu.presentation.http.models import TransportModel

from .identity import BROWSER_COOKIE, CSRF_COOKIE, SESSION_COOKIE, ServiceFactory

type AuditFactory = Callable[[], AuditService]


class API_ADMIN_AUDITRequest(TransportModel):
    actor_id: UUID | SkipJsonSchema[None] = None
    resource_id: UUID | SkipJsonSchema[None] = None
    action: (
        Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
        | SkipJsonSchema[None]
    ) = None
    from_: AwareDatetime = Field(alias="from")
    to: AwareDatetime
    cursor: (
        Annotated[str, StringConstraints(min_length=1, max_length=512)] | SkipJsonSchema[None]
    ) = None
    limit: Annotated[int, Field(ge=1, le=100)] = 25

    @model_validator(mode="after")
    def bounded(self) -> API_ADMIN_AUDITRequest:
        for name in ("actor_id", "resource_id", "action", "cursor"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError("Optional fields cannot be null")
        self.filter()
        return self

    def filter(self) -> AuditFilter:
        return AuditFilter(
            self.from_,
            self.to,
            self.actor_id,
            self.resource_id,
            self.action,
            self.limit,
            self.cursor,
        )


class AuditView(TransportModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    actor_id: UUID | None
    action: str
    resource_type: str
    resource_id: UUID | None
    occurred_at: datetime
    outcome: Literal["allowed", "denied", "failed"]
    request_id: UUID
    reason: str | None


class PageMeta(TransportModel):
    model_config = ConfigDict(from_attributes=True)
    next_cursor: str | None
    has_more: bool


class AuditViewPage(TransportModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[AuditView]
    page: PageMeta


def create_audit_router(identity: ServiceFactory, factory: AuditFactory) -> APIRouter:
    router = APIRouter()

    def service() -> AuditService:
        return factory()

    @router.get("/admin/audit", response_model=AuditViewPage)
    def list_audit(
        request: Request,
        filters: Annotated[API_ADMIN_AUDITRequest, Query()],
        audit: Annotated[AuditService, Depends(service)],
    ) -> Result:
        context = RequestContext(
            request.cookies.get(BROWSER_COOKIE, ""),
            request.cookies.get(CSRF_COOKIE, ""),
            request.headers.get("Origin", ""),
            request.client.host if request.client else "unknown",
            request.cookies.get(SESSION_COOKIE),
        )
        principal = identity(lambda _: None, request.state.request_id).get_principal(
            context, request.state.request_id
        )
        return audit.list_audit(principal, filters.filter())

    return router
