"""RFC-077 strict UTF-8 plain-text parser architecture tests."""

from __future__ import annotations

import ast
import hashlib
import inspect
import subprocess
from importlib import import_module
from pathlib import Path
from typing import get_type_hints

from app.document_parsing.parser import DocumentContentParser
from app.domain.document_content import DocumentContentDescriptor


ROOT = Path(__file__).resolve().parents[2]

TARGET = (
    ROOT
    / "backend/app/infrastructure/document_parsing/"
    "utf8_plain_text_parser.py"
)

PRESERVED_SHA256 = {'backend/app/core/registry/registry.py': 'a8bb351539e4ffc2bae4cae2f2a87155977206990e4108ba12902b10b6e172c5',
 'backend/app/document_parsing/binding.py': '63332e5228ff3db644fed05ce89c0ad583d099852aae2aa5f118ea8e6667c4cc',
 'backend/app/document_parsing/dispatching_parser.py': 'bd1cd81fb56b5afc1227d3e3b9361fd6ede359112ae0d8c3a761de0037224a8b',
 'backend/app/document_parsing/parser.py': '35ac46cfb17ed769a49c87df3e7cb5a7aa438bec60b5ff3511b6e40d7f557787',
 'backend/app/document_parsing/resolver.py': '85f0bff5985028b8246fda0412cd608fad1b2e636afe2a760825c2edb00ea713',
 'backend/app/domain/document_content.py': 'df830249fc611acfca62f9ebe1a340ea8bd4c14bff0365d909668b03256ddbc9',
 'backend/app/infrastructure/document_parsing/__init__.py': '39abfbba5fdcff705ec3db33ab5a6f544bda5335a4c5f67dcf78a87c79b722cd',
 'backend/app/infrastructure/document_parsing/registry_backed_resolver.py': 'b7fd2dff4716138832aeaa0d659f52d0573315b294e141d45fa78d2c31befa10',
 'backend/app/services/document_content_access_application_service.py': '2ffe2984ad9e5e1b2cbb6860093cb26060b3911d40259bb678d7dde1458c5e0a',
 'backend/app/services/document_content_parsing_application_service.py': 'e132a02d0d7e7981a09013d608676084ad6e29b6ce0bb3dd0f3f1567cdd28fa7',
 'tests/document_parsing/test_document_content_parser_binding_and_registry_resolver.py': 'b409c25f458c69de8751739e58e3b90c612a479887a94b171da041cc9c8ee601',
 'tests/document_parsing/test_document_content_parser_binding_and_registry_resolver_architecture.py': '004b8c94db79043848409c9b3622d1cce0149578e0d83f46f500aef52964de1d',
 'tests/document_parsing/test_document_content_parser_resolution.py': '534ebfc68ccd7ce9f19bfa7e9b393563fef7d5fb6ef2bcfc67aefea7f625fae2',
 'tests/document_parsing/test_document_content_parser_resolution_architecture.py': 'c51444fcf14d82b96a9c8db5fbf376047b9114a1d3bb645d67e18ac19aea4af2'}
REQUIREMENTS_SHA256 = {'backend/requirements.txt': 'f1e9b44db3f10e76b3a7041d81285c581adc728b41167b3becc2344ff7c53251'}
MIGRATION_SHA256 = {'backend/alembic.ini': '4be35c86b24192bde1327811488c4fcbc1f446b8c1e688fbbcba8f27640a252b',
 'backend/migrations/env.py': '38813fe44f3028c4568eabb98cb8249d33bf12f9ac1a0c1117a91e5ada13bf60',
 'backend/migrations/script.py.mako': 'fd7be8ed2f31410a1f01dccda809e7b7610e8fae7ad1b91327d48439fd6540fb',
 'backend/migrations/versions/0001_database_foundation.py': '931d525ca554d4b8b0cfa6ac62824a050267f0bdba99fef9047071e91a607cff',
 'backend/migrations/versions/0002_knowledge_records.py': '9d2909bc6a86c8e0a8b16da471e5623d0133f04fd8edac8e44262f7e8750b724',
 'backend/migrations/versions/0003_enterprise_documents.py': 'c5242e0e6ed68961bef33f8dd923668f1107f3f7cd8a8f6d67c0750365775399',
 'backend/migrations/versions/0004_document_knowledge_lineages.py': '800598696415cd207dcb472ec920caafc73e3663623d146b663dbf1d63e39202',
 'backend/migrations/versions/0005_document_content_descriptors.py': '8bd4a8dcea0380aae6b43b1f9bdb134197b4d181c4b000395157476efbc8ef33'}

FORBIDDEN_EXTERNAL_DEPENDENCIES = (
    "pypdf",
    "pdfplumber",
    "pymupdf",
    "fitz",
    "python-docx",
    "docx",
    "openpyxl",
    "xlrd",
    "tika",
    "textract",
    "tesseract",
    "easyocr",
    "chardet",
    "charset-normalizer",
    "cchardet",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def _source() -> str:
    return TARGET.read_text(encoding="utf-8")


def _module():
    return import_module(
        "app.infrastructure.document_parsing.utf8_plain_text_parser"
    )


def test_utf8_plain_text_parser_module_exists() -> None:
    assert TARGET.is_file()


def test_parser_class_is_concrete_existing_port() -> None:
    parser_type = (
        _module()
        .Utf8PlainTextDocumentContentParser
    )

    assert issubclass(
        parser_type,
        DocumentContentParser,
    )
    assert not inspect.isabstract(parser_type)


def test_parse_signature_matches_existing_port() -> None:
    parser_type = (
        _module()
        .Utf8PlainTextDocumentContentParser
    )
    operation = parser_type.parse
    signature = inspect.signature(operation)
    parameters = list(signature.parameters.values())

    assert [parameter.name for parameter in parameters] == [
        "self",
        "descriptor",
        "payload",
    ]
    assert parameters[1].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters[2].kind is inspect.Parameter.KEYWORD_ONLY

    hints = get_type_hints(operation)

    assert hints["descriptor"] is DocumentContentDescriptor
    assert hints["return"] is str


def test_constructor_requires_no_dependencies_and_has_no_custom_init() -> None:
    parser_type = (
        _module()
        .Utf8PlainTextDocumentContentParser
    )

    assert "__init__" not in parser_type.__dict__
    assert str(inspect.signature(parser_type)) == "()"


def test_implementation_imports_are_layered_and_standard_library_only() -> None:
    tree = ast.parse(_source())

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")

    assert imports == {
        "__future__",
        "codecs",
        "typing",
        "app.document_parsing.parser",
        "app.domain.document_content",
    }


def test_implementation_contains_no_forbidden_wiring_or_dependency_signals() -> None:
    source = _source().lower()

    forbidden = (
        "sqlalchemy",
        "alembic",
        "app.services",
        "app.core.registry",
        "app.document_parsing.binding",
        "app.document_parsing.resolver",
        "runtime",
        "composition",
        "bootstrap",
        "requests",
        "subprocess",
        "pathlib",
        ".seek(",
        ".tell(",
        ".fileno(",
        ".close(",
        "charset",
        "fallback",
        "detect_encoding",
        "source_reference",
        "filename",
        "extension",
    )

    for token in forbidden:
        assert token not in source


def test_canonical_read_size_and_decoder_are_explicit() -> None:
    module = _module()

    assert module._READ_SIZE == 1024 * 1024
    assert module._ENCODING == "utf-8-sig"
    assert module._ERRORS == "strict"


def test_only_expected_public_class_is_defined() -> None:
    tree = ast.parse(_source())

    classes = [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]

    assert classes == [
        "Utf8PlainTextDocumentContentParser",
    ]


def test_no_mutable_module_level_container_is_defined() -> None:
    tree = ast.parse(_source())

    for node in tree.body:
        value = None

        if isinstance(node, ast.Assign):
            value = node.value
        elif isinstance(node, ast.AnnAssign):
            value = node.value

        assert not isinstance(
            value,
            (
                ast.List,
                ast.Dict,
                ast.Set,
            ),
        )


def test_preserved_rfc073_through_rfc076_files_are_byte_identical() -> None:
    for relative, expected in PRESERVED_SHA256.items():
        path = ROOT / relative

        assert path.is_file()
        assert _sha256(path) == expected


def test_requirements_files_are_byte_identical_and_dependency_free() -> None:
    for relative, expected in REQUIREMENTS_SHA256.items():
        path = ROOT / relative

        assert path.is_file()
        assert _sha256(path) == expected

        content = path.read_text(
            encoding="utf-8",
        ).lower()

        for dependency in FORBIDDEN_EXTERNAL_DEPENDENCIES:
            assert dependency not in content


def test_migration_inventory_is_byte_identical() -> None:
    current = {}

    for relative, expected in MIGRATION_SHA256.items():
        path = ROOT / relative

        assert path.is_file()
        assert _sha256(path) == expected
        current[relative] = _sha256(path)

    tracked = subprocess.check_output(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
    ).splitlines()

    tracked_migration_paths = set()

    for relative in tracked:
        if relative.startswith(("tests/", "docs/")):
            continue

        parts = set(Path(relative).parts)

        if (
            "alembic" in parts
            or "migrations" in parts
            or relative.endswith("alembic.ini")
        ):
            tracked_migration_paths.add(relative)

    assert tracked_migration_paths == set(MIGRATION_SHA256)
    assert current == MIGRATION_SHA256


def test_parser_is_not_wired_or_registered_elsewhere() -> None:
    class_name = "Utf8PlainTextDocumentContentParser"
    module_name = (
        "app.infrastructure.document_parsing."
        "utf8_plain_text_parser"
    )

    references = []

    for path in (ROOT / "backend/app").rglob("*.py"):
        if path == TARGET:
            continue

        text = path.read_text(
            encoding="utf-8",
        )

        if class_name in text or module_name in text:
            references.append(
                path.relative_to(ROOT).as_posix()
            )

    assert references == []
