"""
PlantMind Plugin Framework
"""

from app.core.plugins.plugin import Plugin
from app.core.plugins.errors import PluginIdentityMismatchError
from app.core.plugins.plugin_metadata import PluginMetadata
from app.core.plugins.plugin_lifecycle_manager import (
    PluginLifecycleManager,
)
from app.core.plugins.plugin_registration import (
    PluginRegistration,
)
from app.core.plugins.plugin_registry import (
    PluginFactory,
    PluginRegistry,
)

__all__ = [
    "Plugin",
    "PluginIdentityMismatchError",
    "PluginMetadata",
    "PluginFactory",
    "PluginRegistration",
    "PluginRegistry",
    "PluginLifecycleManager",
]
