from sqlalchemy import MetaData


def test_canonical_database_base_owns_metadata() -> None:
    from app.infrastructure.database.metadata import DatabaseBase

    assert isinstance(DatabaseBase.metadata, MetaData)


def test_database_metadata_is_singleton_per_process() -> None:
    from app.infrastructure.database.metadata import DatabaseBase

    first = DatabaseBase.metadata
    second = DatabaseBase.metadata

    assert first is second
