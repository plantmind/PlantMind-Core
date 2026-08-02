"""Structured presentation models for PlantMind reasoning outputs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PresentationSection:
    """One section of a reasoning presentation."""

    heading: str
    items: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.heading.strip():
            raise ValueError("Presentation section heading must not be empty.")

        object.__setattr__(self, "heading", self.heading.strip())
        object.__setattr__(self, "items", tuple(self.items))


@dataclass(frozen=True, slots=True)
class ReasoningPresentation:
    """Presentation-ready PlantMind engineering output."""

    title: str
    summary: str
    risk_level: str
    decision: str
    recommendation: str
    sections: tuple[PresentationSection, ...] = ()

    def __post_init__(self) -> None:
        required = {
            "title": self.title,
            "summary": self.summary,
            "risk_level": self.risk_level,
            "decision": self.decision,
            "recommendation": self.recommendation,
        }

        for field_name, value in required.items():
            if not value.strip():
                raise ValueError(
                    f"Presentation {field_name} must not be empty."
                )

        object.__setattr__(self, "sections", tuple(self.sections))
