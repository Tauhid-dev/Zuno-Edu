"""Protected recovery intent; delivery workers receive only a durable token reference."""

import json
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Session

from zuno_edu.infrastructure.persistence.repository import IntegrationRepository
from zuno_edu.infrastructure.persistence.tables import one_time_tokens
from zuno_edu.modules.identity.application.ports import IssuedToken
from zuno_edu.modules.identity.domain import Account, AuthError
from zuno_edu.modules.operations.domain.delivery import OutboxEvent
from zuno_edu.shared.persistence import Clock

from .crypto import VersionedSecrets


class IdentityNotificationWriter:
    def __init__(self, secrets: VersionedSecrets, clock: Clock) -> None:
        self._secrets = secrets
        self._clock = clock

    def __call__(self, session: Session, account: Account, token: IssuedToken) -> None:
        if token.purpose not in {"verification", "reset"} or not account.email:
            raise AuthError("INVALID_STATE")
        reference = session.execute(
            sa.select(one_time_tokens.c.id)
            .where(
                one_time_tokens.c.account_id == account.id,
                one_time_tokens.c.token_hash == token.token_hash,
                one_time_tokens.c.purpose == token.purpose,
            )
            .with_for_update()
        ).scalar_one()
        # The pre-approved protected token payload is separate from the UUID-only outbox.
        payload = json.dumps(
            {
                "recipient": account.email,
                "token": token.value,
                "purpose": token.purpose,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        session.execute(
            one_time_tokens.update()
            .where(one_time_tokens.c.id == reference)
            .values(
                payload_ciphertext=self._secrets.seal(
                    payload, b"identity-notification-v1:" + reference.bytes
                )
            )
        )
        IntegrationRepository(session).append_event(
            OutboxEvent(
                uuid4(),
                "identity_token",
                reference,
                1,
                "identity.email_requested",
                self._clock.now(),
                (("token_id", reference),),
            )
        )
