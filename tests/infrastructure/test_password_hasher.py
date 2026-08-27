"""Unit tests for BcryptPasswordHasher."""

from admirable.infrastructure.security.password_hasher import BcryptPasswordHasher


def test_hash_generates_valid_bcrypt_string() -> None:
    hasher = BcryptPasswordHasher(rounds=12)
    hashed = hasher.hash("secure-password-123")
    assert hashed.startswith("$2b$12$")
    assert hasher.verify("secure-password-123", hashed) is True


def test_verify_rejects_incorrect_password() -> None:
    hasher = BcryptPasswordHasher()
    hashed = hasher.hash("correct-password")
    assert hasher.verify("wrong-password", hashed) is False


def test_needs_rehash_returns_false_when_cost_matches() -> None:
    hasher = BcryptPasswordHasher(rounds=12)
    hashed = hasher.hash("my-password")
    assert hasher.needs_rehash(hashed) is False


def test_needs_rehash_returns_true_when_cost_differs() -> None:
    hasher_12 = BcryptPasswordHasher(rounds=12)
    hashed = hasher_12.hash("my-password")

    hasher_14 = BcryptPasswordHasher(rounds=14)
    assert hasher_14.needs_rehash(hashed) is True


def test_malformed_hash_returns_false_without_raising() -> None:
    hasher = BcryptPasswordHasher()
    assert hasher.verify("password", "invalid-hash-string") is False
    assert hasher.verify("password", "") is False
