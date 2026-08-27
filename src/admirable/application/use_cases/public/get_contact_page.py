from admirable.application.dto.contact_dto import ContactDTO
from admirable.application.dto.public_dto import ContactPageDTO
from admirable.domain.repositories.contact_repository import ContactRepository


class GetContactPage:
    def __init__(self, contacts: ContactRepository) -> None:
        self._contacts = contacts

    async def execute(self) -> ContactPageDTO:
        contacts = await self._contacts.list_active_ordered()
        return ContactPageDTO(contacts=[ContactDTO(**c.__dict__) for c in contacts])
