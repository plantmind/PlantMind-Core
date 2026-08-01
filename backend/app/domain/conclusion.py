"""Engineering conclusion produced after reasoning."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.judgment import Judgment


@dataclass(frozen=True, slots=True, kw_only=True)
class Conclusion:
    """
    Final engineering conclusion.

    A Conclusion is the validated engineering outcome produced from a
    Judgment and consumed by downstream components such as
    Recommendation, RCA and Decision Support.
    """

    judgment: Judgment
    summary: str

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError(
                "Conclusion summary must not be empty."
            )