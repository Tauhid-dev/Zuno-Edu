"""identity accounts, sessions and MFA state"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS citext")
    op.create_table(
        "accounts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("email", postgresql.CITEXT()),
        sa.Column("display_name", sa.String(200), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column(
            "admin_privileges", postgresql.ARRAY(sa.Text()), nullable=False, server_default="{}"
        ),
        sa.Column("mfa_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("version", sa.BigInteger(), nullable=False, server_default="1"),
        sa.PrimaryKeyConstraint("id", name="pk_accounts"),
        sa.UniqueConstraint("email", name="uq_accounts_email"),
        sa.CheckConstraint("version > 0", name="ck_accounts_positive_version"),
    )
    op.create_table(
        "credentials",
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("failed_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("locked_until", sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], name="fk_credentials_account_id_accounts"
        ),
        sa.PrimaryKeyConstraint("account_id", name="pk_credentials"),
        sa.CheckConstraint("failed_attempts >= 0", name="ck_credentials_nonnegative_failures"),
    )
    op.create_table(
        "sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("token_hash", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
        sa.Column("mfa_verified_at", sa.DateTime(timezone=True)),
        sa.Column("device_label", sa.String(200), nullable=False, server_default=""),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], name="fk_sessions_account_id_accounts"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_sessions"),
        sa.UniqueConstraint("token_hash", name="uq_sessions_token_hash"),
    )
    op.create_table(
        "one_time_tokens",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("token_hash", sa.LargeBinary(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True)),
        sa.Column("payload_ciphertext", sa.LargeBinary()),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], name="fk_one_time_tokens_account_id_accounts"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_one_time_tokens"),
        sa.UniqueConstraint("token_hash", name="uq_one_time_tokens_token_hash"),
    )
    op.create_table(
        "mfa_factors",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("secret_ciphertext", sa.LargeBinary(), nullable=False),
        sa.Column("encryption_key_version", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("last_accepted_step", sa.BigInteger()),
        sa.Column("activated_at", sa.DateTime(timezone=True)),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
        sa.Column("version", sa.BigInteger(), nullable=False, server_default="1"),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], name="fk_mfa_factors_account_id_accounts"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_mfa_factors"),
    )
    op.create_index(
        "uq_mfa_factors_active_account",
        "mfa_factors",
        ["account_id"],
        unique=True,
        postgresql_where=sa.text("status = 'active'"),
    )
    op.create_table(
        "idempotency_records",
        sa.Column("principal_scope", sa.Text(), nullable=False),
        sa.Column("operation_id", sa.Text(), nullable=False),
        sa.Column("key", sa.UUID(), nullable=False),
        sa.Column("request_hash", sa.LargeBinary(), nullable=False),
        sa.Column("result_ciphertext", sa.LargeBinary()),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint(
            "principal_scope", "operation_id", "key", name="pk_idempotency_records"
        ),
        sa.CheckConstraint(
            "operation_id <> 'API-AUTH-MFA-ENROL' OR result_ciphertext IS NULL",
            name="ck_idempotency_records_mfa_no_secret_result",
        ),
    )
    op.create_table(
        "mfa_challenges",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("token_hash", sa.LargeBinary(), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("browser_binding_hash", sa.LargeBinary(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("consumed_at", sa.DateTime(timezone=True)),
        sa.Column("factor_id", sa.UUID()),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], name="fk_mfa_challenges_account_id_accounts"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_mfa_challenges"),
        sa.UniqueConstraint("token_hash", name="uq_mfa_challenges_token_hash"),
    )
    op.create_table(
        "mfa_recovery_codes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("factor_id", sa.UUID(), nullable=False),
        sa.Column("code_hash", sa.LargeBinary(), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(
            ["factor_id"], ["mfa_factors.id"], name="fk_mfa_recovery_codes_factor_id_mfa_factors"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_mfa_recovery_codes"),
        sa.UniqueConstraint("code_hash", name="uq_mfa_recovery_codes_code_hash"),
    )
    op.create_index("ix_mfa_factors_account_status", "mfa_factors", ["account_id", "status"])
    op.create_index(
        "ix_mfa_challenges_account_purpose", "mfa_challenges", ["account_id", "purpose"]
    )
    op.create_index("ix_one_time_tokens_expiry", "one_time_tokens", ["expires_at"])
    op.create_index("ix_idempotency_records_expiry", "idempotency_records", ["expires_at"])
    checks = {
        "accounts": {
            "role": "role IN ('parent','student','teacher','admin')",
            "status": "status IN ('invited','pending_verification','active','suspended','closed')",
            "privileges": "(role = 'admin') = (cardinality(admin_privileges) > 0) AND "
            "admin_privileges <@ ARRAY['identity_admin','education_admin','finance_admin',"
            "'operations_admin','audit_admin']::text[]",
            "adult_email": "role = 'student' OR email IS NOT NULL",
        },
        "sessions": {"expiry_order": "expires_at > created_at"},
        "one_time_tokens": {
            "purpose": "purpose IN ('verification','reset','invitation','challenge','setup')"
        },
        "mfa_factors": {
            "status": "status IN ('pending','active','revoked')",
            "positive_version": "version > 0",
        },
        "mfa_challenges": {
            "bounded_attempts": "attempts BETWEEN 0 AND 5",
            "purpose": "purpose IN ('challenge','setup')",
        },
    }
    for table, constraints in checks.items():
        for name, condition in constraints.items():
            op.create_check_constraint(op.f(f"ck_{table}_{name}"), table, condition)
    op.create_foreign_key(
        "fk_mfa_challenges_factor_id_mfa_factors",
        "mfa_challenges",
        "mfa_factors",
        ["factor_id"],
        ["id"],
    )
    op.create_index("ix_accounts_status", "accounts", ["status", "id"])
    op.create_index("ix_sessions_account_revoked", "sessions", ["account_id", "revoked_at"])
    op.create_index("ix_sessions_expiry", "sessions", ["expires_at"])
    op.create_index(
        "ix_one_time_tokens_account_purpose", "one_time_tokens", ["account_id", "purpose"]
    )
    op.create_index("ix_mfa_challenges_expiry", "mfa_challenges", ["expires_at"])
    op.create_index("ix_mfa_challenges_factor", "mfa_challenges", ["factor_id"])
    op.create_index(
        "ix_mfa_recovery_codes_factor_consumed", "mfa_recovery_codes", ["factor_id", "consumed_at"]
    )
    for table in (
        "accounts",
        "credentials",
        "sessions",
        "one_time_tokens",
        "mfa_factors",
        "mfa_challenges",
        "mfa_recovery_codes",
    ):
        if table != "sessions":
            op.add_column(
                table,
                sa.Column(
                    "created_at",
                    sa.DateTime(timezone=True),
                    nullable=False,
                    server_default=sa.func.now(),
                ),
            )
        op.add_column(
            table,
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),
        )


def downgrade() -> None:
    raise RuntimeError("Identity state is forward-only; review a forward-fix migration.")
