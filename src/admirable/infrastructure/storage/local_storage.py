"""Implements FileStoragePort on the local filesystem under `settings.media.root`."""

import secrets
import time
from pathlib import Path, PurePosixPath

import aiofiles

from admirable.application.dto.files import UploadedFileDTO

_ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp", "svg", "mp3", "wav", "m4a", "ogg"}


class PathTraversalError(Exception):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"Path escapes media root: {path!r}")


class UnsupportedFileExtensionError(Exception):
    def __init__(self, extension: str) -> None:
        self.extension = extension
        super().__init__(f"Unsupported file extension: {extension!r}")


class LocalFileStorage:
    def __init__(self, root: str) -> None:
        self._root = Path(root).resolve()

    def _extension(self, filename: str) -> str:
        return PurePosixPath(filename).suffix.lstrip(".").lower()

    def _resolve(self, relative_path: str) -> Path:
        candidate = (self._root / relative_path).resolve()
        if self._root not in candidate.parents and candidate != self._root:
            raise PathTraversalError(relative_path)
        return candidate

    async def save(self, file: UploadedFileDTO, directory: str, slug: str) -> str:
        extension = self._extension(file.filename)
        if extension not in _ALLOWED_EXTENSIONS:
            raise UnsupportedFileExtensionError(extension)

        name = slug or secrets.token_hex(8)
        filename = f"{name}_{int(time.time())}.{extension}"
        relative_path = f"{directory}/{filename}"
        destination = self._resolve(relative_path)

        destination.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(destination, "wb") as out:
            async for piece in file.stream:
                await out.write(piece)

        return relative_path

    async def delete(self, path: str | None) -> None:
        if not path:
            return
        target = self._resolve(path)
        target.unlink(missing_ok=True)

    async def exists(self, path: str) -> bool:
        return self._resolve(path).is_file()
