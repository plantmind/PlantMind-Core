"""Canonical relational representation of PlantMind Knowledge."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.metadata import DatabaseBase


class KnowledgeRecordRow(DatabaseBase):
    """Infrastructure-owned relational representation of KnowledgeRecord."""

    __tablename__ = "knowledge_records"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )
    kind: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    provenance_source_type: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    provenance_source_reference: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )
    provenance_captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    subject_type: Mapped[str | None] = mapped_column(
        String(),
        nullable=True,
    )
    subject_id: Mapped[UUID | None] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=True,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "id",
            name="pk_knowledge_records",
        ),
        CheckConstraint(
            "("
            "subject_type IS NULL AND subject_id IS NULL"
            ") OR ("
            "subject_type IS NOT NULL AND subject_id IS NOT NULL"
            ")",
            name="ck_knowledge_records_subject_pair",
        ),
    )
