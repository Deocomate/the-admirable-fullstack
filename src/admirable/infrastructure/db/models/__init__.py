"""Import every model so `Base.metadata` is fully populated for Alembic autogenerate/check."""

from admirable.infrastructure.db.models.associations import category_figure_table
from admirable.infrastructure.db.models.category import CategoryModel
from admirable.infrastructure.db.models.contact import ContactModel
from admirable.infrastructure.db.models.featured_figure import FeaturedFigureModel
from admirable.infrastructure.db.models.figure import FigureModel
from admirable.infrastructure.db.models.setting import SettingModel
from admirable.infrastructure.db.models.story_snippet import StorySnippetModel
from admirable.infrastructure.db.models.user import UserModel

__all__ = [
    "CategoryModel",
    "ContactModel",
    "FeaturedFigureModel",
    "FigureModel",
    "SettingModel",
    "StorySnippetModel",
    "UserModel",
    "category_figure_table",
]
