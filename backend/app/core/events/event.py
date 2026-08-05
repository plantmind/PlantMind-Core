"""
PlantMind Event Model
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(frozen=True)
class Event:
    """
    Base platform event.
    """

    name: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
