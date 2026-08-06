"""
PlantMind Plugin Lifecycle Manager
"""

from __future__ import annotations

from app.core.plugins.plugin import Plugin
from app.core.plugins.plugin_registry import PluginRegistry


class PluginLifecycleManager:
    """
    Manages plugin activation and deactivation lifecycle.
    """

    def __init__(
        self,
        registry: PluginRegistry,
    ) -> None:
        self._registry = registry
        self._active_plugins: list[Plugin] = []

    def activate_all(self) -> None:
        """
        Create and activate all registered plugins.
        """

        if self._active_plugins:
            return

        for name in self._registry.registered():
            plugin = self._registry.create(name)
            plugin.activate()
            self._active_plugins.append(plugin)

    def deactivate_all(self) -> None:
        """
        Deactivate all active plugins in reverse order.
        """

        for plugin in reversed(self._active_plugins):
            plugin.deactivate()

        self._active_plugins.clear()

    def active_plugin_names(self) -> tuple[str, ...]:
        """
        Return currently active plugin names.
        """

        return tuple(
            plugin.name
            for plugin in self._active_plugins
        )