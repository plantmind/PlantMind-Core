"""
PlantMind Bootstrap Compatibility Module

Preserves the legacy import path while exposing the authoritative
BootstrapManager implementation.
"""

from __future__ import annotations

from app.core.bootstrap_manager import (
    BootstrapManager,
    bootstrap_manager,
)

__all__ = [
    "BootstrapManager",
    "bootstrap_manager",
]