"""Failure and concurrency acceptance on migrated PostgreSQL, not SQLite substitutes."""

import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from threading import Barrier
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.orm import Session
from zuno_edu.bootstrap.app import create_app
from zuno_edu.infrastructure.persistence.database import AuditRecord, Database
from zuno_edu.infrastructure.persistence.tables import inbox, jobs, outbox
from zuno_edu.infrastructure.persistence.worker import DurableWorker, RedisWakeup, RetryableFailure
from zuno_edu.modules.operations.application.dispatch import OperationsService
from zuno_edu.modules.operations.domain.delivery import (
    BackgroundJob,
    FailureCode,
    JOB_OUTBOX_DISPATCHRequest,
    JobScope,
    JobStatus,
    Lease,
    OutboxEvent,
    VerifiedWebhook,
)
from zuno_edu.shared.persistence import FrozenClock, Version, VersionConflict

NOW = datetime(2026, 9, 21, tzinfo=UTC)
SCOPE = JobScope(frozenset({"test.changed"}))


def event() -> OutboxEvent:
    return OutboxEvent(uuid4(), "test", uuid4(), 1, "test.changed", NOW)


def lease(now: datetime = NOW) -> Lease:
    return Lease(uuid4(), now, now + timedelta(minutes=2))


def enqueue(db: Database, intent: OutboxEvent | None = None) -> UUID:
    intent = intent or event()
    claim = lease()
    with db.unit_of_work() as tx:
        tx.commit((intent,))
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_outbox(1, claim) == (intent,)
        id = tx.integrations.materialize_job(intent.id, claim, NOW)
        tx.commit()
    return id


def state(db: Database, id: UUID) -> sa.RowMapping:
    with db.engine.connect() as connection:
        return connection.execute(sa.select(*jobs.c).where(jobs.c.id == id)).mappings().one()


def test_rollback_leaves_neither_business_write_nor_outbox(db: Database) -> None:
    # The fake aggregate demonstrates a future repository sharing the UoW session.
    with db.engine.begin() as connection:
        connection.execute(sa.text("CREATE TABLE test_aggregate (id uuid PRIMARY KEY)"))

    def write_audit(session: Session, records: tuple[AuditRecord, ...]) -> None:
        session.execute(sa.text("INSERT INTO test_aggregate VALUES (:id)"), {"id": records[0].id})
        raise RuntimeError("audit failure")

    with pytest.raises(RuntimeError, match="audit failure"), db.unit_of_work(write_audit) as tx:
        tx.commit((event(),), (AuditRecord(uuid4(), "test", None),))
    with db.engine.connect() as connection:
        assert connection.scalar(sa.select(sa.func.count()).select_from(outbox)) == 0
        assert connection.scalar(sa.text("SELECT count(*) FROM test_aggregate")) == 0
    with db.unit_of_work() as tx:
        tx.integrations.append_event(event())
    with db.engine.connect() as connection:
        assert connection.scalar(sa.select(sa.func.count()).select_from(outbox)) == 0


def test_success_commits_business_audit_and_outbox_together(db: Database) -> None:
    with db.engine.begin() as connection:
        connection.execute(sa.text("CREATE TABLE test_audit (id uuid PRIMARY KEY)"))

    def write_audit(session: Session, records: tuple[AuditRecord, ...]) -> None:
        for record in records:
            session.execute(sa.text("INSERT INTO test_audit VALUES (:id)"), {"id": record.id})

    intent = event()
    with db.unit_of_work(write_audit).begin() as tx:
        result = tx.commit((intent,), (AuditRecord(uuid4(), "test", None),))
        assert result.event_ids == (intent.id,)
    with db.engine.connect() as connection:
        assert connection.scalar(sa.select(sa.func.count()).select_from(outbox)) == 1
        assert connection.scalar(sa.text("SELECT count(*) FROM test_audit")) == 1


def test_missing_audit_adapter_fails_closed(db: Database) -> None:
    with pytest.raises(RuntimeError, match="Audit persistence"), db.unit_of_work() as tx:
        tx.commit((event(),), (AuditRecord(uuid4(), "test", None),))
    with db.engine.connect() as connection:
        assert connection.scalar(sa.select(sa.func.count()).select_from(outbox)) == 0


def test_unique_event_and_job_identity(db: Database) -> None:
    intent = event()
    id = enqueue(db, intent)
    with pytest.raises(IntegrityError), db.unit_of_work() as tx:
        tx.commit((replace(intent, id=uuid4()),))
    with pytest.raises(IntegrityError), db.engine.begin() as connection:
        connection.execute(jobs.insert().values(**{**dict(state(db, id)), "id": uuid4()}))


def test_concurrent_workers_claim_one_lease(db: Database) -> None:
    id = enqueue(db)
    barrier = Barrier(2)

    def claim() -> UUID | None:
        with db.unit_of_work() as tx:
            barrier.wait(timeout=10)
            job = tx.integrations.claim_job(id, SCOPE, lease())
            # Both workers attempt before either releases its row lock.
            barrier.wait(timeout=10)
            tx.commit()
            return job.id if job else None

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: claim(), range(2)))
    assert results.count(id) == 1
    assert state(db, id)["attempt_count"] == 1


def test_concurrent_outbox_claims_are_disjoint(db: Database) -> None:
    with db.unit_of_work() as tx:
        tx.commit((event(), event()))
    barrier = Barrier(2)

    def claim() -> set[UUID]:
        with db.unit_of_work() as tx:
            barrier.wait(timeout=10)
            intents = tx.integrations.claim_outbox(1, lease())
            barrier.wait(timeout=10)
            tx.commit()
            return {item.id for item in intents}

    with ThreadPoolExecutor(max_workers=2) as executor:
        first, second = executor.map(lambda _: claim(), range(2))
    assert len(first) == len(second) == 1
    assert first.isdisjoint(second)


def test_expired_worker_cannot_acknowledge_reclaimed_job(db: Database) -> None:
    id, old = enqueue(db), lease()
    with db.unit_of_work() as tx:
        first = tx.integrations.claim_job(id, SCOPE, old)
        tx.commit()
    assert first is not None
    later = old.until + timedelta(seconds=1)
    fresh = lease(later)
    with db.unit_of_work() as tx:
        second = tx.integrations.claim_job(id, SCOPE, fresh)
        tx.commit()
    assert second is not None and second.version > first.version
    with pytest.raises(VersionConflict), db.unit_of_work() as tx:
        tx.integrations.finish_job(first, old, later)
    with db.unit_of_work() as tx:
        tx.integrations.finish_job(second, fresh, later)
        tx.commit()
    assert state(db, id)["status"] == "succeeded"


def test_expired_outbox_lease_is_recovered_and_fenced(db: Database) -> None:
    intent, old = event(), lease()
    with db.unit_of_work() as tx:
        tx.commit((intent,))
    with db.unit_of_work() as tx:
        tx.integrations.claim_outbox(1, old)
        tx.commit()
    later = old.until + timedelta(seconds=1)
    fresh = lease(later)
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_outbox(1, fresh) == (intent,)
        tx.commit()
    with pytest.raises(VersionConflict), db.unit_of_work() as tx:
        tx.integrations.materialize_job(intent.id, old, later)
    with db.unit_of_work() as tx:
        tx.integrations.materialize_job(intent.id, fresh, later)
        tx.commit()


def test_scope_and_untrusted_dispatch_are_denied(db: Database) -> None:
    id = enqueue(db)
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_job(id, JobScope(frozenset({"other"})), lease()) is None
    service = OperationsService(db.unit_of_work, FrozenClock(NOW), lambda _: None, object())
    for principal in (None, "system", {"role": "system"}, object()):
        with pytest.raises(PermissionError):
            service.dispatch_outbox(principal, JOB_OUTBOX_DISPATCHRequest(10))
    with TestClient(create_app()) as client:
        assert client.post("/worker/dispatch_outbox", json={"role": "system"}).status_code == 404


class IdempotentHandler:
    def __init__(self, db: Database) -> None:
        self.db = db
        self.effects: set[str] = set()
        self.calls = 0

    def reconcile(self, intent: OutboxEvent) -> None:
        assert self.db.engine.pool.checkedout() == 0  # type: ignore[attr-defined]
        self.calls += 1
        self.effects.add(intent.dedupe_key)


def test_redis_loss_recovers_durable_jobs(db: Database) -> None:
    redis_url = os.environ["ZUNO_TEST_REDIS_URL"]
    # Fixed disposable Redis instance; never flush an arbitrary configured service.
    assert redis_url == "redis://127.0.0.1:16379/15"
    client = Redis.from_url(redis_url)
    client.flushdb()
    wakeup, identity = RedisWakeup(redis_url), object()
    with db.unit_of_work() as tx:
        tx.commit((event(),))
    service = OperationsService(db.unit_of_work, FrozenClock(NOW), wakeup, identity)
    result = service.dispatch_outbox(identity, JOB_OUTBOX_DISPATCHRequest(10))
    assert result.status == JobStatus.SUCCEEDED
    assert client.llen("zuno:jobs:wakeup") == 1
    client.flushdb()  # Lose every wakeup after dispatch was acknowledged.
    handler = IdempotentHandler(db)
    worker = DurableWorker(db, FrozenClock(NOW), {"test.changed": handler})
    assert worker.recover() == 1
    assert worker.recover() == 0
    assert len(handler.effects) == 1
    wakeup.close()
    client.close()


def test_redis_unavailable_does_not_lose_intent(db: Database) -> None:
    wakeup, identity = RedisWakeup("redis://127.0.0.1:1/0"), object()
    with db.unit_of_work() as tx:
        tx.commit((event(),))
    service = OperationsService(db.unit_of_work, FrozenClock(NOW), wakeup, identity)
    assert service.dispatch_outbox(identity, JOB_OUTBOX_DISPATCHRequest(10)).status == "succeeded"
    handler = IdempotentHandler(db)
    assert DurableWorker(db, FrozenClock(NOW), {"test.changed": handler}).recover() == 1
    wakeup.close()


def test_restart_after_effect_uses_same_reconciliation_identity(db: Database) -> None:
    id = enqueue(db)
    old = lease()
    handler = IdempotentHandler(db)
    with db.unit_of_work() as tx:
        job = tx.integrations.claim_job(id, SCOPE, old)
        assert job is not None
        intent = tx.integrations.job_event(job)
        tx.commit()
    handler.reconcile(intent)  # Process dies after effect, before acknowledgement.
    worker = DurableWorker(
        db, FrozenClock(old.until + timedelta(seconds=1)), {"test.changed": handler}
    )
    assert worker.recover() == 1
    assert handler.calls == 2 and len(handler.effects) == 1


def test_bounded_retries_retry_after_and_dead_letter(db: Database) -> None:
    id = enqueue(db)
    now = NOW
    for attempt in range(1, 9):
        claim = lease(now)
        with db.unit_of_work() as tx:
            job = tx.integrations.claim_job(id, SCOPE, claim)
            assert job is not None and job.attempt_count == attempt
            tx.integrations.finish_job(job, claim, now, FailureCode.PROVIDER_UNAVAILABLE)
            tx.commit()
        row = state(db, id)
        if row["status"] == "dead_letter":
            assert row["next_attempt_at"] is None
            break
        assert row["next_attempt_at"] > now
        now = row["next_attempt_at"]
    assert state(db, id)["status"] == "dead_letter"
    assert state(db, id)["attempt_count"] <= 8
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_job(id, SCOPE, lease(now + timedelta(days=2))) is None


def test_retry_after_exceeding_24_hours_dead_letters(db: Database) -> None:
    id, claim = enqueue(db), lease()
    with db.unit_of_work() as tx:
        job = tx.integrations.claim_job(id, SCOPE, claim)
        assert job is not None
        tx.integrations.finish_job(
            job, claim, NOW, FailureCode.PROVIDER_UNAVAILABLE, timedelta(days=2)
        )
        tx.commit()
    assert state(db, id)["status"] == "dead_letter"


@pytest.mark.parametrize("code", [FailureCode.CONFIGURATION_ERROR, FailureCode.UNKNOWN_OUTCOME])
def test_non_retryable_and_ambiguous_effects_are_quarantined(
    db: Database, code: FailureCode
) -> None:
    id, claim = enqueue(db), lease()
    with db.unit_of_work() as tx:
        job = tx.integrations.claim_job(id, SCOPE, claim)
        assert job is not None
        tx.integrations.finish_job(job, claim, NOW, code)
        tx.commit()
    assert state(db, id)["status"] == "dead_letter"


def test_worker_redacts_failure_and_schedules_retry(db: Database) -> None:
    class Failing:
        def reconcile(self, intent: OutboxEvent) -> None:
            raise RetryableFailure(timedelta(minutes=20))

    id = enqueue(db)
    assert DurableWorker(db, FrozenClock(NOW), {"test.changed": Failing()}).recover() == 1
    row = state(db, id)
    assert row["last_error_code"] == "PROVIDER_UNAVAILABLE"
    assert row["next_attempt_at"] == NOW + timedelta(minutes=20)


def test_inbox_duplicate_verified_only_and_fenced_completion(db: Database) -> None:
    incoming = VerifiedWebhook("test-provider", "evt1", b"encrypted", NOW)
    with db.unit_of_work() as tx:
        first = tx.integrations.insert_inbox_unique(incoming)
        duplicate = tx.integrations.insert_inbox_unique(
            replace(incoming, payload_ciphertext=b"other")
        )
        assert first.inserted and not duplicate.inserted and first.id == duplicate.id
        tx.commit()
    old = lease()
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_inbox(first.id, "other", old) is None
        claim = tx.integrations.claim_inbox(first.id, incoming.provider, old)
        assert claim is not None and claim.payload_ciphertext == b"encrypted"
        tx.commit()
    later, fresh = old.until, lease(old.until)
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_inbox(first.id, incoming.provider, fresh) is not None
        tx.commit()
    with pytest.raises(VersionConflict), db.unit_of_work() as tx:
        tx.integrations.complete_inbox(first.id, old, later)
    with db.unit_of_work() as tx:
        tx.integrations.complete_inbox(first.id, fresh, later, ignored=True)
        tx.commit()
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_inbox(first.id, incoming.provider, lease(later)) is None


def test_unverified_inbox_never_claimed(db: Database) -> None:
    id = uuid4()
    with db.engine.begin() as connection:
        connection.execute(
            inbox.insert().values(
                id=id,
                provider="test",
                provider_event_id="e",
                verified=False,
                payload_ciphertext=b"encrypted",
                status="pending",
                received_at=NOW,
                updated_at=NOW,
            )
        )
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_inbox(id, "test", lease()) is None


@pytest.mark.parametrize(
    "table,column,value", [(outbox, "payload", {}), (jobs, "dedupe_key", "new")]
)
def test_database_guards_immutable_intent(
    db: Database, table: sa.Table, column: str, value: object
) -> None:
    enqueue(db, replace(event(), payload=(("resource_id", uuid4()),)))
    with pytest.raises(DBAPIError, match="Immutable"), db.engine.begin() as connection:
        connection.execute(table.update().values({column: value}))


def test_utc_clock_version_and_payload_boundaries() -> None:
    assert FrozenClock(NOW).today("Australia/Sydney").isoformat() == "2026-09-21"
    assert Version(3).next().value == 4
    with pytest.raises(ValueError):
        Version(0)
    with pytest.raises(ValueError):
        replace(event(), occurred_at=datetime(2026, 9, 21))
    with pytest.raises(ValueError):
        replace(event(), payload=(("email", "secret@example.com"),))  # type: ignore[arg-type]
    for size in (0, 101, True):
        with pytest.raises(ValueError):
            JOB_OUTBOX_DISPATCHRequest(size)


def test_claim_at_24_hours_dead_letters_without_running_handler(db: Database) -> None:
    id = enqueue(db)
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_job(id, SCOPE, lease(NOW + timedelta(hours=24))) is None
        tx.commit()
    row = state(db, id)
    assert row["status"] == "dead_letter" and row["attempt_count"] == 0
    assert row["last_error_code"] == "RETRY_EXHAUSTED"


def test_eight_crashed_leases_exhaust_without_a_ninth_attempt(db: Database) -> None:
    id, now = enqueue(db), NOW
    for attempt in range(1, 9):
        with db.unit_of_work() as tx:
            job = tx.integrations.claim_job(id, SCOPE, lease(now))
            assert job is not None and job.attempt_count == attempt
            tx.commit()
        now += timedelta(minutes=3)
    with db.unit_of_work() as tx:
        assert tx.integrations.claim_job(id, SCOPE, lease(now)) is None
        tx.commit()
    row = state(db, id)
    assert row["status"] == "dead_letter" and row["attempt_count"] == 8


def test_domain_job_transitions_and_invalid_reconstitution() -> None:
    queued = BackgroundJob(
        uuid4(), "test.changed", uuid4(), "key", JobStatus.QUEUED, 0, None, NOW, None, 1, NOW
    )
    running = queued.claim(NOW, NOW + timedelta(minutes=2))
    assert running.attempt_count == 1 and running.version == 2
    assert running.succeed().status == JobStatus.SUCCEEDED
    retry = running.retry(FailureCode.PROVIDER_UNAVAILABLE, running.retry_at(NOW))
    assert retry.status == JobStatus.FAILED and retry.next_attempt_at == NOW + timedelta(minutes=1)
    with pytest.raises(ValueError):
        queued.succeed()
    with pytest.raises(ValueError):
        running.claim(NOW, NOW + timedelta(minutes=2))
    with pytest.raises(ValueError):
        replace(queued, attempt_count=9)
    with pytest.raises(ValueError):
        replace(queued, version=0)
    with pytest.raises(ValueError):
        replace(queued, status=JobStatus.RUNNING)
    with pytest.raises(ValueError):
        replace(running, last_error_code="private provider response")
    with pytest.raises(ValueError):
        running.succeed().dead_letter(FailureCode.UNKNOWN_OUTCOME)
