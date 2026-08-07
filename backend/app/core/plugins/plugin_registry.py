"""
PlantMind Plugin Registry
"""

from __future__ import annotations

from collections.abc import Callable

from app.core.plugins.errors import PluginIdentityMismatchError
from app.core.plugins.plugin import Plugin
from app.core.plugins.plugin_metadata import PluginMetadata
from app.core.registry import Registry


PluginFactory = Callable[[], Plugin]


class PluginRegistry:
    """Registry-backed manager for PlantMind plugins."""

    def __init__(self) -> None:
        self._registry: Registry[Plugin] = Registry()
        self._metadata: dict[str, PluginMetadata] = {}

    def register(
        self,
        name: str,
        factory: PluginFactory,
        metadata: PluginMetadata | None = None,
    ) -> None:
        """Register a plugin factory and optional metadata."""

        self._registry.register(name, factory)

        if metadata is not None:
            self._metadata[name] = metadata

    def create(self, name: str) -> Plugin:
        """Create a registered plugin instance."""

        plugin = self._registry.resolve(name)

        if plugin.name != name:
            raise PluginIdentityMismatchError(
                f"Plugin identity mismatch: registered as '{name}' "
                f"but instance reports '{plugin.name}'."
            )

        return plugin

    def metadata(self, name: str) -> PluginMetadata | None:
        """Return metadata associated with a plugin registration."""

        return self._metadata.get(name)

    def registered(self) -> tuple[str, ...]:
        """Return registered plugin names."""

        return self._registry.registered()

    def clear(self) -> None:
        """Clear all plugin registrations and associated metadata."""

        self._registry.clear()
        self._metadata.clear()
