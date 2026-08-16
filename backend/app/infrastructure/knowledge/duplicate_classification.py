"""Canonical Knowledge relational duplicate classification."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError


_IDENTITY_UNIQUE_SQLSTATE = "23505"
_IDENTITY_CONSTRAINT_NAME = "pk_knowledge_records"


def is_identity_duplicate(
    error: IntegrityError,
) -> bool:
    """Identify only the canonical Knowledge primary-key conflict."""

    driver_error = error.orig

    if (
        getattr(driver_error, "sqlstate", None)
        != _IDENTITY_UNIQUE_SQLSTATE
    ):
        return False

    diagnostic = getattr(
        driver_error,
        "diag",
        None,
    )

    return (
        getattr(
            diagnostic,
            "constraint_name",
            None,
        )
        == _IDENTITY_CONSTRAINT_NAME
    )
