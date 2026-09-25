"""Build the minimal transport application without business capabilities."""

from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from zuno_edu.interfaces.api.health import router
from zuno_edu.interfaces.api.identity import (
    BROWSER_COOKIE,
    CSRF_COOKIE,
    ServiceFactory,
    create_identity_router,
    set_cookie,
)
from zuno_edu.modules.identity.application.contracts import RequestContext
from zuno_edu.modules.identity.domain import AuthError
from zuno_edu.modules.identity.infrastructure.security import RequestSecurity
from zuno_edu.presentation.http.errors import install_error_handlers
from zuno_edu.presentation.http.models import Error


def create_app(
    identity_factory: ServiceFactory | None = None,
    request_security: RequestSecurity | None = None,
) -> FastAPI:
    if (identity_factory is None) != (request_security is None):
        raise ValueError("Identity service and browser security must be composed together")
    application = FastAPI(
        title="Zuno Edu",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        responses={code: {"model": Error} for code in (401, 403, 404, 409, 422, 429, 503)},
    )
    application.include_router(router, prefix="/api/v1")
    if identity_factory is not None and request_security is not None:
        application.include_router(create_identity_router(identity_factory), prefix="/api/v1")

        @application.middleware("http")
        async def browser_context(
            request: Request, call_next: Callable[[Request], Awaitable[Response]]
        ) -> Response:
            response = await call_next(request)
            if request.method == "GET" and request.url.path == "/api/v1/account/session":
                assert request_security is not None
                browser = request.cookies.get(BROWSER_COOKIE, "")
                try:
                    request_security.validate(RequestContext(browser, "", "", ""), mutation=False)
                except AuthError:
                    browser = request_security.browser()
                    set_cookie(response, BROWSER_COOKIE, browser, 7 * 24 * 3600)
                # Public pre-authentication CSRF bootstrap; no bearer session is exposed.
                response.set_cookie(
                    CSRF_COOKIE,
                    request_security.csrf(browser),
                    path="/",
                    secure=True,
                    httponly=False,
                    samesite="lax",
                )
            return response

    install_error_handlers(application)
    return application
