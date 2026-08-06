from app.core.plugins import Plugin, PluginRegistry
from app.core.registry.errors import (
    DuplicateRegistrationError,
    RegistrationNotFoundError,
)


class MockPlugin(Plugin):
    @property
    def name(self) -> str:
        return "mock"

    def activate(self) -> None:
        pass

    def deactivate(self) -> None:
        pass


def test_register_and_create_plugin() -> None:
    registry = PluginRegistry()

    registry.register("mock", MockPlugin)

    plugin = registry.create("mock")

    assert isinstance(plugin, MockPlugin)
    assert plugin.name == "mock"


def test_duplicate_registration_raises() -> None:
    registry = PluginRegistry()

    registry.register("mock", MockPlugin)

    try:
        registry.register("mock", MockPlugin)
        assert False
    except DuplicateRegistrationError:
        assert True


def test_unknown_plugin_raises() -> None:
    registry = PluginRegistry()

    try:
        registry.create("unknown")
        assert False
    except RegistrationNotFoundError:
        assert True


def test_registered_plugins() -> None:
    registry = PluginRegistry()

    registry.register("mock", MockPlugin)

    assert registry.registered() == ("mock",)


def test_clear_registry() -> None:
    registry = PluginRegistry()

    registry.register("mock", MockPlugin)

    registry.clear()

    assert registry.registered() == ()