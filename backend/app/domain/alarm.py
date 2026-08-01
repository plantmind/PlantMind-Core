"""Alarm domain entity for PlantMind."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.base import DomainEntity, DomainException, EntityId


class AlarmPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlarmState(StrEnum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    CLEARED = "cleared"
    SUPPRESSED = "suppressed"


@dataclass(frozen=True, slots=True, kw_only=True)
class Alarm(DomainEntity[EntityId]):
    """Immutable industrial alarm."""

    tag: str
    message: str
    priority: AlarmPriority
    state: AlarmState = AlarmState.ACTIVE
    source: str | None = None

    def __post_init__(self) -> None:
        tag = self.tag.strip().upper()
        message = self.message.strip()

        if not tag:
            raise DomainException("Alarm tag must not be empty.")

        if not message:
            raise DomainException("Alarm message must not be empty.")

        object.__setattr__(self, "tag", tag)
        object.__setattr__(self, "message", message)

        if self.source is not None:
            source = self.source.strip()
            object.__setattr__(self, "source", source or None)

    @property
    def is_active(self) -> bool:
        return self.state is AlarmState.ACTIVE

    @property
    def requires_operator_action(self) -> bool:
        return self.state is AlarmState.ACTIVE