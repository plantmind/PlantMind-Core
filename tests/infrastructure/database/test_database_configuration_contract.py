from pathlib import Path

from app.config import Settings


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
REQUIREMENTS_FILE = REPOSITORY_ROOT / "backend" / "requirements.txt"


def test_database_url_has_no_committed_default(
    monkeypatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.DATABASE_URL is None


def test_database_url_accepts_explicit_psycopg_url() -> None:
    database_url = (
        "postgresql+psycopg://plantmind@db.internal/plantmind"
    )

    settings = Settings(
        _env_file=None,
        DATABASE_URL=database_url,
    )

    assert settings.DATABASE_URL == database_url


def test_database_foundation_dependencies_are_declared() -> None:
    requirement_names = {
        line.split("==", 1)[0]
        .split("[", 1)[0]
        .strip()
        .lower()
        for line in REQUIREMENTS_FILE.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }

    assert {
        "sqlalchemy",
        "alembic",
        "psycopg",
    } <= requirement_names
