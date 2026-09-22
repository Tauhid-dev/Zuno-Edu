"""Immutable intent and fenced work claims. Payloads contain only opaque identifiers."""

from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from enum import StrEnum
from uuid import UUID

from zuno_edu.shared.persistence import require_instant


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class FailureCode(StrEnum):
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    UNKNOWN_OUTCOME = "UNKNOWN_OUTCOME"
    RETRY_EXHAUSTED = "RETRY_EXHAUSTED"


def bounded_name(value: str) -> None:
    if not value or value != value.strip() or len(value) > 200:
        raise ValueError("Expected a trimmed identifier of 1-200 characters")


@dataclass(frozen=True)
class OutboxEvent:
    id: UUID
    aggregate_type: str
    aggregate_id: UUID
    aggregate_version: int
    event_type: str
    occurred_at: datetime
    payload: tuple[tuple[str, UUID], ...] = ()

    def __post_init__(self) -> None:
        bounded_name(self.aggregate_type)
        bounded_name(self.event_type)
        require_instant(self.occurred_at)
        if type(self.aggregate_version) is not int or self.aggregate_version < 1:
            raise ValueError("Positive aggregate version required")
        if len(self.payload) > 32 or len(dict(self.payload)) != len(self.payload):
            raise ValueError("Bounded unique payload keys required")
        for key, value in self.payload:
            bounded_name(key)
            if not isinstance(value, UUID):
                raise ValueError("Outbox payloads contain opaque UUIDs only")

    @property
    def dedupe_key(self) -> str:
        return f"{self.aggregate_type}:{self.aggregate_id}:{self.aggregate_version}"


@dataclass(frozen=True)
class Lease:
    token: UUID
    now: datetime
    until: datetime

    def __post_init__(self) -> None:
        if (
            not timedelta(0)
            < require_instant(self.until) - require_instant(self.now)
            <= timedelta(minutes=15)
        ):
            raise ValueError("Lease must last between zero and fifteen minutes")


@dataclass(frozen=True)
class JobScope:
    """Trusted worker's closed allowlist; never derived from a browser request."""

    kinds: frozenset[str]

    def __post_init__(self) -> None:
        if not self.kinds:
            raise ValueError("Explicit job kinds required")
        for kind in self.kinds:
            bounded_name(kind)


@dataclass(frozen=True)
class BackgroundJob:
    id: UUID
    kind: str
    source_event_id: UUID | None
    dedupe_key: str
    status: JobStatus
    attempt_count: int
    lease_until: datetime | None
    next_attempt_at: datetime | None
    last_error_code: str | None
    version: int
    created_at: datetime

    def __post_init__(self) -> None:
        bounded_name(self.kind)
        if not isinstance(self.status, JobStatus):
            raise ValueError("Closed job status required")
        if type(self.attempt_count) is not int or not 0 <= self.attempt_count <= 8:
            raise ValueError("Attempts must be between zero and eight")
        if type(self.version) is not int or self.version < 1:
            raise ValueError("Positive version required")
        require_instant(self.created_at)
        for instant in (self.lease_until, self.next_attempt_at):
            if instant is not None:
                require_instant(instant)
        if (self.status == JobStatus.RUNNING) != (self.lease_until is not None):
            raise ValueError("Only running jobs carry leases")
        if self.status == JobStatus.RUNNING and self.attempt_count == 0:
            raise ValueError("Running jobs require an attempt")
        if self.status in (JobStatus.QUEUED, JobStatus.FAILED) and self.next_attempt_at is None:
            raise ValueError("Pending jobs require a due time")
        if self.last_error_code is not None:
            FailureCode(self.last_error_code)

    def claim(self, now: datetime, lease_until: datetime) -> BackgroundJob:
        now, lease_until = require_instant(now), require_instant(lease_until)
        reclaimable = (
            self.status in (JobStatus.QUEUED, JobStatus.FAILED)
            and self.next_attempt_at is not None
            and self.next_attempt_at <= now
        ) or (
            self.status == JobStatus.RUNNING
            and self.lease_until is not None
            and self.lease_until <= now
        )
        if not reclaimable or not timedelta(0) < lease_until - now <= timedelta(minutes=15):
            raise ValueError("Job is not due or lease is invalid")
        if self.attempt_count >= 8 or now >= self.created_at + timedelta(hours=24):
            return self.dead_letter(FailureCode.RETRY_EXHAUSTED)
        return replace(
            self,
            status=JobStatus.RUNNING,
            attempt_count=self.attempt_count + 1,
            lease_until=lease_until,
            next_attempt_at=None,
            version=self.version + 1,
        )

    def succeed(self) -> BackgroundJob:
        self._require_running()
        return replace(
            self,
            status=JobStatus.SUCCEEDED,
            lease_until=None,
            next_attempt_at=None,
            last_error_code=None,
            version=self.version + 1,
        )

    def retry_at(
        self,
        now: datetime,
        retry_after: timedelta | None = None,
        jitter: float = 1.0,
    ) -> datetime:
        self._require_running()
        if not 0.8 <= jitter <= 1.2 or (retry_after is not None and retry_after < timedelta(0)):
            raise ValueError("Invalid retry delay")
        delays = (60, 300, 900, 3600, 21600)
        delay = timedelta(seconds=delays[min(self.attempt_count - 1, 4)] * jitter)
        return require_instant(now) + max(delay, retry_after or timedelta(0))

    def retry(self, code: FailureCode, next_at: datetime) -> BackgroundJob:
        self._require_running()
        next_at = require_instant(next_at)
        if not isinstance(code, FailureCode):
            raise ValueError("Only redacted failure codes may be persisted")
        if (
            code in (FailureCode.CONFIGURATION_ERROR, FailureCode.UNKNOWN_OUTCOME)
            or self.attempt_count >= 8
            or next_at >= self.created_at + timedelta(hours=24)
        ):
            return self.dead_letter(code)
        return replace(
            self,
            status=JobStatus.FAILED,
            lease_until=None,
            next_attempt_at=next_at,
            last_error_code=code.value,
            version=self.version + 1,
        )

    def dead_letter(self, code: FailureCode) -> BackgroundJob:
        if self.status in (JobStatus.SUCCEEDED, JobStatus.DEAD_LETTER):
            raise ValueError("Terminal jobs require an explicit reviewed operation")
        if not isinstance(code, FailureCode):
            raise ValueError("Only redacted failure codes may be persisted")
        return replace(
            self,
            status=JobStatus.DEAD_LETTER,
            lease_until=None,
            next_attempt_at=None,
            last_error_code=code.value,
            version=self.version + 1,
        )

    def _require_running(self) -> None:
        if self.status != JobStatus.RUNNING or self.attempt_count < 1:
            raise ValueError("Only a running job may complete or retry")


@dataclass(frozen=True)
class VerifiedWebhook:
    provider: str
    provider_event_id: str
    payload_ciphertext: bytes
    received_at: datetime

    def __post_init__(self) -> None:
        bounded_name(self.provider)
        bounded_name(self.provider_event_id)
        require_instant(self.received_at)
        if not 1 <= len(self.payload_ciphertext) <= 262144:
            raise ValueError("Encrypted payload must be bounded to 256 KiB")


@dataclass(frozen=True)
class InboxInsertOutcome:
    id: UUID
    inserted: bool


@dataclass(frozen=True)
class WebhookInbox:
    id: UUID
    provider: str
    provider_event_id: str
    received_at: datetime
    verified: bool
    payload_ciphertext: bytes
    status: str


@dataclass(frozen=True)
class JobView:
    id: UUID
    kind: str
    status: JobStatus
    attempts: int
    last_error_code: str | None
    next_attempt_at: datetime | None


@dataclass(frozen=True)
class JOB_OUTBOX_DISPATCHRequest:
    batch_size: int

    def __post_init__(self) -> None:
        if type(self.batch_size) is not int or not 1 <= self.batch_size <= 100:
            raise ValueError("Batch size must be an integer between 1 and 100")
