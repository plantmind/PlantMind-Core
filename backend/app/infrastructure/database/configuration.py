"""Canonical PlantMind database configuration validation."""

from __future__ import annotations

from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError


def validate_database_url(database_url: str | None) -> str:
    """Validate and normalize the canonical PostgreSQL database URL."""

    if not isinstance(database_url, str) or not database_url.strip():
        raise ValueError("Database URL is required.")

    normalized_url = database_url.strip()

    try:
        parsed_url = make_url(normalized_url)
    except ArgumentError:
        raise ValueError("Database URL is invalid.") from None

    if parsed_url.drivername != "postgresql+psycopg":
        raise ValueError(
            "Database URL must use the postgresql+psycopg driver."
        )

    return normalized_url
