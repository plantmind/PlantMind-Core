"""
PlantMind Service Container

Provides explicit dependency registration and resolution.
"""

from __future__ import annotations

from typing import Any, Callable, TypeVar, cast


T = TypeVar("T")
Factory = Callable[["ServiceContainer"], Any]


class ServiceContainer:
    """
    Lightweight dependency injection container.
    """

    def __init__(self) -> None:
        self._instances: dict[type[Any], Any] = {}
        self._factories: dict[type[Any], Factory] = {}

    def register_instance(
        self,
        service_type: type[T],
        instance: T,
    ) -> None:
        """Register an existing singleton instance."""
        self._ensure_not_registered(service_type)
        self._instances[service_type] = instance

    def register_factory(
        self,
        service_type: type[T],
        factory: Callable[["ServiceContainer"], T],
    ) -> None:
        """Register a factory resolved on each request."""
        self._ensure_not_registered(service_type)
        self._factories[service_type] = factory

    def resolve(self, service_type: type[T]) -> T:
        """Resolve a registered dependency."""
        if service_type in self._instances:
            return cast(T, self._instances[service_type])

        factory = self._factories.get(service_type)

        if factory is not None:
            return cast(T, factory(self))

        raise LookupError(
            f"Service '{service_type.__name__}' is not registered."
        )

    def is_registered(self, service_type: type[Any]) -> bool:
        """Return whether a dependency is registered."""
        return (
            service_type in self._instances
            or service_type in self._factories
        )

    def _ensure_not_registered(
        self,
        service_type: type[Any],
    ) -> None:
        if self.is_registered(service_type):
            raise ValueError(
                f"Service '{service_type.__name__}' is already registered."
            )
