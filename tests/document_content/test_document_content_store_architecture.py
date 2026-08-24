"""RFC-070 binary Document Content store architecture guardrails."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "backend/app/document_content"
STORE_FILE = PACKAGE / "store.py"
REPOSITORY_FILE = PACKAGE / "repository.py"
DOMAIN_CONTENT = ROOT / "backend/app/domain/document_content.py"

ALLOWED_IMPORTS = {
    "__future__",
    "abc",
    "contextlib",
    "typing",
    "app.domain.base",
}

FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "alembic",
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
    "boto",
    "botocore",
    "app.infrastructure",
    "app.services",
    "app.core",
    "app.document.repository",
    "app.document_content.repository",
    "app.domain.document",
    "app.domain.document_content",
)


def _tree() -> ast.Module:
    assert STORE_FILE.is_file(), (
        "RFC-070 requires "
        "backend/app/document_content/store.py"
    )
    return ast.parse(STORE_FILE.read_text())


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


def test_store_file_is_separate_from_repository() -> None:
    assert STORE_FILE.is_file()
    assert REPOSITORY_FILE.is_file()
    assert STORE_FILE != REPOSITORY_FILE


def test_store_dependencies_are_exactly_persistence_neutral() -> None:
    imports = _imports()

    assert imports <= ALLOWED_IMPORTS

    assert not any(
        module == prefix
        or module.startswith(prefix + ".")
        for module in imports
        for prefix in FORBIDDEN_IMPORT_PREFIXES
    )


def test_store_does_not_own_descriptor_contract() -> None:
    source = STORE_FILE.read_text()

    forbidden = (
        "DocumentContentDescriptor",
        "DocumentContentMediaType",
        "DocumentContentDigest",
        "DocumentSource",
        "byte_length",
        "media_type",
        "digest",
    )

    assert [
        marker
        for marker in forbidden
        if marker in source
    ] == []


def test_store_has_no_repository_dependency() -> None:
    source = STORE_FILE.read_text()

    forbidden = (
        "DocumentContentRepository",
        "EnterpriseDocumentRepository",
        "KnowledgeRepository",
        "LineageRepository",
    )

    assert [
        marker
        for marker in forbidden
        if marker in source
    ] == []


def test_store_selects_no_storage_technology() -> None:
    source = STORE_FILE.read_text().lower()

    forbidden = (
        "sqlalchemy",
        "alembic",
        "postgres",
        "blob",
        "largeobject",
        "filesystem",
        "pathlib",
        "boto",
        "s3",
        "bucket",
        "storage_path",
        "storage_uri",
        "storage_key",
    )

    assert [
        marker
        for marker in forbidden
        if marker in source
    ] == []


def test_domain_document_content_remains_unchanged_owner() -> None:
    source = DOMAIN_CONTENT.read_text()

    assert "DocumentContentStore" not in source
    assert "DocumentContentPayloadAlreadyExistsError" not in source


def test_repository_remains_descriptor_only() -> None:
    source = REPOSITORY_FILE.read_text()

    assert "DocumentContentStore" not in source
    assert "DocumentContentPayloadAlreadyExistsError" not in source
    assert "BinaryIO" not in source
    assert "AbstractContextManager" not in source


def test_store_contains_no_runtime_or_application_wiring() -> None:
    source = STORE_FILE.read_text()

    prohibited = (
        "DatabaseRuntime",
        "CompositionRoot",
        "ServiceContainer",
        "PlatformComposition",
        "ApplicationFacade",
        "FastAPI",
        "APIRouter",
        "sessionmaker",
        "create_engine",
    )

    assert [
        marker
        for marker in prohibited
        if marker in source
    ] == []
