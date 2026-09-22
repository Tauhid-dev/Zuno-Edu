import os
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from zuno_edu.presentation.http.errors import ApiError
from zuno_edu.presentation.http.pagination import CursorCodec, CursorContext
from zuno_edu.shared.persistence import FrozenClock


def test_opaque_cursor_is_bound_to_actor_scope_operation_query_and_expiry() -> None:
    clock = FrozenClock(datetime(2026, 9, 22, tzinfo=UTC))
    codec = CursorCodec(os.urandom(32), clock)
    context = CursorContext(
        uuid4(), "API-TEST-LIST", {"family": str(uuid4())}, {"sort": "created,id", "limit": 25}
    )
    position = ("2026-09-21T00:00:00Z", str(uuid4()))
    token = codec.encode(context, position)
    assert position[0] not in token and str(context.principal_id) not in token
    assert codec.decode(token, context) == position
    assert codec.encode(context, position) != token
    for other in (
        replace(context, principal_id=uuid4()),
        replace(context, scope={"family": str(uuid4())}),
        replace(context, operation="OTHER"),
        replace(context, query={"sort": "id"}),
    ):
        with pytest.raises(ApiError, match="VALIDATION_ERROR"):
            codec.decode(token, other)
    for invalid in ("", token[:-8] + "abcdefgh", token + "=", "!" * 50, "x" * 4097):
        with pytest.raises(ApiError):
            codec.decode(invalid, context)
    with pytest.raises(ApiError):
        CursorCodec(os.urandom(32), clock).decode(token, context)
    clock.instant += timedelta(minutes=15)
    with pytest.raises(ApiError):
        codec.decode(token, context)


def test_cursor_configuration_requires_secret_and_scope() -> None:
    clock = FrozenClock(datetime(2026, 9, 22, tzinfo=UTC))
    with pytest.raises(ValueError):
        CursorCodec(b"short", clock)
    codec = CursorCodec(os.urandom(32), clock)
    with pytest.raises(ValueError):
        codec.encode(CursorContext(uuid4(), "test", {}, {}), ("position",))
