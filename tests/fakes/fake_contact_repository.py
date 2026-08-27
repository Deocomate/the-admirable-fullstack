from admirable.domain.entities.contact import Contact
from admirable.domain.value_objects.pagination import Page


class FakeContactRepository:
    def __init__(self) -> None:
        self._items: dict[int, Contact] = {}
        self._next_id = 1

    async def get_by_id(self, contact_id: int) -> Contact | None:
        return self._items.get(contact_id)

    async def list_paginated(self, page: int, per_page: int) -> Page[Contact]:
        items = sorted(self._items.values(), key=lambda c: c.sort_order)
        start = (page - 1) * per_page
        return Page(
            items=items[start : start + per_page], total=len(items), page=page, per_page=per_page
        )

    async def list_active_ordered(self) -> list[Contact]:
        items = [c for c in self._items.values() if c.is_active]
        return sorted(items, key=lambda c: c.sort_order)

    async def add(self, contact: Contact) -> Contact:
        contact.id = self._next_id
        self._next_id += 1
        self._items[contact.id] = contact
        return contact

    async def update(self, contact: Contact) -> Contact:
        assert contact.id is not None
        self._items[contact.id] = contact
        return contact

    async def delete(self, contact_id: int) -> None:
        self._items.pop(contact_id, None)
