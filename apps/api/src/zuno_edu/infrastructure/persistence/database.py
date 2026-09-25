"""Explicit composition; construction never connects or migrates the database."""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from uuid import UUID, uuid4

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, sessionmaker

from zuno_edu.modules.identity.application.ports import IssuedToken
from zuno_edu.modules.identity.domain import Account
from zuno_edu.modules.identity.infrastructure.repository import SqlAlchemyIdentityTransaction
from zuno_edu.modules.operations.domain.delivery import OutboxEvent
from zuno_edu.shared.persistence import Clock, CommitResult

from .repository import IntegrationRepository


@dataclass(frozen=True)
class AuditRecord:
    """Transaction envelope; the owning audit chunk supplies its scoped writer."""

    id: UUID
    action: str
    resource_id: UUID | None


type AuditWriter = Callable[[Session, tuple[AuditRecord, ...]], None]
type IdentityNotificationWriter = Callable[[Session, Account, IssuedToken], None]


class Database:
    def __init__(self, url: str) -> None:
        parsed = make_url(url)
        if parsed.drivername != "postgresql+psycopg":
            raise ValueError("PostgreSQL with psycopg is required")
        self.engine: Engine = create_engine(parsed, pool_pre_ping=True)
        self.sessions = sessionmaker(self.engine, expire_on_commit=False)

    def unit_of_work(self, audit_writer: AuditWriter | None = None) -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(self.sessions, audit_writer)

    @contextmanager
    def identity_transaction(
        self,
        audit_writer: AuditWriter,
        notification_writer: IdentityNotificationWriter,
        clock: Clock | None = None,
    ) -> Iterator[SqlAlchemyIdentityTransaction]:
        with self.unit_of_work(audit_writer) as uow:
            assert uow._session is not None

            def commit(action: str, subject: UUID | None) -> None:
                uow.commit(audit=(AuditRecord(uuid4(), action, subject),))

            yield SqlAlchemyIdentityTransaction(uow._session, commit, notification_writer, clock)

    def close(self) -> None:
        self.engine.dispose()


class SqlAlchemyUnitOfWork:
    def __init__(self, sessions: sessionmaker[Session], audit_writer: AuditWriter | None) -> None:
        self._sessions = sessions
        self._audit_writer = audit_writer
        self._session: Session | None = None
        self._integrations: IntegrationRepository | None = None

    @property
    def integrations(self) -> IntegrationRepository:
        if self._integrations is None:
            raise RuntimeError("Transaction is not active")
        return self._integrations

    @property
    def identity(self) -> SqlAlchemyIdentityTransaction:
        if self._session is None:
            raise RuntimeError("Transaction is not active")

        def commit(action: str, subject: UUID | None) -> None:
            self.commit(audit=(AuditRecord(uuid4(), action, subject),))

        return SqlAlchemyIdentityTransaction(self._session, commit)

    def begin(self) -> SqlAlchemyUnitOfWork:
        if self._session is not None:
            raise RuntimeError("Transaction already active")
        self._session = self._sessions()
        self._session.begin()
        self._integrations = IntegrationRepository(self._session)
        return self

    def __enter__(self) -> SqlAlchemyUnitOfWork:
        if self._session is None:
            self.begin()
        return self

    def commit(
        self, events: tuple[OutboxEvent, ...] = (), audit: tuple[AuditRecord, ...] = ()
    ) -> CommitResult:
        if self._session is None:
            raise RuntimeError("Transaction is not active")
        try:
            for event in events:
                self.integrations.append_event(event)
            if audit:
                if self._audit_writer is None:
                    raise RuntimeError("Audit persistence must be composed before accepting audit")
                self._audit_writer(self._session, audit)
            self._session.commit()
            return CommitResult(tuple(event.id for event in events))
        finally:
            self.rollback()

    def rollback(self) -> None:
        if self._session is not None:
            self._session.rollback()
            self._session.close()
            self._session = None
            self._integrations = None

    def __exit__(self, *args: object) -> None:
        self.rollback()
