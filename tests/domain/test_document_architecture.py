"""RFC-057 canonical Document architecture guardrails."""

from __future__ import annotations

import ast
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_MODULE = REPOSITORY_ROOT / "backend/app/domain/document.py"

FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "fastapi",
    "pydantic",
    "app.domain.knowledge",
    "app.infrastructure",
    "app.services",
)

EXPECTED_DOCUMENT_CLASSES = {
    "DocumentType",
    "DocumentSourceType",
    "DocumentSource",
    "EnterpriseDocument",
}


def _document_tree() -> ast.Module:
    assert DOCUMENT_MODULE.is_file(), (
        "RFC-057 requires backend/app/domain/document.py"
    )
    return ast.parse(DOCUMENT_MODULE.read_text())


def _imported_modules(tree: ast.Module) -> set[str]:
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)

    return modules


def test_document_domain_has_only_accepted_canonical_classes() -> None:
    tree = _document_tree()

    classes = {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }

    assert classes == EXPECTED_DOCUMENT_CLASSES
    assert "DocumentId" not in classes


def test_document_domain_has_no_forbidden_dependencies() -> None:
    tree = _document_tree()

    imported_modules = _imported_modules(tree)

    violations = {
        module
        for module in imported_modules
        if module.startswith(FORBIDDEN_IMPORT_PREFIXES)
    }

    assert violations == set()


def test_document_domain_introduces_no_repository_contract() -> None:
    tree = _document_tree()

    class_names = {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }

    assert not any(name.endswith("Repository") for name in class_names)


def test_document_domain_performs_no_file_io() -> None:
    tree = _document_tree()

    forbidden_calls: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name) and node.func.id == "open":
            forbidden_calls.append("open")

        if isinstance(node.func, ast.Attribute) and node.func.attr in {
            "open",
            "read_text",
            "read_bytes",
            "write_text",
            "write_bytes",
        }:
            forbidden_calls.append(node.func.attr)

    assert forbidden_calls == []
