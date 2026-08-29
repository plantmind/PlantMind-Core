"""RFC-074 architecture and containment guardrails."""

from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path
from typing import get_type_hints

from alembic.config import Config
from alembic.script import ScriptDirectory

from app.document_parsing.parser import (
    DocumentContentParser,
    DocumentContentParserInvalidContentError,
    DocumentContentParserUnsupportedMediaTypeError,
)
from app.domain.base import EntityId
from app.domain.document_content import DocumentContentDescriptor
from app.services.document_content_access_application_service import (
    DocumentContentAccessApplicationService,
)
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingApplicationService,
    DocumentContentParsingRequest,
    DocumentContentParsingResult,
)


ROOT = Path(__file__).resolve().parents[2]
BACKEND_APP = ROOT / "backend" / "app"

PARSER = (
    BACKEND_APP
    / "document_parsing"
    / "parser.py"
)

SERVICE = (
    BACKEND_APP
    / "services"
    / "document_content_parsing_application_service.py"
)

LEGACY = (
    BACKEND_APP
    / "knowledge"
    / "document_parser.py"
)

ALEMBIC_INI = ROOT / "backend" / "alembic.ini"


def _tree(path: Path) -> ast.Module:
    assert path.is_file()
    return ast.parse(path.read_text())


def _imports(path: Path) -> set[str]:
    modules: set[str] = set()

    for node in ast.walk(_tree(path)):
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


def _app_imports(path: Path) -> set[str]:
    return {
        module
        for module in _imports(path)
        if module == "app"
        or module.startswith("app.")
    }


def _defined_public_classes(path: Path) -> set[str]:
    return {
        node.name
        for node in _tree(path).body
        if isinstance(node, ast.ClassDef)
        and not node.name.startswith("_")
    }


def test_parser_port_public_surface_is_exact() -> None:
    assert _defined_public_classes(PARSER) == {
        "DocumentContentParser",
        "DocumentContentParserUnsupportedMediaTypeError",
        "DocumentContentParserInvalidContentError",
    }

    assert issubclass(
        DocumentContentParserUnsupportedMediaTypeError,
        Exception,
    )
    assert issubclass(
        DocumentContentParserInvalidContentError,
        Exception,
    )


def test_parser_port_depends_only_on_canonical_descriptor() -> None:
    assert _app_imports(PARSER) == {
        "app.domain.document_content",
    }


def test_parser_operation_is_keyword_only_and_textual() -> None:
    signature = inspect.signature(
        DocumentContentParser.parse
    )
    parameters = list(signature.parameters.values())

    assert [parameter.name for parameter in parameters] == [
        "self",
        "descriptor",
        "payload",
    ]

    assert parameters[1].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters[2].kind is inspect.Parameter.KEYWORD_ONLY

    hints = get_type_hints(DocumentContentParser.parse)

    assert hints["descriptor"] is DocumentContentDescriptor
    assert hints["return"] is str


def test_application_public_surface_is_exact() -> None:
    assert _defined_public_classes(SERVICE) == {
        "DocumentContentParsingRequest",
        "DocumentContentParsingResult",
        "DocumentContentParsingApplicationService",
    }


def test_application_request_and_result_annotations_are_exact() -> None:
    request_hints = get_type_hints(
        DocumentContentParsingRequest
    )
    result_hints = get_type_hints(
        DocumentContentParsingResult
    )

    assert request_hints == {
        "document_id": EntityId,
    }

    assert result_hints == {
        "descriptor": DocumentContentDescriptor,
        "text": str,
    }


def test_application_has_exact_two_dependencies() -> None:
    signature = inspect.signature(
        DocumentContentParsingApplicationService.__init__
    )
    parameters = list(signature.parameters.values())

    assert [parameter.name for parameter in parameters] == [
        "self",
        "content_access_service",
        "parser",
    ]

    assert parameters[1].kind is inspect.Parameter.KEYWORD_ONLY
    assert parameters[2].kind is inspect.Parameter.KEYWORD_ONLY

    hints = get_type_hints(
        DocumentContentParsingApplicationService.__init__
    )

    assert (
        hints["content_access_service"]
        is DocumentContentAccessApplicationService
    )
    assert hints["parser"] is DocumentContentParser


def test_application_imports_only_accepted_rfc074_dependencies() -> None:
    assert _app_imports(SERVICE) == {
        "app.document_parsing.parser",
        "app.domain.base",
        "app.domain.document_content",
        "app.services.document_content_access_application_service",
    }


def test_application_has_no_direct_persistence_or_runtime_dependency() -> None:
    forbidden_prefixes = (
        "app.document.repository",
        "app.document_content.repository",
        "app.document_content.store",
        "app.infrastructure",
        "app.core",
        "sqlalchemy",
        "alembic",
    )

    imports = _imports(SERVICE)

    assert not any(
        module.startswith(forbidden_prefixes)
        for module in imports
    )


def test_application_does_not_own_stream_operations() -> None:
    source = SERVICE.read_text()

    for marker in (
        ".close(",
        ".seek(",
        ".tell(",
        ".fileno(",
        "source_reference",
    ):
        assert marker not in source


def test_rfc074_does_not_promote_downstream_capabilities() -> None:
    source = (
        PARSER.read_text()
        + "\n"
        + SERVICE.read_text()
    ).lower()

    forbidden = (
        "pypdf",
        "pdfplumber",
        "python-docx",
        "openpyxl",
        "tesseract",
        "documentknowledgeingestion",
        "knowledgecapture",
        "qdrant",
        "neo4j",
        "embedding",
        "chunking",
        "language model",
    )

    assert not any(
        marker in source
        for marker in forbidden
    )


def test_legacy_document_parser_seam_remains_unpromoted() -> None:
    assert LEGACY.is_file()
    assert LEGACY.read_text().strip() == ""


def test_services_package_does_not_reexport_rfc074_surface() -> None:
    initializer = (
        BACKEND_APP
        / "services"
        / "__init__.py"
    )

    if initializer.exists():
        source = initializer.read_text()

        assert "DocumentContentParsing" not in source


def test_default_runtime_and_composition_do_not_import_rfc074() -> None:
    files = [
        *(
            BACKEND_APP
            / "core"
            / "composition"
        ).rglob("*.py"),
        BACKEND_APP / "core" / "runtime.py",
        BACKEND_APP / "core" / "bootstrap.py",
        BACKEND_APP / "core" / "bootstrap_manager.py",
    ]

    marker = (
        "app.services."
        "document_content_parsing_application_service"
    )

    violations = [
        str(path.relative_to(ROOT))
        for path in files
        if path.is_file()
        and marker in path.read_text()
    ]

    assert violations == []


def test_no_concrete_parser_library_is_selected() -> None:
    imports = _imports(PARSER) | _imports(SERVICE)

    selected = {
        module
        for module in imports
        if module.split(".", 1)[0]
        not in sys.stdlib_module_names
        and not module.startswith("app.")
    }

    assert selected == set()


def test_canonical_alembic_head_remains_0005() -> None:
    config = Config(str(ALEMBIC_INI))
    scripts = ScriptDirectory.from_config(config)

    assert scripts.get_current_head() == "0005"
