"""RFC-072 architecture and containment guardrails."""

from __future__ import annotations

import ast
import inspect
import sys
from dataclasses import fields
from pathlib import Path
from typing import get_type_hints

from alembic.config import Config
from alembic.script import ScriptDirectory

from app.document.repository import EnterpriseDocumentRepository
from app.document_content.repository import DocumentContentRepository
from app.document_content.store import DocumentContentStore
from app.domain.document_content import DocumentContentDescriptor
from app.services.document_content_establishment_application_service import (
    DocumentContentEstablishmentApplicationService,
    DocumentContentEstablishmentConflictError,
    DocumentContentEstablishmentDocumentNotFoundError,
    DocumentContentEstablishmentIntegrityError,
    DocumentContentEstablishmentRequest,
)


ROOT = Path(__file__).resolve().parents[2]
BACKEND_APP = ROOT / "backend" / "app"
SERVICE = (
    BACKEND_APP
    / "services"
    / "document_content_establishment_application_service.py"
)
ALEMBIC_INI = ROOT / "backend" / "alembic.ini"

EXPECTED_PUBLIC_CLASSES = {
    "DocumentContentEstablishmentRequest",
    "DocumentContentEstablishmentDocumentNotFoundError",
    "DocumentContentEstablishmentConflictError",
    "DocumentContentEstablishmentIntegrityError",
    "DocumentContentEstablishmentApplicationService",
}


def _tree() -> ast.Module:
    assert SERVICE.is_file()

    return ast.parse(
        SERVICE.read_text()
    )


def _imports() -> set[str]:
    modules: set[str] = set()

    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            modules.update(
                alias.name
                for alias in node.names
            )
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
        ):
            modules.add(node.module)

    return modules


def _non_stdlib_imports() -> set[str]:
    return {
        module
        for module in _imports()
        if module.split(".", 1)[0]
        not in sys.stdlib_module_names
    }


def test_rfc072_service_file_exists_at_accepted_module_boundary() -> None:
    assert SERVICE.is_file()


def test_rfc072_public_class_surface_is_exact() -> None:
    module = __import__(
        "app.services."
        "document_content_establishment_application_service",
        fromlist=["*"],
    )

    public_classes = {
        name
        for name, value in vars(module).items()
        if inspect.isclass(value)
        and value.__module__ == module.__name__
        and not name.startswith("_")
    }

    assert public_classes == EXPECTED_PUBLIC_CLASSES

    assert DocumentContentEstablishmentApplicationService is not None
    assert DocumentContentEstablishmentDocumentNotFoundError is not None
    assert DocumentContentEstablishmentConflictError is not None
    assert DocumentContentEstablishmentIntegrityError is not None


def test_request_field_surface_is_exact() -> None:
    assert [
        field.name
        for field in fields(
            DocumentContentEstablishmentRequest
        )
    ] == [
        "document_id",
        "media_type",
        "source",
    ]


def test_service_constructor_depends_exactly_on_three_ports() -> None:
    signature = inspect.signature(
        DocumentContentEstablishmentApplicationService.__init__
    )

    hints = get_type_hints(
        DocumentContentEstablishmentApplicationService.__init__
    )

    assert tuple(signature.parameters) == (
        "self",
        "document_repository",
        "content_repository",
        "content_store",
    )

    assert (
        hints["document_repository"]
        is EnterpriseDocumentRepository
    )
    assert (
        hints["content_repository"]
        is DocumentContentRepository
    )
    assert (
        hints["content_store"]
        is DocumentContentStore
    )


def test_establish_return_contract_is_descriptor() -> None:
    hints = get_type_hints(
        DocumentContentEstablishmentApplicationService.establish
    )

    assert (
        hints["request"]
        is DocumentContentEstablishmentRequest
    )
    assert (
        hints["return"]
        is DocumentContentDescriptor
    )


def test_service_nonstdlib_dependencies_are_exactly_persistence_neutral() -> None:
    assert _non_stdlib_imports() == {
        "app.document.repository",
        "app.document_content.repository",
        "app.document_content.store",
        "app.domain.base",
        "app.domain.document_content",
    }


def test_service_has_no_forbidden_infrastructure_or_runtime_dependencies() -> None:
    forbidden_prefixes = (
        "app.infrastructure",
        "app.core",
        "app.engines",
        "app.models",
        "sqlalchemy",
        "psycopg",
        "fastapi",
        "pydantic",
    )

    assert not any(
        module == prefix
        or module.startswith(prefix + ".")
        for module in _imports()
        for prefix in forbidden_prefixes
    )


def test_service_does_not_depend_on_concrete_filesystem_store_or_transaction_coordinator() -> None:
    source = SERVICE.read_text()

    forbidden = (
        "FilesystemDocumentContentStore",
        "KnowledgeLineageTransactionCoordinator",
        "SQLAlchemy",
        "DatabaseRuntime",
        "CompositionRoot",
        "ServiceContainer",
        "PlatformComposition",
        "ApplicationFacade",
    )

    assert [
        marker
        for marker in forbidden
        if marker in source
    ] == []


def test_service_does_not_interpret_source_reference_or_add_unaccepted_capabilities() -> None:
    source = SERVICE.read_text()

    forbidden = (
        "source_reference",
        "OCR",
        "parser",
        "chunking",
        "embedding",
        "Qdrant",
        "Neo4j",
        "RAG",
        "LLM",
        "RBAC",
        "Active Directory",
    )

    assert [
        marker
        for marker in forbidden
        if marker in source
    ] == []


def test_service_introduces_no_delete_replace_upsert_or_automatic_retry() -> None:
    source = SERVICE.read_text()

    forbidden_calls = (
        ".delete(",
        ".replace(",
        ".upsert(",
    )

    assert [
        marker
        for marker in forbidden_calls
        if marker in source
    ] == []

    assert "retry" not in source.lower()


def test_default_composition_and_runtime_do_not_import_rfc072_service() -> None:
    files = [
        *(
            BACKEND_APP
            / "core"
            / "composition"
        ).rglob("*.py"),
        BACKEND_APP / "core" / "runtime.py",
        BACKEND_APP / "core" / "bootstrap.py",
        BACKEND_APP / "core" / "bootstrap_manager.py",
    ]

    marker = (
        "app.services."
        "document_content_establishment_application_service"
    )

    violations = [
        str(path.relative_to(ROOT))
        for path in files
        if path.is_file()
        and marker in path.read_text()
    ]

    assert violations == []


def test_no_services_package_reexport_is_required() -> None:
    initializer = (
        BACKEND_APP
        / "services"
        / "__init__.py"
    )

    if initializer.exists():
        assert (
            "DocumentContentEstablishment"
            not in initializer.read_text()
        )


def test_canonical_alembic_head_remains_0005() -> None:
    config = Config(
        str(ALEMBIC_INI)
    )

    scripts = ScriptDirectory.from_config(
        config
    )

    assert scripts.get_current_head() == "0005"
