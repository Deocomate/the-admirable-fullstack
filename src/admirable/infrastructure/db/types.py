"""Custom column types bridging JSON storage and domain value objects."""

from typing import Any

from sqlalchemy import JSON
from sqlalchemy.types import TypeDecorator

from admirable.domain.value_objects.content_block import (
    ContentBlock,
    parse_content_blocks,
    serialize_content_blocks,
)
from admirable.domain.value_objects.key_fact import KeyFact, parse_key_facts, serialize_key_facts


class ContentBlocksType(TypeDecorator[list[ContentBlock]]):
    impl = JSON
    cache_ok = True

    def process_bind_param(
        self, value: list[ContentBlock] | None, dialect: Any
    ) -> list[dict[str, object]] | None:
        if value is None:
            return None
        return serialize_content_blocks(value)

    def process_result_value(
        self, value: list[dict[str, object]] | None, dialect: Any
    ) -> list[ContentBlock] | None:
        if value is None:
            return None
        return parse_content_blocks(value)


class KeyFactsType(TypeDecorator[list[KeyFact]]):
    impl = JSON
    cache_ok = True

    def process_bind_param(
        self, value: list[KeyFact] | None, dialect: Any
    ) -> list[dict[str, object]] | None:
        if value is None:
            return None
        return serialize_key_facts(value)

    def process_result_value(
        self, value: list[dict[str, object]] | None, dialect: Any
    ) -> list[KeyFact] | None:
        if value is None:
            return None
        return parse_key_facts(value)
