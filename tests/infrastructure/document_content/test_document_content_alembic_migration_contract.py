from __future__ import annotations

import ast
import importlib
import importlib.util
from pathlib import Path
from types import ModuleType

import sqlalchemy as sa
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.dialects import postgresql

from app.infrastructure.database.metadata import DatabaseBase


ROOT = Path(__file__).resolve().parents[3]

ALEMBIC_INI = ROOT / "backend/alembic.ini"
MIGRATIONS = ROOT / "backend/migrations"
MIGRATION = (
    MIGRATIONS
    / "versions"
    / "0005_document_content_descriptors.py"
)
ALEMBIC_ENV = MIGRATIONS / "env.py"


def _load_revision() -> ModuleType:
    assert MIGRATION.is_file()

    spec = importlib.util.spec_from_file_location(
        "plantmind_migration_0005",
        MIGRATION,
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


def _mapped_table() -> sa.Table:
    importlib.import_module(
        "app.infrastructure.document_content.models"
    )

    return DatabaseBase.metadata.tables[
        "document_content_descriptors"
    ]


def test_revision_0005_extends_0004_linearly() -> None:
    revision = _load_revision()

    assert revision.revision == "0005"
    assert revision.down_revision == "0004"
    assert revision.branch_labels is None
    assert revision.depends_on is None


def test_revision_0005_is_the_only_alembic_head() -> None:
    configuration = Config(str(ALEMBIC_INI))
    scripts = ScriptDirectory.from_config(configuration)

    assert scripts.get_heads() == ["0005"]


def test_revision_0005_schema_matches_canonical_descriptor_metadata(
    monkeypatch,
) -> None:
    revision = _load_revision()
    mapped_table = _mapped_table()

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

    assert (
        migration_table.name
        == "document_content_descriptors"
    )

    assert tuple(
        migration_table.c.keys()
    ) == tuple(
        mapped_table.c.keys()
    )

    for column_name in mapped_table.c.keys():
        migration_column = migration_table.c[column_name]
        mapped_column = mapped_table.c[column_name]

        assert (
            migration_column.nullable
            == mapped_column.nullable
        )
        assert (
            _compiled_type(migration_column)
            == _compiled_type(mapped_column)
        )
        assert migration_column.default is None
        assert migration_column.server_default is None
        assert migration_column.unique is not True

    assert (
        migration_table.primary_key.name
        == "pk_document_content_descriptors"
    )

    assert tuple(
        column.name
        for column in migration_table.primary_key.columns
    ) == ("document_id",)

    assert not migration_table.foreign_keys

    assert [
        constraint
        for constraint in migration_table.constraints
        if isinstance(constraint, UniqueConstraint)
    ] == []

    assert [
        constraint
        for constraint in migration_table.constraints
        if isinstance(constraint, CheckConstraint)
    ] == []


def test_revision_0005_downgrade_drops_only_descriptor_table(
    monkeypatch,
) -> None:
    revision = _load_revision()

    dropped: list[str] = []

    monkeypatch.setattr(
        revision.op,
        "drop_table",
        dropped.append,
    )

    revision.downgrade()

    assert dropped == [
        "document_content_descriptors"
    ]


def test_revision_0005_contains_no_runtime_or_schema_shortcuts() -> None:
    source = MIGRATION.read_text()

    prohibited = (
        "create_all(",
        "create_engine(",
        "sessionmaker(",
        "DatabaseRuntime(",
        "Settings(",
        "DATABASE_URL",
    )

    assert [
        marker
        for marker in prohibited
        if marker in source
    ] == []


def test_alembic_env_registers_descriptor_mapping_before_target_metadata() -> None:
    source = ALEMBIC_ENV.read_text()
    tree = ast.parse(source)

    registration_lines: list[int] = []

    for node in tree.body:
        if (
            isinstance(node, ast.ImportFrom)
            and node.module
            == "app.infrastructure.document_content.models"
        ):
            registration_lines.append(node.lineno)

        if isinstance(node, ast.Import):
            for alias in node.names:
                if (
                    alias.name
                    == "app.infrastructure.document_content.models"
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
