"""Add canonical Knowledge relational persistence schema.

Revision ID: 0002
Revises: 0001
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0002"
down_revision: str | Sequence[str] | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the canonical Knowledge records table."""

    op.create_table(
        "knowledge_records",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "kind",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "provenance_source_type",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "provenance_source_reference",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "provenance_captured_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "subject_type",
            sa.String(),
            nullable=True,
        ),
        sa.Column(
            "subject_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_knowledge_records",
        ),
        sa.CheckConstraint(
            "("
            "subject_type IS NULL AND subject_id IS NULL"
            ") OR ("
            "subject_type IS NOT NULL AND subject_id IS NOT NULL"
            ")",
            name="ck_knowledge_records_subject_pair",
        ),
    )


def downgrade() -> None:
    """Remove only the schema introduced by revision 0002."""

    op.drop_table("knowledge_records")
