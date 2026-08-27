from admirable.application.dto.figure_dto import CreateFigureCommand, UpdateFigureCommand
from admirable.application.use_cases.figures.create_figure import CreateFigure
from admirable.application.use_cases.figures.update_figure import UpdateFigure
from tests.fakes.fake_figure_repository import FakeFigureRepository
from tests.fakes.fake_file_storage import FakeFileStorage


async def test_slug_unchanged_when_name_unchanged() -> None:
    figures = FakeFigureRepository()
    storage = FakeFileStorage()
    created = await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Marie Curie"))
    original_slug = created.slug

    result = await UpdateFigure(figures, storage).execute(
        UpdateFigureCommand(
            figure_id=created.id,
            name="Marie Curie",  # same name
            short_description="Updated bio",
        )
    )

    assert result.slug == original_slug


async def test_slug_regenerated_when_name_changes() -> None:
    figures = FakeFigureRepository()
    storage = FakeFileStorage()
    created = await CreateFigure(figures, storage).execute(CreateFigureCommand(name="Marie Curie"))

    result = await UpdateFigure(figures, storage).execute(
        UpdateFigureCommand(figure_id=created.id, name="Marie Sklodowska Curie")
    )

    assert result.slug == "marie-sklodowska-curie"
    assert result.slug != created.slug
