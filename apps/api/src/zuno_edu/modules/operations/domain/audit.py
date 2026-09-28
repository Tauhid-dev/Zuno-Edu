"""Append-only audit facts with an explicit, non-PII vocabulary."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from zuno_edu.domain.policies import AdminCapabilityScope
from zuno_edu.shared.persistence import require_instant

type AuditOutcome = Literal["allowed", "denied", "failed"]
# Owning chunks add reviewed event codes, never arbitrary request/provider text.
AUDIT_ACTIONS = frozenset(
    {
        "audit.accessed",
        "audit.denied",
        "authorization.grant_denied",
        "authentication.login",
        "authentication.login_denied",
        "authentication.session_accessed",
        "authentication.logout",
        "authentication.mfa_verified",
        "authentication.mfa_enrolled",
        "authentication.mfa_activated",
        "authentication.mfa_denied",
        "authentication.email_requested",
        "authentication.email_verified",
        "authentication.password_reset",
        "authentication.invitation_accepted",
        "authentication.enrolment_denied",
    }
)
AUDIT_REASONS = frozenset({"FORBIDDEN", "UNAUTHENTICATED", "INCOMPATIBLE_ROLE"})


@dataclass(frozen=True)
class AuditRecord:
    id: UUID
    actor_id: UUID | None
    action: str
    resource_type: str
    resource_id: UUID | None
    occurred_at: datetime
    request_id: UUID
    outcome: AuditOutcome
    reason: str | None = None

    def __post_init__(self) -> None:
        require_instant(self.occurred_at)
        if (
            self.action not in AUDIT_ACTIONS
            or self.resource_type not in {"account", "audit"}
            or self.outcome not in {"allowed", "denied", "failed"}
            or (self.reason is not None and self.reason not in AUDIT_REASONS)
        ):
            raise ValueError("Unreviewed audit vocabulary; no raw text or metadata allowed")

    def redacted_view(self, scope: AdminCapabilityScope, now: datetime) -> AuditRecord:
        scope.require("audit_admin", now)
        # The entire immutable record is a whitelisted safe projection: no secret payload.
        return self
