"""Canonical enterprise Document Content domain contracts for PlantMind."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.base import DomainException, EntityId


_ASCII_WHITESPACE = " \t\n\r\v\f"
_HEXADECIMAL_CHARACTERS = frozenset("0123456789abcdef")


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentMediaType:
    """Immutable media-type classification for canonical Document content."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise DomainException(
                "Document content media type must be a string."
            )

        normalized = self.value.strip().lower()

        if not normalized:
            raise DomainException(
                "Document content media type must not be empty."
            )

        if ";" in normalized:
            raise DomainException(
                "Document content media type must not contain parameters."
            )

        if normalized.count("/") != 1:
            raise DomainException(
                "Document content media type must contain exactly one '/'."
            )

        media_type, media_subtype = normalized.split("/", 1)

        if not media_type or not media_subtype:
            raise DomainException(
                "Document content media type must contain non-empty "
                "type and subtype."
            )

        if any(
            character in normalized
            for character in _ASCII_WHITESPACE
        ):
            raise DomainException(
                "Document content media type must not contain "
                "ASCII whitespace."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentDigest:
    """Immutable SHA-256 integrity descriptor for Document content."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise DomainException(
                "Document content digest must be a string."
            )

        normalized = self.value.strip().lower()

        if (
            len(normalized) != 64
            or any(
                character not in _HEXADECIMAL_CHARACTERS
                for character in normalized
            )
        ):
            raise DomainException(
                "Document content digest must contain exactly "
                "64 hexadecimal characters."
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class DocumentContentDescriptor:
    """Immutable canonical descriptor of Enterprise Document content."""

    document_id: EntityId
    media_type: DocumentContentMediaType
    byte_length: int
    digest: DocumentContentDigest

    def __post_init__(self) -> None:
        if not isinstance(self.document_id, EntityId):
            raise DomainException(
                "Document content document id must be an EntityId."
            )

        if not isinstance(
            self.media_type,
            DocumentContentMediaType,
        ):
            raise DomainException(
                "Document content media type must be "
                "a DocumentContentMediaType."
            )

        if (
            isinstance(self.byte_length, bool)
            or not isinstance(self.byte_length, int)
        ):
            raise DomainException(
                "Document content byte length must be an integer."
            )

        if self.byte_length < 0:
            raise DomainException(
                "Document content byte length must not be negative."
            )

        if not isinstance(
            self.digest,
            DocumentContentDigest,
        ):
            raise DomainException(
                "Document content digest must be "
                "a DocumentContentDigest."
            )
