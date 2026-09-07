"""RFC-076 parser binding and registry-backed resolver architecture tests."""

from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

BINDING = (
    ROOT
    / "backend/app/document_parsing/binding.py"
)

ADAPTER_INIT = (
    ROOT
    / "backend/app/infrastructure/document_parsing/__init__.py"
)

ADAPTER = (
    ROOT
    / "backend/app/infrastructure/document_parsing/"
    "registry_backed_resolver.py"
)

PARSER = (
    ROOT
    / "backend/app/document_parsing/parser.py"
)

RESOLVER = (
    ROOT
    / "backend/app/document_parsing/resolver.py"
)

DISPATCHER = (
    ROOT
    / "backend/app/document_parsing/dispatching_parser.py"
)

RFC074_SERVICE = (
    ROOT
    / "backend/app/services/"
    "document_content_parsing_application_service.py"
)

RFC075_TEST1 = (
    ROOT
    / "tests/document_parsing/"
    "test_document_content_parser_resolution.py"
)

RFC075_TEST2 = (
    ROOT
    / "tests/document_parsing/"
    "test_document_content_parser_resolution_architecture.py"
)

REGISTRY = (
    ROOT
    / "backend/app/core/registry/registry.py"
)

REGISTRY_ERRORS = (
    ROOT
    / "backend/app/core/registry/errors.py"
)

REGISTRY_INIT = (
    ROOT
    / "backend/app/core/registry/__init__.py"
)

DOCUMENT_CONTENT = (
    ROOT
    / "backend/app/domain/document_content.py"
)

EXPECTED_SHA256 = {
    PARSER: (
        "35ac46cfb17ed769a49c87df3e7cb5a7"
        "aa438bec60b5ff3511b6e40d7f557787"
    ),
    RESOLVER: (
        "85f0bff5985028b8246fda0412cd608f"
        "ad1b2e636afe2a760825c2edb00ea713"
    ),
    DISPATCHER: (
        "bd1cd81fb56b5afc1227d3e3b9361fd"
        "6ede359112ae0d8c3a761de0037224a8b"
    ),
    RFC074_SERVICE: (
        "e132a02d0d7e7981a09013d608676084"
        "ad6e29b6ce0bb3dd0f3f1567cdd28fa7"
    ),
    RFC075_TEST1: (
        "534ebfc68ccd7ce9f19bfa7e9b393563"
        "fef7d5fb6ef2bcfc67aefea7f625fae2"
    ),
    RFC075_TEST2: (
        "c51444fcf14d82b96a9c8db5fbf37604"
        "7b9114a1d3bb645d67e18ac19aea4af2"
    ),
    REGISTRY: (
        "a8bb351539e4ffc2bae4cae2f2a87155"
        "977206990e4108ba12902b10b6e172c5"
    ),
    REGISTRY_ERRORS: (
        "2c51f675ef3f2e3d8e80e3c71c391570"
        "625badad3c088a79d430727581dc741a"
    ),
    REGISTRY_INIT: (
        "390f439e19e0f83543f53d6d7c0a14a"
        "56227b1ce1dc535b6ac609f4b7e219adb"
    ),
    DOCUMENT_CONTENT: (
        "df830249fc611acfca62f9ebe1a340ea8"
        "bd4c14bff0365d909668b03256ddbc9"
    ),
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sha256(path: Path) -> str:
    return sha256(
        path.read_bytes()
    ).hexdigest()


def _tree(path: Path) -> ast.Module:
    return ast.parse(
        _text(path),
    )


def _resolver_class() -> ast.ClassDef:
    classes = [
        node
        for node in _tree(ADAPTER).body
        if isinstance(node, ast.ClassDef)
        and node.name
        == "RegistryBackedDocumentContentParserResolver"
    ]

    assert len(classes) == 1

    return classes[0]


def test_binding_module_exists() -> None:
    assert BINDING.is_file()


def test_registry_backed_resolver_package_and_module_exist() -> None:
    assert ADAPTER_INIT.is_file()
    assert ADAPTER.is_file()


def test_rfc074_and_rfc075_contracts_remain_byte_identical() -> None:
    for path in (
        PARSER,
        RESOLVER,
        DISPATCHER,
        RFC074_SERVICE,
        RFC075_TEST1,
        RFC075_TEST2,
    ):
        assert _sha256(path) == EXPECTED_SHA256[path]


def test_generic_registry_and_media_type_domain_remain_byte_identical() -> None:
    for path in (
        REGISTRY,
        REGISTRY_ERRORS,
        REGISTRY_INIT,
        DOCUMENT_CONTENT,
    ):
        assert _sha256(path) == EXPECTED_SHA256[path]


def test_binding_module_remains_domain_neutral() -> None:
    source = _text(BINDING).lower()

    forbidden = (
        "app.infrastructure",
        "app.services",
        "app.core.registry",
        "sqlalchemy",
        "alembic",
        "sqlite",
        "postgres",
        "runtime",
        "bootstrap",
        "composition",
        "pypdf",
        "pdfplumber",
        "pymupdf",
        "docx",
        "openpyxl",
        "tesseract",
        "easyocr",
    )

    for token in forbidden:
        assert token not in source


def test_adapter_avoids_application_runtime_persistence_and_concrete_parsers() -> None:
    source = _text(ADAPTER).lower()

    forbidden = (
        "app.services",
        "app.core.composition",
        "app.core.bootstrap",
        "app.core.runtime",
        "app.api",
        "sqlalchemy",
        "alembic",
        "sqlite",
        "postgres",
        "filesystem",
        "pypdf",
        "pdfplumber",
        "pymupdf",
        "python-docx",
        "openpyxl",
        "tika",
        "textract",
        "tesseract",
        "easyocr",
    )

    for token in forbidden:
        assert token not in source


def test_adapter_reuses_existing_registry_without_defining_another_registry() -> None:
    source = _text(ADAPTER)
    tree = _tree(ADAPTER)

    assert "Registry[DocumentContentParserBinding]" in source

    assert not any(
        isinstance(node, ast.ClassDef)
        and node.name == "Registry"
        for node in tree.body
    )


def test_parser_factory_is_not_registered_directly() -> None:
    register_calls = []

    for node in ast.walk(_tree(ADAPTER)):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "register"
        ):
            register_calls.append(node)

    assert len(register_calls) == 1

    call = register_calls[0]

    if len(call.args) >= 2:
        supplier = call.args[1]
    else:
        supplier = next(
            keyword.value
            for keyword in call.keywords
            if keyword.arg == "factory"
        )

    assert ".factory" not in ast.unparse(supplier)


def test_registry_lookup_precedes_parser_factory_invocation() -> None:
    resolver_class = _resolver_class()
    methods = {
        node.name: node
        for node in resolver_class.body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }

    operation = methods["resolve"]

    registry_resolve_calls = []
    parser_factory_calls = []

    for node in ast.walk(operation):
        if not isinstance(node, ast.Call):
            continue

        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "resolve"
            and isinstance(node.func.value, ast.Attribute)
            and node.func.value.attr == "_registry"
        ):
            registry_resolve_calls.append(node)

        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "factory"
        ):
            parser_factory_calls.append(node)

    assert len(registry_resolve_calls) == 1
    assert len(parser_factory_calls) == 1

    assert (
        registry_resolve_calls[0].lineno
        < parser_factory_calls[0].lineno
    )


def test_adapter_exposes_only_resolve_as_public_operation() -> None:
    public_methods = [
        node.name
        for node in _resolver_class().body
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
        and not node.name.startswith("_")
    ]

    assert public_methods == [
        "resolve",
    ]


def test_no_module_level_registry_instance_exists() -> None:
    tree = _tree(ADAPTER)

    module_level_values = []

    for node in tree.body:
        if isinstance(node, ast.Assign):
            module_level_values.append(node.value)
        elif isinstance(node, ast.AnnAssign):
            module_level_values.append(node.value)

    for value in module_level_values:
        if not isinstance(value, ast.Call):
            continue

        assert not (
            isinstance(value.func, ast.Name)
            and value.func.id == "Registry"
        )
