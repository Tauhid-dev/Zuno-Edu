"""Build the minimal transport application without business capabilities."""

from fastapi import FastAPI

from zuno_edu.interfaces.api.health import router
from zuno_edu.presentation.http.errors import install_error_handlers
from zuno_edu.presentation.http.models import Error


def create_app() -> FastAPI:
    application = FastAPI(
        title="Zuno Edu",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        responses={code: {"model": Error} for code in (401, 403, 404, 409, 422, 429, 503)},
    )
    application.include_router(router, prefix="/api/v1")
    install_error_handlers(application)
    return application
