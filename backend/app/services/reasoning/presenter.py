"""Presentation contract for PlantMind output adapters."""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable


SourceT = TypeVar("SourceT", contravariant=True)
ResultT = TypeVar("ResultT", covariant=True)


@runtime_checkable
class Presenter(Protocol[SourceT, ResultT]):
    """Transform a domain result into a presentation format."""

    def present(
        self,
        source: SourceT,
    ) -> ResultT:
        ...
