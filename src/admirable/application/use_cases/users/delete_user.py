from admirable.domain.entities.user import User
from admirable.domain.exceptions import EntityNotFoundError
from admirable.domain.repositories.user_repository import UserRepository


class DeleteUser:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def execute(self, user_id: int, actor: User) -> None:
        target = await self._users.get_by_id(user_id)
        if target is None:
            raise EntityNotFoundError("User", user_id)
        superadmin_count = await self._users.count_superadmins()
        target.can_be_deleted_by(actor, superadmin_count)
        await self._users.delete(user_id)
