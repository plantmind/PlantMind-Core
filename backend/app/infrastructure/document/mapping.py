"""Explicit mapping between canonical Documents and relational rows."""

from __future__ import annotations

from app.domain.base import EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)
from app.infrastructure.document.models import (
    EnterpriseDocumentRow,
)


def document_to_row(
    document: EnterpriseDocument,
) -> EnterpriseDocumentRow:
    """Map canonical EnterpriseDocument to its relational representation."""

    return EnterpriseDocumentRow(
        id=document.id.value,
        document_type=document.document_type.value,
        title=document.title,
        source_type=document.source.source_type.value,
        source_reference=document.source.source_reference,
    )


def row_to_document(
    row: EnterpriseDocumentRow,
) -> EnterpriseDocument:
    """Reconstruct canonical EnterpriseDocument from a relational row."""

    return EnterpriseDocument(
        id=EntityId.from_string(str(row.id)),
        document_type=DocumentType(
            value=row.document_type,
        ),
        title=row.title,
        source=DocumentSource(
            source_type=DocumentSourceType(
                value=row.source_type,
            ),
            source_reference=row.source_reference,
        ),
    )
