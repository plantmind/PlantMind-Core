"""
PlantMind Plugin Metadata Contract
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class PluginMetadata:
    """Immutable metadata associated with a plugin registration."""

    contract_version: ClassVar[str] = "1.0"
    plugin_version: str
