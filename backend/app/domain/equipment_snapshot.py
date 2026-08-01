"""Immutable equipment snapshot consumed by PlantMind intelligence engines."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.domain.alarm import Alarm
from app.domain.base import DomainException
from app.domain.equipment import Equipment


@dataclass(frozen=True, slots=True, kw_only=True)
class EquipmentSnapshot:
    """Point-in-time operational view of one industrial equipment item."""

    equipment: Equipment
    alarms: tuple[Alarm, ...] = ()
    observed_at: datetime
    contract_version: str = "1.0"

    def __post_init__(self) -> None:
        if self.observed_at.tzinfo is None:
            raise DomainException(
                "Equipment snapshot timestamp must include timezone information."
            )

        if not self.contract_version.strip():
            raise DomainException(
                "Equipment snapshot contract version must not be empty."
            )

        object.__setattr__(self, "alarms", tuple(self.alarms))
        object.__setattr__(
            self,
            "observed_at",
            self.observed_at.astimezone(timezone.utc),
        )
        object.__setattr__(
            self,
            "contract_version",
            self.contract_version.strip(),
        )

    @property
    def active_alarms(self) -> tuple[Alarm, ...]:
        """Return active alarms contained in this snapshot."""

        return tuple(alarm for alarm in self.alarms if alarm.is_active)

    @property
    def requires_attention(self) -> bool:
        """Return whether equipment condition or active alarms need attention."""

        return self.equipment.requires_attention or bool(self.active_alarms)