"""Trusted worker composition, deliberately separate from the public API factory."""

from dataclasses import dataclass

from zuno_edu.infrastructure.persistence.database import Database
from zuno_edu.infrastructure.persistence.worker import RedisWakeup
from zuno_edu.modules.operations.application.dispatch import OperationsService
from zuno_edu.modules.operations.domain.delivery import JOB_OUTBOX_DISPATCHRequest, JobView
from zuno_edu.shared.persistence import Clock, SystemClock


@dataclass
class OutboxDispatcher:
    database: Database
    wakeup: RedisWakeup
    _service: OperationsService
    _identity: object

    def dispatch(self, batch_size: int = 100) -> JobView:
        return self._service.dispatch_outbox(self._identity, JOB_OUTBOX_DISPATCHRequest(batch_size))

    def close(self) -> None:
        self.wakeup.close()
        self.database.close()


def create_dispatcher(
    database_url: str, redis_url: str, clock: Clock | None = None
) -> OutboxDispatcher:
    database, wakeup = Database(database_url), RedisWakeup(redis_url)
    identity = object()
    service = OperationsService(database.unit_of_work, clock or SystemClock(), wakeup, identity)
    return OutboxDispatcher(database, wakeup, service, identity)
