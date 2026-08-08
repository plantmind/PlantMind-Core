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
        """Deactivate all active plugins in reverse order."""

        failures: list[tuple[Plugin, Exception]] = []

        for plugin in reversed(self._active_plugins):
            try:
                plugin.deactivate()
            except Exception as exc:
                failures.append((plugin, exc))

        failed_plugins = [
            plugin
            for plugin, _ in failures
        ]

        self._active_plugins = [
            plugin
            for plugin in self._active_plugins
            if any(
                plugin is failed_plugin
                for failed_plugin in failed_plugins
            )
        ]

        if len(failures) == 1:
            raise failures[0][1]

        if failures:
            raise ExceptionGroup(
                "Plugin deactivation failures",
                [
                    error
                    for _, error in failures
                ],
            )

    def active_plugin_names(self) -> tuple[str, ...]:
        """
        Return currently active plugin names.
        """

        return tuple(
            plugin.name
            for plugin in self._active_plugins
        )