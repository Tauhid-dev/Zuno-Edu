"""Immutable server authority and reusable, fail-closed policy results."""

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Protocol
from uuid import UUID

from zuno_edu.modules.identity.domain import AccountStatus, AuthError, Role, RoleGrant
from zuno_edu.shared.persistence import require_instant

RECENT_MFA_MAX_AGE = timedelta(minutes=30)


def require_recent_mfa(verified_at: datetime | None, now: datetime) -> None:
    if verified_at is None:
        raise AuthError("FORBIDDEN")
    age = require_instant(now) - require_instant(verified_at)
    if not timedelta(0) <= age < RECENT_MFA_MAX_AGE:
        raise AuthError("FORBIDDEN")


@dataclass(frozen=True)
class Principal:
    account_id: UUID
    role: RoleGrant
    account_status: AccountStatus
    authentication_time: datetime
    mfa_verified_at: datetime | None
    request_id: UUID
    session_id: UUID
    token_hash: bytes = field(repr=False)

    def require_active(self) -> None:
        if self.account_status != AccountStatus.ACTIVE:
            raise AuthError("FORBIDDEN")

    def require_capability(self, capability: str, now: datetime) -> None:
        self.require_active()
        if not self.role.allows(capability):
            raise AuthError("FORBIDDEN")
        require_recent_mfa(self.mfa_verified_at, now)


@dataclass(frozen=True)
class AdminCapabilityScope:
    principal: Principal
    capability: str

    def require(self, capability: str, now: datetime) -> None:
        if self.capability != capability:
            raise AuthError("FORBIDDEN")
        self.principal.require_capability(capability, now)


@dataclass(frozen=True)
class StudentScope:
    actor_id: UUID
    student_id: UUID
    purpose: str
    resource_id: UUID
    released_only: bool = True


@dataclass(frozen=True)
class FamilyScope:
    actor_id: UUID
    family_id: UUID
    student_ids: frozenset[UUID]
    purpose: str


@dataclass(frozen=True)
class TeachingScope:
    actor_id: UUID
    cohort_id: UUID
    student_id: UUID
    purpose: str


@dataclass(frozen=True)
class BillingScope:
    actor_id: UUID
    family_id: UUID
    purpose: str


class Relationships(Protocol):
    """Owning feature adapters resolve CURRENT links in their transaction/SQL.

    No cache or request fields can supply these relationships. The returned scope
    must also be applied to repository WHERE predicates and explicit projections.
    """

    def own_student(self, actor: UUID) -> UUID | None: ...
    def guardian_link(self, actor: UUID, student: UUID) -> UUID | None: ...
    def billing_membership(self, actor: UUID, family: UUID) -> bool: ...
    def teaching_assignment(self, actor: UUID, cohort: UUID, student: UUID) -> bool: ...
    def released_for_entitled_enrolment(self, student: UUID, resource: UUID) -> bool: ...
    def learner_enrolment(self, student: UUID, cohort: UUID) -> bool: ...


class ResourcePolicy:
    def __init__(
        self, relationships: Relationships, current: Callable[[Principal], Principal]
    ) -> None:
        self._relationships, self._current = relationships, current

    def education(self, actor: Principal, student: UUID, resource: UUID) -> StudentScope:
        actor = self._current(actor)
        actor.require_active()
        if actor.role.role == Role.STUDENT:
            allowed = self._relationships.own_student(actor.account_id) == student
        elif actor.role.role == Role.PARENT:
            allowed = self._relationships.guardian_link(actor.account_id, student) is not None
        else:
            raise AuthError("FORBIDDEN")
        if not allowed or not self._relationships.released_for_entitled_enrolment(
            student, resource
        ):
            raise AuthError("NOT_FOUND")
        return StudentScope(actor.account_id, student, "released_education", resource)

    def billing(self, actor: Principal, family: UUID) -> BillingScope:
        actor = self._current(actor)
        actor.require_active()
        if actor.role.role != Role.PARENT:
            raise AuthError("FORBIDDEN")
        if not self._relationships.billing_membership(actor.account_id, family):
            raise AuthError("NOT_FOUND")
        return BillingScope(actor.account_id, family, "family_billing")

    def teaching(self, actor: Principal, cohort: UUID, student: UUID) -> TeachingScope:
        actor = self._current(actor)
        actor.require_active()
        if actor.role.role != Role.TEACHER:
            raise AuthError("FORBIDDEN")
        if not self._relationships.teaching_assignment(
            actor.account_id, cohort, student
        ) or not self._relationships.learner_enrolment(student, cohort):
            raise AuthError("NOT_FOUND")
        return TeachingScope(actor.account_id, cohort, student, "assigned_education")
