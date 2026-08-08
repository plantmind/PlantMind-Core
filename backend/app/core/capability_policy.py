from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MandatoryCapabilityPolicyState(str, Enum):
    """Configuration state of the mandatory-capability policy."""

    UNCONFIGURED = "unconfigured"
    CONFIGURED = "configured"


@dataclass(frozen=True)
class MandatoryCapabilityPolicy:
    """Immutable policy defining mandatory PlantMind capabilities."""

    state: MandatoryCapabilityPolicyState
    required_capabilities: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.required_capabilities, tuple):
            raise TypeError(
                "Mandatory capability requirements must be provided as a tuple."
            )

        if (
            self.state is MandatoryCapabilityPolicyState.UNCONFIGURED
            and self.required_capabilities
        ):
            raise ValueError(
                "Unconfigured mandatory capability policy must have no requirements."
            )

        if (
            self.state is MandatoryCapabilityPolicyState.CONFIGURED
            and not self.required_capabilities
        ):
            raise ValueError(
                "Configured mandatory capability policy requires at least one capability."
            )

        seen: set[str] = set()

        for capability_name in self.required_capabilities:
            if not isinstance(capability_name, str):
                raise TypeError("Capability identifiers must be strings.")

            if not capability_name.strip():
                raise ValueError("Capability identifiers must be non-empty.")

            if capability_name != capability_name.strip():
                raise ValueError(
                    "Capability identifiers must not contain leading or trailing whitespace."
                )

            if capability_name in seen:
                raise ValueError(
                    f"Duplicate mandatory capability: {capability_name!r}."
                )

            seen.add(capability_name)
