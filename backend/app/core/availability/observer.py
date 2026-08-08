\
from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from app.core.availability.observation import (
    CapabilityAvailabilityObservation,
)
from app.core.availability.source import CapabilityAvailabilitySource
from app.core.availability.state import CapabilityAvailabilityState


class CapabilityAvailabilityObserver:
    """Read-only coordinator for explicitly composed availability sources."""

    def __init__(
        self,
        sources: Sequence[CapabilityAvailabilitySource] = (),
    ) -> None:
        self._sources = tuple(sources)

    def observe_all(
        self,
    ) -> tuple[CapabilityAvailabilityObservation, ...]:
        """Observe all composed sources in deterministic composition order."""

        observations: list[CapabilityAvailabilityObservation] = []

        for source in self._sources:
            try:
                observation = source.observe()
            except Exception:
                observation = CapabilityAvailabilityObservation(
                    capability_name=source.capability_name,
                    state=CapabilityAvailabilityState.UNKNOWN,
                    observed_at=datetime.now(UTC),
                    source_name=source.source_name,
                )

            observations.append(observation)

        return tuple(observations)
