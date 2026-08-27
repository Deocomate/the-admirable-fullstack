"""Proves Python's bcrypt library verifies Laravel-generated `$2y$` hashes.

Hash and plaintext are the real seeded superadmin account documented in
docs/superadmin_account.md (admin@gmail.com / Admin@123), confirmed against
the migrated dev database in Phase 3 — not a synthetic hash.
"""

from admirable.infrastructure.security.password_hasher import BcryptPasswordHasher

_REAL_LARAVEL_HASH = "$2y$12$XG6ci1jaSA5i0mNthFdDMOcJvriWLL3AgV0Y1Y6BICCO6oDeHVQNa"
_REAL_PLAINTEXT = "Admin@123"


def test_verifies_real_laravel_2y_hash() -> None:
    hasher = BcryptPasswordHasher()
    assert hasher.verify(_REAL_PLAINTEXT, _REAL_LARAVEL_HASH) is True


def test_rejects_wrong_password_against_real_hash() -> None:
    hasher = BcryptPasswordHasher()
    assert hasher.verify("wrong-password", _REAL_LARAVEL_HASH) is False


def test_needs_rehash_true_for_laravel_hash_with_matching_cost() -> None:
    # Laravel's default BCRYPT_ROUNDS=12 matches ours, so no rehash needed
    # purely on cost grounds.
    hasher = BcryptPasswordHasher(rounds=12)
    assert hasher.needs_rehash(_REAL_LARAVEL_HASH) is False


def test_needs_rehash_true_when_cost_differs() -> None:
    hasher = BcryptPasswordHasher(rounds=14)
    assert hasher.needs_rehash(_REAL_LARAVEL_HASH) is True


def test_new_hash_round_trips() -> None:
    hasher = BcryptPasswordHasher()
    new_hash = hasher.hash("some-new-password")
    assert new_hash.startswith("$2b$12$")
    assert hasher.verify("some-new-password", new_hash) is True
    assert hasher.needs_rehash(new_hash) is False


def test_malformed_hash_does_not_raise() -> None:
    hasher = BcryptPasswordHasher()
    assert hasher.verify("anything", "not-a-real-hash") is False
