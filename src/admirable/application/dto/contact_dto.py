from pydantic import BaseModel


class CreateContactCommand(BaseModel):
    type: str
    label: str
    value: str
    icon: str | None = None
    sort_order: int = 0
    is_active: bool = True


class UpdateContactCommand(BaseModel):
    contact_id: int
    type: str
    label: str
    value: str
    icon: str | None = None
    sort_order: int = 0
    is_active: bool = True


class ContactDTO(BaseModel):
    id: int
    type: str
    label: str
    value: str
    icon: str | None
    sort_order: int
    is_active: bool
