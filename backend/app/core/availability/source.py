\
from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.availability.observation import (
    CapabilityAvailabilityObservation,
)


class CapabilityAvailabilitySource(ABC):
    """Trusted read-only source for one capability availability observation."""

    @property
    @abstractmethod
    def capability_name(self) -> str:
        """Return the capability identity observed by this source."""
        ...

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the identity of this observation source."""
        ...

    @abstractmethod
    def observe(self) -> CapabilityAvailabilityObservation:
        """Return the current capability availability observation."""
        ...
