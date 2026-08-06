"""
PlantMind Plugin Contract
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    Base contract for all PlantMind plugins.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the unique plugin name.
        """

    @abstractmethod
    def activate(self) -> None:
        """
        Activate the plugin.
        """

    @abstractmethod
    def deactivate(self) -> None:
        """
        Deactivate the plugin.
        """
