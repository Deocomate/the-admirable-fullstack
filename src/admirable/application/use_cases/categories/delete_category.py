from admirable.domain.repositories.category_repository import CategoryRepository


class DeleteCategory:
    """Only detaches the category<->figure relation (via DB cascade on the
    join table's FK) — figures themselves are never deleted."""

    def __init__(self, categories: CategoryRepository) -> None:
        self._categories = categories

    async def execute(self, category_id: int) -> None:
        await self._categories.delete(category_id)
