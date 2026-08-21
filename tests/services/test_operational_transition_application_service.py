from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.core.operational_transition_evidence import OperationalTransitionEvidence
from app.domain.observation import Observation, ObservationType
from app.services.operational_transition_application_service import (
    OperationalTransitionApplicationResult,
    OperationalTransitionApplicationService,
)
from app.services.orchestration.workflow import WorkflowExecution, WorkflowStage
from app.domain.operational_workload_evidence import (
    ApplicationFacadeEntryEvidence,
    OperationalWorkloadEvidence,
    WorkflowExecutionStartEvidence,
)


def make_observations() -> tuple[Observation, ...]:
    return (
        Observation(
            source="PI System",
            observation_type=ObservationType.PROCESS,
            value="Discharge Pressure = 41.2 bar",
            observed_at=datetime.now(UTC),
        ),
    )


def make_workload_evidence() -> OperationalWorkloadEvidence:
    workload_id = uuid4()
    return OperationalWorkloadEvidence(
        facade_entry=ApplicationFacadeEntryEvidence(
            workload_id=workload_id,
        ),
        execution_start=WorkflowExecutionStartEvidence(
            workload_id=workload_id,
        ),
    )


def make_execution(
    workload_evidence: OperationalWorkloadEvidence | None,
) -> WorkflowExecution:
    return WorkflowExecution(
        result={"status": "complete"},
        stages=(WorkflowStage.COMPLETED,),
        operational_workload_evidence=workload_evidence,
    )


class RecordingFacade:
    def __init__(self, execution: WorkflowExecution) -> None:
        self.execution = execution
        self.calls = 0
        self.observations: tuple[Observation, ...] | None = None

    def analyze(
        self,
        observations: tuple[Observation, ...],
    ) -> WorkflowExecution:
        self.calls += 1
        self.observations = observations
        return self.execution


class FailingFacade:
    def __init__(self) -> None:
        self.calls = 0

    def analyze(
        self,
        observations: tuple[Observation, ...],
    ) -> WorkflowExecution:
        self.calls += 1
        raise RuntimeError("workload failure")


class RecordingCoordinator:
    def __init__(
        self,
        transition_evidence: OperationalTransitionEvidence,
    ) -> None:
        self.transition_evidence = transition_evidence
        self.calls = 0
        self.workload_evidence: OperationalWorkloadEvidence | None = None

    def request_operational(
        self,
        workload_evidence: OperationalWorkloadEvidence | None,
    ) -> OperationalTransitionEvidence:
        self.calls += 1
        self.workload_evidence = workload_evidence
        return self.transition_evidence


class FailingCoordinator:
    def __init__(self) -> None:
        self.calls = 0
        self.workload_evidence: OperationalWorkloadEvidence | None = None

    def request_operational(
        self,
        workload_evidence: OperationalWorkloadEvidence | None,
    ) -> OperationalTransitionEvidence:
        self.calls += 1
        self.workload_evidence = workload_evidence
        raise RuntimeError("transition failure")


def make_service(
    facade: object,
    coordinator: object,
) -> OperationalTransitionApplicationService:
    return OperationalTransitionApplicationService(
        application_facade=facade,
        operational_transition_coordinator=coordinator,
    )


def test_application_facade_is_called_exactly_once() -> None:
    workload = make_workload_evidence()
    execution = make_execution(workload)
    facade = RecordingFacade(execution)
    coordinator = RecordingCoordinator(
        OperationalTransitionEvidence(
            operational_workload=workload,
        )
    )
    service = make_service(facade, coordinator)

    service.request_operational(make_observations())

    assert facade.calls == 1


def test_exact_observation_tuple_is_forwarded_to_application_facade() -> None:
    observations = make_observations()
    workload = make_workload_evidence()
    facade = RecordingFacade(make_execution(workload))
    coordinator = RecordingCoordinator(
        OperationalTransitionEvidence(
            operational_workload=workload,
        )
    )
    service = make_service(facade, coordinator)

    service.request_operational(observations)

    assert facade.observations is observations


def test_exact_workload_evidence_is_forwarded_to_coordinator() -> None:
    workload = make_workload_evidence()
    facade = RecordingFacade(make_execution(workload))
    coordinator = RecordingCoordinator(
        OperationalTransitionEvidence(
            operational_workload=workload,
        )
    )
    service = make_service(facade, coordinator)

    service.request_operational(make_observations())

    assert coordinator.workload_evidence is workload


def test_none_workload_evidence_is_forwarded_unchanged() -> None:
    facade = RecordingFacade(make_execution(None))
    transition_evidence = OperationalTransitionEvidence()
    coordinator = RecordingCoordinator(transition_evidence)
    service = make_service(facade, coordinator)

    service.request_operational(make_observations())

    assert coordinator.workload_evidence is None


def test_coordinator_is_called_exactly_once() -> None:
    workload = make_workload_evidence()
    facade = RecordingFacade(make_execution(workload))
    coordinator = RecordingCoordinator(
        OperationalTransitionEvidence(
            operational_workload=workload,
        )
    )
    service = make_service(facade, coordinator)

    service.request_operational(make_observations())

    assert coordinator.calls == 1


def test_result_preserves_exact_execution_and_transition_evidence() -> None:
    workload = make_workload_evidence()
    execution = make_execution(workload)
    transition_evidence = OperationalTransitionEvidence(
        operational_workload=workload,
    )
    facade = RecordingFacade(execution)
    coordinator = RecordingCoordinator(transition_evidence)
    service = make_service(facade, coordinator)

    result = service.request_operational(make_observations())

    assert result.workflow_execution is execution
    assert result.operational_transition_evidence is transition_evidence


def test_application_result_is_immutable() -> None:
    workload = make_workload_evidence()
    execution = make_execution(workload)
    transition_evidence = OperationalTransitionEvidence(
        operational_workload=workload,
    )
    result = OperationalTransitionApplicationResult(
        workflow_execution=execution,
        operational_transition_evidence=transition_evidence,
    )

    with pytest.raises(FrozenInstanceError):
        result.workflow_execution = execution


def test_workload_failure_prevents_coordinator_invocation() -> None:
    facade = FailingFacade()
    coordinator = RecordingCoordinator(
        OperationalTransitionEvidence()
    )
    service = make_service(facade, coordinator)

    with pytest.raises(RuntimeError, match="workload failure"):
        service.request_operational(make_observations())

    assert facade.calls == 1
    assert coordinator.calls == 0


def test_coordinator_failure_propagates_without_retry() -> None:
    workload = make_workload_evidence()
    facade = RecordingFacade(make_execution(workload))
    coordinator = FailingCoordinator()
    service = make_service(facade, coordinator)

    with pytest.raises(RuntimeError, match="transition failure"):
        service.request_operational(make_observations())

    assert facade.calls == 1
    assert coordinator.calls == 1
    assert coordinator.workload_evidence is workload


def test_service_preserves_exact_dependencies() -> None:
    workload = make_workload_evidence()
    facade = RecordingFacade(make_execution(workload))
    coordinator = RecordingCoordinator(
        OperationalTransitionEvidence(
            operational_workload=workload,
        )
    )
    service = make_service(facade, coordinator)

    assert service.application_facade is facade
    assert service.operational_transition_coordinator is coordinator


def test_service_has_no_runtime_or_lifecycle_authority() -> None:
    workload = make_workload_evidence()
    service = make_service(
        RecordingFacade(make_execution(workload)),
        RecordingCoordinator(
            OperationalTransitionEvidence(
                operational_workload=workload,
            )
        ),
    )

    assert not hasattr(service, "runtime")
    assert not hasattr(service, "state")
    assert not hasattr(service, "mark_operational")
    assert not hasattr(service, "enable_request_admission")


def test_service_retains_no_transition_history() -> None:
    workload = make_workload_evidence()
    service = make_service(
        RecordingFacade(make_execution(workload)),
        RecordingCoordinator(
            OperationalTransitionEvidence(
                operational_workload=workload,
            )
        ),
    )

    assert not hasattr(service, "last_execution")
    assert not hasattr(service, "last_evidence")
    assert not hasattr(service, "transition_history")
