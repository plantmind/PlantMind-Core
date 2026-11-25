"""RFC-082 bounded composition delta and predecessor-guard containment."""
import ast
from hashlib import sha256
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "backend/app/core/composition/composition_root.py"
GUARD79 = ROOT / "tests/services/test_parsed_document_knowledge_ingestion_architecture.py"
GUARD80 = ROOT / "tests/services/test_application_facade_document_knowledge_ingestion_architecture.py"
MODULE = "app.services.parsed_document_knowledge_ingestion_application_service"
SERVICE = "ParsedDocumentKnowledgeIngestionApplicationService"
DEPENDENCY = "parsed_document_knowledge_ingestion_service"
PRESERVED79 = {'test_service_module_exists': '2b5655494118261ad395ecb667534f0817e1baec3d6aac26440ecda93b1a2695', 'test_exact_application_imports': '8e9026ea3dcf5ab6862475af68046dd4645060e7032280e0fe838758c3fdf55d', 'test_no_module_graph_or_transaction_control': 'd2ee945b8fa08ea03d8431093ec3aed8dcd2ffde9dfe7b26b45aa7386873bda8', '_rfc081_request_import_allowed': 'b4c1d807d1035a1f453539a73705687f5b88f4195e6fb2a99b87d5bd9e5662e1'}
PRESERVED80 = {'nodes': '118c2616f9936116e8e751ef9daea1cc1b1778624f423d260f82c13878fc6bee', 'test_analyze_source_is_unchanged': 'c46a7d04e0ca11ce31b9ce7cad4cde16c71a8900c614da7fa0f606a1709b5c62', 'test_explicit_imports_and_no_import_time_graph': '948275f942028c131014458952417ffcd3d88baf85eb0fa1c11900fa8ac481a6', 'test_constructor_preserves_gateway_and_only_stores_dependency': '117486cddbaede76bf50e20f4c25cb65d7fc9eccc2176669690a83c0d0b5a6a7', 'test_new_command_only_checks_none_then_delegates': '183cf60618c66a4fe1bc01229ce28fe5aef8b4b4d35168c5c2eb85e1f36f1711'}
API_BRANCH = '            if path == allowed:\n                assert _rfc081_request_import_allowed(content)\n'


@pytest.fixture
def guard79():
    spec = importlib.util.spec_from_file_location("_rfc082_architecture_guard", GUARD79)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_root_contains_only_the_accepted_graph_delta(guard79):
    source = TARGET.read_text(encoding="utf-8")
    assert guard79._rfc082_composition_import_allowed(source)
    assert guard79._rfc082_composition_import_allowed(ast.unparse(ast.parse(source)) + "\n")


def test_other_predecessor_functions_and_api_exception_are_byte_preserved():
    for path, expected, mutable in (
        (GUARD79, PRESERVED79, {"test_default_host_does_not_import_new_boundary", "_rfc082_composition_import_allowed"}),
        (GUARD80, PRESERVED80, {"test_default_composition_has_explicit_optional_ingestion_input"}),
    ):
        source = path.read_text(encoding="utf-8")
        functions = {n.name: n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
        assert set(functions) == set(expected) | mutable
        for name, digest in expected.items():
            assert sha256(ast.get_source_segment(source, functions[name]).encode()).hexdigest() == digest
    source = GUARD79.read_text(encoding="utf-8")
    function = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)
                    and n.name == "test_default_host_does_not_import_new_boundary")
    branches = [n for n in ast.walk(function) if isinstance(n, ast.If)
                and ast.unparse(n.test) == "path == allowed"]
    assert len(branches) == 1
    lines = source.splitlines(keepends=True)
    branch = "".join(lines[branches[0].lineno - 1:branches[0].body[-1].end_lineno])
    assert branch == API_BRANCH


@pytest.mark.parametrize("wrong_path", [
    "backend/app/core/composition/other.py", "backend/app/core/other.py",
    "backend/app/api/other.py", "backend/app/main.py",
])
def test_service_exception_does_not_extend_to_another_file(guard79, monkeypatch, tmp_path, wrong_path):
    source = TARGET.read_text(encoding="utf-8")
    allowed = tmp_path / "backend/app/core/composition/composition_root.py"
    allowed.parent.mkdir(parents=True)
    allowed.write_text(source, encoding="utf-8")
    api = tmp_path / "backend/app/api/document_knowledge_ingestion.py"
    api.parent.mkdir(parents=True)
    api.write_text(
        f"from {MODULE} import ParsedDocumentKnowledgeIngestionRequest\n", encoding="utf-8")
    monkeypatch.setattr(guard79, "ROOT", tmp_path)
    guard79.test_default_host_does_not_import_new_boundary()
    forbidden = tmp_path / wrong_path
    forbidden.parent.mkdir(parents=True, exist_ok=True)
    forbidden.write_text(source, encoding="utf-8")
    with pytest.raises(AssertionError):
        guard79.test_default_host_does_not_import_new_boundary()


def mutated_root(source, scenario):
    if scenario == "syntax":
        return source + "\ndef broken(\n"
    tree = ast.parse(source)
    imported = next(n for n in tree.body if isinstance(n, ast.ImportFrom) and n.module == MODULE)
    root = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "CompositionRoot")
    build = next(n for n in root.body if isinstance(n, ast.FunctionDef) and n.name == "build")
    wrapper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "build_platform_composition")
    facade = next(n for n in ast.walk(build) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Name) and n.func.id == "ApplicationFacade")
    forwarded = next(n for n in ast.walk(wrapper) if isinstance(n, ast.Call)
                     and ast.unparse(n.func) == "CompositionRoot.build")
    if scenario == "alias":
        imported.names[0].asname = "HiddenService"
    elif scenario == "star":
        imported.names = [ast.alias(name="*")]
    elif scenario == "module_import":
        tree.body[tree.body.index(imported)] = ast.Import(names=[ast.alias(name=MODULE)])
    elif scenario == "relative":
        imported.level = 1
    elif scenario == "extra_symbol":
        imported.names.append(ast.alias(name="ParsedDocumentKnowledgeIngestionRequest"))
    elif scenario == "extra_import":
        tree.body.insert(1, ast.parse("from app.infrastructure.database.runtime import DatabaseRuntime").body[0])
    elif scenario in {"service_construct", "ingest", "registration", "dynamic", "dynamic_attribute", "extra_service_use"}:
        statements = {
            "service_construct": f"{SERVICE}(parsing_service=None, ingestion_service=None)",
            "ingest": f"{DEPENDENCY}.ingest(None)",
            "registration": f"container.register_instance({SERVICE}, {DEPENDENCY})",
            "dynamic": '__import__("app.services." + "parsed_document_knowledge_ingestion_application_service")',
            "dynamic_attribute": f'getattr({DEPENDENCY}, "ingest")(None)',
            "extra_service_use": f"hidden = {DEPENDENCY}",
        }
        build.body.insert(2, ast.parse(statements[scenario]).body[0])
    elif scenario == "reexport":
        tree.body.append(ast.parse(f"ExportedService = {SERVICE}").body[0])
    elif scenario == "late_validation":
        build.body[0], build.body[1] = build.body[1], build.body[0]
    elif scenario == "truthiness_validation":
        build.body[0].test = ast.Name(id=DEPENDENCY, ctx=ast.Load())
    elif scenario == "drop_validation":
        del build.body[0]
    elif scenario == "wrong_type":
        call = next(n for n in ast.walk(build.body[0]) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Name) and n.func.id == "isinstance")
        call.args[1] = ast.Name(id="object", ctx=ast.Load())
    elif scenario in {"wrapper_fallback", "facade_fallback", "wrapper_drop", "facade_drop"}:
        call = forwarded if scenario.startswith("wrapper_") else facade
        keyword = next(k for k in call.keywords if k.arg == DEPENDENCY)
        if scenario.endswith("drop"):
            call.keywords.remove(keyword)
        else:
            keyword.value = ast.parse(DEPENDENCY + " or None", mode="eval").body
    elif scenario == "non_none_default":
        build.args.kw_defaults[0] = ast.Constant(value=False)
    elif scenario == "positional_dependency":
        build.args.args.append(build.args.kwonlyargs.pop())
        build.args.defaults.append(build.args.kw_defaults.pop())
    elif scenario == "runtime_admission":
        at = next(i for i, n in enumerate(build.body) if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "runtime" for t in n.targets))
        build.body.insert(at + 1, ast.parse("runtime.enable_request_admission()").body[0])
    elif scenario == "replace_facade":
        at = next(i for i, n in enumerate(build.body) if isinstance(n, ast.Assign) and n.value is facade)
        build.body.insert(at + 1, ast.parse("application_facade = ApplicationFacade(gateway=integration_gateway)").body[0])
    elif scenario == "changed_gateway":
        next(k for k in facade.keywords if k.arg == "gateway").value = ast.parse("IntegrationGateway()", mode="eval").body
    elif scenario == "shadow_isinstance":
        tree.body.append(ast.parse("isinstance = lambda *values: True").body[0])
    else:
        raise AssertionError("Unknown mutation scenario: " + scenario)
    return ast.unparse(ast.fix_missing_locations(tree)) + "\n"


@pytest.mark.parametrize("scenario", [
    "alias", "star", "module_import", "relative", "extra_symbol", "extra_import",
    "service_construct", "ingest", "registration", "reexport", "dynamic", "dynamic_attribute",
    "late_validation", "truthiness_validation", "drop_validation", "wrong_type",
    "wrapper_fallback", "facade_fallback", "wrapper_drop", "facade_drop",
    "non_none_default", "positional_dependency", "runtime_admission", "replace_facade",
    "extra_service_use", "changed_gateway", "shadow_isinstance", "syntax",
])
def test_guard_rejects_unauthorized_composition_forms(guard79, scenario):
    source = TARGET.read_text(encoding="utf-8")
    assert guard79._rfc082_composition_import_allowed(source)
    changed = mutated_root(source, scenario)
    assert changed != source
    if scenario != "syntax":
        assert ast.dump(ast.parse(changed)) != ast.dump(ast.parse(source))
    assert guard79._rfc082_composition_import_allowed(changed) is False
