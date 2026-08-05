"""
PlantMind Registry Exceptions
"""

from __future__ import annotations


class RegistryError(Exception):
    """Base registry exception."""


class DuplicateRegistrationError(RegistryError, ValueError):
    """Raised when a key is already registered."""


class RegistrationNotFoundError(RegistryError, LookupError):
    """Raised when a registration cannot be resolved."""
