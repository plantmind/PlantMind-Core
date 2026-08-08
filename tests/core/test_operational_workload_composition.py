from app.core.composition import CompositionRoot
from app.services.application_facade import ApplicationFacade
from app.services.integration_gateway import IntegrationGateway
from app.services.orchestration.orchestration_service import (
    OrchestrationService,
)
from app.services.orchestration.workflow import WorkflowStage
from app.services.orchestration.workflow_executor import WorkflowExecutor


def test_composition_exposes_application_facade() -> None:
    platform = CompositionRoot.build()

    assert isinstance(
        platform.application_facade,
        ApplicationFacade,
    )


def test_container_resolves_composed_application_facade() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.container.resolve(ApplicationFacade)
        is platform.application_facade
    )


def test_application_facade_uses_composed_integration_gateway() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.application_facade._gateway
        is platform.integration_gateway
    )


def test_integration_gateway_uses_composed_orchestration_service() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.integration_gateway._orchestration_service
        is platform.orchestration_service
    )


def test_orchestration_service_uses_composed_workflow_executor() -> None:
    platform = CompositionRoot.build()

    assert (
        platform.orchestration_service._executor
        is platform.workflow_executor
    )


def test_composed_application_facade_executes_complete_workflow() -> None:
    platform = CompositionRoot.build()

    execution = platform.application_facade.analyze(())

    assert execution.is_complete is True
    assert execution.stages[-1] is WorkflowStage.COMPLETED
    assert execution.result["risk_level"] == "low"


def test_workload_execution_does_not_modify_runtime_lifecycle() -> None:
    platform = CompositionRoot.build()

    initial_state = platform.runtime.state
    initial_admission = platform.runtime.is_request_admission_enabled

    platform.application_facade.analyze(())

    assert platform.runtime.state is initial_state
    assert (
        platform.runtime.is_request_admission_enabled
        is initial_admission
    )
