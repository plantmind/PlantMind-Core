"""Registry-backed canonical Document Content parser resolver adapter."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from app.core.registry import (
    DuplicateRegistrationError,
    RegistrationNotFoundError,
    Registry,
)
from app.document_parsing.binding import (
    DocumentContentParserBinding,
    DocumentContentParserDuplicateBindingError,
)
from app.document_parsing.parser import (
    DocumentContentParser,
    DocumentContentParserUnsupportedMediaTypeError,
)
from app.document_parsing.resolver import DocumentContentParserResolver
from app.domain.document_content import DocumentContentMediaType


BindingSupplier = Callable[[], DocumentContentParserBinding]


class RegistryBackedDocumentContentParserResolver(
    DocumentContentParserResolver
):
    """Resolve canonical parsers through a private binding-valued Registry."""

    def __init__(
        self,
        *,
        bindings: Iterable[DocumentContentParserBinding],
    ) -> None:
        snapshot = tuple(bindings)

        for binding in snapshot:
            if not isinstance(
                binding,
                DocumentContentParserBinding,
            ):
                raise TypeError(
                    "Document Content parser bindings must contain only "
                    "DocumentContentParserBinding values."
                )

        registry: Registry[DocumentContentParserBinding] = Registry()

        for binding in snapshot:
            try:
                registry.register(
                    binding.media_type.value,
                    self._binding_supplier(binding),
                )
            except DuplicateRegistrationError as exc:
                raise DocumentContentParserDuplicateBindingError(
                    "Duplicate Document Content parser binding for "
                    f"'{binding.media_type.value}'."
                ) from exc

        self._registry = registry

    @staticmethod
    def _binding_supplier(
        binding: DocumentContentParserBinding,
    ) -> BindingSupplier:
        def supply_binding() -> DocumentContentParserBinding:
            return binding

        return supply_binding

    def resolve(
        self,
        *,
        media_type: DocumentContentMediaType,
    ) -> DocumentContentParser:
        """Resolve one parser from a canonical media-type binding."""
        if not isinstance(
            media_type,
            DocumentContentMediaType,
        ):
            raise TypeError(
                "Document Content parser resolver media type must be "
                "a DocumentContentMediaType."
            )

        try:
            binding = self._registry.resolve(
                media_type.value,
            )
        except RegistrationNotFoundError as exc:
            raise DocumentContentParserUnsupportedMediaTypeError(
                "No Document Content parser is bound for "
                f"'{media_type.value}'."
            ) from exc

        parser = binding.factory()

        if not isinstance(
            parser,
            DocumentContentParser,
        ):
            raise TypeError(
                "Document Content parser factory must return "
                "DocumentContentParser."
            )

        return parser
