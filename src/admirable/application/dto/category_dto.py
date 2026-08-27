from datetime import datetime

from pydantic import BaseModel


class CreateCategoryCommand(BaseModel):
    name: str


class UpdateCategoryCommand(BaseModel):
    category_id: int
    name: str


class CategoryDTO(BaseModel):
    id: int
    name: str
    slug: str
    figures_count: int = 0
    created_at: datetime | None = None
