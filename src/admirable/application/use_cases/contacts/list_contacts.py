from pydantic import BaseModel

from admirable.application.dto.contact_dto import ContactDTO
from admirable.domain.repositories.contact_repository import ContactRepository


class ListContactsQuery(BaseModel):
    page: int = 1
    per_page: int = 15


class ListContactsResult(BaseModel):
    items: list[ContactDTO]
    total: int
    page: int
    per_page: int


class ListContacts:
    def __init__(self, contacts: ContactRepository) -> None:
        self._contacts = contacts

    async def execute(self, query: ListContactsQuery) -> ListContactsResult:
        page = await self._contacts.list_paginated(query.page, query.per_page)
        items = [ContactDTO(**c.__dict__) for c in page.items]
        return ListContactsResult(
            items=items, total=page.total, page=page.page, per_page=page.per_page
        )
