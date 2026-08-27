from admirable.domain.repositories.contact_repository import ContactRepository


class DeleteContact:
    def __init__(self, contacts: ContactRepository) -> None:
        self._contacts = contacts

    async def execute(self, contact_id: int) -> None:
        await self._contacts.delete(contact_id)
