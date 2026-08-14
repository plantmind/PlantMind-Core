from __future__ import annotations

import importlib

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)


def _models_module():
    return importlib.import_module(
        "app.infrastructure.document.models"
    )


def _mapping_module():
    return importlib.import_module(
        "app.infrastructure.document.mapping"
    )


def _build_document() -> EnterpriseDocument:
    return EnterpriseDocument(
        id=EntityId.new(),
        document_type=DocumentType(
            value=" Procedure ",
        ),
        title=" Compressor Startup Procedure ",
        source=DocumentSource(
            source_type=DocumentSourceType(
                value=" CMMS ",
            ),
            source_reference=" PROC-001 ",
        ),
    )


def test_domain_to_relational_mapping_preserves_canonical_values() -> None:
    models = _models_module()
    mapping = _mapping_module()
    document = _build_document()

    row = mapping.document_to_row(document)

    assert isinstance(
        row,
        models.EnterpriseDocumentRow,
    )
    assert row.id == document.id.value
    assert row.document_type == "procedure"
    assert row.title == "Compressor Startup Procedure"
    assert row.source_type == "cmms"
    assert row.source_reference == "PROC-001"


def test_relational_to_domain_mapping_round_trips_document() -> None:
    mapping = _mapping_module()
    original = _build_document()

    restored = mapping.row_to_document(
        mapping.document_to_row(original)
    )

    assert restored == original


def test_mapping_preserves_source_reference_case() -> None:
    mapping = _mapping_module()

    document = EnterpriseDocument(
        id=EntityId.new(),
        document_type=DocumentType(
            value="procedure",
        ),
        title="Startup Procedure",
        source=DocumentSource(
            source_type=DocumentSourceType(
                value="document",
            ),
            source_reference="Proc-ABC-001",
        ),
    )

    row = mapping.document_to_row(document)

    assert row.source_reference == "Proc-ABC-001"

    restored = mapping.row_to_document(row)

    assert (
        restored.source.source_reference
        == "Proc-ABC-001"
    )


def test_relational_to_domain_mapping_preserves_domain_validation() -> None:
    models = _models_module()
    mapping = _mapping_module()

    row = models.EnterpriseDocumentRow(
        id=EntityId.new().value,
        document_type="procedure",
        title="   ",
        source_type="document",
        source_reference="PROC-001",
    )

    with pytest.raises(DomainException):
        mapping.row_to_document(row)


def test_relational_to_domain_mapping_reconstructs_open_classifications() -> None:
    models = _models_module()
    mapping = _mapping_module()

    row = models.EnterpriseDocumentRow(
        id=EntityId.new().value,
        document_type=" Procedure ",
        title="Compressor Procedure",
        source_type=" CMMS ",
        source_reference="REF-001",
    )

    restored = mapping.row_to_document(row)

    assert restored.document_type.value == "procedure"
    assert restored.source.source_type.value == "cmms"
