"""RFC-064 persistence-neutral transaction coordinator contract tests."""

from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageRepository,
)
from app.knowledge.repository import KnowledgeRecordRepository
from app.knowledge_lineage_transaction.coordinator import (
    KnowledgeLineageTransactionCoordinator,
    KnowledgeLineageTransactionPostCommitCleanupError,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

COORDINATOR_MODULE = (
    PROJECT_ROOT
    / "backend/app/knowledge_lineage_transaction/coordinator.py"
)

PACKAGE_INITIALIZER = (
    PROJECT_ROOT
    / "backend/app/knowledge_lineage_transaction/__init__.py"
)


def _non_stdlib_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            modules.add(node.module)

    return {
        module
        for module in modules
        if module.split(".", 1)[0] not in sys.stdlib_module_names
    }


def test_coordinator_is_abstract_persistence_neutral_contract() -> None:
    assert inspect.isabstract(
        KnowledgeLineageTransactionCoordinator
    )

    method = (
        KnowledgeLineageTransactionCoordinator
        .__dict__["execute"]
    )

    assert getattr(method, "__isabstractmethod__", False)

    signature = inspect.signature(method)

    assert tuple(signature.parameters) == (
        "self",
        "operation",
    )


def test_coordinator_contract_depends_only_on_repository_ports() -> None:
    assert _non_stdlib_modules(COORDINATOR_MODULE) == {
        "app.document_knowledge_lineage.repository",
        "app.knowledge.repository",
    }


def test_post_commit_cleanup_error_is_persistence_neutral() -> None:
    assert issubclass(
        KnowledgeLineageTransactionPostCommitCleanupError,
        Exception,
    )


def test_repository_ports_remain_the_coordinator_dependencies() -> None:
    annotations = inspect.get_annotations(
        KnowledgeLineageTransactionCoordinator.execute,
        eval_str=False,
    )

    rendered = " ".join(
        str(value)
        for value in annotations.values()
    )

    assert "KnowledgeRecordRepository" in rendered
    assert "DocumentKnowledgeLineageRepository" in rendered


def test_transaction_package_initializer_remains_empty() -> None:
    assert PACKAGE_INITIALIZER.read_text().strip() == ""
