\
from __future__ import annotations

from enum import Enum


class CapabilityAvailabilityState(str, Enum):
    """Observed availability state of a PlantMind capability."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
