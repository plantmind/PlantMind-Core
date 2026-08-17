"""RFC-065 canonical Document-to-Knowledge ingestion application tests."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

import pytest

from app.document.repository import EnterpriseDocumentRepository
from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageRepository,
)
from app.domain.base import EntityId
from app.domain.document import (
    DocumentSource,
    DocumentSourceType,
    DocumentType,
    EnterpriseDocument,
)
from app.domain.document_knowledge_lineage import DocumentKnowledgeLineage
from app.domain.knowledge import KnowledgeRecord
from app.knowledge.repository import KnowledgeRecordRepository
from app.knowledge_lineage_transaction.coordinator import (
    KnowledgeLineageTransactionCoordinator,
)
from app.services.document_knowledge_ingestion_application_service import (
    DocumentKnowledgeIngestionApplicationService,
    DocumentKnowledgeIngestionDocumentNotFoundError,
    DocumentKnowledgeIngestionRequest,
    DocumentKnowledgeIngestionResult,
)
from app.services.knowledge_capture_application_service import (
    KnowledgeCaptureApplicationService,
    KnowledgeCaptureSubject,
)


class RecordingDocumentRepository(EnterpriseDocumentRepository):
    def __init__(
        self,
        document: EnterpriseDocument | None,
    ) -> None:
        self.document = document
        self.add_calls = 0
        self.get_calls: list[EntityId] = []

    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        self.add_calls += 1

    def get(
        self,
        document_id: EntityId,
    ) -> EnterpriseDocument | None:
        self.get_calls.append(document_id)

        if (
            self.document is not None
            and self.document.id == document_id
        ):
            return self.document

        return None


class RecordingKnowledgeRepository(KnowledgeRecordRepository):
    def __init__(self) -> None:
        self.add_calls = 0
        self.added_record: KnowledgeRecord | None = None
        self.get_calls = 0

    def add(
        self,
        record: KnowledgeRecord,
    ) -> None:
        self.add_calls += 1
        self.added_record = record

    def get(
        self,
        record_id: EntityId,
    ) -> KnowledgeRecord | None:
        self.get_calls += 1
        return None


class RecordingLineageRepository(
    DocumentKnowledgeLineageRepository
):
    def __init__(self) -> None:
        self.add_calls = 0
        self.added_lineage: DocumentKnowledgeLineage | None = None
        self.get_calls = 0

    def add(
        self,
        lineage: DocumentKnowledgeLineage,
    ) -> None:
        self.add_calls += 1
        self.added_lineage = lineage

    def get(
        self,
        document_id: EntityId,
        knowledge_record_id: EntityId,
    ) -> DocumentKnowledgeLineage | None:
        self.get_calls += 1
        return None


class RecordingTransactionCoordinator(
    KnowledgeLineageTransactionCoordinator
):
    def __init__(
        self,
        *,
        knowledge_repository: KnowledgeRecordRepository,
        lineage_repository: DocumentKnowledgeLineageRepository,
    ) -> None:
        self.knowledge_repository = knowledge_repository
        self.lineage_repository = lineage_repository
        self.execute_calls = 0

    def execute(
        self,
        operation: Callable[
            [
                KnowledgeRecordRepository,
                DocumentKnowledgeLineageRepository,
            ],
            object,
        ],
    ) -> object:
        self.execute_calls += 1

        return operation(
            self.knowledge_repository,
            self.lineage_repository,
        )


def make_document() -> EnterpriseDocument:
    return EnterpriseDocument(
        id=EntityId.from_string(
            "11111111-1111-1111-1111-111111111111"
        ),
        document_type=DocumentType(
            value="procedure",
        ),
        title="Compressor Start Procedure",
        source=DocumentSource(
            source_type=DocumentSourceType(
                value="  Manual  ",
            ),
            source_reference="Proc-ABC-001",
        ),
    )


def make_request(
    *,
    document_id: EntityId,
    subject: KnowledgeCaptureSubject | None = None,
) -> DocumentKnowledgeIngestionRequest:
    return DocumentKnowledgeIngestionRequest(
        document_id=document_id,
        kind="procedure",
        title="Compressor Start Knowledge",
        content="Verify suction pressure before startup.",
        subject=subject,
    )


def test_rfc065_canonical_application_surface_exists() -> None:
    assert DocumentKnowledgeIngestionApplicationService is not None
    assert DocumentKnowledgeIngestionRequest is not None
    assert DocumentKnowledgeIngestionResult is not None
    assert DocumentKnowledgeIngestionDocumentNotFoundError is not None


def test_missing_document_stops_before_transaction_and_capture() -> None:
    missing_id = EntityId.from_string(
        "22222222-2222-2222-2222-222222222222"
    )

    document_repository = RecordingDocumentRepository(
        document=None,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    factory_calls: list[KnowledgeRecordRepository] = []

    def capture_factory(
        repository: KnowledgeRecordRepository,
    ) -> KnowledgeCaptureApplicationService:
        factory_calls.append(repository)

        return KnowledgeCaptureApplicationService(
            repository=repository,
        )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
        knowledge_capture_factory=capture_factory,
    )

    with pytest.raises(
        DocumentKnowledgeIngestionDocumentNotFoundError
    ):
        service.ingest(
            make_request(
                document_id=missing_id,
            )
        )

    assert document_repository.get_calls == [missing_id]
    assert document_repository.add_calls == 0
    assert coordinator.execute_calls == 0
    assert factory_calls == []
    assert knowledge_repository.add_calls == 0
    assert lineage_repository.add_calls == 0


def test_ingest_captures_knowledge_and_creates_exact_lineage() -> None:
    document = make_document()

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    knowledge_id = EntityId.from_string(
        "33333333-3333-3333-3333-333333333333"
    )
    subject_id = EntityId.from_string(
        "44444444-4444-4444-4444-444444444444"
    )
    captured_at = datetime(
        2026,
        8,
        16,
        18,
        30,
        tzinfo=UTC,
    )

    factory_calls: list[KnowledgeRecordRepository] = []

    def capture_factory(
        repository: KnowledgeRecordRepository,
    ) -> KnowledgeCaptureApplicationService:
        factory_calls.append(repository)

        return KnowledgeCaptureApplicationService(
            repository=repository,
            identity_source=lambda: knowledge_id,
            capture_time_source=lambda: captured_at,
        )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
        knowledge_capture_factory=capture_factory,
    )

    result = service.ingest(
        make_request(
            document_id=document.id,
            subject=KnowledgeCaptureSubject(
                subject_type="equipment",
                subject_id=subject_id,
            ),
        )
    )

    assert isinstance(
        result,
        DocumentKnowledgeIngestionResult,
    )

    assert document_repository.get_calls == [document.id]
    assert document_repository.add_calls == 0

    assert coordinator.execute_calls == 1
    assert factory_calls == [knowledge_repository]

    assert knowledge_repository.add_calls == 1
    assert knowledge_repository.get_calls == 0

    record = result.knowledge_record

    assert record is knowledge_repository.added_record
    assert record.id == knowledge_id
    assert record.provenance.source_type.value == "manual"
    assert (
        record.provenance.source_reference
        == "Proc-ABC-001"
    )
    assert record.provenance.captured_at == captured_at

    assert record.subject is not None
    assert record.subject.subject_type.value == "equipment"
    assert record.subject.subject_id == subject_id

    assert lineage_repository.add_calls == 1
    assert lineage_repository.get_calls == 0

    lineage = result.lineage

    assert lineage is lineage_repository.added_lineage
    assert lineage.document_id == document.id
    assert lineage.knowledge_record_id == knowledge_id


# RFC-065 FAILURE SEMANTICS

from app.knowledge_lineage_transaction.coordinator import (
    KnowledgeLineageTransactionPostCommitCleanupError,
)


class DocumentReadFailure(RuntimeError):
    pass


class KnowledgeWriteFailure(RuntimeError):
    pass


class LineageWriteFailure(RuntimeError):
    pass


class FinalCommitFailure(RuntimeError):
    pass


class FailingDocumentRepository(RecordingDocumentRepository):
    def get(
        self,
        document_id: EntityId,
    ) -> EnterpriseDocument | None:
        self.get_calls.append(document_id)
        raise DocumentReadFailure("document read failed")


class FailingKnowledgeRepository(RecordingKnowledgeRepository):
    def add(
        self,
        record: KnowledgeRecord,
    ) -> None:
        self.add_calls += 1
        self.added_record = record
        raise KnowledgeWriteFailure("knowledge write failed")


class FailingLineageRepository(RecordingLineageRepository):
    def add(
        self,
        lineage: DocumentKnowledgeLineage,
    ) -> None:
        self.add_calls += 1
        self.added_lineage = lineage
        raise LineageWriteFailure("lineage write failed")


class FailingAfterOperationCoordinator(
    RecordingTransactionCoordinator
):
    def execute(
        self,
        operation: Callable[
            [
                KnowledgeRecordRepository,
                DocumentKnowledgeLineageRepository,
            ],
            object,
        ],
    ) -> object:
        self.execute_calls += 1

        operation(
            self.knowledge_repository,
            self.lineage_repository,
        )

        raise FinalCommitFailure("final commit failed")


class PostCommitCleanupFailureCoordinator(
    RecordingTransactionCoordinator
):
    def __init__(
        self,
        *,
        knowledge_repository: KnowledgeRecordRepository,
        lineage_repository: DocumentKnowledgeLineageRepository,
        failure: KnowledgeLineageTransactionPostCommitCleanupError,
    ) -> None:
        super().__init__(
            knowledge_repository=knowledge_repository,
            lineage_repository=lineage_repository,
        )
        self.failure = failure

    def execute(
        self,
        operation: Callable[
            [
                KnowledgeRecordRepository,
                DocumentKnowledgeLineageRepository,
            ],
            object,
        ],
    ) -> object:
        self.execute_calls += 1

        operation(
            self.knowledge_repository,
            self.lineage_repository,
        )

        raise self.failure


def test_document_repository_failure_propagates_before_transaction() -> None:
    document = make_document()

    document_repository = FailingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    factory_calls: list[KnowledgeRecordRepository] = []

    def capture_factory(
        repository: KnowledgeRecordRepository,
    ) -> KnowledgeCaptureApplicationService:
        factory_calls.append(repository)
        return KnowledgeCaptureApplicationService(
            repository=repository,
        )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
        knowledge_capture_factory=capture_factory,
    )

    with pytest.raises(
        DocumentReadFailure,
        match="document read failed",
    ):
        service.ingest(
            make_request(
                document_id=document.id,
            )
        )

    assert document_repository.get_calls == [document.id]
    assert coordinator.execute_calls == 0
    assert factory_calls == []
    assert knowledge_repository.add_calls == 0
    assert lineage_repository.add_calls == 0


def test_capture_failure_propagates_without_lineage_write_or_retry() -> None:
    document = make_document()

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = FailingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    factory_calls: list[KnowledgeRecordRepository] = []

    def capture_factory(
        repository: KnowledgeRecordRepository,
    ) -> KnowledgeCaptureApplicationService:
        factory_calls.append(repository)
        return KnowledgeCaptureApplicationService(
            repository=repository,
        )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
        knowledge_capture_factory=capture_factory,
    )

    with pytest.raises(
        KnowledgeWriteFailure,
        match="knowledge write failed",
    ):
        service.ingest(
            make_request(
                document_id=document.id,
            )
        )

    assert document_repository.get_calls == [document.id]
    assert coordinator.execute_calls == 1
    assert factory_calls == [knowledge_repository]
    assert knowledge_repository.add_calls == 1
    assert lineage_repository.add_calls == 0


def test_lineage_failure_propagates_without_retry() -> None:
    document = make_document()

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = FailingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    factory_calls: list[KnowledgeRecordRepository] = []

    def capture_factory(
        repository: KnowledgeRecordRepository,
    ) -> KnowledgeCaptureApplicationService:
        factory_calls.append(repository)
        return KnowledgeCaptureApplicationService(
            repository=repository,
        )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
        knowledge_capture_factory=capture_factory,
    )

    with pytest.raises(
        LineageWriteFailure,
        match="lineage write failed",
    ):
        service.ingest(
            make_request(
                document_id=document.id,
            )
        )

    assert document_repository.get_calls == [document.id]
    assert coordinator.execute_calls == 1
    assert factory_calls == [knowledge_repository]
    assert knowledge_repository.add_calls == 1
    assert lineage_repository.add_calls == 1


def test_final_transaction_failure_does_not_escape_as_success() -> None:
    document = make_document()

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = FailingAfterOperationCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
    )

    with pytest.raises(
        FinalCommitFailure,
        match="final commit failed",
    ):
        service.ingest(
            make_request(
                document_id=document.id,
            )
        )

    assert document_repository.get_calls == [document.id]
    assert coordinator.execute_calls == 1
    assert knowledge_repository.add_calls == 1
    assert lineage_repository.add_calls == 1


def test_postcommit_cleanup_failure_propagates_unchanged() -> None:
    document = make_document()

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    failure = KnowledgeLineageTransactionPostCommitCleanupError(
        "post-commit close failed"
    )

    coordinator = PostCommitCleanupFailureCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
        failure=failure,
    )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
    )

    with pytest.raises(
        KnowledgeLineageTransactionPostCommitCleanupError
    ) as exc_info:
        service.ingest(
            make_request(
                document_id=document.id,
            )
        )

    assert exc_info.value is failure
    assert coordinator.execute_calls == 1
    assert knowledge_repository.add_calls == 1
    assert lineage_repository.add_calls == 1

# RFC-065 CONTRACT SURFACE VERIFICATION

from dataclasses import FrozenInstanceError, fields
from inspect import Parameter, signature


def test_ingestion_request_has_exact_immutable_keyword_only_contract() -> None:
    assert [
        field.name
        for field in fields(DocumentKnowledgeIngestionRequest)
    ] == [
        "document_id",
        "kind",
        "title",
        "content",
        "subject",
    ]

    document_id = EntityId.from_string(
        "55555555-5555-5555-5555-555555555555"
    )

    request = DocumentKnowledgeIngestionRequest(
        document_id=document_id,
        kind="procedure",
        title="Knowledge",
        content="Content",
    )

    with pytest.raises(FrozenInstanceError):
        request.title = "Changed"

    with pytest.raises(TypeError):
        DocumentKnowledgeIngestionRequest(
            document_id,
            "procedure",
            "Knowledge",
            "Content",
        )


def test_ingestion_result_has_exact_immutable_keyword_only_contract() -> None:
    assert [
        field.name
        for field in fields(DocumentKnowledgeIngestionResult)
    ] == [
        "knowledge_record",
        "lineage",
    ]

    result = DocumentKnowledgeIngestionResult(
        knowledge_record=object(),
        lineage=object(),
    )

    with pytest.raises(FrozenInstanceError):
        result.lineage = object()

    with pytest.raises(TypeError):
        DocumentKnowledgeIngestionResult(
            object(),
            object(),
        )


def test_service_constructor_has_exact_dependency_contract() -> None:
    parameters = list(
        signature(
            DocumentKnowledgeIngestionApplicationService.__init__
        ).parameters.values()
    )

    assert [parameter.name for parameter in parameters] == [
        "self",
        "document_repository",
        "transaction_coordinator",
        "knowledge_capture_factory",
    ]

    assert parameters[1].kind is Parameter.KEYWORD_ONLY
    assert parameters[2].kind is Parameter.KEYWORD_ONLY
    assert parameters[3].kind is Parameter.KEYWORD_ONLY
    assert parameters[3].default is None

    document_repository = RecordingDocumentRepository(
        document=None,
    )
    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=RecordingKnowledgeRepository(),
        lineage_repository=RecordingLineageRepository(),
    )

    with pytest.raises(TypeError):
        DocumentKnowledgeIngestionApplicationService(
            document_repository=document_repository,
            transaction_coordinator=coordinator,
            knowledge_capture_service=object(),
        )


def test_ingest_has_exact_application_operation_contract() -> None:
    parameters = list(
        signature(
            DocumentKnowledgeIngestionApplicationService.ingest
        ).parameters.values()
    )

    assert [parameter.name for parameter in parameters] == [
        "self",
        "request",
    ]

    assert parameters[1].kind is Parameter.POSITIONAL_OR_KEYWORD

# RFC-065 REMAINING BEHAVIORAL CONTRACT EVIDENCE

from app.document_knowledge_lineage.repository import (
    DocumentKnowledgeLineageAlreadyExistsError,
)
from app.knowledge.repository import (
    KnowledgeRecordAlreadyExistsError,
)


def test_document_lookup_precedes_transaction_coordination() -> None:
    document = make_document()
    events: list[str] = []

    class OrderedDocumentRepository(RecordingDocumentRepository):
        def get(
            self,
            document_id: EntityId,
        ) -> EnterpriseDocument | None:
            events.append("document_get")
            return super().get(document_id)

    class OrderedCoordinator(RecordingTransactionCoordinator):
        def execute(
            self,
            operation: Callable[
                [
                    KnowledgeRecordRepository,
                    DocumentKnowledgeLineageRepository,
                ],
                object,
            ],
        ) -> object:
            events.append("coordinator_execute")
            return super().execute(operation)

    document_repository = OrderedDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = OrderedCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
    )

    service.ingest(
        make_request(
            document_id=document.id,
        )
    )

    assert events == [
        "document_get",
        "coordinator_execute",
    ]
    assert document_repository.get_calls == [document.id]
    assert coordinator.execute_calls == 1


def test_document_lineage_does_not_automatically_become_knowledge_subject() -> None:
    document = make_document()

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
    )

    result = service.ingest(
        make_request(
            document_id=document.id,
            subject=None,
        )
    )

    assert result.knowledge_record.subject is None
    assert result.lineage.document_id == document.id


def test_knowledge_duplicate_exception_propagates_exactly_without_retry() -> None:
    document = make_document()

    failure = KnowledgeRecordAlreadyExistsError(
        "knowledge duplicate"
    )

    class DuplicateKnowledgeRepository(
        RecordingKnowledgeRepository
    ):
        def add(
            self,
            record: KnowledgeRecord,
        ) -> None:
            self.add_calls += 1
            self.added_record = record
            raise failure

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = DuplicateKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
    )

    with pytest.raises(
        KnowledgeRecordAlreadyExistsError
    ) as exc_info:
        service.ingest(
            make_request(
                document_id=document.id,
            )
        )

    assert exc_info.value is failure
    assert document_repository.get_calls == [document.id]
    assert coordinator.execute_calls == 1
    assert knowledge_repository.add_calls == 1
    assert lineage_repository.add_calls == 0


def test_lineage_duplicate_exception_propagates_exactly_without_retry() -> None:
    document = make_document()

    failure = DocumentKnowledgeLineageAlreadyExistsError(
        "lineage duplicate"
    )

    class DuplicateLineageRepository(
        RecordingLineageRepository
    ):
        def add(
            self,
            lineage: DocumentKnowledgeLineage,
        ) -> None:
            self.add_calls += 1
            self.added_lineage = lineage
            raise failure

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = DuplicateLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
    )

    with pytest.raises(
        DocumentKnowledgeLineageAlreadyExistsError
    ) as exc_info:
        service.ingest(
            make_request(
                document_id=document.id,
            )
        )

    assert exc_info.value is failure
    assert document_repository.get_calls == [document.id]
    assert coordinator.execute_calls == 1
    assert knowledge_repository.add_calls == 1
    assert lineage_repository.add_calls == 1


def test_same_document_may_be_ingested_more_than_once_without_service_dedup() -> None:
    document = make_document()

    document_repository = RecordingDocumentRepository(
        document=document,
    )
    knowledge_repository = RecordingKnowledgeRepository()
    lineage_repository = RecordingLineageRepository()

    coordinator = RecordingTransactionCoordinator(
        knowledge_repository=knowledge_repository,
        lineage_repository=lineage_repository,
    )

    knowledge_ids = iter(
        (
            EntityId.from_string(
                "66666666-6666-6666-6666-666666666666"
            ),
            EntityId.from_string(
                "77777777-7777-7777-7777-777777777777"
            ),
        )
    )

    def capture_factory(
        repository: KnowledgeRecordRepository,
    ) -> KnowledgeCaptureApplicationService:
        return KnowledgeCaptureApplicationService(
            repository=repository,
            identity_source=lambda: next(knowledge_ids),
            capture_time_source=lambda: datetime(
                2026,
                8,
                17,
                10,
                0,
                tzinfo=UTC,
            ),
        )

    service = DocumentKnowledgeIngestionApplicationService(
        document_repository=document_repository,
        transaction_coordinator=coordinator,
        knowledge_capture_factory=capture_factory,
    )

    first = service.ingest(
        make_request(
            document_id=document.id,
        )
    )
    second = service.ingest(
        make_request(
            document_id=document.id,
        )
    )

    assert first.knowledge_record.id != second.knowledge_record.id

    assert document_repository.get_calls == [
        document.id,
        document.id,
    ]

    assert coordinator.execute_calls == 2
    assert knowledge_repository.add_calls == 2
    assert lineage_repository.add_calls == 2

    assert first.lineage.document_id == document.id
    assert second.lineage.document_id == document.id
