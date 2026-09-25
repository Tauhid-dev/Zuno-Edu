"""Real database regressions for the boundaries that serialized fakes cannot prove."""

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from pathlib import Path
from threading import Event
from time import monotonic
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy.exc import IntegrityError
from zuno_edu.infrastructure.persistence.database import Database
from zuno_edu.infrastructure.persistence.tables import (
    accounts,
    credentials,
    mfa_challenges,
    mfa_factors,
    mfa_recovery_codes,
)
from zuno_edu.modules.identity.application.ports import IssuedToken, SelfAuthScope
from zuno_edu.modules.identity.domain import (
    AuthError,
    Credential,
    MfaChallenge,
    MfaFactor,
    RecoveryCode,
)
from zuno_edu.modules.identity.domain import Session as IdentitySession
from zuno_edu.modules.identity.infrastructure.repository import SqlAlchemyIdentityTransaction
from zuno_edu.shared.persistence import FrozenClock

NOW = datetime.now(UTC)
ROOT = Path(__file__).resolve().parents[3]


def seed(db: Database) -> UUID:
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
    return subject


def test_migration_matches_metadata(db: Database) -> None:
    command.check(Config(str(ROOT / "alembic.ini")))


def test_invitation_first_credential_and_scope_denial(db: Database) -> None:
    subject, foreign = seed(db), seed(db)
    factor = MfaFactor(uuid4(), subject, b"encrypted", "v1")
    challenge = MfaChallenge(
        uuid4(), subject, b"token", "setup", NOW + timedelta(minutes=10), b"browser"
    )
    with db.sessions.begin() as session:
        tx = SqlAlchemyIdentityTransaction(session)
        tx.save_credential(Credential(subject, "$argon2id$synthetic", NOW))
        tx.mfa.save_factor(factor, 0)
        tx.mfa.save_challenge(challenge)
    with db.sessions.begin() as session:
        tx = SqlAlchemyIdentityTransaction(session)
        login = tx.users.find_login(f"{subject}@example.org")
        assert login and login.credential.password_hash == "$argon2id$synthetic"
        for action in (
            lambda: tx.mfa.save_recovery_codes(
                factor.id, (RecoveryCode(uuid4(), factor.id, b"hash"),), SelfAuthScope(foreign)
            ),
            lambda: tx.mfa.revoke_recovery_codes(factor.id, SelfAuthScope(foreign)),
        ):
            with pytest.raises(AuthError, match="NOT_FOUND"):
                action()
    with db.engine.connect() as conn:
        assert conn.scalar(sa.select(sa.func.count()).select_from(mfa_recovery_codes)) == 0


def test_password_reset_invalidates_mfa_challenges(db: Database) -> None:
    subject = seed(db)
    with db.sessions.begin() as session:
        tx = SqlAlchemyIdentityTransaction(session)
        for purpose in ("setup", "challenge"):
            tx.mfa.save_challenge(
                MfaChallenge(
                    uuid4(),
                    subject,
                    purpose.encode(),
                    purpose,
                    NOW + timedelta(minutes=5),
                    b"browser",
                )
            )
        tx.invalidate_tokens(subject)
    with db.engine.connect() as conn:
        rows = conn.execute(sa.select(mfa_challenges.c.consumed_at)).scalars().all()
        assert len(rows) == 2 and all(rows)


def test_login_waits_for_reset_and_reads_new_hash(db: Database) -> None:
    subject = seed(db)
    with db.sessions.begin() as session:
        SqlAlchemyIdentityTransaction(session).save_credential(
            Credential(subject, "$argon2id$old", NOW)
        )
    started = Event()

    def login() -> str:
        with db.sessions.begin() as session:
            session.execute(sa.text("SET LOCAL lock_timeout = '5s'"))
            started.set()
            found = SqlAlchemyIdentityTransaction(session).users.find_login(
                f"{subject}@example.org"
            )
            assert found
            return found.credential.password_hash

    with ThreadPoolExecutor(max_workers=1) as executor:
        with db.sessions.begin() as session:
            tx = SqlAlchemyIdentityTransaction(session)
            credential = tx.credential(subject, SelfAuthScope(subject))
            credential.replace("$argon2id$new", NOW)
            tx.save_credential(credential)
            future = executor.submit(login)
            assert started.wait(2)
        assert future.result(timeout=7) == "$argon2id$new"
    with db.engine.connect() as conn:
        assert conn.scalar(sa.select(credentials.c.password_hash)) == "$argon2id$new"


def test_challenge_reader_does_not_hold_challenge_before_account(db: Database) -> None:
    subject = seed(db)
    with db.sessions.begin() as session:
        SqlAlchemyIdentityTransaction(session).mfa.save_challenge(
            MfaChallenge(
                uuid4(), subject, b"token", "setup", NOW + timedelta(minutes=10), b"browser"
            )
        )
    started = Event()

    def confirm() -> bool:
        with db.sessions.begin() as session:
            session.execute(sa.text("SET LOCAL lock_timeout = '5s'"))
            started.set()
            challenge = SqlAlchemyIdentityTransaction(session).mfa.get_challenge_for_update(
                b"token", b"browser"
            )
            assert challenge
            return challenge.consumed_at is not None

    with ThreadPoolExecutor(max_workers=1) as executor:
        with db.sessions.begin() as session:
            tx = SqlAlchemyIdentityTransaction(session)
            tx.users.get_scoped(subject, SelfAuthScope(subject))
            future = executor.submit(confirm)
            assert started.wait(2)
            tx.invalidate_tokens(subject)
        assert future.result(timeout=7)


def test_database_rejects_invalid_role_and_attempts(db: Database) -> None:
    subject = seed(db)
    with pytest.raises(IntegrityError), db.engine.begin() as conn:
        conn.execute(accounts.update().where(accounts.c.id == subject).values(role="owner"))
    with pytest.raises(IntegrityError), db.engine.begin() as conn:
        conn.execute(
            mfa_challenges.insert().values(
                id=uuid4(),
                account_id=subject,
                token_hash=b"token",
                purpose="setup",
                browser_binding_hash=b"browser",
                expires_at=NOW,
                attempts=6,
            )
        )
    with pytest.raises(IntegrityError), db.engine.begin() as conn:
        conn.execute(
            mfa_factors.insert().values(
                id=uuid4(),
                account_id=subject,
                secret_ciphertext=b"ciphertext",
                encryption_key_version="v1",
                status="invalid",
            )
        )


def test_email_less_student_requires_provisioned_credentials(db: Database) -> None:
    subject, adult = seed(db), seed(db)
    with db.engine.begin() as conn:
        conn.execute(
            accounts.update().where(accounts.c.id == subject).values(role="student", email=None)
        )
    with db.sessions.begin() as session:
        tx = SqlAlchemyIdentityTransaction(session)
        assert tx.users.find_login(str(subject)) is None
        tx.save_credential(Credential(subject, "$argon2id$student", NOW))
        tx.save_credential(Credential(adult, "$argon2id$adult", NOW))
        found = tx.users.find_login(str(subject))
        assert found and found.account.email is None
        assert tx.users.find_login(str(adult)) is None


def test_unconfigured_commit_fails_closed_and_context_rolls_back(db: Database) -> None:
    subject = seed(db)
    with db.sessions() as session:
        with pytest.raises(RuntimeError, match="Audited unit of work"):
            with SqlAlchemyIdentityTransaction(session) as tx:
                tx.save_credential(Credential(subject, "$argon2id$synthetic", NOW))
                tx.commit("authentication.test", subject)
    with db.engine.connect() as conn:
        assert conn.scalar(sa.select(sa.func.count()).select_from(credentials)) == 0


@pytest.mark.parametrize("expired,attempts", [(True, 0), (False, 5)])
def test_pending_factor_rejects_expired_or_exhausted_setup(
    db: Database,
    expired: bool,
    attempts: int,
) -> None:
    subject = seed(db)
    clock = FrozenClock(NOW)
    factor = MfaFactor(uuid4(), subject, b"encrypted", "v1")
    with db.sessions.begin() as session:
        tx = SqlAlchemyIdentityTransaction(session, clock=clock)
        tx.mfa.save_factor(factor, 0)
        tx.mfa.save_challenge(
            MfaChallenge(
                uuid4(),
                subject,
                b"token",
                "setup",
                NOW + timedelta(minutes=-1 if expired else 10),
                b"browser",
                factor.id,
                attempts,
            )
        )
    with db.sessions.begin() as session:
        tx = SqlAlchemyIdentityTransaction(session, clock=clock)
        assert (
            tx.mfa.get_pending_factor_for_update(
                subject, b"token", b"browser", SelfAuthScope(subject)
            )
            is None
        )


@pytest.mark.parametrize("kind", ["session", "reset"])
def test_waiting_for_account_lock_cannot_extend_expired_credentials(
    db: Database, kind: str
) -> None:
    subject = seed(db)
    clock = FrozenClock(NOW)
    expiry = NOW + timedelta(seconds=1)
    label = "c01_expiry_" + uuid4().hex
    with db.sessions.begin() as session:
        session.execute(accounts.update().where(accounts.c.id == subject).values(role="parent"))
        tx = SqlAlchemyIdentityTransaction(session, clock=clock)
        if kind == "session":
            tx.sessions.save(IdentitySession(uuid4(), subject, b"token", NOW, NOW, expiry, False))
        else:
            tx.store_token(IssuedToken("secret", b"token", subject, "reset", expiry))
    started = Event()

    def waiting() -> bool:
        with db.sessions.begin() as session:
            session.execute(sa.text("SET LOCAL lock_timeout = '5s'"))
            session.execute(
                sa.text("SELECT set_config('application_name', :name, true)"), {"name": label}
            )
            tx = SqlAlchemyIdentityTransaction(session, clock=clock)
            before_lock = clock.now()
            started.set()
            if kind == "session":
                return tx.sessions.find_active(b"token", before_lock) is None
            try:
                tx.sessions.consume_token(b"token", "reset", before_lock)
            except AuthError as error:
                return error.code == "INVALID_STATE"
            return False

    with ThreadPoolExecutor(max_workers=1) as pool:
        with db.sessions.begin() as session:
            SqlAlchemyIdentityTransaction(session).users.get_scoped(subject, SelfAuthScope(subject))
            future = pool.submit(waiting)
            assert started.wait(2)
            deadline = monotonic() + 3
            with db.engine.connect() as observer:
                while not observer.scalar(
                    sa.text(
                        "SELECT count(*) FROM pg_stat_activity "
                        "WHERE application_name=:name AND wait_event_type='Lock'"
                    ),
                    {"name": label},
                ):
                    assert monotonic() < deadline, "worker never reached account lock"
                    observer.rollback()
                    Event().wait(0.01)
            clock.instant = expiry + timedelta(seconds=1)
        assert future.result(timeout=7)
