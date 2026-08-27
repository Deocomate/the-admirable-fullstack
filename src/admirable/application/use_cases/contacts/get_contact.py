from admirable.application.dto.contact_dto import ContactDTO
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.contact_repository import ContactRepository


class GetContact:
    def __init__(self, contacts: ContactRepository) -> None:
        self._contacts = contacts

    async def execute(self, contact_id: int) -> ContactDTO:
        contact = await self._contacts.get_by_id(contact_id)
        if contact is None:
            raise EntityNotFoundError("Contact", contact_id)
        return ContactDTO(**contact.__dict__)
