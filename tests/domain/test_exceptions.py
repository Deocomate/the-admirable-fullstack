from admirable.domain.exceptions import DuplicateSlugError, EntityNotFoundError


def test_entity_not_found_error_message() -> None:
    error = EntityNotFoundError("Figure", 42)
    assert error.entity == "Figure"
    assert error.identifier == 42
    assert "Figure" in str(error)


def test_duplicate_slug_error_message() -> None:
    error = DuplicateSlugError("marie-curie")
    assert error.slug == "marie-curie"
    assert "marie-curie" in str(error)
