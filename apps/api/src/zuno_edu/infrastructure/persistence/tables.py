"""Explicit relational mapping. Alembic alone creates or changes these tables."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

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
