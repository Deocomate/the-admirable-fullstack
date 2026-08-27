from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.contact import Contact
from admirable.domain.value_objects.pagination import Page
from admirable.infrastructure.db.mappers import contact_mapper
from admirable.infrastructure.db.models.contact import ContactModel


class ContactRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, contact_id: int) -> Contact | None:
        model = await self._session.get(ContactModel, contact_id)
        return contact_mapper.to_entity(model) if model else None

    async def list_paginated(self, page: int, per_page: int) -> Page[Contact]:
        count_stmt = select(func.count()).select_from(ContactModel)
        stmt = (
            select(ContactModel)
            .order_by(ContactModel.sort_order, ContactModel.created_at.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        total = (await self._session.execute(count_stmt)).scalar_one()
        models = (await self._session.execute(stmt)).scalars().all()
        items = [contact_mapper.to_entity(m) for m in models]
        return Page(items=items, total=total, page=page, per_page=per_page)

    async def list_active_ordered(self) -> list[Contact]:
        stmt = (
            select(ContactModel)
            .where(ContactModel.is_active.is_(True))
            .order_by(ContactModel.sort_order)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [contact_mapper.to_entity(m) for m in models]

    async def add(self, contact: Contact) -> Contact:
        model = ContactModel()
        contact_mapper.apply_to_model(contact, model)
        self._session.add(model)
        await self._session.flush()
        return contact_mapper.to_entity(model)

    async def update(self, contact: Contact) -> Contact:
        model = await self._session.get(ContactModel, contact.id)
        if model is None:
            raise ValueError(f"Contact {contact.id} not found")
        contact_mapper.apply_to_model(contact, model)
        await self._session.flush()
        return contact_mapper.to_entity(model)

    async def delete(self, contact_id: int) -> None:
        model = await self._session.get(ContactModel, contact_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()
