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


def _rfc081_request_import_allowed(source):
    """Only one unaliased request-type import in the governed transport file."""
    marker = "app.services.parsed_document_knowledge_ingestion_application_service"
    forbidden = "ParsedDocumentKnowledgeIngestionApplicationService"
    if source.count(marker) != 1 or forbidden in source:
        return False
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module == marker]
    if len(imports) != 1 or imports[0].level != 0:
        return False
    if [(n.name, n.asname) for n in imports[0].names] != [
        ("ParsedDocumentKnowledgeIngestionRequest", None)
    ]:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"__import__", "eval", "exec"}:
                return False
            if isinstance(node.func, ast.Attribute) and node.func.attr == "import_module":
                return False
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(node.value, ast.Name):
            if node.value.id == "ParsedDocumentKnowledgeIngestionRequest":
                return False
    return True


def _rfc082_composition_import_allowed(source):
    """Allow only the AD-068 injection delta in the exact composition-root file."""
    import hashlib
    import json

    def shape(value):
        if isinstance(value, ast.AST):
            return [type(value).__name__, [[name, shape(item)]
                for name, item in ast.iter_fields(value)
                if not (name == "type_params" and item == [])]]
        if isinstance(value, list):
            return [shape(item) for item in value]
        return value

    marker = "app.services.parsed_document_knowledge_ingestion_application_service"
    service = "ParsedDocumentKnowledgeIngestionApplicationService"
    dependency = "parsed_document_knowledge_ingestion_service"
    try:
        tree = ast.parse(source)
    except (SyntaxError, TypeError, ValueError):
        return False
    imports = [node for node in ast.walk(tree)
               if isinstance(node, ast.ImportFrom) and node.module == marker]
    if len(imports) != 1 or imports[0] not in tree.body or imports[0].level != 0:
        return False
    if [(item.name, item.asname) for item in imports[0].names] != [(service, None)]:
        return False
    roots = [node for node in tree.body
             if isinstance(node, ast.ClassDef) and node.name == "CompositionRoot"]
    wrappers = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == "build_platform_composition"]
    if len(roots) != 1 or len(wrappers) != 1:
        return False
    builds = [node for node in roots[0].body
              if isinstance(node, ast.FunctionDef) and node.name == "build"]
    if len(builds) != 1:
        return False
    build, wrapper = builds[0], wrappers[0]
    annotation = ast.parse(service + " | None", mode="eval").body
    for factory in (build, wrapper):
        args = factory.args
        if len(args.kwonlyargs) != 1 or len(args.kw_defaults) != 1:
            return False
        if args.kwonlyargs[0].arg != dependency or shape(args.kwonlyargs[0].annotation) != shape(annotation):
            return False
        default = args.kw_defaults[0]
        if not isinstance(default, ast.Constant) or default.value is not None:
            return False
    validation = ast.parse(
        "if parsed_document_knowledge_ingestion_service is not None and not isinstance("
        "parsed_document_knowledge_ingestion_service, ParsedDocumentKnowledgeIngestionApplicationService):\n"
        "    raise TypeError('parsed_document_knowledge_ingestion_service must be a "
        "ParsedDocumentKnowledgeIngestionApplicationService or None.')\n"
    ).body[0]
    if not build.body or shape(build.body[0]) != shape(validation):
        return False
    facade_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name) and node.func.id == "ApplicationFacade"]
    wrapper_calls = [node for node in ast.walk(wrapper) if isinstance(node, ast.Call)
                     and isinstance(node.func, ast.Attribute) and node.func.attr == "build"
                     and isinstance(node.func.value, ast.Name) and node.func.value.id == "CompositionRoot"]
    if len(facade_calls) != 1 or len(wrapper_calls) != 1:
        return False
    for call in (facade_calls[0], wrapper_calls[0]):
        forwards = [item for item in call.keywords if item.arg == dependency]
        if len(forwards) != 1 or not isinstance(forwards[0].value, ast.Name):
            return False
        if forwards[0].value.id != dependency or forwards[0] is not call.keywords[-1]:
            return False
        call.keywords.remove(forwards[0])
    tree.body.remove(imports[0])
    for factory in (build, wrapper):
        factory.args.kwonlyargs = []
        factory.args.kw_defaults = []
    del build.body[0]
    # Empty type_params exists in Python 3.12+, but not in the accepted 3.11 baseline.
    # A nonempty type parameter list is retained, so it cannot hide a graph change.
    projected = json.dumps(shape(tree), ensure_ascii=True, separators=(",", ":")).encode()
    return hashlib.sha256(projected).hexdigest() == "cd421593677695d93f0066e47b120c68d3ea0a0d70b95cc5ef7143a3af39d9f2"


def test_default_host_does_not_import_new_boundary():
    paths = list((ROOT / "backend/app/core").rglob("*.py"))
    paths += list((ROOT / "backend/app/api").rglob("*.py"))
    paths += [ROOT / "backend/app/main.py"]
    allowed = ROOT / "backend/app/api/document_knowledge_ingestion.py"
    allowed_composition = ROOT / "backend/app/core/composition/composition_root.py"
    for path in paths:
        if path.is_file():
            content = path.read_text(encoding="utf-8")
            if path == allowed:
                assert _rfc081_request_import_allowed(content)
            elif path == allowed_composition:
                assert _rfc082_composition_import_allowed(content)
            else:
                assert "parsed_document_knowledge_ingestion_application_service" not in content
                assert "ParsedDocumentKnowledgeIngestionApplicationService" not in content
