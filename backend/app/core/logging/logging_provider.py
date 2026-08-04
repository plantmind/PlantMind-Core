"""
PlantMind Logging Provider

Provides centralized and idempotent logging configuration.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass


@dataclass(frozen=True)
class LoggingConfiguration:
    """Immutable logging configuration."""

    level: int = logging.INFO
    format: str = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )


class LoggingProvider:
    """Configure and provide PlantMind loggers."""

    def __init__(
        self,
        configuration: LoggingConfiguration | None = None,
    ) -> None:
        self.configuration = configuration or LoggingConfiguration()
        self._configured_loggers: set[str] = set()

    def get_logger(self, name: str) -> logging.Logger:
        """Return a configured logger."""

        logger = logging.getLogger(name)

        if name not in self._configured_loggers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(self.configuration.format)
            )

            logger.handlers.clear()
            logger.addHandler(handler)
            logger.setLevel(self.configuration.level)
            logger.propagate = False

            self._configured_loggers.add(name)

        return logger


logging_provider = LoggingProvider()
