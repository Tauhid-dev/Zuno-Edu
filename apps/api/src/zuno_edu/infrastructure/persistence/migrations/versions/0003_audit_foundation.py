"""Append-only audit with separate non-login database privileges."""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_records",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("actor_id", sa.UUID(), sa.ForeignKey("accounts.id")),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("resource_type", sa.Text(), nullable=False),
        sa.Column("resource_id", sa.UUID()),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_id", sa.UUID(), nullable=False),
        sa.Column("outcome", sa.Text(), nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("metadata", postgresql.JSONB(), nullable=False, server_default="{}"),
        sa.CheckConstraint("outcome IN ('allowed','denied','failed')", name="ck_audit_outcome"),
        sa.CheckConstraint("metadata = '{}'::jsonb", name="ck_audit_metadata_redacted"),
    )
    for name, columns in (
        ("time", ["occurred_at", "id"]),
        ("actor_time", ["actor_id", "occurred_at"]),
        ("resource_time", ["resource_type", "resource_id", "occurred_at"]),
        ("request", ["request_id"]),
    ):
        op.create_index("ix_audit_" + name, "audit_records", columns)
    op.execute("""
        CREATE FUNCTION zuno_audit_immutable() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN RAISE EXCEPTION 'Audit records are append-only'; END $$;
        CREATE TRIGGER audit_immutable BEFORE UPDATE OR DELETE OR TRUNCATE ON audit_records
        FOR EACH STATEMENT EXECUTE FUNCTION zuno_audit_immutable();
        REVOKE ALL ON audit_records FROM PUBLIC;
        DO $$ BEGIN
          IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='zuno_audit_writer') THEN
            CREATE ROLE zuno_audit_writer NOLOGIN;
          END IF;
          IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='zuno_audit_reader') THEN
            CREATE ROLE zuno_audit_reader NOLOGIN;
          END IF;
        END $$;
        GRANT INSERT ON audit_records TO zuno_audit_writer;
        GRANT SELECT ON audit_records TO zuno_audit_reader;
        CREATE FUNCTION zuno_revoke_changed_authority() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
          IF NEW.role IS DISTINCT FROM OLD.role
             OR NEW.admin_privileges IS DISTINCT FROM OLD.admin_privileges
             OR NEW.status IS DISTINCT FROM OLD.status THEN
            UPDATE sessions SET revoked_at=COALESCE(revoked_at, clock_timestamp())
            WHERE account_id=NEW.id;
          END IF;
          RETURN NEW;
        END $$;
        CREATE TRIGGER revoke_changed_authority
        AFTER UPDATE OF role, admin_privileges, status ON accounts
        FOR EACH ROW EXECUTE FUNCTION zuno_revoke_changed_authority();
    """)


def downgrade() -> None:
    raise RuntimeError("forward-only: preserve audit records; roll back application, not evidence")
