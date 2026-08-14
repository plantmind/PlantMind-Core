"""Canonical relational representation of PlantMind Enterprise Documents."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import (
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.metadata import DatabaseBase


class EnterpriseDocumentRow(DatabaseBase):
    """Infrastructure-owned relational representation of EnterpriseDocument."""

    __tablename__ = "enterprise_documents"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )
    document_type: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    source_reference: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "id",
            name="pk_enterprise_documents",
        ),
    )
