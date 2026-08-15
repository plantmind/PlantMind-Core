"""Architecture guardrails for the canonical lineage repository port."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from app.core.composition import CompositionRoot
from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageRepository,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPOSITORY_FILE = (
    PROJECT_ROOT
    / "backend/app/document_knowledge_lineage/repository.py"
)

PACKAGE_INIT = (
    PROJECT_ROOT
    / "backend/app/document_knowledge_lineage/__init__.py"
)

EXPECTED_CLASSES = {
    "DocumentKnowledgeLineageAlreadyExistsError",
    "DocumentKnowledgeLineageRepository",
}

FORBIDDEN_REPOSITORY_METHODS = {
    "list",
    "find",
    "search",
    "filter",
    "query",
    "update",
    "delete",
    "remove",
    "upsert",
    "replace",
    "save",
    "get_by_document",
    "get_by_knowledge",
}

FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "psycopg",
    "fastapi",
    "pydantic",
    "app.infrastructure",
    "app.services",
    "app.document.repository",
    "app.knowledge.repository",
)


def _tree() -> ast.Module:
    return ast.parse(REPOSITORY_FILE.read_text())


def _imported_modules() -> set[str]:
    modules: set[str] = set()

    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)

    return modules


def _non_stdlib_modules() -> set[str]:
    return {
        module
        for module in _imported_modules()
        if module.split(".", 1)[0] not in sys.stdlib_module_names
    }


def test_repository_module_exists() -> None:
    assert REPOSITORY_FILE.is_file()


def test_package_initializer_remains_empty() -> None:
    assert PACKAGE_INIT.is_file()
    assert PACKAGE_INIT.read_text() == ""


def test_repository_module_has_exact_top_level_classes() -> None:
    classes = {
        node.name
        for node in _tree().body
        if isinstance(node, ast.ClassDef)
    }

    assert classes == EXPECTED_CLASSES


def test_repository_depends_only_on_canonical_domain_contracts() -> None:
    assert _non_stdlib_modules() == {
        "app.domain.base",
        "app.domain.document_knowledge_lineage",
    }


def test_repository_has_no_forbidden_dependencies() -> None:
    imports = _imported_modules()

    assert not any(
        imported == prefix
        or imported.startswith(f"{prefix}.")
        for imported in imports
        for prefix in FORBIDDEN_IMPORT_PREFIXES
    )


def test_repository_exposes_exact_operation_set() -> None:
    repository_class = next(
        node
        for node in _tree().body
        if isinstance(node, ast.ClassDef)
        and node.name == "DocumentKnowledgeLineageRepository"
    )

    methods = {
        node.name
        for node in repository_class.body
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    }

    assert methods == {"add", "get"}
    assert methods.isdisjoint(FORBIDDEN_REPOSITORY_METHODS)


def test_repository_performs_no_file_io() -> None:
    forbidden_calls = {
        "open",
        "read",
        "read_text",
        "read_bytes",
        "write",
        "write_text",
        "write_bytes",
    }

    calls = {
        node.func.id
        for node in ast.walk(_tree())
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
    }

    attribute_calls = {
        node.func.attr
        for node in ast.walk(_tree())
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
    }

    assert calls.isdisjoint(forbidden_calls)
    assert attribute_calls.isdisjoint(forbidden_calls)


def test_repository_generates_no_identity() -> None:
    for node in ast.walk(_tree()):
        if not isinstance(node, ast.Call):
            continue

        if not isinstance(node.func, ast.Attribute):
            continue

        assert not (
            isinstance(node.func.value, ast.Name)
            and node.func.value.id == "EntityId"
            and node.func.attr == "new"
        )


def test_default_composition_does_not_register_lineage_repository() -> None:
    platform = CompositionRoot.build()

    assert not platform.container.is_registered(
        DocumentKnowledgeLineageRepository
    )


def test_platform_composition_exposes_no_lineage_repository() -> None:
    platform = CompositionRoot.build()

    assert not hasattr(
        platform,
        "document_knowledge_lineage_repository",
    )
