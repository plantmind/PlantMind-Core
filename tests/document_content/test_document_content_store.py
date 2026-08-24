"""RFC-070 canonical binary Document Content store contract tests."""

from __future__ import annotations

from abc import ABC
from contextlib import AbstractContextManager
import importlib
import inspect
from typing import BinaryIO, get_type_hints


MODULE_NAME = "app.document_content.store"


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


def test_store_module_exists() -> None:
    module = _module()
    assert module.__name__ == MODULE_NAME


def test_store_public_class_family_is_exact() -> None:
    module = _module()

    assert set(_defined_public_classes(module)) == {
        "DocumentContentPayloadAlreadyExistsError",
        "DocumentContentStore",
    }


def test_duplicate_error_is_plain_exception() -> None:
    module = _module()

    assert (
        module.DocumentContentPayloadAlreadyExistsError.__bases__
        == (Exception,)
    )


def test_store_is_abstract_add_open_port() -> None:
    module = _module()
    store = module.DocumentContentStore

    assert issubclass(store, ABC)
    assert inspect.isabstract(store)

    public_methods = {
        name
        for name, value in store.__dict__.items()
        if callable(value)
        and not name.startswith("_")
    }

    assert public_methods == {"add", "open"}
    assert store.__abstractmethods__ == frozenset(
        {"add", "open"}
    )


def test_add_signature_is_canonical() -> None:
    module = _module()

    from app.domain.base import EntityId

    method = module.DocumentContentStore.add
    signature = inspect.signature(method)
    hints = get_type_hints(method)

    assert list(signature.parameters) == [
        "self",
        "document_id",
        "source",
    ]
    assert hints["document_id"] is EntityId
    assert hints["source"] is BinaryIO
    assert hints["return"] is type(None)


def test_open_signature_is_canonical() -> None:
    module = _module()

    from app.domain.base import EntityId

    method = module.DocumentContentStore.open
    signature = inspect.signature(method)
    hints = get_type_hints(method)

    assert list(signature.parameters) == [
        "self",
        "document_id",
    ]
    assert hints["document_id"] is EntityId
    assert hints["return"] == (
        AbstractContextManager[BinaryIO] | None
    )


def test_store_has_no_forbidden_operations() -> None:
    module = _module()
    store = module.DocumentContentStore

    forbidden = {
        "list",
        "find",
        "search",
        "filter",
        "query",
        "paginate",
        "get_by_digest",
        "get_by_path",
        "get_by_uri",
        "read_bytes",
        "open_stream",
        "download",
        "update",
        "replace",
        "delete",
        "upsert",
    }

    assert not (set(store.__dict__) & forbidden)


def test_store_exposes_no_canonical_content_identity() -> None:
    module = _module()

    assert not hasattr(module, "DocumentContentId")
    assert not hasattr(module, "BlobId")
    assert not hasattr(module, "StorageId")
