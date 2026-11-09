"""RFC-081 transport ownership and exact predecessor guard exception."""
import ast
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "backend/app/api/document_knowledge_ingestion.py"
GUARD = ROOT / "tests/services/test_parsed_document_knowledge_ingestion_architecture.py"


def test_api_module_exists():
    assert TARGET.is_file()


def test_explicit_imports_have_no_service_or_infrastructure_owner():
    tree = ast.parse(TARGET.read_text(encoding="utf-8"))
    imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert not any(isinstance(n, ast.Import) for n in ast.walk(tree))
    assert {n.module for n in imports} == {
        "__future__", "typing", "uuid", "fastapi", "pydantic",
        "app.core.runtime", "app.domain.base", "app.document_parsing.parser",
        "app.knowledge_lineage_transaction.coordinator", "app.services.application_facade",
        "app.services.document_content_access_application_service",
        "app.services.document_knowledge_ingestion_application_service",
        "app.services.knowledge_capture_application_service",
        "app.services.parsed_document_knowledge_ingestion_application_service",
    }
    assert all(n.level == 0 and all(a.asname is None and a.name != "*" for a in n.names) for n in imports)
    for node in imports:
        for alias in node.names:
            if node.module.startswith("app."):
                assert not alias.name.endswith("ApplicationService")
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id in {"Runtime", "ApplicationFacade", "create_engine", "sessionmaker",
                       "__import__", "eval", "exec"} for n in ast.walk(tree))


def test_one_facade_call_no_direct_ingestion_and_no_runtime_mutation():
    tree = ast.parse(TARGET.read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    delegated = [n for n in calls if isinstance(n.func, ast.Attribute)
                 and n.func.attr == "ingest_document_knowledge"]
    assert len(delegated) == 1 and ast.unparse(delegated[0].func.value) == "facade"
    forbidden = {"ingest", "analyze", "execute", "commit", "rollback", "request_operational",
                 "enable_request_admission", "disable_request_admission", "import_module"}
    assert not any(isinstance(n.func, ast.Attribute) and n.func.attr in forbidden for n in calls)
    catches = [n for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler)]
    assert len(catches) == 1 and ast.unparse(catches[0].type) == "Exception"
    factory = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "create_router")
    assert not factory.args.args and [a.arg for a in factory.args.kwonlyargs] == ["facade", "runtime"]
    assert factory.args.kw_defaults == [None, None]


def test_no_default_registration_or_import_time_service_graph():
    tree = ast.parse(TARGET.read_text(encoding="utf-8"))
    assert not any(isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) for n in tree.body)
    assignments = [n for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign))]
    assert len(assignments) == 1 and ast.unparse(assignments[0].targets[0]) == "NonblankText"
    files = list((ROOT / "backend/app/core").rglob("*.py"))
    files += [ROOT / "backend/app/main.py", ROOT / "backend/app/api/__init__.py"]
    for path in files:
        if path.is_file():
            assert "app.api.document_knowledge_ingestion" not in path.read_text(encoding="utf-8")
    from app.main import app
    assert "/documents/{document_id}/knowledge" not in app.openapi()["paths"]


@pytest.mark.parametrize("form", ["valid", "alias", "star", "service", "module",
    "relative", "dynamic", "reexport", "syntax"])
def test_guard_exception_does_not_become_an_open_import_permission(form):
    spec = importlib.util.spec_from_file_location("_rfc081_guard_review", GUARD)
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    module = "app.services.parsed_document_knowledge_ingestion_application_service"
    request = "ParsedDocumentKnowledgeIngestionRequest"
    forms = {
        "valid": f"from {module} import {request}\n",
        "alias": f"from {module} import {request} as Hidden\n",
        "star": f"from {module} import *\n",
        "service": f"from {module} import ParsedDocumentKnowledgeIngestionApplicationService\n",
        "module": f"import {module}\n",
        "relative": f"from .{module} import {request}\n",
        "dynamic": f"__import__({module!r})\n",
        "reexport": f"from {module} import {request}\nExport = {request}\n",
        "syntax": f"from {module} import (\n",
    }
    assert guard._rfc081_request_import_allowed(forms[form]) is (form == "valid")
