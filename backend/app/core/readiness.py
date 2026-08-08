"""
PlantMind Runtime Readiness

Defines immutable evidence used by Runtime to validate
the READY lifecycle decision.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadinessEvidence:
    """Immutable evidence for Runtime readiness verification."""

    configuration_validated: bool
    runtime_created: bool
    bootstrap_completed: bool
    required_services_initialized: bool
    required_services_validated: bool
    service_registry_operational: bool
    health_capability_initialized: bool
    runtime_metadata_available: bool

    @property
    def is_complete(self) -> bool:
        """Return whether all mandatory readiness evidence is satisfied."""
        return all(
            (
                self.configuration_validated,
                self.runtime_created,
                self.bootstrap_completed,
                self.required_services_initialized,
                self.required_services_validated,
                self.service_registry_operational,
                self.health_capability_initialized,
                self.runtime_metadata_available,
            )
        )
