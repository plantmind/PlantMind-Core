"""
PlantMind Connector State
"""

from __future__ import annotations

from enum import Enum


class ConnectorState(str, Enum):
    """
    Lifecycle state of an industrial connector.
    """

    CREATED = "created"
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DEGRADED = "degraded"
    FAILED = "failed"
