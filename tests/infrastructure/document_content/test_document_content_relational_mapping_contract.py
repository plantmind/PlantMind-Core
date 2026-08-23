from __future__ import annotations

import importlib

from sqlalchemy import BigInteger, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID

from app.infrastructure.database.metadata import DatabaseBase


def _models():
    return importlib.import_module(
        "app.infrastructure.document_content.models"
    )


def _table():
    return _models().DocumentContentDescriptorRow.__table__


def test_mapping_registers_with_canonical_database_metadata() -> None:
    table = _table()

    assert table.metadata is DatabaseBase.metadata
    assert table.name == "document_content_descriptors"


def test_relational_shape_contains_exact_descriptor_columns() -> None:
    table = _table()

    assert tuple(table.c.keys()) == (
        "document_id",
        "media_type",
        "byte_length",
        "digest",
    )


def test_document_id_is_canonical_postgresql_uuid() -> None:
    column = _table().c.document_id

    assert isinstance(column.type, PostgreSQLUUID)
    assert column.type.as_uuid is True
    assert column.nullable is False
    assert column.default is None
    assert column.server_default is None


def test_descriptor_metadata_uses_accepted_relational_types() -> None:
    table = _table()

    assert isinstance(table.c.media_type.type, String)
    assert isinstance(table.c.byte_length.type, BigInteger)
    assert isinstance(table.c.digest.type, String)

    assert table.c.media_type.nullable is False
    assert table.c.byte_length.nullable is False
    assert table.c.digest.nullable is False


def test_document_id_is_sole_primary_key() -> None:
    primary_key = _table().primary_key

    assert primary_key.name == "pk_document_content_descriptors"
    assert tuple(
        column.name for column in primary_key.columns
    ) == ("document_id",)


def test_relational_schema_has_no_surrogate_identity() -> None:
    table = _table()

    assert "id" not in table.c
    assert len(table.c) == 4


def test_digest_is_not_relationally_unique() -> None:
    table = _table()

    unique_constraints = [
        constraint
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    ]

    assert unique_constraints == []
    assert table.c.digest.unique is not True


def test_descriptor_table_has_no_foreign_keys() -> None:
    assert not _table().foreign_keys


def test_database_generates_no_descriptor_values() -> None:
    table = _table()

    for column in table.c:
        assert column.default is None
        assert column.server_default is None


def test_relational_row_remains_distinct_from_domain_descriptor() -> None:
    from app.domain.document_content import DocumentContentDescriptor

    row = _models().DocumentContentDescriptorRow

    assert row is not DocumentContentDescriptor
    assert not issubclass(row, DocumentContentDescriptor)
