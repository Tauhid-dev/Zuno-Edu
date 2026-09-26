import base64
from datetime import UTC, datetime, timedelta
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from zuno_edu.modules.identity.domain import AuthError
from zuno_edu.modules.identity.infrastructure.crypto import (
    MfaVerifier,
    PasswordHasher,
    TokenIssuer,
    VersionedSecrets,
)
from zuno_edu.shared.persistence import FrozenClock

NOW = datetime(2026, 9, 25, tzinfo=UTC)


def test_password_hashes_salted_and_screened() -> None:
    hasher = PasswordHasher(lambda value: value == "known-breached-password")
    password = "Synthetic test passphrase 123!"
    first, second = hasher.hash(password), hasher.hash(password)
    assert first != second
    assert first.startswith("$argon2id$v=19$m=65536,t=3,p=1$")
    assert hasher.verify(password, first)
    assert not hasher.verify("Wrong synthetic passphrase", first)
    assert not hasher.needs_rehash(first)
    for rejected in ("short", "x" * 129, "known-breached-password"):
        with pytest.raises(AuthError):
            hasher.hash(rejected)


def test_tokens_use_entropy_and_hide_secrets_in_repr() -> None:
    issuer = TokenIssuer(FrozenClock(NOW))
    token = issuer.issue("reset", uuid4(), timedelta(minutes=30))
    assert len(base64.urlsafe_b64decode(token.value + "=")) == 32
    assert token.expires_at == NOW + timedelta(minutes=30)
    assert issuer.verify_digest(token.value, token.token_hash)
    assert not issuer.verify_digest("different", token.token_hash)
    assert token.value not in repr(token)


def test_totp_library_compatibility_tolerance_and_encryption() -> None:
    keys = VersionedSecrets({"k1": b"k" * 32}, "k1")
    verifier = MfaVerifier(keys)
    setup = verifier.generate_setup("synthetic@example.org")
    params = parse_qs(urlparse(setup.otpauth_uri).query)
    seed = base64.b32decode(params["secret"][0])
    assert len(seed) == 20
    assert seed not in setup.secret_reference
    assert setup.otpauth_uri not in repr(setup)
    totp = TOTP(seed, 6, hashes.SHA1(), 30)
    step = int(NOW.timestamp()) // 30
    for offset in (-1, 0, 1):
        code = totp.generate((step + offset) * 30).decode()
        assert verifier.verify_totp(setup.secret_reference, code, NOW) == step + offset
    with pytest.raises(AuthError):
        verifier.verify_totp(setup.secret_reference, totp.generate((step + 4) * 30).decode(), NOW)
    with pytest.raises(AuthError):
        MfaVerifier(VersionedSecrets({"k2": b"z" * 32}, "k2")).verify_totp(
            setup.secret_reference, "123456", NOW
        )


def test_keyed_idempotency_survives_rotation_and_fails_closed_without_key() -> None:
    body = {"password": "synthetic secret", "setup_token": "opaque", "Idempotency-Key": "uuid"}
    old = VersionedSecrets({"k1": b"a" * 32}, "k1")
    recorded = old.request_digest(body)
    rotated = VersionedSecrets({"k1": b"a" * 32, "k2": b"b" * 32}, "k2")
    assert rotated.matches_request(recorded, body)
    assert not rotated.matches_request(recorded, {**body, "password": "changed"})
    assert rotated.request_digest(body) != recorded
    with pytest.raises(AuthError):
        VersionedSecrets({"k2": b"b" * 32}, "k2").matches_request(recorded, body)
    with pytest.raises(AuthError):
        rotated.matches_request(b"malformed", body)


def test_recovery_codes_have_128_bits_and_only_hashes_are_persistable() -> None:
    verifier = MfaVerifier(VersionedSecrets({"k1": b"k" * 32}, "k1"))
    codes = verifier.issue_recovery_codes(10)
    assert len(set(codes)) == 10
    for code in codes:
        assert len(base64.b32decode(code + "======")) == 16
        assert len(verifier.hash_recovery_code(code)) == 32
