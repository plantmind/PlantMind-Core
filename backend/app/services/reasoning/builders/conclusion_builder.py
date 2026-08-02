"""Build engineering conclusions from engineering judgments."""

from __future__ import annotations

from app.domain.conclusion import Conclusion
from app.domain.judgment import Judgment


class ConclusionBuilder:
    """
    Transform an engineering judgment into a final engineering
    conclusion.
    """

    def build(
        self,
        judgment: Judgment,
    ) -> Conclusion:
        return Conclusion(
            judgment=judgment,
            summary=judgment.summary,
        )