from app.core.events.event import Event
from app.core.events.event_bus import EventBus


def test_subscribe_and_publish_event() -> None:
    bus = EventBus()
    received: list[Event] = []

    bus.subscribe("equipment.updated", received.append)

    event = Event(name="equipment.updated")
    bus.publish(event)

    assert received == [event]


def test_publish_without_subscribers_is_safe() -> None:
    bus = EventBus()

    bus.publish(Event(name="unhandled.event"))


def test_subscriber_count() -> None:
    bus = EventBus()

    bus.subscribe("alarm.raised", lambda event: None)
    bus.subscribe("alarm.raised", lambda event: None)

    assert bus.subscribers("alarm.raised") == 2
    assert bus.subscribers("alarm.cleared") == 0
