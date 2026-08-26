from dataclasses import dataclass


@dataclass
class Contact:
    id: int | None
    type: str
    label: str
    value: str
    icon: str | None
    sort_order: int
    is_active: bool
