"""
PlantMind PI Tag Reader Factory
"""

from __future__ import annotations

from collections.abc import Callable

from app.connectors.pi.readers.tag_reader import PITagReader


ReaderFactory = Callable[[], PITagReader]


class TagReaderFactory:
    """
    Registry-based factory for PI tag readers.
    """

    _registry: dict[str, ReaderFactory] = {}

    @classmethod
    def register(
        cls,
        name: str,
        factory: ReaderFactory,
    ) -> None:
        if name in cls._registry:
            raise ValueError(
                f"Reader '{name}' is already registered."
            )

        cls._registry[name] = factory

    @classmethod
    def create(
        cls,
        name: str,
    ) -> PITagReader:
        try:
            return cls._registry[name]()
        except KeyError as exc:
            raise LookupError(
                f"Unknown PI tag reader '{name}'."
            ) from exc

    @classmethod
    def registered_readers(cls) -> tuple[str, ...]:
        return tuple(sorted(cls._registry))
