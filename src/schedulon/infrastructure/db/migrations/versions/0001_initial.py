from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "jobs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("execution_backend", sa.String(64), nullable=False),
        sa.Column("backend_config", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("target_source_id", sa.String(64)),
        sa.Column("environment", sa.String(32), nullable=False, server_default="development"),
        sa.Column("schedule_type", sa.String(32), nullable=False, server_default="manual"),
        sa.Column("schedule_expr", sa.String(255)),
        sa.Column("timezone", sa.String(64), nullable=False, server_default="Europe/Paris"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("requires_approval", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("max_concurrent_runs", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("max_parallel_targets", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("max_retries", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("dependencies", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "target_sources",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("source_type", sa.String(64), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "targets",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("source_id", sa.String(64), sa.ForeignKey("target_sources.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("address", sa.String(255), nullable=False),
        sa.Column("vars", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )

    op.create_table(
        "job_runs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("job_id", sa.String(64), sa.ForeignKey("jobs.id"), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("actor_id", sa.String(255)),
        sa.Column("actor_type", sa.String(64), nullable=False, server_default="user"),
        sa.Column("ticket_number", sa.String(128)),
        sa.Column("environment", sa.String(32), nullable=False, server_default="development"),
        sa.Column("runtime_config", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("idempotency_key", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("job_id", "idempotency_key", name="uq_job_idempotency"),
    )

    op.create_table(
        "target_runs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("run_id", sa.String(64), sa.ForeignKey("job_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_id", sa.String(64)),
        sa.Column("target_name", sa.String(255), nullable=False),
        sa.Column("target_address", sa.String(255), nullable=False),
        sa.Column("target_vars", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("status", sa.String(32), nullable=False, server_default="queued"),
        sa.Column("attempt", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("locked_by", sa.String(255)),
        sa.Column("locked_at", sa.DateTime(timezone=True)),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("exit_code", sa.Integer()),
        sa.Column("error_message", sa.Text()),
        sa.Column("result", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
    )

    op.create_table(
        "approvals",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("run_id", sa.String(64), sa.ForeignKey("job_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("requested_by", sa.String(255)),
        sa.Column("approved_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("decided_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("actor_type", sa.String(64), nullable=False, server_default="user"),
        sa.Column("actor_id", sa.String(255)),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("entity_id", sa.String(64)),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("run_id", sa.String(64)),
        sa.Column("channel", sa.String(64), nullable=False),
        sa.Column("recipients", sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column("subject", sa.String(512), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("provider_message_id", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )

    op.create_table(
        "distributed_locks",
        sa.Column("name", sa.String(128), primary_key=True),
        sa.Column("owner_id", sa.String(255), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "execution_policies",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("config", sa.JSON(), nullable=False, server_default=sa.text("'{}'::json")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )


def downgrade():
    for table_name in [
        "execution_policies",
        "distributed_locks",
        "notifications",
        "audit_events",
        "approvals",
        "target_runs",
        "job_runs",
        "targets",
        "target_sources",
        "jobs",
    ]:
        op.drop_table(table_name)
