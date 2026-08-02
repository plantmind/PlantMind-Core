from app.services.orchestration.workflow import (
    WorkflowExecution,
    WorkflowStage,
)


def test_workflow_execution_reports_completion() -> None:
    execution = WorkflowExecution(
        result={"status": "ready"},
        stages=(
            WorkflowStage.RECEIVED,
            WorkflowStage.COMPLETED,
        ),
    )

    assert execution.is_complete is True
    assert execution.result["status"] == "ready"


def test_incomplete_workflow_is_reported() -> None:
    execution = WorkflowExecution(
        result={},
        stages=(WorkflowStage.RECEIVED,),
    )

    assert execution.is_complete is False