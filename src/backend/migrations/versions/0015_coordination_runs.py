"""Add durable coordination-run correlation tables.

Coordination runs correlate existing executions and operator-queue items
without duplicating their logs, output, cost, or agent-defined pipeline state.

Revision ID: 0015_coordination_runs
Revises: 0014_agent_schedules_webhook_auth
Create Date: 2026-07-18
"""

from alembic import op


revision = "0015_coordination_runs"
down_revision = "0014_agent_schedules_webhook_auth"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS coordination_runs (
            id TEXT PRIMARY KEY,
            owner_agent TEXT NOT NULL,
            root_execution_id TEXT,
            outcome TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
                CHECK(status IN ('active', 'waiting', 'blocked', 'completed', 'cancelled')),
            context TEXT,
            version INTEGER NOT NULL DEFAULT 1,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            closed_at TEXT
        )
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS coordination_run_resources (
            run_id TEXT NOT NULL,
            resource_type TEXT NOT NULL
                CHECK(resource_type IN ('execution', 'operator_queue')),
            resource_id TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL,
            notified_status TEXT,
            notified_at TEXT,
            PRIMARY KEY (run_id, resource_type, resource_id),
            FOREIGN KEY (run_id) REFERENCES coordination_runs(id) ON DELETE CASCADE
        )
    """)
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_coordination_runs_owner_status "
        "ON coordination_runs(owner_agent, status, updated_at DESC)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_coordination_resources_lookup "
        "ON coordination_run_resources(resource_type, resource_id)"
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS coordination_run_resources")
    op.execute("DROP TABLE IF EXISTS coordination_runs")
