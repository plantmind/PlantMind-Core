from __future__ import annotations

import pytest

from app.core.composition import CompositionRoot
from app.services.operational_transition_application_service import (
    OperationalTransitionApplicationService,
)


def test_composition_exposes_operational_transition_application_service() -> None:
    platform = CompositionRoot.build()

    assert isinstance(
        platform.operational_transition_application_service,
        OperationalTransitionApplicationService,
    )


def test_container_resolves_same_operational_transition_application_service() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.container.resolve(OperationalTransitionApplicationService)
        is platform.operational_transition_application_service
    )


def test_application_service_uses_exact_composed_dependencies() -> None:
    platform = CompositionRoot.build()
    service = platform.operational_transition_application_service

    assert service.application_facade is platform.application_facade
    assert (
        service.operational_transition_coordinator
        is platform.operational_transition_coordinator
    )


def test_composition_does_not_execute_application_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_request(
        self: OperationalTransitionApplicationService,
        observations: object,
    ) -> object:
        raise AssertionError(
            "Composition must not execute the operational transition application service."
        )

    monkeypatch.setattr(
        OperationalTransitionApplicationService,
        "request_operational",
        forbidden_request,
    )

    CompositionRoot.build()


def test_bootstrap_does_not_execute_application_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_request(
        self: OperationalTransitionApplicationService,
        observations: object,
    ) -> object:
        raise AssertionError(
            "Bootstrap must not execute the operational transition application service."
        )

    monkeypatch.setattr(
        OperationalTransitionApplicationService,
        "request_operational",
        forbidden_request,
    )

    platform = CompositionRoot.build()
    platform.bootstrap.startup()


def test_health_does_not_execute_application_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden_request(
        self: OperationalTransitionApplicationService,
        observations: object,
    ) -> object:
        raise AssertionError(
            "Health must not execute the operational transition application service."
        )

    monkeypatch.setattr(
        OperationalTransitionApplicationService,
        "request_operational",
        forbidden_request,
    )

    platform = CompositionRoot.build()
    platform.health.get_status()
