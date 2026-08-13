"""Application boundary for canonical enterprise Knowledge capture."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from app.domain.base import EntityId
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
    KnowledgeSubject,
    KnowledgeSubjectType,
)
from app.knowledge.repository import KnowledgeRecordRepository


IdentitySource = Callable[[], EntityId]
CaptureTimeSource = Callable[[], datetime]


def _default_capture_time() -> datetime:
    """Return the current canonical capture time in UTC."""
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeCaptureSubject:
    """Immutable application input for one optional Knowledge subject."""

    subject_type: str
    subject_id: EntityId


@dataclass(frozen=True, slots=True, kw_only=True)
class KnowledgeCaptureRequest:
    """Immutable application input for one canonical Knowledge capture."""

    kind: str
    title: str
    content: str
    source_type: str
    source_reference: str
    subject: KnowledgeCaptureSubject | None = None


class KnowledgeCaptureApplicationService:
    """Coordinate one canonical enterprise Knowledge capture use case."""

    def __init__(
        self,
        *,
        repository: KnowledgeRecordRepository,
        identity_source: IdentitySource = EntityId.new,
        capture_time_source: CaptureTimeSource = _default_capture_time,
    ) -> None:
        self._repository = repository
        self._identity_source = identity_source
        self._capture_time_source = capture_time_source

    @property
    def repository(self) -> KnowledgeRecordRepository:
        """Return the persistence-neutral Knowledge repository dependency."""
        return self._repository

    def capture(
        self,
        request: KnowledgeCaptureRequest,
    ) -> KnowledgeRecord:
        """Construct, persist and return one canonical Knowledge record."""
        record_id = self._identity_source()
        subject = self._build_subject(request.subject)

        provenance = KnowledgeProvenance(
            source_type=KnowledgeSourceType(
                value=request.source_type,
            ),
            source_reference=request.source_reference,
            captured_at=self._capture_time_source(),
        )

        record = KnowledgeRecord(
            id=record_id,
            kind=KnowledgeKind(value=request.kind),
            title=request.title,
            content=request.content,
            provenance=provenance,
            subject=subject,
        )

        self._repository.add(record)

        return record

    @staticmethod
    def _build_subject(
        subject: KnowledgeCaptureSubject | None,
    ) -> KnowledgeSubject | None:
        if subject is None:
            return None

        return KnowledgeSubject(
            subject_type=KnowledgeSubjectType(
                value=subject.subject_type,
            ),
            subject_id=subject.subject_id,
        )
