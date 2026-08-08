from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from app.core.availability import (
    CapabilityAvailabilityObservation,
    CapabilityAvailabilityState,
)
from app.core.capability_policy import (
    MandatoryCapabilityPolicy,
    MandatoryCapabilityPolicyState,
)


class MandatoryCapabilityCoverageState(str, Enum):
    """Coverage state for mandatory capability requirements."""

    SATISFIED = "satisfied"
    UNSATISFIED = "unsatisfied"


@dataclass(frozen=True)
class MandatoryCapabilityCoverageResult:
    """Immutable diagnostic result of mandatory capability coverage."""

    state: MandatoryCapabilityCoverageState
    required_capabilities: tuple[str, ...]
    satisfied_capabilities: tuple[str, ...]
    missing_capabilities: tuple[str, ...]
    unavailable_capabilities: tuple[str, ...]
    unknown_capabilities: tuple[str, ...]
    ambiguous_capabilities: tuple[str, ...]


class MandatoryCapabilityCoverageEvaluator:
    """Read-only evaluator for mandatory capability availability coverage."""

    def __init__(
        self,
        policy: MandatoryCapabilityPolicy,
    ) -> None:
        self._policy = policy

    def evaluate(
        self,
        observations: Sequence[CapabilityAvailabilityObservation],
    ) -> MandatoryCapabilityCoverageResult:
        """Evaluate supplied availability evidence against mandatory policy."""

        if self._policy.state is MandatoryCapabilityPolicyState.UNCONFIGURED:
            return MandatoryCapabilityCoverageResult(
                state=MandatoryCapabilityCoverageState.UNSATISFIED,
                required_capabilities=(),
                satisfied_capabilities=(),
                missing_capabilities=(),
                unavailable_capabilities=(),
                unknown_capabilities=(),
                ambiguous_capabilities=(),
            )

        observation_snapshot = tuple(observations)

        satisfied: list[str] = []
        missing: list[str] = []
        unavailable: list[str] = []
        unknown: list[str] = []
        ambiguous: list[str] = []

        for capability_name in self._policy.required_capabilities:
            matches = tuple(
                observation
                for observation in observation_snapshot
                if observation.capability_name == capability_name
            )

            if not matches:
                missing.append(capability_name)
                continue

            if len(matches) > 1:
                ambiguous.append(capability_name)
                continue

            state = matches[0].state

            if state is CapabilityAvailabilityState.AVAILABLE:
                satisfied.append(capability_name)
            elif state is CapabilityAvailabilityState.UNAVAILABLE:
                unavailable.append(capability_name)
            else:
                unknown.append(capability_name)

        coverage_state = (
            MandatoryCapabilityCoverageState.SATISFIED
            if len(satisfied) == len(self._policy.required_capabilities)
            else MandatoryCapabilityCoverageState.UNSATISFIED
        )

        return MandatoryCapabilityCoverageResult(
            state=coverage_state,
            required_capabilities=self._policy.required_capabilities,
            satisfied_capabilities=tuple(satisfied),
            missing_capabilities=tuple(missing),
            unavailable_capabilities=tuple(unavailable),
            unknown_capabilities=tuple(unknown),
            ambiguous_capabilities=tuple(ambiguous),
        )
