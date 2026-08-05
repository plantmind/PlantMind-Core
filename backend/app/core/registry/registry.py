"""
PlantMind Generic Registry
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

from app.core.registry.errors import (
    DuplicateRegistrationError,
    RegistrationNotFoundError,
)

T = TypeVar("T")
Factory = Callable[[], T]


class Registry(Generic[T]):
    """
    Generic self-registering registry.
    """

    def __init__(self) -> None:
        self._entries: dict[str, Factory[T]] = {}

    def register(
        self,
        name: str,
        factory: Factory[T],
    ) -> None:
        if name in self._entries:
            raise DuplicateRegistrationError(
                f"'{name}' is already registered."
            )

        self._entries[name] = factory

    def resolve(self, name: str) -> T:
        try:
            return self._entries[name]()
        except KeyError as exc:
            raise RegistrationNotFoundError(
                f"'{name}' is not registered."
            ) from exc

    def registered(self) -> tuple[str, ...]:
        return tuple(sorted(self._entries))

    def clear(self) -> None:
        self._entries.clear()
