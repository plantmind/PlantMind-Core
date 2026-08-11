import pytest

from app.infrastructure.database.configuration import (
    validate_database_url,
)


CANONICAL_URL = (
    "postgresql+psycopg://plantmind@db.internal/plantmind"
)


def test_database_url_validator_accepts_canonical_url() -> None:
    assert validate_database_url(CANONICAL_URL) == CANONICAL_URL


@pytest.mark.parametrize(
    "database_url",
    (
        None,
        "",
        "   ",
        "postgresql://plantmind@db.internal/plantmind",
        "sqlite:///plantmind.db",
    ),
)
def test_database_url_validator_rejects_noncanonical_configuration(
    database_url,
) -> None:
    with pytest.raises(ValueError):
        validate_database_url(database_url)


def test_database_url_validation_does_not_expose_credentials() -> None:
    database_url = (
        "postgresql://plantmind:super-secret@db.internal/plantmind"
    )

    with pytest.raises(ValueError) as exc_info:
        validate_database_url(database_url)

    message = str(exc_info.value)

    assert "super-secret" not in message
    assert database_url not in message
