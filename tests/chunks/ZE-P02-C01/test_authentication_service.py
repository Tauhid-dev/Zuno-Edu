from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from fakes import Store
from zuno_edu.modules.identity.application.contracts import RequestContext
from zuno_edu.modules.identity.application.service import AuthenticationService
from zuno_edu.modules.identity.domain import (
    Account,
    AccountStatus,
    AuthError,
    Credential,
    Role,
    RoleGrant,
)
from zuno_edu.modules.identity.infrastructure.crypto import (
    MfaVerifier,
    PasswordHasher,
    TokenIssuer,
    VersionedSecrets,
)
from zuno_edu.modules.identity.infrastructure.security import RequestSecurity
from zuno_edu.shared.persistence import FrozenClock

PASSWORD = "Synthetic password for tests 123!"
NOW = datetime(2026, 9, 25, tzinfo=UTC)


class Abuse:
    denied = False

    def check(self, operation: str, identity: str, network: str) -> None:
        if self.denied:
            raise AuthError("RATE_LIMITED")


class Harness:
    def __init__(self) -> None:
        self.clock = FrozenClock(NOW)
        self.store = Store(self.clock)
        self.passwords = PasswordHasher(lambda _: False)
        self.hash = self.passwords.hash(PASSWORD)
        self.tokens = TokenIssuer(self.clock)
        self.keys = VersionedSecrets({"k1": b"k" * 32}, "k1")
        self.verifier = MfaVerifier(self.keys)
        self.security = RequestSecurity(b"s" * 32, "https://zuno.test")
        self.browser = self.security.browser()
        self.context = RequestContext(
            self.browser, self.security.csrf(self.browser), "https://zuno.test", "synthetic-network"
        )
        self.cookies: list[str | None] = []
        self.abuse = Abuse()
        self.approved = True
        self.service = AuthenticationService(
            self.store.transaction,
            self.passwords,
            self.tokens,
            self.verifier,
            self.keys,
            self.security,
            self.abuse,
            self.clock,
            self.cookies.append,
            lambda _: self.approved,
            self.hash,
        )

    def account(
        self, role: Role = Role.TEACHER, status: AccountStatus = AccountStatus.ACTIVE
    ) -> UUID:
        id = uuid4()
        grants = frozenset({"identity_admin"}) if role == Role.ADMIN else frozenset()
        account = Account(id, RoleGrant(role, grants), status, f"{id}@example.org", "Synthetic")
        self.store.state.accounts[id] = account
        self.store.state.credentials[id] = Credential(id, self.hash, NOW)
        return id

    def login(self, id: UUID) -> str:
        outcome = self.service.login(
            self.context,
            {
                "identifier": self.store.state.accounts[id].email or "",
                "password": PASSWORD,
            },
        )
        assert outcome.session is None and outcome.status == "mfa_setup_required"
        assert outcome.setup_token
        return outcome.setup_token

    def enrol(self, token: str, key: UUID | None = None) -> dict[str, str]:
        request = {
            "password": PASSWORD,
            "setup_token": token,
            "Idempotency-Key": str(key or uuid4()),
        }
        self.service.enrol_mfa(self.context, request)
        return request

    def code(self, token: str) -> str:
        challenge = next(
            c
            for c in self.store.state.challenges.values()
            if c.token_hash == self.tokens.digest(token)
        )
        assert challenge.factor_id
        factor = self.store.state.factors[challenge.factor_id]
        seed = self.keys.open(factor.secret_reference, b"identity-totp-v1")
        return TOTP(seed, 6, hashes.SHA1(), 30).generate(self.clock.now().timestamp()).decode()

    def activate(self, id: UUID) -> tuple[str, ...]:
        token = self.login(id)
        self.enrol(token)
        view = self.service.confirm_mfa(
            self.context, {"setup_token": token, "code": self.code(token)}
        )
        assert view.session.role in {Role.TEACHER, Role.ADMIN}
        assert len(view.recovery_codes) == 10
        return view.recovery_codes


@pytest.fixture
def h() -> Harness:
    return Harness()


def test_unknown_wrong_and_suspended_login_are_uniform(h: Harness) -> None:
    id = h.account(Role.PARENT)
    for identifier, password in (
        ("absent@example.org", PASSWORD),
        (str(h.store.state.accounts[id].email), "Wrong synthetic password"),
    ):
        with pytest.raises(AuthError, match="^INVALID_CREDENTIALS$"):
            h.service.login(h.context, {"identifier": identifier, "password": password})
    h.store.state.accounts[id].suspend("test")
    with pytest.raises(AuthError, match="^INVALID_CREDENTIALS$"):
        h.service.login(
            h.context, {"identifier": str(h.store.state.accounts[id].email), "password": PASSWORD}
        )
    assert not h.store.state.sessions


@pytest.mark.parametrize("role", [Role.PARENT, Role.STUDENT])
def test_full_session_logout_and_current_status_recheck(h: Harness, role: Role) -> None:
    id = h.account(role)
    view = h.service.login(
        h.context, {"identifier": str(h.store.state.accounts[id].email), "password": PASSWORD}
    )
    assert view.session and view.session.user_id == id
    context = replace(h.context, session_token=h.cookies[-1])
    assert h.service.get_session(context, {}).user_id == id
    h.service.logout(context, {})
    with pytest.raises(AuthError, match="UNAUTHENTICATED"):
        h.service.get_session(context, {})
    h.service.login(
        h.context, {"identifier": str(h.store.state.accounts[id].email), "password": PASSWORD}
    )
    context = replace(h.context, session_token=h.cookies[-1])
    h.store.state.accounts[id].suspend("test revocation")
    with pytest.raises(AuthError, match="UNAUTHENTICATED"):
        h.service.get_session(context, {})


def test_limited_context_cannot_be_used_as_full_session(h: Harness) -> None:
    token = h.login(h.account())
    assert h.cookies[-1] is None and not h.store.state.sessions
    with pytest.raises(AuthError, match="UNAUTHENTICATED"):
        h.service.get_session(replace(h.context, session_token=token), {})


def test_enrolment_replay_and_changed_body_never_reemit_setup(h: Harness) -> None:
    id = h.account()
    token = h.login(id)
    request = h.enrol(token)
    before = len(h.store.state.factors), len(h.store.state.challenges)
    with pytest.raises(AuthError, match="^MFA_REPLAY$"):
        h.service.enrol_mfa(h.context, request)
    fresh = h.login(id)
    with pytest.raises(AuthError, match="IDEMPOTENCY_CONFLICT"):
        h.service.enrol_mfa(h.context, {**request, "setup_token": fresh})
    assert len(h.store.state.factors) == before[0]
    for digest, expires in h.store.state.digests.values():
        assert PASSWORD.encode() not in digest
        assert token.encode() not in digest
        assert expires == NOW + timedelta(days=7)


def test_new_key_requires_fresh_setup_context_and_restart_invalidates_old_proof(h: Harness) -> None:
    id = h.account()
    first = h.login(id)
    h.enrol(first)
    old_code = h.code(first)
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.enrol(first)
    second = h.login(id)
    h.enrol(second)
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.service.confirm_mfa(h.context, {"setup_token": first, "code": old_code})
    assert sum(f.status == "pending" for f in h.store.state.factors.values()) == 1
    h.service.confirm_mfa(h.context, {"setup_token": second, "code": h.code(second)})
    assert sum(f.status == "active" for f in h.store.state.factors.values()) == 1


def test_enrolment_rollback_then_retry_and_uncertain_commit(h: Harness) -> None:
    token = h.login(h.account())
    request = {"password": PASSWORD, "setup_token": token, "Idempotency-Key": str(uuid4())}
    h.store.fail_commit = True
    with pytest.raises(RuntimeError):
        h.service.enrol_mfa(h.context, request)
    assert not h.store.state.factors and not h.store.state.digests
    h.store.fail_commit = False
    h.store.uncertain_commit = True
    with pytest.raises(RuntimeError):
        h.service.enrol_mfa(h.context, request)
    h.store.uncertain_commit = False
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.service.enrol_mfa(h.context, request)
    assert len(h.store.state.factors) == 1


def test_concurrent_duplicate_emits_one_setup(h: Harness) -> None:
    token = h.login(h.account())
    request = {"password": PASSWORD, "setup_token": token, "Idempotency-Key": str(uuid4())}

    def call() -> str:
        try:
            h.service.enrol_mfa(h.context, request)
            return "success"
        except AuthError as exc:
            return exc.code

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda _: call(), range(2)))
    assert sorted(results) == ["MFA_REPLAY", "success"]
    assert len(h.store.state.factors) == 1


@pytest.mark.parametrize(
    "failure", ["browser", "expired", "consumed", "suspended", "csrf", "origin"]
)
def test_setup_denies_invalid_context_without_mutation(h: Harness, failure: str) -> None:
    id = h.account()
    token = h.login(id)
    context = h.context
    if failure == "browser":
        browser = h.security.browser()
        context = replace(context, browser_token=browser, csrf_token=h.security.csrf(browser))
    if failure == "expired":
        h.clock.instant += timedelta(minutes=10)
    if failure == "consumed":
        next(iter(h.store.state.challenges.values())).consumed_at = NOW
    if failure == "suspended":
        h.store.state.accounts[id].suspend("test")
    if failure == "csrf":
        context = replace(context, csrf_token="forged")
    if failure == "origin":
        context = replace(context, origin="https://foreign.test")
    with pytest.raises(AuthError):
        h.service.enrol_mfa(
            context, {"password": PASSWORD, "setup_token": token, "Idempotency-Key": str(uuid4())}
        )
    assert not h.store.state.factors


def test_confirmation_replay_and_recovery_login_replay(h: Harness) -> None:
    id = h.account(Role.ADMIN)
    codes = h.activate(id)
    outcome = h.service.login(
        h.context, {"identifier": str(h.store.state.accounts[id].email), "password": PASSWORD}
    )
    assert outcome.challenge_token and outcome.session is None
    view = h.service.verify_mfa(
        h.context, {"challenge_token": outcome.challenge_token, "code": codes[0]}
    )
    assert view.role == Role.ADMIN
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.service.verify_mfa(
            h.context, {"challenge_token": outcome.challenge_token, "code": codes[0]}
        )
    outcome = h.service.login(
        h.context, {"identifier": str(h.store.state.accounts[id].email), "password": PASSWORD}
    )
    assert outcome.challenge_token
    with pytest.raises(AuthError, match="MFA_REPLAY"):
        h.service.verify_mfa(
            h.context, {"challenge_token": outcome.challenge_token, "code": codes[0]}
        )


def test_replacement_preserves_active_factor_and_codes_until_confirmed(h: Harness) -> None:
    id = h.account()
    codes = h.activate(id)
    old_factor = next(f for f in h.store.state.factors.values() if f.status == "active").id
    context = replace(h.context, session_token=h.cookies[-1])
    setup = h.service.enrol_mfa(context, {"password": PASSWORD, "Idempotency-Key": str(uuid4())})
    assert h.store.state.factors[old_factor].status == "active"
    assert all(c.consumed_at is None for c in h.store.state.codes.values())
    h.clock.instant += timedelta(seconds=30)
    h.service.confirm_mfa(
        context, {"setup_token": setup.setup_token, "code": h.code(setup.setup_token)}
    )
    assert h.store.state.factors[old_factor].status == "revoked"
    assert all(c.consumed_at for c in h.store.state.codes.values() if c.factor_id == old_factor)
    assert len(codes) == 10


def test_reset_uniform_adult_only_single_use_and_revokes(h: Harness) -> None:
    id = h.account(Role.PARENT)
    student = h.account(Role.STUDENT)
    for email in ("absent@example.org", str(h.store.state.accounts[student].email)):
        h.service.request_password_reset(h.context, {"email": email})
    assert not h.store.state.notifications
    h.service.login(
        h.context, {"identifier": str(h.store.state.accounts[id].email), "password": PASSWORD}
    )
    context = replace(h.context, session_token=h.cookies[-1])
    h.service.request_password_reset(h.context, {"email": str(h.store.state.accounts[id].email)})
    token = h.store.state.notifications[-1]
    assert token.expires_at == NOW + timedelta(minutes=30)
    request = {"token": token.value, "new_password": "Changed synthetic password 456!"}
    h.service.reset_password(h.context, request)
    with pytest.raises(AuthError):
        h.service.reset_password(h.context, request)
    with pytest.raises(AuthError):
        h.service.get_session(context, {})
    assert h.passwords.verify(request["new_password"], h.store.state.credentials[id].password_hash)


def test_invitation_single_use_requires_human_gate_and_only_limited_context(h: Harness) -> None:
    id = h.account(Role.TEACHER, AccountStatus.INVITED)
    token = h.tokens.issue("invitation", id, timedelta(hours=24))
    h.store.state.tokens[token.token_hash] = token
    request = {"token": token.value, "password": PASSWORD}
    h.approved = False
    with pytest.raises(AuthError, match="FORBIDDEN"):
        h.service.accept_staff_invitation(h.context, request)
    assert token.token_hash not in h.store.state.used
    h.approved = True
    result = h.service.accept_staff_invitation(h.context, request)
    assert result.account.status == "pending_verification"
    assert not h.store.state.sessions
    with pytest.raises(AuthError):
        h.service.accept_staff_invitation(h.context, request)
    h.enrol(result.setup_token)


def test_abuse_outage_fails_closed(h: Harness) -> None:
    id = h.account()
    h.abuse.denied = True
    with pytest.raises(AuthError, match="RATE_LIMITED"):
        h.login(id)
    assert not h.store.state.challenges
