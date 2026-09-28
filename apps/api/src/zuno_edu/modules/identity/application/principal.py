"""Resolve current server-owned session evidence inside the caller's transaction."""

from collections.abc import Callable
from uuid import UUID

from zuno_edu.domain.policies import Principal
from zuno_edu.modules.identity.domain import Account, AccountStatus, AuthError, Session
from zuno_edu.shared.persistence import Clock

from .ports import IdentityTransaction, SelfAuthScope


def current_identity(
    tx: IdentityTransaction, token_hash: bytes, clock: Clock, staff_approved: Callable[[UUID], bool]
) -> tuple[Account, Session]:
    session = tx.sessions.find_active(token_hash, clock.now())
    if session is None:
        raise AuthError("UNAUTHENTICATED")
    account = tx.users.get_scoped(session.user_id, SelfAuthScope(session.user_id))
    if account is None or account.status not in {AccountStatus.ACTIVE, AccountStatus.PENDING}:
        raise AuthError("UNAUTHENTICATED")
    if account.staff and (
        account.status != AccountStatus.ACTIVE
        or session.mfa_verified_at is None
        or not account.mfa_enabled
        or not staff_approved(account.id)
    ):
        raise AuthError("UNAUTHENTICATED")
    # Time is read after every identity lock and approval lookup.
    if not session.is_active(clock.now()):
        raise AuthError("UNAUTHENTICATED")
    return account, session


def principal_for(account: Account, session: Session, request_id: UUID) -> Principal:
    return Principal(
        account.id,
        account.role,
        account.status,
        session.created_at,
        session.mfa_verified_at,
        request_id,
        session.id,
        session.token_hash,
    )
