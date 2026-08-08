\
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from app.core.availability.state import CapabilityAvailabilityState


@dataclass(frozen=True)
class CapabilityAvailabilityObservation:
    """Immutable availability observation for one capability."""

    capability_name: str
    state: CapabilityAvailabilityState
    observed_at: datetime
    source_name: str

    def __post_init__(self) -> None:
        if not self.capability_name.strip():
            raise ValueError("Capability name must be non-empty.")

        if not self.source_name.strip():
            raise ValueError("Source name must be non-empty.")

        if self.observed_at.tzinfo is None:
            raise ValueError(
                "Capability availability timestamp must include timezone information."
            )

        object.__setattr__(
            self,
            "observed_at",
            self.observed_at.astimezone(UTC),
        )
