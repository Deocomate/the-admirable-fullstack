from dataclasses import dataclass


@dataclass(frozen=True)
class KeyFact:
    label: str
    value: str


def parse_key_facts(raw: list[dict[str, object]]) -> list[KeyFact]:
    """Drop entries with a blank label or value (mirrors `normalizeKeyFacts`)."""
    facts: list[KeyFact] = []
    for entry in raw:
        label = str(entry.get("label") or "").strip()
        value = str(entry.get("value") or "").strip()
        if label and value:
            facts.append(KeyFact(label=label, value=value))
    return facts


def serialize_key_facts(facts: list[KeyFact]) -> list[dict[str, object]]:
    return [{"label": f.label, "value": f.value} for f in facts]
