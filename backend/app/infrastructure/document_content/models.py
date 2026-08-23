"""Relational representation of canonical Document Content descriptors."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import BigInteger, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.metadata import DatabaseBase


class DocumentContentDescriptorRow(DatabaseBase):
    """Infrastructure-owned relational Document Content descriptor."""

    __tablename__ = "document_content_descriptors"

    document_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )
    media_type: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )
    byte_length: Mapped[int] = mapped_column(
        BigInteger(),
        nullable=False,
    )
    digest: Mapped[str] = mapped_column(
        String(),
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "document_id",
            name="pk_document_content_descriptors",
        ),
    )
