"""RFC-068 canonical Document Content repository contract tests."""

from __future__ import annotations

from abc import ABC
import importlib
import inspect
from typing import get_type_hints


MODULE_NAME = "app.document_content.repository"


def _module():
    return importlib.import_module(MODULE_NAME)


def _defined_public_classes(module):
    return {
        name: value
        for name, value in vars(module).items()
        if inspect.isclass(value)
        and value.__module__ == module.__name__
        and not name.startswith("_")
    }


def test_repository_module_exists() -> None:
    module = _module()
    assert module.__name__ == MODULE_NAME


def test_repository_family_is_exact() -> None:
    module = _module()

    assert set(_defined_public_classes(module)) == {
        "DocumentContentAlreadyExistsError",
        "DocumentContentRepository",
    }


def test_conflict_error_is_plain_exception() -> None:
    module = _module()

    assert (
        module.DocumentContentAlreadyExistsError.__bases__
        == (Exception,)
    )


def test_repository_is_abstract_add_get_port() -> None:
    module = _module()
    repository = module.DocumentContentRepository

    assert issubclass(repository, ABC)
    assert inspect.isabstract(repository)

    public_methods = {
        name
        for name, value in repository.__dict__.items()
        if callable(value)
        and not name.startswith("_")
    }

    assert public_methods == {"add", "get"}
    assert repository.__abstractmethods__ == frozenset(
        {"add", "get"}
    )


def test_add_signature_is_canonical() -> None:
    module = _module()

    from app.domain.document_content import (
        DocumentContentDescriptor,
    )

    method = module.DocumentContentRepository.add
    signature = inspect.signature(method)
    hints = get_type_hints(method)

    assert list(signature.parameters) == [
        "self",
        "descriptor",
    ]
    assert hints["descriptor"] is DocumentContentDescriptor
    assert hints["return"] is type(None)


def test_get_signature_is_canonical() -> None:
    module = _module()

    from app.domain.base import EntityId
    from app.domain.document_content import (
        DocumentContentDescriptor,
    )

    method = module.DocumentContentRepository.get
    signature = inspect.signature(method)
    hints = get_type_hints(method)

    assert list(signature.parameters) == [
        "self",
        "document_id",
    ]
    assert hints["document_id"] is EntityId
    assert hints["return"] == (
        DocumentContentDescriptor | None
    )


def test_no_forbidden_repository_operations() -> None:
    module = _module()
    repository = module.DocumentContentRepository

    forbidden = {
        "list",
        "find",
        "search",
        "filter",
        "query",
        "paginate",
        "get_by_digest",
        "update",
        "replace",
        "delete",
        "upsert",
        "read",
        "read_bytes",
        "open",
        "stream",
        "download",
    }

    assert not (set(repository.__dict__) & forbidden)


def test_no_content_identity_or_binary_store_contract() -> None:
    module = _module()

    assert not hasattr(module, "DocumentContentId")
    assert not hasattr(module, "DocumentContentStore")
