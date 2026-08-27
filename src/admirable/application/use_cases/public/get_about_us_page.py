from admirable.application.dto.settings_dto import AboutUsDTO
from admirable.application.use_cases.settings.get_about_us import GetAboutUs
from admirable.domain.repositories.setting_repository import SettingRepository


class GetAboutUsPage:
    def __init__(self, settings: SettingRepository) -> None:
        self._get_about_us = GetAboutUs(settings)

    async def execute(self) -> AboutUsDTO:
        return await self._get_about_us.execute()
