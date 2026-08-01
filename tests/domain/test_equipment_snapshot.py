"""Unit tests for the EquipmentSnapshot domain contract."""

from datetime import datetime, timezone

import pytest

from app.domain.alarm import Alarm, AlarmPriority, AlarmState
from app.domain.base import DomainException, EntityId
from app.domain.equipment import (
    Equipment,
    EquipmentCriticality,
    EquipmentStatus,
)
from app.domain.equipment_snapshot import EquipmentSnapshot


def make_equipment() -> Equipment:
    return Equipment(
        id=EntityId.new(),
        tag="COMP-H-001",
        name="Ethane Booster Compressor",
        equipment_type="compressor",
        status=EquipmentStatus.RUNNING,
        criticality=EquipmentCriticality.CRITICAL,
    )


def make_alarm(
    *,
    state: AlarmState = AlarmState.ACTIVE,
) -> Alarm:
    return Alarm(
        id=EntityId.new(),
        tag="PAHH-1001",
        message="Discharge pressure high-high",
        priority=AlarmPriority.HIGH,
        state=state,
        source="DeltaV",
    )


def test_snapshot_normalizes_alarm_collection() -> None:
    snapshot = EquipmentSnapshot(
        equipment=make_equipment(),
        alarms=[],
        observed_at=datetime.now(timezone.utc),
    )

    assert isinstance(snapshot.alarms, tuple)


def test_snapshot_requires_timezone() -> None:
    with pytest.raises(
        DomainException,
        match="Equipment snapshot timestamp must include timezone information.",
    ):
        EquipmentSnapshot(
            equipment=make_equipment(),
            alarms=[],
            observed_at=datetime.now(),
        )


def test_snapshot_contract_version_must_not_be_empty() -> None:
    with pytest.raises(
        DomainException,
        match="Equipment snapshot contract version must not be empty.",
    ):
        EquipmentSnapshot(
            equipment=make_equipment(),
            alarms=[],
            observed_at=datetime.now(timezone.utc),
            contract_version="   ",
        )


def test_active_alarms_returns_only_active_alarms() -> None:
    active_alarm = make_alarm(state=AlarmState.ACTIVE)
    cleared_alarm = make_alarm(state=AlarmState.CLEARED)

    snapshot = EquipmentSnapshot(
        equipment=make_equipment(),
        alarms=[active_alarm, cleared_alarm],
        observed_at=datetime.now(timezone.utc),
    )

    assert snapshot.active_alarms == (active_alarm,)


def test_snapshot_requires_attention_when_alarm_is_active() -> None:
    snapshot = EquipmentSnapshot(
        equipment=make_equipment(),
        alarms=[make_alarm(state=AlarmState.ACTIVE)],
        observed_at=datetime.now(timezone.utc),
    )

    assert snapshot.requires_attention is True