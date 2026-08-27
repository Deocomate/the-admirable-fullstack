from admirable.application.dto.contact_dto import CreateContactCommand, UpdateContactCommand
from admirable.application.use_cases.contacts.create_contact import CreateContact
from admirable.application.use_cases.contacts.delete_contact import DeleteContact
from admirable.application.use_cases.contacts.get_contact import GetContact
from admirable.application.use_cases.contacts.list_contacts import ListContacts, ListContactsQuery
from admirable.application.use_cases.contacts.update_contact import UpdateContact
from tests.fakes.fake_contact_repository import FakeContactRepository


async def test_create_get_update_delete_contact() -> None:
    contacts = FakeContactRepository()
    created = await CreateContact(contacts).execute(
        CreateContactCommand(type="email", label="Email", value="a@b.com")
    )
    assert created.id is not None

    fetched = await GetContact(contacts).execute(created.id)
    assert fetched.value == "a@b.com"

    updated = await UpdateContact(contacts).execute(
        UpdateContactCommand(contact_id=created.id, type="email", label="Email 2", value="c@d.com")
    )
    assert updated.label == "Email 2"

    await DeleteContact(contacts).execute(created.id)
    assert await contacts.get_by_id(created.id) is None


async def test_list_contacts() -> None:
    contacts = FakeContactRepository()
    await CreateContact(contacts).execute(CreateContactCommand(type="email", label="A", value="a"))
    await CreateContact(contacts).execute(CreateContactCommand(type="phone", label="B", value="b"))
    result = await ListContacts(contacts).execute(ListContactsQuery(page=1, per_page=15))
    assert result.total == 2
