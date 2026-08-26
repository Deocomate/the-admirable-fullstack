from admirable.domain.entities.category import Category
from admirable.domain.entities.contact import Contact
from admirable.domain.entities.featured_figure import FeaturedFigure
from admirable.domain.entities.setting import Setting


def test_category() -> None:
    category = Category(id=1, name="Scientists", slug="scientists")
    assert category.slug == "scientists"


def test_contact() -> None:
    contact = Contact(
        id=1,
        type="email",
        label="Email",
        value="hi@admirable.site",
        icon="mail",
        sort_order=0,
        is_active=True,
    )
    assert contact.is_active is True


def test_featured_figure() -> None:
    featured = FeaturedFigure(id=1, figure_id=5, priority=0)
    assert featured.figure_id == 5


def test_setting() -> None:
    setting = Setting(key="about_us_data", value=None)
    assert setting.value is None
