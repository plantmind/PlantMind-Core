"""RFC-057 canonical enterprise Document domain tests."""

from dataclasses import FrozenInstanceError

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)


def test_document_type_normalizes_open_classification() -> None:
    document_type = DocumentType(value="  Operating_Philosophy  ")

    assert document_type.value == "operating_philosophy"


@pytest.mark.parametrize("value", ["", "   "])
def test_document_type_rejects_empty_value(value: str) -> None:
    with pytest.raises(DomainException):
        DocumentType(value=value)


def test_document_type_rejects_non_string_value() -> None:
    with pytest.raises(DomainException):
        DocumentType(value=123)  # type: ignore[arg-type]


def test_document_source_type_normalizes_open_classification() -> None:
    source_type = DocumentSourceType(value="  File_Server  ")

    assert source_type.value == "file_server"


@pytest.mark.parametrize("value", ["", "   "])
def test_document_source_type_rejects_empty_value(value: str) -> None:
    with pytest.raises(DomainException):
        DocumentSourceType(value=value)


def test_document_source_type_rejects_non_string_value() -> None:
    with pytest.raises(DomainException):
        DocumentSourceType(value=123)  # type: ignore[arg-type]


def test_document_source_preserves_opaque_reference_casing() -> None:
    source = DocumentSource(
        source_type=DocumentSourceType(value="document_control"),
        source_reference="  PROC-001/Rev-A  ",
    )

    assert source.source_reference == "PROC-001/Rev-A"


@pytest.mark.parametrize("value", ["", "   "])
def test_document_source_rejects_empty_reference(value: str) -> None:
    with pytest.raises(DomainException):
        DocumentSource(
            source_type=DocumentSourceType(value="file_server"),
            source_reference=value,
        )


def test_document_source_rejects_non_string_reference() -> None:
    with pytest.raises(DomainException):
        DocumentSource(
            source_type=DocumentSourceType(value="file_server"),
            source_reference=123,  # type: ignore[arg-type]
        )


def test_document_source_requires_canonical_source_type() -> None:
    with pytest.raises(DomainException):
        DocumentSource(
            source_type="file_server",  # type: ignore[arg-type]
            source_reference="DOC-001",
        )


def test_enterprise_document_constructs_canonical_record() -> None:
    document_id = EntityId.new()
    document_type = DocumentType(value=" Procedure ")
    source = DocumentSource(
        source_type=DocumentSourceType(value=" File_Server "),
        source_reference="  PROC-001  ",
    )

    document = EnterpriseDocument(
        id=document_id,
        document_type=document_type,
        title="  Ethane Booster Compressor Startup Procedure  ",
        source=source,
    )

    assert document.id is document_id
    assert document.document_type is document_type
    assert document.title == "Ethane Booster Compressor Startup Procedure"
    assert document.source is source


@pytest.mark.parametrize("title", ["", "   "])
def test_enterprise_document_rejects_empty_title(title: str) -> None:
    with pytest.raises(DomainException):
        EnterpriseDocument(
            id=EntityId.new(),
            document_type=DocumentType(value="manual"),
            title=title,
            source=DocumentSource(
                source_type=DocumentSourceType(value="file_server"),
                source_reference="MAN-001",
            ),
        )


def test_enterprise_document_rejects_non_string_title() -> None:
    with pytest.raises(DomainException):
        EnterpriseDocument(
            id=EntityId.new(),
            document_type=DocumentType(value="manual"),
            title=123,  # type: ignore[arg-type]
            source=DocumentSource(
                source_type=DocumentSourceType(value="file_server"),
                source_reference="MAN-001",
            ),
        )


def test_enterprise_document_requires_canonical_entity_id() -> None:
    with pytest.raises(DomainException):
        EnterpriseDocument(
            id="DOC-001",  # type: ignore[arg-type]
            document_type=DocumentType(value="manual"),
            title="Vendor Manual",
            source=DocumentSource(
                source_type=DocumentSourceType(value="file_server"),
                source_reference="MAN-001",
            ),
        )


def test_enterprise_document_requires_document_type() -> None:
    with pytest.raises(DomainException):
        EnterpriseDocument(
            id=EntityId.new(),
            document_type="manual",  # type: ignore[arg-type]
            title="Vendor Manual",
            source=DocumentSource(
                source_type=DocumentSourceType(value="file_server"),
                source_reference="MAN-001",
            ),
        )


def test_enterprise_document_requires_document_source() -> None:
    with pytest.raises(DomainException):
        EnterpriseDocument(
            id=EntityId.new(),
            document_type=DocumentType(value="manual"),
            title="Vendor Manual",
            source="MAN-001",  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("factory", "field", "replacement"),
    [
        (
            lambda: DocumentType(value="procedure"),
            "value",
            "manual",
        ),
        (
            lambda: DocumentSourceType(value="file_server"),
            "value",
            "sap",
        ),
        (
            lambda: DocumentSource(
                source_type=DocumentSourceType(value="file_server"),
                source_reference="PROC-001",
            ),
            "source_reference",
            "PROC-002",
        ),
        (
            lambda: EnterpriseDocument(
                id=EntityId.new(),
                document_type=DocumentType(value="procedure"),
                title="Startup Procedure",
                source=DocumentSource(
                    source_type=DocumentSourceType(value="file_server"),
                    source_reference="PROC-001",
                ),
            ),
            "title",
            "Changed",
        ),
    ],
)
def test_document_contracts_are_immutable(
    factory,
    field: str,
    replacement: object,
) -> None:
    instance = factory()

    with pytest.raises(FrozenInstanceError):
        setattr(instance, field, replacement)
