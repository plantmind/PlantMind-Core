"""Canonical enterprise Document domain contracts for PlantMind."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.base import DomainEntity, DomainException, EntityId


def _normalize_open_classification(
    value: str,
    *,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise DomainException(
            f"{field_name} must be a string."
        )

    normalized = value.strip().lower()

    if not normalized:
        raise DomainException(
            f"{field_name} must not be empty."
        )

    return normalized


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentType:
    """Open immutable classification of an enterprise Document."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_open_classification(
                self.value,
                field_name="Document type",
            ),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentSourceType:
    """Open immutable classification of a Document source."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_open_classification(
                self.value,
                field_name="Document source type",
            ),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentSource:
    """Immutable traceable source reference for an enterprise Document."""

    source_type: DocumentSourceType
    source_reference: str

    def __post_init__(self) -> None:
        if not isinstance(
            self.source_type,
            DocumentSourceType,
        ):
            raise DomainException(
                "Document source type must be a DocumentSourceType."
            )

        if not isinstance(self.source_reference, str):
            raise DomainException(
                "Document source reference must be a string."
            )

        source_reference = self.source_reference.strip()

        if not source_reference:
            raise DomainException(
                "Document source reference must not be empty."
            )

        object.__setattr__(
            self,
            "source_reference",
            source_reference,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class EnterpriseDocument(DomainEntity[EntityId]):
    """Immutable canonical enterprise Document record."""

    document_type: DocumentType
    title: str
    source: DocumentSource

    def __post_init__(self) -> None:
        if not isinstance(self.id, EntityId):
            raise DomainException(
                "Enterprise Document id must be an EntityId."
            )

        if not isinstance(
            self.document_type,
            DocumentType,
        ):
            raise DomainException(
                "Enterprise Document type must be a DocumentType."
            )

        if not isinstance(self.title, str):
            raise DomainException(
                "Enterprise Document title must be a string."
            )

        if not isinstance(
            self.source,
            DocumentSource,
        ):
            raise DomainException(
                "Enterprise Document source must be a DocumentSource."
            )

        title = self.title.strip()

        if not title:
            raise DomainException(
                "Enterprise Document title must not be empty."
            )

        object.__setattr__(
            self,
            "title",
            title,
        )
