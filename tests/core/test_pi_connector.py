from app.connectors.connector_state import ConnectorState
from app.connectors.pi_connector import PIConnector


def test_pi_connector_initial_state() -> None:
    connector = PIConnector()

    assert connector.name == "PI System"
    assert connector.state is ConnectorState.CREATED
    assert connector.is_connected is False


def test_pi_connector_connect() -> None:
    connector = PIConnector()

    connector.connect()

    assert connector.state is ConnectorState.CONNECTED
    assert connector.is_connected is True


def test_pi_connector_disconnect() -> None:
    connector = PIConnector()

    connector.connect()
    connector.disconnect()

    assert connector.state is ConnectorState.DISCONNECTED
    assert connector.is_connected is False


def test_invalid_endpoint_raises_error() -> None:
    connector = PIConnector(endpoint="   ")

    try:
        connector.connect()
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
