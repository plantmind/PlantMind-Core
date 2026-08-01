"""Shared domain primitives for PlantMind."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4


class DomainException(Exception):
    """Base exception for all domain rule violations."""


@dataclass(frozen=True, slots=True)
class EntityId:
    """Immutable identifier shared by PlantMind domain entities."""

    value: UUID

    @classmethod
    def new(cls) -> "EntityId":
        """Create a new unique entity identifier."""
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, value: str) -> "EntityId":
        """Create an identifier from its string representation."""
        try:
            return cls(value=UUID(value))
        except (ValueError, AttributeError, TypeError) as exc:
            raise DomainException(f"Invalid entity identifier: {value!r}") from exc

    def __str__(self) -> str:
        return str(self.value)


IdT = TypeVar("IdT", bound=EntityId)


@dataclass(frozen=True, slots=True, kw_only=True)
class DomainEntity(Generic[IdT]):
    """Base class for immutable PlantMind domain entities."""

    id: IdT