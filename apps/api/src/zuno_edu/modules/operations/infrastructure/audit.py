"""PostgreSQL audit projection; every read revalidates current session authority."""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from zuno_edu.domain.policies import AdminCapabilityScope, Principal
from zuno_edu.infrastructure.persistence.database import AuditRecord as AuditEnvelope
from zuno_edu.infrastructure.persistence.tables import audit_records
from zuno_edu.modules.identity.application.principal import current_identity, principal_for
from zuno_edu.modules.identity.domain import AuthError
from zuno_edu.modules.identity.infrastructure.repository import SqlAlchemyIdentityTransaction
from zuno_edu.modules.operations.application.audit import (
    AuditFilter,
    AuditTransaction,
    AuditViewPage,
    PageMeta,
)
from zuno_edu.modules.operations.domain.audit import AuditRecord
from zuno_edu.presentation.http.errors import ApiError
from zuno_edu.presentation.http.pagination import CursorCodec, CursorContext
from zuno_edu.shared.persistence import Clock, require_instant


class SqlAuditRepository:
    def __init__(
        self,
        session: Session,
        clock: Clock,
        current: Callable[[Principal], Principal],
        cursors: CursorCodec,
    ) -> None:
        self.session, self.clock, self.current, self.cursors = session, clock, current, cursors

    def append(self, record: AuditRecord) -> None:
        self.session.execute(audit_records.insert().values(**asdict(record), metadata={}))

    def list_redacted(self, scope: AdminCapabilityScope, filter: AuditFilter) -> AuditViewPage:
        # A scope carried from another transaction is NOT a reusable grant.
        actor = self.current(scope.principal)
        current_scope = AdminCapabilityScope(actor, scope.capability)
        current_scope.require("audit_admin", self.clock.now())
        binding = CursorContext(
            actor.account_id,
            "API-ADMIN-AUDIT",
            {"capability": "audit_admin"},
            {
                "from": require_instant(filter.start).isoformat(),
                "to": require_instant(filter.end).isoformat(),
                "actor_id": str(filter.actor_id) if filter.actor_id else None,
                "resource_id": str(filter.resource_id) if filter.resource_id else None,
                "action": filter.action,
                "limit": filter.limit,
            },
        )
        query = sa.select(*(c for c in audit_records.c if c.name != "metadata")).where(
            audit_records.c.occurred_at >= filter.start,
            audit_records.c.occurred_at < filter.end,
        )
        for name in ("actor_id", "resource_id", "action"):
            value = getattr(filter, name)
            if value is not None:
                query = query.where(audit_records.c[name] == value)
        if filter.cursor:
            try:
                position = self.cursors.decode(filter.cursor, binding)
                if len(position) != 2:
                    raise ValueError
                instant, id = (
                    require_instant(datetime.fromisoformat(position[0])),
                    UUID(position[1]),
                )
            except ApiError, ValueError:
                raise AuthError("VALIDATION_ERROR") from None
            query = query.where(
                sa.tuple_(audit_records.c.occurred_at, audit_records.c.id)
                < sa.tuple_(sa.literal(instant), sa.literal(id))
            )
        rows = (
            self.session.execute(
                query.order_by(audit_records.c.occurred_at.desc(), audit_records.c.id.desc()).limit(
                    filter.limit + 1
                )
            )
            .mappings()
            .all()
        )
        # SELECT itself may wait on a relation lock, even when it returns no rows.
        current_scope = AdminCapabilityScope(self.current(actor), scope.capability)
        current_scope.require("audit_admin", self.clock.now())
        items = tuple(
            AuditRecord(**dict(row)).redacted_view(current_scope, self.clock.now())
            for row in rows[: filter.limit]
        )
        more = len(rows) > filter.limit
        cursor = (
            self.cursors.encode(binding, (items[-1].occurred_at.isoformat(), str(items[-1].id)))
            if more
            else None
        )
        return AuditViewPage(items, PageMeta(cursor, more))


class SqlAuditTransaction:
    def __init__(
        self, session: Session, clock: Clock, approved: Callable[[UUID], bool], cursors: CursorCodec
    ) -> None:
        self.session, self.clock, self.approved = session, clock, approved
        self.audit = SqlAuditRepository(session, clock, self.current, cursors)

    def current(self, principal: Principal) -> Principal:
        def no_identity_commit(action: str, subject: UUID | None) -> None:
            raise RuntimeError("Identity writes are not part of audit reads")

        identity = SqlAlchemyIdentityTransaction(self.session, no_identity_commit, clock=self.clock)
        account, session = current_identity(
            identity, principal.token_hash, self.clock, self.approved
        )
        if account.id != principal.account_id or session.id != principal.session_id:
            raise AuthError("UNAUTHENTICATED")
        return principal_for(account, session, principal.request_id)

    def commit(self) -> None:
        self.session.commit()


class AuditTransactions:
    def __init__(
        self,
        sessions: sessionmaker[Session],
        clock: Clock,
        approved: Callable[[UUID], bool],
        cursors: CursorCodec,
    ) -> None:
        self.sessions, self.clock, self.approved, self.cursors = sessions, clock, approved, cursors

    @contextmanager
    def __call__(self) -> Iterator[AuditTransaction]:
        with self.sessions() as session, session.begin():
            yield SqlAuditTransaction(session, self.clock, self.approved, self.cursors)


class IdentityAuditWriter:
    """Inject per request; actor is trusted authority or None before authentication.

    This uses the SAME SQL transaction as identity mutation. No independent commit.
    """

    def __init__(self, clock: Clock, request_id: UUID, actor_id: UUID | None = None) -> None:
        self.clock, self.request_id, self.actor_id = clock, request_id, actor_id

    def __call__(self, session: Session, records: tuple[AuditEnvelope, ...]) -> None:
        for item in records:
            denied = item.action.endswith("_denied")
            # Successful identity actions already established this subject through
            # session/password/MFA/token proof. Anonymous email requests and denied
            # attempts never assert that the supplied target authenticated.
            actor_id = self.actor_id
            if not denied and item.action != "authentication.email_requested":
                actor_id = item.resource_id
            record = AuditRecord(
                item.id,
                actor_id,
                item.action,
                "account",
                item.resource_id,
                self.clock.now(),
                self.request_id,
                "denied" if denied else "allowed",
            )
            session.execute(audit_records.insert().values(**asdict(record), metadata={}))
