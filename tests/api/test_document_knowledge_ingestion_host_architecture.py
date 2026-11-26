"""RFC-083: explicit transport hosting without a second composition owner."""
import ast
from hashlib import sha256
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "backend/app/api/document_knowledge_ingestion_host.py"
PRESERVED = {
    "backend/app/main.py": "a852e4f463b8704b5fcb328a17581bd724a7c5ea25d3ee8b995abec1c3285efb",
    "backend/app/core/bootstrap_manager.py": "0bb6180ac20ef92117b1038554076083c9cf4adada615fc1d4c09f0e9f6837cf",
    "backend/app/core/composition/composition_root.py": "12749403b5e707806fecb61278cd2f4afe10846709ebc918c501d8c19c368374",
    "backend/app/core/composition/__init__.py": "269ae463ecfd1455c1bfda563d67643b7546ef9d6d13cc6f8f9febb2e06843a5",
    "backend/app/api/request_admission.py": "b1a5384d2912e125a2f27f5643f6da7aff92e49839ccd936a7106b85ac79f8b3",
    "backend/app/api/document_knowledge_ingestion.py": "37495325e90275082ed0fc9865e5fb7f45e4937042d2bd064a0fe74a7b5321de",
    "tests/core/test_document_content_parsing_composition_architecture.py": "6b7d443ca6764e0b1098293a179ac15ed71eda6e6a9328624112af98220f3120",
    "tests/services/test_parsed_document_knowledge_ingestion_architecture.py": "d95f910f411fc442b77823d97e4bce2d76a88729f90e4a418f477d9cbd8aedb5",
    "tests/services/test_application_facade_document_knowledge_ingestion_architecture.py": "151e7d144617b180dc5cd9b05419a8ea4e7a9a4917a272cef09698f944cd6cbb",
    "tests/api/test_document_knowledge_ingestion_api_architecture.py": "5f0acc5f6f32028d41d6a7dd1f7c00f4763c705d6b7fafc525897266d1076d2b",
    "tests/core/test_document_knowledge_ingestion_composition_architecture.py": "16e3a55f8313716ab989d3d758f30e9ab3d8a66d79a61d4c12e4d155ccc75a3a",
}


def _source():
    return ast.parse(TARGET.read_text(encoding="utf-8"))


def _imports(tree):
    return {
        item.asname or item.name: node.module + "." + item.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for item in node.names
    }


def _name(node, bindings):
    if isinstance(node, ast.Name):
        return bindings.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        return _name(node.value, bindings) + "." + node.attr
    return "<dynamic>"


def test_imports_are_only_existing_transport_and_platform_contracts():
    tree = _source()
    allowed = {
        "__future__": {"annotations"},
        "collections.abc": {"AsyncIterator"},
        "contextlib": {"asynccontextmanager"},
        "fastapi": {"FastAPI"},
        "app.api.document_knowledge_ingestion": {"create_router"},
        "app.api.operational_transition": {"create_router"},
        "app.api.request_admission": {"RequestAdmissionMiddleware"},
        "app.config": {"settings"},
        "app.core.composition": {"PlatformComposition"},
        "app.schemas.platform": {"PlatformInfo", "PlatformStatus", "RuntimeInfo"},
    }
    assert not any(isinstance(node, ast.Import) for node in ast.walk(tree))
    declarations = [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
    for node in declarations:
        assert node in tree.body and node.level == 0
        assert node.module in allowed
        assert {item.name for item in node.names} <= allowed[node.module]
    required = {
        module + "." + name
        for module, names in allowed.items()
        if module not in {"__future__", "collections.abc"}
        for name in names
    }
    assert required <= set(_imports(tree).values())


def test_import_defines_only_the_required_factory_without_executing_a_graph():
    tree = _source()
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert [node.name for node in functions] == ["create_app"]
    for node in tree.body:
        assert isinstance(node, (ast.ImportFrom, ast.FunctionDef)) or (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        )
    factory = functions[0]
    assert not factory.decorator_list
    args = factory.args
    assert not args.posonlyargs and not args.args and not args.defaults
    assert args.vararg is None and args.kwarg is None
    assert [item.arg for item in args.kwonlyargs] == ["platform"]
    assert args.kw_defaults == [None]
    bindings = _imports(tree)
    assert _name(args.kwonlyargs[0].annotation, bindings) == "app.core.composition.PlatformComposition"
    assert _name(factory.returns, bindings) == "fastapi.FastAPI"
    assert not any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))


def test_calls_delegate_transport_and_lifecycle_without_resource_ownership():
    tree = _source()
    bindings = _imports(tree)
    factories = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                 and isinstance(node.value, ast.Call)
                 and _name(node.value.func, bindings) == "fastapi.FastAPI"]
    assert len(factories) == 1
    assert len(factories[0].targets) == 1 and isinstance(factories[0].targets[0], ast.Name)
    bindings[factories[0].targets[0].id] = "<host>"
    allowed = {
        "isinstance", "TypeError", "fastapi.FastAPI",
        "app.api.document_knowledge_ingestion.create_router",
        "app.api.operational_transition.create_router",
        "app.schemas.platform.PlatformInfo", "app.schemas.platform.PlatformStatus",
        "app.schemas.platform.RuntimeInfo", "<host>.add_middleware", "<host>.include_router",
        "<host>.get", "platform.bootstrap.startup", "platform.bootstrap.shutdown",
        "platform.health.get_status",
    }
    calls = [_name(node.func, bindings) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    assert set(calls) <= allowed
    assert calls.count("app.api.document_knowledge_ingestion.create_router") == 1
    assert calls.count("app.api.operational_transition.create_router") == 1
    assert calls.count("<host>.add_middleware") == 1
    assert calls.count("platform.bootstrap.startup") == 1
    assert calls.count("platform.bootstrap.shutdown") == 1
    assert not any(isinstance(node, (ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler,
                                     ast.With, ast.AsyncWith, ast.Global, ast.Nonlocal))
                   for node in ast.walk(tree))
    assert not any(isinstance(node, (ast.Attribute, ast.Subscript))
                   and isinstance(node.ctx, (ast.Store, ast.Del)) for node in ast.walk(tree))
    components = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
                  and isinstance(node.value, ast.Name) and node.value.id == "platform"}
    assert components <= {"bootstrap", "runtime", "health", "application_facade",
                          "operational_transition_application_service"}


def test_explicit_host_is_not_imported_by_default_entry_or_package_initializers():
    files = {ROOT / "backend/app/main.py"}
    files.update((ROOT / "backend/app").rglob("__init__.py"))
    files.update((ROOT / "backend/app/core").rglob("*.py"))
    for path in files:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                assert not any("document_knowledge_ingestion_host" in item.name for item in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert "document_knowledge_ingestion_host" not in (node.module or "")
                assert not any(item.name == "document_knowledge_ingestion_host" for item in node.names)


@pytest.mark.parametrize("relative", tuple(PRESERVED))
def test_default_boundaries_and_governed_guards_are_byte_preserved(relative):
    assert sha256((ROOT / relative).read_bytes()).hexdigest() == PRESERVED[relative]
