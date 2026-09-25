import hashlib
import hmac
import os
from uuid import uuid4

import pytest
from redis import Redis
from redis.exceptions import ConnectionError
from zuno_edu.modules.identity.domain import AuthError
from zuno_edu.modules.identity.infrastructure.security import RedisAbuseControls


def test_shared_abuse_limit_and_outage_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    url = os.environ.get("ZUNO_TEST_REDIS_URL")
    assert url == "redis://127.0.0.1:16379/15", "isolated Redis database 15 required"
    redis = Redis.from_url(url, socket_timeout=2)
    identity, network = uuid4().hex, uuid4().hex
    key = uuid4().bytes + uuid4().bytes
    limiter = RedisAbuseControls(redis, key)
    keys = [
        f"zuno:auth:login:{kind}:" + hmac.new(key, value.encode(), hashlib.sha256).hexdigest()
        for kind, value in (("identity", identity), ("network", network))
    ]
    try:
        for _ in range(5):
            limiter.check("login", identity, network)
        with pytest.raises(AuthError, match="RATE_LIMITED"):
            limiter.check("login", identity, network)
        assert redis.get(keys[0]) == b"6"
        assert 0 < redis.ttl(keys[0]) <= 60

        def unavailable(*args: object, **kwargs: object) -> None:
            raise ConnectionError("synthetic outage")

        monkeypatch.setattr(redis, "eval", unavailable)
        with pytest.raises(AuthError, match="RATE_LIMITED"):
            limiter.check("login", uuid4().hex, network)
    finally:
        redis.delete(*keys)
        redis.close()
