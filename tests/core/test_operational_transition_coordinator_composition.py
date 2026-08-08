from __future__ import annotations

import pytest

from app.core.composition import CompositionRoot
from app.core.operational_transition_coordinator import (
    OperationalTransitionCoordinator,
)


def test_composition_exposes_operational_transition_coordinator() -> None:
    platform = CompositionRoot.build()

    assert isinstance(
        platform.operational_transition_coordinator,
        OperationalTransitionCoordinator,
    )


def test_container_resolves_same_operational_transition_coordinator() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.container.resolve(OperationalTransitionCoordinator)
        is platform.operational_transition_coordinator
    )


def test_coordinator_uses_exact_composed_dependencies() -> None:
    platform = CompositionRoot.build()
    coordinator = platform.operational_transition_coordinator

    assert coordinator.runtime is platform.runtime
    assert coordinator.availability_observer is platform.availability_observer
    assert (
        coordinator.coverage_evaluator
        is platform.mandatory_capability_coverage_evaluator
    )


def test_composition_does_not_execute_operational_transition_coordinator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_request(
        self: OperationalTransitionCoordinator,
        workload_evidence: object,
    ) -> object:
        raise AssertionError(
            "Composition must not execute operational transition coordination."
        )

    monkeypatch.setattr(
        OperationalTransitionCoordinator,
        "request_operational",
        forbidden_request,
    )

    CompositionRoot.build()
