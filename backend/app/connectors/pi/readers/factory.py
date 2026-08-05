"""
PlantMind PI Tag Reader Factory
"""

from __future__ import annotations

from collections.abc import Callable

from app.connectors.pi.readers.tag_reader import PITagReader
from app.core.registry.registry import Registry


ReaderFactory = Callable[[], PITagReader]


class TagReaderFactory:
    """
    PI Tag Reader factory built on the generic Registry framework.
    """

    _registry: Registry[PITagReader] = Registry()

    @classmethod
    def register(
        cls,
        name: str,
        factory: ReaderFactory,
    ) -> None:
        cls._registry.register(name, factory)

    @classmethod
    def create(
        cls,
        name: str,
    ) -> PITagReader:
        return cls._registry.resolve(name)

    @classmethod
    def registered_readers(cls) -> tuple[str, ...]:
        return cls._registry.registered()

    @classmethod
    def clear(cls) -> None:
        cls._registry.clear()
