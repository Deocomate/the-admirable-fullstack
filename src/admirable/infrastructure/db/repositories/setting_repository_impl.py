from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.ext.asyncio import AsyncSession

from admirable.infrastructure.clock import SystemClock
from admirable.infrastructure.db.models.setting import SettingModel


class SettingRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._clock = SystemClock()

    async def get(self, key: str) -> str | None:
        model = await self._session.get(SettingModel, key)
        return model.value if model else None

    async def set(self, key: str, value: str | None) -> None:
        now = self._clock.now()
        stmt = mysql_insert(SettingModel).values(
            key=key, value=value, created_at=now, updated_at=now
        )
        stmt = stmt.on_duplicate_key_update(value=stmt.inserted.value, updated_at=now)
        await self._session.execute(stmt)
        await self._session.flush()
