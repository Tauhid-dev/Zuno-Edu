"""SQLAlchemy identity mappers with account-first row locking."""

from collections.abc import Callable
from datetime import datetime
from typing import Any, cast
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from zuno_edu.infrastructure.persistence.tables import (
    accounts,
    credentials,
    idempotency_records,
    mfa_challenges,
    mfa_factors,
    mfa_recovery_codes,
    one_time_tokens,
    sessions,
)
from zuno_edu.modules.identity.application.ports import (
    AccountCredentials,
    IssuedToken,
    SelfAuthScope,
)
from zuno_edu.modules.identity.domain import (
    Account,
    AccountStatus,
    AuthError,
    Credential,
    MfaChallenge,
    MfaFactor,
    RecoveryCode,
    Role,
    RoleGrant,
)
from zuno_edu.modules.identity.domain import (
    Session as IdentitySession,
)
from zuno_edu.shared.persistence import Clock, SystemClock, require_instant


def _lock_account(session: Session, account_id: UUID) -> None:
    existing = session.execute(
        sa.select(accounts.c.id).where(accounts.c.id == account_id).with_for_update()
    ).scalar_one_or_none()
    if existing is None:
        raise AuthError("NOT_FOUND")


def _account(row: sa.RowMapping) -> Account:
    return Account(
        row["id"],
        RoleGrant(Role(row["role"]), frozenset(row["admin_privileges"])),
        AccountStatus(row["status"]),
        row["email"],
        row["display_name"],
        row["mfa_enabled"],
        row["version"],
    )


def _credential(row: sa.RowMapping) -> Credential:
    return Credential(
        row["account_id"],
        row["password_hash"],
        row["changed_at"],
        row["failed_attempts"],
        row["locked_until"],
    )


class SqlAlchemyUsers:
    def __init__(self, session: Session) -> None:
        self.session = session

    def find_login(self, identifier: str) -> AccountCredentials | None:
        # Guardian provisioning exposes the opaque Account UUID as the student username.
        # A profile ID, adult account ID, or account without credentials cannot sign in.
        predicate = accounts.c.email == identifier
        try:
            student_id = UUID(identifier)
        except ValueError:
            pass
        else:
            predicate = sa.and_(accounts.c.id == student_id, accounts.c.role == "student")
        account_id = self.session.execute(
            sa.select(accounts.c.id).where(predicate)
        ).scalar_one_or_none()
        if account_id is None:
            return None
        _lock_account(self.session, account_id)
        row = (
            self.session.execute(
                sa.select(accounts, credentials)
                .join(credentials, credentials.c.account_id == accounts.c.id)
                .where(accounts.c.id == account_id, predicate)
                .with_for_update(of=credentials)
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        return AccountCredentials(_account(row), _credential(row))

    def get_scoped(self, id: UUID, scope: SelfAuthScope) -> Account | None:
        if id != scope.account_id:
            return None
        _lock_account(self.session, id)
        row = (
            self.session.execute(sa.select(accounts).where(accounts.c.id == id))
            .mappings()
            .one_or_none()
        )
        return _account(row) if row else None

    def save(self, account: Account, expected_version: int) -> None:
        result = self.session.execute(
            accounts.update()
            .where(accounts.c.id == account.id, accounts.c.version == expected_version)
            .values(
                role=account.role.role.value,
                admin_privileges=list(account.role.admin_privileges),
                status=account.status.value,
                email=account.email,
                display_name=account.display_name,
                mfa_enabled=account.mfa_enabled,
                version=account.version,
            )
        )
        if int(cast(Any, result).rowcount or 0) != 1:
            raise RuntimeError("VERSION_CONFLICT")


class SqlAlchemySessions:
    def __init__(self, session: Session, clock: Clock | None = None) -> None:
        self.session = session
        self.clock = clock or SystemClock()

    def _domain(self, row: sa.RowMapping) -> IdentitySession:
        account = self.session.execute(
            sa.select(accounts.c.role).where(accounts.c.id == row["account_id"])
        ).scalar_one()
        return IdentitySession(
            row["id"],
            row["account_id"],
            row["token_hash"],
            row["created_at"],
            row["last_seen_at"],
            row["expires_at"],
            account in {"teacher", "admin"},
            row["revoked_at"],
            row["mfa_verified_at"],
            row["device_label"],
        )

    def find_active(self, token_hash: bytes, now: datetime) -> IdentitySession | None:
        account_id = self.session.execute(
            sa.select(sessions.c.account_id).where(sessions.c.token_hash == token_hash)
        ).scalar_one_or_none()
        if account_id is None:
            return None
        _lock_account(self.session, account_id)
        now = max(require_instant(now), self.clock.now())
        row = (
            self.session.execute(
                sa.select(sessions)
                .where(
                    sessions.c.token_hash == token_hash,
                    sessions.c.revoked_at.is_(None),
                    sessions.c.expires_at > require_instant(now),
                )
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        session = self._domain(row)
        return session if session.is_active(now) else None

    def list_owned(self, user_id: UUID, scope: SelfAuthScope) -> tuple[IdentitySession, ...]:
        if user_id != scope.account_id:
            return ()
        return tuple(
            self._domain(row)
            for row in self.session.execute(
                sa.select(sessions).where(sessions.c.account_id == user_id)
            ).mappings()
        )

    def revoke_all(self, user_id: UUID) -> int:
        return (
            cast(
                Any,
                self.session.execute(
                    sessions.update()
                    .where(sessions.c.account_id == user_id, sessions.c.revoked_at.is_(None))
                    .values(revoked_at=sa.func.now())
                ),
            ).rowcount
            or 0
        )

    def save(self, session: IdentitySession) -> None:
        self.session.execute(
            insert(sessions)
            .values(
                id=session.id,
                account_id=session.user_id,
                token_hash=session.token_hash,
                created_at=session.created_at,
                last_seen_at=session.last_seen_at,
                expires_at=session.expires_at,
                revoked_at=session.revoked_at,
                mfa_verified_at=session.mfa_verified_at,
                device_label=session.device_label,
            )
            .on_conflict_do_update(
                index_elements=[sessions.c.id],
                set_=dict(
                    token_hash=session.token_hash,
                    last_seen_at=session.last_seen_at,
                    revoked_at=session.revoked_at,
                    mfa_verified_at=session.mfa_verified_at,
                ),
            )
        )

    def consume_token(self, token_hash: bytes, purpose: str, now: datetime) -> UUID:
        account_id = self.session.execute(
            sa.select(one_time_tokens.c.account_id).where(
                one_time_tokens.c.token_hash == token_hash, one_time_tokens.c.purpose == purpose
            )
        ).scalar_one_or_none()
        if account_id is None:
            raise AuthError("INVALID_STATE")
        _lock_account(self.session, account_id)
        now = max(require_instant(now), self.clock.now())
        row = (
            self.session.execute(
                sa.select(one_time_tokens)
                .where(
                    one_time_tokens.c.token_hash == token_hash,
                    one_time_tokens.c.purpose == purpose,
                    one_time_tokens.c.expires_at > require_instant(now),
                    one_time_tokens.c.consumed_at.is_(None),
                )
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            raise AuthError("INVALID_STATE")
        self.session.execute(
            one_time_tokens.update()
            .where(one_time_tokens.c.id == row["id"])
            .values(consumed_at=require_instant(now))
        )
        return cast(UUID, row["account_id"])


class SqlAlchemyMfa:
    def __init__(self, session: Session, clock: Clock | None = None) -> None:
        self.session = session
        self.clock = clock or SystemClock()

    def _account_lock(self, account_id: UUID, scope: SelfAuthScope) -> None:
        if account_id != scope.account_id:
            raise RuntimeError("NOT_FOUND")
        _lock_account(self.session, account_id)

    def _factor(self, row: sa.RowMapping) -> MfaFactor:
        return MfaFactor(
            row["id"],
            row["account_id"],
            row["secret_ciphertext"],
            row["encryption_key_version"],
            row["status"],
            row["last_accepted_step"],
            row["activated_at"],
            row["revoked_at"],
            row["version"],
        )

    def get_factor_for_update(self, account_id: UUID, scope: SelfAuthScope) -> MfaFactor | None:
        self._account_lock(account_id, scope)
        row = (
            self.session.execute(
                sa.select(mfa_factors)
                .where(mfa_factors.c.account_id == account_id, mfa_factors.c.status == "active")
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        return self._factor(row) if row else None

    def get_pending_factor_for_update(
        self, account_id: UUID, setup_token_hash: bytes, browser_hash: bytes, scope: SelfAuthScope
    ) -> MfaFactor | None:
        self._account_lock(account_id, scope)
        row = (
            self.session.execute(
                sa.select(mfa_challenges)
                .where(
                    mfa_challenges.c.account_id == account_id,
                    mfa_challenges.c.token_hash == setup_token_hash,
                    mfa_challenges.c.browser_binding_hash == browser_hash,
                    mfa_challenges.c.purpose == "setup",
                    mfa_challenges.c.consumed_at.is_(None),
                    mfa_challenges.c.expires_at > self.clock.now(),
                    mfa_challenges.c.attempts < 5,
                )
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        if row is None or row["factor_id"] is None:
            return None
        factor = (
            self.session.execute(
                sa.select(mfa_factors)
                .where(
                    mfa_factors.c.id == row["factor_id"],
                    mfa_factors.c.account_id == account_id,
                    mfa_factors.c.status == "pending",
                )
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        return self._factor(factor) if factor else None

    def invalidate_pending_setup(self, account_id: UUID, scope: SelfAuthScope) -> int:
        self._account_lock(account_id, scope)
        rows = (
            self.session.execute(
                sa.select(mfa_factors.c.id)
                .where(mfa_factors.c.account_id == account_id, mfa_factors.c.status == "pending")
                .with_for_update()
            )
            .scalars()
            .all()
        )
        if rows:
            self.session.execute(
                mfa_factors.update()
                .where(mfa_factors.c.id.in_(rows))
                .values(status="revoked", revoked_at=sa.func.now())
            )
            self.session.execute(
                mfa_challenges.update()
                .where(
                    mfa_challenges.c.account_id == account_id, mfa_challenges.c.factor_id.in_(rows)
                )
                .values(consumed_at=sa.func.now())
            )
        return len(rows)

    def get_challenge_for_update(
        self, token_hash: bytes, browser_hash: bytes
    ) -> MfaChallenge | None:
        account_id = self.session.execute(
            sa.select(mfa_challenges.c.account_id).where(
                mfa_challenges.c.token_hash == token_hash,
                mfa_challenges.c.browser_binding_hash == browser_hash,
            )
        ).scalar_one_or_none()
        if account_id is None:
            return None
        _lock_account(self.session, account_id)
        row = (
            self.session.execute(
                sa.select(mfa_challenges)
                .where(
                    mfa_challenges.c.token_hash == token_hash,
                    mfa_challenges.c.browser_binding_hash == browser_hash,
                )
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        return MfaChallenge(
            row["id"],
            row["account_id"],
            row["token_hash"],
            row["purpose"],
            row["expires_at"],
            row["browser_binding_hash"],
            row["factor_id"],
            row["attempts"],
            row["consumed_at"],
        )

    def find_recovery_for_update(self, factor_id: UUID, code_hash: bytes) -> RecoveryCode | None:
        row = (
            self.session.execute(
                sa.select(mfa_recovery_codes)
                .where(
                    mfa_recovery_codes.c.factor_id == factor_id,
                    mfa_recovery_codes.c.code_hash == code_hash,
                )
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        return (
            RecoveryCode(row["id"], row["factor_id"], row["code_hash"], row["consumed_at"])
            if row
            else None
        )

    def save_factor(self, factor: MfaFactor, expected_version: int) -> None:
        values = dict(
            id=factor.id,
            account_id=factor.account_id,
            secret_ciphertext=factor.secret_reference,
            encryption_key_version=factor.encryption_key_version,
            status=factor.status,
            last_accepted_step=factor.last_accepted_step,
            activated_at=factor.activated_at,
            revoked_at=factor.revoked_at,
            version=factor.version,
        )
        if expected_version == 0:
            self.session.execute(mfa_factors.insert().values(values))
            return
        result = self.session.execute(
            mfa_factors.update()
            .where(mfa_factors.c.id == factor.id, mfa_factors.c.version == expected_version)
            .values(**{key: value for key, value in values.items() if key != "id"})
        )
        if int(cast(Any, result).rowcount or 0) != 1:
            raise RuntimeError("VERSION_CONFLICT")

    def save_challenge(self, challenge: MfaChallenge) -> None:
        values = dict(
            id=challenge.id,
            account_id=challenge.account_id,
            token_hash=challenge.token_hash,
            purpose=challenge.purpose,
            browser_binding_hash=challenge.browser_binding_hash,
            expires_at=challenge.expires_at,
            attempts=challenge.attempts,
            consumed_at=challenge.consumed_at,
            factor_id=challenge.factor_id,
        )
        result = self.session.execute(
            mfa_challenges.update()
            .where(mfa_challenges.c.id == challenge.id)
            .values(
                attempts=challenge.attempts,
                consumed_at=challenge.consumed_at,
                factor_id=challenge.factor_id,
            )
        )
        if int(cast(Any, result).rowcount or 0) == 0:
            self.session.execute(mfa_challenges.insert().values(values))

    def consume_recovery(self, code: RecoveryCode) -> None:
        self.session.execute(
            mfa_recovery_codes.update()
            .where(mfa_recovery_codes.c.id == code.id)
            .values(consumed_at=code.consumed_at)
        )

    def save_recovery_codes(
        self, factor_id: UUID, codes: tuple[RecoveryCode, ...], scope: SelfAuthScope
    ) -> None:
        self._require_owned_factor(factor_id, scope)
        if any(code.factor_id != factor_id for code in codes):
            raise AuthError("NOT_FOUND")
        self.session.execute(
            sa.insert(mfa_recovery_codes),
            [
                {
                    "id": code.id,
                    "factor_id": factor_id,
                    "code_hash": code.code_hash,
                    "consumed_at": code.consumed_at,
                }
                for code in codes
            ],
        )

    def revoke_recovery_codes(self, factor_id: UUID, scope: SelfAuthScope) -> int:
        self._require_owned_factor(factor_id, scope)
        return (
            cast(
                Any,
                self.session.execute(
                    mfa_recovery_codes.update()
                    .where(
                        mfa_recovery_codes.c.factor_id == factor_id,
                        mfa_recovery_codes.c.consumed_at.is_(None),
                    )
                    .values(consumed_at=sa.func.now())
                ),
            ).rowcount
            or 0
        )

    def _require_owned_factor(self, factor_id: UUID, scope: SelfAuthScope) -> None:
        self._account_lock(scope.account_id, scope)
        owned = self.session.execute(
            sa.select(mfa_factors.c.id)
            .where(mfa_factors.c.id == factor_id, mfa_factors.c.account_id == scope.account_id)
            .with_for_update()
        ).scalar_one_or_none()
        if owned is None:
            raise AuthError("NOT_FOUND")


class SqlAlchemyIdentityTransaction:
    """Identity view over the existing request-scoped SQLAlchemy transaction."""

    def __init__(
        self,
        session: Session,
        commit: Callable[[str, UUID | None], None] | None = None,
        notification: Callable[[Session, Account, IssuedToken], None] | None = None,
        clock: Clock | None = None,
    ) -> None:
        self.session = session
        self._commit = commit
        self._notification = notification
        self.users = SqlAlchemyUsers(session)
        self.sessions = SqlAlchemySessions(session, clock)
        self.mfa = SqlAlchemyMfa(session, clock)

    def __enter__(self) -> SqlAlchemyIdentityTransaction:
        return self

    def __exit__(self, *args: object) -> None:
        self.session.rollback()

    def credential(self, account_id: UUID, scope: SelfAuthScope) -> Credential:
        if account_id != scope.account_id:
            raise RuntimeError("NOT_FOUND")
        _lock_account(self.session, account_id)
        row = (
            self.session.execute(
                sa.select(credentials)
                .where(credentials.c.account_id == account_id)
                .with_for_update()
            )
            .mappings()
            .one()
        )
        return _credential(row)

    def save_credential(self, credential: Credential) -> None:
        _lock_account(self.session, credential.user_id)
        values = dict(
            account_id=credential.user_id,
            password_hash=credential.password_hash,
            changed_at=credential.changed_at,
            failed_attempts=credential.failed_attempts,
            locked_until=credential.locked_until,
        )
        self.session.execute(
            insert(credentials)
            .values(values)
            .on_conflict_do_update(index_elements=[credentials.c.account_id], set_=values)
        )

    def store_token(self, token: IssuedToken) -> None:
        self.session.execute(
            one_time_tokens.insert().values(
                id=uuid4(),
                account_id=token.subject,
                purpose=token.purpose,
                token_hash=token.token_hash,
                expires_at=token.expires_at,
            )
        )

    def invalidate_tokens(self, account_id: UUID) -> None:
        _lock_account(self.session, account_id)
        self.session.execute(
            mfa_challenges.update()
            .where(
                mfa_challenges.c.account_id == account_id,
                mfa_challenges.c.consumed_at.is_(None),
            )
            .values(consumed_at=sa.func.now())
        )
        self.session.execute(
            one_time_tokens.update()
            .where(
                one_time_tokens.c.account_id == account_id, one_time_tokens.c.consumed_at.is_(None)
            )
            .values(consumed_at=sa.func.now())
        )

    def enrolment_digest(self, account_id: UUID, key: UUID, now: datetime) -> bytes | None:
        _lock_account(self.session, account_id)
        self.session.execute(
            idempotency_records.delete().where(
                idempotency_records.c.principal_scope == str(account_id),
                idempotency_records.c.operation_id == "API-AUTH-MFA-ENROL",
                idempotency_records.c.key == key,
                idempotency_records.c.expires_at <= require_instant(now),
            )
        )
        row = self.session.execute(
            sa.select(idempotency_records.c.request_hash)
            .where(
                idempotency_records.c.principal_scope == str(account_id),
                idempotency_records.c.operation_id == "API-AUTH-MFA-ENROL",
                idempotency_records.c.key == key,
                idempotency_records.c.expires_at > require_instant(now),
            )
            .with_for_update()
        ).scalar_one_or_none()
        return row

    def record_enrolment(
        self, account_id: UUID, key: UUID, digest: bytes, expires: datetime
    ) -> None:
        self.session.execute(
            idempotency_records.insert().values(
                principal_scope=str(account_id),
                operation_id="API-AUTH-MFA-ENROL",
                key=key,
                request_hash=digest,
                result_ciphertext=None,
                status="committed",
                expires_at=expires,
            )
        )

    def notify(self, account: Account, token: IssuedToken) -> None:
        if self._notification is None:
            raise RuntimeError("Durable notification writer must be composed")
        self._notification(self.session, account, token)

    def commit(self, action: str, account_id: UUID | None) -> None:
        if self._commit is None:
            raise RuntimeError("Audited unit of work must be composed")
        self._commit(action, account_id)
