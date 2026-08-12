from __future__ import annotations

import importlib
from pathlib import Path

from sqlalchemy import CheckConstraint

from app.infrastructure.database.metadata import DatabaseBase


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MAPPING_MODULE = (
    REPOSITORY_ROOT
    / "backend"
    / "app"
    / "infrastructure"
    / "knowledge"
    / "models.py"
)


def _knowledge_table():
    importlib.import_module(
        "app.infrastructure.knowledge.models"
    )

    return DatabaseBase.metadata.tables["knowledge_records"]


def test_canonical_knowledge_mapping_registers_with_database_metadata() -> None:
    table = _knowledge_table()

    assert table.metadata is DatabaseBase.metadata
    assert table.name == "knowledge_records"


def test_canonical_knowledge_schema_preserves_required_nullability() -> None:
    table = _knowledge_table()

    required_non_nullable = (
        "id",
        "kind",
        "title",
        "content",
        "provenance_source_type",
        "provenance_source_reference",
        "provenance_captured_at",
    )

    for column_name in required_non_nullable:
        assert table.c[column_name].nullable is False

    assert table.c.subject_type.nullable is True
    assert table.c.subject_id.nullable is True


def test_canonical_knowledge_constraints_have_stable_identity() -> None:
    table = _knowledge_table()

    assert table.primary_key.name == "pk_knowledge_records"

    check_constraint_names = {
        constraint.name
        for constraint in table.constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert (
        "ck_knowledge_records_subject_pair"
        in check_constraint_names
    )


def test_database_does_not_generate_canonical_identity_or_provenance_time() -> None:
    table = _knowledge_table()

    assert table.c.id.default is None
    assert table.c.id.server_default is None

    assert table.c.provenance_captured_at.default is None
    assert table.c.provenance_captured_at.server_default is None


def test_mapping_module_does_not_own_database_runtime_lifecycle() -> None:
    assert MAPPING_MODULE.is_file()

    source = MAPPING_MODULE.read_text()

    prohibited = (
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "Settings(",
        "DATABASE_URL",
    )

    violations = [
        marker
        for marker in prohibited
        if marker in source
    ]

    assert violations == []

def test_canonical_identity_columns_use_postgresql_uuid() -> None:
    table = _knowledge_table()

    assert table.c.id.type.__class__.__name__ == "UUID"
    assert table.c.id.type.as_uuid is True

    assert table.c.subject_id.type.__class__.__name__ == "UUID"
    assert table.c.subject_id.type.as_uuid is True


def test_provenance_timestamp_preserves_timezone_aware_schema_semantics() -> None:
    table = _knowledge_table()

    assert table.c.provenance_captured_at.type.timezone is True


def test_relational_row_remains_distinct_from_canonical_domain_entity() -> None:
    from app.domain.knowledge import KnowledgeRecord
    from app.infrastructure.knowledge.models import KnowledgeRecordRow

    assert KnowledgeRecordRow is not KnowledgeRecord
    assert not issubclass(KnowledgeRecordRow, KnowledgeRecord)


def test_canonical_knowledge_schema_contains_only_accepted_columns() -> None:
    table = _knowledge_table()

    assert tuple(table.c.keys()) == (
        "id",
        "kind",
        "title",
        "content",
        "provenance_source_type",
        "provenance_source_reference",
        "provenance_captured_at",
        "subject_type",
        "subject_id",
    )


def test_canonical_knowledge_schema_has_no_subject_foreign_key() -> None:
    table = _knowledge_table()

    assert len(table.foreign_keys) == 0
