"""
PlantMind Composition

Exports the platform composition root.
"""

from app.core.composition.composition_root import (
    CompositionRoot,
    PlatformComposition,
    build_platform_composition,
)

__all__ = [
    "CompositionRoot",
    "PlatformComposition",
    "build_platform_composition",
]