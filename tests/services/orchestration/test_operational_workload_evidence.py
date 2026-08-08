from dataclasses import FrozenInstanceError
from uuid import UUID, uuid4

import pytest

from app.core.composition import CompositionRoot
from app.core.runtime_state import RuntimeState
from app.services.application_facade import ApplicationFacade
from app.services.integration_gateway import IntegrationGateway
from app.services.orchestration.orchestration_service import OrchestrationService
from app.services.orchestration.workflow import (
    WorkflowExecution,
    WorkflowStage,
)
from app.services.orchestration.workflow_executor import WorkflowExecutor
from app.services.orchestration.workload_evidence import (
    ApplicationFacadeEntryEvidence,
    OperationalWorkloadEvidence,
    WorkflowExecutionStartEvidence,
)


class StubPresentationService:
    def generate(
        self,
        observations: tuple[object, ...],
    ) -> dict[str, object]:
        return {"status": "ok"}


class RecordingGateway:
    def __init__(self) -> None:
        self.facade_entry_evidence = None

    def execute(
        self,
        observations: tuple[object, ...],
        facade_entry_evidence=None,
    ) -> WorkflowExecution:
        self.facade_entry_evidence = facade_entry_evidence
        return WorkflowExecution(
            result={"status": "ok"},
            stages=(WorkflowStage.COMPLETED,),
        )


class RecordingOrchestrationService:
    def __init__(self) -> None:
        self.facade_entry_evidence = None

    def run(
        self,
        observations: tuple[object, ...],
        facade_entry_evidence=None,
    ) -> WorkflowExecution:
        self.facade_entry_evidence = facade_entry_evidence
        return WorkflowExecution(
            result={"status": "ok"},
            stages=(WorkflowStage.COMPLETED,),
        )


class RecordingExecutor:
    def __init__(self) -> None:
        self.facade_entry_evidence = None

    def execute(
        self,
        observations: tuple[object, ...],
        facade_entry_evidence=None,
    ) -> WorkflowExecution:
        self.facade_entry_evidence = facade_entry_evidence
        return WorkflowExecution(
            result={"status": "ok"},
            stages=(WorkflowStage.COMPLETED,),
        )


def build_executor() -> WorkflowExecutor:
    return WorkflowExecutor(
        presentation_service=StubPresentationService()
    )


def build_canonical_facade() -> ApplicationFacade:
    executor = build_executor()
    orchestration_service = OrchestrationService(executor=executor)
    gateway = IntegrationGateway(
        orchestration_service=orchestration_service
    )
    return ApplicationFacade(gateway=gateway)


def test_evidence_models_are_immutable() -> None:
    workload_id = uuid4()
    entry = ApplicationFacadeEntryEvidence(workload_id=workload_id)
    start = WorkflowExecutionStartEvidence(workload_id=workload_id)
    evidence = OperationalWorkloadEvidence(
        facade_entry=entry,
        execution_start=start,
    )

    with pytest.raises(FrozenInstanceError):
        entry.workload_id = uuid4()

    with pytest.raises(FrozenInstanceError):
        start.workload_id = uuid4()

    with pytest.raises(FrozenInstanceError):
        evidence.facade_entry = entry


def test_workload_identity_uses_uuid() -> None:
    facade = build_canonical_facade()

    execution = facade.analyze(())

    evidence = execution.operational_workload_evidence
    assert evidence is not None
    assert isinstance(evidence.facade_entry.workload_id, UUID)
    assert isinstance(evidence.execution_start.workload_id, UUID)


def test_mismatched_evidence_identities_are_rejected() -> None:
    entry = ApplicationFacadeEntryEvidence(workload_id=uuid4())
    start = WorkflowExecutionStartEvidence(workload_id=uuid4())

    with pytest.raises(ValueError):
        OperationalWorkloadEvidence(
            facade_entry=entry,
            execution_start=start,
        )


def test_canonical_facade_invocation_produces_correlated_evidence() -> None:
    facade = build_canonical_facade()

    execution = facade.analyze(())

    assert execution.operational_workload_evidence is not None


def test_facade_entry_and_execution_start_share_workload_identity() -> None:
    facade = build_canonical_facade()

    execution = facade.analyze(())

    evidence = execution.operational_workload_evidence
    assert evidence is not None
    assert (
        evidence.facade_entry.workload_id
        == evidence.execution_start.workload_id
    )


def test_separate_facade_invocations_receive_distinct_workload_ids() -> None:
    facade = build_canonical_facade()

    first = facade.analyze(())
    second = facade.analyze(())

    first_evidence = first.operational_workload_evidence
    second_evidence = second.operational_workload_evidence

    assert first_evidence is not None
    assert second_evidence is not None
    assert (
        first_evidence.facade_entry.workload_id
        != second_evidence.facade_entry.workload_id
    )


def test_application_facade_originates_facade_entry_evidence() -> None:
    gateway = RecordingGateway()
    facade = ApplicationFacade(gateway=gateway)

    facade.analyze(())

    assert isinstance(
        gateway.facade_entry_evidence,
        ApplicationFacadeEntryEvidence,
    )
    assert isinstance(
        gateway.facade_entry_evidence.workload_id,
        UUID,
    )


def test_integration_gateway_forwards_entry_evidence_unchanged() -> None:
    orchestration_service = RecordingOrchestrationService()
    gateway = IntegrationGateway(
        orchestration_service=orchestration_service
    )
    entry = ApplicationFacadeEntryEvidence(workload_id=uuid4())

    gateway.execute(
        (),
        facade_entry_evidence=entry,
    )

    assert orchestration_service.facade_entry_evidence is entry


def test_orchestration_service_forwards_entry_evidence_unchanged() -> None:
    executor = RecordingExecutor()
    service = OrchestrationService(executor=executor)
    entry = ApplicationFacadeEntryEvidence(workload_id=uuid4())

    service.run(
        (),
        facade_entry_evidence=entry,
    )

    assert executor.facade_entry_evidence is entry


def test_workflow_executor_creates_execution_start_from_entry_identity() -> None:
    executor = build_executor()
    entry = ApplicationFacadeEntryEvidence(workload_id=uuid4())

    execution = executor.execute(
        (),
        facade_entry_evidence=entry,
    )

    evidence = execution.operational_workload_evidence
    assert evidence is not None
    assert evidence.facade_entry is entry
    assert evidence.execution_start.workload_id == entry.workload_id


def test_direct_gateway_execution_does_not_fabricate_evidence() -> None:
    executor = build_executor()
    service = OrchestrationService(executor=executor)
    gateway = IntegrationGateway(orchestration_service=service)

    execution = gateway.execute(())

    assert execution.operational_workload_evidence is None


def test_direct_orchestration_execution_does_not_fabricate_evidence() -> None:
    executor = build_executor()
    service = OrchestrationService(executor=executor)

    execution = service.run(())

    assert execution.operational_workload_evidence is None


def test_direct_workflow_execution_does_not_fabricate_evidence() -> None:
    executor = build_executor()

    execution = executor.execute(())

    assert execution.operational_workload_evidence is None


def test_existing_workflow_execution_construction_remains_valid() -> None:
    execution = WorkflowExecution(
        result={"status": "ok"},
        stages=(WorkflowStage.COMPLETED,),
    )

    assert execution.operational_workload_evidence is None


def test_existing_workflow_completion_semantics_remain_unchanged() -> None:
    execution = WorkflowExecution(
        result={"status": "ok"},
        stages=(
            WorkflowStage.RECEIVED,
            WorkflowStage.REASONING,
            WorkflowStage.PRESENTATION,
            WorkflowStage.COMPLETED,
        ),
    )

    assert execution.is_complete is True


def test_operational_workload_evidence_does_not_modify_runtime() -> None:
    platform = CompositionRoot.build()
    platform.runtime.mark_ready()
    platform.runtime.enable_request_admission()

    initial_state = platform.runtime.state
    initial_admission = platform.runtime.is_request_admission_enabled

    platform.application_facade.analyze(())

    assert platform.runtime.state is initial_state
    assert platform.runtime.state is RuntimeState.READY
    assert platform.runtime.is_request_admission_enabled is initial_admission


def test_workload_evidence_does_not_modify_capability_boundaries() -> None:
    platform = CompositionRoot.build()

    policy = platform.mandatory_capability_policy
    observer = platform.availability_observer
    evaluator = platform.mandatory_capability_coverage_evaluator

    policy_state = policy.state
    requirements = policy.required_capabilities
    sources = observer._sources

    platform.application_facade.analyze(())

    assert platform.mandatory_capability_policy is policy
    assert policy.state is policy_state
    assert policy.required_capabilities is requirements
    assert platform.availability_observer is observer
    assert observer._sources is sources
    assert platform.mandatory_capability_coverage_evaluator is evaluator


def test_rfc046_introduces_no_runtime_operational_transition_api() -> None:
    platform = CompositionRoot.build()

    assert not hasattr(platform.runtime, "mark_operational")
    assert not hasattr(platform.runtime, "request_operational")
