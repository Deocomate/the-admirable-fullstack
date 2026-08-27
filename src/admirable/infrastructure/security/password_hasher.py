"""Implements PasswordHasherPort with bcrypt.

Python's `bcrypt` verifies Laravel's `$2y$` hashes directly (it's just a
notation variant of `$2b$`), so no prefix rewrite is needed for `verify()`.
New hashes are written with the standard `$2b$` prefix.
"""

import bcrypt

_ROUNDS = 12


class BcryptPasswordHasher:
    def __init__(self, rounds: int = _ROUNDS) -> None:
        self._rounds = rounds

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt(rounds=self._rounds)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("ascii")

    def verify(self, password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("ascii"))
        except ValueError:
            return False

    def needs_rehash(self, password_hash: str) -> bool:
        try:
            cost = int(password_hash.split("$")[2])
        except (IndexError, ValueError):
            return True
        return cost != self._rounds
