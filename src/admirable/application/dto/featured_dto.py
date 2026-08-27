from pydantic import BaseModel


class FeaturedFigureDTO(BaseModel):
    id: int
    figure_id: int
    figure_name: str
    figure_slug: str
    figure_avatar_path: str | None
    priority: int
