"""Framework-free transaction and time contracts shared by capability modules."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Protocol
from uuid import UUID
from zoneinfo import ZoneInfo

type EntityId = UUID


class VersionConflict(Exception):
    """The caller must reload current state before retrying (VERSION_CONFLICT/409)."""


@dataclass(frozen=True)
class Version:
    value: int = 1

    def __post_init__(self) -> None:
        if type(self.value) is not int or self.value < 1:
            raise ValueError("Version must be a positive integer")

    def next(self) -> Version:
        return Version(self.value + 1)


def require_instant(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone-aware instant required")
    return value.astimezone(UTC)


class Clock(Protocol):
    def now(self) -> datetime: ...
    def today(self, zone: str) -> date: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)

    def today(self, zone: str) -> date:
        return self.now().astimezone(ZoneInfo(zone)).date()


@dataclass
class FrozenClock:
    instant: datetime

    def now(self) -> datetime:
        return require_instant(self.instant)

    def today(self, zone: str) -> date:
        return self.now().astimezone(ZoneInfo(zone)).date()


class Transaction(Protocol):
    def __enter__(self) -> Transaction: ...
    def __exit__(self, *args: object) -> None: ...


@dataclass(frozen=True)
class CommitResult:
    event_ids: tuple[UUID, ...]


class UnitOfWork[Event, Audit](Protocol):
    def begin(self) -> Transaction: ...
    def commit(self, events: tuple[Event, ...], audit: tuple[Audit, ...]) -> CommitResult: ...
    def rollback(self) -> None: ...


type Wakeup = Callable[[UUID], None]
