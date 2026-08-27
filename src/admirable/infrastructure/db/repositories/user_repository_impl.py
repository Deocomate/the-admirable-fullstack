from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.domain.entities.user import User
from admirable.domain.value_objects.role import Role
from admirable.infrastructure.db.mappers import user_mapper
from admirable.infrastructure.db.models.user import UserModel


class UserRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        model = await self._session.get(UserModel, user_id)
        return user_mapper.to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return user_mapper.to_entity(model) if model else None

    async def list_all_admins(self, page: int, per_page: int) -> list[User]:
        stmt = (
            select(UserModel)
            .order_by(UserModel.created_at.desc())
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [user_mapper.to_entity(m) for m in models]

    async def count_superadmins(self) -> int:
        stmt = select(func.count()).select_from(UserModel).where(UserModel.role == Role.SUPERADMIN)
        return (await self._session.execute(stmt)).scalar_one()

    async def add(self, user: User) -> User:
        model = UserModel()
        user_mapper.apply_to_model(user, model)
        self._session.add(model)
        await self._session.flush()
        return user_mapper.to_entity(model)

    async def update(self, user: User) -> User:
        model = await self._session.get(UserModel, user.id)
        if model is None:
            raise ValueError(f"User {user.id} not found")
        user_mapper.apply_to_model(user, model)
        await self._session.flush()
        return user_mapper.to_entity(model)

    async def delete(self, user_id: int) -> None:
        model = await self._session.get(UserModel, user_id)
        if model is not None:
            await self._session.delete(model)
            await self._session.flush()
