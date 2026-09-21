"""Internal outbox operation. No HTTP route exposes worker authority."""

from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Protocol, Self
from uuid import UUID, uuid4

from zuno_edu.modules.operations.domain.delivery import (
    JOB_OUTBOX_DISPATCHRequest,
    JobView,
    Lease,
    OutboxEvent,
)
from zuno_edu.shared.persistence import Clock, CommitResult, Wakeup


class DispatchRepository(Protocol):
    def claim_outbox(self, batch_size: int, lease: Lease) -> tuple[OutboxEvent, ...]: ...
    def materialize_job(self, event_id: UUID, lease: Lease, now: datetime) -> UUID: ...
    def record_dispatch(self, now: datetime) -> JobView: ...


class DispatchTransaction(Protocol):
    @property
    def integrations(self) -> DispatchRepository: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...
    def commit(self) -> CommitResult: ...


class OperationsService:
    def __init__(
        self,
        unit_of_work: Callable[[], DispatchTransaction],
        clock: Clock,
        wakeup: Wakeup,
        worker_identity: object,
    ) -> None:
        self._uow = unit_of_work
        self._clock = clock
        self._wakeup = wakeup
        self._identity = worker_identity

    def dispatch_outbox(self, principal: object, request: JOB_OUTBOX_DISPATCHRequest) -> JobView:
        # Identity is supplied by trusted worker composition, never from request data.
        if principal is not self._identity:
            raise PermissionError("FORBIDDEN")
        now = self._clock.now()
        lease = Lease(uuid4(), now, now + timedelta(minutes=2))
        with self._uow() as tx:
            events = tx.integrations.claim_outbox(request.batch_size, lease)
            tx.commit()
        for event in events:
            with self._uow() as tx:
                id = tx.integrations.materialize_job(event.id, lease, self._clock.now())
                tx.commit()
            # Wakeup adapter tolerates Redis loss. Durable state is already committed.
            self._wakeup(id)
        with self._uow() as tx:
            result = tx.integrations.record_dispatch(self._clock.now())
            tx.commit()
        return result
