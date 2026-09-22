"""Encrypted, authenticated cursors bound to the authorized principal/scope/query."""

import base64
import hashlib
import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from zuno_edu.shared.persistence import Clock

from .errors import ApiError

type QueryValue = str | int | bool | None


@dataclass(frozen=True)
class CursorContext:
    principal_id: UUID
    operation: str
    scope: Mapping[str, QueryValue]
    query: Mapping[str, QueryValue]

    def binding(self) -> bytes:
        if not self.operation or not self.scope:
            raise ValueError("Explicit operation and authorized scope required")
        raw = json.dumps(
            [str(self.principal_id), self.operation, dict(self.scope), dict(self.query)],
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
        return b"zuno:cursor:v1:" + hashlib.sha256(raw).digest()


class CursorCodec:
    def __init__(
        self, key: bytes, clock: Clock, lifetime: timedelta = timedelta(minutes=15)
    ) -> None:
        if len(key) != 32 or not timedelta(0) < lifetime <= timedelta(hours=1):
            raise ValueError("Explicit 256-bit key and bounded cursor lifetime required")
        self._cipher, self._clock, self._lifetime = AESGCM(key), clock, lifetime

    def encode(self, context: CursorContext, position: tuple[str, ...]) -> str:
        if not 1 <= len(position) <= 4 or any(not value or len(value) > 200 for value in position):
            raise ValueError("Bounded stable ordering position required")
        expiry = int((self._clock.now() + self._lifetime).timestamp())
        raw = json.dumps(
            {"v": 1, "position": position, "expires": expiry}, separators=(",", ":")
        ).encode()
        nonce = os.urandom(12)
        encrypted = nonce + self._cipher.encrypt(nonce, raw, context.binding())
        return base64.urlsafe_b64encode(encrypted).decode().rstrip("=")

    def decode(self, token: str, context: CursorContext) -> tuple[str, ...]:
        try:
            if not 1 <= len(token) <= 4096 or not token.isascii():
                raise ValueError("Malformed cursor")
            raw = base64.b64decode(token + "=" * (-len(token) % 4), altchars=b"-_", validate=True)
            if len(raw) < 29 or base64.urlsafe_b64encode(raw).decode().rstrip("=") != token:
                raise ValueError("Noncanonical cursor")
            payload = json.loads(self._cipher.decrypt(raw[:12], raw[12:], context.binding()))
            if (
                set(payload) != {"v", "position", "expires"}
                or payload["v"] != 1
                or type(payload["expires"]) is not int
                or payload["expires"] <= self._clock.now().timestamp()
            ):
                raise ValueError("Expired cursor")
            position = payload["position"]
            if (
                not isinstance(position, list)
                or not 1 <= len(position) <= 4
                or any(
                    not isinstance(value, str) or not 1 <= len(value) <= 200 for value in position
                )
            ):
                raise ValueError("Invalid position")
            return tuple(position)
        except ValueError, TypeError, KeyError, InvalidTag, UnicodeDecodeError:
            raise ApiError("VALIDATION_ERROR") from None
