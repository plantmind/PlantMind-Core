"""Traceable reasoning execution."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.services.reasoning.result import ReasoningResult


@dataclass(frozen=True, slots=True)
class TraceStep:
    """One step executed by the reasoning pipeline."""

    name: str
    description: str


@dataclass(frozen=True, slots=True)
class ReasoningTrace:
    """
    Complete execution trace for one reasoning run.
    """

    result: ReasoningResult
    steps: tuple[TraceStep, ...] = field(default_factory=tuple)