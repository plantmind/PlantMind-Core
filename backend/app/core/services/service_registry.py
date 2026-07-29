"""
PlantMind Service Registry

Central registry responsible for managing the lifecycle
of all PlantMind Core Services.
"""

from __future__ import annotations

from typing import Dict

from app.core.services import BaseService


class ServiceRegistry:
    """
    Central registry for all PlantMind Core Services.
    """

    def __init__(self) -> None:
        self._services: Dict[str, BaseService] = {}

    def register(self, service: BaseService) -> None:
        """
        Register a Core Service.
        """

        if service.name in self._services:
            raise ValueError(
                f"Service '{service.name}' is already registered."
            )

        self._services[service.name] = service

    def get(self, name: str) -> BaseService | None:
        """
        Retrieve a registered service.
        """

        return self._services.get(name)

    def exists(self, name: str) -> bool:
        """
        Check whether a service is registered.
        """

        return name in self._services

    def unregister(self, name: str) -> None:
        """
        Remove a registered service.
        """

        self._services.pop(name, None)

    def registered_services(self) -> list[str]:
        """
        Return registered service names.
        """

        return sorted(self._services.keys())

    @property
    def count(self) -> int:
        """
        Return total number of registered services.
        """

        return len(self._services)