"""Generate complete presentation-ready PlantMind reasoning output."""

from __future__ import annotations

from app.domain.observation import Observation
from app.services.reasoning.presentation_builder import PresentationBuilder
from app.services.reasoning.report_generator import ReportGenerator
from app.services.reasoning.report_presenter import ReportPresenter


class PresentationService:
    """Coordinate report generation, presentation building and serialization."""

    def __init__(self) -> None:
        self._report_generator = ReportGenerator()
        self._presentation_builder = PresentationBuilder()
        self._presenter = ReportPresenter()

    def generate(
        self,
        observations: tuple[Observation, ...],
    ) -> dict[str, object]:
        report = self._report_generator.generate(observations)
        presentation = self._presentation_builder.build(report)

        return self._presenter.present(presentation)
