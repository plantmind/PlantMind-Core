"""
PlantMind Plugin Exceptions
"""

from __future__ import annotations


class PluginError(Exception):
    """Base plugin exception."""


class PluginIdentityMismatchError(PluginError, ValueError):
    """Raised when registry and runtime plugin identities differ."""


class InvalidPluginVersionError(PluginError, ValueError):
    """Raised when a plugin version violates the version-format contract."""
