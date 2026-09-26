"""CSPRNG, Argon2id and audited-library TOTP adapters; keys are injected."""

import base64
import hashlib
import hmac
import json
import secrets
from collections.abc import Callable, Mapping
from datetime import datetime, timedelta
from uuid import UUID

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.twofactor.totp import TOTP

from zuno_edu.modules.identity.application.ports import EncryptedMfaSetup, IssuedToken
from zuno_edu.modules.identity.domain import AuthError
from zuno_edu.shared.persistence import Clock, require_instant


class TokenIssuer:
    def __init__(self, clock: Clock) -> None:
        self.clock = clock

    def issue(self, purpose: str, subject: UUID, ttl: timedelta) -> IssuedToken:
        if purpose not in {"session", "verification", "reset", "invitation", "challenge", "setup"}:
            raise AuthError("INVALID_STATE")
        if ttl <= timedelta(0):
            raise AuthError("INVALID_STATE")
        value = secrets.token_urlsafe(32)
        return IssuedToken(value, self.digest(value), subject, purpose, self.clock.now() + ttl)

    def digest(self, token: str) -> bytes:
        if not token or len(token) > 512:
            raise AuthError("UNAUTHENTICATED")
        return hashlib.sha256(token.encode("utf-8")).digest()

    def verify_digest(self, token: str, token_hash: bytes) -> bool:
        return hmac.compare_digest(self.digest(token), token_hash)


class PasswordHasher:
    """Offline breached-password screening is injected and must fail closed."""

    def __init__(self, breached: Callable[[str], bool]) -> None:
        self._breached = breached

    def hash(self, password: str) -> str:
        if not 12 <= len(password) <= 128 or self._breached(password):
            raise AuthError("VALIDATION_ERROR")
        return Argon2id(
            salt=secrets.token_bytes(16), length=32, iterations=3, lanes=1, memory_cost=65536
        ).derive_phc_encoded(password.encode("utf-8"))

    def verify(self, password: str, password_hash: str) -> bool:
        if not 12 <= len(password) <= 128 or not password_hash.startswith("$argon2id$"):
            return False
        try:
            Argon2id.verify_phc_encoded(password.encode("utf-8"), password_hash)
        except InvalidKey, ValueError:
            return False
        return True

    def needs_rehash(self, password_hash: str) -> bool:
        fields = password_hash.split("$")
        return len(fields) != 6 or fields[1:4] != ["argon2id", "v=19", "m=65536,t=3,p=1"]


class VersionedSecrets:
    """Managed-key bytes supplied by deployment, never stored in PostgreSQL."""

    def __init__(self, keys: Mapping[str, bytes], active: str) -> None:
        if active not in keys or any(
            not version.isascii() or not version.isalnum() or len(key) != 32
            for version, key in keys.items()
        ):
            raise ValueError("Invalid managed key configuration")
        self._keys = dict(keys)
        self.active = active

    def _key(self, version: str) -> bytes:
        try:
            return self._keys[version]
        except KeyError:
            raise AuthError("INVALID_STATE") from None

    def seal(self, plaintext: bytes, purpose: bytes) -> bytes:
        nonce = secrets.token_bytes(12)
        ciphertext = AESGCM(self._key(self.active)).encrypt(nonce, plaintext, purpose)
        return self.active.encode("ascii") + b":" + nonce + ciphertext

    def open(self, ciphertext: bytes, purpose: bytes) -> bytes:
        from cryptography.exceptions import InvalidTag

        try:
            version, payload = ciphertext.split(b":", 1)
            return AESGCM(self._key(version.decode("ascii"))).decrypt(
                payload[:12], payload[12:], purpose
            )
        except ValueError, UnicodeError, InvalidTag:
            raise AuthError("INVALID_STATE") from None

    def request_digest(self, body: Mapping[str, str], version: str | None = None) -> bytes:
        version = self.active if version is None else version
        encoded = json.dumps(dict(body), sort_keys=True, separators=(",", ":")).encode("utf-8")
        digest = hmac.digest(self._key(version), b"mfa-enrol-body-v1\x00" + encoded, "sha256")
        return b"v1:" + version.encode("ascii") + b":" + digest

    def matches_request(self, recorded: bytes, body: Mapping[str, str]) -> bool:
        try:
            format_version, key_version, digest = recorded.split(b":", 2)
            if format_version != b"v1" or len(digest) != 32:
                raise ValueError
            expected = self.request_digest(body, key_version.decode("ascii"))
        except ValueError, UnicodeError:
            raise AuthError("INVALID_STATE") from None
        return hmac.compare_digest(expected, recorded)


class MfaVerifier:
    def __init__(self, secrets_store: VersionedSecrets) -> None:
        self._secrets = secrets_store

    def generate_setup(self, account_label: str) -> EncryptedMfaSetup:
        seed = secrets.token_bytes(20)
        totp = TOTP(seed, 6, hashes.SHA1(), 30)
        return EncryptedMfaSetup(
            self._secrets.seal(seed, b"identity-totp-v1"),
            self._secrets.active,
            totp.get_provisioning_uri(account_label, "Zuno Edu"),
        )

    def verify_totp(self, secret_reference: bytes, code: str, now: datetime) -> int:
        if len(code) != 6 or not code.isascii() or not code.isdigit():
            raise AuthError("INVALID_CREDENTIALS")
        seed = self._secrets.open(secret_reference, b"identity-totp-v1")
        totp = TOTP(seed, 6, hashes.SHA1(), 30)
        step = int(require_instant(now).timestamp()) // 30
        # Check newest first so an unlikely repeated adjacent code cannot lower the counter.
        for candidate in (step + 1, step, step - 1):
            if candidate >= 0 and hmac.compare_digest(totp.generate(candidate * 30), code.encode()):
                return candidate
        raise AuthError("INVALID_CREDENTIALS")

    def issue_recovery_codes(self, count: int) -> tuple[str, ...]:
        if count != 10:
            raise AuthError("INVALID_STATE")
        return tuple(
            base64.b32encode(secrets.token_bytes(16)).decode().rstrip("=") for _ in range(count)
        )

    def hash_recovery_code(self, code: str) -> bytes:
        if len(code) != 26 or not code.isascii():
            raise AuthError("INVALID_CREDENTIALS")
        return hashlib.sha256(b"mfa-recovery-v1\x00" + code.encode("ascii")).digest()
