from collections.abc import AsyncIterator
from pathlib import Path

import pytest

from admirable.application.dto.files import UploadedFileDTO
from admirable.infrastructure.storage.local_storage import (
    LocalFileStorage,
    PathTraversalError,
    UnsupportedFileExtensionError,
)


async def _upload(filename: str, data: bytes = b"content") -> UploadedFileDTO:
    async def _stream() -> AsyncIterator[bytes]:
        yield data

    return UploadedFileDTO(filename=filename, content_type="image/jpeg", stream=_stream())


async def test_save_and_delete_round_trip(tmp_path: Path) -> None:
    storage = LocalFileStorage(str(tmp_path))
    path = await storage.save(await _upload("photo.jpg"), "uploads/avatars", "marie-curie")

    assert path.startswith("uploads/avatars/marie-curie_")
    assert await storage.exists(path) is True

    await storage.delete(path)
    assert await storage.exists(path) is False


async def test_delete_missing_file_is_noop(tmp_path: Path) -> None:
    storage = LocalFileStorage(str(tmp_path))
    await storage.delete("uploads/avatars/nonexistent.jpg")  # must not raise
    await storage.delete(None)  # must not raise


async def test_path_traversal_is_blocked(tmp_path: Path) -> None:
    storage = LocalFileStorage(str(tmp_path))
    with pytest.raises(PathTraversalError):
        await storage.save(await _upload("evil.jpg"), "../../etc", "x")


async def test_unsupported_extension_rejected(tmp_path: Path) -> None:
    storage = LocalFileStorage(str(tmp_path))
    with pytest.raises(UnsupportedFileExtensionError):
        await storage.save(await _upload("script.exe"), "uploads/avatars", "x")


async def test_filename_uses_slug_and_timestamp(tmp_path: Path) -> None:
    storage = LocalFileStorage(str(tmp_path))
    path = await storage.save(await _upload("photo.png"), "uploads/avatars", "steve-jobs")
    assert path.split("/")[-1].startswith("steve-jobs_")
    assert path.endswith(".png")
