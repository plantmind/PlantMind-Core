from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.knowledge import KnowledgeRecord
from app.knowledge.repository import (
    KnowledgeRecordAlreadyExistsError,
    KnowledgeRecordRepository,
)
from app.services.knowledge_capture_application_service import (
    KnowledgeCaptureApplicationService,
    KnowledgeCaptureRequest,
    KnowledgeCaptureSubject,
)


class RecordingKnowledgeRepository(KnowledgeRecordRepository):
    def __init__(self) -> None:
        self.add_calls = 0
        self.get_calls = 0
        self.added_record: KnowledgeRecord | None = None

    def add(self, record: KnowledgeRecord) -> None:
        self.add_calls += 1
        self.added_record = record

    def get(self, record_id: EntityId) -> KnowledgeRecord | None:
        self.get_calls += 1
        return None


class DuplicateKnowledgeRepository(RecordingKnowledgeRepository):
    def add(self, record: KnowledgeRecord) -> None:
        super().add(record)
        raise KnowledgeRecordAlreadyExistsError(
            "Canonical knowledge identity already exists."
        )


class FailingKnowledgeRepository(RecordingKnowledgeRepository):
    def add(self, record: KnowledgeRecord) -> None:
        super().add(record)
        raise RuntimeError("repository failure")


class RecordingIdentitySource:
    def __init__(self, identity: EntityId) -> None:
        self.identity = identity
        self.calls = 0

    def __call__(self) -> EntityId:
        self.calls += 1
        return self.identity


class FailingIdentitySource:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self) -> EntityId:
        self.calls += 1
        raise RuntimeError("identity failure")


class RecordingTimeSource:
    def __init__(self, captured_at: datetime) -> None:
        self.captured_at = captured_at
        self.calls = 0

    def __call__(self) -> datetime:
        self.calls += 1
        return self.captured_at


def make_request(
    *,
    kind: str = "  Procedure  ",
    title: str = "  Compressor Start Procedure  ",
    content: str = "  Verify suction pressure before startup.  ",
    source_type: str = "  Document  ",
    source_reference: str = "  PROC-001  ",
    subject: KnowledgeCaptureSubject | None = None,
) -> KnowledgeCaptureRequest:
    return KnowledgeCaptureRequest(
        kind=kind,
        title=title,
        content=content,
        source_type=source_type,
        source_reference=source_reference,
        subject=subject,
    )


def test_capture_request_is_immutable() -> None:
    request = make_request()

    with pytest.raises(FrozenInstanceError):
        request.title = "Changed"


def test_capture_subject_is_immutable() -> None:
    subject = KnowledgeCaptureSubject(
        subject_type="equipment",
        subject_id=EntityId.new(),
    )

    with pytest.raises(FrozenInstanceError):
        subject.subject_type = "procedure"


def test_capture_constructs_and_persists_canonical_record() -> None:
    repository = RecordingKnowledgeRepository()
    identity = EntityId.from_string(
        "11111111-1111-1111-1111-111111111111"
    )
    identity_source = RecordingIdentitySource(identity)
    capture_time = datetime(
        2026,
        8,
        13,
        16,
        0,
        tzinfo=timezone(timedelta(hours=3)),
    )
    time_source = RecordingTimeSource(capture_time)

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=identity_source,
        capture_time_source=time_source,
    )

    record = service.capture(make_request())

    assert record.id == identity
    assert record.kind.value == "procedure"
    assert record.title == "Compressor Start Procedure"
    assert record.content == "Verify suction pressure before startup."
    assert record.provenance.source_type.value == "document"
    assert record.provenance.source_reference == "PROC-001"
    assert record.provenance.captured_at == datetime(
        2026,
        8,
        13,
        13,
        0,
        tzinfo=UTC,
    )
    assert record.subject is None

    assert repository.add_calls == 1
    assert repository.get_calls == 0
    assert repository.added_record is record

    assert identity_source.calls == 1
    assert time_source.calls == 1


def test_capture_constructs_canonical_subject_from_capture_input() -> None:
    repository = RecordingKnowledgeRepository()
    subject_id = EntityId.from_string(
        "22222222-2222-2222-2222-222222222222"
    )

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=RecordingIdentitySource(
            EntityId.from_string(
                "33333333-3333-3333-3333-333333333333"
            )
        ),
        capture_time_source=RecordingTimeSource(
            datetime(2026, 8, 13, 13, 0, tzinfo=UTC)
        ),
    )

    record = service.capture(
        make_request(
            subject=KnowledgeCaptureSubject(
                subject_type="  Equipment  ",
                subject_id=subject_id,
            )
        )
    )

    assert record.subject is not None
    assert record.subject.subject_type.value == "equipment"
    assert record.subject.subject_id == subject_id


def test_identity_source_failure_prevents_capture_time_and_persistence() -> None:
    repository = RecordingKnowledgeRepository()
    identity_source = FailingIdentitySource()
    time_source = RecordingTimeSource(
        datetime(2026, 8, 13, 13, 0, tzinfo=UTC)
    )

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=identity_source,
        capture_time_source=time_source,
    )

    with pytest.raises(RuntimeError, match="identity failure"):
        service.capture(make_request())

    assert identity_source.calls == 1
    assert time_source.calls == 0
    assert repository.add_calls == 0
    assert repository.get_calls == 0


def test_duplicate_conflict_propagates_without_retry() -> None:
    repository = DuplicateKnowledgeRepository()
    identity_source = RecordingIdentitySource(EntityId.new())
    time_source = RecordingTimeSource(
        datetime(2026, 8, 13, 13, 0, tzinfo=UTC)
    )

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=identity_source,
        capture_time_source=time_source,
    )

    with pytest.raises(KnowledgeRecordAlreadyExistsError):
        service.capture(make_request())

    assert repository.add_calls == 1
    assert repository.get_calls == 0
    assert identity_source.calls == 1
    assert time_source.calls == 1


def test_unexpected_repository_failure_propagates_without_retry() -> None:
    repository = FailingKnowledgeRepository()
    identity_source = RecordingIdentitySource(EntityId.new())
    time_source = RecordingTimeSource(
        datetime(2026, 8, 13, 13, 0, tzinfo=UTC)
    )

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=identity_source,
        capture_time_source=time_source,
    )

    with pytest.raises(RuntimeError, match="repository failure"):
        service.capture(make_request())

    assert repository.add_calls == 1
    assert repository.get_calls == 0
    assert identity_source.calls == 1
    assert time_source.calls == 1


def test_domain_validation_failure_is_not_converted_to_success() -> None:
    repository = RecordingKnowledgeRepository()

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=RecordingIdentitySource(EntityId.new()),
        capture_time_source=RecordingTimeSource(
            datetime(2026, 8, 13, 13, 0, tzinfo=UTC)
        ),
    )

    with pytest.raises(DomainException):
        service.capture(
            make_request(
                kind="   ",
            )
        )

    assert repository.add_calls == 0
    assert repository.get_calls == 0


def test_default_identity_and_time_sources_require_no_database() -> None:
    repository = RecordingKnowledgeRepository()

    service = KnowledgeCaptureApplicationService(
        repository=repository,
    )

    record = service.capture(make_request())

    assert isinstance(record.id, EntityId)
    assert record.provenance.captured_at.tzinfo is not None
    assert record.provenance.captured_at.utcoffset() == timedelta(0)
    assert repository.added_record is record


def test_dependency_sources_are_not_invoked_during_service_construction() -> None:
    repository = RecordingKnowledgeRepository()
    identity_source = RecordingIdentitySource(EntityId.new())
    time_source = RecordingTimeSource(
        datetime(2026, 8, 13, 13, 0, tzinfo=UTC)
    )

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=identity_source,
        capture_time_source=time_source,
    )

    assert service.repository is repository
    assert identity_source.calls == 0
    assert time_source.calls == 0
    assert repository.add_calls == 0
    assert repository.get_calls == 0


def test_capture_time_source_failure_prevents_persistence() -> None:
    class FailingTimeSource:
        def __init__(self) -> None:
            self.calls = 0

        def __call__(self) -> datetime:
            self.calls += 1
            raise RuntimeError("capture-time failure")

    repository = RecordingKnowledgeRepository()
    identity_source = RecordingIdentitySource(EntityId.new())
    time_source = FailingTimeSource()

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=identity_source,
        capture_time_source=time_source,
    )

    with pytest.raises(RuntimeError, match="capture-time failure"):
        service.capture(make_request())

    assert identity_source.calls == 1
    assert time_source.calls == 1
    assert repository.add_calls == 0
    assert repository.get_calls == 0


def test_invalid_subject_prevents_capture_time_and_persistence() -> None:
    repository = RecordingKnowledgeRepository()
    identity_source = RecordingIdentitySource(EntityId.new())
    time_source = RecordingTimeSource(
        datetime(2026, 8, 13, 13, 0, tzinfo=UTC)
    )

    service = KnowledgeCaptureApplicationService(
        repository=repository,
        identity_source=identity_source,
        capture_time_source=time_source,
    )

    with pytest.raises(DomainException):
        service.capture(
            make_request(
                subject=KnowledgeCaptureSubject(
                    subject_type="   ",
                    subject_id=EntityId.new(),
                )
            )
        )

    assert identity_source.calls == 1
    assert time_source.calls == 0
    assert repository.add_calls == 0
    assert repository.get_calls == 0
