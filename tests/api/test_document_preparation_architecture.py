"""AD-070: a bounded transport adapter and an exact opt-in extension of AD-069."""

import ast
import inspect
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
HOST = ROOT / "backend/app/api/document_knowledge_ingestion_host.py"
ROUTER = ROOT / "backend/app/api/document_preparation.py"
ORIGINAL_HOST_AST_SHA256 = "0f63323383e0f57d70c1ffd1617dedb495dcf613e0e753a9a2394bb220947eb7"
PRESERVED = {
    "backend/app/services/enterprise_document_registration_application_service.py": "0363fff7386d6174750cdc1f44b44c8746099fbc132069acf8ba3915906bba37",
    "backend/app/services/document_content_establishment_application_service.py": "4f6e31b03fc118f44b3dc8f2322e084537bf6dcd7bff9ec6c79ea2ea647f1a94",
    "backend/app/services/application_facade.py": "3f9d53aaed7efa98c295f59fc5971e11a1a440724c42a9841b54932595a46b5b",
    "backend/app/core/composition/composition_root.py": "12749403b5e707806fecb61278cd2f4afe10846709ebc918c501d8c19c368374",
    "backend/app/document/repository.py": "38a38e5a18adde9a76a87908c90981908ce2f8b6c9dcb6a7578ae4d103430fbf",
    "backend/app/document_content/repository.py": "ace21180cab3a31fe89f4ac699c2dd96881a9037bf35b0e00e416a5a8b28d30e",
    "backend/app/document_content/store.py": "f82064df0deeb75940336d56748c2ed568555b6f02547050c44b2b77670a5e6f",
    "backend/app/domain/base.py": "230b7ae0e832be20980924c2da9642cfb4c4688f0099091c172e56a768701774",
    "backend/app/domain/document.py": "6c55ceed0d44dca13229b19ba7ebc792336f7b74f633c0269aa2400ec9739ed9",
    "backend/app/domain/document_content.py": "df830249fc611acfca62f9ebe1a340ea8bd4c14bff0365d909668b03256ddbc9",
    "tests/services/test_enterprise_document_registration_application_service.py": "8af40cdd6933e738cb8e4436d5015850f5a963c26bd9b7cd4dab5c9f35587cfa",
    "tests/services/test_document_content_establishment_architecture.py": "dda56c46b5bcd1afc4ee46880a34bab6699ea99327987e7fc9699eea1161ad90",
    "tests/services/test_document_knowledge_ingestion_architecture.py": "27b5e00d4a377fc32dc00d157f4c7be55ee0b41cc273ae8537ed8adb0214009d",
    "tests/integration/test_document_knowledge_ingestion_host_local_pipeline.py": "ac8577b38a075ca9df2442564c71099d0a62dd5ed55d1e1dd06057d855654e52",
}
_ADDED_IMPORTS = '''from app.api.document_preparation import create_router as create_document_preparation_router
from app.services.document_content_establishment_application_service import DocumentContentEstablishmentApplicationService
from app.services.enterprise_document_registration_application_service import EnterpriseDocumentRegistrationApplicationService
'''
_SIGNATURE = '''def create_app(
    *,
    platform: PlatformComposition,
    document_registration_service: EnterpriseDocumentRegistrationApplicationService | None = None,
    document_content_establishment_service: DocumentContentEstablishmentApplicationService | None = None,
) -> FastAPI:
    pass
'''
_PAIR_CHECK = '''if (
    (document_registration_service is None)
    != (document_content_establishment_service is None)
    or (
        document_registration_service is not None
        and not isinstance(
            document_registration_service,
            EnterpriseDocumentRegistrationApplicationService,
        )
    )
    or (
        document_content_establishment_service is not None
        and not isinstance(
            document_content_establishment_service,
            DocumentContentEstablishmentApplicationService,
        )
    )
):
    raise TypeError("Both preparation services must be supplied together as canonical instances.")
'''
_MOUNT = '''if document_registration_service is not None:
    app.include_router(
        create_document_preparation_router(
            document_registration_service=document_registration_service,
            document_content_establishment_service=document_content_establishment_service,
            runtime=platform.runtime,
        )
    )
'''


# BEGIN AD-070 A1 canonical host AST representation
# Frozen from the SHA-pinned original host and exact authorized host candidate.
# A new node class or field requires review; it is not silently normalized away.
HOST_AST_FIELDS = {
    "And": (),
    "Assign": ("targets", "value", "type_comment"),
    "AsyncFunctionDef": ("name", "args", "body", "decorator_list", "returns", "type_comment", "type_params"),
    "Attribute": ("value", "attr", "ctx"),
    "BinOp": ("left", "op", "right"),
    "BitOr": (),
    "BoolOp": ("op", "values"),
    "Call": ("func", "args", "keywords"),
    "Compare": ("left", "ops", "comparators"),
    "Constant": ("value", "kind"),
    "Expr": ("value",),
    "FunctionDef": ("name", "args", "body", "decorator_list", "returns", "type_comment", "type_params"),
    "If": ("test", "body", "orelse"),
    "ImportFrom": ("module", "names", "level"),
    "Is": (),
    "IsNot": (),
    "Load": (),
    "Module": ("body", "type_ignores"),
    "Name": ("id", "ctx"),
    "Not": (),
    "NotEq": (),
    "Or": (),
    "Raise": ("exc", "cause"),
    "Return": ("value",),
    "Store": (),
    "Subscript": ("value", "slice", "ctx"),
    "Try": ("body", "handlers", "orelse", "finalbody"),
    "UnaryOp": ("op", "operand"),
    "Yield": ("value",),
    "alias": ("name", "asname"),
    "arg": ("arg", "annotation", "type_comment"),
    "arguments": ("posonlyargs", "args", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults"),
    "keyword": ("arg", "value"),
}
_LOCATION_ATTRIBUTES = {"lineno", "col_offset", "end_lineno", "end_col_offset"}
_FUNCTION_NODES = {"FunctionDef", "AsyncFunctionDef"}


def normalized_host_dump(node):
    """Validate input before copying; retain exact fields and native None semantics."""
    if not isinstance(node, ast.AST):
        raise AssertionError("Host fingerprint requires parsed AST data.")
    originals, seen, pending = [], set(), [node]
    while pending:
        item = pending.pop()
        if id(item) in seen:
            continue
        seen.add(id(item))
        name = type(item).__name__
        if name not in HOST_AST_FIELDS:
            raise AssertionError("Unsupported host AST node: " + name)
        expected = HOST_AST_FIELDS[name]
        declared = item._fields
        legacy = name in _FUNCTION_NODES and declared == expected[:-1]
        if declared != expected and not legacy:
            raise AssertionError("Unsupported host AST field schema: " + name)
        attributes = set(vars(item))
        if attributes - set(expected) - _LOCATION_ATTRIBUTES:
            raise AssertionError("Unexpected host AST instance attribute: " + name)
        if name in _FUNCTION_NODES:
            parameters = getattr(item, "type_params", [] if legacy else None)
            if not isinstance(parameters, list):
                raise AssertionError("Host AST type_params must be a list: " + name)
            if legacy:
                # The old field schema does not enumerate these preserved children.
                pending.extend(child for child in parameters if isinstance(child, ast.AST))
        originals.append((item, expected, legacy, attributes))
        pending.extend(ast.iter_child_nodes(item))

    memo = {}
    normalized = deepcopy(node, memo)
    for original, expected, legacy, attributes in originals:
        copied = memo[id(original)]
        name = type(original).__name__
        if type(copied) is not type(original) or copied._fields != original._fields:
            raise AssertionError("AST copy changed node type or field schema: " + name)
        copied_attributes = set(vars(copied))
        allowed_additions = {"type_params"} if legacy and "type_params" not in attributes else set()
        if attributes - copied_attributes or copied_attributes - attributes - allowed_additions:
            raise AssertionError("AST copy synthesized or removed input attributes: " + name)
        if copied_attributes - attributes and copied.type_params != []:
            raise AssertionError("AST copy supplied a nonempty legacy default: " + name)
        if legacy:
            copied._fields = expected
            if "type_params" not in attributes:
                copied.type_params = []
    options = {"include_attributes": False}
    if "show_empty" in inspect.signature(ast.dump).parameters:
        options["show_empty"] = True
    return ast.dump(normalized, **options)
# END AD-070 A1 canonical host AST representation


def _dump(node):
    return normalized_host_dump(node)


def _verify_host_delta(source):
    """Remove only exact authorized nodes; hash all remaining approved behavior."""
    tree = ast.parse(source)
    for approved_import in ast.parse(_ADDED_IMPORTS).body:
        matches = [i for i, node in enumerate(tree.body) if _dump(node) == _dump(approved_import)]
        assert len(matches) == 1
        tree.body.pop(matches[0])
    factories = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "create_app"]
    assert len(factories) == 1
    factory = factories[0]
    assert _dump(factory.args) == _dump(ast.parse(_SIGNATURE).body[0].args)
    factory.args.kwonlyargs = factory.args.kwonlyargs[:1]
    factory.args.kw_defaults = factory.args.kw_defaults[:1]
    assert _dump(factory.body[2]) == _dump(ast.parse(_PAIR_CHECK).body[0])
    factory.body.pop(2)
    assert _dump(factory.body[7]) == _dump(ast.parse(_MOUNT).body[0])
    factory.body.pop(7)
    assert sha256(_dump(tree).encode()).hexdigest() == ORIGINAL_HOST_AST_SHA256


def test_host_delta_is_only_the_exact_pair_validation_and_conditional_router():
    source = HOST.read_text(encoding="utf-8")
    _verify_host_delta(source)
    _verify_host_delta(ast.unparse(ast.parse(source)))


@pytest.mark.parametrize("mutation", [
    "lifecycle", "runtime-write", "default-route", "resource-owner", "dependency",
    "copy-platform", "service-constructor", "pair-truthiness", "pair-validation",
    "wrong-pair-forwarding", "wrong-runtime", "duplicate-mount", "unconditional-mount",
    "wrong-default", "extra-keyword", "private-field", "platform-validation", "metadata",
])
def test_host_delta_guard_rejects_unrelated_or_widened_changes(mutation):
    tree = ast.parse(HOST.read_text(encoding="utf-8"))
    factory = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                   and node.name == "create_app")
    lifespan = next(node for node in factory.body if isinstance(node, ast.AsyncFunctionDef))
    mount = next(node for node in factory.body if _dump(node) == _dump(ast.parse(_MOUNT).body[0]))
    if mutation == "lifecycle":
        lifespan.body[0].value.func.attr = "shutdown"
    elif mutation == "runtime-write":
        factory.body.insert(3, ast.parse("platform.runtime.enable_request_admission()").body[0])
    elif mutation == "default-route":
        health = next(node for node in factory.body if isinstance(node, ast.FunctionDef)
                      and node.name == "health")
        health.decorator_list[0].args[0].value = "/health/"
    elif mutation == "resource-owner":
        lifespan.body[1].finalbody.append(ast.parse("platform.application_facade.close()").body[0])
    elif mutation == "dependency":
        tree.body.insert(2, ast.parse("from app.config import another_owner").body[0])
    elif mutation == "copy-platform":
        factory.body.insert(3, ast.parse("platform = copy(platform)").body[0])
    elif mutation == "service-constructor":
        factory.body.insert(3, ast.parse("EnterpriseDocumentRegistrationApplicationService()").body[0])
    elif mutation == "pair-truthiness":
        mount.test = ast.Name(id="document_registration_service", ctx=ast.Load())
    elif mutation == "pair-validation":
        factory.body[2].test = ast.Constant(value=False)
    elif mutation == "wrong-pair-forwarding":
        mount.body[0].value.args[0].keywords[0].value.id = "document_content_establishment_service"
    elif mutation == "wrong-runtime":
        mount.body[0].value.args[0].keywords[2].value = ast.parse("Runtime()", mode="eval").body
    elif mutation == "duplicate-mount":
        factory.body.insert(factory.body.index(mount), deepcopy(mount))
    elif mutation == "unconditional-mount":
        factory.body[factory.body.index(mount)] = mount.body[0]
    elif mutation == "wrong-default":
        factory.args.kw_defaults[1] = ast.Constant(value=False)
    elif mutation == "extra-keyword":
        factory.args.kwarg = ast.arg(arg="kwargs")
    elif mutation == "private-field":
        mount.body[0].value.args[0].keywords[0].value = ast.parse(
            "platform.application_facade._registration", mode="eval",
        ).body
    elif mutation == "platform-validation":
        factory.body[1].test = ast.Constant(value=False)
    elif mutation == "metadata":
        constructor = next(node.value for node in factory.body if isinstance(node, ast.Assign))
        constructor.keywords[0].value = ast.Constant(value="Another platform")
    with pytest.raises(AssertionError):
        _verify_host_delta(ast.unparse(ast.fix_missing_locations(tree)))


def _bindings(tree):
    result = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                result[item.asname or item.name] = item.name
        elif isinstance(node, ast.ImportFrom):
            for item in node.names:
                result[item.asname or item.name] = node.module + "." + item.name
    return result


def _name(node, bindings):
    if isinstance(node, ast.Name):
        return bindings.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        return _name(node.value, bindings) + "." + node.attr
    return "<dynamic>"


def test_router_imports_only_transport_canonical_values_and_the_two_use_cases():
    tree = ast.parse(ROUTER.read_text(encoding="utf-8"))
    standard = {"__future__", "json", "re", "hashlib", "io", "uuid", "typing", "dataclasses",
                "email.message", "collections.abc"}
    application = {
        "fastapi": {"APIRouter", "HTTPException", "Request", "Response", "status"},
        "pydantic": {"BaseModel", "ConfigDict", "StrictStr", "ValidationError", "field_validator"},
        "starlette.concurrency": {"run_in_threadpool"},
        "app.core.runtime": {"Runtime"},
        "app.domain.base": {"DomainException", "EntityId"},
        "app.domain.document": {"DocumentType", "DocumentSourceType", "DocumentSource", "EnterpriseDocument"},
        "app.domain.document_content": {"DocumentContentDescriptor", "DocumentContentDigest", "DocumentContentMediaType"},
        "app.document.repository": {"EnterpriseDocumentAlreadyExistsError"},
        "app.services.enterprise_document_registration_application_service": {
            "EnterpriseDocumentRegistrationApplicationService", "EnterpriseDocumentRegistrationRequest",
        },
        "app.services.document_content_establishment_application_service": {
            "DocumentContentEstablishmentApplicationService", "DocumentContentEstablishmentRequest",
            "DocumentContentEstablishmentDocumentNotFoundError", "DocumentContentEstablishmentConflictError",
            "DocumentContentEstablishmentIntegrityError",
        },
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            assert node in tree.body and all(item.name in standard for item in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node in tree.body and node.level == 0
            assert all(item.name != "*" for item in node.names)
            if node.module not in standard:
                assert node.module in application
                assert {item.name for item in node.names} <= application[node.module]
    imported = set(_bindings(tree).values())
    assert "starlette.concurrency.run_in_threadpool" in imported
    assert "app.services.enterprise_document_registration_application_service.EnterpriseDocumentRegistrationApplicationService" in imported
    assert "app.services.document_content_establishment_application_service.DocumentContentEstablishmentApplicationService" in imported


def test_router_has_only_one_required_keyword_only_public_factory():
    tree = ast.parse(ROUTER.read_text(encoding="utf-8"))
    public = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
              and not node.name.startswith("_")]
    assert len(public) == 1 and isinstance(public[0], ast.FunctionDef)
    factory = public[0]
    assert factory.name == "create_router" and not factory.decorator_list
    arguments = factory.args
    assert not arguments.posonlyargs and not arguments.args and not arguments.defaults
    assert arguments.vararg is None and arguments.kwarg is None
    assert [item.arg for item in arguments.kwonlyargs] == [
        "document_registration_service", "document_content_establishment_service", "runtime",
    ]
    assert arguments.kw_defaults == [None, None, None]
    bindings = _bindings(tree)
    assert [_name(item.annotation, bindings) for item in arguments.kwonlyargs] == [
        "app.services.enterprise_document_registration_application_service.EnterpriseDocumentRegistrationApplicationService",
        "app.services.document_content_establishment_application_service.DocumentContentEstablishmentApplicationService",
        "app.core.runtime.Runtime",
    ]
    assert _name(factory.returns, bindings) == "fastapi.APIRouter"


def test_router_does_not_own_infrastructure_or_mutate_runtime_or_chain_operations():
    tree = ast.parse(ROUTER.read_text(encoding="utf-8"))
    bindings = _bindings(tree)
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    forbidden_names = {
        "open", "eval", "exec", "__import__", "getattr", "setattr", "delattr", "compile",
        "app.core.runtime.Runtime", "app.domain.base.EntityId.new",
        "app.domain.document.EnterpriseDocument", "app.domain.document_content.DocumentContentDescriptor",
        "app.services.enterprise_document_registration_application_service.EnterpriseDocumentRegistrationApplicationService",
        "app.services.document_content_establishment_application_service.DocumentContentEstablishmentApplicationService",
    }
    assert not any(_name(node.func, bindings) in forbidden_names for node in calls)
    forbidden_methods = {
        "ingest", "ingest_document_knowledge", "request_operational", "analyze", "parse", "build",
        "enable_request_admission", "disable_request_admission", "startup", "shutdown", "dispose",
        "commit", "rollback", "begin", "connect", "execute", "add", "unlink", "mkdir", "rmdir",
        "rename", "replace", "remove", "write_bytes", "write_text", "read_bytes", "read_text",
        "body", "json", "form", "getenv", "import_module",
    }
    assert not any(isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_methods for node in calls)
    assert not any(isinstance(node, ast.Attribute) and node.attr.startswith("_")
                   and not (_name(node, bindings) == "int.__int__"
                            and any(call.func is node and len(call.args) == 1 and not call.keywords
                                    for call in calls)) for node in ast.walk(tree))
    assert not any(isinstance(node, (ast.Global, ast.Nonlocal, ast.Delete)) for node in ast.walk(tree))
    assert not any(isinstance(node, ast.ExceptHandler) and (
        node.type is None or any(isinstance(part, ast.Name) and part.id == "BaseException"
                                 for part in ast.walk(node.type))
    ) for node in ast.walk(tree))
    delegated = [node for node in calls if isinstance(node.func, ast.Attribute)
                 and node.func.attr in {"register", "establish"}]
    assert [node.func.attr for node in delegated].count("register") == 1
    assert [node.func.attr for node in delegated].count("establish") == 1
    owners = []
    for node in delegated:
        functions = [function for function in tree.body if isinstance(function, ast.FunctionDef)
                     and node in ast.walk(function)]
        assert len(functions) == 1 and functions[0].name.startswith("_")
        owners.append(functions[0])
        assert not any(isinstance(part, (ast.For, ast.While, ast.AsyncFor)) for part in ast.walk(functions[0]))
    assert owners[0] is not owners[1]
    assert sum(_name(node.func, bindings) == "starlette.concurrency.run_in_threadpool" for node in calls) == 2
    assert any(isinstance(node, ast.AsyncFor) for node in ast.walk(tree))


def test_preparation_is_mounted_only_by_the_explicit_host():
    for path in (ROOT / "backend/app").rglob("*.py"):
        if path in {HOST, ROUTER}:
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                assert not any("document_preparation" in item.name for item in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert "document_preparation" not in (node.module or "")
                assert not any(item.name == "document_preparation" for item in node.names)
    source = ast.parse(ROUTER.read_text(encoding="utf-8"))
    assert not any(isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) for node in source.body)


@pytest.mark.parametrize("relative", tuple(PRESERVED))
def test_other_services_ports_domains_tests_and_guards_remain_byte_exact(relative):
    assert sha256((ROOT / relative).read_bytes()).hexdigest() == PRESERVED[relative]


# BEGIN AD-070 A1 compatibility cases
# AD-070 A1 compatibility fixtures are parsed as data; they import no application.
_APPROVED_HOST_SOURCE = '''"""Explicit opt-in HTTP host for a caller-built PlantMind platform (AD-069)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.document_knowledge_ingestion import (
    create_router as create_document_knowledge_ingestion_router,
)
from app.api.operational_transition import (
    create_router as create_operational_transition_router,
)
from app.api.request_admission import RequestAdmissionMiddleware
from app.config import settings
from app.core.composition import PlatformComposition
from app.schemas.platform import PlatformInfo, PlatformStatus, RuntimeInfo


def create_app(*, platform: PlatformComposition) -> FastAPI:
    """Host this platform; the caller dedicates it to one active lifespan."""
    if not isinstance(platform, PlatformComposition):
        raise TypeError("platform must be a PlatformComposition.")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        platform.bootstrap.startup()
        try:
            yield
        finally:
            platform.bootstrap.shutdown()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Enterprise Operational Intelligence Platform",
        version=settings.VERSION,
        lifespan=lifespan,
    )
    app.add_middleware(RequestAdmissionMiddleware, runtime=platform.runtime)
    app.include_router(
        create_operational_transition_router(
            platform.operational_transition_application_service
        )
    )
    app.include_router(
        create_document_knowledge_ingestion_router(
            facade=platform.application_facade,
            runtime=platform.runtime,
        )
    )

    @app.get("/", response_model=PlatformStatus)
    def root() -> PlatformStatus:
        return PlatformStatus(
            platform=PlatformInfo(
                name=settings.APP_NAME,
                edition="Enterprise",
                deployment=settings.DEPLOYMENT_MODE,
                version=settings.VERSION,
            ),
            runtime=RuntimeInfo(
                status=platform.runtime.state.value,
                environment=platform.runtime.environment,
            ),
        )

    @app.get("/health")
    def health():
        return platform.health.get_status()

    return app
'''
_APPROVED_HOST_SOURCE_SHA256 = "8bff3d357523e4ae56943992da6d109167c0ef8e43322270b92b071b0efa259d"
_LEGACY_HOST_AST_SHA256 = "30f76d9ec9b4c54ba2af7a55bb7a491b5940df8614d8dbdadcb1a2bcc40c30a1"


def _host_ast_state(value):
    if isinstance(value, ast.AST):
        return (type(value).__name__, tuple(value._fields),
                tuple((name, _host_ast_state(item)) for name, item in sorted(vars(value).items())))
    if isinstance(value, (list, tuple)):
        return (type(value).__name__, tuple(_host_ast_state(item) for item in value))
    if isinstance(value, dict):
        return ("dict", tuple((name, _host_ast_state(item)) for name, item in sorted(value.items())))
    return value


def _host_schema_state():
    return tuple((name, tuple(getattr(ast, name)._fields)) for name in sorted(HOST_AST_FIELDS))


def _complete_native_ast_dump(tree):
    options = {"include_attributes": False}
    if "show_empty" in inspect.signature(ast.dump).parameters:
        options["show_empty"] = True
    return ast.dump(tree, **options)


def _normalization_preserves_input_and_global_schemas(tree):
    before, schemas = _host_ast_state(tree), _host_schema_state()
    result = normalized_host_dump(tree)
    assert _host_ast_state(tree) == before
    assert _host_schema_state() == schemas
    return result


def _normalization_rejects_without_mutation(tree, message):
    before, schemas = _host_ast_state(tree), _host_schema_state()
    with pytest.raises(AssertionError, match=message):
        normalized_host_dump(tree)
    assert _host_ast_state(tree) == before
    assert _host_schema_state() == schemas


def _model_function_schema(patch, tree, *, legacy):
    """An explicit representation model, never a claim to run another Python."""
    for name in ("FunctionDef", "AsyncFunctionDef"):
        fields = HOST_AST_FIELDS[name]
        patch.setattr(getattr(ast, name), "_fields", fields[:-1] if legacy else fields)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if legacy and "type_params" in vars(node):
                del node.type_params
            elif not legacy and "type_params" not in vars(node):
                node.type_params = []


def test_a1_native_host_normalization_has_the_immutable_fingerprint():
    assert sha256(_APPROVED_HOST_SOURCE.encode()).hexdigest() == _APPROVED_HOST_SOURCE_SHA256
    parsed = ast.parse(_APPROVED_HOST_SOURCE)
    result = _normalization_preserves_input_and_global_schemas(parsed)
    assert sha256(result.encode()).hexdigest() == ORIGINAL_HOST_AST_SHA256
    assert len(result.encode()) == 6120
    assert result.count("type_params=[]") == 4
    assert "type_ignores=[]" in result


def test_a1_explicit_legacy_model_reproduces_captured_mac_data_and_frozen_digest(monkeypatch):
    tree = ast.parse(_APPROVED_HOST_SOURCE)
    expected = _normalization_preserves_input_and_global_schemas(tree)
    schemas = _host_schema_state()
    with monkeypatch.context() as patch:
        _model_function_schema(patch, tree, legacy=True)
        before = _complete_native_ast_dump(tree)
        assert sha256(before.encode()).hexdigest() == _LEGACY_HOST_AST_SHA256
        assert len(before.encode()) == 6056
        assert "type_params" not in before
        result = _normalization_preserves_input_and_global_schemas(tree)
        assert result == expected
        assert sha256(result.encode()).hexdigest() == ORIGINAL_HOST_AST_SHA256
        assert len(result.encode()) == 6120
        assert all("type_params" not in vars(node) and "type_params" not in node._fields
                   for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("source", [
    "class NewOwner:\n    pass\n",
    "def extension():\n    pass\n",
    "while True:\n    break\n",
])
def test_a1_unknown_node_classes_are_rejected(source):
    _normalization_rejects_without_mutation(ast.parse(source), "Unsupported host AST node")


@pytest.mark.parametrize("value", [None, [], {}], ids=["none", "empty-list", "empty-dict"])
def test_a1_unknown_instance_attributes_are_rejected_even_when_empty(value):
    tree = ast.parse(_APPROVED_HOST_SOURCE)
    tree.unrecognized_semantic_field = value
    _normalization_rejects_without_mutation(tree, "Unexpected host AST instance attribute")


@pytest.mark.parametrize("change", ["added-none", "added-empty", "missing", "reordered"])
def test_a1_unknown_missing_and_reordered_schema_fields_are_rejected(monkeypatch, change):
    tree = ast.parse(_APPROVED_HOST_SOURCE)
    schemas = _host_schema_state()
    fields = HOST_AST_FIELDS["Module"]
    if change.startswith("added-"):
        fields = fields + ("unrecognized_semantic_field",)
        tree.unrecognized_semantic_field = None if change == "added-none" else []
    elif change == "missing":
        fields = fields[:-1]
    else:
        fields = tuple(reversed(fields))
    with monkeypatch.context() as patch:
        patch.setattr(ast.Module, "_fields", fields)
        _normalization_rejects_without_mutation(tree, "Unsupported host AST field schema")
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("asynchronous", [False, True], ids=["function", "async-function"])
def test_a1_legacy_exception_cannot_hide_another_missing_function_field(monkeypatch, asynchronous):
    tree = ast.parse(("async " if asynchronous else "") + "def example():\n    return None\n")
    schemas = _host_schema_state()
    function = tree.body[0]
    name = type(function).__name__
    fields = tuple(field for field in HOST_AST_FIELDS[name] if field != "returns")
    with monkeypatch.context() as patch:
        patch.setattr(type(function), "_fields", fields)
        _normalization_rejects_without_mutation(tree, "Unsupported host AST field schema")
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("asynchronous", [False, True], ids=["function", "async-function"])
def test_a1_full_schema_requires_an_existing_type_parameter_list(monkeypatch, asynchronous):
    tree = ast.parse(("async " if asynchronous else "") + "def example():\n    return None\n")
    schemas = _host_schema_state()
    with monkeypatch.context() as patch:
        _model_function_schema(patch, tree, legacy=False)
        del tree.body[0].type_params
        _normalization_rejects_without_mutation(tree, "Host AST type_params must be a list")
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("missing", ["module-type-ignores", "call-keywords", "argument-defaults"])
def test_a1_copy_cannot_repair_other_missing_fields_to_the_approved_fingerprint(missing):
    tree = ast.parse(_APPROVED_HOST_SOURCE)
    if missing == "module-type-ignores":
        owner, field = tree, "type_ignores"
    elif missing == "call-keywords":
        owner = next(node for node in ast.walk(tree) if isinstance(node, ast.Call) and node.keywords == [])
        field = "keywords"
    else:
        owner = next(node for node in ast.walk(tree) if isinstance(node, ast.arguments) and node.defaults == [])
        field = "defaults"
    delattr(owner, field)
    before, schemas = _host_ast_state(tree), _host_schema_state()
    try:
        result = normalized_host_dump(tree)
    except AssertionError as error:
        assert "AST copy synthesized or removed input attributes" in str(error)
    else:
        # Older constructors retain the absence; its different dump must fail
        # the immutable digest instead of acquiring a synthesized empty list.
        assert sha256(result.encode()).hexdigest() != ORIGINAL_HOST_AST_SHA256
    assert _host_ast_state(tree) == before
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("legacy", [False, True], ids=["full-schema-model", "legacy-schema-model"])
@pytest.mark.parametrize("value", [None, (), "T"], ids=["none", "tuple", "string"])
def test_a1_type_parameters_are_lists_in_both_supported_schemas(monkeypatch, legacy, value):
    tree = ast.parse(_APPROVED_HOST_SOURCE)
    schemas = _host_schema_state()
    with monkeypatch.context() as patch:
        _model_function_schema(patch, tree, legacy=legacy)
        tree.body[-1].type_params = value
        _normalization_rejects_without_mutation(tree, "Host AST type_params must be a list")
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("legacy", [False, True], ids=["full-schema-model", "legacy-schema-model"])
def test_a1_nonempty_type_parameters_are_retained_and_fail_the_fixed_fingerprint(monkeypatch, legacy):
    tree = ast.parse(_APPROVED_HOST_SOURCE)
    schemas = _host_schema_state()
    with monkeypatch.context() as patch:
        _model_function_schema(patch, tree, legacy=legacy)
        tree.body[-1].type_params = [ast.Name(id="T", ctx=ast.Load())]
        result = _normalization_preserves_input_and_global_schemas(tree)
        assert "type_params=[Name(id='T', ctx=Load())]" in result
        assert sha256(result.encode()).hexdigest() != ORIGINAL_HOST_AST_SHA256
        assert tree.body[-1].type_params[0].id == "T"
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("legacy", [False, True], ids=["full-schema-model", "legacy-schema-model"])
def test_a1_preserved_type_parameter_children_must_obey_the_closed_schema(monkeypatch, legacy):
    tree = ast.parse(_APPROVED_HOST_SOURCE)
    schemas = _host_schema_state()
    with monkeypatch.context() as patch:
        _model_function_schema(patch, tree, legacy=legacy)
        tree.body[-1].type_params = [ast.Pass()]
        _normalization_rejects_without_mutation(tree, "Unsupported host AST node")
    assert _host_schema_state() == schemas


@pytest.mark.parametrize("legacy", [False, True], ids=["full-schema-model", "legacy-schema-model"])
def test_a1_none_values_and_empty_lists_keep_their_native_semantics(monkeypatch, legacy):
    tree = ast.parse("def accepts(*, required, optional=None):\n    return None\n")
    schemas = _host_schema_state()
    expected = (
        "Module(body=[FunctionDef(name='accepts', args=arguments(posonlyargs=[], args=[], "
        "kwonlyargs=[arg(arg='required'), arg(arg='optional')], "
        "kw_defaults=[None, Constant(value=None)], defaults=[]), "
        "body=[Return(value=Constant(value=None))], decorator_list=[], type_params=[])], type_ignores=[])"
    )
    with monkeypatch.context() as patch:
        _model_function_schema(patch, tree, legacy=legacy)
        assert _normalization_preserves_input_and_global_schemas(tree) == expected
    assert _host_schema_state() == schemas
# END AD-070 A1 compatibility cases
