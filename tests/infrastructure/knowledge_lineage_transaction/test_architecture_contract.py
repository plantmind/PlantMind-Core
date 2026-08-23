"""RFC-064 architecture, containment and deferred-scope guardrails."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory

from app.core.composition import CompositionRoot
from app.knowledge_lineage_transaction.coordinator import (
    KnowledgeLineageTransactionCoordinator,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
BACKEND_APP = REPOSITORY_ROOT / "backend" / "app"

COORDINATOR_CONTRACT = (
    BACKEND_APP
    / "knowledge_lineage_transaction"
    / "coordinator.py"
)

TRANSACTION_INFRASTRUCTURE = (
    BACKEND_APP
    / "infrastructure"
    / "knowledge_lineage_transaction"
)

COMPOSITION_ROOT = (
    BACKEND_APP
    / "core"
    / "composition"
    / "composition_root.py"
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


def _non_stdlib_modules(path: Path) -> set[str]:
    return {
        module
        for module in _imported_modules(path)
        if module.split(".", 1)[0]
        not in sys.stdlib_module_names
    }


def test_default_composition_does_not_register_transaction_coordinator() -> None:
    platform = CompositionRoot.build()

    assert not platform.container.is_registered(
        KnowledgeLineageTransactionCoordinator
    )

    assert not hasattr(
        platform,
        "knowledge_lineage_transaction_coordinator",
    )


def test_default_composition_does_not_import_transaction_coordination() -> None:
    imports = _imported_modules(COMPOSITION_ROOT)

    assert not any(
        module.startswith(
            "app.knowledge_lineage_transaction"
        )
        or module.startswith(
            "app.infrastructure.knowledge_lineage_transaction"
        )
        for module in imports
    )


def test_runtime_and_bootstrap_do_not_depend_on_transaction_coordination() -> None:
    violations: list[tuple[str, str]] = []

    for path in RUNTIME_FILES:
        for module in _imported_modules(path):
            if (
                module.startswith(
                    "app.knowledge_lineage_transaction"
                )
                or module.startswith(
                    "app.infrastructure.knowledge_lineage_transaction"
                )
            ):
                violations.append(
                    (
                        str(path.relative_to(REPOSITORY_ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_domain_and_core_do_not_depend_on_transaction_infrastructure() -> None:
    violations: list[tuple[str, str]] = []

    roots = (
        BACKEND_APP / "domain",
        BACKEND_APP / "core",
    )

    forbidden = (
        "app.infrastructure.knowledge_lineage_transaction",
    )

    for root in roots:
        for path in root.rglob("*.py"):
            for module in _imported_modules(path):
                if module.startswith(forbidden):
                    violations.append(
                        (
                            str(path.relative_to(REPOSITORY_ROOT)),
                            module,
                        )
                    )

    assert violations == []


def test_coordinator_contract_remains_persistence_neutral() -> None:
    assert _non_stdlib_modules(
        COORDINATOR_CONTRACT
    ) == {
        "app.document_knowledge_lineage.repository",
        "app.knowledge.repository",
    }


def test_transaction_infrastructure_does_not_own_database_runtime() -> None:
    prohibited = (
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "DATABASE_URL",
        "create_all(",
    )

    violations: list[tuple[str, str]] = []

    for path in TRANSACTION_INFRASTRUCTURE.glob("*.py"):
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


def test_transaction_infrastructure_introduces_no_metadata_authority() -> None:
    prohibited = (
        "DeclarativeBase",
        "declarative_base(",
        "MetaData(",
        "Table(",
    )

    violations: list[tuple[str, str]] = []

    for path in TRANSACTION_INFRASTRUCTURE.glob("*.py"):
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


def test_transaction_infrastructure_does_not_become_application_entry_boundary() -> None:
    forbidden_prefixes = (
        "app.services",
        "app.core",
        "app.engines",
        "fastapi",
    )

    violations: list[tuple[str, str]] = []

    for path in TRANSACTION_INFRASTRUCTURE.glob("*.py"):
        for module in _imported_modules(path):
            if module.startswith(
                forbidden_prefixes
            ):
                violations.append(
                    (
                        str(path.relative_to(REPOSITORY_ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_transaction_coordination_remains_synchronous_and_local() -> None:
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

    violations: list[tuple[str, str]] = []

    paths = (
        COORDINATOR_CONTRACT,
        *TRANSACTION_INFRASTRUCTURE.glob("*.py"),
    )

    for path in paths:
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


def test_rfc064_schema_baseline_remains_in_alembic_history() -> None:
    config = Config(str(ALEMBIC_INI))
    scripts = ScriptDirectory.from_config(config)

    revision = scripts.get_revision("0004")

    assert revision is not None
    assert revision.revision == "0004"
    assert revision.down_revision == "0003"
