"""RFC-066 canonical Document Content architecture guardrails."""

from __future__ import annotations

import ast
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTENT_MODULE = (
    REPOSITORY_ROOT
    / "backend/app/domain/document_content.py"
)

EXPECTED_CLASSES = {
    "DocumentContentMediaType",
    "DocumentContentDigest",
    "DocumentContentDescriptor",
}

EXPECTED_FIELDS = {
    "DocumentContentMediaType": {
        "value",
    },
    "DocumentContentDigest": {
        "value",
    },
    "DocumentContentDescriptor": {
        "document_id",
        "media_type",
        "byte_length",
        "digest",
    },
}

FORBIDDEN_IMPORT_PREFIXES = (
    "sqlalchemy",
    "fastapi",
    "pydantic",
    "app.domain.document",
    "app.document.repository",
    "app.services",
    "app.infrastructure",
)


def _content_tree() -> ast.Module:
    assert CONTENT_MODULE.is_file(), (
        "RFC-066 requires "
        "backend/app/domain/document_content.py"
    )

    return ast.parse(CONTENT_MODULE.read_text())


def _classes(tree: ast.Module) -> dict[str, ast.ClassDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }


def _annotated_fields(node: ast.ClassDef) -> set[str]:
    return {
        statement.target.id
        for statement in node.body
        if isinstance(statement, ast.AnnAssign)
        and isinstance(statement.target, ast.Name)
    }


def _imported_modules(tree: ast.Module) -> set[str]:
    modules: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(
                alias.name
                for alias in node.names
            )
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module
        ):
            modules.add(node.module)

    return modules


def _dataclass_options(node: ast.ClassDef) -> dict[str, object]:
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue

        if (
            isinstance(decorator.func, ast.Name)
            and decorator.func.id == "dataclass"
        ):
            return {
                keyword.arg: ast.literal_eval(keyword.value)
                for keyword in decorator.keywords
                if keyword.arg is not None
            }

    raise AssertionError(
        f"{node.name} must use @dataclass."
    )


def test_document_content_has_exact_canonical_class_surface() -> None:
    tree = _content_tree()
    classes = _classes(tree)

    assert set(classes) == EXPECTED_CLASSES

    source = CONTENT_MODULE.read_text()

    assert "DocumentContentId" not in source


def test_document_content_classes_have_exact_fields() -> None:
    classes = _classes(_content_tree())

    actual = {
        name: _annotated_fields(node)
        for name, node in classes.items()
    }

    assert actual == EXPECTED_FIELDS


def test_document_content_contracts_are_immutable_value_objects() -> None:
    classes = _classes(_content_tree())

    for node in classes.values():
        options = _dataclass_options(node)

        assert options.get("frozen") is True
        assert options.get("slots") is True
        assert options.get("kw_only") is True


def test_document_content_descriptor_is_not_domain_entity() -> None:
    descriptor = _classes(
        _content_tree()
    )["DocumentContentDescriptor"]

    base_names = {
        base.id
        for base in descriptor.bases
        if isinstance(base, ast.Name)
    }

    assert "DomainEntity" not in base_names
    assert descriptor.bases == []


def test_document_content_has_no_forbidden_dependencies() -> None:
    imported_modules = _imported_modules(
        _content_tree()
    )

    violations = {
        module
        for module in imported_modules
        if module.startswith(
            FORBIDDEN_IMPORT_PREFIXES
        )
    }

    assert violations == set()


def test_document_content_introduces_no_repository_contract() -> None:
    class_names = set(
        _classes(_content_tree())
    )

    assert not any(
        name.endswith("Repository")
        or name.endswith("Store")
        for name in class_names
    )


def test_document_content_performs_no_file_io() -> None:
    tree = _content_tree()

    forbidden_calls: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "open"
        ):
            forbidden_calls.append("open")

        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr
            in {
                "open",
                "read_text",
                "read_bytes",
                "write_text",
                "write_bytes",
            }
        ):
            forbidden_calls.append(
                node.func.attr
            )

    assert forbidden_calls == []


def test_document_content_does_not_depend_on_document_aggregate() -> None:
    imported_modules = _imported_modules(
        _content_tree()
    )

    assert "app.domain.document" not in imported_modules
