import json

from admirable.application.dto.settings_dto import UpdateAboutUsCommand
from admirable.domain.repositories.setting_repository import SettingRepository

_KEY = "about_us_data"


class UpdateAboutUs:
    def __init__(self, settings: SettingRepository) -> None:
        self._settings = settings

    async def execute(self, cmd: UpdateAboutUsCommand) -> None:
        await self._settings.set(_KEY, json.dumps(cmd.data, ensure_ascii=False))
