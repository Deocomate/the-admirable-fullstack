"""Mirrors `SettingService::getDefaultAboutUsData()` / `array_replace_recursive`."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Hero:
    tagline: str = ""
    headline: str = ""
    headline_gradient: str = ""
    description: str = ""


@dataclass
class Stat:
    value: str = ""
    label: str = ""


@dataclass
class Problem:
    title: str = ""
    description: str = ""


@dataclass
class Solution:
    title: str = ""
    description: str = ""
    bullets: list[str] = field(default_factory=lambda: ["", "", ""])


@dataclass
class ValueItem:
    title: str = ""
    description: str = ""


@dataclass
class CoreValues:
    tagline: str = ""
    title: str = ""
    items: list[ValueItem] = field(default_factory=lambda: [ValueItem() for _ in range(4)])


@dataclass
class Audience:
    title: str = ""
    description: str = ""
    items: list[ValueItem] = field(default_factory=lambda: [ValueItem() for _ in range(3)])


@dataclass
class Cta:
    quote: str = ""
    headline: str = ""
    description: str = ""


@dataclass
class AboutUsContent:
    hero: Hero = field(default_factory=Hero)
    stats: list[Stat] = field(default_factory=lambda: [Stat() for _ in range(4)])
    problem: Problem = field(default_factory=Problem)
    solution: Solution = field(default_factory=Solution)
    core_values: CoreValues = field(default_factory=CoreValues)
    audience: Audience = field(default_factory=Audience)
    cta: Cta = field(default_factory=Cta)

    @classmethod
    def default(cls) -> AboutUsContent:
        return cls()

    @classmethod
    def merge(cls, raw: dict[str, object]) -> AboutUsContent:
        """Equivalent to `array_replace_recursive(default, raw)`: missing keys
        fall back to defaults, present keys (even partially) override them."""
        content = cls.default()
        if not raw:
            return content

        hero_raw = raw.get("hero")
        if isinstance(hero_raw, dict):
            content.hero = Hero(**{**content.hero.__dict__, **_str_only(hero_raw)})

        stats_raw = raw.get("stats")
        if isinstance(stats_raw, list):
            content.stats = [
                Stat(**{**Stat().__dict__, **_str_only(item)}) if isinstance(item, dict) else Stat()
                for item in stats_raw
            ] or content.stats

        problem_raw = raw.get("problem")
        if isinstance(problem_raw, dict):
            content.problem = Problem(**{**content.problem.__dict__, **_str_only(problem_raw)})

        solution_raw = raw.get("solution")
        if isinstance(solution_raw, dict):
            bullets = solution_raw.get("bullets")
            content.solution = Solution(
                title=str(solution_raw.get("title", content.solution.title)),
                description=str(solution_raw.get("description", content.solution.description)),
                bullets=(
                    [str(b) for b in bullets]
                    if isinstance(bullets, list)
                    else content.solution.bullets
                ),
            )

        core_values_raw = raw.get("core_values")
        if isinstance(core_values_raw, dict):
            items = core_values_raw.get("items")
            content.core_values = CoreValues(
                tagline=str(core_values_raw.get("tagline", content.core_values.tagline)),
                title=str(core_values_raw.get("title", content.core_values.title)),
                items=_merge_value_items(items, content.core_values.items),
            )

        audience_raw = raw.get("audience")
        if isinstance(audience_raw, dict):
            items = audience_raw.get("items")
            content.audience = Audience(
                title=str(audience_raw.get("title", content.audience.title)),
                description=str(audience_raw.get("description", content.audience.description)),
                items=_merge_value_items(items, content.audience.items),
            )

        cta_raw = raw.get("cta")
        if isinstance(cta_raw, dict):
            content.cta = Cta(**{**content.cta.__dict__, **_str_only(cta_raw)})

        return content


def _str_only(raw: dict[str, object]) -> dict[str, str]:
    return {k: str(v) for k, v in raw.items() if isinstance(v, str)}


def _merge_value_items(items_raw: object, defaults: list[ValueItem]) -> list[ValueItem]:
    if not isinstance(items_raw, list) or not items_raw:
        return defaults
    result: list[ValueItem] = []
    for i, default in enumerate(defaults):
        raw_item = items_raw[i] if i < len(items_raw) else None
        if isinstance(raw_item, dict):
            result.append(ValueItem(**{**default.__dict__, **_str_only(raw_item)}))
        else:
            result.append(default)
    return result
