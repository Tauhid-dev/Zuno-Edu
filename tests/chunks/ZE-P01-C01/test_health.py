from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from zuno_edu.bootstrap.app import create_app
from zuno_edu.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


def test_health_is_liveness_without_private_configuration(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["cache-control"] == "no-store"


def test_only_health_is_registered() -> None:
    application = create_app()
    paths = application.openapi()["paths"]
    assert set(paths) == {"/api/v1/health"}
    assert set(paths["/api/v1/health"]) == {"get"}


@pytest.mark.parametrize("path", ["/api/v1/users", "/api/v1/payments", "/docs", "/openapi.json"])
def test_business_and_documentation_endpoints_are_absent(client: TestClient, path: str) -> None:
    assert client.get(path).status_code == 404


def test_health_cannot_mutate_state(client: TestClient) -> None:
    assert client.post("/api/v1/health").status_code == 405
