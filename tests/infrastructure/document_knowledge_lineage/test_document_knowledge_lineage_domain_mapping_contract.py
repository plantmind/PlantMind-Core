"""RFC-063 canonical lineage Domain/relational mapping contract tests."""

from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import (
    DocumentKnowledgeLineage,
)
from app.infrastructure.document_knowledge_lineage.mapping import (
    lineage_to_row,
    row_to_lineage,
)
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)


def _build_lineage() -> DocumentKnowledgeLineage:
    return DocumentKnowledgeLineage(
        document_id=EntityId.new(),
        knowledge_record_id=EntityId.new(),
    )


def test_lineage_to_row_preserves_both_canonical_identities() -> None:
    lineage = _build_lineage()

    row = lineage_to_row(lineage)

    assert isinstance(row, DocumentKnowledgeLineageRow)
    assert row.document_id == lineage.document_id.value
    assert row.knowledge_record_id == lineage.knowledge_record_id.value


def test_row_to_lineage_reconstructs_canonical_domain_value() -> None:
    original = _build_lineage()

    row = DocumentKnowledgeLineageRow(
        document_id=original.document_id.value,
        knowledge_record_id=original.knowledge_record_id.value,
    )

    lineage = row_to_lineage(row)

    assert isinstance(lineage, DocumentKnowledgeLineage)
    assert lineage.document_id == original.document_id
    assert lineage.knowledge_record_id == original.knowledge_record_id


def test_lineage_mapping_round_trip_is_exact() -> None:
    original = _build_lineage()

    reconstructed = row_to_lineage(
        lineage_to_row(original)
    )

    assert reconstructed == original
