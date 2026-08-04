import logging

from app.core.logging.logging_provider import (
    LoggingProvider,
)


def test_returns_logger() -> None:
    provider = LoggingProvider()

    logger = provider.get_logger("plantmind.test")

    assert isinstance(logger, logging.Logger)


def test_returns_same_logger() -> None:
    provider = LoggingProvider()

    logger1 = provider.get_logger("plantmind.test")
    logger2 = provider.get_logger("plantmind.test")

    assert logger1 is logger2
    assert len(logger1.handlers) == 1
