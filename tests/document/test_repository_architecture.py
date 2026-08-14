"""Architecture guardrails for the Enterprise Document repository port."""

from __future__ import annotations

import ast
from pathlib import Path


REPOSITORY_FILE = Path(
    "backend/app/document/repository.py"
)

EXPECTED_CLASSES = {
    "EnterpriseDocumentAlreadyExistsError",
    "EnterpriseDocumentRepository",
}

FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "fastapi",
    "pydantic",
    "app.infrastructure",
    "app.services",
    "app.models",
)

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
    "find_by_source_reference",
}


def _tree() -> ast.Module:
    return ast.parse(REPOSITORY_FILE.read_text())


def test_repository_module_exists() -> None:
    assert REPOSITORY_FILE.is_file()


def test_repository_module_has_exact_top_level_classes() -> None:
    classes = {
        node.name
        for node in _tree().body
        if isinstance(node, ast.ClassDef)
    }

    assert classes == EXPECTED_CLASSES


def test_repository_has_no_forbidden_dependencies() -> None:
    imports: list[str] = []

    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)

        if isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)

    assert not any(
        imported == prefix
        or imported.startswith(f"{prefix}.")
        for imported in imports
        for prefix in FORBIDDEN_IMPORT_PREFIXES
    )


def test_repository_exposes_no_search_or_mutation_expansion() -> None:
    repository_class = next(
        node
        for node in _tree().body
        if isinstance(node, ast.ClassDef)
        and node.name == "EnterpriseDocumentRepository"
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


def test_repository_module_performs_no_file_io() -> None:
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


PACKAGE_INIT = Path(
    "backend/app/document/__init__.py"
)


def test_document_package_initializer_remains_empty() -> None:
    assert PACKAGE_INIT.is_file()
    assert PACKAGE_INIT.read_text() == ""
