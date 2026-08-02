from app.services.integration_gateway import IntegrationGateway
from app.services.orchestration.workflow import WorkflowStage


def test_integration_gateway_executes_workflow() -> None:
    execution = IntegrationGateway().execute(())

    assert execution.is_complete is True
    assert execution.stages[-1] is WorkflowStage.COMPLETED
    assert execution.result["risk_level"] == "low"