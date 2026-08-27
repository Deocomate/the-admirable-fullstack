from typing import Any

from pydantic import BaseModel


class UpdateAboutUsCommand(BaseModel):
    data: dict[str, Any]


class AboutUsDTO(BaseModel):
    data: dict[str, Any]
