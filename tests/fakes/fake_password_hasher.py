class FakePasswordHasher:
    """`hash()` prefixes so `verify()` can check equality without real crypto."""

    def __init__(self, rehash_needed_for: set[str] | None = None) -> None:
        self._rehash_needed_for = rehash_needed_for or set()

    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == f"hashed:{password}"

    def needs_rehash(self, password_hash: str) -> bool:
        return password_hash in self._rehash_needed_for
