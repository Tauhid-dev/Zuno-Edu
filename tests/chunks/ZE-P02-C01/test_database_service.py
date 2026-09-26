"""Application acceptance on PostgreSQL, including concurrent enrolment and rollback."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import AbstractContextManager
from datetime import UTC, datetime
from uuid import uuid4

import pytest
import sqlalchemy as sa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from sqlalchemy.orm import Session
from test_authentication_service import PASSWORD, Harness
from zuno_edu.infrastructure.persistence.database import AuditRecord, Database
from zuno_edu.infrastructure.persistence.repository import IntegrationRepository
from zuno_edu.infrastructure.persistence.tables import (
    accounts,
    credentials,
    idempotency_records,
    mfa_challenges,
    mfa_factors,
    one_time_tokens,
    outbox,
)
from zuno_edu.modules.identity.application.ports import IdentityTransaction
from zuno_edu.modules.identity.domain import AuthError
from zuno_edu.modules.identity.infrastructure.notifications import IdentityNotificationWriter
from zuno_edu.modules.operations.domain.delivery import OutboxEvent


def harness(db: Database) -> tuple[Harness, str]:
    h = Harness()
    h.clock.instant = datetime.now(UTC)
    subject = uuid4()
    with db.engine.begin() as conn:
        conn.execute(
            accounts.insert().values(
                id=subject,
                role="teacher",
                email=f"{subject}@example.org",
                display_name="Synthetic",
                status="active",
            )
        )
        conn.execute(
            credentials.insert().values(
                account_id=subject,
                password_hash=h.hash,
                changed_at=h.clock.now(),
            )
        )

    def audit(session: Session, records: tuple[AuditRecord, ...]) -> None:
        # Test-only durable sink demonstrates shared-transaction commit/rollback.
        for record in records:
            IntegrationRepository(session).append_event(
                OutboxEvent(
                    record.id,
                    "test_audit",
                    record.id,
                    1,
                    record.action,
                    h.clock.now(),
                )
            )

    def transaction() -> AbstractContextManager[IdentityTransaction]:
        return db.identity_transaction(audit, IdentityNotificationWriter(h.keys, h.clock), h.clock)

    h.service._transactions = transaction
    return h, f"{subject}@example.org"


def test_concurrent_enrolment_returns_secret_once_and_confirmation_consumes(db: Database) -> None:
    h, email = harness(db)
    outcome = h.service.login(h.context, {"identifier": email, "password": PASSWORD})
    assert outcome.setup_token
    body = {
        "password": PASSWORD,
        "setup_token": outcome.setup_token,
        "Idempotency-Key": str(uuid4()),
    }

    def enrol() -> str:
        try:
            return h.service.enrol_mfa(h.context, body).otpauth_uri
        except AuthError as error:
            return error.code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: enrol(), range(2)))
    assert results.count("MFA_REPLAY") == 1
    assert sum(result.startswith("otpauth://") for result in results) == 1
    with db.engine.connect() as conn:
        assert conn.scalar(sa.select(sa.func.count()).select_from(mfa_factors)) == 1
        row = conn.execute(sa.select(mfa_factors)).mappings().one()
        seed = h.keys.open(row["secret_ciphertext"], b"identity-totp-v1")
        assert conn.scalar(sa.select(idempotency_records.c.result_ciphertext)) is None
    code = TOTP(seed, 6, hashes.SHA1(), 30).generate(h.clock.now().timestamp()).decode()
    result = h.service.confirm_mfa(h.context, {"setup_token": outcome.setup_token, "code": code})
    assert len(result.recovery_codes) == 10 and result.session.role == "teacher"
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.service.confirm_mfa(h.context, {"setup_token": outcome.setup_token, "code": code})


def test_email_intent_is_encrypted_and_rollback_is_atomic(db: Database) -> None:
    h, email = harness(db)
    h.service.request_password_reset(h.context, {"email": email})
    with db.engine.connect() as conn:
        token = conn.execute(sa.select(one_time_tokens)).mappings().one()
        payload = h.keys.open(
            token["payload_ciphertext"], b"identity-notification-v1:" + token["id"].bytes
        )
        assert email.encode() in payload and email.encode() not in token["payload_ciphertext"]
        event = (
            conn.execute(sa.select(outbox).where(outbox.c.event_type == "identity.email_requested"))
            .mappings()
            .one()
        )
        assert event["payload"] == {"token_id": str(token["id"])}

    def fail_audit(session: Session, records: tuple[AuditRecord, ...]) -> None:
        raise RuntimeError("synthetic audit failure")

    def transaction() -> AbstractContextManager[IdentityTransaction]:
        return db.identity_transaction(
            fail_audit, IdentityNotificationWriter(h.keys, h.clock), h.clock
        )

    h.service._transactions = transaction
    with pytest.raises(RuntimeError, match="audit failure"):
        h.service.request_password_reset(h.context, {"email": email})
    with db.engine.connect() as conn:
        assert conn.scalar(sa.select(sa.func.count()).select_from(one_time_tokens)) == 1
        assert conn.scalar(sa.select(sa.func.count()).select_from(outbox)) == 2


def test_reset_invalidates_previously_issued_setup_through_service(db: Database) -> None:
    import json

    h, email = harness(db)
    outcome = h.service.login(h.context, {"identifier": email, "password": PASSWORD})
    assert outcome.setup_token
    h.service.request_password_reset(h.context, {"email": email})
    with db.engine.connect() as conn:
        token = conn.execute(sa.select(one_time_tokens)).mappings().one()
    protected = h.keys.open(
        token["payload_ciphertext"], b"identity-notification-v1:" + token["id"].bytes
    )
    h.service.reset_password(
        h.context,
        {
            "token": json.loads(protected)["token"],
            "new_password": "New synthetic passphrase 123!",
        },
    )
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.service.enrol_mfa(
            h.context,
            {
                "password": "New synthetic passphrase 123!",
                "setup_token": outcome.setup_token,
                "Idempotency-Key": str(uuid4()),
            },
        )
    with db.engine.connect() as conn:
        assert conn.scalar(sa.select(mfa_challenges.c.consumed_at)) is not None
