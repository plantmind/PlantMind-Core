from datetime import datetime

import pytest

from app.domain.observation import Observation, ObservationType


def test_valid_observation():
    observation = Observation(
        source="PI System",
        observation_type=ObservationType.PROCESS,
        value="Discharge Pressure = 41.2 bar",
        observed_at=datetime.now().astimezone(),
    )

    assert observation.source == "PI System"


def test_empty_source():
    with pytest.raises(ValueError):
        Observation(
            source="",
            observation_type=ObservationType.PROCESS,
            value="OK",
            observed_at=datetime.now().astimezone(),
        )


def test_empty_value():
    with pytest.raises(ValueError):
        Observation(
            source="PI",
            observation_type=ObservationType.PROCESS,
            value="",
            observed_at=datetime.now().astimezone(),
        )


def test_timestamp_requires_timezone():
    with pytest.raises(ValueError):
        Observation(
            source="PI",
            observation_type=ObservationType.PROCESS,
            value="OK",
            observed_at=datetime.now(),
        )