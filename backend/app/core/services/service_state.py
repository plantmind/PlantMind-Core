"""
PlantMind Service State
"""

from __future__ import annotations

from enum import Enum


class ServiceState(str, Enum):
    """
    Lifecycle state of a PlantMind Core Service.
    """

    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"