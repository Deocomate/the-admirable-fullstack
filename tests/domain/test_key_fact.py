from admirable.domain.value_objects.key_fact import parse_key_facts, serialize_key_facts


def test_filters_blank_label_or_value() -> None:
    raw: list[dict[str, object]] = [
        {"label": "Born", "value": "1867"},
        {"label": "  ", "value": "1934"},
        {"label": "Died", "value": "  "},
    ]
    facts = parse_key_facts(raw)
    assert len(facts) == 1
    assert facts[0].label == "Born"


def test_serialize_round_trip() -> None:
    facts = parse_key_facts([{"label": "Born", "value": "1867"}])
    assert serialize_key_facts(facts) == [{"label": "Born", "value": "1867"}]
