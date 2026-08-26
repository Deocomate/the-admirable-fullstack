from admirable.domain.value_objects.pagination import Page


def test_last_page_rounds_up() -> None:
    page: Page[int] = Page(items=[1, 2, 3], total=25, page=1, per_page=10)
    assert page.last_page == 3


def test_has_prev_and_has_next() -> None:
    page: Page[int] = Page(items=[], total=25, page=2, per_page=10)
    assert page.has_prev is True
    assert page.has_next is True

    first: Page[int] = Page(items=[], total=25, page=1, per_page=10)
    assert first.has_prev is False

    last: Page[int] = Page(items=[], total=25, page=3, per_page=10)
    assert last.has_next is False


def test_window_centers_on_current_page() -> None:
    page: Page[int] = Page(items=[], total=200, page=10, per_page=10)
    window = page.window(size=5)
    assert len(window) == 5
    assert 10 in window


def test_window_clamped_at_start() -> None:
    page: Page[int] = Page(items=[], total=200, page=1, per_page=10)
    window = page.window(size=5)
    assert window == [1, 2, 3, 4, 5]


def test_window_clamped_at_end() -> None:
    page: Page[int] = Page(items=[], total=50, page=5, per_page=10)
    window = page.window(size=5)
    assert window == [1, 2, 3, 4, 5]
