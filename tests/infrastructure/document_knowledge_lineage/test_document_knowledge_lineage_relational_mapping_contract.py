"""RFC-063 relational lineage mapping contract tests."""

from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID

from app.infrastructure.database.metadata import DatabaseBase
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)


def test_lineage_row_uses_canonical_metadata_authority() -> None:
    assert DocumentKnowledgeLineageRow.metadata is DatabaseBase.metadata


def test_lineage_row_has_exact_canonical_table_shape() -> None:
    table = DocumentKnowledgeLineageRow.__table__

    assert table.name == "document_knowledge_lineages"
    assert tuple(table.columns.keys()) == (
        "document_id",
        "knowledge_record_id",
    )

    document_id = table.c.document_id
    knowledge_record_id = table.c.knowledge_record_id

    assert isinstance(document_id.type, PostgreSQLUUID)
    assert document_id.type.as_uuid is True
    assert document_id.nullable is False

    assert isinstance(knowledge_record_id.type, PostgreSQLUUID)
    assert knowledge_record_id.type.as_uuid is True
    assert knowledge_record_id.nullable is False


def test_lineage_row_uses_exact_composite_primary_key() -> None:
    table = DocumentKnowledgeLineageRow.__table__
    primary_key = table.primary_key

    assert primary_key.name == "pk_document_knowledge_lineages"
    assert tuple(column.name for column in primary_key.columns) == (
        "document_id",
        "knowledge_record_id",
    )


def test_lineage_row_has_no_surrogate_identity_or_foreign_keys() -> None:
    table = DocumentKnowledgeLineageRow.__table__

    assert "id" not in table.columns
    assert len(table.columns) == 2
    assert not table.foreign_keys


def test_neither_lineage_identity_side_is_individually_unique() -> None:
    table = DocumentKnowledgeLineageRow.__table__

    assert table.c.document_id.unique is not True
    assert table.c.knowledge_record_id.unique is not True
