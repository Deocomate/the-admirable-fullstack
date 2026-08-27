from sqlalchemy.ext.asyncio import AsyncSession

from admirable.infrastructure.db.repositories.setting_repository_impl import SettingRepositoryImpl


async def test_set_and_get(db_session: AsyncSession) -> None:
    repo = SettingRepositoryImpl(db_session)
    assert await repo.get("nonexistent_key_it") is None

    await repo.set("about_us_data_it", '{"hero": {"tagline": "x"}}')
    assert await repo.get("about_us_data_it") == '{"hero": {"tagline": "x"}}'

    await repo.set("about_us_data_it", '{"hero": {"tagline": "y"}}')
    assert await repo.get("about_us_data_it") == '{"hero": {"tagline": "y"}}'
