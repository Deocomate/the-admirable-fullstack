from dataclasses import dataclass


@dataclass
class Setting:
    key: str
    value: str | None
