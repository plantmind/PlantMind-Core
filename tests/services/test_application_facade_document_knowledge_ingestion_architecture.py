"""RFC-080 exact ownership and unchanged analysis/default composition."""
import ast
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "backend/app/services/application_facade.py"


def nodes():
    source = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(source)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ApplicationFacade")
    methods = {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}
    return source, tree, methods


def test_analyze_source_is_unchanged():
    source, _, methods = nodes()
    assert sha256(ast.get_source_segment(source, methods["analyze"]).encode()).hexdigest() == "1ea867de057a385b06188143747ca51e857d355031f6ebb9615c76177d0f5ad4"


def test_explicit_imports_and_no_import_time_graph():
    _, tree, methods = nodes()
    assert set(methods) == {"__init__", "analyze", "ingest_document_knowledge"}
    assert all(isinstance(n, (ast.ImportFrom, ast.ClassDef)) or
        (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str))
        for n in tree.body)
    assert {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} == {
        "__future__", "uuid", "app.domain.observation", "app.domain.operational_workload_evidence",
        "app.services.integration_gateway", "app.services.orchestration.workflow",
        "app.services.parsed_document_knowledge_ingestion_application_service",
        "app.services.document_knowledge_ingestion_application_service",
    }
    assert [n.name for n in tree.body if isinstance(n, ast.ClassDef)] == [
        "ApplicationFacadeDocumentIngestionNotConfiguredError", "ApplicationFacade"]


def test_constructor_preserves_gateway_and_only_stores_dependency():
    _, _, methods = nodes()
    body = methods["__init__"].body
    assert len(body) == 2 and all(isinstance(n, ast.Assign) for n in body)
    assert ast.unparse(body[0]) == "self._gateway = gateway or IntegrationGateway()"
    assert ast.unparse(body[1]) == (
        "self._parsed_document_knowledge_ingestion_service = parsed_document_knowledge_ingestion_service")


def test_new_command_only_checks_none_then_delegates():
    _, _, methods = nodes()
    method = methods["ingest_document_knowledge"]
    body = [n for n in method.body if not isinstance(n, ast.Expr)]
    assert len(body) == 2 and isinstance(body[0], ast.If) and isinstance(body[1], ast.Return)
    check = body[0]
    assert ast.unparse(check.test) == "self._parsed_document_knowledge_ingestion_service is None"
    assert not check.orelse and len(check.body) == 1 and isinstance(check.body[0], ast.Raise)
    assert ast.unparse(body[1].value) == "self._parsed_document_knowledge_ingestion_service.ingest(request)"
    calls = [n for n in ast.walk(method) if isinstance(n, ast.Call)]
    assert len(calls) == 2
    assert {ast.unparse(n.func) for n in calls} == {
        "ApplicationFacadeDocumentIngestionNotConfiguredError",
        "self._parsed_document_knowledge_ingestion_service.ingest"}
    assert not any(isinstance(n, (ast.Try, ast.With, ast.For, ast.While, ast.AsyncFunctionDef))
                   for n in ast.walk(method))


def test_default_composition_still_supplies_only_gateway():
    path = ROOT / "backend/app/core/composition/composition_root.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "ApplicationFacade"]
    assert len(calls) == 1 and not calls[0].args
    assert [(k.arg, ast.unparse(k.value)) for k in calls[0].keywords] == [
        ("gateway", "integration_gateway")]
