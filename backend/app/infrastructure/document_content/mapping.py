"""Explicit mapping for canonical Document Content descriptors."""

from __future__ import annotations

from app.domain.base import EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)
from app.infrastructure.document_content.models import (
    DocumentContentDescriptorRow,
)


def descriptor_to_row(
    descriptor: DocumentContentDescriptor,
) -> DocumentContentDescriptorRow:
    """Map a canonical descriptor to its relational representation."""

    return DocumentContentDescriptorRow(
        document_id=descriptor.document_id.value,
        media_type=descriptor.media_type.value,
        byte_length=descriptor.byte_length,
        digest=descriptor.digest.value,
    )


def row_to_descriptor(
    row: DocumentContentDescriptorRow,
) -> DocumentContentDescriptor:
    """Reconstruct a canonical descriptor from a relational row."""

    return DocumentContentDescriptor(
        document_id=EntityId.from_string(
            str(row.document_id)
        ),
        media_type=DocumentContentMediaType(
            value=row.media_type
        ),
        byte_length=row.byte_length,
        digest=DocumentContentDigest(
            value=row.digest
        ),
    )
