from typing import Protocol

from admirable.application.dto.files import UploadedFileDTO


class FileStoragePort(Protocol):
    async def save(self, file: UploadedFileDTO, directory: str, slug: str) -> str: ...

    async def delete(self, path: str | None) -> None: ...

    async def exists(self, path: str) -> bool: ...
