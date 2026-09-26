"""Explicit relational mapping. Alembic alone creates or changes these tables."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import CITEXT, JSONB, UUID

metadata = sa.MetaData(
    naming_convention={
        "pk": "pk_%(table_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
    }
)


def created() -> sa.Column[datetime]:
    return sa.Column(
        "created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )


outbox = sa.Table(
    "outbox_events",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("aggregate_type", sa.Text, nullable=False),
    sa.Column("aggregate_id", UUID(as_uuid=True), nullable=False),
    sa.Column("aggregate_version", sa.BigInteger, nullable=False),
    sa.Column("event_type", sa.Text, nullable=False),
    sa.Column("payload", JSONB, nullable=False),
    sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("published_at", sa.DateTime(timezone=True)),
    sa.Column("lease_until", sa.DateTime(timezone=True)),
    sa.Column("lease_token", UUID(as_uuid=True)),
    created(),
    sa.UniqueConstraint(
        "aggregate_type",
        "aggregate_id",
        "aggregate_version",
        "event_type",
        name="uq_outbox_aggregate_event",
    ),
    sa.CheckConstraint("aggregate_version > 0", name="positive_version"),
    sa.CheckConstraint("jsonb_typeof(payload) = 'object'", name="object_payload"),
    sa.CheckConstraint("(lease_until IS NULL) = (lease_token IS NULL)", name="lease_pair"),
)
sa.Index("ix_outbox_pending", outbox.c.published_at, outbox.c.occurred_at)

accounts = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("role", sa.Text, nullable=False),
    sa.Column("email", CITEXT),
    sa.Column("display_name", sa.String(200), nullable=False),
    sa.Column("status", sa.Text, nullable=False),
    sa.Column("admin_privileges", sa.ARRAY(sa.Text), nullable=False, server_default="{}"),
    sa.Column("mfa_enabled", sa.Boolean, nullable=False, server_default=sa.false()),
    sa.Column("version", sa.BigInteger, nullable=False, server_default="1"),
    sa.UniqueConstraint("email", name="uq_accounts_email"),
    sa.CheckConstraint("version > 0", name="positive_version"),
    sa.CheckConstraint("role IN ('parent','student','teacher','admin')", name="role"),
    sa.CheckConstraint(
        "status IN ('invited','pending_verification','active','suspended','closed')", name="status"
    ),
    sa.CheckConstraint(
        "(role = 'admin') = (cardinality(admin_privileges) > 0) AND "
        "admin_privileges <@ ARRAY['identity_admin','education_admin','finance_admin',"
        "'operations_admin','audit_admin']::text[]",
        name="privileges",
    ),
    sa.CheckConstraint("role = 'student' OR email IS NOT NULL", name="adult_email"),
)
credentials = sa.Table(
    "credentials",
    metadata,
    sa.Column("account_id", UUID(as_uuid=True), sa.ForeignKey("accounts.id"), primary_key=True),
    sa.Column("password_hash", sa.Text, nullable=False),
    sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("failed_attempts", sa.Integer, nullable=False, server_default="0"),
    sa.Column("locked_until", sa.DateTime(timezone=True)),
    sa.CheckConstraint("failed_attempts >= 0", name="nonnegative_failures"),
)
sessions = sa.Table(
    "sessions",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("account_id", UUID(as_uuid=True), sa.ForeignKey("accounts.id"), nullable=False),
    sa.Column("token_hash", sa.LargeBinary, nullable=False, unique=True),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("revoked_at", sa.DateTime(timezone=True)),
    sa.Column("mfa_verified_at", sa.DateTime(timezone=True)),
    sa.Column("device_label", sa.String(200), nullable=False, server_default=""),
    sa.CheckConstraint("expires_at > created_at", name="expiry_order"),
)
one_time_tokens = sa.Table(
    "one_time_tokens",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("account_id", UUID(as_uuid=True), sa.ForeignKey("accounts.id"), nullable=False),
    sa.Column("purpose", sa.Text, nullable=False),
    sa.Column("token_hash", sa.LargeBinary, nullable=False, unique=True),
    sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("consumed_at", sa.DateTime(timezone=True)),
    sa.Column("payload_ciphertext", sa.LargeBinary),
    sa.CheckConstraint(
        "purpose IN ('verification','reset','invitation','challenge','setup')", name="purpose"
    ),
)
mfa_factors = sa.Table(
    "mfa_factors",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("account_id", UUID(as_uuid=True), sa.ForeignKey("accounts.id"), nullable=False),
    sa.Column("secret_ciphertext", sa.LargeBinary, nullable=False),
    sa.Column("encryption_key_version", sa.Text, nullable=False),
    sa.Column("status", sa.Text, nullable=False),
    sa.Column("last_accepted_step", sa.BigInteger),
    sa.Column("activated_at", sa.DateTime(timezone=True)),
    sa.Column("revoked_at", sa.DateTime(timezone=True)),
    sa.Column("version", sa.BigInteger, nullable=False, server_default="1"),
    sa.CheckConstraint("status IN ('pending','active','revoked')", name="status"),
    sa.CheckConstraint("version > 0", name="positive_version"),
)
idempotency_records = sa.Table(
    "idempotency_records",
    metadata,
    sa.Column("principal_scope", sa.Text, primary_key=True),
    sa.Column("operation_id", sa.Text, primary_key=True),
    sa.Column("key", UUID(as_uuid=True), primary_key=True),
    sa.Column("request_hash", sa.LargeBinary, nullable=False),
    sa.Column("result_ciphertext", sa.LargeBinary),
    sa.Column("status", sa.Text, nullable=False),
    sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint(
        "operation_id <> 'API-AUTH-MFA-ENROL' OR result_ciphertext IS NULL",
        name="mfa_no_secret_result",
    ),
)
mfa_challenges = sa.Table(
    "mfa_challenges",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("account_id", UUID(as_uuid=True), sa.ForeignKey("accounts.id"), nullable=False),
    sa.Column("token_hash", sa.LargeBinary, nullable=False, unique=True),
    sa.Column("purpose", sa.Text, nullable=False),
    sa.Column("browser_binding_hash", sa.LargeBinary, nullable=False),
    sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("attempts", sa.Integer, nullable=False, server_default="0"),
    sa.Column("consumed_at", sa.DateTime(timezone=True)),
    sa.Column("factor_id", UUID(as_uuid=True), sa.ForeignKey("mfa_factors.id")),
    sa.CheckConstraint("attempts BETWEEN 0 AND 5", name="bounded_attempts"),
    sa.CheckConstraint("purpose IN ('challenge','setup')", name="purpose"),
)
mfa_recovery_codes = sa.Table(
    "mfa_recovery_codes",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("factor_id", UUID(as_uuid=True), sa.ForeignKey("mfa_factors.id"), nullable=False),
    sa.Column("code_hash", sa.LargeBinary, nullable=False, unique=True),
    sa.Column("consumed_at", sa.DateTime(timezone=True)),
)
for identity_table in (
    accounts,
    credentials,
    sessions,
    one_time_tokens,
    mfa_factors,
    mfa_challenges,
    mfa_recovery_codes,
):
    if "created_at" not in identity_table.c:
        identity_table.append_column(created())
    identity_table.append_column(
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        )
    )
sa.Index("ix_mfa_factors_account_status", mfa_factors.c.account_id, mfa_factors.c.status)
sa.Index(
    "uq_mfa_factors_active_account",
    mfa_factors.c.account_id,
    unique=True,
    postgresql_where=mfa_factors.c.status == "active",
)
sa.Index("ix_mfa_challenges_account_purpose", mfa_challenges.c.account_id, mfa_challenges.c.purpose)
sa.Index("ix_one_time_tokens_expiry", one_time_tokens.c.expires_at)
sa.Index("ix_idempotency_records_expiry", idempotency_records.c.expires_at)
sa.Index("ix_accounts_status", accounts.c.status, accounts.c.id)
sa.Index("ix_sessions_account_revoked", sessions.c.account_id, sessions.c.revoked_at)
sa.Index("ix_sessions_expiry", sessions.c.expires_at)
sa.Index(
    "ix_one_time_tokens_account_purpose", one_time_tokens.c.account_id, one_time_tokens.c.purpose
)
sa.Index("ix_mfa_challenges_expiry", mfa_challenges.c.expires_at)
sa.Index("ix_mfa_challenges_factor", mfa_challenges.c.factor_id)
sa.Index(
    "ix_mfa_recovery_codes_factor_consumed",
    mfa_recovery_codes.c.factor_id,
    mfa_recovery_codes.c.consumed_at,
)
sa.Index("ix_outbox_lease", outbox.c.lease_until)

jobs = sa.Table(
    "background_jobs",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("kind", sa.Text, nullable=False),
    sa.Column(
        "source_event_id",
        UUID(as_uuid=True),
        sa.ForeignKey("outbox_events.id", ondelete="RESTRICT"),
    ),
    sa.Column("dedupe_key", sa.Text, nullable=False),
    sa.Column("payload", JSONB, nullable=False),
    sa.Column("status", sa.Text, nullable=False),
    sa.Column("attempt_count", sa.Integer, nullable=False, server_default="0"),
    sa.Column("lease_until", sa.DateTime(timezone=True)),
    sa.Column("lease_token", UUID(as_uuid=True)),
    sa.Column("next_attempt_at", sa.DateTime(timezone=True)),
    sa.Column("last_error_code", sa.Text),
    sa.Column("version", sa.BigInteger, nullable=False, server_default="1"),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    created(),
    sa.UniqueConstraint("kind", "dedupe_key", name="uq_job_kind_dedupe"),
    sa.CheckConstraint(
        "status IN ('queued','running','succeeded','failed','dead_letter')", name="status"
    ),
    sa.CheckConstraint("attempt_count BETWEEN 0 AND 8", name="bounded_attempts"),
    sa.CheckConstraint("version > 0", name="positive_version"),
    sa.CheckConstraint(
        "(status = 'running') = (lease_until IS NOT NULL AND lease_token IS NOT NULL)",
        name="running_lease",
    ),
    sa.CheckConstraint("(lease_until IS NULL) = (lease_token IS NULL)", name="lease_pair"),
    sa.CheckConstraint(
        "last_error_code IS NULL OR last_error_code IN "
        "('PROVIDER_UNAVAILABLE','CONFIGURATION_ERROR','UNKNOWN_OUTCOME','RETRY_EXHAUSTED')",
        name="safe_error",
    ),
)
sa.Index("ix_jobs_ready", jobs.c.status, jobs.c.next_attempt_at)
sa.Index("ix_jobs_lease", jobs.c.lease_until)
sa.Index("ix_jobs_source", jobs.c.source_event_id)

inbox = sa.Table(
    "webhook_inbox",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True),
    sa.Column("provider", sa.Text, nullable=False),
    sa.Column("provider_event_id", sa.Text, nullable=False),
    sa.Column("verified", sa.Boolean, nullable=False),
    sa.Column("payload_ciphertext", sa.LargeBinary, nullable=False),
    sa.Column("status", sa.Text, nullable=False),
    sa.Column("lease_until", sa.DateTime(timezone=True)),
    sa.Column("lease_token", UUID(as_uuid=True)),
    sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
    sa.Column("processed_at", sa.DateTime(timezone=True)),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    created(),
    sa.UniqueConstraint("provider", "provider_event_id", name="uq_inbox_provider_event"),
    sa.CheckConstraint("status IN ('pending','processing','processed','ignored')", name="status"),
    sa.CheckConstraint("status = 'pending' OR verified", name="verified_processing"),
    sa.CheckConstraint(
        "octet_length(payload_ciphertext) BETWEEN 1 AND 262144", name="bounded_payload"
    ),
    sa.CheckConstraint("(lease_until IS NULL) = (lease_token IS NULL)", name="lease_pair"),
)
sa.Index("ix_inbox_pending", inbox.c.status, inbox.c.received_at)
sa.Index("ix_inbox_lease", inbox.c.lease_until)
