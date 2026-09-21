"""Purpose-specific Core queries; callers never receive a session or ORM row."""

from datetime import datetime, timedelta
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import RowMapping
from sqlalchemy.orm import Session

from zuno_edu.modules.operations.domain.delivery import (
    BackgroundJob,
    FailureCode,
    InboxInsertOutcome,
    JobScope,
    JobStatus,
    JobView,
    Lease,
    OutboxEvent,
    VerifiedWebhook,
    WebhookInbox,
)
from zuno_edu.shared.persistence import VersionConflict, require_instant

from .tables import inbox, jobs, outbox


def _event(row: RowMapping) -> OutboxEvent:
    return OutboxEvent(
        row["id"],
        row["aggregate_type"],
        row["aggregate_id"],
        row["aggregate_version"],
        row["event_type"],
        row["occurred_at"],
        tuple((key, UUID(value)) for key, value in row["payload"].items()),
    )


def _job(row: RowMapping) -> BackgroundJob:
    return BackgroundJob(
        row["id"],
        row["kind"],
        row["source_event_id"],
        row["dedupe_key"],
        JobStatus(row["status"]),
        row["attempt_count"],
        row["lease_until"],
        row["next_attempt_at"],
        row["last_error_code"],
        row["version"],
        row["created_at"],
    )


class IntegrationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def append_event(self, event: OutboxEvent) -> None:
        self._session.execute(
            outbox.insert().values(
                id=event.id,
                aggregate_type=event.aggregate_type,
                aggregate_id=event.aggregate_id,
                aggregate_version=event.aggregate_version,
                event_type=event.event_type,
                payload={key: str(value) for key, value in event.payload},
                occurred_at=require_instant(event.occurred_at),
            )
        )

    def record_dispatch(self, now: datetime) -> JobView:
        id = uuid4()
        self._session.execute(
            jobs.insert().values(
                id=id,
                kind="outbox.dispatch",
                dedupe_key=str(id),
                payload={},
                status="succeeded",
                attempt_count=1,
                version=1,
                created_at=now,
                updated_at=now,
            )
        )
        return JobView(id, "outbox.dispatch", JobStatus.SUCCEEDED, 1, None, None)

    def job_event(self, job: BackgroundJob) -> OutboxEvent:
        if job.source_event_id is None:
            raise ValueError("A handler requires durable event provenance")
        row = (
            self._session.execute(
                sa.select(*outbox.c).where(
                    outbox.c.id == job.source_event_id,
                    outbox.c.event_type == job.kind,
                )
            )
            .mappings()
            .one()
        )
        return _event(row)

    def claim_outbox(self, batch_size: int, lease: Lease) -> tuple[OutboxEvent, ...]:
        if type(batch_size) is not int or not 1 <= batch_size <= 100:
            raise ValueError("Batch size must be 1-100")
        ids = (
            sa.select(outbox.c.id)
            .where(
                outbox.c.published_at.is_(None),
                sa.or_(outbox.c.lease_until.is_(None), outbox.c.lease_until <= lease.now),
            )
            .order_by(outbox.c.occurred_at, outbox.c.id)
            .limit(batch_size)
            .with_for_update(skip_locked=True)
        )
        rows = self._session.execute(
            outbox.update()
            .where(outbox.c.id.in_(ids))
            .values(
                lease_until=lease.until,
                lease_token=lease.token,
            )
            .returning(*outbox.c)
        ).mappings()
        return tuple(_event(row) for row in rows)

    def materialize_job(self, event_id: UUID, lease: Lease, now: datetime) -> UUID:
        """Atomically save the durable job before considering the intent published."""
        row = (
            self._session.execute(
                sa.select(*outbox.c)
                .where(
                    outbox.c.id == event_id,
                    outbox.c.lease_token == lease.token,
                    outbox.c.lease_until > require_instant(now),
                    outbox.c.published_at.is_(None),
                )
                .with_for_update()
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            raise VersionConflict("Outbox lease expired or replaced")
        event = _event(row)
        job_id = self._session.execute(
            insert(jobs)
            .values(
                id=uuid4(),
                kind=event.event_type,
                source_event_id=event.id,
                dedupe_key=event.dedupe_key,
                payload=row["payload"],
                status="queued",
                attempt_count=0,
                version=1,
                next_attempt_at=now,
                created_at=now,
                updated_at=now,
            )
            .on_conflict_do_nothing(constraint="uq_job_kind_dedupe")
            .returning(jobs.c.id)
        ).scalar_one_or_none()
        if job_id is None:
            job_id = self._session.execute(
                sa.select(jobs.c.id).where(
                    jobs.c.kind == event.event_type,
                    jobs.c.dedupe_key == event.dedupe_key,
                    jobs.c.source_event_id == event.id,
                )
            ).scalar_one()
        self._session.execute(
            outbox.update()
            .where(outbox.c.id == event.id)
            .values(
                published_at=now,
                lease_until=None,
                lease_token=None,
            )
        )
        return UUID(str(job_id))

    def due_job_ids(self, scope: JobScope, now: datetime, limit: int = 100) -> tuple[UUID, ...]:
        if not 1 <= limit <= 100:
            raise ValueError("Bounded recovery batch required")
        now = require_instant(now)
        rows = self._session.execute(
            sa.select(jobs.c.id)
            .where(
                jobs.c.kind.in_(scope.kinds),
                sa.or_(
                    sa.and_(jobs.c.status.in_(("queued", "failed")), jobs.c.next_attempt_at <= now),
                    sa.and_(jobs.c.status == "running", jobs.c.lease_until <= now),
                ),
            )
            .order_by(jobs.c.created_at, jobs.c.id)
            .limit(limit)
        ).scalars()
        return tuple(rows)

    def claim_job(self, id: UUID, scope: JobScope, lease: Lease) -> BackgroundJob | None:
        row = (
            self._session.execute(
                sa.select(*jobs.c)
                .where(
                    jobs.c.id == id,
                    jobs.c.kind.in_(scope.kinds),
                    sa.or_(
                        sa.and_(
                            jobs.c.status.in_(("queued", "failed")),
                            jobs.c.next_attempt_at <= lease.now,
                        ),
                        sa.and_(jobs.c.status == "running", jobs.c.lease_until <= lease.now),
                    ),
                )
                .with_for_update(skip_locked=True)
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        transition = _job(row).claim(lease.now, lease.until)
        claimed = (
            self._session.execute(
                jobs.update()
                .where(jobs.c.id == id)
                .values(
                    status=transition.status.value,
                    attempt_count=transition.attempt_count,
                    lease_until=transition.lease_until,
                    lease_token=lease.token if transition.lease_until else None,
                    next_attempt_at=transition.next_attempt_at,
                    last_error_code=transition.last_error_code,
                    updated_at=lease.now,
                    version=transition.version,
                )
                .returning(*jobs.c)
            )
            .mappings()
            .one()
        )
        return _job(claimed) if transition.status == JobStatus.RUNNING else None

    def finish_job(
        self,
        job: BackgroundJob,
        lease: Lease,
        now: datetime,
        failure: FailureCode | None = None,
        retry_after: timedelta | None = None,
        jitter: float = 1.0,
    ) -> None:
        """Compare both lease token and version: a stale worker cannot acknowledge newer work."""
        now = require_instant(now)
        transition = (
            job.succeed()
            if failure is None
            else job.retry(failure, job.retry_at(now, retry_after, jitter))
        )
        changed = self._session.execute(
            jobs.update()
            .where(
                jobs.c.id == job.id,
                jobs.c.version == job.version,
                jobs.c.status == "running",
                jobs.c.lease_token == lease.token,
                jobs.c.lease_until > now,
            )
            .values(
                status=transition.status.value,
                next_attempt_at=transition.next_attempt_at,
                lease_until=None,
                lease_token=None,
                last_error_code=transition.last_error_code,
                updated_at=now,
                version=transition.version,
            )
            .returning(jobs.c.id)
        ).scalar_one_or_none()
        if changed is None:
            raise VersionConflict("Job lease expired or version changed")

    def insert_inbox_unique(self, event: VerifiedWebhook) -> InboxInsertOutcome:
        id = self._session.execute(
            insert(inbox)
            .values(
                id=uuid4(),
                provider=event.provider,
                provider_event_id=event.provider_event_id,
                verified=True,
                payload_ciphertext=event.payload_ciphertext,
                status="pending",
                received_at=event.received_at,
                updated_at=event.received_at,
            )
            .on_conflict_do_nothing(constraint="uq_inbox_provider_event")
            .returning(inbox.c.id)
        ).scalar_one_or_none()
        if id is not None:
            return InboxInsertOutcome(id, True)
        id = self._session.execute(
            sa.select(inbox.c.id).where(
                inbox.c.provider == event.provider,
                inbox.c.provider_event_id == event.provider_event_id,
            )
        ).scalar_one()
        return InboxInsertOutcome(id, False)

    def claim_inbox(self, id: UUID, provider: str, lease: Lease) -> WebhookInbox | None:
        candidate = (
            sa.select(inbox.c.id)
            .where(
                inbox.c.id == id,
                inbox.c.provider == provider,
                inbox.c.verified.is_(True),
                inbox.c.status.in_(("pending", "processing")),
                sa.or_(inbox.c.lease_until.is_(None), inbox.c.lease_until <= lease.now),
            )
            .with_for_update(skip_locked=True)
        )
        row = (
            self._session.execute(
                inbox.update()
                .where(inbox.c.id.in_(candidate))
                .values(
                    status="processing",
                    lease_until=lease.until,
                    lease_token=lease.token,
                    updated_at=lease.now,
                )
                .returning(*inbox.c)
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        return WebhookInbox(
            row["id"],
            row["provider"],
            row["provider_event_id"],
            row["received_at"],
            row["verified"],
            row["payload_ciphertext"],
            row["status"],
        )

    def complete_inbox(
        self, id: UUID, lease: Lease, now: datetime, *, ignored: bool = False
    ) -> None:
        changed = self._session.execute(
            inbox.update()
            .where(
                inbox.c.id == id,
                inbox.c.verified.is_(True),
                inbox.c.status == "processing",
                inbox.c.lease_token == lease.token,
                inbox.c.lease_until > require_instant(now),
            )
            .values(
                status="ignored" if ignored else "processed",
                processed_at=now,
                updated_at=now,
                lease_until=None,
                lease_token=None,
            )
            .returning(inbox.c.id)
        ).scalar_one_or_none()
        if changed is None:
            raise VersionConflict("Inbox lease expired or replaced")
