from admirable.application.dto.contact_dto import ContactDTO, UpdateContactCommand
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.contact_repository import ContactRepository


class UpdateContact:
    def __init__(self, contacts: ContactRepository) -> None:
        self._contacts = contacts

    async def execute(self, cmd: UpdateContactCommand) -> ContactDTO:
        contact = await self._contacts.get_by_id(cmd.contact_id)
        if contact is None:
            raise EntityNotFoundError("Contact", cmd.contact_id)
        contact.type = cmd.type
        contact.label = cmd.label
        contact.value = cmd.value
        contact.icon = cmd.icon
        contact.sort_order = cmd.sort_order
        contact.is_active = cmd.is_active
        updated = await self._contacts.update(contact)
        return ContactDTO(**updated.__dict__)
