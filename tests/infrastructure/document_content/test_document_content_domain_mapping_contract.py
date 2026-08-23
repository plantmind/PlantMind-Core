from __future__ import annotations

import importlib

import pytest

from app.domain.base import DomainException, EntityId
from app.domain.document_content import (
    DocumentContentDescriptor,
    DocumentContentDigest,
    DocumentContentMediaType,
)


def _models():
    return importlib.import_module(
        "app.infrastructure.document_content.models"
    )


def _mapping():
    return importlib.import_module(
        "app.infrastructure.document_content.mapping"
    )


def _descriptor() -> DocumentContentDescriptor:
    return DocumentContentDescriptor(
        document_id=EntityId.new(),
        media_type=DocumentContentMediaType(
            value=" Application/PDF "
        ),
        byte_length=4096,
        digest=DocumentContentDigest(
            value="AB" * 32
        ),
    )


def test_domain_to_row_preserves_canonical_descriptor_values() -> None:
    descriptor = _descriptor()

    row = _mapping().descriptor_to_row(descriptor)

    assert isinstance(
        row,
        _models().DocumentContentDescriptorRow,
    )
    assert row.document_id == descriptor.document_id.value
    assert row.media_type == "application/pdf"
    assert row.byte_length == 4096
    assert row.digest == ("ab" * 32)


def test_descriptor_round_trip_is_exact() -> None:
    original = _descriptor()

    restored = _mapping().row_to_descriptor(
        _mapping().descriptor_to_row(original)
    )

    assert restored == original


def test_row_to_descriptor_reconstructs_canonical_domain_types() -> None:
    row = _models().DocumentContentDescriptorRow(
        document_id=EntityId.new().value,
        media_type=" Text/Plain ",
        byte_length=12,
        digest="CD" * 32,
    )

    descriptor = _mapping().row_to_descriptor(row)

    assert isinstance(descriptor.document_id, EntityId)
    assert isinstance(
        descriptor.media_type,
        DocumentContentMediaType,
    )
    assert isinstance(
        descriptor.digest,
        DocumentContentDigest,
    )
    assert descriptor.media_type.value == "text/plain"
    assert descriptor.digest.value == ("cd" * 32)


def test_relational_reconstruction_preserves_domain_byte_length_validation() -> None:
    row = _models().DocumentContentDescriptorRow(
        document_id=EntityId.new().value,
        media_type="application/pdf",
        byte_length=-1,
        digest="ab" * 32,
    )

    with pytest.raises(DomainException):
        _mapping().row_to_descriptor(row)


def test_relational_reconstruction_preserves_media_type_validation() -> None:
    row = _models().DocumentContentDescriptorRow(
        document_id=EntityId.new().value,
        media_type="not-a-media-type",
        byte_length=1,
        digest="ab" * 32,
    )

    with pytest.raises(DomainException):
        _mapping().row_to_descriptor(row)


def test_relational_reconstruction_preserves_digest_validation() -> None:
    row = _models().DocumentContentDescriptorRow(
        document_id=EntityId.new().value,
        media_type="application/pdf",
        byte_length=1,
        digest="not-a-sha256-digest",
    )

    with pytest.raises(DomainException):
        _mapping().row_to_descriptor(row)
