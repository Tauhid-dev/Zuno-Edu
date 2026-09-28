"""Bounded, authorized audit reads, with durable audit of the read itself."""

from collections.abc import Callable
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol
from uuid import UUID, uuid4

from zuno_edu.domain.policies import AdminCapabilityScope, Principal
from zuno_edu.modules.identity.domain import AuthError
from zuno_edu.modules.operations.domain.audit import AuditRecord
from zuno_edu.shared.persistence import Clock, require_instant


@dataclass(frozen=True)
class AuditFilter:
    start: datetime
    end: datetime
    actor_id: UUID | None = None
    resource_id: UUID | None = None
    action: str | None = None
    limit: int = 25
    cursor: str | None = None

    def __post_init__(self) -> None:
        try:
            span = require_instant(self.end) - require_instant(self.start)
            valid = (
                timedelta(0) < span <= timedelta(days=31)
                and type(self.limit) is int
                and 1 <= self.limit <= 100
                and (
                    self.action is None
                    or (self.action == self.action.strip() and 1 <= len(self.action) <= 200)
                )
                and (self.cursor is None or 1 <= len(self.cursor) <= 512)
            )
        except TypeError, ValueError:
            valid = False
        if not valid:
            raise AuthError("VALIDATION_ERROR")


@dataclass(frozen=True)
class PageMeta:
    next_cursor: str | None
    has_more: bool


@dataclass(frozen=True)
class AuditViewPage:
    items: tuple[AuditRecord, ...]
    page: PageMeta


class AuditRepository(Protocol):
    def append(self, record: AuditRecord) -> None: ...
    def list_redacted(self, scope: AdminCapabilityScope, filter: AuditFilter) -> AuditViewPage: ...


class AuditTransaction(Protocol):
    @property
    def audit(self) -> AuditRepository: ...
    def current(self, principal: Principal) -> Principal: ...
    def commit(self) -> None: ...


class AuditService:
    def __init__(
        self, transactions: Callable[[], AbstractContextManager[AuditTransaction]], clock: Clock
    ) -> None:
        self._transactions, self._clock = transactions, clock

    def list_audit(self, principal: Principal, request: AuditFilter) -> AuditViewPage:
        with self._transactions() as tx:
            current = tx.current(principal)
            try:
                current.require_capability("audit_admin", self._clock.now())
            except AuthError:
                tx.audit.append(
                    AuditRecord(
                        uuid4(),
                        current.account_id,
                        "audit.denied",
                        "audit",
                        None,
                        self._clock.now(),
                        current.request_id,
                        "denied",
                        "FORBIDDEN",
                    )
                )
                tx.commit()
                raise
            scope = AdminCapabilityScope(current, "audit_admin")
            result = tx.audit.list_redacted(scope, request)
            tx.audit.append(
                AuditRecord(
                    uuid4(),
                    current.account_id,
                    "audit.accessed",
                    "audit",
                    None,
                    self._clock.now(),
                    current.request_id,
                    "allowed",
                )
            )
            tx.commit()
            return result
