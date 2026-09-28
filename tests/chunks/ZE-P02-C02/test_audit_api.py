import importlib
from collections.abc import Callable
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from fastapi.testclient import TestClient
from test_authorization_audit import NOW, seed, service
from zuno_edu.bootstrap.app import create_app
from zuno_edu.infrastructure.persistence.database import Database
from zuno_edu.infrastructure.persistence.tables import (
    audit_records,
    credentials,
    mfa_factors,
    sessions,
)
from zuno_edu.interfaces.api.identity import BROWSER_COOKIE, SESSION_COOKIE
from zuno_edu.modules.identity.application.service import AuthenticationService
from zuno_edu.modules.operations.infrastructure.audit import IdentityAuditWriter

Harness = importlib.import_module("test_authentication_service").Harness


@pytest.mark.parametrize(
    "role,privileges,expected",
    [
        ("admin", ("audit_admin",), 200),
        ("admin", ("identity_admin",), 403),
        ("teacher", (), 403),
        ("student", (), 403),
        ("parent", (), 403),
    ],
)
def test_direct_audit_api_and_forged_input(
    db: Database, role: str, privileges: tuple[str, ...], expected: int
) -> None:
    h = Harness()
    actor = seed(db, role, privileges)
    raw_token = h.tokens.issue("session", actor.account_id, timedelta(days=1))
    with db.engine.begin() as c:
        c.execute(
            sessions.update()
            .where(sessions.c.id == actor.session_id)
            .values(token_hash=raw_token.token_hash)
        )

    def factory(cookie: Callable[[str | None], None], request_id: UUID) -> AuthenticationService:
        return AuthenticationService(
            lambda: db.identity_transaction(
                IdentityAuditWriter(h.clock, request_id), lambda *_: None, h.clock
            ),
            h.passwords,
            h.tokens,
            h.verifier,
            h.keys,
            h.security,
            h.abuse,
            h.clock,
            cookie,
            lambda _: True,
            h.hash,
        )

    app = create_app(factory, h.security, lambda: service(db, h.clock))
    query = {
        "from": (NOW - timedelta(days=1)).isoformat(),
        "to": (NOW + timedelta(days=1)).isoformat(),
    }
    with TestClient(app, base_url="https://zuno.test") as client:
        client.cookies.set(BROWSER_COOKIE, h.browser)
        assert client.get("/api/v1/admin/audit", params=query).status_code == 401
        client.cookies.set(SESSION_COOKIE, raw_token.value)
        response = client.get(
            "/api/v1/admin/audit",
            params=query,
            headers={"X-Role": "admin", "X-Privileges": "audit_admin"},
        )
        assert response.status_code == expected
        assert response.headers["cache-control"] == "no-store"
        for key in ("role", "family_id", "mfa_verified_at", "privileges", "principal"):
            assert (
                client.get("/api/v1/admin/audit", params={**query, key: "forged"}).status_code
                == 422
            )
        for invalid in (
            {"limit": "101"},
            {"limit": "0"},
            {"to": (NOW + timedelta(days=40)).isoformat()},
            {"from": "2026-09-25T00:00:00"},
        ):
            assert client.get("/api/v1/admin/audit", params={**query, **invalid}).status_code == 422
        if expected == 200:
            second = client.get("/api/v1/admin/audit", params=query)
            item = second.json()["items"][0]
            assert set(item) == {
                "id",
                "actor_id",
                "action",
                "resource_type",
                "resource_id",
                "occurred_at",
                "outcome",
                "request_id",
                "reason",
            }
            assert "metadata" not in second.text and raw_token.value not in second.text
            # Activity keeps the normal session alive; MFA independently expires.
            h.clock.instant += timedelta(minutes=20)
            assert client.get("/api/v1/account/session").status_code == 200
            h.clock.instant += timedelta(minutes=10)
            assert client.get("/api/v1/admin/audit", params=query).status_code == 403
            assert client.get("/api/v1/account/session").status_code == 200


def test_real_stepup_restores_audit_without_losing_ordinary_session(db: Database) -> None:
    h = Harness()
    actor = seed(db)
    token = h.tokens.issue("session", actor.account_id, timedelta(days=1))
    setup = h.verifier.generate_setup("synthetic@example.org")
    with db.engine.begin() as c:
        c.execute(
            sessions.update()
            .where(sessions.c.id == actor.session_id)
            .values(token_hash=token.token_hash)
        )
        c.execute(
            credentials.insert().values(
                account_id=actor.account_id, password_hash=h.hash, changed_at=NOW, failed_attempts=0
            )
        )
        c.execute(
            mfa_factors.insert().values(
                id=uuid4(),
                account_id=actor.account_id,
                secret_ciphertext=setup.secret_reference,
                encryption_key_version=setup.key_version,
                status="active",
                activated_at=NOW,
            )
        )

    def factory(cookie: Callable[[str | None], None], request_id: UUID) -> AuthenticationService:
        return AuthenticationService(
            lambda: db.identity_transaction(
                IdentityAuditWriter(h.clock, request_id), lambda *_: None, h.clock
            ),
            h.passwords,
            h.tokens,
            h.verifier,
            h.keys,
            h.security,
            h.abuse,
            h.clock,
            cookie,
            lambda _: True,
            h.hash,
        )

    query = {
        "from": (NOW - timedelta(days=1)).isoformat(),
        "to": (NOW + timedelta(days=1)).isoformat(),
    }
    with TestClient(
        create_app(factory, h.security, lambda: service(db, h.clock)), base_url="https://zuno.test"
    ) as client:
        client.cookies.set(BROWSER_COOKIE, h.browser, domain="zuno.test", path="/")
        client.cookies.set(SESSION_COOKIE, token.value, domain="zuno.test", path="/")
        h.clock.instant += timedelta(minutes=20)
        assert client.get("/api/v1/account/session").status_code == 200
        h.clock.instant += timedelta(minutes=10)
        assert client.get("/api/v1/admin/audit", params=query).status_code == 403
        headers = {"Origin": "https://zuno.test", "X-CSRF-Token": h.security.csrf(h.browser)}
        result = client.post(
            "/api/v1/auth/sessions",
            json={
                "identifier": f"{actor.account_id}@example.org",
                "password": importlib.import_module("test_authentication_service").PASSWORD,
            },
            headers=headers,
        )
        assert result.status_code == 200
        challenge = result.json()["challenge_token"]
        assert client.cookies[SESSION_COOKIE] == token.value
        seed_bytes = h.keys.open(setup.secret_reference, b"identity-totp-v1")
        code = TOTP(seed_bytes, 6, hashes.SHA1(), 30).generate(h.clock.now().timestamp()).decode()
        wrong = "000000" if code != "000000" else "111111"
        failed = client.post(
            "/api/v1/auth/mfa/verifications",
            json={"challenge_token": challenge, "code": wrong},
            headers=headers,
        )
        assert failed.status_code == 401
        assert client.cookies[SESSION_COOKIE] == token.value
        assert client.get("/api/v1/account/session").status_code == 200
        with db.engine.connect() as c:
            stored = (
                c.execute(sa.select(sessions).where(sessions.c.id == actor.session_id))
                .mappings()
                .one()
            )
            assert stored["mfa_verified_at"] == NOW and stored["revoked_at"] is None
        verified = client.post(
            "/api/v1/auth/mfa/verifications",
            json={"challenge_token": challenge, "code": code},
            headers=headers,
        )
        assert verified.status_code == 200
        with db.engine.connect() as c:
            proof = (
                c.execute(
                    sa.select(audit_records).where(
                        audit_records.c.action == "authentication.mfa_verified"
                    )
                )
                .mappings()
                .one()
            )
            assert str(proof["request_id"]) == verified.headers["X-Request-ID"]
            assert proof["actor_id"] == actor.account_id
        assert client.cookies[SESSION_COOKIE] != token.value
        assert client.get("/api/v1/admin/audit", params=query).status_code == 200
        with db.engine.connect() as c:
            stored = (
                c.execute(
                    sa.select(sessions).where(
                        sessions.c.token_hash == h.tokens.digest(client.cookies[SESSION_COOKIE])
                    )
                )
                .mappings()
                .one()
            )
            assert stored["mfa_verified_at"] == h.clock.now()
