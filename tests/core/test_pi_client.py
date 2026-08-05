from app.connectors.pi.client import (
    PIClient,
    PIClientConfiguration,
)


def test_default_configuration() -> None:
    client = PIClient()

    assert client.endpoint is None


def test_custom_configuration() -> None:
    client = PIClient(
        PIClientConfiguration(
            endpoint="https://pi-server"
        )
    )

    assert client.endpoint == "https://pi-server"


def test_ping_returns_true() -> None:
    client = PIClient()

    assert client.ping() is True
