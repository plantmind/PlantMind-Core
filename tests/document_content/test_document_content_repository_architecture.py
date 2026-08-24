"""RFC-068 Document Content repository architecture guardrails."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PACKAGE = ROOT / "backend/app/document_content"
INIT_FILE = PACKAGE / "__init__.py"
REPOSITORY_FILE = PACKAGE / "repository.py"

DOMAIN_CONTENT = ROOT / "backend/app/domain/document_content.py"
DOMAIN_DOCUMENT = ROOT / "backend/app/domain/document.py"


def _tree() -> ast.Module:
    assert REPOSITORY_FILE.is_file(), (
        "RFC-068 requires "
        "backend/app/document_content/repository.py"
    )
    return ast.parse(REPOSITORY_FILE.read_text())


def _imports() -> set[str]:
    imported: set[str] = set()

    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            imported.update(
                alias.name for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")

    return imported


def test_canonical_package_files_exist() -> None:
    assert PACKAGE.is_dir()
    assert INIT_FILE.is_file()
    assert REPOSITORY_FILE.is_file()


def test_package_initializer_is_empty() -> None:
    assert INIT_FILE.read_bytes() == b""


def test_package_contains_only_contract_python_files() -> None:
    python_files = {
        path.name
        for path in PACKAGE.iterdir()
        if path.is_file()
        and path.suffix == ".py"
    }

    assert python_files == {
        "__init__.py",
        "repository.py",
        "store.py",
    }


def test_repository_dependencies_are_minimal() -> None:
    assert _imports() <= {
        "__future__",
        "abc",
        "app.domain.base",
        "app.domain.document_content",
    }


def test_repository_has_no_forbidden_dependencies() -> None:
    forbidden = (
        "app.domain.document",
        "app.document.repository",
        "app.services",
        "app.infrastructure",
        "sqlalchemy",
        "fastapi",
        "pydantic",
        "pathlib",
        "os",
        "io",
        "socket",
        "urllib",
        "http",
        "requests",
        "aiohttp",
    )

    assert not any(
        module == prefix or module.startswith(prefix + ".")
        for module in _imports()
        for prefix in forbidden
    )


def test_no_enterprise_document_repository_dependency() -> None:
    assert REPOSITORY_FILE.is_file()
    source = REPOSITORY_FILE.read_text()

    assert "EnterpriseDocumentRepository" not in source
    assert "app.document.repository" not in source


def test_no_digest_lookup_content_id_or_store() -> None:
    assert REPOSITORY_FILE.is_file()
    source = REPOSITORY_FILE.read_text()

    assert "get_by_digest" not in source
    assert "DocumentContentId" not in source
    assert "DocumentContentStore" not in source


def test_existing_domain_modules_remain_present() -> None:
    assert DOMAIN_CONTENT.is_file()
    assert DOMAIN_DOCUMENT.is_file()
