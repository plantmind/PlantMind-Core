from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.document_knowledge_lineage import DocumentKnowledgeLineage


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = (
    REPOSITORY_ROOT
    / "backend"
    / "app"
    / "domain"
    / "document_knowledge_lineage.py"
)


def test_lineage_contract_contains_exactly_canonical_identity_pair() -> None:
    assert tuple(field.name for field in fields(DocumentKnowledgeLineage)) == (
        "document_id",
        "knowledge_record_id",
    )


def test_lineage_preserves_canonical_document_and_knowledge_identity() -> None:
    document_id = EntityId.from_string(
        "11111111-1111-1111-1111-111111111111"
    )
    knowledge_record_id = EntityId.from_string(
        "22222222-2222-2222-2222-222222222222"
    )

    lineage = DocumentKnowledgeLineage(
        document_id=document_id,
        knowledge_record_id=knowledge_record_id,
    )

    assert lineage.document_id is document_id
    assert lineage.knowledge_record_id is knowledge_record_id


def test_lineage_is_immutable() -> None:
    lineage = DocumentKnowledgeLineage(
        document_id=EntityId.new(),
        knowledge_record_id=EntityId.new(),
    )

    with pytest.raises(FrozenInstanceError):
        lineage.document_id = EntityId.new()


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("document_id", "not-an-entity-id"),
        ("document_id", None),
        ("knowledge_record_id", "not-an-entity-id"),
        ("knowledge_record_id", None),
    ],
)
def test_lineage_rejects_non_entity_identity(
    field_name: str,
    invalid_value: object,
) -> None:
    values: dict[str, object] = {
        "document_id": EntityId.new(),
        "knowledge_record_id": EntityId.new(),
    }
    values[field_name] = invalid_value

    with pytest.raises(DomainException):
        DocumentKnowledgeLineage(
            document_id=values["document_id"],  # type: ignore[arg-type]
            knowledge_record_id=values["knowledge_record_id"],  # type: ignore[arg-type]
        )


def test_lineage_does_not_generate_or_replace_identity() -> None:
    document_id = EntityId.new()
    knowledge_record_id = EntityId.new()

    lineage = DocumentKnowledgeLineage(
        document_id=document_id,
        knowledge_record_id=knowledge_record_id,
    )

    assert lineage.document_id == document_id
    assert lineage.knowledge_record_id == knowledge_record_id


def test_lineage_module_depends_only_on_shared_domain_primitives() -> None:
    assert MODULE_PATH.is_file()

    tree = ast.parse(MODULE_PATH.read_text())

    imported_modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.add(node.module)

        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)

    prohibited_prefixes = (
        "app.document",
        "app.knowledge",
        "app.services",
        "app.infrastructure",
        "app.api",
        "sqlalchemy",
        "psycopg",
    )

    violations = sorted(
        module
        for module in imported_modules
        if module.startswith(prohibited_prefixes)
    )

    assert violations == []


def test_lineage_module_does_not_redefine_adjacent_domain_semantics() -> None:
    assert MODULE_PATH.is_file()

    source = MODULE_PATH.read_text()

    prohibited = (
        "KnowledgeProvenance",
        "KnowledgeSubject",
        "DocumentSource",
        "source_reference",
        "source_type",
        "captured_at",
        "EnterpriseDocument",
        "KnowledgeRecord",
        "Repository",
        "SQLAlchemy",
        "Session",
        "DatabaseRuntime",
        "DATABASE_URL",
    )

    violations = [
        marker
        for marker in prohibited
        if marker in source
    ]

    assert violations == []


def test_lineage_module_does_not_introduce_lineage_identity_generator() -> None:
    assert MODULE_PATH.is_file()

    source = MODULE_PATH.read_text()

    prohibited = (
        "LineageId",
        "EntityId.new(",
        "uuid4(",
    )

    violations = [
        marker
        for marker in prohibited
        if marker in source
    ]

    assert violations == []
