"""Transactional port fakes. PostgreSQL verification remains a separate requirement."""

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from threading import RLock
from uuid import UUID

from zuno_edu.modules.identity.application.ports import (
    AccountCredentials,
    IssuedToken,
    SelfAuthScope,
)
from zuno_edu.modules.identity.domain import (
    Account,
    AuthError,
    Credential,
    MfaChallenge,
    MfaFactor,
    RecoveryCode,
    Session,
)
from zuno_edu.shared.persistence import Clock


@dataclass
class State:
    accounts: dict[UUID, Account] = field(default_factory=dict)
    credentials: dict[UUID, Credential] = field(default_factory=dict)
    sessions: dict[UUID, Session] = field(default_factory=dict)
    challenges: dict[UUID, MfaChallenge] = field(default_factory=dict)
    factors: dict[UUID, MfaFactor] = field(default_factory=dict)
    codes: dict[UUID, RecoveryCode] = field(default_factory=dict)
    tokens: dict[bytes, IssuedToken] = field(default_factory=dict)
    used: set[bytes] = field(default_factory=set)
    digests: dict[tuple[UUID, UUID], tuple[bytes, datetime]] = field(default_factory=dict)
    notifications: list[IssuedToken] = field(default_factory=list)
    audit: list[str] = field(default_factory=list)


class Store:
    def __init__(self, clock: Clock) -> None:
        self.state = State()
        self.clock = clock
        self.lock = RLock()
        self.fail_commit = False
        self.uncertain_commit = False

    def transaction(self) -> Transaction:
        return Transaction(self)


class Users:
    def __init__(self, tx: Transaction) -> None:
        self.tx = tx

    def find_login(self, identifier: str) -> AccountCredentials | None:
        for account in self.tx.state.accounts.values():
            if account.email == identifier or (
                account.role.role.value == "student" and str(account.id) == identifier
            ):
                credential = self.tx.state.credentials.get(account.id)
                if credential:
                    return AccountCredentials(account, credential)
        return None

    def get_scoped(self, id: UUID, scope: SelfAuthScope) -> Account | None:
        return self.tx.state.accounts.get(id) if id == scope.account_id else None

    def save(self, account: Account, expected_version: int) -> None:
        self.tx.state.accounts[account.id] = account


class Sessions:
    def __init__(self, tx: Transaction) -> None:
        self.tx = tx

    def find_active(self, token_hash: bytes, now: datetime) -> Session | None:
        return next(
            (
                s
                for s in self.tx.state.sessions.values()
                if s.token_hash == token_hash and s.is_active(now)
            ),
            None,
        )

    def list_owned(self, user_id: UUID, scope: SelfAuthScope) -> tuple[Session, ...]:
        if user_id != scope.account_id:
            raise AuthError("NOT_FOUND")
        return tuple(s for s in self.tx.state.sessions.values() if s.user_id == user_id)

    def revoke_all(self, user_id: UUID) -> int:
        count = 0
        for session in self.tx.state.sessions.values():
            if session.user_id == user_id and session.revoked_at is None:
                session.revoke(self.tx.store.clock.now())
                count += 1
        return count

    def save(self, session: Session) -> None:
        self.tx.state.sessions[session.id] = session

    def consume_token(self, token_hash: bytes, purpose: str, now: datetime) -> UUID:
        token = self.tx.state.tokens.get(token_hash)
        if (
            token is None
            or token.purpose != purpose
            or token.expires_at <= now
            or token_hash in self.tx.state.used
        ):
            raise AuthError("INVALID_STATE")
        self.tx.state.used.add(token_hash)
        return token.subject


class Mfa:
    def __init__(self, tx: Transaction) -> None:
        self.tx = tx

    def get_factor_for_update(self, account_id: UUID, scope: SelfAuthScope) -> MfaFactor | None:
        if account_id != scope.account_id:
            raise AuthError("NOT_FOUND")
        return next(
            (
                f
                for f in self.tx.state.factors.values()
                if f.account_id == account_id and f.status == "active"
            ),
            None,
        )

    def get_pending_factor_for_update(
        self, account_id: UUID, setup_token_hash: bytes, browser_hash: bytes, scope: SelfAuthScope
    ) -> MfaFactor | None:
        if account_id != scope.account_id:
            raise AuthError("NOT_FOUND")
        challenge = self.get_challenge_for_update(setup_token_hash, browser_hash)
        if challenge is None or challenge.account_id != account_id:
            return None
        challenge.check("setup", browser_hash, self.tx.store.clock.now())
        factor = self.tx.state.factors.get(challenge.factor_id) if challenge.factor_id else None
        return factor if factor and factor.status == "pending" else None

    def invalidate_pending_setup(self, account_id: UUID, scope: SelfAuthScope) -> int:
        if account_id != scope.account_id:
            raise AuthError("NOT_FOUND")
        pending = {
            f.id
            for f in self.tx.state.factors.values()
            if f.account_id == account_id and f.status == "pending"
        }
        for factor_id in pending:
            self.tx.state.factors[factor_id].revoke("restart")
        for challenge in self.tx.state.challenges.values():
            if challenge.account_id == account_id and challenge.factor_id in pending:
                challenge.consumed_at = self.tx.store.clock.now()
        return len(pending)

    def get_challenge_for_update(
        self, token_hash: bytes, browser_hash: bytes
    ) -> MfaChallenge | None:
        return next(
            (
                c
                for c in self.tx.state.challenges.values()
                if c.token_hash == token_hash and c.browser_binding_hash == browser_hash
            ),
            None,
        )

    def find_recovery_for_update(self, factor_id: UUID, code_hash: bytes) -> RecoveryCode | None:
        return next(
            (
                c
                for c in self.tx.state.codes.values()
                if c.factor_id == factor_id and c.code_hash == code_hash
            ),
            None,
        )

    def save_factor(self, factor: MfaFactor, expected_version: int) -> None:
        self.tx.state.factors[factor.id] = factor

    def save_challenge(self, challenge: MfaChallenge) -> None:
        self.tx.state.challenges[challenge.id] = challenge

    def consume_recovery(self, code: RecoveryCode) -> None:
        self.tx.state.codes[code.id] = code

    def save_recovery_codes(
        self, factor_id: UUID, codes: tuple[RecoveryCode, ...], scope: SelfAuthScope
    ) -> None:
        if self.tx.state.factors[factor_id].account_id != scope.account_id:
            raise AuthError("NOT_FOUND")
        self.tx.state.codes.update({code.id: code for code in codes})

    def revoke_recovery_codes(self, factor_id: UUID, scope: SelfAuthScope) -> int:
        if self.tx.state.factors[factor_id].account_id != scope.account_id:
            raise AuthError("NOT_FOUND")
        count = 0
        for code in self.tx.state.codes.values():
            if code.factor_id == factor_id:
                code.consumed_at = self.tx.store.clock.now()
                count += 1
        return count


class Transaction:
    def __init__(self, store: Store) -> None:
        self.store = store
        self.state = State()
        self.users = Users(self)
        self.sessions = Sessions(self)
        self.mfa = Mfa(self)

    def __enter__(self) -> Transaction:
        self.store.lock.acquire()
        self.state = deepcopy(self.store.state)
        return self

    def __exit__(self, *args: object) -> None:
        self.store.lock.release()

    def credential(self, account_id: UUID, scope: SelfAuthScope) -> Credential:
        if account_id != scope.account_id:
            raise AuthError("NOT_FOUND")
        return self.state.credentials[account_id]

    def save_credential(self, credential: Credential) -> None:
        self.state.credentials[credential.user_id] = credential

    def store_token(self, token: IssuedToken) -> None:
        self.state.tokens[token.token_hash] = token

    def invalidate_tokens(self, account_id: UUID) -> None:
        self.state.used.update(
            t.token_hash for t in self.state.tokens.values() if t.subject == account_id
        )
        for challenge in self.state.challenges.values():
            if challenge.account_id == account_id:
                challenge.consumed_at = self.store.clock.now()

    def enrolment_digest(self, account_id: UUID, key: UUID, now: datetime) -> bytes | None:
        record = self.state.digests.get((account_id, key))
        return record[0] if record and now < record[1] else None

    def record_enrolment(
        self, account_id: UUID, key: UUID, digest: bytes, expires: datetime
    ) -> None:
        self.state.digests[account_id, key] = (digest, expires)

    def notify(self, account: Account, token: IssuedToken) -> None:
        self.state.notifications.append(token)

    def commit(self, action: str, account_id: UUID | None) -> None:
        if self.store.fail_commit:
            raise RuntimeError("synthetic rollback")
        self.state.audit.append(action)
        self.store.state = deepcopy(self.state)
        if self.store.uncertain_commit:
            raise RuntimeError("synthetic uncertain outcome")
