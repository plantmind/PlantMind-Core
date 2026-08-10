"""Architecture guardrails for the RFC-053 knowledge foundation."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from app.core.composition import CompositionRoot
from app.knowledge.repository import KnowledgeRecordRepository


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_DOMAIN = PROJECT_ROOT / "backend/app/domain/knowledge.py"
KNOWLEDGE_REPOSITORY = PROJECT_ROOT / "backend/app/knowledge/repository.py"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())

    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            modules.add(node.module)

    return modules


def non_stdlib_modules(path: Path) -> set[str]:
    return {
        module
        for module in imported_modules(path)
        if module.split(".", 1)[0] not in sys.stdlib_module_names
    }


def test_canonical_knowledge_domain_depends_only_on_domain_base() -> None:
    assert non_stdlib_modules(KNOWLEDGE_DOMAIN) == {
        "app.domain.base",
    }


def test_repository_port_depends_only_on_canonical_knowledge_domain() -> None:
    assert non_stdlib_modules(KNOWLEDGE_REPOSITORY) == {
        "app.domain.base",
        "app.domain.knowledge",
    }


def test_composition_root_does_not_register_knowledge_repository() -> None:
    platform = CompositionRoot.build()

    assert not platform.container.is_registered(
        KnowledgeRecordRepository
    )


def test_platform_composition_exposes_no_knowledge_repository() -> None:
    platform = CompositionRoot.build()

    assert not hasattr(platform, "knowledge_repository")
