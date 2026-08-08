from __future__ import annotations

from dataclasses import dataclass

from app.core.capability_coverage import (
    MandatoryCapabilityCoverageResult,
    MandatoryCapabilityCoverageState,
)
from app.services.orchestration.workload_evidence import (
    OperationalWorkloadEvidence,
)


@dataclass(frozen=True, slots=True)
class OperationalTransitionEvidence:
    """Immutable aggregate of external operational-transition evidence."""

    operational_workload: OperationalWorkloadEvidence | None = None
    mandatory_capability_coverage: MandatoryCapabilityCoverageResult | None = None

    @property
    def is_complete(self) -> bool:
        """Return whether all required external evidence is complete."""
        return (
            self.operational_workload is not None
            and self.mandatory_capability_coverage is not None
            and self.mandatory_capability_coverage.state
            is MandatoryCapabilityCoverageState.SATISFIED
        )
