from admirable.domain.entities.category import Category
from admirable.infrastructure.db.models.category import CategoryModel


def to_entity(model: CategoryModel) -> Category:
    return Category(id=model.id, name=model.name, slug=model.slug, created_at=model.created_at)


def apply_to_model(entity: Category, model: CategoryModel) -> None:
    model.name = entity.name
    model.slug = entity.slug
