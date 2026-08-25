"""Filesystem-backed binary Document Content store adapter."""

from __future__ import annotations

import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path
from typing import BinaryIO

from app.document_content.store import (
    DocumentContentPayloadAlreadyExistsError,
    DocumentContentStore,
)
from app.domain.base import EntityId


class FilesystemDocumentContentStore(DocumentContentStore):
    """Persist immutable binary Document Content on a filesystem."""

    _COPY_BUFFER_SIZE = 1024 * 1024

    def __init__(
        self,
        root: Path,
    ) -> None:
        if not isinstance(root, Path):
            raise TypeError(
                "Document Content storage root must be a pathlib.Path."
            )

        if not root.is_absolute():
            raise ValueError(
                "Document Content storage root must be absolute."
            )

        self._root = root
        self._require_healthy_root()

    def add(
        self,
        document_id: EntityId,
        source: BinaryIO,
    ) -> None:
        """Establish one immutable payload without overwrite."""

        document_hex = self._document_hex(document_id)
        shard = self._ensure_shard(document_hex)
        final_path = shard / f"{document_hex}.bin"

        fd, temp_name = tempfile.mkstemp(
            prefix=f".{document_hex}.",
            suffix=".tmp",
            dir=shard,
        )
        temp_path = Path(temp_name)

        try:
            self._write_temporary_payload(
                fd,
                source,
            )

            try:
                os.link(
                    temp_path,
                    final_path,
                )
            except FileExistsError as exc:
                raise DocumentContentPayloadAlreadyExistsError(
                    "Binary Document Content payload already exists "
                    f"for document {document_id.value}."
                ) from exc
        finally:
            self._cleanup_temporary_path(
                temp_path
            )

    def open(
        self,
        document_id: EntityId,
    ) -> BinaryIO | None:
        """Open the payload, or return None for confirmed absence."""

        self._require_healthy_root()

        document_hex = self._document_hex(document_id)
        final_path = self._final_path(document_hex)

        try:
            return final_path.open("rb")
        except FileNotFoundError:
            # Re-check root before classifying the missing final
            # path as confirmed payload absence.
            self._require_healthy_root()
            return None

    def _require_healthy_root(self) -> None:
        mode = self._root.stat().st_mode

        if not stat.S_ISDIR(mode):
            raise NotADirectoryError(
                str(self._root)
            )

    def _ensure_shard(
        self,
        document_hex: str,
    ) -> Path:
        self._require_healthy_root()

        first = (
            self._root
            / document_hex[:2]
        )
        second = (
            first
            / document_hex[2:4]
        )

        # parents=False is intentional: the adapter must never
        # recreate a missing configured storage root.
        first.mkdir(
            exist_ok=True,
        )
        second.mkdir(
            exist_ok=True,
        )

        return second

    def _final_path(
        self,
        document_hex: str,
    ) -> Path:
        return (
            self._root
            / document_hex[:2]
            / document_hex[2:4]
            / f"{document_hex}.bin"
        )

    @staticmethod
    def _document_hex(
        document_id: EntityId,
    ) -> str:
        return document_id.value.hex

    @classmethod
    def _write_temporary_payload(
        cls,
        fd: int,
        source: BinaryIO,
    ) -> None:
        try:
            writer = os.fdopen(
                fd,
                "wb",
            )
        except BaseException:
            os.close(fd)
            raise

        try:
            shutil.copyfileobj(
                source,
                writer,
                length=cls._COPY_BUFFER_SIZE,
            )
            writer.flush()
            os.fsync(
                writer.fileno()
            )
        except BaseException as exc:
            try:
                writer.close()
            except BaseException as close_exc:
                if hasattr(
                    exc,
                    "add_note",
                ):
                    exc.add_note(
                        "Temporary payload close also failed: "
                        f"{close_exc!r}"
                    )
            raise
        else:
            # A close failure is a pre-publication failure.
            writer.close()

    @staticmethod
    def _cleanup_temporary_path(
        temp_path: Path,
    ) -> None:
        primary = sys.exc_info()[1]

        try:
            temp_path.unlink(
                missing_ok=True
            )
        except OSError as cleanup_exc:
            if primary is None:
                raise

            if hasattr(
                primary,
                "add_note",
            ):
                primary.add_note(
                    "Temporary payload cleanup also failed: "
                    f"{cleanup_exc!r}"
                )
