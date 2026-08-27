from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.contact import Contact
from admirable.infrastructure.db.repositories.contact_repository_impl import ContactRepositoryImpl


async def test_active_ordered(db_session: AsyncSession) -> None:
    repo = ContactRepositoryImpl(db_session)
    await repo.add(
        Contact(
            id=None, type="email", label="Email IT", value="a@b.com",
            icon=None, sort_order=1, is_active=True,
        )
    )
    await repo.add(
        Contact(
            id=None, type="phone", label="Phone IT", value="123",
            icon=None, sort_order=0, is_active=True,
        )
    )
    await repo.add(
        Contact(
            id=None, type="fax", label="Fax IT (inactive)", value="000",
            icon=None, sort_order=2, is_active=False,
        )
    )

    active = await repo.list_active_ordered()
    labels = [c.label for c in active if c.label.endswith("IT") or "IT (inactive)" in c.label]
    assert "Fax IT (inactive)" not in [c.label for c in active]
    assert labels[0] == "Phone IT"  # sort_order 0 before 1
