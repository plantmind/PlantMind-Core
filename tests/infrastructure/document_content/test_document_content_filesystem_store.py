from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import pytest

from app.document_content.store import (
    DocumentContentPayloadAlreadyExistsError,
    DocumentContentStore,
)
from app.domain.base import EntityId
from app.infrastructure.document_content import (
    filesystem_store as module,
)
from app.infrastructure.document_content.filesystem_store import (
    FilesystemDocumentContentStore,
)


def entity_id() -> EntityId:
    return EntityId(
        value=uuid4()
    )


def final_path(
    root: Path,
    document_id: EntityId,
) -> Path:
    value = document_id.value.hex

    return (
        root
        / value[:2]
        / value[2:4]
        / f"{value}.bin"
    )


def temporary_files(
    root: Path,
) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if (
            path.is_file()
            and path.suffix == ".tmp"
        )
    ]


class NonSeekableSource:
    def __init__(
        self,
        payload: bytes,
    ) -> None:
        self._stream = BytesIO(
            payload
        )
        self.closed = False

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        return self._stream.read(
            size
        )

    def seek(
        self,
        *args: object,
        **kwargs: object,
    ) -> None:
        raise AssertionError(
            "seek() must not be required"
        )

    def tell(self) -> int:
        raise AssertionError(
            "tell() must not be required"
        )

    def fileno(self) -> int:
        raise AssertionError(
            "source fileno() must not be required"
        )

    def close(self) -> None:
        self.closed = True


class ExplodingSource:
    closed = False

    def read(
        self,
        size: int = -1,
    ) -> bytes:
        raise OSError(
            "source read failed"
        )

    def close(self) -> None:
        self.closed = True


def test_adapter_implements_canonical_store_port(
    tmp_path: Path,
) -> None:
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    assert isinstance(
        store,
        DocumentContentStore,
    )


def test_root_must_be_path() -> None:
    with pytest.raises(TypeError):
        FilesystemDocumentContentStore(
            "/tmp/plantmind"  # type: ignore[arg-type]
        )


def test_root_must_be_absolute() -> None:
    with pytest.raises(ValueError):
        FilesystemDocumentContentStore(
            Path("relative-root")
        )


def test_root_must_already_exist(
    tmp_path: Path,
) -> None:
    root = (
        tmp_path
        / "missing"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        FilesystemDocumentContentStore(
            root
        )

    assert not root.exists()


def test_root_must_be_directory(
    tmp_path: Path,
) -> None:
    root = (
        tmp_path
        / "content-root"
    )
    root.write_bytes(b"x")

    with pytest.raises(
        NotADirectoryError
    ):
        FilesystemDocumentContentStore(
            root
        )


def test_add_uses_deterministic_private_layout(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    payload = b"payload"

    store = FilesystemDocumentContentStore(
        tmp_path
    )
    store.add(
        document_id,
        BytesIO(payload),
    )

    path = final_path(
        tmp_path,
        document_id,
    )

    assert path.is_file()
    assert path.read_bytes() == payload


def test_add_consumes_current_position_to_eof(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    source = BytesIO(
        b"prefix-payload"
    )
    source.seek(
        len(b"prefix-")
    )

    store = FilesystemDocumentContentStore(
        tmp_path
    )
    store.add(
        document_id,
        source,
    )

    assert final_path(
        tmp_path,
        document_id,
    ).read_bytes() == b"payload"

    assert not source.closed


def test_non_seekable_source_supported_and_not_closed(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    source = NonSeekableSource(
        b"streamed"
    )

    store = FilesystemDocumentContentStore(
        tmp_path
    )
    store.add(
        document_id,
        source,  # type: ignore[arg-type]
    )

    assert final_path(
        tmp_path,
        document_id,
    ).read_bytes() == b"streamed"

    assert source.closed is False


def test_zero_byte_payload_is_present(
    tmp_path: Path,
) -> None:
    document_id = entity_id()

    store = FilesystemDocumentContentStore(
        tmp_path
    )
    store.add(
        document_id,
        BytesIO(b""),
    )

    path = final_path(
        tmp_path,
        document_id,
    )

    assert path.exists()
    assert path.stat().st_size == 0

    opened = store.open(
        document_id
    )

    assert opened is not None

    with opened as stream:
        assert stream.read() == b""


def test_duplicate_identical_payload_rejected(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    store.add(
        document_id,
        BytesIO(b"a"),
    )

    source = BytesIO(b"a")

    with pytest.raises(
        DocumentContentPayloadAlreadyExistsError
    ):
        store.add(
            document_id,
            source,
        )

    assert source.closed is False
    assert final_path(
        tmp_path,
        document_id,
    ).read_bytes() == b"a"


def test_duplicate_different_payload_preserves_existing(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    store.add(
        document_id,
        BytesIO(b"first"),
    )

    with pytest.raises(
        DocumentContentPayloadAlreadyExistsError
    ):
        store.add(
            document_id,
            BytesIO(b"second"),
        )

    assert final_path(
        tmp_path,
        document_id,
    ).read_bytes() == b"first"


def test_temporary_collision_is_not_document_duplicate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    def collide(
        *args: object,
        **kwargs: object,
    ) -> tuple[int, str]:
        raise FileExistsError(
            "temporary collision"
        )

    monkeypatch.setattr(
        module.tempfile,
        "mkstemp",
        collide,
    )

    with pytest.raises(
        FileExistsError
    ) as exc_info:
        store.add(
            entity_id(),
            BytesIO(b"x"),
        )

    assert not isinstance(
        exc_info.value,
        DocumentContentPayloadAlreadyExistsError,
    )


def test_non_duplicate_link_error_propagates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    def denied(
        *args: object,
        **kwargs: object,
    ) -> None:
        raise PermissionError(
            "link denied"
        )

    monkeypatch.setattr(
        module.os,
        "link",
        denied,
    )

    with pytest.raises(
        PermissionError
    ):
        store.add(
            document_id,
            BytesIO(b"x"),
        )

    assert not final_path(
        tmp_path,
        document_id,
    ).exists()

    assert temporary_files(
        tmp_path
    ) == []


def test_source_failure_publishes_no_partial_payload(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    source = ExplodingSource()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    with pytest.raises(
        OSError,
        match="source read failed",
    ):
        store.add(
            document_id,
            source,  # type: ignore[arg-type]
        )

    assert not final_path(
        tmp_path,
        document_id,
    ).exists()

    assert temporary_files(
        tmp_path
    ) == []

    assert source.closed is False


def test_fsync_failure_publishes_no_partial_payload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    def fail_fsync(
        fd: int,
    ) -> None:
        raise OSError(
            "fsync failed"
        )

    monkeypatch.setattr(
        module.os,
        "fsync",
        fail_fsync,
    )

    with pytest.raises(
        OSError,
        match="fsync failed",
    ):
        store.add(
            document_id,
            BytesIO(b"payload"),
        )

    assert not final_path(
        tmp_path,
        document_id,
    ).exists()

    assert temporary_files(
        tmp_path
    ) == []


def test_post_publication_cleanup_failure_keeps_complete_payload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    original_unlink = module.Path.unlink

    def fail_temp_unlink(
        self: Path,
        *args: object,
        **kwargs: object,
    ) -> None:
        if self.suffix == ".tmp":
            raise OSError(
                "cleanup failed"
            )

        original_unlink(
            self,
            *args,
            **kwargs,
        )

    monkeypatch.setattr(
        module.Path,
        "unlink",
        fail_temp_unlink,
    )

    with pytest.raises(
        OSError,
        match="cleanup failed",
    ):
        store.add(
            document_id,
            BytesIO(b"complete"),
        )

    assert final_path(
        tmp_path,
        document_id,
    ).read_bytes() == b"complete"


def test_success_leaves_no_temporary_artifact(
    tmp_path: Path,
) -> None:
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    store.add(
        entity_id(),
        BytesIO(b"x"),
    )

    assert temporary_files(
        tmp_path
    ) == []


def test_missing_payload_under_healthy_root_returns_none(
    tmp_path: Path,
) -> None:
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    assert store.open(
        entity_id()
    ) is None


def test_missing_root_after_construction_is_operational_failure(
    tmp_path: Path,
) -> None:
    root = (
        tmp_path
        / "content-root"
    )
    root.mkdir()

    store = FilesystemDocumentContentStore(
        root
    )

    root.rmdir()

    with pytest.raises(
        FileNotFoundError
    ):
        store.open(
            entity_id()
        )

    assert not root.exists()


def test_add_never_recreates_missing_root(
    tmp_path: Path,
) -> None:
    root = (
        tmp_path
        / "content-root"
    )
    root.mkdir()

    store = FilesystemDocumentContentStore(
        root
    )

    root.rmdir()

    with pytest.raises(
        FileNotFoundError
    ):
        store.add(
            entity_id(),
            BytesIO(b"x"),
        )

    assert not root.exists()


def test_shard_file_collision_is_operational_not_duplicate(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    value = document_id.value.hex

    first = (
        tmp_path
        / value[:2]
    )
    first.write_bytes(b"not-a-directory")

    store = FilesystemDocumentContentStore(
        tmp_path
    )

    with pytest.raises(
        FileExistsError
    ) as exc_info:
        store.add(
            document_id,
            BytesIO(b"x"),
        )

    assert not isinstance(
        exc_info.value,
        DocumentContentPayloadAlreadyExistsError,
    )


def test_open_operational_error_does_not_become_none(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    store.add(
        document_id,
        BytesIO(b"x"),
    )

    def denied_open(
        self: Path,
        *args: object,
        **kwargs: object,
    ) -> object:
        raise PermissionError(
            "read denied"
        )

    monkeypatch.setattr(
        module.Path,
        "open",
        denied_open,
    )

    with pytest.raises(
        PermissionError,
        match="read denied",
    ):
        store.open(
            document_id
        )


def test_repeated_opens_are_independent_and_begin_at_zero(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    store.add(
        document_id,
        BytesIO(b"abcdef"),
    )

    first = store.open(
        document_id
    )
    second = store.open(
        document_id
    )

    assert first is not None
    assert second is not None

    with first as left:
        assert left.read(2) == b"ab"

        with second as right:
            assert right.read(3) == b"abc"

        assert second.closed
        assert left.read(2) == b"cd"

    assert first.closed


def test_exceptional_context_exit_closes_read_resource(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    store.add(
        document_id,
        BytesIO(b"x"),
    )

    opened = store.open(
        document_id
    )

    assert opened is not None

    with pytest.raises(
        RuntimeError,
        match="consumer failed",
    ):
        with opened:
            raise RuntimeError(
                "consumer failed"
            )

    assert opened.closed


def test_concurrent_same_document_add_has_one_winner(
    tmp_path: Path,
) -> None:
    document_id = entity_id()
    store = FilesystemDocumentContentStore(
        tmp_path
    )

    payloads = [
        f"payload-{index}".encode()
        for index in range(8)
    ]

    def write(
        payload: bytes,
    ) -> tuple[str, bytes]:
        try:
            store.add(
                document_id,
                BytesIO(payload),
            )
        except DocumentContentPayloadAlreadyExistsError:
            return (
                "duplicate",
                payload,
            )

        return (
            "success",
            payload,
        )

    with ThreadPoolExecutor(
        max_workers=8
    ) as executor:
        results = list(
            executor.map(
                write,
                payloads,
            )
        )

    winners = [
        payload
        for status, payload in results
        if status == "success"
    ]

    duplicates = [
        payload
        for status, payload in results
        if status == "duplicate"
    ]

    assert len(winners) == 1
    assert len(duplicates) == 7

    assert final_path(
        tmp_path,
        document_id,
    ).read_bytes() == winners[0]

    assert temporary_files(
        tmp_path
    ) == []


def test_adapter_has_no_forbidden_cross_boundary_dependencies() -> None:
    source = Path(
        module.__file__
    ).read_text()

    forbidden = [
        "sqlalchemy",
        "databaseruntime",
        "compositionroot",
        "configurationprovider",
        "documentcontentdescriptor",
        "documentcontentrepository",
        "enterprisedocumentrepository",
        "boto",
        "minio",
        "requests",
        "httpx",
    ]

    lowered = source.lower()

    for marker in forbidden:
        assert marker not in lowered


def test_adapter_does_not_use_process_local_correctness_lock() -> None:
    source = Path(
        module.__file__
    ).read_text()

    assert "threading.Lock" not in source
    assert "threading.RLock" not in source
    assert "multiprocessing" not in source
