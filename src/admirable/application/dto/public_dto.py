from pydantic import BaseModel

from admirable.application.dto.category_dto import CategoryDTO
from admirable.application.dto.contact_dto import ContactDTO
from admirable.application.dto.figure_dto import FigureSummaryDTO
from admirable.application.dto.story_dto import StoryDetailDTO


class HomeStatsDTO(BaseModel):
    figures: int
    categories: int
    stories: int


class HomePageDTO(BaseModel):
    categories: list[CategoryDTO]
    featured_figure: FigureSummaryDTO | None
    latest_figures: list[FigureSummaryDTO]
    stats: HomeStatsDTO


class SearchResultsDTO(BaseModel):
    query: str
    category_slug: str | None
    categories: list[CategoryDTO]
    figures: list[FigureSummaryDTO]
    total: int
    page: int
    per_page: int
    trending_figures: list[FigureSummaryDTO]


class FigureDetailPageDTO(BaseModel):
    id: int
    name: str
    slug: str
    avatar_path: str | None
    short_description: str | None
    key_facts: list[dict[str, str]]
    content_blocks: list[dict[str, object]]
    audio_path: str | None
    youtube_url: str | None
    category_names: list[str]
    story_snippets: list[StorySummaryLite]
    related_figures: list[FigureSummaryDTO]


class StorySummaryLite(BaseModel):
    id: int
    title: str
    subtitle: str | None
    image_path: str | None


class CategoryPageDTO(BaseModel):
    categories: list[CategoryDTO]
    category: CategoryDTO | None
    featured_figure: FigureSummaryDTO | None
    figures: list[FigureSummaryDTO]
    total: int
    page: int
    per_page: int


class ContactPageDTO(BaseModel):
    contacts: list[ContactDTO]


class StoryDetailPageDTO(BaseModel):
    snippet: StoryDetailDTO
    other_stories: list[StorySummaryLite]
