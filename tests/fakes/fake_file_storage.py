from admirable.application.dto.files import UploadedFileDTO


class FakeFileStorage:
    def __init__(self) -> None:
        self.saved: list[tuple[str, str, str]] = []
        self.deleted: list[str] = []
        self._counter = 0

    async def save(self, file: UploadedFileDTO, directory: str, slug: str) -> str:
        self._counter += 1
        path = f"{directory}/{slug or 'file'}_{self._counter}_{file.filename}"
        self.saved.append((path, directory, slug))
        return path

    async def delete(self, path: str | None) -> None:
        if path:
            self.deleted.append(path)

    async def exists(self, path: str) -> bool:
        return path in {p for p, _, _ in self.saved} and path not in self.deleted
