from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import pytest
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from zuno_edu.domain.policies import (
    AdminCapabilityScope,
    Principal,
    ResourcePolicy,
    require_recent_mfa,
)
from zuno_edu.infrastructure.persistence.database import Database
from zuno_edu.infrastructure.persistence.tables import accounts, audit_records, sessions
from zuno_edu.modules.identity.domain import AccountStatus, AuthError, Role, RoleGrant
from zuno_edu.modules.operations.application.audit import AuditFilter, AuditService
from zuno_edu.modules.operations.domain.audit import AuditRecord
from zuno_edu.modules.operations.infrastructure.audit import AuditTransactions, SqlAuditTransaction
from zuno_edu.presentation.http.pagination import CursorCodec
from zuno_edu.shared.persistence import FrozenClock

NOW = datetime(2026, 9, 25, tzinfo=UTC)


def seed(
    db: Database, role: str = "admin", privileges: tuple[str, ...] = ("audit_admin",)
) -> Principal:
    subject, session_id, token_hash = uuid4(), uuid4(), uuid4().bytes * 2
    with db.engine.begin() as c:
        c.execute(
            accounts.insert().values(
                id=subject,
                role=role,
                admin_privileges=list(privileges),
                email=f"{subject}@example.org",
                display_name="Synthetic",
                status="active",
                mfa_enabled=True,
            )
        )
        c.execute(
            sessions.insert().values(
                id=session_id,
                account_id=subject,
                token_hash=token_hash,
                created_at=NOW,
                last_seen_at=NOW,
                expires_at=NOW + timedelta(days=1),
                mfa_verified_at=NOW,
            )
        )
    return Principal(
        subject,
        RoleGrant(Role(role), frozenset(privileges)),
        AccountStatus.ACTIVE,
        NOW,
        NOW,
        uuid4(),
        session_id,
        token_hash,
    )


def service(db: Database, clock: FrozenClock) -> AuditService:
    return AuditService(
        AuditTransactions(db.sessions, clock, lambda _: True, CursorCodec(b"x" * 32, clock)), clock
    )


def filters(**kwargs: object) -> AuditFilter:
    return AuditFilter(NOW - timedelta(days=1), NOW + timedelta(days=1), **kwargs)  # type: ignore[arg-type]


def record(actor: UUID, offset: int = 0) -> AuditRecord:
    return AuditRecord(
        uuid4(),
        actor,
        "authentication.login",
        "account",
        actor,
        NOW + timedelta(seconds=offset),
        uuid4(),
        "allowed",
    )


@pytest.mark.parametrize(
    "age,allowed",
    [
        (timedelta(minutes=30) - timedelta(microseconds=1), True),
        (timedelta(minutes=30), False),
        (timedelta(minutes=31), False),
        (timedelta(seconds=-1), False),
        (None, False),
    ],
)
def test_fixed_recent_mfa_boundary(age: timedelta | None, allowed: bool) -> None:
    verified = None if age is None else NOW - age
    if allowed:
        require_recent_mfa(verified, NOW)
    else:
        with pytest.raises(AuthError, match="FORBIDDEN"):
            require_recent_mfa(verified, NOW)


@pytest.mark.parametrize("role", [Role.PARENT, Role.STUDENT, Role.TEACHER])
def test_incompatible_admin_grants(role: Role) -> None:
    with pytest.raises(AuthError, match="INCOMPATIBLE_ROLE"):
        RoleGrant(role, frozenset({"finance_admin"}))


def test_immutable_redacted_record_rejects_payloads() -> None:
    r = record(uuid4())
    with pytest.raises(FrozenInstanceError):
        r.reason = "password"  # type: ignore[misc]
    changes: tuple[dict[str, Any], ...] = (
        {"reason": "child private work"},
        {"action": "secret_token"},
        {"resource_type": "https://secret"},
    )
    for change in changes:
        with pytest.raises(ValueError, match="vocabulary"):
            replace(r, **change)


@pytest.mark.parametrize(
    "role,privileges",
    [
        ("parent", ()),
        ("student", ()),
        ("teacher", ()),
        ("admin", ("education_admin",)),
        ("admin", ("finance_admin",)),
    ],
)
def test_denied_roles_never_receive_audit(
    db: Database, role: str, privileges: tuple[str, ...]
) -> None:
    actor = seed(db, role, privileges)
    with pytest.raises(AuthError, match="FORBIDDEN"):
        service(db, FrozenClock(NOW)).list_audit(actor, filters())
    with db.engine.connect() as c:
        assert c.execute(sa.select(audit_records.c.action)).scalars().all() == ["audit.denied"]


def test_scoped_audit_pagination_filters_and_revocation(db: Database) -> None:
    actor, foreign = seed(db), seed(db)
    clock = FrozenClock(NOW + timedelta(seconds=5))
    transactions = AuditTransactions(
        db.sessions, clock, lambda _: True, CursorCodec(b"x" * 32, clock)
    )
    with transactions() as tx:
        for i in range(3):
            tx.audit.append(record(actor.account_id, i))
        tx.audit.append(record(foreign.account_id))
        tx.commit()
    api = service(db, clock)
    page = api.list_audit(
        actor, filters(actor_id=actor.account_id, action="authentication.login", limit=2)
    )
    assert len(page.items) == 2 and page.page.has_more and page.page.next_cursor
    assert all(r.actor_id == actor.account_id for r in page.items)
    second = api.list_audit(
        actor,
        filters(
            actor_id=actor.account_id,
            action="authentication.login",
            limit=2,
            cursor=page.page.next_cursor,
        ),
    )
    assert len(second.items) == 1 and not second.page.has_more
    assert set(r.id for r in page.items).isdisjoint(r.id for r in second.items)
    with pytest.raises(AuthError, match="VALIDATION_ERROR"):
        api.list_audit(
            foreign,
            filters(
                actor_id=actor.account_id,
                action="authentication.login",
                limit=2,
                cursor=page.page.next_cursor,
            ),
        )
    with db.engine.begin() as c:
        c.execute(
            accounts.update()
            .where(accounts.c.id == actor.account_id)
            .values(admin_privileges=["identity_admin"])
        )
    with pytest.raises(AuthError, match="UNAUTHENTICATED"):
        api.list_audit(actor, filters())
    with db.engine.connect() as c:
        assert (
            c.execute(
                sa.select(sessions.c.revoked_at).where(sessions.c.id == actor.session_id)
            ).scalar_one()
            is not None
        )


@pytest.mark.parametrize("mfa", [None, NOW - timedelta(minutes=31), NOW + timedelta(seconds=1)])
def test_repository_rechecks_current_evidence(db: Database, mfa: object) -> None:
    actor = seed(db)
    with db.engine.begin() as c:
        c.execute(
            sessions.update().where(sessions.c.id == actor.session_id).values(mfa_verified_at=mfa)
        )
    clock = FrozenClock(NOW)
    with db.sessions.begin() as session:
        tx = SqlAuditTransaction(session, clock, lambda _: True, CursorCodec(b"x" * 32, clock))
        with pytest.raises(AuthError, match="FORBIDDEN|UNAUTHENTICATED"):
            tx.audit.list_redacted(AdminCapabilityScope(actor, "audit_admin"), filters())


def test_audit_append_only_and_role_grants(db: Database) -> None:
    actor = seed(db)
    with AuditTransactions(
        db.sessions, FrozenClock(NOW), lambda _: True, CursorCodec(b"x" * 32, FrozenClock(NOW))
    )() as tx:
        tx.audit.append(record(actor.account_id))
        tx.commit()
    for statement in (
        audit_records.update().values(reason="FORBIDDEN"),
        audit_records.delete(),
        sa.text("TRUNCATE audit_records"),
    ):
        with pytest.raises(DBAPIError, match="append-only"):
            with db.engine.begin() as c:
                c.execute(statement)
    with db.engine.connect() as c:
        assert c.execute(
            sa.text("SELECT has_table_privilege('zuno_audit_writer','audit_records','INSERT')")
        ).scalar_one()
        assert not c.execute(
            sa.text(
                "SELECT "
                "has_table_privilege('zuno_audit_writer','audit_records','SELECT,UPDATE,DELETE,TRUNCATE')"
            )
        ).scalar_one()
        assert c.execute(
            sa.text("SELECT has_table_privilege('zuno_audit_reader','audit_records','SELECT')")
        ).scalar_one()
        assert not c.execute(
            sa.text(
                "SELECT "
                "has_table_privilege('zuno_audit_reader','audit_records','INSERT,UPDATE,DELETE,TRUNCATE')"
            )
        ).scalar_one()


class Links:
    def __init__(self) -> None:
        self.owner, self.child, self.family, self.cohort = uuid4(), uuid4(), uuid4(), uuid4()
        self.active = True
        self.billing = False
        self.release = True
        self.enrolled = True

    def own_student(self, actor: UUID) -> UUID | None:
        return self.child if self.active and actor == self.owner else None

    def guardian_link(self, actor: UUID, student: UUID) -> UUID | None:
        return (
            self.family if self.active and actor == self.owner and student == self.child else None
        )

    def billing_membership(self, actor: UUID, family: UUID) -> bool:
        return self.billing and actor == self.owner and family == self.family

    def teaching_assignment(self, actor: UUID, cohort: UUID, student: UUID) -> bool:
        return self.active and (actor, cohort, student) == (self.owner, self.cohort, self.child)

    def released_for_entitled_enrolment(self, student: UUID, resource: UUID) -> bool:
        return self.release and self.enrolled and student == self.child

    def learner_enrolment(self, student: UUID, cohort: UUID) -> bool:
        return self.enrolled and student == self.child and cohort == self.cohort


def test_relationships_release_and_purpose_are_independent() -> None:
    links = Links()
    actor = Principal(
        links.owner,
        RoleGrant(Role.PARENT),
        AccountStatus.ACTIVE,
        NOW,
        None,
        uuid4(),
        uuid4(),
        b"evidence",
    )
    policy = ResourcePolicy(links, lambda principal: principal)
    assert policy.education(actor, links.child, uuid4()).released_only
    with pytest.raises(AuthError, match="NOT_FOUND"):
        policy.billing(actor, links.family)
    for change in ("release", "active", "enrolled"):
        setattr(links, change, False)
        with pytest.raises(AuthError, match="NOT_FOUND"):
            policy.education(actor, links.child, uuid4())
        setattr(links, change, True)
    student = replace(actor, role=RoleGrant(Role.STUDENT))
    with pytest.raises(AuthError, match="NOT_FOUND"):
        policy.education(student, uuid4(), uuid4())
    teacher = replace(actor, role=RoleGrant(Role.TEACHER))
    assert policy.teaching(teacher, links.cohort, links.child)
    with pytest.raises(AuthError, match="FORBIDDEN"):
        policy.billing(teacher, links.family)
    links.active = False
    with pytest.raises(AuthError, match="NOT_FOUND"):
        policy.teaching(teacher, links.cohort, links.child)


def test_lock_wait_crossing_mfa_expiry_fails_closed(db: Database) -> None:
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    actor = seed(db)
    clock = FrozenClock(NOW + timedelta(minutes=29, seconds=59))
    # Keep idle expiry independent from freshness expiry.
    with db.engine.begin() as c:
        c.execute(
            sessions.update()
            .where(sessions.c.id == actor.session_id)
            .values(last_seen_at=clock.now())
        )
    waiting = Event()

    def began(
        conn: object,
        cursor: object,
        statement: str,
        parameters: object,
        context: object,
        many: bool,
    ) -> None:
        if "FOR UPDATE" in statement and "accounts" in statement:
            waiting.set()

    def attempt() -> str:
        try:
            service(db, clock).list_audit(actor, filters())
        except AuthError as e:
            return e.code
        return "UNEXPECTED_ALLOW"

    with db.engine.connect() as holder:
        transaction = holder.begin()
        holder.execute(
            sa.select(accounts.c.id).where(accounts.c.id == actor.account_id).with_for_update()
        )
        sa.event.listen(db.engine, "before_cursor_execute", began)
        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(attempt)
                assert waiting.wait(5)
                clock.instant = NOW + timedelta(minutes=30)
                transaction.commit()
                assert future.result(timeout=5) == "FORBIDDEN"
        finally:
            sa.event.remove(db.engine, "before_cursor_execute", began)
            if transaction.is_active:
                transaction.rollback()


def test_failed_audit_append_rolls_back_and_does_not_return_data(db: Database) -> None:
    actor = seed(db)
    clock = FrozenClock(NOW)
    with db.engine.begin() as c:
        c.execute(
            sa.text(
                "CREATE FUNCTION reject_audit() RETURNS trigger LANGUAGE plpgsql AS $$ "
                "BEGIN RAISE EXCEPTION 'synthetic append failure'; END $$"
            )
        )
        c.execute(
            sa.text(
                "CREATE TRIGGER reject_append BEFORE INSERT ON audit_records FOR EACH ROW "
                "EXECUTE FUNCTION reject_audit()"
            )
        )
    with pytest.raises(DBAPIError, match="synthetic append failure"):
        service(db, clock).list_audit(actor, filters())
    with db.engine.connect() as c:
        assert c.execute(sa.select(sa.func.count()).select_from(audit_records)).scalar_one() == 0


def test_false_cached_authority_and_purpose_fail_at_repository(db: Database) -> None:
    actor = seed(db, "teacher", ())
    forged = replace(actor, role=RoleGrant(Role.ADMIN, frozenset({"audit_admin"})))
    clock = FrozenClock(NOW)
    with db.sessions.begin() as session:
        tx = SqlAuditTransaction(session, clock, lambda _: True, CursorCodec(b"x" * 32, clock))
        with pytest.raises(AuthError, match="FORBIDDEN"):
            tx.audit.list_redacted(AdminCapabilityScope(forged, "audit_admin"), filters())
    admin = seed(db)
    with db.sessions.begin() as session:
        tx = SqlAuditTransaction(session, clock, lambda _: True, CursorCodec(b"x" * 32, clock))
        with pytest.raises(AuthError, match="FORBIDDEN"):
            tx.audit.list_redacted(AdminCapabilityScope(admin, "finance_admin"), filters())


def test_empty_audit_select_rechecks_after_table_lock_wait(db: Database) -> None:
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event

    actor = seed(db)
    clock = FrozenClock(NOW + timedelta(minutes=29, seconds=59))
    with db.engine.begin() as c:
        c.execute(
            sessions.update()
            .where(sessions.c.id == actor.session_id)
            .values(last_seen_at=clock.now())
        )
    waiting = Event()

    def began(
        conn: object,
        cursor: object,
        statement: str,
        parameters: object,
        context: object,
        many: bool,
    ) -> None:
        if "FROM audit_records" in statement:
            waiting.set()

    def attempt() -> str:
        try:
            service(db, clock).list_audit(actor, filters())
        except AuthError as e:
            return e.code
        return "UNEXPECTED_ALLOW"

    with db.engine.connect() as holder:
        transaction = holder.begin()
        holder.execute(sa.text("LOCK TABLE audit_records IN ACCESS EXCLUSIVE MODE"))
        sa.event.listen(db.engine, "before_cursor_execute", began)
        try:
            with ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(attempt)
                try:
                    assert waiting.wait(5)
                    clock.instant = NOW + timedelta(minutes=30)
                finally:
                    transaction.commit()
                assert future.result(timeout=5) == "FORBIDDEN"
        finally:
            sa.event.remove(db.engine, "before_cursor_execute", began)
            if transaction.is_active:
                transaction.rollback()


def test_resource_policy_refreshes_cached_principal_and_binds_resource() -> None:
    links = Links()
    actor = Principal(
        links.owner,
        RoleGrant(Role.PARENT),
        AccountStatus.ACTIVE,
        NOW,
        None,
        uuid4(),
        uuid4(),
        b"server-evidence",
    )
    resource = uuid4()
    current = actor
    policy = ResourcePolicy(links, lambda _: current)
    assert policy.education(actor, links.child, resource).resource_id == resource
    current = replace(actor, account_status=AccountStatus.SUSPENDED)
    with pytest.raises(AuthError, match="FORBIDDEN"):
        policy.education(actor, links.child, resource)
