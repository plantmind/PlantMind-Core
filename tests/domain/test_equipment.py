"""Unit tests for the Equipment domain entity."""

from __future__ import annotations

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.equipment import (
    Equipment,
    EquipmentCriticality,
    EquipmentStatus,
)


def build_equipment(
    *,
    tag: str = "COMP-H-001",
    name: str = "Ethane Booster Compressor",
    equipment_type: str = "compressor",
    status: EquipmentStatus = EquipmentStatus.UNKNOWN,
    criticality: EquipmentCriticality = EquipmentCriticality.CRITICAL,
    description: str | None = None,
) -> Equipment:
    """Create a valid Equipment instance for testing."""

    return Equipment(
        id=EntityId.new(),
        tag=tag,
        name=name,
        equipment_type=equipment_type,
        status=status,
        criticality=criticality,
        description=description,
    )


def test_equipment_normalizes_text_fields() -> None:
    equipment = build_equipment(
        tag="  comp-h-001  ",
        name="  Ethane Booster Compressor  ",
        equipment_type="  compressor  ",
        description="  Phase 1 anchor equipment  ",
    )

    assert equipment.tag == "COMP-H-001"
    assert equipment.name == "Ethane Booster Compressor"
    assert equipment.equipment_type == "compressor"
    assert equipment.description == "Phase 1 anchor equipment"


@pytest.mark.parametrize(
    ("field_name", "field_value", "expected_message"),
    [
        ("tag", "   ", "Equipment tag must not be empty."),
        ("name", "   ", "Equipment name must not be empty."),
        ("equipment_type", "   ", "Equipment type must not be empty."),
    ],
)
def test_equipment_rejects_empty_required_fields(
    field_name: str,
    field_value: str,
    expected_message: str,
) -> None:
    values = {
        "tag": "COMP-H-001",
        "name": "Ethane Booster Compressor",
        "equipment_type": "compressor",
    }
    values[field_name] = field_value

    with pytest.raises(DomainException, match=expected_message):
        build_equipment(**values)


@pytest.mark.parametrize(
    "status",
    [
        EquipmentStatus.AVAILABLE,
        EquipmentStatus.RUNNING,
        EquipmentStatus.STANDBY,
        EquipmentStatus.DEGRADED,
    ],
)
def test_equipment_reports_operational_states(status: EquipmentStatus) -> None:
    equipment = build_equipment(status=status)

    assert equipment.is_operational is True


@pytest.mark.parametrize(
    "status",
    [
        EquipmentStatus.UNKNOWN,
        EquipmentStatus.TRIPPED,
        EquipmentStatus.OUT_OF_SERVICE,
        EquipmentStatus.MAINTENANCE,
    ],
)
def test_equipment_reports_non_operational_states(status: EquipmentStatus) -> None:
    equipment = build_equipment(status=status)

    assert equipment.is_operational is False


@pytest.mark.parametrize(
    "status",
    [
        EquipmentStatus.DEGRADED,
        EquipmentStatus.TRIPPED,
        EquipmentStatus.OUT_OF_SERVICE,
        EquipmentStatus.MAINTENANCE,
    ],
)
def test_equipment_reports_states_requiring_attention(
    status: EquipmentStatus,
) -> None:
    equipment = build_equipment(status=status)

    assert equipment.requires_attention is True


def test_equipment_converts_blank_description_to_none() -> None:
    equipment = build_equipment(description="   ")

    assert equipment.description is None