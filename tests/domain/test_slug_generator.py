from admirable.domain.services.slug_generator import ensure_unique
from admirable.domain.value_objects.slug import Slug


async def test_returns_base_when_free() -> None:
    async def exists(_: str) -> bool:
        return False

    result = await ensure_unique(Slug("marie-curie"), exists)
    assert result.value == "marie-curie"


async def test_appends_counter_until_free() -> None:
    taken = {"marie-curie", "marie-curie-1", "marie-curie-2"}

    async def exists(candidate: str) -> bool:
        return candidate in taken

    result = await ensure_unique(Slug("marie-curie"), exists)
    assert result.value == "marie-curie-3"
