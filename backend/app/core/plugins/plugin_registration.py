"""
PlantMind Plugin Registration
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.plugins.plugin_metadata import PluginMetadata
from app.core.plugins.plugin_registry import PluginFactory


@dataclass(frozen=True)
class PluginRegistration:
    """Immutable declaration for a controlled plugin registration."""

    name: str
    factory: PluginFactory
    metadata: PluginMetadata | None = None
