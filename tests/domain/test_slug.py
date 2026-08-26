import pytest

from admirable.domain.exceptions import ValidationError
from admirable.domain.value_objects.slug import Slug


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("Marie Curie", "marie-curie"),
        ("Nguyễn Trãi", "nguyen-trai"),
        ("Hồ Chí Minh", "ho-chi-minh"),
        ("Đặng Thùy Trâm", "dang-thuy-tram"),
        ("  Extra   Spaces  ", "extra-spaces"),
    ],
)
def test_from_text(name: str, expected: str) -> None:
    assert Slug.from_text(name).value == expected


def test_invalid_slug_raises() -> None:
    with pytest.raises(ValidationError):
        Slug("Not A Valid Slug!")


def test_str_conversion() -> None:
    assert str(Slug("marie-curie")) == "marie-curie"
