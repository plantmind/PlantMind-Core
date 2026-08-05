"""
PlantMind PI Session Manager
"""

from __future__ import annotations

from dataclasses import dataclass

from app.connectors.connector_state import ConnectorState


@dataclass
class PISession:
    """
    Represents a PI System session.
    """

    endpoint: str | None = None
    state: ConnectorState = ConnectorState.CREATED


class PISessionManager:
    """
    Manages the PI System session lifecycle.
    """

    def __init__(self) -> None:
        self._session = PISession()

    @property
    def session(self) -> PISession:
        return self._session

    def open(self, endpoint: str | None = None) -> None:
        self._session.endpoint = endpoint
        self._session.state = ConnectorState.CONNECTED

    def close(self) -> None:
        self._session.state = ConnectorState.DISCONNECTED

    @property
    def is_open(self) -> bool:
        return self._session.state is ConnectorState.CONNECTED
