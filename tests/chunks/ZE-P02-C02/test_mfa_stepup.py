import importlib
from dataclasses import replace
from datetime import timedelta
from uuid import uuid4

import pytest
from zuno_edu.domain.policies import require_recent_mfa
from zuno_edu.interfaces.api.identity import BROWSER_COOKIE, CSRF_COOKIE, SESSION_COOKIE
from zuno_edu.modules.identity.domain import AuthError, Role

Harness = importlib.import_module("test_authentication_service").Harness
PASSWORD = importlib.import_module("test_authentication_service").PASSWORD
client_for = importlib.import_module("test_http").client_for


def test_activity_expiry_and_successful_stepup() -> None:
    h = Harness()
    subject = h.account(Role.ADMIN)
    h.activate(subject)
    old = h.cookies[-1]
    assert old
    h.context = replace(h.context, session_token=old)
    original = h.clock.now()
    h.clock.instant += timedelta(minutes=20)
    h.service.get_session(h.context, {})
    h.clock.instant += timedelta(minutes=10)
    assert h.service.get_session(h.context, {}).user_id == subject
    actor = h.service.get_principal(h.context, uuid4())
    assert actor.mfa_verified_at == original
    with pytest.raises(AuthError, match="FORBIDDEN"):
        require_recent_mfa(actor.mfa_verified_at, h.clock.now())
    before = len(h.cookies)
    outcome = h.service.login(
        h.context, {"identifier": str(h.store.state.accounts[subject].email), "password": PASSWORD}
    )
    assert len(h.cookies) == before and outcome.challenge_token
    token = outcome.challenge_token
    with pytest.raises(AuthError):
        h.service.verify_mfa(h.context, {"challenge_token": token, "code": "000000"})
    assert len(h.cookies) == before
    assert h.service.get_session(h.context, {}).user_id == subject
    h.service.verify_mfa(h.context, {"challenge_token": token, "code": h.code(token)})
    new = h.cookies[-1]
    assert new and new != old
    current = replace(h.context, session_token=new)
    refreshed = h.service.get_principal(current, uuid4())
    assert refreshed.mfa_verified_at == h.clock.now()
    require_recent_mfa(refreshed.mfa_verified_at, h.clock.now())
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.service.verify_mfa(current, {"challenge_token": token, "code": h.code(token)})
    with pytest.raises(AuthError, match="UNAUTHENTICATED"):
        h.service.get_session(h.context, {})


def test_pending_and_failed_mfa_preserve_http_cookie_and_session() -> None:
    h = Harness()
    subject = h.account(Role.ADMIN)
    h.activate(subject)
    secret = h.cookies[-1]
    assert secret
    h.clock.instant += timedelta(minutes=20)
    with client_for(h) as client:
        client.cookies.set(BROWSER_COOKIE, h.browser)
        client.cookies.set(SESSION_COOKIE, secret)
        assert client.get("/api/v1/account/session").status_code == 200
        h.clock.instant += timedelta(minutes=10)
        assert client.get("/api/v1/account/session").status_code == 200
        headers = {"Origin": "https://zuno.test", "X-CSRF-Token": client.cookies[CSRF_COOKIE]}
        response = client.post(
            "/api/v1/auth/sessions",
            json={"identifier": str(h.store.state.accounts[subject].email), "password": PASSWORD},
            headers=headers,
        )
        token = response.json()["challenge_token"]
        assert response.status_code == 200
        assert not any(SESSION_COOKIE in c for c in response.headers.get_list("set-cookie"))
        failed = client.post(
            "/api/v1/auth/mfa/verifications",
            json={"challenge_token": token, "code": "000000"},
            headers=headers,
        )
        assert failed.status_code == 401
        assert not any(SESSION_COOKIE in c for c in failed.headers.get_list("set-cookie"))
        assert client.cookies[SESSION_COOKIE] == secret
        assert client.get("/api/v1/account/session").status_code == 200
        original = next(
            s for s in h.store.state.sessions.values() if s.token_hash == h.tokens.digest(secret)
        )
        assert original.revoked_at is None and original.mfa_verified_at == original.created_at


def test_foreign_second_factor_does_not_replace_current_session() -> None:
    h = Harness()
    original, foreign = h.account(Role.ADMIN), h.account(Role.ADMIN)
    h.activate(original)
    original_token = h.cookies[-1]
    h.activate(foreign)
    h.context = replace(h.context, session_token=original_token)
    h.clock.instant += timedelta(seconds=30)
    outcome = h.service.login(
        h.context, {"identifier": str(h.store.state.accounts[foreign].email), "password": PASSWORD}
    )
    assert outcome.challenge_token
    before = list(h.cookies)
    with pytest.raises(AuthError, match="FORBIDDEN"):
        h.service.verify_mfa(
            h.context,
            {"challenge_token": outcome.challenge_token, "code": h.code(outcome.challenge_token)},
        )
    assert before == h.cookies
    assert h.service.get_session(h.context, {}).user_id == original
