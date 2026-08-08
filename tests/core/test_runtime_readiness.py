from dataclasses import FrozenInstanceError

import pytest

from app.core.readiness import ReadinessEvidence
from app.core.runtime import Runtime
from app.core.runtime_state import RuntimeState


def complete_evidence() -> ReadinessEvidence:
    return ReadinessEvidence(
        configuration_validated=True,
        runtime_created=True,
        bootstrap_completed=True,
        required_services_initialized=True,
        required_services_validated=True,
        service_registry_operational=True,
        health_capability_initialized=True,
        runtime_metadata_available=True,
    )


def test_readiness_evidence_is_immutable() -> None:
    evidence = complete_evidence()

    with pytest.raises(FrozenInstanceError):
        evidence.configuration_validated = False


def test_runtime_accepts_complete_readiness_evidence() -> None:
    runtime = Runtime()

    runtime.request_readiness(complete_evidence())

    assert runtime.state is RuntimeState.READY
    assert runtime.is_ready is True


def test_runtime_rejects_incomplete_readiness_evidence() -> None:
    runtime = Runtime()
    evidence = ReadinessEvidence(
        configuration_validated=False,
        runtime_created=True,
        bootstrap_completed=True,
        required_services_initialized=True,
        required_services_validated=True,
        service_registry_operational=True,
        health_capability_initialized=True,
        runtime_metadata_available=True,
    )

    with pytest.raises(RuntimeError):
        runtime.request_readiness(evidence)

    assert runtime.state is not RuntimeState.READY
    assert runtime.is_ready is False


def test_rejected_readiness_disables_request_admission() -> None:
    runtime = Runtime()
    runtime.enable_request_admission()
    evidence = ReadinessEvidence(
        configuration_validated=False,
        runtime_created=True,
        bootstrap_completed=True,
        required_services_initialized=True,
        required_services_validated=True,
        service_registry_operational=True,
        health_capability_initialized=True,
        runtime_metadata_available=True,
    )

    with pytest.raises(RuntimeError):
        runtime.request_readiness(evidence)

    assert runtime.is_request_admission_enabled is False
