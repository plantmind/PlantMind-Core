"""Equipment domain entity for PlantMind."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.base import DomainEntity, DomainException, EntityId


class EquipmentStatus(StrEnum):
    """Supported lifecycle states for industrial equipment."""

    UNKNOWN = "unknown"
    AVAILABLE = "available"
    RUNNING = "running"
    STANDBY = "standby"
    DEGRADED = "degraded"
    TRIPPED = "tripped"
    OUT_OF_SERVICE = "out_of_service"
    MAINTENANCE = "maintenance"


class EquipmentCriticality(StrEnum):
    """Business criticality assigned to industrial equipment."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True, kw_only=True)
class Equipment(DomainEntity[EntityId]):
    """Immutable representation of industrial equipment."""

    tag: str
    name: str
    equipment_type: str
    status: EquipmentStatus = EquipmentStatus.UNKNOWN
    criticality: EquipmentCriticality = EquipmentCriticality.MEDIUM
    description: str | None = None

    def __post_init__(self) -> None:
        tag = self.tag.strip()
        name = self.name.strip()
        equipment_type = self.equipment_type.strip()

        if not tag:
            raise DomainException("Equipment tag must not be empty.")

        if not name:
            raise DomainException("Equipment name must not be empty.")

        if not equipment_type:
            raise DomainException("Equipment type must not be empty.")

        object.__setattr__(self, "tag", tag.upper())
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "equipment_type", equipment_type)

        if self.description is not None:
            description = self.description.strip()
            object.__setattr__(self, "description", description or None)

    @property
    def is_operational(self) -> bool:
        """Return whether the equipment is available for operation."""

        return self.status in {
            EquipmentStatus.AVAILABLE,
            EquipmentStatus.RUNNING,
            EquipmentStatus.STANDBY,
            EquipmentStatus.DEGRADED,
        }

    @property
    def requires_attention(self) -> bool:
        """Return whether the current state requires engineering attention."""

        return self.status in {
            EquipmentStatus.DEGRADED,
            EquipmentStatus.TRIPPED,
            EquipmentStatus.OUT_OF_SERVICE,
            EquipmentStatus.MAINTENANCE,
        }