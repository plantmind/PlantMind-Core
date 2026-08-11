"""Establish canonical PlantMind relational schema lineage.

Revision ID: 0001
Revises: None
"""

from collections.abc import Sequence


revision: str = "0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Establish schema lineage without creating application tables."""

    pass


def downgrade() -> None:
    """Reverse the schema-neutral foundation revision."""

    pass
