from datetime import datetime, timezone

from app.domain.observation import Observation, ObservationType
from app.services.orchestration.workflow import WorkflowStage
from app.services.orchestration.workflow_executor import WorkflowExecutor


def test_workflow_executor_runs_complete_workflow() -> None:
    observation = Observation(
        source="PI System",
        observation_type=ObservationType.ALARM,
        value="PAHH-1001 active.",
        observed_at=datetime.now(timezone.utc),
    )

    execution = WorkflowExecutor().execute((observation,))

    assert execution.is_complete is True
    assert execution.stages == (
        WorkflowStage.RECEIVED,
        WorkflowStage.REASONING,
        WorkflowStage.PRESENTATION,
        WorkflowStage.COMPLETED,
    )
    assert execution.result["title"] == "PlantMind Engineering Analysis"