"""
PlantMind Runtime State

Defines the official lifecycle states of the PlantMind platform.
"""

from __future__ import annotations

from enum import Enum


class RuntimeState(str, Enum):
    """
    Official lifecycle state of the PlantMind platform.
    """

    CREATED = "created"
    BOOTSTRAPPING = "bootstrapping"
    INITIALIZING = "initializing"
    READY = "ready"
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"