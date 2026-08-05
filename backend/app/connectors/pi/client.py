"""
PlantMind PI Client
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PIClientConfiguration:
    """
    PI client configuration.
    """

    endpoint: str | None = None


class PIClient:
    """
    Gateway for future PI Web API communication.
    """

    def __init__(
        self,
        configuration: PIClientConfiguration | None = None,
    ) -> None:
        self.configuration = (
            configuration or PIClientConfiguration()
        )

    @property
    def endpoint(self) -> str | None:
        return self.configuration.endpoint

    def ping(self) -> bool:
        """
        Placeholder connectivity check.

        Real HTTP communication will be implemented
        in a future RFC.
        """

        return True
