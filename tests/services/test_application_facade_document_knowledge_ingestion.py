"""RFC-080 facade delegation, default rejection and analysis compatibility."""
from inspect import Parameter, signature
from typing import get_type_hints
from unittest.mock import MagicMock, Mock
from uuid import UUID

import pytest
from app.core.composition import CompositionRoot
from app.domain.base import EntityId
from app.services import application_facade as facade
from app.services.document_content_parsing_application_service import DocumentContentParsingApplicationService
from app.services.document_knowledge_ingestion_application_service import DocumentKnowledgeIngestionResult
from app.services.parsed_document_knowledge_ingestion_application_service import (
    ParsedDocumentKnowledgeIngestionApplicationService as Service,
    ParsedDocumentKnowledgeIngestionRequest as Request,
)
from app.knowledge_lineage_transaction.coordinator import KnowledgeLineageTransactionPostCommitCleanupError


def configured(dependency, gateway=None):
    return facade.ApplicationFacade(gateway=gateway,
        parsed_document_knowledge_ingestion_service=dependency)


def test_explicit_ingestion_command_exists():
    assert callable(getattr(facade.ApplicationFacade, "ingest_document_knowledge", None))


def test_public_signature_and_error_contract():
    params = signature(facade.ApplicationFacade).parameters
    assert list(params) == ["gateway", "parsed_document_knowledge_ingestion_service"]
    assert params["gateway"].kind is Parameter.POSITIONAL_OR_KEYWORD
    assert params["gateway"].default is None
    dependency = params["parsed_document_knowledge_ingestion_service"]
    assert dependency.kind is Parameter.KEYWORD_ONLY and dependency.default is None
    with pytest.raises(TypeError):
        facade.ApplicationFacade(Mock(), Mock())
    assert get_type_hints(facade.ApplicationFacade.ingest_document_knowledge) == {
        "request": Request, "return": DocumentKnowledgeIngestionResult}
    assert issubclass(facade.ApplicationFacadeDocumentIngestionNotConfiguredError, RuntimeError)


@pytest.mark.parametrize("mode", ["default", "positional", "keyword", "composition"])
def test_unconfigured_rejects_without_constructing_parsing_or_writing(mode, monkeypatch):
    construction = Mock(side_effect=AssertionError("Unexpected service construction"))
    parsing = Mock(side_effect=AssertionError("Unexpected parse"))
    writing = Mock(side_effect=AssertionError("Unexpected ingestion"))
    monkeypatch.setattr(Service, "__init__", construction)
    monkeypatch.setattr(Service, "ingest", writing)
    monkeypatch.setattr(DocumentContentParsingApplicationService, "parse", parsing)
    gateway, platform = Mock(), None
    if mode == "default":
        entry = facade.ApplicationFacade()
    elif mode == "positional":
        entry = facade.ApplicationFacade(gateway)
    elif mode == "keyword":
        entry = facade.ApplicationFacade(gateway=gateway)
    else:
        platform = CompositionRoot.build()
        entry = platform.application_facade
        before = platform.runtime.state, platform.runtime.is_request_admission_enabled
        assert not platform.container.is_registered(Service)
    if mode in ("positional", "keyword"):
        assert entry._gateway is gateway
    with pytest.raises(facade.ApplicationFacadeDocumentIngestionNotConfiguredError):
        entry.ingest_document_knowledge(object())  # Disabled takes precedence over invalid input.
    construction.assert_not_called()
    parsing.assert_not_called()
    writing.assert_not_called()
    gateway.execute.assert_not_called()
    if platform is not None:
        assert before == (platform.runtime.state, platform.runtime.is_request_admission_enabled)


@pytest.mark.parametrize("truthy", [True, False])
def test_exact_delegation_without_analysis_or_truthiness(truthy, monkeypatch):
    dependency, gateway, request, result = MagicMock(), Mock(), object(), object()
    dependency.__bool__.return_value = truthy
    dependency.ingest.return_value = result
    entry = configured(dependency, gateway)
    assert entry._parsed_document_knowledge_ingestion_service is dependency
    traps = [Mock(side_effect=AssertionError("Unexpected analysis/evidence")) for _ in range(3)]
    monkeypatch.setattr(entry, "analyze", traps[0])
    monkeypatch.setattr(facade, "uuid4", traps[1])
    monkeypatch.setattr(facade, "ApplicationFacadeEntryEvidence", traps[2])
    assert entry.ingest_document_knowledge(request) is result
    dependency.ingest.assert_called_once_with(request)
    assert dependency.ingest.call_args.args[0] is request
    dependency.__bool__.assert_not_called()
    gateway.execute.assert_not_called()
    for trap in traps:
        trap.assert_not_called()


@pytest.mark.parametrize("injected", [False, True])
def test_analyze_retains_exact_gateway_and_evidence_behavior(injected, monkeypatch):
    dependency, gateway, result, observations = Mock(), Mock(), object(), ()
    gateway.execute.return_value = result
    identifier = UUID("11111111-1111-4111-8111-111111111111")
    identity_source = Mock(return_value=identifier)
    monkeypatch.setattr(facade, "uuid4", identity_source)
    entry = configured(dependency if injected else None, gateway)
    assert entry.analyze(observations) is result
    gateway.execute.assert_called_once_with(observations,
        facade_entry_evidence=facade.ApplicationFacadeEntryEvidence(workload_id=identifier))
    assert gateway.execute.call_args.args[0] is observations
    identity_source.assert_called_once_with()
    dependency.ingest.assert_not_called()


@pytest.mark.parametrize("error_type", [TypeError, ValueError, OSError,
    KnowledgeLineageTransactionPostCommitCleanupError])
def test_exception_identity_cause_and_no_retry(error_type):
    dependency, gateway = Mock(), Mock()
    failure, cause = error_type("sentinel failure"), OSError("original cause")
    failure.__cause__ = cause
    dependency.ingest.side_effect = failure
    with pytest.raises(error_type) as caught:
        configured(dependency, gateway).ingest_document_knowledge(object())
    assert caught.value is failure and caught.value.__cause__ is cause
    dependency.ingest.assert_called_once()
    gateway.execute.assert_not_called()


def test_repeated_explicit_requests_are_not_deduplicated():
    dependency, request, first, second = Mock(), object(), object(), object()
    dependency.ingest.side_effect = [first, second]
    entry = configured(dependency)
    assert entry.ingest_document_knowledge(request) is first
    assert entry.ingest_document_knowledge(request) is second
    assert len(dependency.ingest.call_args_list) == 2
    assert all(call.args[0] is request for call in dependency.ingest.call_args_list)


def test_configuration_is_instance_local():
    left, right = Mock(), Mock()
    a, b = configured(left), configured(right)
    assert a.ingest_document_knowledge(object()) is left.ingest.return_value
    right.ingest.assert_not_called()
    assert b.ingest_document_knowledge(object()) is right.ingest.return_value
    left.ingest.assert_called_once()
    with pytest.raises(facade.ApplicationFacadeDocumentIngestionNotConfiguredError):
        facade.ApplicationFacade().ingest_document_knowledge(object())


def test_configured_request_validation_remains_with_rfc079():
    reader, writer = Mock(), Mock()
    entry = configured(Service(parsing_service=reader, ingestion_service=writer))
    with pytest.raises(TypeError):
        entry.ingest_document_knowledge(object())
    reader.parse.assert_not_called()
    writer.ingest.assert_not_called()


@pytest.mark.parametrize("fails", [False, True])
def test_ingestion_does_not_change_runtime_or_admission(fails):
    platform, dependency = CompositionRoot.build(), Mock()
    before = platform.runtime.state, platform.runtime.is_request_admission_enabled
    entry = configured(dependency, platform.integration_gateway)
    if fails:
        dependency.ingest.side_effect = ValueError("sentinel")
        with pytest.raises(ValueError):
            entry.ingest_document_knowledge(object())
    else:
        entry.ingest_document_knowledge(object())
    assert before == (platform.runtime.state, platform.runtime.is_request_admission_enabled)
    with pytest.raises(facade.ApplicationFacadeDocumentIngestionNotConfiguredError):
        platform.application_facade.ingest_document_knowledge(object())
