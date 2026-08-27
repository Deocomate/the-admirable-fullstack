"""Ports `StoreContactRequest`/`UpdateContactRequest` (identical rules on
both, matching the Laravel source)."""

from pydantic import BaseModel, Field

CONTACT_FIELD_LABELS = {
    "type": "Loại liên hệ",
    "label": "Nhãn hiển thị",
    "value": "Giá trị liên hệ",
}


class ContactForm(BaseModel):
    type: str = Field(min_length=1, max_length=50)
    label: str = Field(min_length=1, max_length=255)
    value: str = Field(min_length=1, max_length=500)
    icon: str | None = Field(default=None, max_length=100)
    sort_order: int = Field(default=0, ge=0)
    is_active: bool = True
