from admirable.domain.value_objects.about_us_content import AboutUsContent


def test_default_has_empty_strings() -> None:
    content = AboutUsContent.default()
    assert content.hero.tagline == ""
    assert len(content.stats) == 4
    assert len(content.core_values.items) == 4
    assert len(content.audience.items) == 3


def test_merge_with_empty_dict_returns_default() -> None:
    content = AboutUsContent.merge({})
    assert content == AboutUsContent.default()


def test_merge_partial_hero_keeps_other_fields_default() -> None:
    content = AboutUsContent.merge({"hero": {"tagline": "New tagline"}})
    assert content.hero.tagline == "New tagline"
    assert content.hero.headline == ""
    assert len(content.stats) == 4


def test_merge_solution_bullets() -> None:
    content = AboutUsContent.merge({"solution": {"bullets": ["a", "b", "c"]}})
    assert content.solution.bullets == ["a", "b", "c"]


def test_merge_core_values_items_partial() -> None:
    content = AboutUsContent.merge({"core_values": {"items": [{"title": "First"}]}})
    assert content.core_values.items[0].title == "First"
    assert len(content.core_values.items) == 4
    assert content.core_values.items[1].title == ""


def test_merge_stats() -> None:
    content = AboutUsContent.merge({"stats": [{"value": "10", "label": "Years"}]})
    assert content.stats[0].value == "10"


def test_merge_stats_partial_keeps_fixed_length() -> None:
    """A form editing only the first of 4 stat cards must not truncate the
    other 3 — matches PHP's `array_replace_recursive`, not a wholesale
    list replace."""
    content = AboutUsContent.merge({"stats": [{"value": "10", "label": "Years"}]})
    assert len(content.stats) == 4
    assert content.stats[1].value == ""
    assert content.stats[1].label == ""


def test_merge_solution_bullets_partial_keeps_fixed_length() -> None:
    content = AboutUsContent.merge({"solution": {"bullets": ["only one"]}})
    assert len(content.solution.bullets) == 3
    assert content.solution.bullets[0] == "only one"
    assert content.solution.bullets[1] == ""


def test_merge_problem_and_cta() -> None:
    content = AboutUsContent.merge({"problem": {"title": "Problem"}, "cta": {"quote": "Quote"}})
    assert content.problem.title == "Problem"
    assert content.cta.quote == "Quote"


def test_merge_audience_items() -> None:
    content = AboutUsContent.merge({"audience": {"items": [{"title": "Devs"}]}})
    assert content.audience.items[0].title == "Devs"
    assert len(content.audience.items) == 3


def test_merge_ignores_non_dict_sections() -> None:
    content = AboutUsContent.merge({"hero": "not-a-dict", "stats": "not-a-list"})
    assert content == AboutUsContent.default()
