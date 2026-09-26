from collections.abc import Callable
from dataclasses import replace
from datetime import timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from test_authentication_service import PASSWORD, Harness
from zuno_edu.bootstrap.app import create_app
from zuno_edu.interfaces.api.identity import CSRF_COOKIE, SESSION_COOKIE
from zuno_edu.modules.identity.application.service import AuthenticationService
from zuno_edu.modules.identity.domain import AuthError, Role


def client_for(h: Harness) -> TestClient:
    def factory(cookie: Callable[[str | None], None]) -> AuthenticationService:
        return AuthenticationService(
            h.store.transaction,
            h.passwords,
            h.tokens,
            h.verifier,
            h.keys,
            h.security,
            h.abuse,
            h.clock,
            cookie,
            lambda _: h.approved,
            h.hash,
        )

    return TestClient(create_app(factory, h.security), base_url="https://zuno.test")


def bootstrap(client: TestClient) -> dict[str, str]:
    response = client.get("/api/v1/account/session")
    assert response.status_code == 401
    return {"Origin": "https://zuno.test", "X-CSRF-Token": client.cookies[CSRF_COOKIE]}


def test_http_login_cookies_session_logout_and_csrf() -> None:
    h = Harness()
    subject = h.account(Role.PARENT)
    with client_for(h) as client:
        headers = bootstrap(client)
        body = {"identifier": h.store.state.accounts[subject].email, "password": PASSWORD}
        assert client.post("/api/v1/auth/sessions", json=body).status_code == 403
        result = client.post("/api/v1/auth/sessions", json=body, headers=headers)
        assert result.status_code == 200
        assert result.json()["session"]["role"] == "parent"
        secret = client.cookies[SESSION_COOKIE]
        assert secret not in result.text
        cookie = next(c for c in result.headers.get_list("set-cookie") if SESSION_COOKIE in c)
        assert "HttpOnly" in cookie and "Secure" in cookie and "SameSite=lax" in cookie
        assert client.get("/api/v1/account/session").status_code == 200
        assert client.delete("/api/v1/auth/sessions/current", headers=headers).status_code == 204
        assert client.get("/api/v1/account/session").status_code == 401


def test_http_setup_is_limited_and_response_never_replays_secret() -> None:
    h = Harness()
    subject = h.account()
    with client_for(h) as client:
        headers = bootstrap(client)
        result = client.post(
            "/api/v1/auth/sessions",
            json={
                "identifier": h.store.state.accounts[subject].email,
                "password": PASSWORD,
            },
            headers=headers,
        )
        assert result.status_code == 200
        token = result.json()["setup_token"]
        assert result.json()["session"] is None
        assert client.get("/api/v1/account/session").status_code == 401
        headers["Idempotency-Key"] = str(uuid4())
        body = {"password": PASSWORD, "setup_token": token}
        result = client.post("/api/v1/account/mfa/enrolment", json=body, headers=headers)
        assert result.status_code == 200
        assert result.headers["cache-control"] == "no-store"
        uri = result.json()["otpauth_uri"]
        result = client.post("/api/v1/account/mfa/enrolment", json=body, headers=headers)
        assert result.status_code == 409 and result.json()["code"] == "MFA_REPLAY"
        assert uri not in result.text and token not in result.text
        assert client.delete("/api/v1/auth/sessions/current", headers=headers).status_code == 204


@pytest.mark.parametrize("error", ["RATE_LIMITED", "MFA_ATTEMPTS_EXCEEDED"])
def test_rate_limit_error_has_safe_429_and_retry_header(error: str) -> None:
    h = Harness()

    class Deny:
        def check(self, operation: str, identity: str, network: str) -> None:
            raise AuthError(error)

    h.abuse = Deny()  # type: ignore[assignment]
    with client_for(h) as client:
        headers = bootstrap(client)
        result = client.post(
            "/api/v1/auth/sessions",
            json={
                "identifier": "unknown@example.org",
                "password": PASSWORD,
            },
            headers=headers,
        )
        assert result.status_code == 429 and result.json()["code"] == error
        assert int(result.headers["retry-after"]) > 0
        assert PASSWORD not in result.text


def test_unknown_fields_and_null_setup_are_rejected_without_echo() -> None:
    h = Harness()
    with client_for(h) as client:
        headers = bootstrap(client)
        result = client.post(
            "/api/v1/auth/sessions",
            json={
                "identifier": "unknown@example.org",
                "password": PASSWORD,
                "role": "admin",
            },
            headers=headers,
        )
        assert result.status_code == 422 and PASSWORD not in result.text
        headers["Idempotency-Key"] = str(uuid4())
        result = client.post(
            "/api/v1/account/mfa/enrolment",
            json={
                "password": PASSWORD,
                "setup_token": None,
            },
            headers=headers,
        )
        assert result.status_code == 422


def test_session_activity_slides_idle_but_never_absolute_expiry() -> None:
    h = Harness()
    subject = h.account(Role.PARENT)
    h.service.login(
        h.context,
        {
            "identifier": h.store.state.accounts[subject].email or "",
            "password": PASSWORD,
        },
    )
    context = replace(h.context, session_token=h.cookies[-1])
    initial = h.clock.now()
    h.clock.instant += timedelta(hours=11)
    h.service.get_session(context, {})
    h.clock.instant += timedelta(hours=2)
    h.service.get_session(context, {})
    session = next(iter(h.store.state.sessions.values()))
    assert session.last_seen_at == h.clock.now()
    h.clock.instant = initial + timedelta(days=7)
    with pytest.raises(AuthError, match="UNAUTHENTICATED"):
        h.service.get_session(context, {})
