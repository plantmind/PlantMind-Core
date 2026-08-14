from __future__ import annotations

import ast
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from app.core.composition import CompositionRoot
from app.document.repository import (
    EnterpriseDocumentAlreadyExistsError,
    EnterpriseDocumentRepository,
)
from app.domain.base import DomainException, EntityId
from app.domain.document import EnterpriseDocument
from app.services.enterprise_document_registration_application_service import (
    EnterpriseDocumentRegistrationApplicationService,
    EnterpriseDocumentRegistrationRequest,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SERVICE_MODULE = (
    PROJECT_ROOT
    / "backend/app/services/"
    "enterprise_document_registration_application_service.py"
)


class RecordingDocumentRepository(EnterpriseDocumentRepository):
    def __init__(self) -> None:
        self.add_calls = 0
        self.get_calls = 0
        self.added_documents: list[EnterpriseDocument] = []

    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        self.add_calls += 1
        self.added_documents.append(document)

    def get(
        self,
        document_id: EntityId,
    ) -> EnterpriseDocument | None:
        self.get_calls += 1
        return None


class DuplicateDocumentRepository(RecordingDocumentRepository):
    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        super().add(document)
        raise EnterpriseDocumentAlreadyExistsError(
            "Canonical enterprise Document identity already exists."
        )


class FailingDocumentRepository(RecordingDocumentRepository):
    def add(
        self,
        document: EnterpriseDocument,
    ) -> None:
        super().add(document)
        raise RuntimeError("repository failure")


class RecordingIdentitySource:
    def __init__(
        self,
        identities: list[EntityId],
    ) -> None:
        self.identities = identities
        self.calls = 0

    def __call__(self) -> EntityId:
        identity = self.identities[self.calls]
        self.calls += 1
        return identity


class FailingIdentitySource:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self) -> EntityId:
        self.calls += 1
        raise RuntimeError("identity failure")


def make_request(
    *,
    document_type: str = "  Procedure  ",
    title: str = "  Compressor Start Procedure  ",
    source_type: str = "  Document_Control  ",
    source_reference: str = "  PROC-001  ",
) -> EnterpriseDocumentRegistrationRequest:
    return EnterpriseDocumentRegistrationRequest(
        document_type=document_type,
        title=title,
        source_type=source_type,
        source_reference=source_reference,
    )


def imported_modules(
    path: Path,
) -> set[str]:
    tree = ast.parse(path.read_text())

    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(
                alias.name
                for alias in node.names
            )
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
        ):
            modules.add(node.module)

    return modules


def non_stdlib_modules(
    path: Path,
) -> set[str]:
    return {
        module
        for module in imported_modules(path)
        if module.split(".", 1)[0]
        not in sys.stdlib_module_names
    }


def test_registration_request_is_immutable() -> None:
    request = make_request()

    with pytest.raises(FrozenInstanceError):
        request.title = "Changed"


def test_register_constructs_persists_and_returns_canonical_document() -> None:
    repository = RecordingDocumentRepository()
    identity = EntityId.from_string(
        "11111111-1111-1111-1111-111111111111"
    )
    identity_source = RecordingIdentitySource(
        [identity]
    )

    service = EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
        identity_source=identity_source,
    )

    document = service.register(make_request())

    assert document.id == identity
    assert document.document_type.value == "procedure"
    assert document.title == "Compressor Start Procedure"
    assert document.source.source_type.value == "document_control"
    assert document.source.source_reference == "PROC-001"

    assert repository.add_calls == 1
    assert repository.get_calls == 0
    assert repository.added_documents == [document]
    assert repository.added_documents[0] is document
    assert identity_source.calls == 1


def test_service_construction_has_no_registration_side_effects() -> None:
    repository = RecordingDocumentRepository()
    identity_source = RecordingIdentitySource(
        [EntityId.new()]
    )

    EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
        identity_source=identity_source,
    )

    assert identity_source.calls == 0
    assert repository.add_calls == 0
    assert repository.get_calls == 0


def test_identity_source_failure_prevents_persistence() -> None:
    repository = RecordingDocumentRepository()
    identity_source = FailingIdentitySource()

    service = EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
        identity_source=identity_source,
    )

    with pytest.raises(
        RuntimeError,
        match="identity failure",
    ):
        service.register(make_request())

    assert identity_source.calls == 1
    assert repository.add_calls == 0
    assert repository.get_calls == 0


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("document_type", "   "),
        ("title", "   "),
        ("source_type", "   "),
        ("source_reference", "   "),
    ],
)
def test_domain_validation_failure_prevents_persistence(
    field_name: str,
    invalid_value: str,
) -> None:
    repository = RecordingDocumentRepository()
    identity_source = RecordingIdentitySource(
        [EntityId.new()]
    )

    service = EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
        identity_source=identity_source,
    )

    values = {
        "document_type": "procedure",
        "title": "Compressor Start Procedure",
        "source_type": "document_control",
        "source_reference": "PROC-001",
    }
    values[field_name] = invalid_value

    with pytest.raises(DomainException):
        service.register(
            EnterpriseDocumentRegistrationRequest(
                **values
            )
        )

    assert identity_source.calls == 1
    assert repository.add_calls == 0
    assert repository.get_calls == 0


def test_duplicate_conflict_propagates_without_retry() -> None:
    repository = DuplicateDocumentRepository()
    identity_source = RecordingIdentitySource(
        [EntityId.new()]
    )

    service = EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
        identity_source=identity_source,
    )

    with pytest.raises(
        EnterpriseDocumentAlreadyExistsError
    ):
        service.register(make_request())

    assert repository.add_calls == 1
    assert repository.get_calls == 0
    assert identity_source.calls == 1


def test_unexpected_repository_failure_propagates_without_retry() -> None:
    repository = FailingDocumentRepository()
    identity_source = RecordingIdentitySource(
        [EntityId.new()]
    )

    service = EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
        identity_source=identity_source,
    )

    with pytest.raises(
        RuntimeError,
        match="repository failure",
    ):
        service.register(make_request())

    assert repository.add_calls == 1
    assert repository.get_calls == 0
    assert identity_source.calls == 1


def test_equal_source_references_do_not_trigger_application_deduplication() -> None:
    repository = RecordingDocumentRepository()

    first_identity = EntityId.from_string(
        "22222222-2222-2222-2222-222222222222"
    )
    second_identity = EntityId.from_string(
        "33333333-3333-3333-3333-333333333333"
    )

    identity_source = RecordingIdentitySource(
        [
            first_identity,
            second_identity,
        ]
    )

    service = EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
        identity_source=identity_source,
    )

    first = service.register(
        make_request(
            title="First Document",
            source_reference="SAME-REFERENCE",
        )
    )
    second = service.register(
        make_request(
            title="Second Document",
            source_reference="SAME-REFERENCE",
        )
    )

    assert first.id == first_identity
    assert second.id == second_identity
    assert first.source.source_reference == "SAME-REFERENCE"
    assert second.source.source_reference == "SAME-REFERENCE"

    assert repository.add_calls == 2
    assert repository.get_calls == 0
    assert identity_source.calls == 2


def test_default_identity_generation_requires_no_database() -> None:
    repository = RecordingDocumentRepository()

    service = EnterpriseDocumentRegistrationApplicationService(
        repository=repository,
    )

    document = service.register(make_request())

    assert isinstance(document.id, EntityId)
    assert repository.add_calls == 1
    assert repository.get_calls == 0
    assert repository.added_documents == [document]


def test_registration_service_depends_only_on_canonical_contracts() -> None:
    assert SERVICE_MODULE.is_file()

    assert non_stdlib_modules(
        SERVICE_MODULE
    ) == {
        "app.document.repository",
        "app.domain.base",
        "app.domain.document",
    }


def test_default_composition_does_not_register_document_registration_service() -> None:
    platform = CompositionRoot.build()

    assert not platform.container.is_registered(
        EnterpriseDocumentRegistrationApplicationService
    )


def test_default_composition_does_not_register_document_repository() -> None:
    platform = CompositionRoot.build()

    assert not platform.container.is_registered(
        EnterpriseDocumentRepository
    )


def test_platform_composition_exposes_no_document_registration_service() -> None:
    platform = CompositionRoot.build()

    assert not hasattr(
        platform,
        "enterprise_document_registration_application_service",
    )
