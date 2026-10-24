"""RFC-079 request, ordering and unchanged exception semantics."""
from contextlib import contextmanager
from dataclasses import FrozenInstanceError, fields
from hashlib import sha256
from importlib import import_module
from inspect import Parameter, signature
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from app.domain.base import EntityId
from app.domain.document_content import DocumentContentDescriptor, DocumentContentDigest, DocumentContentMediaType
from app.services import document_content_parsing_application_service as parsing
from app.services.document_content_access_application_service import DocumentContentAccess
from app.services.document_knowledge_ingestion_application_service import DocumentKnowledgeIngestionResult
from app.services.knowledge_capture_application_service import KnowledgeCaptureSubject
from app.knowledge_lineage_transaction.coordinator import KnowledgeLineageTransactionPostCommitCleanupError


def module():
    return import_module("app.services.parsed_document_knowledge_ingestion_application_service")


def descriptor(identity):
    return DocumentContentDescriptor(document_id=identity,
        media_type=DocumentContentMediaType(value="text/plain"), byte_length=1,
        digest=DocumentContentDigest(value=sha256(b"x").hexdigest()))


def rig():
    m = module()
    request = m.ParsedDocumentKnowledgeIngestionRequest(
        document_id=EntityId.new(), kind="procedure", title="Title")
    reader, writer = Mock(), Mock()
    reader.parse.return_value = parsing.DocumentContentParsingResult(
        descriptor=descriptor(request.document_id), text="  A\r\nنص عربي\n ")
    writer.ingest.return_value = DocumentKnowledgeIngestionResult(
        knowledge_record=object(), lineage=object())
    service = m.ParsedDocumentKnowledgeIngestionApplicationService(
        parsing_service=reader, ingestion_service=writer)
    return request, reader, writer, service


def test_request_and_dependency_contracts():
    m = module()
    request, reader, writer, _ = rig()
    cls = type(request)
    assert [f.name for f in fields(cls)] == ["document_id", "kind", "title", "subject"]
    assert request.subject is None and not hasattr(request, "__dict__")
    assert all(p.kind is Parameter.KEYWORD_ONLY for p in signature(cls).parameters.values())
    with pytest.raises(FrozenInstanceError):
        request.title = "changed"
    with pytest.raises(TypeError):
        cls(document_id=request.document_id, kind="x", title="x", content="override")
    ctor = signature(m.ParsedDocumentKnowledgeIngestionApplicationService)
    assert list(ctor.parameters) == ["parsing_service", "ingestion_service"]
    assert all(p.kind is Parameter.KEYWORD_ONLY for p in ctor.parameters.values())
    assert not reader.mock_calls and not writer.mock_calls


@pytest.mark.parametrize("unvalidated", [False, True])
def test_exact_forwarding_order_and_result_identity(unvalidated):
    request, reader, writer, service = rig()
    subject = KnowledgeCaptureSubject(subject_type="equipment", subject_id=EntityId.new())
    request = type(request)(document_id=request.document_id,
        kind=object() if unvalidated else " procedure ",
        title=object() if unvalidated else " title ", subject=subject)
    events = []
    expected = writer.ingest.return_value
    def parse(value):
        events.append("parse")
        assert value.document_id == request.document_id
        return reader.parse.return_value
    def ingest(value):
        events.append("ingest")
        assert value.document_id == request.document_id
        assert value.kind is request.kind and value.title is request.title
        assert value.subject is subject and value.content is reader.parse.return_value.text
        return expected
    reader.parse.side_effect, writer.ingest.side_effect = parse, ingest
    assert service.ingest(request) is expected
    assert events == ["parse", "ingest"]
    reader.parse.assert_called_once()
    writer.ingest.assert_called_once()


@pytest.mark.parametrize("bad", [None, {}, "request", 5])
def test_wrong_request_rejected_before_services(bad):
    _, reader, writer, service = rig()
    with pytest.raises(TypeError):
        service.ingest(bad)
    assert not reader.mock_calls and not writer.mock_calls


@pytest.mark.parametrize("bad", [None, "not-an-id", 5])
def test_wrong_identity_rejected_before_services(bad):
    request, reader, writer, service = rig()
    request = type(request)(document_id=bad, kind="x", title="x")
    with pytest.raises(TypeError):
        service.ingest(request)
    assert not reader.mock_calls and not writer.mock_calls


@pytest.mark.parametrize("case,error", [
    ("result", TypeError), ("descriptor", TypeError), ("bytes", TypeError),
    ("none_text", TypeError), ("identity", ValueError),
    ("empty", ValueError), ("whitespace", ValueError), ("unicode_space", ValueError),
])
def test_invalid_parsing_result_never_reaches_ingestion(case, error):
    request, reader, writer, service = rig()
    desc, value = descriptor(request.document_id), "valid"
    if case == "descriptor": desc = object()
    if case == "identity": desc = descriptor(EntityId.new())
    values = {"bytes": b"text", "none_text": None, "empty": "",
              "whitespace": " \t\r\n", "unicode_space": "\u2003"}
    value = values.get(case, value)
    reader.parse.return_value = (SimpleNamespace(descriptor=desc, text=value) if case == "result"
        else parsing.DocumentContentParsingResult(descriptor=desc, text=value))
    with pytest.raises(error):
        service.ingest(request)
    reader.parse.assert_called_once()
    writer.ingest.assert_not_called()


@pytest.mark.parametrize("stage,error_type", [
    ("parse", OSError), ("parse", ValueError), ("ingest", RuntimeError),
    ("ingest", KnowledgeLineageTransactionPostCommitCleanupError),
])
def test_failure_identity_and_no_retry(stage, error_type):
    request, reader, writer, service = rig()
    failure = error_type("sentinel failure")
    (reader.parse if stage == "parse" else writer.ingest).side_effect = failure
    with pytest.raises(error_type) as caught:
        service.ingest(request)
    assert caught.value is failure
    assert reader.parse.call_count == 1
    assert writer.ingest.call_count == (stage == "ingest")


def test_repeated_explicit_calls_are_not_deduplicated():
    request, reader, writer, service = rig()
    first, second = object(), object()
    writer.ingest.side_effect = [first, second]
    assert service.ingest(request) is first
    assert service.ingest(request) is second
    assert reader.parse.call_count == writer.ingest.call_count == 2


@pytest.mark.parametrize("cleanup_fails", [False, True])
def test_real_parsing_cleanup_finishes_before_ingestion(cleanup_fails):
    request, _, writer, _ = rig()
    events, failure = [], OSError("payload cleanup failed")
    @contextmanager
    def opened(_):
        with BytesIO(b"x") as stream:
            yield DocumentContentAccess(descriptor=descriptor(request.document_id), payload=stream)
        events.append("closed")
        if cleanup_fails:
            raise failure
    reader = parsing.DocumentContentParsingApplicationService(
        content_access_service=SimpleNamespace(open=opened),
        parser=SimpleNamespace(parse=lambda **kw: kw["payload"].read().decode()))
    service = module().ParsedDocumentKnowledgeIngestionApplicationService(
        parsing_service=reader, ingestion_service=writer)
    writer.ingest.side_effect = lambda _: events.append("ingest")
    if cleanup_fails:
        with pytest.raises(OSError) as caught:
            service.ingest(request)
        assert caught.value is failure and events == ["closed"]
        writer.ingest.assert_not_called()
    else:
        service.ingest(request)
        assert events == ["closed", "ingest"]
