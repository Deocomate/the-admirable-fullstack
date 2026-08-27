from admirable.application.dto.contact_dto import ContactDTO, CreateContactCommand
from admirable.domain.entities.contact import Contact
from admirable.domain.repositories.contact_repository import ContactRepository


class CreateContact:
    def __init__(self, contacts: ContactRepository) -> None:
        self._contacts = contacts

    async def execute(self, cmd: CreateContactCommand) -> ContactDTO:
        contact = Contact(
            id=None,
            type=cmd.type,
            label=cmd.label,
            value=cmd.value,
            icon=cmd.icon,
            sort_order=cmd.sort_order,
            is_active=cmd.is_active,
        )
        created = await self._contacts.add(contact)
        return ContactDTO(**created.__dict__)
