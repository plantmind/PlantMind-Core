from app.domain.conclusion import Conclusion
from app.domain.context import EngineeringContext
from app.domain.decision import Decision, DecisionType
from app.domain.judgment import Judgment, JudgmentLevel
from app.domain.recommendation import (
    Recommendation,
    RecommendationPriority,
)
from app.domain.risk_assessment import RiskAssessment, RiskLevel
from app.services.reasoning.explanation import Explanation
from app.services.reasoning.report_builder import ReportBuilder
from app.services.reasoning.result import ReasoningResult


def test_report_builder_creates_report() -> None:
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

    explanation = Explanation(
        title="Engineering Analysis",
        summary="Operating conditions require investigation.",
        details=("Evidence collected.",),
    )

    report = ReportBuilder().build(
        result=result,
        explanation=explanation,
    )

    assert report.result is result
    assert report.explanation is explanation
    assert report.explanation.summary == (
        "Operating conditions require investigation."
    )