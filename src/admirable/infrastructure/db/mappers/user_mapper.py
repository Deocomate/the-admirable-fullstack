from admirable.domain.entities.user import User
from admirable.infrastructure.db.models.user import UserModel


def to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        name=model.name,
        email=model.email,
        password_hash=model.password,
        role=model.role,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def apply_to_model(entity: User, model: UserModel) -> None:
    model.name = entity.name
    model.email = entity.email
    model.password = entity.password_hash
    model.role = entity.role
