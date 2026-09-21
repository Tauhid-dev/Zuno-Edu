"""Redis wakeups plus PostgreSQL recovery. Provider handlers are composed explicitly."""

import logging
import random
from collections.abc import Mapping
from datetime import timedelta
from typing import Protocol
from uuid import UUID, uuid4

from redis import Redis
from redis.exceptions import RedisError

from zuno_edu.modules.operations.domain.delivery import FailureCode, JobScope, Lease, OutboxEvent
from zuno_edu.shared.persistence import Clock, VersionConflict

from .database import Database

logger = logging.getLogger(__name__)


class RedisWakeup:
    def __init__(self, url: str) -> None:
        self._client: Redis = Redis.from_url(
            url,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=1,
        )

    def __call__(self, id: UUID) -> None:
        try:
            # Only opaque IDs enter Redis; lost/trimmed wakeups are recovered from SQL.
            with self._client.pipeline(transaction=True) as pipe:
                pipe.lpush("zuno:jobs:wakeup", str(id))
                pipe.ltrim("zuno:jobs:wakeup", 0, 9999)
                pipe.execute()
        except RedisError:
            logger.warning("WORKER_WAKEUP_UNAVAILABLE")

    def wait(self, timeout: int = 1) -> None:
        try:
            self._client.blpop("zuno:jobs:wakeup", timeout=timeout)
        except RedisError:
            logger.warning("WORKER_WAKEUP_UNAVAILABLE")

    def close(self) -> None:
        self._client.close()


class RetryableFailure(Exception):
    def __init__(self, retry_after: timedelta | None = None) -> None:
        super().__init__("PROVIDER_UNAVAILABLE")
        self.retry_after = retry_after


class ReconciliationHandler(Protocol):
    def reconcile(self, event: OutboxEvent) -> None:
        """Reload latest desired state and dedupe by aggregate/version before effects.

        An ambiguous provider result must be reconciled before repeating an effect.
        Raise RetryableFailure only when repeating is known to be safe; unknown
        errors are quarantined. Future provider chunks supply concrete handlers.
        """
        ...


class DurableWorker:
    def __init__(
        self,
        database: Database,
        clock: Clock,
        handlers: Mapping[str, ReconciliationHandler],
    ) -> None:
        self._database, self._clock = database, clock
        self._handlers = dict(handlers)
        self._scope = JobScope(frozenset(handlers))

    def recover(self) -> int:
        """A bounded database sweep runs even when Redis has lost every wakeup."""
        with self._database.unit_of_work() as tx:
            ids = tx.integrations.due_job_ids(self._scope, self._clock.now())
        return sum(self.run_one(id) for id in ids)

    def run_one(self, id: UUID) -> bool:
        now = self._clock.now()
        lease = Lease(uuid4(), now, now + timedelta(minutes=2))
        with self._database.unit_of_work() as tx:
            job = tx.integrations.claim_job(id, self._scope, lease)
            event = tx.integrations.job_event(job) if job is not None else None
            tx.commit()
        if job is None or event is None:
            return False
        failure, retry_after = None, None
        try:
            # No transaction/row lock survives into a provider call.
            self._handlers[job.kind].reconcile(event)
        except RetryableFailure as error:
            failure, retry_after = FailureCode.PROVIDER_UNAVAILABLE, error.retry_after
        except Exception:
            # Never log exception text or blindly retry ambiguous external effects.
            failure = FailureCode.UNKNOWN_OUTCOME
        try:
            with self._database.unit_of_work() as tx:
                tx.integrations.finish_job(
                    job,
                    lease,
                    self._clock.now(),
                    failure,
                    retry_after,
                    jitter=random.uniform(0.8, 1.2),
                )
                tx.commit()
        except VersionConflict:
            logger.warning("WORKER_LEASE_LOST")
            return False
        if failure is not None and job.attempt_count >= 5:
            logger.error("WORKER_ATTENTION_REQUIRED")
        return True
