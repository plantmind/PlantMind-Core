"""Add canonical Document-to-Knowledge lineage relational schema.

Revision ID: 0004
Revises: 0003
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0004"
down_revision: str | Sequence[str] | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the canonical Document-to-Knowledge lineage table."""

    op.create_table(
        "document_knowledge_lineages",
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "knowledge_record_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "document_id",
            "knowledge_record_id",
            name="pk_document_knowledge_lineages",
        ),
    )


def downgrade() -> None:
    """Remove only the schema introduced by revision 0004."""

    op.drop_table("document_knowledge_lineages")
