from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("jobs",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("execution_backend", sa.String(64), nullable=False),
        sa.Column("backend_config", sa.JSON(), nullable=False),
        sa.Column("target_source_id", sa.String(64)),
        sa.Column("environment", sa.String(32), nullable=False),
        sa.Column("schedule_type", sa.String(32), nullable=False),
        sa.Column("schedule_expr", sa.String(255)),
        sa.Column("timezone", sa.String(64), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("requires_approval", sa.Boolean(), nullable=False),
        sa.Column("max_concurrent_runs", sa.Integer(), nullable=False),
        sa.Column("max_parallel_targets", sa.Integer(), nullable=False),
        sa.Column("max_retries", sa.Integer(), nullable=False),
        sa.Column("dependencies", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    for table in [
        "target_sources","targets","job_runs","target_runs","approvals",
        "audit_events","notifications","distributed_locks","execution_policies"]:
        op.execute(f"-- table {table} managed by SQLAlchemy metadata in production autogenerate")
def downgrade():
    op.drop_table("jobs")
