"""Build the minimal transport application without business capabilities."""

from fastapi import FastAPI

from zuno_edu.interfaces.api.health import router


def create_app() -> FastAPI:
    application = FastAPI(
        title="Zuno Edu",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    application.include_router(router, prefix="/api/v1")
    return application
