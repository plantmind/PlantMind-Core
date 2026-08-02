"""Present a reasoning presentation as an API-ready dictionary."""

from __future__ import annotations

from app.services.reasoning.presentation import ReasoningPresentation


class ReportPresenter:
    """Serialize reasoning presentations for API or UI consumption."""

    def present(
        self,
        source: ReasoningPresentation,
    ) -> dict[str, object]:
        return {
            "title": source.title,
            "summary": source.summary,
            "risk_level": source.risk_level,
            "decision": source.decision,
            "recommendation": source.recommendation,
            "sections": [
                {
                    "heading": section.heading,
                    "items": list(section.items),
                }
                for section in source.sections
            ],
        }
