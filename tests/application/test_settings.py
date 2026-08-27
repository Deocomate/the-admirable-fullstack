from admirable.application.dto.settings_dto import UpdateAboutUsCommand
from admirable.application.use_cases.settings.get_about_us import GetAboutUs
from admirable.application.use_cases.settings.update_about_us import UpdateAboutUs
from tests.fakes.fake_setting_repository import FakeSettingRepository


async def test_get_about_us_returns_default_when_unset() -> None:
    settings = FakeSettingRepository()
    result = await GetAboutUs(settings).execute()
    assert result.data["hero"]["tagline"] == ""
    assert len(result.data["stats"]) == 4


async def test_update_then_get_about_us_merges_with_default() -> None:
    settings = FakeSettingRepository()
    await UpdateAboutUs(settings).execute(
        UpdateAboutUsCommand(data={"hero": {"tagline": "Cà phê ☕"}})
    )
    result = await GetAboutUs(settings).execute()
    assert result.data["hero"]["tagline"] == "Cà phê ☕"
    assert result.data["hero"]["headline"] == ""  # untouched fields keep defaults


async def test_update_about_us_preserves_unicode_in_storage() -> None:
    settings = FakeSettingRepository()
    await UpdateAboutUs(settings).execute(UpdateAboutUsCommand(data={"hero": {"tagline": "Việt"}}))
    raw = await settings.get("about_us_data")
    assert raw is not None
    assert "\\u" not in raw  # ensure_ascii=False keeps Vietnamese literal
    assert "Việt" in raw
