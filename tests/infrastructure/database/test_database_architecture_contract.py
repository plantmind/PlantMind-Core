import importlib
import sys
from pathlib import Path

import sqlalchemy


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
BACKEND_APP = REPOSITORY_ROOT / "backend" / "app"


def test_importing_database_package_does_not_create_engine(
    monkeypatch,
) -> None:
    calls = []

    def fail_if_called(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError(
            "Database engine must not be created during module import."
        )

    monkeypatch.setattr(sqlalchemy, "create_engine", fail_if_called)

    sys.modules.pop(
        "app.infrastructure.database.runtime",
        None,
    )
    sys.modules.pop(
        "app.infrastructure.database",
        None,
    )

    importlib.import_module("app.infrastructure.database")

    assert calls == []


def test_legacy_database_module_is_retired() -> None:
    legacy_database = BACKEND_APP / "database.py"

    assert not legacy_database.exists()


def test_domain_and_knowledge_do_not_depend_on_sqlalchemy() -> None:
    prohibited = []

    for package in ("domain", "knowledge"):
        for path in (BACKEND_APP / package).rglob("*.py"):
            source = path.read_text()
            if "sqlalchemy" in source.lower():
                prohibited.append(
                    str(path.relative_to(REPOSITORY_ROOT))
                )

    assert prohibited == []
