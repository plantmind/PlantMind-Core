"""
PlantMind PI System Connector

Initial lifecycle implementation for future PI Web API integration.
"""

from __future__ import annotations

from app.connectors.base_connector import BaseConnector
from app.connectors.connector_state import ConnectorState


class PIConnector(BaseConnector):
    """
    PI System industrial connector.

    Network communication will be introduced in a later RFC.
    """

    def __init__(
        self,
        endpoint: str | None = None,
    ) -> None:
        super().__init__(name="PI System")
        self.endpoint = endpoint

    def connect(self) -> None:
        """
        Transition the connector into the connected state.
        """

        self.state = ConnectorState.CONNECTING

        try:
            self._validate_configuration()
            self.state = ConnectorState.CONNECTED
        except Exception:
            self.state = ConnectorState.FAILED
            raise

    def disconnect(self) -> None:
        """
        Transition the connector into the disconnected state.
        """

        self.state = ConnectorState.DISCONNECTED

    def _validate_configuration(self) -> None:
        """
        Validate connector configuration.

        Endpoint remains optional until PI Web API integration is enabled.
        """

        if self.endpoint is not None and not self.endpoint.strip():
            raise ValueError("PI System endpoint cannot be empty.")
