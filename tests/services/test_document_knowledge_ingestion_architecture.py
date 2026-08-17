"""RFC-065 architecture, containment and deferred-scope guardrails."""

from __future__ import annotations

import ast
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

from app.core.composition import CompositionRoot
from app.services.document_knowledge_ingestion_application_service import (
    DocumentKnowledgeIngestionApplicationService,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_APP = REPOSITORY_ROOT / "backend" / "app"

INGESTION_SERVICE = (
    BACKEND_APP
    / "services"
    / "document_knowledge_ingestion_application_service.py"
)

COMPOSITION_PACKAGE = (
    BACKEND_APP
    / "core"
    / "composition"
)

RUNTIME_FILES = (
    BACKEND_APP / "core" / "runtime.py",
    BACKEND_APP / "core" / "bootstrap.py",
    BACKEND_APP / "core" / "bootstrap_manager.py",
)

ALEMBIC_INI = REPOSITORY_ROOT / "backend" / "alembic.ini"


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    modules: set[str] = set()

    for node in ast.walk(tree):
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


def test_ingestion_service_respects_application_dependency_boundary() -> None:
    imports = _imported_modules(INGESTION_SERVICE)

    forbidden_prefixes = (
        "app.infrastructure",
        "app.core",
        "app.engines",
        "app.models",
        "sqlalchemy",
        "psycopg",
        "fastapi",
    )

    violations = sorted(
        module
        for module in imports
        if module.startswith(forbidden_prefixes)
    )

    assert violations == []


def test_ingestion_service_uses_only_accepted_peer_service_dependency() -> None:
    service_imports = {
        module
        for module in _imported_modules(INGESTION_SERVICE)
        if module.startswith("app.services")
    }

    assert service_imports == {
        "app.services.knowledge_capture_application_service",
    }


def test_default_composition_does_not_register_ingestion_service() -> None:
    platform = CompositionRoot.build()

    assert not platform.container.is_registered(
        DocumentKnowledgeIngestionApplicationService
    )

    assert not hasattr(
        platform,
        "document_knowledge_ingestion_application_service",
    )

    assert not hasattr(
        platform,
        "document_knowledge_ingestion_service",
    )


def test_default_composition_does_not_import_ingestion_boundary() -> None:
    violations: list[tuple[str, str]] = []

    for path in COMPOSITION_PACKAGE.rglob("*.py"):
        for module in _imported_modules(path):
            if module.startswith(
                "app.services."
                "document_knowledge_ingestion_application_service"
            ):
                violations.append(
                    (
                        str(path.relative_to(REPOSITORY_ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_runtime_and_bootstrap_do_not_depend_on_ingestion_boundary() -> None:
    violations: list[tuple[str, str]] = []

    for path in RUNTIME_FILES:
        for module in _imported_modules(path):
            if module.startswith(
                "app.services."
                "document_knowledge_ingestion_application_service"
            ):
                violations.append(
                    (
                        str(path.relative_to(REPOSITORY_ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_ingestion_service_owns_no_database_or_schema_runtime() -> None:
    prohibited = (
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "DATABASE_URL",
        "create_all(",
        "DeclarativeBase",
        "declarative_base(",
        "MetaData(",
        "Table(",
    )

    source = INGESTION_SERVICE.read_text()

    violations = [
        marker
        for marker in prohibited
        if marker in source
    ]

    assert violations == []


def test_ingestion_service_remains_synchronous_and_local() -> None:
    prohibited = (
        "AsyncSession",
        "async def ",
        "asyncio",
        "threading",
        "ThreadPool",
        "ProcessPool",
        "requests",
        "httpx",
        "Kafka",
        "outbox",
        "two_phase",
        "two-phase",
    )

    source = INGESTION_SERVICE.read_text()

    violations = [
        marker
        for marker in prohibited
        if marker in source
    ]

    assert violations == []


def test_rfc065_introduces_no_new_alembic_revision() -> None:
    config = Config(str(ALEMBIC_INI))
    scripts = ScriptDirectory.from_config(config)

    assert scripts.get_current_head() == "0004"
