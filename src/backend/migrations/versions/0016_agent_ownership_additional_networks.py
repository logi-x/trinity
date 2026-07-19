"""Add persisted additional Docker networks to agent ownership.

Revision ID: 0016_agent_ownership_additional_networks
Revises: 0015_coordination_runs
Create Date: 2026-07-19
"""

import sqlalchemy as sa
from alembic import op


revision = "0016_agent_ownership_additional_networks"
down_revision = "0015_coordination_runs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("agent_ownership", sa.Column("additional_networks", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("agent_ownership", "additional_networks")
