"""Canonical relational representation of Document-to-Knowledge lineage."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.metadata import DatabaseBase


class DocumentKnowledgeLineageRow(DatabaseBase):
    """Infrastructure-owned relational representation of canonical lineage."""

    __tablename__ = "document_knowledge_lineages"

    document_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )
    knowledge_record_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "document_id",
            "knowledge_record_id",
            name="pk_document_knowledge_lineages",
        ),
    )
