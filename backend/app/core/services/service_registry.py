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

    def __init__(self):
        self._services: Dict[str, BaseService] = {}

    def register(self, service: BaseService) -> None:
        """
        Register a Core Service.
        """

        self._services[service.name] = service

    def get(self, name: str) -> BaseService | None:
        """
        Retrieve a registered service.
        """

        return self._services.get(name)

    def registered_services(self) -> list[str]:
        """
        Return registered service names.
        """

        return sorted(self._services.keys())