"""
PlantMind Registry Exceptions
"""

from __future__ import annotations


class RegistryError(Exception):
    """Base registry exception."""


class DuplicateRegistrationError(RegistryError):
    """Raised when a key is already registered."""


class RegistrationNotFoundError(RegistryError):
    """Raised when a registration cannot be resolved."""
