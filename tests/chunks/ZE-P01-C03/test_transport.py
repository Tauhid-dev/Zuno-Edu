"""Transport failures cannot expose inputs, internals, or untrusted authority."""

from typing import Annotated
from uuid import UUID

import pytest
from fastapi import Depends, Query
from fastapi.testclient import TestClient
from pydantic import ValidationError
from zuno_edu.bootstrap.app import create_app
from zuno_edu.presentation.http.errors import ERRORS, ApiError
from zuno_edu.presentation.http.models import (
    BoundedText,
    Instant,
    OptionalText,
    PageQuery,
    TransportModel,
)
from zuno_edu.presentation.http.validation import (
    expected_version,
    first_write_version,
    require_json,
)
from zuno_edu.shared.persistence import VersionConflict


class Input(TransportModel):
    name: BoundedText
    note: OptionalText = None
    at: Instant


def test_strict_input_blank_null_patch_and_aware_instants() -> None:
    base = dict(name=" hello ", at="2026-09-22T12:00:00+10:00")
    omitted = Input.model_validate(base)
    assert omitted.name == "hello" and "note" not in omitted.model_fields_set
    assert omitted.at.utcoffset().total_seconds() == 0  # type: ignore[union-attr]
    assert Input.model_validate({**base, "note": "  "}).note is None
    assert "note" in Input.model_validate({**base, "note": None}).model_fields_set
    for changes in (
        {"unknown": "sensitive"},
        {"name": " "},
        {"name": "a" * 201},
        {"at": "2026-09-22T12:00:00"},
    ):
        with pytest.raises(ValidationError):
            Input.model_validate({**base, **changes})


def test_request_validation_does_not_reflect_sensitive_values_or_field_names() -> None:
    app = create_app()

    @app.post("/api/v1/test-input", dependencies=[Depends(require_json)])
    def endpoint(body: Input) -> dict[str, str]:
        return {"name": body.name}

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/test-input",
            json={"child-private-name": "password=secret"},
            headers={"X-Request-ID": "untrusted-sensitive"},
        )
        assert response.status_code == 422
        assert set(response.json()) == {"code", "message", "request_id"}
        assert response.json()["code"] == "VALIDATION_ERROR"
        assert "secret" not in response.text and "child-private-name" not in response.text
        UUID(response.json()["request_id"])
        assert response.headers["x-request-id"] == response.json()["request_id"]
        assert response.headers["cache-control"] == "no-store"
        assert (
            client.post(
                "/api/v1/test-input", content="{}", headers={"Content-Type": "text/plain"}
            ).status_code
            == 422
        )


@pytest.mark.parametrize("code", list(ERRORS))
def test_stable_status_and_retry_contract(code: str) -> None:
    app = create_app()

    @app.get("/api/v1/test-error")
    def endpoint() -> None:
        raise ApiError(code, 30 if code in {"RATE_LIMITED", "PROVIDER_UNAVAILABLE"} else None)

    with TestClient(app) as client:
        response = client.get("/api/v1/test-error")
    assert response.status_code == ERRORS[code][0]
    assert response.json()["code"] == code
    if code in {"RATE_LIMITED", "PROVIDER_UNAVAILABLE"}:
        assert response.headers["retry-after"] == "30"
        assert response.json()["retry_after_seconds"] == 30
    else:
        assert "retry_after_seconds" not in response.json()


def test_unexpected_errors_and_version_conflicts_are_safe() -> None:
    app = create_app()

    @app.get("/api/v1/test-crash")
    def crash() -> None:
        raise RuntimeError("SQL private child secret token")

    @app.get("/api/v1/test-version")
    def version() -> None:
        raise VersionConflict("private aggregate ID")

    with TestClient(app) as client:
        failure = client.get("/api/v1/test-crash")
        assert failure.status_code == 503 and "SQL" not in failure.text
        assert client.get("/api/v1/test-version").json()["code"] == "VERSION_CONFLICT"
        assert client.get("/api/v1/unknown").json()["code"] == "NOT_FOUND"
        assert client.post("/api/v1/health").status_code == 405


def test_pagination_is_bounded_at_http_boundary() -> None:
    app = create_app()

    @app.get("/api/v1/test-page")
    def endpoint(query: Annotated[PageQuery, Query()]) -> dict[str, int]:
        return {"limit": query.limit}

    with TestClient(app) as client:
        assert client.get("/api/v1/test-page").json() == {"limit": 25}
        assert client.get("/api/v1/test-page?limit=100").status_code == 200
        for query in ("limit=0", "limit=101", "limit=1.5", "extra=1", "cursor="):
            assert client.get("/api/v1/test-page?" + query).status_code == 422


def test_conditional_headers_reject_absence_wildcards_and_double_conditions() -> None:
    assert expected_version('"12"') == 12
    assert expected_version("12") == 12
    assert first_write_version(None, "*") is None
    assert first_write_version("3", None) == 3
    for value in (None, "0", "-1", "*", 'W/"1"', '"1', "true", "1,2"):
        with pytest.raises(ApiError):
            expected_version(value)
    for both in ((None, None), ("1", "*"), (None, "other")):
        with pytest.raises(ApiError):
            first_write_version(*both)


def test_rate_limits_require_retry_metadata() -> None:
    from starlette.exceptions import HTTPException

    with pytest.raises(ValueError, match="retry metadata"):
        ApiError("RATE_LIMITED")
    app = create_app()

    @app.get("/api/v1/test-rate")
    def endpoint() -> None:
        raise HTTPException(429)

    with TestClient(app) as client:
        response = client.get("/api/v1/test-rate")
        assert response.status_code == 429
        assert response.headers["Retry-After"] == "1"
        assert response.json()["retry_after_seconds"] == 1
