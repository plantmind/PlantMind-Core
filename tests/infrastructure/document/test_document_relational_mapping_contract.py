from __future__ import annotations

import importlib
from pathlib import Path

from sqlalchemy import UniqueConstraint

from app.infrastructure.database.metadata import DatabaseBase


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MODEL_MODULE = (
    REPOSITORY_ROOT
    / "backend"
    / "app"
    / "infrastructure"
    / "document"
    / "models.py"
)


def _document_table():
    importlib.import_module(
        "app.infrastructure.document.models"
    )

    return DatabaseBase.metadata.tables[
        "enterprise_documents"
    ]


def test_canonical_document_mapping_registers_with_database_metadata() -> None:
    table = _document_table()

    assert table.metadata is DatabaseBase.metadata
    assert table.name == "enterprise_documents"


def test_canonical_document_schema_preserves_required_nullability() -> None:
    table = _document_table()

    for column_name in (
        "id",
        "document_type",
        "title",
        "source_type",
        "source_reference",
    ):
        assert table.c[column_name].nullable is False


def test_canonical_document_primary_key_has_stable_identity() -> None:
    table = _document_table()

    assert table.primary_key.name == (
        "pk_enterprise_documents"
    )


def test_database_does_not_generate_canonical_document_identity() -> None:
    table = _document_table()

    assert table.c.id.default is None
    assert table.c.id.server_default is None


def test_canonical_document_identity_uses_postgresql_uuid() -> None:
    table = _document_table()

    assert table.c.id.type.__class__.__name__ == "UUID"
    assert table.c.id.type.as_uuid is True


def test_relational_row_remains_distinct_from_canonical_document() -> None:
    from app.domain.document import EnterpriseDocument
    from app.infrastructure.document.models import (
        EnterpriseDocumentRow,
    )

    assert EnterpriseDocumentRow is not EnterpriseDocument
    assert not issubclass(
        EnterpriseDocumentRow,
        EnterpriseDocument,
    )


def test_canonical_document_schema_contains_only_accepted_columns() -> None:
    table = _document_table()

    assert tuple(table.c.keys()) == (
        "id",
        "document_type",
        "title",
        "source_type",
        "source_reference",
    )


def test_source_reference_is_not_relationally_unique() -> None:
    table = _document_table()

    unique_constraints = [
        constraint
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    ]

    assert unique_constraints == []
    assert table.c.source_reference.unique is not True


def test_canonical_document_schema_has_no_foreign_keys() -> None:
    table = _document_table()

    assert len(table.foreign_keys) == 0


def test_document_model_does_not_own_database_runtime_lifecycle() -> None:
    assert MODEL_MODULE.is_file()

    source = MODEL_MODULE.read_text()

    prohibited = (
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "Settings(",
        "DATABASE_URL",
        "create_all(",
    )

    assert [
        marker
        for marker in prohibited
        if marker in source
    ] == []
