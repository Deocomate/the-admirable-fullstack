from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.infrastructure.db.models.featured_figure import FeaturedFigureModel


def to_entity(model: FeaturedFigureModel) -> FeaturedFigure:
    return FeaturedFigure(id=model.id, figure_id=model.figure_id, priority=model.priority)


def apply_to_model(entity: FeaturedFigure, model: FeaturedFigureModel) -> None:
    model.figure_id = entity.figure_id
    model.priority = entity.priority
