"""Alembic environment for PlantMind relational schema migrations."""

from __future__ import annotations

from alembic import context

from app.config import Settings
from app.infrastructure.database import DatabaseRuntime
from app.infrastructure.database.configuration import (
    validate_database_url,
)
from app.infrastructure.database.metadata import DatabaseBase
from app.infrastructure.knowledge.models import (
    KnowledgeRecordRow as _KnowledgeRecordRow,
)
from app.infrastructure.document.models import (
    EnterpriseDocumentRow as _EnterpriseDocumentRow,
)


target_metadata = DatabaseBase.metadata


def _database_url() -> str:
    database_url = Settings().DATABASE_URL

    return validate_database_url(database_url)


def run_migrations_offline() -> None:
    """Run migrations without establishing a database connection."""

    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations through the canonical database runtime."""

    runtime = DatabaseRuntime(_database_url())

    try:
        with runtime.engine.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        runtime.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
