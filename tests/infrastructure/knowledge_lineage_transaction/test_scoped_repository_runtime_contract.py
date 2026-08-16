"""RFC-064 transaction-scoped repository participant runtime tests."""

from __future__ import annotations

import importlib
from datetime import datetime, timezone
from unittest.mock import Mock

from app.domain.base import EntityId
from app.domain.document_knowledge_lineage import (
    DocumentKnowledgeLineage,
)
from app.domain.knowledge import (
    KnowledgeKind,
    KnowledgeProvenance,
    KnowledgeRecord,
    KnowledgeSourceType,
)
from app.infrastructure.document_knowledge_lineage.models import (
    DocumentKnowledgeLineageRow,
)
from app.infrastructure.knowledge.models import KnowledgeRecordRow


def _coordinator_class():
    module = importlib.import_module(
        "app.infrastructure.knowledge_lineage_transaction.coordinator"
    )

    return module.SQLAlchemyKnowledgeLineageTransactionCoordinator


def _build_record() -> KnowledgeRecord:
    return KnowledgeRecord(
        id=EntityId.new(),
        kind=KnowledgeKind(value="procedure"),
        title="Compressor Start Procedure",
        content="Verify suction pressure before startup.",
        provenance=KnowledgeProvenance(
            source_type=KnowledgeSourceType(value="document"),
            source_reference="PROC-001",
            captured_at=datetime(
                2026,
                8,
                16,
                10,
                30,
                tzinfo=timezone.utc,
            ),
        ),
        subject=None,
    )


def _build_lineage(
    knowledge_record_id: EntityId,
) -> DocumentKnowledgeLineage:
    return DocumentKnowledgeLineage(
        document_id=EntityId.new(),
        knowledge_record_id=knowledge_record_id,
    )


def test_scoped_knowledge_add_uses_shared_session_and_flushes() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    record = _build_record()

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> str:
        knowledge_repository.add(record)

        session.add.assert_called_once()

        persisted = session.add.call_args.args[0]

        assert isinstance(
            persisted,
            KnowledgeRecordRow,
        )
        assert persisted.id == record.id.value

        session.flush.assert_called_once_with()

        session.commit.assert_not_called()
        session.rollback.assert_not_called()
        session.close.assert_not_called()

        return "completed"

    result = coordinator.execute(operation)

    assert result == "completed"

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_scoped_lineage_add_uses_shared_session_and_flushes() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    record = _build_record()
    lineage = _build_lineage(record.id)

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> str:
        lineage_repository.add(lineage)

        session.add.assert_called_once()

        persisted = session.add.call_args.args[0]

        assert isinstance(
            persisted,
            DocumentKnowledgeLineageRow,
        )
        assert persisted.document_id == lineage.document_id.value
        assert (
            persisted.knowledge_record_id
            == lineage.knowledge_record_id.value
        )

        session.flush.assert_called_once_with()

        session.commit.assert_not_called()
        session.rollback.assert_not_called()
        session.close.assert_not_called()

        return "completed"

    result = coordinator.execute(operation)

    assert result == "completed"

    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_scoped_knowledge_get_uses_shared_session_and_is_read_only() -> None:
    from app.infrastructure.knowledge.mapping import record_to_row

    coordinator_class = _coordinator_class()

    record = _build_record()
    session = Mock()
    session.get.return_value = record_to_row(record)

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> KnowledgeRecord:
        restored = knowledge_repository.get(record.id)

        session.get.assert_called_once_with(
            KnowledgeRecordRow,
            record.id.value,
        )

        session.commit.assert_not_called()
        session.rollback.assert_not_called()
        session.close.assert_not_called()

        assert restored == record

        return restored

    result = coordinator.execute(operation)

    assert result == record
    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_scoped_lineage_get_uses_exact_shared_session_identity() -> None:
    from app.infrastructure.document_knowledge_lineage.mapping import (
        lineage_to_row,
    )

    coordinator_class = _coordinator_class()

    record = _build_record()
    lineage = _build_lineage(record.id)

    session = Mock()
    session.get.return_value = lineage_to_row(lineage)

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    def operation(
        knowledge_repository,
        lineage_repository,
    ) -> DocumentKnowledgeLineage:
        restored = lineage_repository.get(
            lineage.document_id,
            lineage.knowledge_record_id,
        )

        session.get.assert_called_once_with(
            DocumentKnowledgeLineageRow,
            (
                lineage.document_id.value,
                lineage.knowledge_record_id.value,
            ),
        )

        session.commit.assert_not_called()
        session.rollback.assert_not_called()
        session.close.assert_not_called()

        assert restored == lineage

        return restored

    result = coordinator.execute(operation)

    assert result == lineage
    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_scoped_knowledge_get_returns_none_when_absent() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    session.get.return_value = None

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    record_id = EntityId.new()

    def operation(
        knowledge_repository,
        lineage_repository,
    ):
        result = knowledge_repository.get(record_id)

        assert result is None

        session.get.assert_called_once_with(
            KnowledgeRecordRow,
            record_id.value,
        )

        session.commit.assert_not_called()
        session.rollback.assert_not_called()
        session.close.assert_not_called()

        return result

    result = coordinator.execute(operation)

    assert result is None
    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()


def test_scoped_lineage_get_returns_none_when_absent() -> None:
    coordinator_class = _coordinator_class()

    session = Mock()
    session.get.return_value = None

    coordinator = coordinator_class(
        Mock(return_value=session)
    )

    document_id = EntityId.new()
    knowledge_record_id = EntityId.new()

    def operation(
        knowledge_repository,
        lineage_repository,
    ):
        result = lineage_repository.get(
            document_id,
            knowledge_record_id,
        )

        assert result is None

        session.get.assert_called_once_with(
            DocumentKnowledgeLineageRow,
            (
                document_id.value,
                knowledge_record_id.value,
            ),
        )

        session.commit.assert_not_called()
        session.rollback.assert_not_called()
        session.close.assert_not_called()

        return result

    result = coordinator.execute(operation)

    assert result is None
    session.commit.assert_called_once_with()
    session.rollback.assert_not_called()
    session.close.assert_called_once_with()
