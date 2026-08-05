"""
PlantMind Base Connector
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.connectors.connector_state import ConnectorState


class BaseConnector(ABC):
    """
    Base contract for all industrial connectors.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.state = ConnectorState.CREATED

    @abstractmethod
    def connect(self) -> None:
        """
        Establish the external connection.
        """

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the external connection.
        """

    @property
    def is_connected(self) -> bool:
        """
        Return connection status.
        """

        return self.state is ConnectorState.CONNECTED
