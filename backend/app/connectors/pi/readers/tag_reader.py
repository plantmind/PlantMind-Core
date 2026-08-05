"""
PlantMind PI Tag Reader Contract
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class PITagValue:
    """
    Immutable PI tag value.
    """

    tag: str
    value: Any
    timestamp: datetime
    quality: str


class PITagReader(ABC):
    """
    Contract for reading PI tag values.
    """

    @abstractmethod
    def read_current(self, tag: str) -> PITagValue:
        """
        Read the current value of a PI tag.
        """
        ...
