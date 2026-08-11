import ast
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
ALEMBIC_INI = REPOSITORY_ROOT / "backend" / "alembic.ini"
MIGRATIONS = REPOSITORY_ROOT / "backend" / "migrations"


def test_alembic_configuration_exists() -> None:
    assert ALEMBIC_INI.is_file()
    assert MIGRATIONS.is_dir()


def test_alembic_configuration_contains_no_database_credentials() -> None:
    configuration = ALEMBIC_INI.read_text().lower()

    assert "postgresql://" not in configuration
    assert "postgresql+psycopg://" not in configuration


def test_alembic_uses_canonical_database_metadata() -> None:
    env_file = MIGRATIONS / "env.py"

    source = env_file.read_text()
    tree = ast.parse(source)

    imports = {
        (node.module, alias.name)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }

    assert (
        "app.infrastructure.database.metadata",
        "DatabaseBase",
    ) in imports
    assert (
        "app.infrastructure.database.configuration",
        "validate_database_url",
    ) in imports
    assert "target_metadata = DatabaseBase.metadata" in source

    database_url_function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_database_url"
    )

    return_values = [
        node.value
        for node in ast.walk(database_url_function)
        if isinstance(node, ast.Return)
    ]

    assert any(
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Name)
        and value.func.id == "validate_database_url"
        for value in return_values
    )


def test_alembic_has_exactly_one_migration_head() -> None:
    configuration = Config(str(ALEMBIC_INI))
    scripts = ScriptDirectory.from_config(configuration)

    assert len(scripts.get_heads()) == 1

def test_alembic_migration_template_provides_canonical_imports() -> None:
    template = MIGRATIONS / "script.py.mako"
    source = template.read_text()

    assert "from alembic import op" in source
    assert "import sqlalchemy as sa" in source
