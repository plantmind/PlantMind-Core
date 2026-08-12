from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
from types import ModuleType

import sqlalchemy as sa
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects import postgresql

from app.infrastructure.database.metadata import DatabaseBase
from app.infrastructure.knowledge import models as _knowledge_models


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

ALEMBIC_INI = REPOSITORY_ROOT / "backend" / "alembic.ini"
MIGRATIONS = REPOSITORY_ROOT / "backend" / "migrations"
MIGRATION_0002 = (
    MIGRATIONS
    / "versions"
    / "0002_knowledge_records.py"
)
ALEMBIC_ENV = MIGRATIONS / "env.py"


def _load_revision() -> ModuleType:
    assert MIGRATION_0002.is_file()

    spec = importlib.util.spec_from_file_location(
        "plantmind_migration_0002",
        MIGRATION_0002,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def _compiled_type(column: sa.Column) -> str:
    return str(
        column.type.compile(
            dialect=postgresql.dialect()
        )
    )


def _normalized_check_constraints(
    table: sa.Table,
) -> dict[str | None, str]:
    return {
        constraint.name: " ".join(
            str(constraint.sqltext).split()
        )
        for constraint in table.constraints
        if isinstance(constraint, CheckConstraint)
    }


def test_revision_0002_extends_database_foundation_linearly() -> None:
    revision = _load_revision()

    assert revision.revision == "0002"
    assert revision.down_revision == "0001"
    assert revision.branch_labels is None
    assert revision.depends_on is None


def test_revision_0002_is_the_only_alembic_head() -> None:
    configuration = Config(str(ALEMBIC_INI))
    scripts = ScriptDirectory.from_config(configuration)

    assert scripts.get_heads() == ["0002"]


def test_revision_0002_schema_matches_canonical_knowledge_metadata(
    monkeypatch,
) -> None:
    revision = _load_revision()

    captured: dict[str, sa.Table] = {}

    def capture_create_table(
        table_name: str,
        *schema_items,
        **kwargs,
    ) -> sa.Table:
        table = sa.Table(
            table_name,
            sa.MetaData(),
            *schema_items,
        )
        captured["table"] = table
        return table

    monkeypatch.setattr(
        revision.op,
        "create_table",
        capture_create_table,
    )

    revision.upgrade()

    assert set(captured) == {"table"}

    migration_table = captured["table"]
    mapped_table = DatabaseBase.metadata.tables[
        "knowledge_records"
    ]

    assert migration_table.name == "knowledge_records"

    assert tuple(migration_table.c.keys()) == tuple(
        mapped_table.c.keys()
    )

    for column_name in mapped_table.c.keys():
        migration_column = migration_table.c[column_name]
        mapped_column = mapped_table.c[column_name]

        assert migration_column.nullable == mapped_column.nullable
        assert (
            _compiled_type(migration_column)
            == _compiled_type(mapped_column)
        )
        assert migration_column.default is None
        assert migration_column.server_default is None

    assert migration_table.primary_key.name == (
        mapped_table.primary_key.name
    )

    assert tuple(
        column.name
        for column in migration_table.primary_key.columns
    ) == tuple(
        column.name
        for column in mapped_table.primary_key.columns
    )

    assert (
        _normalized_check_constraints(migration_table)
        == _normalized_check_constraints(mapped_table)
    )

    assert len(migration_table.foreign_keys) == 0


def test_revision_0002_downgrade_reverses_only_its_table(
    monkeypatch,
) -> None:
    revision = _load_revision()
    dropped_tables: list[str] = []

    monkeypatch.setattr(
        revision.op,
        "drop_table",
        dropped_tables.append,
    )

    revision.downgrade()

    assert dropped_tables == ["knowledge_records"]


def test_revision_0002_contains_no_runtime_or_schema_creation_shortcuts() -> None:
    assert MIGRATION_0002.is_file()

    source = MIGRATION_0002.read_text()

    prohibited = (
        "create_all(",
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "Settings(",
        "DATABASE_URL",
    )

    violations = [
        marker
        for marker in prohibited
        if marker in source
    ]

    assert violations == []


def test_alembic_env_registers_knowledge_mapping_before_target_metadata() -> None:
    source = ALEMBIC_ENV.read_text()
    tree = ast.parse(source)

    registration_lines: list[int] = []

    for node in tree.body:
        if (
            isinstance(node, ast.ImportFrom)
            and node.module
            == "app.infrastructure.knowledge.models"
        ):
            registration_lines.append(node.lineno)

        if isinstance(node, ast.Import):
            for alias in node.names:
                if (
                    alias.name
                    == "app.infrastructure.knowledge.models"
                ):
                    registration_lines.append(node.lineno)

    target_metadata_line = next(
        node.lineno
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name)
            and target.id == "target_metadata"
            for target in node.targets
        )
    )

    assert registration_lines
    assert min(registration_lines) < target_metadata_line
