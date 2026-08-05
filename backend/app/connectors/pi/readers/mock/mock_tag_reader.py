"""
PlantMind Mock PI Tag Reader
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.connectors.pi.readers.tag_reader import (
    PITagReader,
    PITagValue,
)


class MockTagReader(PITagReader):
    """
    In-memory PI tag reader for development and testing.
    """

    def __init__(
        self,
        values: dict[str, Any] | None = None,
    ) -> None:
        self._values = values or {}

    def read_current(self, tag: str) -> PITagValue:
        if tag not in self._values:
            raise LookupError(
                f"Mock PI tag '{tag}' is not configured."
            )

        return PITagValue(
            tag=tag,
            value=self._values[tag],
            timestamp=datetime.now(UTC),
            quality="good",
        )
