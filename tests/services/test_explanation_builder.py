from app.domain.conclusion import Conclusion
from app.domain.context import EngineeringContext
from app.domain.decision import Decision, DecisionType
from app.domain.judgment import Judgment, JudgmentLevel
from app.domain.recommendation import (
    Recommendation,
    RecommendationPriority,
)
from app.domain.risk_assessment import RiskAssessment, RiskLevel
from app.services.reasoning.explanation_builder import ExplanationBuilder
from app.services.reasoning.result import ReasoningResult
from app.services.reasoning.trace import (
    ReasoningTrace,
    TraceStep,
)


def test_explanation_builder_creates_explanation() -> None:
    context = EngineeringContext()

    risk = RiskAssessment(
        context=context,
        level=RiskLevel.MEDIUM,
        score=0.40,
        rationale="Baseline assessment.",
    )

    judgment = Judgment(
        context=context,
        level=JudgmentLevel.CAUTION,
        summary="Engineering review recommended.",
        confidence=0.60,
    )

    conclusion = Conclusion(
        judgment=judgment,
        summary=judgment.summary,
    )

    decision = Decision(
        judgment=judgment,
        decision_type=DecisionType.INVESTIGATE,
        rationale="Investigate operating conditions.",
    )

    recommendation = Recommendation(
        decision=decision,
        priority=RecommendationPriority.MEDIUM,
        title="Review engineering decision",
        description="Investigate operating conditions.",
    )

    result = ReasoningResult(
        context=context,
        risk=risk,
        judgment=judgment,
        conclusion=conclusion,
        decision=decision,
        recommendation=recommendation,
    )

    trace = ReasoningTrace(
        result=result,
        steps=(
            TraceStep(
                name="ContextBuilder",
                description="Engineering context created.",
            ),
            TraceStep(
                name="RiskBuilder",
                description="Risk assessment completed.",
            ),
        ),
    )

    explanation = ExplanationBuilder().build(trace)

    assert explanation.title == "PlantMind Engineering Analysis"
    assert explanation.summary == judgment.summary
    assert len(explanation.details) == 2
    assert explanation.details[0].startswith("ContextBuilder")