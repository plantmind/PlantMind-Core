"""
PlantMind Event Bus
"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from app.core.events.event import Event


EventHandler = Callable[[Event], None]


class EventBus:
    """
    Simple synchronous event bus.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:
        """
        Register an event handler.
        """

        self._handlers[event_name].append(handler)

    def publish(self, event: Event) -> None:
        """
        Publish an event.
        """

        for handler in self._handlers.get(event.name, []):
            handler(event)

    def subscribers(self, event_name: str) -> int:
        """
        Return subscriber count.
        """

        return len(self._handlers.get(event_name, []))


event_bus = EventBus()
