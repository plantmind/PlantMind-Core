from app.connectors.connector_state import ConnectorState
from app.connectors.pi.session import PISessionManager


def test_session_starts_closed() -> None:
    manager = PISessionManager()

    assert manager.session.state is ConnectorState.CREATED
    assert manager.is_open is False


def test_open_session() -> None:
    manager = PISessionManager()

    manager.open("https://pi-server")

    assert manager.is_open is True
    assert manager.session.endpoint == "https://pi-server"
    assert manager.session.state is ConnectorState.CONNECTED


def test_close_session() -> None:
    manager = PISessionManager()

    manager.open("https://pi-server")
    manager.close()

    assert manager.is_open is False
    assert manager.session.state is ConnectorState.DISCONNECTED
