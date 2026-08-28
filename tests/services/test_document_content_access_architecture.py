"""RFC-073 architecture and containment guardrails."""

from __future__ import annotations

import ast
import inspect
import sys
from contextlib import AbstractContextManager
from dataclasses import fields
from pathlib import Path
from typing import get_type_hints

from alembic.config import Config
from alembic.script import ScriptDirectory

from app.document.repository import EnterpriseDocumentRepository
from app.document_content.repository import DocumentContentRepository
from app.document_content.store import DocumentContentStore
from app.domain.document_content import DocumentContentDescriptor
from app.services.document_content_access_application_service import (
    DocumentContentAccess,
    DocumentContentAccessApplicationService,
    DocumentContentAccessContentNotFoundError,
    DocumentContentAccessDocumentNotFoundError,
    DocumentContentAccessIntegrityError,
    DocumentContentAccessRequest,
)


ROOT = Path(__file__).resolve().parents[2]
BACKEND_APP = ROOT / "backend" / "app"

SERVICE = (
    BACKEND_APP
    / "services"
    / "document_content_access_application_service.py"
)

ALEMBIC_INI = ROOT / "backend" / "alembic.ini"

EXPECTED_PUBLIC_CLASSES = {
    "DocumentContentAccessRequest",
    "DocumentContentAccess",
    "DocumentContentAccessDocumentNotFoundError",
    "DocumentContentAccessContentNotFoundError",
    "DocumentContentAccessIntegrityError",
    "DocumentContentAccessApplicationService",
}


def _tree() -> ast.Module:
    assert SERVICE.is_file()

    return ast.parse(
        SERVICE.read_text()
    )


def _imports() -> set[str]:
    modules: set[str] = set()

    for node in ast.walk(
        _tree()
    ):
        if isinstance(
            node,
            ast.Import,
        ):
            modules.update(
                alias.name
                for alias in node.names
            )

        elif (
            isinstance(
                node,
                ast.ImportFrom,
            )
            and node.module is not None
        ):
            modules.add(
                node.module
            )

    return modules


def _non_stdlib_imports() -> set[str]:
    return {
        module
        for module in _imports()
        if module.split(
            ".",
            1,
        )[0]
        not in sys.stdlib_module_names
    }


def test_rfc073_service_file_exists_at_accepted_boundary() -> None:
    assert SERVICE.is_file()


def test_rfc073_public_class_surface_is_exact() -> None:
    module = __import__(
        "app.services."
        "document_content_access_application_service",
        fromlist=["*"],
    )

    public_classes = {
        name
        for name, value in vars(
            module
        ).items()
        if inspect.isclass(value)
        and value.__module__ == module.__name__
        and not name.startswith("_")
    }

    assert public_classes == EXPECTED_PUBLIC_CLASSES

    assert DocumentContentAccessApplicationService is not None
    assert DocumentContentAccessDocumentNotFoundError is not None
    assert DocumentContentAccessContentNotFoundError is not None
    assert DocumentContentAccessIntegrityError is not None


def test_request_and_access_field_surfaces_are_exact() -> None:
    assert [
        field.name
        for field in fields(
            DocumentContentAccessRequest
        )
    ] == [
        "document_id",
    ]

    assert [
        field.name
        for field in fields(
            DocumentContentAccess
        )
    ] == [
        "descriptor",
        "payload",
    ]


def test_service_constructor_depends_exactly_on_three_ports() -> None:
    signature = inspect.signature(
        DocumentContentAccessApplicationService.__init__
    )

    hints = get_type_hints(
        DocumentContentAccessApplicationService.__init__
    )

    assert tuple(
        signature.parameters
    ) == (
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

    assert all(
        parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
        for parameter in list(
            signature.parameters.values()
        )[1:]
    )


def test_open_contract_is_exact_context_managed_access() -> None:
    hints = get_type_hints(
        DocumentContentAccessApplicationService.open
    )

    assert (
        hints["request"]
        is DocumentContentAccessRequest
    )

    assert (
        hints["return"]
        == AbstractContextManager[
            DocumentContentAccess
        ]
    )


def test_access_descriptor_type_is_exact() -> None:
    hints = get_type_hints(
        DocumentContentAccess
    )

    assert (
        hints["descriptor"]
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
        or module.startswith(
            prefix + "."
        )
        for module in _imports()
        for prefix in forbidden_prefixes
    )


def test_service_is_read_only_and_has_no_unaccepted_capabilities() -> None:
    tree = _tree()
    source = SERVICE.read_text()

    forbidden_words = (
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
        "FilesystemDocumentContentStore",
        "KnowledgeLineageTransactionCoordinator",
        "DatabaseRuntime",
        "CompositionRoot",
    )

    assert [
        marker
        for marker in forbidden_words
        if marker in source
    ] == []

    repository_attributes = {
        "_document_repository",
        "_content_repository",
        "_content_store",
    }

    forbidden_write_methods = {
        "add",
        "update",
        "delete",
        "replace",
        "upsert",
    }

    violating_dependency_calls: list[str] = []

    for node in ast.walk(
        tree
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        if not isinstance(
            node.func,
            ast.Attribute,
        ):
            continue

        method_name = node.func.attr
        owner = node.func.value

        if method_name not in forbidden_write_methods:
            continue

        if not isinstance(
            owner,
            ast.Attribute,
        ):
            continue

        if not isinstance(
            owner.value,
            ast.Name,
        ):
            continue

        if owner.value.id != "self":
            continue

        if owner.attr not in repository_attributes:
            continue

        violating_dependency_calls.append(
            f"{owner.attr}.{method_name}"
        )

    assert violating_dependency_calls == []

    assert "retry" not in source.lower()


def test_hash_digest_update_is_not_misclassified_as_persistence_write() -> None:
    tree = _tree()

    digest_update_calls = [
        node
        for node in ast.walk(
            tree
        )
        if isinstance(
            node,
            ast.Call,
        )
        and isinstance(
            node.func,
            ast.Attribute,
        )
        and node.func.attr == "update"
        and isinstance(
            node.func.value,
            ast.Name,
        )
        and node.func.value.id == "digest"
    ]

    assert len(
        digest_update_calls
    ) == 1


def test_default_runtime_and_composition_do_not_import_rfc073_service() -> None:
    files = [
        *(
            BACKEND_APP
            / "core"
            / "composition"
        ).rglob("*.py"),
        BACKEND_APP
        / "core"
        / "runtime.py",
        BACKEND_APP
        / "core"
        / "bootstrap.py",
        BACKEND_APP
        / "core"
        / "bootstrap_manager.py",
    ]

    marker = (
        "app.services."
        "document_content_access_application_service"
    )

    violations = [
        str(
            path.relative_to(
                ROOT
            )
        )
        for path in files
        if path.is_file()
        and marker
        in path.read_text()
    ]

    assert violations == []


def test_services_package_does_not_reexport_rfc073_surface() -> None:
    initializer = (
        BACKEND_APP
        / "services"
        / "__init__.py"
    )

    if initializer.exists():
        source = initializer.read_text()

        assert (
            "DocumentContentAccess"
            not in source
        )


def test_canonical_alembic_head_remains_0005() -> None:
    config = Config(
        str(
            ALEMBIC_INI
        )
    )

    scripts = ScriptDirectory.from_config(
        config
    )

    assert (
        scripts.get_current_head()
        == "0005"
    )
