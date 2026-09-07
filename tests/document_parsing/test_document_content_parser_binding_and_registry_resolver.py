"""RFC-076 canonical parser binding and registry-backed resolver tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from importlib import import_module
from typing import Any

import pytest

from app.core.registry import (
    DuplicateRegistrationError,
    RegistrationNotFoundError,
)
from app.document_parsing.parser import (
    DocumentContentParser,
    DocumentContentParserUnsupportedMediaTypeError,
)
from app.document_parsing.resolver import DocumentContentParserResolver
from app.domain.document_content import DocumentContentMediaType


def _binding_module():
    return import_module("app.document_parsing.binding")


def _adapter_module():
    return import_module(
        "app.infrastructure.document_parsing.registry_backed_resolver"
    )


def _binding(
    *,
    media_type: DocumentContentMediaType,
    factory: object,
):
    return _binding_module().DocumentContentParserBinding(
        media_type=media_type,
        factory=factory,
    )


def _resolver(*, bindings: object):
    return _adapter_module().RegistryBackedDocumentContentParserResolver(
        bindings=bindings,
    )


class RecordingParser(DocumentContentParser):
    def __init__(self, marker: str) -> None:
        self.marker = marker

    def parse(
        self,
        *,
        descriptor: object,
        payload: object,
    ) -> str:
        return self.marker


class SinglePassBindings:
    def __init__(self, values: list[object]) -> None:
        self.values = values
        self.iterations = 0

    def __iter__(self):
        self.iterations += 1

        if self.iterations > 1:
            raise AssertionError(
                "bindings iterable must be consumed exactly once"
            )

        yield from self.values


def test_binding_is_frozen_and_slot_backed() -> None:
    media_type = DocumentContentMediaType(
        value="application/pdf",
    )
    binding = _binding(
        media_type=media_type,
        factory=lambda: RecordingParser("pdf"),
    )

    with pytest.raises(FrozenInstanceError):
        binding.media_type = media_type

    assert not hasattr(binding, "__dict__")


def test_binding_preserves_exact_media_type_and_factory_identity() -> None:
    media_type = DocumentContentMediaType(
        value="application/pdf",
    )
    factory = lambda: RecordingParser("pdf")

    binding = _binding(
        media_type=media_type,
        factory=factory,
    )

    assert binding.media_type is media_type
    assert binding.factory is factory


def test_binding_rejects_non_media_type() -> None:
    with pytest.raises(
        TypeError,
        match="must be a DocumentContentMediaType",
    ):
        _binding(
            media_type="application/pdf",
            factory=lambda: RecordingParser("pdf"),
        )


def test_binding_rejects_non_callable_factory() -> None:
    with pytest.raises(
        TypeError,
        match="factory must be callable",
    ):
        _binding(
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
            factory=object(),
        )


def test_resolver_implements_existing_resolver_port() -> None:
    resolver = _resolver(
        bindings=(),
    )

    assert isinstance(
        resolver,
        DocumentContentParserResolver,
    )


def test_bindings_iterable_is_consumed_exactly_once() -> None:
    bindings = SinglePassBindings(
        [
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=lambda: RecordingParser("pdf"),
            ),
        ]
    )

    _resolver(
        bindings=bindings,
    )

    assert bindings.iterations == 1


def test_resolver_rejects_non_binding_item() -> None:
    with pytest.raises(
        TypeError,
        match="must contain only DocumentContentParserBinding",
    ):
        _resolver(
            bindings=[object()],
        )


def test_parser_factories_are_not_invoked_during_construction() -> None:
    calls = 0

    def factory() -> DocumentContentParser:
        nonlocal calls
        calls += 1
        return RecordingParser("pdf")

    _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=factory,
            ),
        ],
    )

    assert calls == 0


def test_normalized_media_type_value_is_exact_registry_key() -> None:
    media_type = DocumentContentMediaType(
        value=" APPLICATION/PDF ",
    )
    resolver = _resolver(
        bindings=[
            _binding(
                media_type=media_type,
                factory=lambda: RecordingParser("pdf"),
            ),
        ],
    )

    assert media_type.value == "application/pdf"
    assert resolver._registry.registered() == (
        "application/pdf",
    )


def test_registry_supplier_returns_exact_binding_not_parser() -> None:
    calls = 0

    def factory() -> DocumentContentParser:
        nonlocal calls
        calls += 1
        return RecordingParser("pdf")

    media_type = DocumentContentMediaType(
        value="application/pdf",
    )
    binding = _binding(
        media_type=media_type,
        factory=factory,
    )
    resolver = _resolver(
        bindings=[binding],
    )

    supplier = resolver._registry._entries[
        media_type.value
    ]

    assert supplier() is binding
    assert calls == 0


def test_duplicate_normalized_media_types_fail_with_preserved_cause() -> None:
    duplicate_error = (
        _binding_module()
        .DocumentContentParserDuplicateBindingError
    )

    first = _binding(
        media_type=DocumentContentMediaType(
            value=" APPLICATION/PDF ",
        ),
        factory=lambda: RecordingParser("first"),
    )
    second = _binding(
        media_type=DocumentContentMediaType(
            value="application/pdf",
        ),
        factory=lambda: RecordingParser("second"),
    )

    with pytest.raises(duplicate_error) as exc_info:
        _resolver(
            bindings=[first, second],
        )

    assert isinstance(
        exc_info.value.__cause__,
        DuplicateRegistrationError,
    )


def test_resolver_exposes_no_public_mutation_api() -> None:
    resolver = _resolver(
        bindings=(),
    )

    assert not hasattr(resolver, "register")
    assert not hasattr(resolver, "clear")


def test_non_media_type_resolution_input_fails_before_lookup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resolver = _resolver(
        bindings=(),
    )
    lookup_calls = 0

    def fail_if_called(name: str) -> object:
        nonlocal lookup_calls
        lookup_calls += 1
        raise AssertionError(
            "registry lookup must not occur for invalid media type"
        )

    monkeypatch.setattr(
        resolver._registry,
        "resolve",
        fail_if_called,
    )

    with pytest.raises(
        TypeError,
        match="resolver media type must be",
    ):
        resolver.resolve(
            media_type="application/pdf",
        )

    assert lookup_calls == 0


def test_missing_media_type_maps_to_existing_unsupported_error_with_cause() -> None:
    resolver = _resolver(
        bindings=(),
    )

    with pytest.raises(
        DocumentContentParserUnsupportedMediaTypeError
    ) as exc_info:
        resolver.resolve(
            media_type=DocumentContentMediaType(
                value="application/x-missing",
            ),
        )

    assert isinstance(
        exc_info.value.__cause__,
        RegistrationNotFoundError,
    )


def test_selected_factory_is_invoked_exactly_once_per_resolution() -> None:
    calls = 0
    parser = RecordingParser("pdf")

    def factory() -> DocumentContentParser:
        nonlocal calls
        calls += 1
        return parser

    resolver = _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=factory,
            ),
        ],
    )

    result = resolver.resolve(
        media_type=DocumentContentMediaType(
            value="application/pdf",
        ),
    )

    assert result is parser
    assert calls == 1


def test_factory_keyerror_propagates_as_same_instance() -> None:
    failure = KeyError(
        "registered parser factory failure"
    )

    def factory() -> DocumentContentParser:
        raise failure

    resolver = _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=factory,
            ),
        ],
    )

    with pytest.raises(KeyError) as exc_info:
        resolver.resolve(
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
        )

    assert exc_info.value is failure


def test_other_factory_failure_propagates_as_same_instance() -> None:
    failure = RuntimeError(
        "parser factory operational failure"
    )

    def factory() -> DocumentContentParser:
        raise failure

    resolver = _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=factory,
            ),
        ],
    )

    with pytest.raises(RuntimeError) as exc_info:
        resolver.resolve(
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
        )

    assert exc_info.value is failure


def test_invalid_factory_result_raises_typeerror() -> None:
    resolver = _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=lambda: object(),
            ),
        ],
    )

    with pytest.raises(
        TypeError,
        match="factory must return DocumentContentParser",
    ):
        resolver.resolve(
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
        )


def test_resolver_performs_no_parser_caching() -> None:
    calls = 0

    def factory() -> DocumentContentParser:
        nonlocal calls
        calls += 1
        return RecordingParser(
            marker=str(calls),
        )

    resolver = _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=factory,
            ),
        ],
    )
    media_type = DocumentContentMediaType(
        value="application/pdf",
    )

    first = resolver.resolve(
        media_type=media_type,
    )
    second = resolver.resolve(
        media_type=media_type,
    )

    assert first is not second
    assert calls == 2


def test_factory_owned_stable_instance_policy_is_preserved() -> None:
    parser = RecordingParser("stable")
    resolver = _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="text/plain",
                ),
                factory=lambda: parser,
            ),
        ],
    )
    media_type = DocumentContentMediaType(
        value="text/plain",
    )

    assert resolver.resolve(
        media_type=media_type,
    ) is parser
    assert resolver.resolve(
        media_type=media_type,
    ) is parser


def test_multiple_canonical_bindings_resolve_independently() -> None:
    pdf_parser = RecordingParser("pdf")
    text_parser = RecordingParser("text")

    resolver = _resolver(
        bindings=[
            _binding(
                media_type=DocumentContentMediaType(
                    value="application/pdf",
                ),
                factory=lambda: pdf_parser,
            ),
            _binding(
                media_type=DocumentContentMediaType(
                    value="text/plain",
                ),
                factory=lambda: text_parser,
            ),
        ],
    )

    assert resolver.resolve(
        media_type=DocumentContentMediaType(
            value="application/pdf",
        ),
    ) is pdf_parser

    assert resolver.resolve(
        media_type=DocumentContentMediaType(
            value="text/plain",
        ),
    ) is text_parser


def test_empty_binding_set_fails_closed_on_resolution() -> None:
    resolver = _resolver(
        bindings=(),
    )

    with pytest.raises(
        DocumentContentParserUnsupportedMediaTypeError
    ):
        resolver.resolve(
            media_type=DocumentContentMediaType(
                value="text/plain",
            ),
        )
