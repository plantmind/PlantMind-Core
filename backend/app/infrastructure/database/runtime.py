"""Canonical PlantMind relational database runtime."""

from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.database.configuration import (
    validate_database_url,
)


class DatabaseRuntime:
    """Own the canonical SQLAlchemy engine and session factory."""

    def __init__(self, database_url: str) -> None:
        normalized_url = validate_database_url(database_url)

        self._engine: Engine = create_engine(normalized_url)
        self._session_factory = sessionmaker(
            bind=self._engine,
            autoflush=False,
        )

    @property
    def engine(self) -> Engine:
        """Return the engine owned by this database runtime."""
        return self._engine

    @property
    def session_factory(self) -> sessionmaker[Session]:
        """Return the session factory owned by this database runtime."""
        return self._session_factory

    def create_session(self) -> Session:
        """Create an independent SQLAlchemy session."""
        return self._session_factory()

    def dispose(self) -> None:
        """Dispose engine-owned database resources explicitly."""
        self._engine.dispose()
