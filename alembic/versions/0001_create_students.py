"""Создает таблицу для студентов."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_create_students"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Создает."""
    op.create_table(
        "student",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("faculty", sa.String(length=100), nullable=False),
        sa.Column("course", sa.String(length=100), nullable=False),
        sa.Column("grade", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Удаляет."""
    op.drop_table("student")
