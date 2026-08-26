from dataclasses import dataclass


@dataclass
class Category:
    id: int | None
    name: str
    slug: str
