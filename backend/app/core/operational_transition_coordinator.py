from __future__ import annotations

from app.core.availability import CapabilityAvailabilityObserver
from app.core.capability_coverage import MandatoryCapabilityCoverageEvaluator
from app.core.operational_transition_evidence import OperationalTransitionEvidence
from app.core.runtime import Runtime
from app.services.orchestration.workload_evidence import OperationalWorkloadEvidence


class OperationalTransitionCoordinator:
    """Coordinate operational-transition evidence and delegate to Runtime."""

    def __init__(
        self,
        runtime: Runtime,
        availability_observer: CapabilityAvailabilityObserver,
        coverage_evaluator: MandatoryCapabilityCoverageEvaluator,
    ) -> None:
        self._runtime = runtime
        self._availability_observer = availability_observer
        self._coverage_evaluator = coverage_evaluator

    @property
    def runtime(self) -> Runtime:
        """Return the authoritative Runtime dependency."""
        return self._runtime

    @property
    def availability_observer(self) -> CapabilityAvailabilityObserver:
        """Return the canonical capability availability observer."""
        return self._availability_observer

    @property
    def coverage_evaluator(self) -> MandatoryCapabilityCoverageEvaluator:
        """Return the canonical mandatory-capability coverage evaluator."""
        return self._coverage_evaluator

    def request_operational(
        self,
        workload_evidence: OperationalWorkloadEvidence | None,
    ) -> OperationalTransitionEvidence:
        """Coordinate external evidence and delegate transition authority to Runtime."""
        if (
            workload_evidence is not None
            and not isinstance(workload_evidence, OperationalWorkloadEvidence)
        ):
            raise TypeError(
                "Operational transition coordination requires "
                "OperationalWorkloadEvidence or None."
            )

        observations = self._availability_observer.observe_all()
        coverage = self._coverage_evaluator.evaluate(observations)

        evidence = OperationalTransitionEvidence(
            operational_workload=workload_evidence,
            mandatory_capability_coverage=coverage,
        )

        self._runtime.request_operational(evidence)

        return evidence
