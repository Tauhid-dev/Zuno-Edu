"""Stable safe responses; exception bodies and validation inputs never leave the server."""

import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from zuno_edu.shared.persistence import VersionConflict

from .models import Error

logger = logging.getLogger(__name__)
ERRORS: dict[str, tuple[int, str]] = {
    "UNAUTHENTICATED": (401, "Sign in to continue."),
    "FORBIDDEN": (403, "This action is not permitted."),
    "NOT_FOUND": (404, "The requested resource is unavailable."),
    "VERSION_CONFLICT": (409, "Reload the latest version before retrying."),
    "INVALID_STATE": (409, "The current state does not permit this action."),
    "VALIDATION_ERROR": (422, "Check required fields, allowed fields and formats."),
    "RATE_LIMITED": (429, "Too many requests. Try again later."),
    "PROVIDER_UNAVAILABLE": (503, "The service is temporarily unavailable."),
}


@dataclass
class ApiError(Exception):
    code: str
    retry_after_seconds: int | None = None

    def __post_init__(self) -> None:
        if self.code not in ERRORS:
            raise ValueError("Undocumented error code")
        if self.code == "RATE_LIMITED" and self.retry_after_seconds is None:
            raise ValueError("Rate limits require retry metadata")
        if self.retry_after_seconds is not None and (
            type(self.retry_after_seconds) is not int
            or not 1 <= self.retry_after_seconds <= 3600
            or self.code not in {"RATE_LIMITED", "PROVIDER_UNAVAILABLE"}
        ):
            raise ValueError("Invalid retry metadata")


def problem(request: Request, error: ApiError, status: int | None = None) -> JSONResponse:
    http_status, message = ERRORS[error.code]
    request_id = getattr(request.state, "request_id", uuid4())
    body = Error(code=error.code, message=message, request_id=request_id)
    headers = {"Cache-Control": "no-store", "X-Request-ID": str(request_id)}
    if error.retry_after_seconds is not None:
        body.retry_after_seconds = error.retry_after_seconds
        headers["Retry-After"] = str(error.retry_after_seconds)
    return JSONResponse(
        body.model_dump(mode="json", exclude_unset=True),
        status_code=status or http_status,
        headers=headers,
    )


def install_error_handlers(app: FastAPI) -> None:
    @app.middleware("http")
    async def correlation(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request.state.request_id = uuid4()
        try:
            response = await call_next(request)
        except Exception:
            logger.error("REQUEST_FAILED request_id=%s", request.state.request_id)
            response = problem(request, ApiError("PROVIDER_UNAVAILABLE"))
        response.headers["X-Request-ID"] = str(request.state.request_id)
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(ApiError)
    async def api_error(request: Request, error: ApiError) -> JSONResponse:
        return problem(request, error)

    @app.exception_handler(VersionConflict)
    async def version_error(request: Request, error: VersionConflict) -> JSONResponse:
        return problem(request, ApiError("VERSION_CONFLICT"))

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, error: RequestValidationError) -> JSONResponse:
        # FastAPI's default detail includes raw inputs and untrusted field names.
        return problem(request, ApiError("VALIDATION_ERROR"))

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, error: HTTPException) -> JSONResponse:
        code = next(
            (key for key, value in ERRORS.items() if value[0] == error.status_code),
            "VALIDATION_ERROR",
        )
        retry = 1 if code == "RATE_LIMITED" else None
        return problem(request, ApiError(code, retry), error.status_code)
