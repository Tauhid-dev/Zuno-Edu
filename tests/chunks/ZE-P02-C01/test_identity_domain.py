from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from zuno_edu.modules.identity.domain import (
    Account,
    AccountStatus,
    AuthError,
    Credential,
    MfaChallenge,
    MfaFactor,
    RecoveryCode,
    Role,
    RoleGrant,
    Session,
    VerifiedRecoveryProof,
    VerifiedSecondFactor,
    VerifiedTotpProof,
)

NOW = datetime(2026, 9, 25, 0, 0, tzinfo=UTC)


def test_role_boundary_and_inactive_accounts() -> None:
    with pytest.raises(AuthError, match="INCOMPATIBLE_ROLE"):
        RoleGrant(Role.TEACHER, frozenset({"finance_admin"}))
    with pytest.raises(AuthError):
        RoleGrant(Role.ADMIN)
    for status in (AccountStatus.INVITED, AccountStatus.SUSPENDED, AccountStatus.CLOSED):
        account = Account(uuid4(), RoleGrant(Role.PARENT), status, "test@example.org", "Adult")
        with pytest.raises(AuthError, match="INVALID_CREDENTIALS"):
            account.require_login()


def test_staff_activation_requires_mfa() -> None:
    account = Account(uuid4(), RoleGrant(Role.TEACHER), AccountStatus.INVITED, "t@example.org", "T")
    with pytest.raises(AuthError):
        account.activate(NOW)
    account.mfa_enabled = True
    account.activate(NOW)
    assert account.status == AccountStatus.ACTIVE
    assert account.version == 2


@pytest.mark.parametrize(
    "staff,idle", [(True, timedelta(minutes=30)), (False, timedelta(hours=12))]
)
def test_session_expiry_rotation_and_revocation(staff: bool, idle: timedelta) -> None:
    session = Session(
        uuid4(),
        uuid4(),
        b"a" * 32,
        NOW,
        NOW,
        NOW + timedelta(days=7),
        staff,
        mfa_verified_at=NOW if staff else None,
    )
    assert session.is_active(NOW + idle - timedelta(microseconds=1))
    assert not session.is_active(NOW + idle)
    session.rotate(b"b" * 32, NOW + timedelta(minutes=1))
    assert session.token_hash == b"b" * 32
    session.last_seen_at = session.expires_at - timedelta(seconds=1)
    assert not session.is_active(session.expires_at)
    session.revoke(NOW)
    assert not session.is_active(NOW)
    with pytest.raises(AuthError):
        session.rotate(b"c" * 32, NOW)


def test_password_only_staff_session_has_no_authority() -> None:
    session = Session(uuid4(), uuid4(), b"a" * 32, NOW, NOW, NOW + timedelta(days=7), True)
    assert not session.is_active(NOW)


def test_credential_failure_window_cannot_be_reset_during_lockout() -> None:
    credential = Credential(uuid4(), "$argon2id$test", NOW)
    for _ in range(4):
        assert not credential.verify_attempt(False, NOW)
    assert credential.verify_attempt(False, NOW)
    assert credential.verify_attempt(True, NOW + timedelta(seconds=59))
    assert not credential.verify_attempt(True, NOW + timedelta(minutes=1))
    assert credential.failed_attempts == 0
    with pytest.raises(AuthError):
        credential.replace("plaintext", NOW)


def test_challenge_proof_is_bound_and_consumed_once() -> None:
    account, factor = uuid4(), uuid4()
    challenge = MfaChallenge(
        uuid4(), account, b"t" * 32, "setup", NOW + timedelta(minutes=10), b"browser", factor
    )
    for proof in (
        VerifiedSecondFactor(uuid4(), factor, b"browser", "setup"),
        VerifiedSecondFactor(account, uuid4(), b"browser", "setup"),
        VerifiedSecondFactor(account, factor, b"foreign", "setup"),
        VerifiedSecondFactor(account, factor, b"browser", "challenge"),
    ):
        with pytest.raises(AuthError):
            challenge.consume(proof, NOW)
        assert challenge.consumed_at is None
    proof = VerifiedSecondFactor(account, factor, b"browser", "setup")
    challenge.consume(proof, NOW)
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        challenge.consume(proof, NOW)


def test_challenge_attempt_and_expiry_boundaries() -> None:
    challenge = MfaChallenge(
        uuid4(), uuid4(), b"t" * 32, "challenge", NOW + timedelta(minutes=5), b"browser"
    )
    for _ in range(5):
        challenge.reject_attempt(NOW)
    with pytest.raises(AuthError, match="MFA_ATTEMPTS_EXCEEDED"):
        challenge.check("challenge", b"browser", NOW)
    with pytest.raises(AuthError, match="MFA_CHALLENGE_EXPIRED"):
        challenge.check("challenge", b"browser", NOW + timedelta(minutes=5))


def test_factor_timestep_and_recovery_are_single_use() -> None:
    factor = MfaFactor(uuid4(), uuid4(), b"encrypted", "v1")
    with pytest.raises(AuthError):
        factor.activate(VerifiedTotpProof(uuid4(), 1), NOW)
    factor.activate(VerifiedTotpProof(factor.id, 1), NOW)
    for step in (0, 1):
        with pytest.raises(AuthError, match="MFA_REPLAY"):
            factor.accept_step(step)
    factor.accept_step(2)
    recovery = RecoveryCode(uuid4(), factor.id, b"digest")
    with pytest.raises(AuthError):
        recovery.consume(VerifiedRecoveryProof(uuid4(), b"digest"), NOW)
    recovery.consume(VerifiedRecoveryProof(factor.id, b"digest"), NOW)
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        recovery.consume(VerifiedRecoveryProof(factor.id, b"digest"), NOW)
    factor.revoke("replacement")
    with pytest.raises(AuthError):
        factor.accept_step(3)
