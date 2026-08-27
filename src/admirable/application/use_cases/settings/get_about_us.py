import json

from admirable.application.dto.settings_dto import AboutUsDTO
from admirable.domain.repositories.setting_repository import SettingRepository
from admirable.domain.value_objects.about_us_content import AboutUsContent

_KEY = "about_us_data"


class GetAboutUs:
    def __init__(self, settings: SettingRepository) -> None:
        self._settings = settings

    async def execute(self) -> AboutUsDTO:
        raw = await self._settings.get(_KEY)
        parsed = json.loads(raw) if raw else {}
        content = AboutUsContent.merge(parsed)
        return AboutUsDTO(data=_content_to_dict(content))


def _content_to_dict(content: AboutUsContent) -> dict[str, object]:
    return {
        "hero": content.hero.__dict__,
        "stats": [s.__dict__ for s in content.stats],
        "problem": content.problem.__dict__,
        "solution": content.solution.__dict__,
        "core_values": {
            "tagline": content.core_values.tagline,
            "title": content.core_values.title,
            "items": [i.__dict__ for i in content.core_values.items],
        },
        "audience": {
            "title": content.audience.title,
            "description": content.audience.description,
            "items": [i.__dict__ for i in content.audience.items],
        },
        "cta": content.cta.__dict__,
    }
