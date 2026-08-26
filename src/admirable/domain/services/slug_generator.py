from collections.abc import Awaitable, Callable

from admirable.domain.value_objects.slug import Slug

_SlugExistsCheck = Callable[[str], Awaitable[bool]]


async def ensure_unique(base: Slug, exists: _SlugExistsCheck) -> Slug:
    """Append `-1`, `-2`, ... until a free slug is found (mirrors `FigureService::uniqueSlug`)."""
    candidate = base.value
    counter = 1
    while await exists(candidate):
        candidate = f"{base.value}-{counter}"
        counter += 1
    return Slug(candidate)
