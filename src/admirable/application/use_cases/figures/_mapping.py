"""Shared DTO<->domain conversion helpers for the figures use case group."""

from admirable.application.dto.figure_dto import ContentBlockInput, FigureDetailDTO, KeyFactInput
from admirable.domain.entities.figure import Figure
from admirable.domain.value_objects.content_block import (
    ContentBlock,
    HeadingBlock,
    ParagraphBlock,
    QuoteBlock,
)


def to_domain_blocks(raw: list[ContentBlockInput]) -> list[ContentBlock]:
    result: list[ContentBlock] = []
    for block in raw:
        text_en = block.text_en.strip()
        if not text_en:
            continue
        if block.type == "heading":
            result.append(HeadingBlock(text_en=text_en))
        elif block.type == "paragraph":
            result.append(
                ParagraphBlock(text_en=text_en, text_vi=block.text_vi, heading_en=block.heading_en)
            )
        elif block.type == "quote":
            result.append(QuoteBlock(text_en=text_en, author=block.author))
    return result


def to_dto_blocks(blocks: list[ContentBlock]) -> list[ContentBlockInput]:
    result: list[ContentBlockInput] = []
    for block in blocks:
        if isinstance(block, HeadingBlock):
            result.append(ContentBlockInput(type="heading", text_en=block.text_en))
        elif isinstance(block, ParagraphBlock):
            result.append(
                ContentBlockInput(
                    type="paragraph",
                    text_en=block.text_en,
                    text_vi=block.text_vi,
                    heading_en=block.heading_en,
                )
            )
        elif isinstance(block, QuoteBlock):
            result.append(
                ContentBlockInput(type="quote", text_en=block.text_en, author=block.author)
            )
    return result


def to_figure_detail_dto(figure: Figure, category_names: list[str]) -> FigureDetailDTO:
    assert figure.id is not None
    return FigureDetailDTO(
        id=figure.id,
        name=figure.name,
        slug=figure.slug,
        avatar_path=figure.avatar_path,
        short_description=figure.short_description,
        key_facts=[KeyFactInput(label=f.label, value=f.value) for f in figure.key_facts],
        content_blocks=to_dto_blocks(figure.content_blocks),
        audio_path=figure.audio_path,
        audio_status=figure.audio_status,
        audio_error=figure.audio_error,
        youtube_url=figure.youtube_url,
        category_ids=figure.category_ids,
        category_names=category_names,
    )
