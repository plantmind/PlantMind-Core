"""
PlantMind Plugin Metadata Contract
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import ClassVar

from app.core.plugins.errors import InvalidPluginVersionError


_PLUGIN_VERSION_PATTERN = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


@dataclass(frozen=True)
class PluginMetadata:
    """Immutable metadata associated with a plugin registration."""

    contract_version: ClassVar[str] = "1.0"
    plugin_version: str

    def __post_init__(self) -> None:
        if _PLUGIN_VERSION_PATTERN.fullmatch(self.plugin_version) is None:
            raise InvalidPluginVersionError(
                f"Invalid plugin version: {self.plugin_version!r}."
            )
