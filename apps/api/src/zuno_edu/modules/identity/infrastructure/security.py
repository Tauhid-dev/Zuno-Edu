"""Signed browser binding, CSRF and shared Redis abuse controls."""

import hashlib
import hmac
import secrets
from urllib.parse import urlsplit

from redis import Redis
from redis.exceptions import RedisError

from zuno_edu.modules.identity.application.contracts import RequestContext
from zuno_edu.modules.identity.domain import AuthError


class RequestSecurity:
    def __init__(self, key: bytes, origin: str) -> None:
        parsed = urlsplit(origin)
        if (
            len(key) < 32
            or parsed.scheme != "https"
            or parsed.path
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("HTTPS origin and a strong signing key are required")
        self._key = key
        self._origin = origin

    def browser(self) -> str:
        nonce = secrets.token_urlsafe(32)
        signature = hmac.new(self._key, b"browser:" + nonce.encode(), hashlib.sha256).hexdigest()
        return nonce + "." + signature

    def csrf(self, browser_token: str) -> str:
        return hmac.new(self._key, b"csrf:" + browser_token.encode(), hashlib.sha256).hexdigest()

    def validate(self, context: RequestContext, *, mutation: bool) -> bytes:
        try:
            nonce, signature = context.browser_token.split(".")
        except ValueError:
            raise AuthError("UNAUTHENTICATED") from None
        expected = hmac.new(self._key, b"browser:" + nonce.encode(), hashlib.sha256).hexdigest()
        if len(nonce) != 43 or not hmac.compare_digest(signature, expected):
            raise AuthError("UNAUTHENTICATED")
        if mutation and (
            context.origin != self._origin
            or not hmac.compare_digest(context.csrf_token, self.csrf(context.browser_token))
        ):
            raise AuthError("FORBIDDEN")
        return hashlib.sha256(context.browser_token.encode()).digest()


class RedisAbuseControls:
    # INCR plus EXPIRE in one atomic operation; no permanent counter on partial failure.
    _SCRIPT = """
local count = redis.call('INCR', KEYS[1])
if count == 1 then redis.call('EXPIRE', KEYS[1], ARGV[1]) end
return count
"""

    def __init__(self, redis: Redis, key: bytes) -> None:
        if len(key) < 32:
            raise ValueError("Abuse-control identifier key is required")
        self._redis = redis
        self._key = key

    def check(self, operation: str, identity: str, network: str) -> None:
        limit, seconds = (3, 3600) if operation in {"reset", "verification"} else (5, 60)
        try:
            for kind, value, maximum in (("identity", identity, limit), ("network", network, 100)):
                digest = hmac.new(self._key, value.encode(), hashlib.sha256).hexdigest()
                key = f"zuno:auth:{operation}:{kind}:{digest}"
                count = int(self._redis.eval(self._SCRIPT, 1, key, seconds))
                if count > maximum:
                    raise AuthError("RATE_LIMITED")
        except RedisError:
            raise AuthError("RATE_LIMITED") from None
