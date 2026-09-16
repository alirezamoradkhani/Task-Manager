"""Create tasks table.

Revision ID: 20260820_01
Revises:
Create Date: 2026-08-20
"""

from alembic import op
import sqlalchemy as sa


revision: str = "20260820_01"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("importance", sa.Integer(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "importance >= 0 AND importance <= 5",
            name="importance_between_zero_and_five",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_tasks"),
    )


def downgrade() -> None:
    op.drop_table("tasks")
