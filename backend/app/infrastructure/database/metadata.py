"""Canonical PlantMind relational schema metadata authority."""

from sqlalchemy.orm import DeclarativeBase


class DatabaseBase(DeclarativeBase):
    """Base for PlantMind infrastructure-owned relational mappings."""

    pass
