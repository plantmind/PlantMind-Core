"""RFC-066 canonical Document Content domain behavior."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.domain.base import DomainEntity, DomainException, EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)


# ---------------------------------------------------------------------------
# DocumentContentMediaType
# ---------------------------------------------------------------------------


def test_document_content_media_type_normalizes_value() -> None:
    media_type = DocumentContentMediaType(
        value="  Application/PDF  ",
    )

    assert media_type.value == "application/pdf"


def test_document_content_media_type_accepts_unknown_structural_type() -> None:
    media_type = DocumentContentMediaType(
        value="X-PlantMind/Custom",
    )

    assert media_type.value == "x-plantmind/custom"


@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
        True,
    ],
)
def test_document_content_media_type_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        DomainException,
        match="Document content media type must be a string",
    ):
        DocumentContentMediaType(value=value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        "\t\n",
    ],
)
def test_document_content_media_type_rejects_empty_value(
    value: str,
) -> None:
    with pytest.raises(
        DomainException,
        match="Document content media type must not be empty",
    ):
        DocumentContentMediaType(value=value)


@pytest.mark.parametrize(
    "value",
    [
        "text/plain; charset=utf-8",
        "application/pdf;version=1",
    ],
)
def test_document_content_media_type_rejects_parameters(
    value: str,
) -> None:
    with pytest.raises(
        DomainException,
        match="must not contain parameters",
    ):
        DocumentContentMediaType(value=value)


@pytest.mark.parametrize(
    "value",
    [
        "applicationpdf",
        "application/pdf/extra",
    ],
)
def test_document_content_media_type_requires_exactly_one_slash(
    value: str,
) -> None:
    with pytest.raises(
        DomainException,
        match="must contain exactly one '/'",
    ):
        DocumentContentMediaType(value=value)


@pytest.mark.parametrize(
    "value",
    [
        "/pdf",
        "application/",
    ],
)
def test_document_content_media_type_requires_type_and_subtype(
    value: str,
) -> None:
    with pytest.raises(
        DomainException,
        match="must contain non-empty type and subtype",
    ):
        DocumentContentMediaType(value=value)


@pytest.mark.parametrize(
    "value",
    [
        "application /pdf",
        "application/ pdf",
        "application/\tpdf",
        "application/\npdf",
        "application/\rpdf",
    ],
)
def test_document_content_media_type_rejects_internal_ascii_whitespace(
    value: str,
) -> None:
    with pytest.raises(
        DomainException,
        match="must not contain ASCII whitespace",
    ):
        DocumentContentMediaType(value=value)


def test_document_content_media_type_is_immutable() -> None:
    media_type = DocumentContentMediaType(
        value="application/pdf",
    )

    with pytest.raises(FrozenInstanceError):
        media_type.value = "text/plain"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# DocumentContentDigest
# ---------------------------------------------------------------------------


def test_document_content_digest_normalizes_sha256_hex() -> None:
    digest = DocumentContentDigest(
        value="  " + ("A" * 64) + "  ",
    )

    assert digest.value == "a" * 64


def test_document_content_digest_accepts_valid_sha256_format() -> None:
    digest = DocumentContentDigest(
        value="0123456789abcdef" * 4,
    )

    assert digest.value == "0123456789abcdef" * 4


def test_document_content_digest_validates_format_without_payload() -> None:
    digest = DocumentContentDigest(
        value="0" * 64,
    )

    assert digest.value == "0" * 64


@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
        True,
    ],
)
def test_document_content_digest_requires_string(
    value: object,
) -> None:
    with pytest.raises(
        DomainException,
        match="Document content digest must be a string",
    ):
        DocumentContentDigest(value=value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        "a" * 63,
        "a" * 65,
    ],
)
def test_document_content_digest_requires_exactly_64_characters(
    value: str,
) -> None:
    with pytest.raises(
        DomainException,
        match="must contain exactly 64 hexadecimal characters",
    ):
        DocumentContentDigest(value=value)


@pytest.mark.parametrize(
    "value",
    [
        "g" * 64,
        ("a" * 63) + "!",
        ("0" * 32) + ("z" * 32),
    ],
)
def test_document_content_digest_rejects_non_hexadecimal_value(
    value: str,
) -> None:
    with pytest.raises(
        DomainException,
        match="must contain exactly 64 hexadecimal characters",
    ):
        DocumentContentDigest(value=value)


def test_document_content_digest_is_immutable() -> None:
    digest = DocumentContentDigest(
        value="a" * 64,
    )

    with pytest.raises(FrozenInstanceError):
        digest.value = "b" * 64  # type: ignore[misc]

# ---------------------------------------------------------------------------
# DocumentContentDescriptor
# ---------------------------------------------------------------------------


def _valid_document_content_descriptor() -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=EntityId.new(),
        media_type=DocumentContentMediaType(
            value="application/pdf",
        ),
        byte_length=1024,
        digest=DocumentContentDigest(
            value="a" * 64,
        ),
    )


def test_document_content_descriptor_preserves_canonical_values() -> None:
    document_id = EntityId.new()
    media_type = DocumentContentMediaType(
        value="application/pdf",
    )
    digest = DocumentContentDigest(
        value="b" * 64,
    )

    descriptor = DocumentContentDescriptor(
        document_id=document_id,
        media_type=media_type,
        byte_length=2048,
        digest=digest,
    )

    assert descriptor.document_id is document_id
    assert descriptor.media_type is media_type
    assert descriptor.byte_length == 2048
    assert descriptor.digest is digest


def test_document_content_descriptor_allows_zero_byte_length() -> None:
    descriptor = DocumentContentDescriptor(
        document_id=EntityId.new(),
        media_type=DocumentContentMediaType(
            value="application/octet-stream",
        ),
        byte_length=0,
        digest=DocumentContentDigest(
            value="0" * 64,
        ),
    )

    assert descriptor.byte_length == 0


@pytest.mark.parametrize(
    "document_id",
    [
        None,
        "document-1",
        123,
    ],
)
def test_document_content_descriptor_requires_entity_id(
    document_id: object,
) -> None:
    with pytest.raises(
        DomainException,
        match="Document content document id must be an EntityId",
    ):
        DocumentContentDescriptor(
            document_id=document_id,  # type: ignore[arg-type]
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
            byte_length=1,
            digest=DocumentContentDigest(
                value="a" * 64,
            ),
        )


@pytest.mark.parametrize(
    "media_type",
    [
        None,
        "application/pdf",
        123,
    ],
)
def test_document_content_descriptor_requires_canonical_media_type(
    media_type: object,
) -> None:
    with pytest.raises(
        DomainException,
        match=(
            "Document content media type must be "
            "a DocumentContentMediaType"
        ),
    ):
        DocumentContentDescriptor(
            document_id=EntityId.new(),
            media_type=media_type,  # type: ignore[arg-type]
            byte_length=1,
            digest=DocumentContentDigest(
                value="a" * 64,
            ),
        )


@pytest.mark.parametrize(
    "digest",
    [
        None,
        "a" * 64,
        123,
    ],
)
def test_document_content_descriptor_requires_canonical_digest(
    digest: object,
) -> None:
    with pytest.raises(
        DomainException,
        match=(
            "Document content digest must be "
            "a DocumentContentDigest"
        ),
    ):
        DocumentContentDescriptor(
            document_id=EntityId.new(),
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
            byte_length=1,
            digest=digest,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "byte_length",
    [
        None,
        "1",
        1.5,
        True,
        False,
    ],
)
def test_document_content_descriptor_requires_integer_byte_length(
    byte_length: object,
) -> None:
    with pytest.raises(
        DomainException,
        match="Document content byte length must be an integer",
    ):
        DocumentContentDescriptor(
            document_id=EntityId.new(),
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
            byte_length=byte_length,  # type: ignore[arg-type]
            digest=DocumentContentDigest(
                value="a" * 64,
            ),
        )


def test_document_content_descriptor_rejects_negative_byte_length() -> None:
    with pytest.raises(
        DomainException,
        match="Document content byte length must not be negative",
    ):
        DocumentContentDescriptor(
            document_id=EntityId.new(),
            media_type=DocumentContentMediaType(
                value="application/pdf",
            ),
            byte_length=-1,
            digest=DocumentContentDigest(
                value="a" * 64,
            ),
        )


def test_document_content_descriptor_is_not_domain_entity() -> None:
    descriptor = _valid_document_content_descriptor()

    assert not isinstance(descriptor, DomainEntity)


def test_document_content_descriptor_is_immutable() -> None:
    descriptor = _valid_document_content_descriptor()

    with pytest.raises(FrozenInstanceError):
        descriptor.byte_length = 2  # type: ignore[misc]
