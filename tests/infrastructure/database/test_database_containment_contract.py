from pathlib import Path

from app.infrastructure.database import DatabaseRuntime


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
BACKEND_APP = REPOSITORY_ROOT / "backend" / "app"

VALID_DATABASE_URL = (
    "postgresql+psycopg://plantmind@db.internal/plantmind"
)


def test_database_runtime_does_not_auto_commit() -> None:
    runtime = DatabaseRuntime(VALID_DATABASE_URL)

    class FakeSession:
        def __init__(self) -> None:
            self.commit_calls = 0

        def commit(self) -> None:
            self.commit_calls += 1

    session = FakeSession()
    runtime._session_factory = lambda: session

    try:
        created = runtime.create_session()

        assert created is session
        assert session.commit_calls == 0
    finally:
        runtime.dispose()


def test_platform_startup_has_no_database_lifecycle_coupling() -> None:
    startup_files = (
        BACKEND_APP / "main.py",
        BACKEND_APP / "core" / "bootstrap.py",
        BACKEND_APP / "core" / "bootstrap_manager.py",
        BACKEND_APP
        / "core"
        / "composition"
        / "composition_root.py",
        BACKEND_APP / "core" / "runtime.py",
    )

    prohibited = (
        "DatabaseRuntime",
        "DatabaseBase",
        "alembic",
        "create_all",
        "run_migrations",
    )

    violations = []

    for path in startup_files:
        source = path.read_text()

        for marker in prohibited:
            if marker in source:
                violations.append(
                    f"{path.relative_to(REPOSITORY_ROOT)}: {marker}"
                )

    assert violations == []


def test_rfc054_database_foundation_remains_knowledge_neutral() -> None:
    database_infrastructure = (
        BACKEND_APP / "infrastructure" / "database"
    )
    composition_root = (
        BACKEND_APP
        / "core"
        / "composition"
        / "composition_root.py"
    )

    sources = [
        path.read_text()
        for path in database_infrastructure.rglob("*.py")
    ]
    sources.append(composition_root.read_text())

    combined = "\n".join(sources)

    assert "KnowledgeRecordRepository" not in combined
    assert "KnowledgeRecord" not in combined
