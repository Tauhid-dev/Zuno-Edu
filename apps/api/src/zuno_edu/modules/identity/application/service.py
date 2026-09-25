"""Authentication orchestration; all mutable identity state shares one transaction."""

from collections.abc import Callable, Mapping
from contextlib import AbstractContextManager
from datetime import timedelta
from typing import Protocol
from uuid import UUID, uuid4

from zuno_edu.modules.identity.domain import (
    Account,
    AccountStatus,
    AuthError,
    Credential,
    MfaChallenge,
    MfaFactor,
    RecoveryCode,
    Role,
    Session,
    VerifiedRecoveryProof,
    VerifiedSecondFactor,
    VerifiedTotpProof,
)
from zuno_edu.shared.persistence import Clock

from .contracts import (
    AccountView,
    AuthOutcomeView,
    MfaActivationView,
    MfaSetupView,
    RequestContext,
    SessionView,
    StaffSetupSessionView,
)
from .ports import (
    AbuseControls,
    IdentityTransaction,
    MfaVerifier,
    PasswordHasher,
    RequestDigests,
    SelfAuthScope,
    TokenIssuer,
)


class RequestSecurity(Protocol):
    def validate(self, context: RequestContext, *, mutation: bool) -> bytes: ...
    def csrf(self, browser_token: str) -> str: ...


class AuthenticationService:
    def __init__(
        self,
        transactions: Callable[[], AbstractContextManager[IdentityTransaction]],
        passwords: PasswordHasher,
        tokens: TokenIssuer,
        mfa: MfaVerifier,
        digests: RequestDigests,
        security: RequestSecurity,
        abuse: AbuseControls,
        clock: Clock,
        session_cookie: Callable[[str | None], None],
        staff_approved: Callable[[UUID], bool],
        dummy_password_hash: str,
    ) -> None:
        self._transactions = transactions
        self._passwords = passwords
        self._tokens = tokens
        self._mfa = mfa
        self._digests = digests
        self._security = security
        self._abuse = abuse
        self._clock = clock
        self._cookie = session_cookie
        self._staff_approved = staff_approved
        self._dummy = dummy_password_hash

    def _start(self, context: RequestContext, operation: str, identity: str) -> bytes:
        browser = self._security.validate(context, mutation=True)
        self._abuse.check(operation, identity.casefold().strip(), context.network)
        return browser

    def _session_view(
        self, account: Account, session: Session, context: RequestContext
    ) -> SessionView:
        return SessionView(
            account.id,
            account.role.role,
            tuple(sorted(account.role.admin_privileges)),
            account.display_name,
            session.expires_at,
            self._security.csrf(context.browser_token),
            False,
        )

    def _new_session(
        self, tx: IdentityTransaction, account: Account, context: RequestContext, mfa: bool
    ) -> tuple[SessionView, str]:
        if account.staff and (not mfa or not self._staff_approved(account.id)):
            raise AuthError("FORBIDDEN")
        account.require_login()
        if account.staff and account.status != AccountStatus.ACTIVE:
            raise AuthError("FORBIDDEN")
        now = self._clock.now()
        token = self._tokens.issue("session", account.id, timedelta(days=7))
        session = Session(
            uuid4(),
            account.id,
            token.token_hash,
            now,
            now,
            token.expires_at,
            account.staff,
            mfa_verified_at=now if mfa else None,
        )
        # Successful authentication replaces the browser's previous full session.
        if context.session_token:
            previous = tx.sessions.find_active(self._tokens.digest(context.session_token), now)
            if previous:
                previous.revoke(now)
                tx.sessions.save(previous)
        tx.sessions.save(session)
        return self._session_view(account, session, context), token.value

    def _limited(
        self, tx: IdentityTransaction, account: Account, browser: bytes, purpose: str
    ) -> tuple[MfaChallenge, str]:
        ttl = timedelta(minutes=5 if purpose == "challenge" else 10)
        token = self._tokens.issue(purpose, account.id, ttl)
        factor = tx.mfa.get_factor_for_update(account.id, SelfAuthScope(account.id))
        challenge = MfaChallenge(
            uuid4(),
            account.id,
            token.token_hash,
            purpose,
            token.expires_at,
            browser,
            factor.id if factor is not None and purpose == "challenge" else None,
        )
        tx.mfa.save_challenge(challenge)
        return challenge, token.value

    def login(self, principal: RequestContext, request: Mapping[str, str]) -> AuthOutcomeView:
        identifier, password = request["identifier"].strip().casefold(), request["password"]
        browser = self._start(principal, "login", identifier)
        cookie: str | None = None
        with self._transactions() as tx:
            found = tx.users.find_login(identifier)
            valid = self._passwords.verify(
                password, found.credential.password_hash if found else self._dummy
            )
            if found is None:
                raise AuthError("INVALID_CREDENTIALS")
            account, credential = found.account, found.credential
            locked = credential.verify_attempt(valid, self._clock.now())
            tx.save_credential(credential)
            if (
                not valid
                or locked
                or account.status not in {AccountStatus.ACTIVE, AccountStatus.PENDING}
            ):
                tx.commit("authentication.login_denied", account.id)
                raise AuthError("INVALID_CREDENTIALS")
            if self._passwords.needs_rehash(credential.password_hash):
                credential.replace(self._passwords.hash(password), self._clock.now())
                tx.save_credential(credential)
            if account.staff:
                if not self._staff_approved(account.id):
                    raise AuthError("FORBIDDEN")
                factor = tx.mfa.get_factor_for_update(account.id, SelfAuthScope(account.id))
                purpose = "challenge" if factor else "setup"
                challenge, token = self._limited(tx, account, browser, purpose)
                result = AuthOutcomeView(
                    "mfa_challenge" if factor else "mfa_setup_required",
                    None,
                    token if factor else None,
                    None if factor else token,
                    challenge.expires_at,
                )
            else:
                view, cookie = self._new_session(tx, account, principal, False)
                result = AuthOutcomeView("authenticated", view, None, None, view.expires_at)
            tx.commit("authentication.login", account.id)
        self._cookie(cookie)
        return result

    def _challenge(
        self, tx: IdentityTransaction, token: str, browser: bytes, purpose: str
    ) -> tuple[Account, MfaChallenge]:
        challenge = tx.mfa.get_challenge_for_update(self._tokens.digest(token), browser)
        if challenge is None:
            raise AuthError("UNAUTHENTICATED")
        challenge.check(purpose, browser, self._clock.now())
        account = tx.users.get_scoped(challenge.account_id, SelfAuthScope(challenge.account_id))
        if account is None or not account.staff:
            raise AuthError("UNAUTHENTICATED")
        account.require_login()
        if not self._staff_approved(account.id):
            raise AuthError("FORBIDDEN")
        return account, challenge

    def _current(
        self, tx: IdentityTransaction, principal: RequestContext
    ) -> tuple[Account, Session]:
        if principal.session_token is None:
            raise AuthError("UNAUTHENTICATED")
        session = tx.sessions.find_active(
            self._tokens.digest(principal.session_token), self._clock.now()
        )
        if session is None:
            raise AuthError("UNAUTHENTICATED")
        if not session.is_active(self._clock.now()):
            raise AuthError("UNAUTHENTICATED")
        account = tx.users.get_scoped(session.user_id, SelfAuthScope(session.user_id))
        if account is None or account.status not in {AccountStatus.ACTIVE, AccountStatus.PENDING}:
            raise AuthError("UNAUTHENTICATED")
        if account.staff and (
            account.status != AccountStatus.ACTIVE
            or not session.mfa_verified_at
            or not account.mfa_enabled
            or not self._staff_approved(account.id)
        ):
            raise AuthError("UNAUTHENTICATED")
        return account, session

    def get_session(self, principal: RequestContext, request: Mapping[str, str]) -> SessionView:
        self._security.validate(principal, mutation=False)
        with self._transactions() as tx:
            account, session = self._current(tx, principal)
            session.last_seen_at = self._clock.now()
            tx.sessions.save(session)
            view = self._session_view(account, session, principal)
            tx.commit("authentication.session_accessed", account.id)
            return view

    def logout(self, principal: RequestContext, request: Mapping[str, str]) -> None:
        browser = self._start(principal, "logout", principal.browser_token)
        with self._transactions() as tx:
            if principal.session_token:
                account, session = self._current(tx, principal)
                session.revoke(self._clock.now())
                tx.sessions.save(session)
                subject = account.id
            elif request.get("setup_token"):
                account, challenge = self._challenge(tx, request["setup_token"], browser, "setup")
                challenge.consumed_at = self._clock.now()
                tx.mfa.save_challenge(challenge)
                subject = account.id
            else:
                raise AuthError("UNAUTHENTICATED")
            tx.commit("authentication.logout", subject)
        self._cookie(None)

    def enrol_mfa(self, principal: RequestContext, request: Mapping[str, str]) -> MfaSetupView:
        browser = self._start(principal, "enrol_mfa", principal.browser_token)
        key = UUID(request["Idempotency-Key"])
        now = self._clock.now()
        with self._transactions() as tx:
            challenge: MfaChallenge | None = None
            if request.get("setup_token"):
                account, challenge = self._challenge(tx, request["setup_token"], browser, "setup")
                if principal.session_token:
                    current, _ = self._current(tx, principal)
                    if current.id != account.id:
                        raise AuthError("FORBIDDEN")
            else:
                account, _ = self._current(tx, principal)
                if not account.staff:
                    raise AuthError("FORBIDDEN")
            scope = SelfAuthScope(account.id)
            credential = tx.credential(account.id, scope)
            now = self._clock.now()
            valid = self._passwords.verify(request["password"], credential.password_hash)
            locked = credential.verify_attempt(valid, now)
            tx.save_credential(credential)
            if not valid or locked:
                if challenge:
                    challenge.reject_attempt(now)
                    tx.mfa.save_challenge(challenge)
                tx.commit("authentication.enrolment_denied", account.id)
                raise AuthError("FORBIDDEN")
            active = tx.mfa.get_factor_for_update(account.id, scope)
            if active and challenge:
                # A limited password-only context cannot replace an existing factor.
                raise AuthError("FORBIDDEN")
            recorded = tx.enrolment_digest(account.id, key, now)
            if recorded is not None:
                if not self._digests.matches_request(recorded, request):
                    raise AuthError("IDEMPOTENCY_CONFLICT")
                raise AuthError("MFA_REPLAY")
            if challenge and challenge.factor_id is not None:
                # New key alone is not the required freshly authenticated restart.
                raise AuthError("MFA_REPLAY")
            tx.mfa.invalidate_pending_setup(account.id, scope)
            setup = self._mfa.generate_setup(account.email or str(account.id))
            factor = MfaFactor(uuid4(), account.id, setup.secret_reference, setup.key_version)
            tx.mfa.save_factor(factor, 0)
            if challenge:
                # Keep the original context bounds; it now names this exact pending factor.
                challenge.factor_id = factor.id
                setup_token = request["setup_token"]
            else:
                issued = self._tokens.issue("setup", account.id, timedelta(minutes=10))
                setup_token = issued.value
                challenge = MfaChallenge(
                    uuid4(),
                    account.id,
                    issued.token_hash,
                    "setup",
                    issued.expires_at,
                    browser,
                    factor.id,
                )
            tx.mfa.save_challenge(challenge)
            tx.record_enrolment(
                account.id, key, self._digests.request_digest(request), now + timedelta(days=7)
            )
            result = MfaSetupView(setup_token, setup.otpauth_uri, challenge.expires_at)
            tx.commit("authentication.mfa_enrolled", account.id)
        return result

    def _reject(self, tx: IdentityTransaction, challenge: MfaChallenge) -> None:
        challenge.reject_attempt(self._clock.now())
        tx.mfa.save_challenge(challenge)
        tx.commit("authentication.mfa_denied", challenge.account_id)

    def confirm_mfa(
        self, principal: RequestContext, request: Mapping[str, str]
    ) -> MfaActivationView:
        browser = self._start(principal, "confirm_mfa", principal.browser_token)
        now = self._clock.now()
        with self._transactions() as tx:
            account, challenge = self._challenge(tx, request["setup_token"], browser, "setup")
            now = self._clock.now()
            scope = SelfAuthScope(account.id)
            factor = tx.mfa.get_pending_factor_for_update(
                account.id, self._tokens.digest(request["setup_token"]), browser, scope
            )
            if factor is None:
                raise AuthError("MFA_REPLAY")
            try:
                step = self._mfa.verify_totp(factor.secret_reference, request["code"], now)
            except AuthError as exc:
                if exc.code == "INVALID_CREDENTIALS":
                    self._reject(tx, challenge)
                raise
            active = tx.mfa.get_factor_for_update(account.id, scope)
            previous_version = factor.version
            factor.activate(VerifiedTotpProof(factor.id, step), now)
            if active:
                old_version = active.version
                active.revoke("verified replacement")
                active.revoked_at = now
                tx.mfa.save_factor(active, old_version)
                tx.mfa.revoke_recovery_codes(active.id, scope)
            tx.mfa.save_factor(factor, previous_version)
            codes = self._mfa.issue_recovery_codes(10)
            tx.mfa.save_recovery_codes(
                factor.id,
                tuple(
                    RecoveryCode(uuid4(), factor.id, self._mfa.hash_recovery_code(code))
                    for code in codes
                ),
                scope,
            )
            challenge.consume(VerifiedSecondFactor(account.id, factor.id, browser, "setup"), now)
            tx.mfa.save_challenge(challenge)
            version = account.version
            account.mfa_enabled = True
            if account.status != AccountStatus.ACTIVE:
                account.activate(now)
            else:
                account.version += 1
            tx.users.save(account, version)
            tx.sessions.revoke_all(account.id)
            tx.invalidate_tokens(account.id)
            view, cookie = self._new_session(tx, account, principal, True)
            result = MfaActivationView(view, codes)
            tx.commit("authentication.mfa_activated", account.id)
        self._cookie(cookie)
        return result

    def verify_mfa(self, principal: RequestContext, request: Mapping[str, str]) -> SessionView:
        browser = self._start(principal, "verify_mfa", principal.browser_token)
        now = self._clock.now()
        with self._transactions() as tx:
            account, challenge = self._challenge(
                tx, request["challenge_token"], browser, "challenge"
            )
            now = self._clock.now()
            factor = tx.mfa.get_factor_for_update(account.id, SelfAuthScope(account.id))
            if factor is None or factor.id != challenge.factor_id:
                raise AuthError("MFA_REPLAY")
            code = request["code"]
            try:
                if len(code) == 6 and code.isascii() and code.isdigit():
                    step = self._mfa.verify_totp(factor.secret_reference, code, now)
                    version = factor.version
                    factor.accept_step(step)
                    tx.mfa.save_factor(factor, version)
                else:
                    digest = self._mfa.hash_recovery_code(code)
                    recovery = tx.mfa.find_recovery_for_update(factor.id, digest)
                    if recovery is None:
                        raise AuthError("INVALID_CREDENTIALS")
                    recovery.consume(VerifiedRecoveryProof(factor.id, digest), now)
                    tx.mfa.consume_recovery(recovery)
            except AuthError as exc:
                if exc.code in {"INVALID_CREDENTIALS", "MFA_REPLAY"}:
                    self._reject(tx, challenge)
                raise
            challenge.consume(
                VerifiedSecondFactor(account.id, factor.id, browser, "challenge"), now
            )
            tx.mfa.save_challenge(challenge)
            view, cookie = self._new_session(tx, account, principal, True)
            tx.commit("authentication.mfa_verified", account.id)
        self._cookie(cookie)
        return view

    def _email(self, principal: RequestContext, request: Mapping[str, str], purpose: str) -> None:
        email = request["email"].casefold().strip()
        self._start(principal, purpose, email)
        with self._transactions() as tx:
            found = tx.users.find_login(email)
            if found:
                account = found.account
                eligible = (
                    account.role.role != Role.STUDENT
                    and account.email == email
                    and account.status
                    == (AccountStatus.ACTIVE if purpose == "reset" else AccountStatus.PENDING)
                    and (purpose == "reset" or not account.staff)
                )
                if eligible:
                    ttl = timedelta(minutes=30) if purpose == "reset" else timedelta(hours=24)
                    token = self._tokens.issue(purpose, account.id, ttl)
                    tx.store_token(token)
                    tx.notify(account, token)
                    tx.commit("authentication.email_requested", account.id)

    def request_password_reset(self, principal: RequestContext, request: Mapping[str, str]) -> None:
        self._email(principal, request, "reset")

    def resend_verification(self, principal: RequestContext, request: Mapping[str, str]) -> None:
        self._email(principal, request, "verification")

    def verify_email(self, principal: RequestContext, request: Mapping[str, str]) -> None:
        self._start(principal, "verify_email", principal.browser_token)
        with self._transactions() as tx:
            subject = tx.sessions.consume_token(
                self._tokens.digest(request["token"]), "verification", self._clock.now()
            )
            account = tx.users.get_scoped(subject, SelfAuthScope(subject))
            if account is None or account.role.role != Role.PARENT:
                raise AuthError("INVALID_STATE")
            version = account.version
            account.activate(self._clock.now())
            tx.users.save(account, version)
            tx.commit("authentication.email_verified", subject)

    def reset_password(self, principal: RequestContext, request: Mapping[str, str]) -> None:
        self._start(principal, "reset_password", principal.browser_token)
        password_hash = self._passwords.hash(request["new_password"])
        with self._transactions() as tx:
            subject = tx.sessions.consume_token(
                self._tokens.digest(request["token"]), "reset", self._clock.now()
            )
            scope = SelfAuthScope(subject)
            account = tx.users.get_scoped(subject, scope)
            if (
                account is None
                or account.role.role == Role.STUDENT
                or account.status != AccountStatus.ACTIVE
            ):
                raise AuthError("INVALID_STATE")
            credential = tx.credential(subject, scope)
            credential.replace(password_hash, self._clock.now())
            tx.save_credential(credential)
            tx.sessions.revoke_all(subject)
            tx.invalidate_tokens(subject)
            tx.commit("authentication.password_reset", subject)
        self._cookie(None)

    def accept_staff_invitation(
        self, principal: RequestContext, request: Mapping[str, str]
    ) -> StaffSetupSessionView:
        browser = self._start(principal, "accept_invitation", principal.browser_token)
        password_hash = self._passwords.hash(request["password"])
        with self._transactions() as tx:
            subject = tx.sessions.consume_token(
                self._tokens.digest(request["token"]), "invitation", self._clock.now()
            )
            account = tx.users.get_scoped(subject, SelfAuthScope(subject))
            if account is None or not account.staff or account.status != AccountStatus.INVITED:
                raise AuthError("INVALID_STATE")
            if not self._staff_approved(subject):
                raise AuthError("FORBIDDEN")
            version = account.version
            account.status = AccountStatus.PENDING
            account.version += 1
            tx.users.save(account, version)
            tx.save_credential(Credential(subject, password_hash, self._clock.now()))
            tx.sessions.revoke_all(subject)
            challenge, token = self._limited(tx, account, browser, "setup")
            result = StaffSetupSessionView(
                AccountView.from_account(account), token, challenge.expires_at
            )
            tx.commit("authentication.invitation_accepted", subject)
        self._cookie(None)
        return result
