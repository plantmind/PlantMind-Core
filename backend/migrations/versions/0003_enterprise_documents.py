"""Add canonical Enterprise Document relational persistence schema.

Revision ID: 0003
Revises: 0002
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0003"
down_revision: str | Sequence[str] | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the canonical Enterprise Documents table."""

    op.create_table(
        "enterprise_documents",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "document_type",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "source_type",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "source_reference",
            sa.Text(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_enterprise_documents",
        ),
    )


def downgrade() -> None:
    """Remove only the schema introduced by revision 0003."""

    op.drop_table("enterprise_documents")
