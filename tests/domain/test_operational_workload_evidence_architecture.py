"""RFC-067 operational workload evidence architecture guardrails."""

from __future__ import annotations

import ast
import importlib
import importlib.util
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

CANONICAL_MODULE = "app.domain.operational_workload_evidence"
LEGACY_MODULE = "app.services.orchestration.workload_evidence"

CANONICAL_PATH = (
    REPOSITORY_ROOT
    / "backend/app/domain/operational_workload_evidence.py"
)

LEGACY_PATH = (
    REPOSITORY_ROOT
    / "backend/app/services/orchestration/workload_evidence.py"
)

DOMAIN_EVIDENCE_PATH = (
    REPOSITORY_ROOT
    / "backend/app/domain/evidence.py"
)

CONTRACT_NAMES = (
    "ApplicationFacadeEntryEvidence",
    "WorkflowExecutionStartEvidence",
    "OperationalWorkloadEvidence",
)

NON_TEST_CONSUMERS = (
    REPOSITORY_ROOT
    / "backend/app/core/operational_transition_coordinator.py",
    REPOSITORY_ROOT
    / "backend/app/core/operational_transition_evidence.py",
    REPOSITORY_ROOT
    / "backend/app/services/application_facade.py",
    REPOSITORY_ROOT
    / "backend/app/services/integration_gateway.py",
    REPOSITORY_ROOT
    / "backend/app/services/orchestration/orchestration_service.py",
    REPOSITORY_ROOT
    / "backend/app/services/orchestration/workflow.py",
    REPOSITORY_ROOT
    / "backend/app/services/orchestration/workflow_executor.py",
)


def _tree(path: Path) -> ast.AST:
    return ast.parse(path.read_text())


def _class_names(path: Path) -> tuple[str, ...]:
    return tuple(
        node.name
        for node in _tree(path).body
        if isinstance(node, ast.ClassDef)
    )


def _import_from_modules(path: Path) -> set[str]:
    return {
        node.module
        for node in ast.walk(_tree(path))
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    }


def test_canonical_operational_workload_evidence_domain_module_exists() -> None:
    assert importlib.util.find_spec(CANONICAL_MODULE) is not None


def test_canonical_domain_module_owns_exact_contract_definitions() -> None:
    assert _class_names(CANONICAL_PATH) == CONTRACT_NAMES


def test_canonical_domain_module_is_dependency_light() -> None:
    assert _import_from_modules(CANONICAL_PATH) <= {
        "__future__",
        "dataclasses",
        "uuid",
    }


def test_legacy_module_defines_no_contract_classes() -> None:
    assert _class_names(LEGACY_PATH) == ()


def test_legacy_imports_are_exact_canonical_class_objects() -> None:
    canonical = importlib.import_module(CANONICAL_MODULE)
    legacy = importlib.import_module(LEGACY_MODULE)

    for name in CONTRACT_NAMES:
        assert getattr(legacy, name) is getattr(canonical, name)


def test_contract_classes_have_exactly_one_backend_definition() -> None:
    definitions: dict[str, list[Path]] = {
        name: []
        for name in CONTRACT_NAMES
    }

    for path in (REPOSITORY_ROOT / "backend/app").rglob("*.py"):
        for class_name in _class_names(path):
            if class_name in definitions:
                definitions[class_name].append(path)

    for name in CONTRACT_NAMES:
        assert definitions[name] == [CANONICAL_PATH]


def test_core_does_not_import_operational_workload_evidence_from_services() -> None:
    core_consumers = NON_TEST_CONSUMERS[:2]

    offenders = tuple(
        str(path.relative_to(REPOSITORY_ROOT))
        for path in core_consumers
        if LEGACY_MODULE in _import_from_modules(path)
    )

    assert offenders == ()


def test_all_maintained_non_test_consumers_use_canonical_domain_import() -> None:
    for path in NON_TEST_CONSUMERS:
        imports = _import_from_modules(path)

        assert CANONICAL_MODULE in imports
        assert LEGACY_MODULE not in imports


def test_no_backend_consumer_uses_legacy_import_path() -> None:
    offenders = []

    for path in (REPOSITORY_ROOT / "backend/app").rglob("*.py"):
        if path == LEGACY_PATH:
            continue

        if LEGACY_MODULE in _import_from_modules(path):
            offenders.append(
                str(path.relative_to(REPOSITORY_ROOT))
            )

    assert offenders == []


def test_existing_domain_evidence_remains_a_separate_concept() -> None:
    assert not any(
        name in _class_names(DOMAIN_EVIDENCE_PATH)
        for name in CONTRACT_NAMES
    )

    imports = _import_from_modules(DOMAIN_EVIDENCE_PATH)

    assert CANONICAL_MODULE not in imports
    assert LEGACY_MODULE not in imports
