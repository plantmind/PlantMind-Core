"""
PlantMind Base Service

Defines the lifecycle contract that every Core Service
must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseService(ABC):
    """
    Base contract for all PlantMind Core Services.
    """

    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version
        self.ready = False

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the service.
        """
        ...

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate service configuration and dependencies.
        """
        ...

    @abstractmethod
    def shutdown(self) -> None:
        """
        Gracefully stop the service.
        """
        ...

    def status(self) -> dict:
        """
        Return current service status.
        """
        return {
            "name": self.name,
            "version": self.version,
            "ready": self.ready,
        }