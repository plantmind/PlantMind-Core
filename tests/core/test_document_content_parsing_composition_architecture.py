"""RFC-078 document parsing composition architecture tests."""

from __future__ import annotations

import ast
import hashlib
import inspect
import subprocess
from dataclasses import fields, is_dataclass
from importlib import import_module
from pathlib import Path
from typing import get_type_hints

from app.document_parsing.binding import DocumentContentParserBinding
from app.document_parsing.dispatching_parser import (
    DispatchingDocumentContentParser,
)
from app.infrastructure.document_parsing.registry_backed_resolver import (
    RegistryBackedDocumentContentParserResolver,
)
from app.infrastructure.document_parsing.utf8_plain_text_parser import (
    Utf8PlainTextDocumentContentParser,
)
from app.services.document_content_access_application_service import (
    DocumentContentAccessApplicationService,
)
from app.services.document_content_parsing_application_service import (
    DocumentContentParsingApplicationService,
)


ROOT = Path(__file__).resolve().parents[2]

TARGET = (
    ROOT
    / "backend/app/core/composition/"
    "document_content_parsing.py"
)

GUARD_TEST = (
    ROOT
    / "tests/document_parsing/"
    "test_utf8_plain_text_document_content_parser_architecture.py"
)

EXPECTED_GUARD_SHA256 = "1a469b6799ac2cb1740b28ce9067129cda5845248b199f1fc86f48dfccc4048d"

PRESERVED_PRODUCTION_SHA256 = {'backend/app/core/bootstrap.py': '07736041461a3ebcc69f48f8560495f032176596da1a926197800a843bec0240',
 'backend/app/core/bootstrap_manager.py': '0bb6180ac20ef92117b1038554076083c9cf4adada615fc1d4c09f0e9f6837cf',
 'backend/app/core/composition/__init__.py': '269ae463ecfd1455c1bfda563d67643b7546ef9d6d13cc6f8f9febb2e06843a5',
 'backend/app/core/composition/composition_root.py': '563ad20be949c66e47298c20dff7a2c8e3de8afc5048fdc03eb71156c7d47138',
 'backend/app/core/container/__init__.py': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
 'backend/app/core/container/service_container.py': '3e66943d51d01fbadf191c3e421fef35c3c6906c5e058d7d5ed1897f3bfde434',
 'backend/app/core/registry/__init__.py': '390f439e19e0f83543f53d6d7c0a14a56227b1ce1dc535b6ac609f4b7e219adb',
 'backend/app/core/registry/errors.py': '2c51f675ef3f2e3d8e80e3c71c391570625badad3c088a79d430727581dc741a',
 'backend/app/core/registry/registry.py': 'a8bb351539e4ffc2bae4cae2f2a87155977206990e4108ba12902b10b6e172c5',
 'backend/app/core/runtime.py': '6e5e8a3366be72d324ef13c19ac6c4d0735299880138ead283ded525e3ce7e5c',
 'backend/app/core/runtime_state.py': '3acc2f4ce7b3f29690b5524f4446d3bbf9c96d65dd540db2a9cdcbcfa810e83b',
 'backend/app/document_parsing/binding.py': '63332e5228ff3db644fed05ce89c0ad583d099852aae2aa5f118ea8e6667c4cc',
 'backend/app/document_parsing/dispatching_parser.py': 'bd1cd81fb56b5afc1227d3e3b9361fd6ede359112ae0d8c3a761de0037224a8b',
 'backend/app/document_parsing/parser.py': '35ac46cfb17ed769a49c87df3e7cb5a7aa438bec60b5ff3511b6e40d7f557787',
 'backend/app/document_parsing/resolver.py': '85f0bff5985028b8246fda0412cd608fad1b2e636afe2a760825c2edb00ea713',
 'backend/app/domain/document_content.py': 'df830249fc611acfca62f9ebe1a340ea8bd4c14bff0365d909668b03256ddbc9',
 'backend/app/infrastructure/database/runtime.py': 'df7519b296a4b3673e37bfad513b7e242759cbb55e02af991c4f2894899a37a8',
 'backend/app/infrastructure/document_parsing/__init__.py': '39abfbba5fdcff705ec3db33ab5a6f544bda5335a4c5f67dcf78a87c79b722cd',
 'backend/app/infrastructure/document_parsing/registry_backed_resolver.py': 'b7fd2dff4716138832aeaa0d659f52d0573315b294e141d45fa78d2c31befa10',
 'backend/app/infrastructure/document_parsing/utf8_plain_text_parser.py': '539aec40256bc68bdd1f4d142f274294eff3efb38b6f140fb26c63b06dd0be0d',
 'backend/app/main.py': 'a852e4f463b8704b5fcb328a17581bd724a7c5ea25d3ee8b995abec1c3285efb',
 'backend/app/services/document_content_access_application_service.py': '2ffe2984ad9e5e1b2cbb6860093cb26060b3911d40259bb678d7dde1458c5e0a',
 'backend/app/services/document_content_parsing_application_service.py': 'e132a02d0d7e7981a09013d608676084ad6e29b6ce0bb3dd0f3f1567cdd28fa7'}
PRESERVED_TEST_SHA256 = {'tests/document_parsing/test_document_content_parser_binding_and_registry_resolver.py': 'b409c25f458c69de8751739e58e3b90c612a479887a94b171da041cc9c8ee601',
 'tests/document_parsing/test_document_content_parser_binding_and_registry_resolver_architecture.py': '004b8c94db79043848409c9b3622d1cce0149578e0d83f46f500aef52964de1d',
 'tests/document_parsing/test_document_content_parser_resolution.py': '534ebfc68ccd7ce9f19bfa7e9b393563fef7d5fb6ef2bcfc67aefea7f625fae2',
 'tests/document_parsing/test_document_content_parser_resolution_architecture.py': 'c51444fcf14d82b96a9c8db5fbf376047b9114a1d3bb645d67e18ac19aea4af2',
 'tests/document_parsing/test_utf8_plain_text_document_content_parser.py': '71a1cb72786e0ab65f9647587601757a2bfb290f241f56b78b1608223af96aaf',
 'tests/services/test_document_content_access_application_service.py': '2ef737aa58e018a9827a0e99e2ba68744236a5e3b66fc5d72f9969af9c7e40fd',
 'tests/services/test_document_content_access_architecture.py': '8eb79b4b809de156a667b720e0d3d29bbd2c5f8ca4c1cdf80d265ee5e6653c01',
 'tests/services/test_document_content_parsing_application_service.py': '59d58a33b8438c2e62b9693efbbdc69f16954d85d2305cfd995bac5375084c09',
 'tests/services/test_document_content_parsing_architecture.py': '71e4207f6f00bc7c2d96370c62172daf30ccde4f523c5a6b1363727d3a9971a4'}
REQUIREMENTS_SHA256 = {'backend/requirements.txt': 'f1e9b44db3f10e76b3a7041d81285c581adc728b41167b3becc2344ff7c53251'}
MIGRATION_SHA256 = {'backend/alembic.ini': '4be35c86b24192bde1327811488c4fcbc1f446b8c1e688fbbcba8f27640a252b',
 'backend/migrations/env.py': '38813fe44f3028c4568eabb98cb8249d33bf12f9ac1a0c1117a91e5ada13bf60',
 'backend/migrations/script.py.mako': 'fd7be8ed2f31410a1f01dccda809e7b7610e8fae7ad1b91327d48439fd6540fb',
 'backend/migrations/versions/0001_database_foundation.py': '931d525ca554d4b8b0cfa6ac62824a050267f0bdba99fef9047071e91a607cff',
 'backend/migrations/versions/0002_knowledge_records.py': '9d2909bc6a86c8e0a8b16da471e5623d0133f04fd8edac8e44262f7e8750b724',
 'backend/migrations/versions/0003_enterprise_documents.py': 'c5242e0e6ed68961bef33f8dd923668f1107f3f7cd8a8f6d67c0750365775399',
 'backend/migrations/versions/0004_document_knowledge_lineages.py': '800598696415cd207dcb472ec920caafc73e3663623d146b663dbf1d63e39202',
 'backend/migrations/versions/0005_document_content_descriptors.py': '8bd4a8dcea0380aae6b43b1f9bdb134197b4d181c4b000395157476efbc8ef33'}

EXPECTED_IMPORTS = {
    "__future__",
    "dataclasses",
    "app.document_parsing.binding",
    "app.document_parsing.dispatching_parser",
    "app.domain.document_content",
    (
        "app.infrastructure.document_parsing."
        "registry_backed_resolver"
    ),
    (
        "app.infrastructure.document_parsing."
        "utf8_plain_text_parser"
    ),
    (
        "app.services."
        "document_content_access_application_service"
    ),
    (
        "app.services."
        "document_content_parsing_application_service"
    ),
}

EXACT_ALLOWED_REFERENCE = (
    "backend/app/core/composition/"
    "document_content_parsing.py"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def _source() -> str:
    return TARGET.read_text(encoding="utf-8")


def _module():
    return import_module(
        "app.core.composition.document_content_parsing"
    )


def _production_references() -> list[str]:
    class_name = "Utf8PlainTextDocumentContentParser"
    module_name = (
        "app.infrastructure.document_parsing."
        "utf8_plain_text_parser"
    )
    parser_target = (
        ROOT
        / "backend/app/infrastructure/document_parsing/"
        "utf8_plain_text_parser.py"
    )
    references = []

    for path in (ROOT / "backend/app").rglob("*.py"):
        if path == parser_target:
            continue

        text = path.read_text(
            encoding="utf-8",
        )

        if class_name in text or module_name in text:
            references.append(
                path.relative_to(ROOT).as_posix()
            )

    return references


def test_document_content_parsing_composition_module_exists() -> None:
    assert TARGET.is_file()


def test_composition_result_is_frozen_slot_backed_and_keyword_only() -> None:
    composition_type = (
        _module()
        .DocumentContentParsingComposition
    )

    assert is_dataclass(composition_type)
    assert composition_type.__dataclass_params__.frozen is True
    assert composition_type.__slots__ == (
        "plain_text_parser",
        "plain_text_binding",
        "resolver",
        "dispatcher",
        "application_service",
    )

    signature = inspect.signature(composition_type)

    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )


def test_composition_result_fields_are_exact_and_typed() -> None:
    composition_type = (
        _module()
        .DocumentContentParsingComposition
    )

    assert tuple(
        field.name
        for field in fields(composition_type)
    ) == (
        "plain_text_parser",
        "plain_text_binding",
        "resolver",
        "dispatcher",
        "application_service",
    )

    hints = get_type_hints(composition_type)

    assert hints == {
        "plain_text_parser": Utf8PlainTextDocumentContentParser,
        "plain_text_binding": DocumentContentParserBinding,
        "resolver": RegistryBackedDocumentContentParserResolver,
        "dispatcher": DispatchingDocumentContentParser,
        "application_service": DocumentContentParsingApplicationService,
    }


def test_builder_signature_is_exact_keyword_only_contract() -> None:
    builder = (
        _module()
        .build_document_content_parsing_composition
    )
    signature = inspect.signature(builder)
    parameters = list(signature.parameters.values())

    assert [parameter.name for parameter in parameters] == [
        "content_access_service",
    ]
    assert (
        parameters[0].kind
        is inspect.Parameter.KEYWORD_ONLY
    )
    assert (
        parameters[0].default
        is inspect.Parameter.empty
    )

    hints = get_type_hints(builder)

    assert (
        hints["content_access_service"]
        is DocumentContentAccessApplicationService
    )
    assert (
        hints["return"]
        is _module().DocumentContentParsingComposition
    )


def test_only_expected_top_level_class_and_builder_are_defined() -> None:
    tree = ast.parse(_source())

    classes = [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]
    functions = [
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]

    assert classes == [
        "DocumentContentParsingComposition",
    ]
    assert functions == [
        "build_document_content_parsing_composition",
    ]


def test_import_surface_is_exact_and_layered() -> None:
    tree = ast.parse(_source())
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(
                alias.name
                for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")

    assert imports == EXPECTED_IMPORTS


def test_composition_source_has_no_forbidden_host_or_adapter_surface() -> None:
    source = _source().lower()

    forbidden = (
        "composition_root",
        "platformcomposition",
        "build_platform_composition",
        "servicecontainer",
        "service_container",
        "bootstrap",
        "runtime",
        "app.main",
        "fastapi",
        "apirouter",
        "sqlalchemy",
        "alembic",
        "repository",
        "content_store",
        "filesystem",
        "database",
        "configuration",
        "importlib",
        "getattr(",
        "setattr(",
        "globals(",
        "locals(",
        "eval(",
        "exec(",
        ".open(",
        ".parse(",
    )

    for token in forbidden:
        assert token not in source


def test_builder_contains_no_exception_translation_or_context_management() -> None:
    tree = ast.parse(_source())
    builder = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name
        == "build_document_content_parsing_composition"
    )

    assert not any(
        isinstance(
            node,
            (
                ast.Try,
                ast.With,
                ast.AsyncWith,
                ast.Raise,
            ),
        )
        for node in ast.walk(builder)
        if not (
            isinstance(node, ast.Raise)
            and isinstance(node.exc, ast.Call)
            and isinstance(node.exc.func, ast.Name)
            and node.exc.func.id == "TypeError"
        )
    )


def test_no_mutable_module_level_state_or_constructed_graph() -> None:
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
                ast.Call,
            ),
        )


def test_default_composition_and_runtime_files_are_byte_preserved() -> None:
    for relative, expected in PRESERVED_PRODUCTION_SHA256.items():
        path = ROOT / relative

        assert path.is_file()
        assert _sha256(path) == expected


def test_existing_rfc073_through_rfc077_tests_match_authorized_state() -> None:
    for relative, expected in PRESERVED_TEST_SHA256.items():
        path = ROOT / relative

        assert path.is_file()
        assert _sha256(path) == expected


def test_rfc077_guard_is_exact_authorized_successor_adaptation() -> None:
    assert GUARD_TEST.is_file()
    assert _sha256(GUARD_TEST) == EXPECTED_GUARD_SHA256

    source = GUARD_TEST.read_text(
        encoding="utf-8",
    )

    assert (
        "def test_parser_is_not_wired_or_registered_elsewhere()"
        " -> None:"
    ) in source
    assert (
        'class_name = "Utf8PlainTextDocumentContentParser"'
    ) in source
    assert (
        '"app.infrastructure.document_parsing."'
    ) in source
    assert (
        '"utf8_plain_text_parser"'
    ) in source
    assert (
        'allowed_reference = ('
    ) in source
    assert (
        '"backend/app/core/composition/"'
    ) in source
    assert (
        '"document_content_parsing.py"'
    ) in source
    assert (
        "assert references == [allowed_reference]"
    ) in source
    assert "assert references == []" not in source

    function_source = source[
        source.index(
            "def test_parser_is_not_wired_or_registered_elsewhere"
        ):
    ]

    assert ".startswith(" not in function_source
    assert "fnmatch" not in function_source
    assert "allowed_references" not in function_source


def test_plain_text_parser_has_exactly_one_production_reference() -> None:
    assert _production_references() == [
        EXACT_ALLOWED_REFERENCE,
    ]


def test_default_composition_package_exports_remain_unchanged() -> None:
    relative = "backend/app/core/composition/__init__.py"

    assert (
        _sha256(ROOT / relative)
        == PRESERVED_PRODUCTION_SHA256[relative]
    )


def test_requirements_files_are_byte_preserved() -> None:
    for relative, expected in REQUIREMENTS_SHA256.items():
        path = ROOT / relative

        assert path.is_file()
        assert _sha256(path) == expected


def test_migration_inventory_and_bytes_are_preserved() -> None:
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

    observed = set()

    for relative in tracked:
        if relative.startswith(("tests/", "docs/")):
            continue

        parts = set(Path(relative).parts)

        if (
            "alembic" in parts
            or "migrations" in parts
            or relative.endswith("alembic.ini")
        ):
            observed.add(relative)

    assert observed == set(MIGRATION_SHA256)
    assert current == MIGRATION_SHA256


def test_no_repository_store_database_or_api_import_is_added() -> None:
    tree = ast.parse(_source())
    imported_modules = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(
                alias.name
                for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            imported_modules.add(node.module or "")

    forbidden_fragments = (
        ".repository",
        ".store",
        ".database",
        ".api",
        "sqlalchemy",
        "fastapi",
    )

    assert not any(
        fragment in imported
        for imported in imported_modules
        for fragment in forbidden_fragments
    )


def test_composition_module_has_no_public_registration_or_lifecycle_api() -> None:
    module = _module()
    public_names = {
        name
        for name in vars(module)
        if not name.startswith("_")
    }

    assert "register" not in public_names
    assert "clear" not in public_names
    assert "start" not in public_names
    assert "stop" not in public_names
    assert "close" not in public_names
    assert "configure" not in public_names


def test_source_contains_exact_text_plain_binding_and_single_binding_tuple() -> None:
    source = _source()

    assert 'value="text/plain"' in source
    assert "bindings=(plain_text_binding,)" in source
    assert "factory=provide_plain_text_parser" in source


def test_source_has_no_fallback_alias_or_dynamic_discovery() -> None:
    source = _source().lower()

    forbidden = (
        "fallback",
        "alias",
        "wildcard",
        "default_parser",
        "sniff",
        "discover",
        "scan",
        "plugin",
        "hot_register",
    )

    for token in forbidden:
        assert token not in source
