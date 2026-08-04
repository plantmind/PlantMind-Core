
from app.core.container.service_container import ServiceContainer


class Database:
    pass


class Repository:
    def __init__(self, db: Database):
        self.db = db


def test_register_instance() -> None:
    container = ServiceContainer()

    database = Database()

    container.register_instance(Database, database)

    assert container.resolve(Database) is database


def test_register_factory() -> None:
    container = ServiceContainer()

    container.register_factory(
        Repository,
        lambda c: Repository(c.resolve(Database)),
    )

    database = Database()

    container.register_instance(Database, database)

    repository = container.resolve(Repository)

    assert isinstance(repository, Repository)
    assert repository.db is database


def test_duplicate_registration_fails() -> None:
    container = ServiceContainer()

    container.register_instance(Database, Database())

    try:
        container.register_instance(Database, Database())
    except ValueError:
        return

    assert False


def test_unknown_service_fails() -> None:
    container = ServiceContainer()

    try:
        container.resolve(Database)
    except LookupError:
        return

    assert False
