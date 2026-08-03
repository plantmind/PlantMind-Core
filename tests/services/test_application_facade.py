from app.services.application_facade import ApplicationFacade
from app.services.orchestration.workflow import WorkflowStage


def test_application_facade_runs_complete_analysis() -> None:
    execution = ApplicationFacade().analyze(())

    assert execution.is_complete is True
    assert execution.stages[-1] is WorkflowStage.COMPLETED
    assert execution.result["risk_level"] == "low"