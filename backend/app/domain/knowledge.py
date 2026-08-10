"""Canonical enterprise knowledge domain contracts for PlantMind."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.domain.base import DomainEntity, DomainException, EntityId


def _normalize_open_type_value(value: str, *, field_name: str) -> str:
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
class KnowledgeKind:
    """Open immutable classification of canonical enterprise knowledge."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_open_type_value(
                self.value,
                field_name="Knowledge kind",
            ),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeSourceType:
    """Open immutable classification of a knowledge provenance source."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_open_type_value(
                self.value,
                field_name="Knowledge source type",
            ),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeSubjectType:
    """Open immutable classification of a knowledge subject reference."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_open_type_value(
                self.value,
                field_name="Knowledge subject type",
            ),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeProvenance:
    """Immutable traceable origin of one canonical knowledge record."""

    source_type: KnowledgeSourceType
    source_reference: str
    captured_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.source_type, KnowledgeSourceType):
            raise DomainException(
                "Knowledge provenance source type must be a KnowledgeSourceType."
            )

        if not isinstance(self.source_reference, str):
            raise DomainException(
                "Knowledge provenance source reference must be a string."
            )

        if not isinstance(self.captured_at, datetime):
            raise DomainException(
                "Knowledge provenance timestamp must be a datetime."
            )

        source_reference = self.source_reference.strip()

        if not source_reference:
            raise DomainException(
                "Knowledge provenance source reference must not be empty."
            )

        if (
            self.captured_at.tzinfo is None
            or self.captured_at.utcoffset() is None
        ):
            raise DomainException(
                "Knowledge provenance timestamp must include timezone information."
            )

        object.__setattr__(
            self,
            "source_reference",
            source_reference,
        )
        object.__setattr__(
            self,
            "captured_at",
            self.captured_at.astimezone(timezone.utc),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeSubject:
    """Typed primary contextual reference to an existing domain entity."""

    subject_type: KnowledgeSubjectType
    subject_id: EntityId

    def __post_init__(self) -> None:
        if not isinstance(self.subject_type, KnowledgeSubjectType):
            raise DomainException(
                "Knowledge subject type must be a KnowledgeSubjectType."
            )

        if not isinstance(self.subject_id, EntityId):
            raise DomainException(
                "Knowledge subject id must be an EntityId."
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeRecord(DomainEntity[EntityId]):
    """Immutable canonical representation of one enterprise knowledge item."""

    kind: KnowledgeKind
    title: str
    content: str
    provenance: KnowledgeProvenance
    subject: KnowledgeSubject | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, EntityId):
            raise DomainException(
                "Knowledge record id must be an EntityId."
            )

        if not isinstance(self.kind, KnowledgeKind):
            raise DomainException(
                "Knowledge record kind must be a KnowledgeKind."
            )

        if not isinstance(self.title, str):
            raise DomainException(
                "Knowledge record title must be a string."
            )

        if not isinstance(self.content, str):
            raise DomainException(
                "Knowledge record content must be a string."
            )

        if not isinstance(self.provenance, KnowledgeProvenance):
            raise DomainException(
                "Knowledge record provenance must be a KnowledgeProvenance."
            )

        if (
            self.subject is not None
            and not isinstance(self.subject, KnowledgeSubject)
        ):
            raise DomainException(
                "Knowledge record subject must be a KnowledgeSubject or None."
            )

        title = self.title.strip()
        content = self.content.strip()

        if not title:
            raise DomainException(
                "Knowledge record title must not be empty."
            )

        if not content:
            raise DomainException(
                "Knowledge record content must not be empty."
            )

        object.__setattr__(self, "title", title)
        object.__setattr__(self, "content", content)
