"""Add canonical Document Content descriptor relational schema.

Revision ID: 0005
Revises: 0004
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0005"
down_revision: str | Sequence[str] | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the canonical Document Content descriptor table."""

    op.create_table(
        "document_content_descriptors",
        sa.Column(
            "document_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "media_type",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "byte_length",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "digest",
            sa.String(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "document_id",
            name="pk_document_content_descriptors",
        ),
    )


def downgrade() -> None:
    """Remove only the schema introduced by revision 0005."""

    op.drop_table("document_content_descriptors")
