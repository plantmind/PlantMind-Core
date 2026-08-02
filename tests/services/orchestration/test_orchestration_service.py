from app.services.orchestration.orchestration_service import (
    OrchestrationService,
)
from app.services.orchestration.workflow import WorkflowStage


def test_orchestration_service_is_unified_entry_point() -> None:
    execution = OrchestrationService().run(())

    assert execution.is_complete is True
    assert execution.stages[-1] is WorkflowStage.COMPLETED
    assert execution.result["risk_level"] == "low"
    assert execution.result["sections"][0]["items"] == []