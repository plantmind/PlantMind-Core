"""Unit tests for the Alarm domain entity."""

from __future__ import annotations

import pytest

from app.domain.alarm import Alarm, AlarmPriority, AlarmState
from app.domain.base import DomainException, EntityId


def build_alarm(
    *,
    tag: str = "PAHH-1001",
    message: str = "Discharge pressure high-high",
    priority: AlarmPriority = AlarmPriority.HIGH,
    state: AlarmState = AlarmState.ACTIVE,
    source: str | None = "DeltaV",
) -> Alarm:
    return Alarm(
        id=EntityId.new(),
        tag=tag,
        message=message,
        priority=priority,
        state=state,
        source=source,
    )


def test_alarm_normalizes_text_fields() -> None:
    alarm = build_alarm(
        tag="  pahh-1001  ",
        message="  Discharge pressure high-high  ",
        source="  DeltaV  ",
    )

    assert alarm.tag == "PAHH-1001"
    assert alarm.message == "Discharge pressure high-high"
    assert alarm.source == "DeltaV"


@pytest.mark.parametrize(
    ("field_name", "field_value", "expected_message"),
    [
        ("tag", "   ", "Alarm tag must not be empty."),
        ("message", "   ", "Alarm message must not be empty."),
    ],
)
def test_alarm_rejects_empty_required_fields(
    field_name: str,
    field_value: str,
    expected_message: str,
) -> None:
    values = {
        "tag": "PAHH-1001",
        "message": "Discharge pressure high-high",
    }
    values[field_name] = field_value

    with pytest.raises(DomainException, match=expected_message):
        build_alarm(**values)


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (AlarmState.ACTIVE, True),
        (AlarmState.ACKNOWLEDGED, False),
        (AlarmState.CLEARED, False),
        (AlarmState.SUPPRESSED, False),
    ],
)
def test_alarm_reports_active_state(
    state: AlarmState,
    expected: bool,
) -> None:
    alarm = build_alarm(state=state)

    assert alarm.is_active is expected


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (AlarmState.ACTIVE, True),
        (AlarmState.ACKNOWLEDGED, False),
        (AlarmState.CLEARED, False),
        (AlarmState.SUPPRESSED, False),
    ],
)
def test_alarm_reports_operator_action_requirement(
    state: AlarmState,
    expected: bool,
) -> None:
    alarm = build_alarm(state=state)

    assert alarm.requires_operator_action is expected


def test_alarm_converts_blank_source_to_none() -> None:
    alarm = build_alarm(source="   ")

    assert alarm.source is None