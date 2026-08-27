from admirable.domain.entities.contact import Contact
from admirable.infrastructure.db.models.contact import ContactModel


def to_entity(model: ContactModel) -> Contact:
    return Contact(
        id=model.id,
        type=model.type,
        label=model.label,
        value=model.value,
        icon=model.icon,
        sort_order=model.sort_order,
        is_active=model.is_active,
    )


def apply_to_model(entity: Contact, model: ContactModel) -> None:
    model.type = entity.type
    model.label = entity.label
    model.value = entity.value
    model.icon = entity.icon
    model.sort_order = entity.sort_order
    model.is_active = entity.is_active
