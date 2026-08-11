import pytest

from app.infrastructure.database import DatabaseRuntime


VALID_DATABASE_URL = (
    "postgresql+psycopg://plantmind@db.internal/plantmind"
)


def test_database_runtime_requires_database_url() -> None:
    with pytest.raises(ValueError):
        DatabaseRuntime("")


def test_database_runtime_rejects_non_psycopg_url() -> None:
    with pytest.raises(ValueError):
        DatabaseRuntime(
            "postgresql://plantmind@db.internal/plantmind"
        )


def test_database_runtime_rejects_non_postgresql_url() -> None:
    with pytest.raises(ValueError):
        DatabaseRuntime("sqlite:///plantmind.db")


def test_database_runtime_constructs_explicitly() -> None:
    runtime = DatabaseRuntime(VALID_DATABASE_URL)

    assert runtime.engine is not None
    assert runtime.session_factory is not None

    runtime.dispose()


def test_database_runtime_instances_own_distinct_engines() -> None:
    first = DatabaseRuntime(VALID_DATABASE_URL)
    second = DatabaseRuntime(VALID_DATABASE_URL)

    try:
        assert first.engine is not second.engine
        assert first.session_factory is not second.session_factory
    finally:
        first.dispose()
        second.dispose()


def test_database_runtime_creates_independent_sessions() -> None:
    runtime = DatabaseRuntime(VALID_DATABASE_URL)

    first = runtime.create_session()
    second = runtime.create_session()

    try:
        assert first is not second
    finally:
        first.close()
        second.close()
        runtime.dispose()


def test_database_runtime_dispose_is_explicit() -> None:
    runtime = DatabaseRuntime(VALID_DATABASE_URL)

    result = runtime.dispose()

    assert result is None
