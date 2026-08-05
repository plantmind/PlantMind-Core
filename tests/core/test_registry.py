import pytest

from app.core.registry.errors import (
    DuplicateRegistrationError,
    RegistrationNotFoundError,
)
from app.core.registry.registry import Registry


def test_register_and_resolve() -> None:
    registry: Registry[int] = Registry()

    registry.register("one", lambda: 1)

    assert registry.resolve("one") == 1
    assert registry.registered() == ("one",)


def test_duplicate_registration() -> None:
    registry: Registry[int] = Registry()

    registry.register("one", lambda: 1)

    with pytest.raises(DuplicateRegistrationError):
        registry.register("one", lambda: 2)


def test_missing_registration() -> None:
    registry: Registry[int] = Registry()

    with pytest.raises(RegistrationNotFoundError):
        registry.resolve("missing")


def test_clear_registry() -> None:
    registry: Registry[int] = Registry()

    registry.register("one", lambda: 1)
    registry.clear()

    assert registry.registered() == ()
