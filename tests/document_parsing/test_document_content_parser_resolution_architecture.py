"""RFC-075 parser resolution/dispatch architecture tests."""

from __future__ import annotations

from hashlib import sha256
from importlib.util import find_spec
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

RESOLVER = (
    ROOT
    / "backend/app/document_parsing/resolver.py"
)

DISPATCHER = (
    ROOT
    / "backend/app/document_parsing/dispatching_parser.py"
)

PARSER = (
    ROOT
    / "backend/app/document_parsing/parser.py"
)

RFC074_SERVICE = (
    ROOT
    / "backend/app/services/"
    "document_content_parsing_application_service.py"
)

EXPECTED_PARSER_SHA256 = (
    "35ac46cfb17ed769a49c87df3e7cb5a7"
    "aa438bec60b5ff3511b6e40d7f557787"
)

EXPECTED_RFC074_SERVICE_SHA256 = (
    "e132a02d0d7e7981a09013d608676084"
    "ad6e29b6ce0bb3dd0f3f1567cdd28fa7"
)


def _text(path: Path) -> str:
    return path.read_text()


def _sha256(path: Path) -> str:
    return sha256(
        path.read_bytes()
    ).hexdigest()


def test_resolver_module_exists() -> None:
    assert find_spec(
        "app.document_parsing.resolver"
    ) is not None


def test_dispatching_parser_module_exists() -> None:
    assert find_spec(
        "app.document_parsing.dispatching_parser"
    ) is not None


def test_rfc074_parser_contract_remains_byte_identical() -> None:
    assert _sha256(PARSER) == EXPECTED_PARSER_SHA256


def test_rfc074_application_service_remains_byte_identical() -> None:
    assert (
        _sha256(RFC074_SERVICE)
        == EXPECTED_RFC074_SERVICE_SHA256
    )


def test_rfc075_modules_are_persistence_neutral() -> None:
    combined = (
        _text(RESOLVER)
        + "\n"
        + _text(DISPATCHER)
    )

    forbidden = (
        "app.infrastructure",
        "sqlalchemy",
        "alembic",
        "app.document_content.repository",
        "app.document_content.store",
        "pathlib",
        "sqlite",
        "postgres",
    )

    for token in forbidden:
        assert token not in combined.lower()


def test_rfc075_does_not_depend_on_application_or_runtime_layers() -> None:
    combined = (
        _text(RESOLVER)
        + "\n"
        + _text(DISPATCHER)
    )

    forbidden = (
        "app.services",
        "app.core.composition",
        "app.core.bootstrap",
        "app.core.runtime",
        "app.api",
    )

    for token in forbidden:
        assert token not in combined


def test_rfc075_does_not_create_or_bind_general_registry_infrastructure() -> None:
    combined = (
        _text(RESOLVER)
        + "\n"
        + _text(DISPATCHER)
    )

    forbidden = (
        "app.core.registry",
        "PluginRegistry",
        "ServiceRegistry",
        "class Registry",
        "Generic[",
    )

    for token in forbidden:
        assert token not in combined


def test_resolution_has_no_filename_sniffing_or_fallback_signals() -> None:
    combined = (
        _text(RESOLVER)
        + "\n"
        + _text(DISPATCHER)
    ).lower()

    forbidden = (
        "source_reference",
        "filename",
        "file_extension",
        "content sniff",
        "fallback",
        "wildcard",
        "default_parser",
        "parser_chain",
    )

    for token in forbidden:
        assert token not in combined


def test_no_concrete_parser_technology_is_introduced() -> None:
    combined = (
        _text(RESOLVER)
        + "\n"
        + _text(DISPATCHER)
    ).lower()

    forbidden = (
        "pypdf",
        "pdfplumber",
        "pymupdf",
        "python-docx",
        "docx",
        "openpyxl",
        "xlrd",
        "tika",
        "textract",
        "tesseract",
        "easyocr",
    )

    for token in forbidden:
        assert token not in combined


def test_legacy_document_parser_seam_is_not_promoted() -> None:
    combined = (
        _text(RESOLVER)
        + "\n"
        + _text(DISPATCHER)
    )

    assert "app.knowledge.document_parser" not in combined
