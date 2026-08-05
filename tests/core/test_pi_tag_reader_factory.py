from app.connectors.pi.readers.factory import TagReaderFactory
from app.connectors.pi.readers.mock.mock_tag_reader import MockTagReader


def setup_function() -> None:
    TagReaderFactory._registry.clear()


def test_register_and_create_reader() -> None:
    TagReaderFactory.register(
        "mock",
        lambda: MockTagReader(
            {"TAG-001": 100}
        ),
    )

    reader = TagReaderFactory.create("mock")

    assert isinstance(reader, MockTagReader)
    assert "mock" in TagReaderFactory.registered_readers()


def test_unknown_reader_raises() -> None:
    try:
        TagReaderFactory.create("unknown")
    except LookupError:
        return

    raise AssertionError("Expected LookupError")


def test_duplicate_registration_raises() -> None:
    TagReaderFactory.register("mock", MockTagReader)

    try:
        TagReaderFactory.register("mock", MockTagReader)
    except ValueError:
        return

    raise AssertionError("Expected ValueError")
