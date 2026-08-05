from datetime import UTC, datetime

import pytest

from app.connectors.pi.readers.tag_reader import (
    PITagReader,
    PITagValue,
)


class DummyTagReader(PITagReader):
    def read_current(self, tag: str) -> PITagValue:
        return PITagValue(
            tag=tag,
            value=42.5,
            timestamp=datetime.now(UTC),
            quality="good",
        )


def test_read_current_returns_tag_value() -> None:
    reader = DummyTagReader()

    result = reader.read_current("COMP-H-001.SUCTION_PRESSURE")

    assert result.tag == "COMP-H-001.SUCTION_PRESSURE"
    assert result.value == 42.5
    assert result.quality == "good"
    assert result.timestamp.tzinfo is UTC


def test_tag_value_is_immutable() -> None:
    value = PITagValue(
        tag="TAG-001",
        value=10,
        timestamp=datetime.now(UTC),
        quality="good",
    )

    with pytest.raises(AttributeError):
        value.value = 20
