from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BACKEND_APP = ROOT / "backend/app"

INFRA = (
    BACKEND_APP
    / "infrastructure"
    / "document_content"
)

EXPECTED_FILES = {
    "__init__.py",
    "duplicate_classification.py",
    "mapping.py",
    "models.py",
    "repository.py",
}

CANONICAL_FILES = (
    BACKEND_APP / "domain/document_content.py",
    BACKEND_APP / "document_content/repository.py",
)


def _imports(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text())
    modules: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module is not None:
                modules.append(node.module)

        elif isinstance(node, ast.Import):
            modules.extend(
                alias.name for alias in node.names
            )

    return tuple(modules)


def test_canonical_infrastructure_package_has_exact_surface() -> None:
    assert INFRA.is_dir()

    files = {
        path.name
        for path in INFRA.iterdir()
        if path.is_file()
        and path.suffix == ".py"
    }

    assert files == EXPECTED_FILES


def test_package_initializer_is_empty() -> None:
    initializer = INFRA / "__init__.py"

    assert initializer.is_file()
    assert initializer.read_bytes() == b""


def test_domain_and_repository_port_remain_persistence_neutral() -> None:
    forbidden = (
        "sqlalchemy",
        "psycopg",
        "app.infrastructure",
        "app.services",
        "app.core",
        "fastapi",
    )

    violations: list[tuple[str, str]] = []

    for path in CANONICAL_FILES:
        for module in _imports(path):
            if module.startswith(forbidden):
                violations.append(
                    (
                        str(path.relative_to(ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_document_content_infrastructure_has_no_peer_repository_or_application_dependency() -> None:
    forbidden = (
        "app.document.repository",
        "app.knowledge.repository",
        "app.document_knowledge_lineage.repository",
        "app.services",
        "app.core",
        "app.engines",
        "fastapi",
    )

    violations: list[tuple[str, str]] = []

    for path in INFRA.glob("*.py"):
        for module in _imports(path):
            if module.startswith(forbidden):
                violations.append(
                    (
                        str(path.relative_to(ROOT)),
                        module,
                    )
                )

    assert violations == []


def test_document_content_adapter_owns_no_database_runtime_lifecycle() -> None:
    prohibited = (
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "Settings(",
        "DATABASE_URL",
        "create_all(",
    )

    violations: list[tuple[str, str]] = []

    for path in INFRA.glob("*.py"):
        source = path.read_text()

        for marker in prohibited:
            if marker in source:
                violations.append(
                    (
                        str(path.relative_to(ROOT)),
                        marker,
                    )
                )

    assert violations == []


def test_rfc069_introduces_no_binary_content_storage_contract() -> None:
    prohibited = (
        "DocumentContentStore",
        "read_bytes",
        "open_stream",
        "download_content",
        "storage_path",
        "storage_uri",
        "storage_key",
        "blob_data",
        "binary_payload",
    )

    violations: list[tuple[str, str]] = []

    for path in INFRA.glob("*.py"):
        source = path.read_text()

        for marker in prohibited:
            if marker in source:
                violations.append(
                    (
                        str(path.relative_to(ROOT)),
                        marker,
                    )
                )

    assert violations == []


def test_database_runtime_does_not_gain_document_content_ownership() -> None:
    runtime = (
        BACKEND_APP
        / "infrastructure/database/runtime.py"
    )

    assert "document_content" not in runtime.read_text()


def test_core_runtime_and_bootstrap_do_not_import_document_content_adapter() -> None:
    files = (
        BACKEND_APP / "core/runtime.py",
        BACKEND_APP / "core/bootstrap.py",
        BACKEND_APP / "core/bootstrap_manager.py",
        BACKEND_APP
        / "core/composition/composition_root.py",
    )

    violations: list[str] = []

    for path in files:
        source = path.read_text()

        if (
            "app.infrastructure.document_content"
            in source
        ):
            violations.append(
                str(path.relative_to(ROOT))
            )

    assert violations == []
