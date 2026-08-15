"""RFC-063 relational lineage architecture and scope guardrails."""

from __future__ import annotations

import ast
from pathlib import Path

from app.infrastructure.database.metadata import DatabaseBase
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
BACKEND_APP = REPOSITORY_ROOT / "backend" / "app"

LINEAGE_INFRASTRUCTURE = (
    BACKEND_APP
    / "infrastructure"
    / "document_knowledge_lineage"
)

CANONICAL_FILES = (
    BACKEND_APP / "domain" / "document_knowledge_lineage.py",
    BACKEND_APP / "document_knowledge_lineage" / "repository.py",
)


def _imported_modules(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text())
    modules: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module is not None:
                modules.append(node.module)

        elif isinstance(node, ast.Import):
            modules.extend(
                alias.name
                for alias in node.names
            )

    return tuple(modules)


def test_canonical_lineage_domain_and_port_remain_persistence_neutral() -> None:
    forbidden_prefixes = (
        "sqlalchemy",
        "psycopg",
        "app.infrastructure",
        "app.services",
        "app.core",
        "fastapi",
    )

    violations: list[tuple[str, str]] = []

    for path in CANONICAL_FILES:
        for module in _imported_modules(path):
            if module.startswith(forbidden_prefixes):
                violations.append(
                    (
                        str(path.relative_to(REPOSITORY_ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_lineage_infrastructure_does_not_reach_peer_or_application_boundaries() -> None:
    forbidden_prefixes = (
        "app.document.repository",
        "app.knowledge.repository",
        "app.services",
        "app.core",
        "app.engines",
        "fastapi",
    )

    violations: list[tuple[str, str]] = []

    for path in LINEAGE_INFRASTRUCTURE.glob("*.py"):
        for module in _imported_modules(path):
            if module.startswith(forbidden_prefixes):
                violations.append(
                    (
                        str(path.relative_to(REPOSITORY_ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_no_other_application_module_imports_lineage_relational_adapter() -> None:
    violations: list[str] = []

    for path in BACKEND_APP.rglob("*.py"):
        if LINEAGE_INFRASTRUCTURE in path.parents:
            continue

        for module in _imported_modules(path):
            if module.startswith(
                "app.infrastructure.document_knowledge_lineage"
            ):
                violations.append(
                    str(path.relative_to(REPOSITORY_ROOT))
                )

    assert violations == []


def test_lineage_relational_adapter_owns_no_runtime_or_engine_lifecycle() -> None:
    prohibited = (
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "Settings(",
        "DATABASE_URL",
        "create_all(",
        "KnowledgeCaptureApplicationService",
        "EnterpriseDocumentRegistrationApplicationService",
    )

    violations: list[tuple[str, str]] = []

    for path in LINEAGE_INFRASTRUCTURE.glob("*.py"):
        source = path.read_text()

        for marker in prohibited:
            if marker in source:
                violations.append(
                    (
                        str(path.relative_to(REPOSITORY_ROOT)),
                        marker,
                    )
                )

    assert violations == []


def test_lineage_row_uses_only_canonical_metadata_and_no_foreign_keys() -> None:
    table = DocumentKnowledgeLineageRow.__table__

    assert table.metadata is DatabaseBase.metadata
    assert tuple(table.columns.keys()) == (
        "document_id",
        "knowledge_record_id",
    )
    assert not table.foreign_keys


def test_lineage_infrastructure_package_initializer_remains_empty() -> None:
    initializer = (
        LINEAGE_INFRASTRUCTURE
        / "__init__.py"
    )

    assert initializer.read_text() == ""
