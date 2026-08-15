"""Explicit mapping between canonical lineage and relational rows."""

from __future__ import annotations

from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import (
    DocumentKnowledgeLineage,
)
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)


def lineage_to_row(
    lineage: DocumentKnowledgeLineage,
) -> DocumentKnowledgeLineageRow:
    """Map canonical lineage to its relational representation."""

    return DocumentKnowledgeLineageRow(
        document_id=lineage.document_id.value,
        knowledge_record_id=lineage.knowledge_record_id.value,
    )


def row_to_lineage(
    row: DocumentKnowledgeLineageRow,
) -> DocumentKnowledgeLineage:
    """Reconstruct canonical lineage from its relational representation."""

    return DocumentKnowledgeLineage(
        document_id=EntityId.from_string(str(row.document_id)),
        knowledge_record_id=EntityId.from_string(
            str(row.knowledge_record_id)
        ),
    )
