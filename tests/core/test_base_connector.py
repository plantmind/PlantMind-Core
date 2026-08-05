from app.connectors.base_connector import BaseConnector
from app.connectors.connector_state import ConnectorState


class DummyConnector(BaseConnector):
    def connect(self) -> None:
        self.state = ConnectorState.CONNECTED

    def disconnect(self) -> None:
        self.state = ConnectorState.DISCONNECTED


def test_connector_starts_created() -> None:
    connector = DummyConnector("Dummy")

    assert connector.name == "Dummy"
    assert connector.state is ConnectorState.CREATED
    assert connector.is_connected is False


def test_connector_connect() -> None:
    connector = DummyConnector("Dummy")

    connector.connect()

    assert connector.is_connected is True
    assert connector.state is ConnectorState.CONNECTED


def test_connector_disconnect() -> None:
    connector = DummyConnector("Dummy")

    connector.connect()
    connector.disconnect()

    assert connector.is_connected is False
    assert connector.state is ConnectorState.DISCONNECTED
