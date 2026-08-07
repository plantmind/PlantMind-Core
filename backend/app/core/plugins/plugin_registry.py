"""
PlantMind Plugin Registry
"""

from __future__ import annotations

from collections.abc import Callable

from app.core.plugins.errors import PluginIdentityMismatchError
from app.core.plugins.plugin import Plugin
from app.core.registry import Registry


PluginFactory = Callable[[], Plugin]


class PluginRegistry:
    """
    Registry-backed manager for PlantMind plugins.
    """

    def __init__(self) -> None:
        self._registry: Registry[Plugin] = Registry()

    def register(
        self,
        name: str,
        factory: PluginFactory,
    ) -> None:
        """
        Register a plugin factory.
        """

        self._registry.register(name, factory)

    def create(self, name: str) -> Plugin:
        """
        Create a registered plugin instance.
        """

        plugin = self._registry.resolve(name)

        if plugin.name != name:
            raise PluginIdentityMismatchError(
                f"Plugin identity mismatch: registered as '{name}' "
                f"but instance reports '{plugin.name}'."
            )

        return plugin

    def registered(self) -> tuple[str, ...]:
        """
        Return registered plugin names.
        """

        return self._registry.registered()

    def clear(self) -> None:
        """
        Clear all plugin registrations.
        """

        self._registry.clear()
