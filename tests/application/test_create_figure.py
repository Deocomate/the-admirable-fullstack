from admirable.application.dto.figure_dto import ContentBlockInput, CreateFigureCommand
from admirable.application.use_cases.figures.create_figure import CreateFigure
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage


async def test_create_figure_generates_slug_and_search_text() -> None:
    figures = FakeFigureRepository()
    storage = FakeFileStorage()
    use_case = CreateFigure(figures, storage)

    result = await use_case.execute(
        CreateFigureCommand(
            name="Marie Curie",
            content_blocks=[ContentBlockInput(type="heading", text_en="Early life")],
        )
    )

    assert result.slug == "marie-curie"
    stored = await figures.get_by_id(result.id)
    assert stored is not None
    assert stored.search_text == "Early life"


async def test_create_figure_dedupes_slug() -> None:
    figures = FakeFigureRepository()
    storage = FakeFileStorage()
    use_case = CreateFigure(figures, storage)

    await use_case.execute(CreateFigureCommand(name="Marie Curie"))
    second = await use_case.execute(CreateFigureCommand(name="Marie Curie"))

    assert second.slug == "marie-curie-1"
