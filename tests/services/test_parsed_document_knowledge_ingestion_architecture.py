"""RFC-079 application dependency and default-host containment checks."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "backend/app/services/parsed_document_knowledge_ingestion_application_service.py"


def test_service_module_exists():
    assert TARGET.is_file()


def test_exact_application_imports():
    tree = ast.parse(TARGET.read_text(encoding="utf-8"))
    assert not any(isinstance(n, ast.Import) for n in ast.walk(tree))
    assert {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} == {
        "__future__", "dataclasses", "app.domain.base", "app.domain.document_content",
        "app.services.document_content_parsing_application_service",
        "app.services.document_knowledge_ingestion_application_service",
        "app.services.knowledge_capture_application_service",
    }


def test_no_module_graph_or_transaction_control():
    tree = ast.parse(TARGET.read_text(encoding="utf-8"))
    assert {n.name for n in tree.body if isinstance(n, ast.ClassDef)} == {
        "ParsedDocumentKnowledgeIngestionRequest", "ParsedDocumentKnowledgeIngestionApplicationService"}
    assert not any(isinstance(n, (ast.Assign, ast.AnnAssign, ast.FunctionDef)) for n in tree.body)
    assert not any(isinstance(n, (ast.Try, ast.With, ast.AsyncFunctionDef, ast.For, ast.While))
                   for n in ast.walk(tree))
    allowed = {"dataclass", "isinstance", "TypeError", "ValueError",
               "DocumentContentParsingRequest", "DocumentKnowledgeIngestionRequest"}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name):
                assert n.func.id in allowed
            else:
                assert isinstance(n.func, ast.Attribute)
                assert n.func.attr in {"parse", "ingest", "strip"}


def test_default_host_does_not_import_new_boundary():
    paths = list((ROOT / "backend/app/core").rglob("*.py"))
    paths += list((ROOT / "backend/app/api").rglob("*.py"))
    paths += [ROOT / "backend/app/main.py"]
    for path in paths:
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            assert "parsed_document_knowledge_ingestion_application_service" not in content
            assert "ParsedDocumentKnowledgeIngestionApplicationService" not in content
