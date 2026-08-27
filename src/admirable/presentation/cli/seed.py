"""Ports UserSeeder/CategorySeeder/ContactSeeder/SettingSeeder.

Usage: uv run python -m admirable.presentation.cli.seed
"""

import asyncio
import json

import typer

from admirable.config import get_settings
from admirable.domain.entities.category import Category
from admirable.domain.entities.contact import Contact
from admirable.domain.entities.user import User
from admirable.domain.value_objects.role import Role
from admirable.infrastructure.container import build_worker_scope

app = typer.Typer(add_completion=False)

_SUPERADMIN_EMAIL = "admin@gmail.com"
_SUPERADMIN_PASSWORD = "Admin@123"

_CATEGORIES = [
    ("Tội phạm & Pháp luật (Crime & Law)", "toi-pham-phap-luat-crime-law"),
    ("Môi trường (Environment)", "moi-truong-environment"),
    ("Lịch sử (History)", "lich-su-history"),
    ("Truyền thông (Media & Communication)", "truyen-thong-media-communication"),
    ("Sức khỏe & Y tế (Health & Medicine)", "suc-khoe-y-te-health-medicine"),
    ("Giáo dục (Education)", "giao-duc-education"),
    ("Chính trị", "chinh-tri"),
    ("Khoa học", "khoa-hoc"),
    ("Nghệ thuật", "nghe-thuat"),
    ("Kinh tế", "kinh-te"),
    ("Thể thao", "the-thao"),
    ("Công nghệ", "cong-nghe"),
    ("Văn hóa", "van-hoa"),
    ("Đời sống", "doi-song"),
]

_CONTACTS = [
    ("email", "Email", "longnvm2003@gmail.com", 1),
    ("phone", "Số điện thoại", "0865095066", 2),
    ("facebook", "Facebook", "https://facebook.com/", 3),
    ("github", "GitHub", "https://github.com/", 4),
    ("whatsapp", "WhatsApp", "https://wa.me/84865095066", 5),
]

_ABOUT_US_DATA = {
    "hero": {
        "tagline": "Câu chuyện của chúng tôi",
        "headline": "Học ngôn ngữ qua",
        "headline_gradient": "những tầm cao nhân loại.",
        "description": (
            '"The Admirable" ra đời mang theo một sứ mệnh: Biến quá trình học tiếng Anh đầy gian '
            "nan trở thành một hành trình tận hưởng những giá trị tốt đẹp nhất của tri thức."
        ),
    },
    "stats": [
        {"value": "50+", "label": "Nhân vật vĩ đại"},
        {"value": "8", "label": "Lĩnh vực đa dạng"},
        {"value": "200+", "label": "Bài đọc song ngữ"},
        {"value": "100%", "label": "Miễn phí, mãi mãi"},
    ],
    "problem": {
        "title": "Nỗi trăn trở của người học",
        "description": (
            "Chúng tôi thấu hiểu rằng việc học IELTS hay nâng cao vốn tiếng Anh thường đi kèm với "
            "những bài báo học thuật khô khan, phức tạp. Người học rất dễ cảm thấy chán nản, buồn "
            "ngủ và gặp khó khăn trong việc ghi nhớ từ vựng cũng như duy trì động lực mỗi ngày."
        ),
    },
    "solution": {
        "title": 'Giải pháp mang tên "The Admirable"',
        "description": (
            "Thay vì ép bản thân đọc những nội dung vô hồn, chúng tôi cung cấp các bài viết song "
            "ngữ chất lượng cao kể về những tấm gương vĩ đại trên toàn thế giới—từ văn hóa, kinh "
            "tế, khoa học đến chính trị."
        ),
        "bullets": [
            "Nội dung truyền cảm hứng, tích cực và sâu sắc.",
            "Hệ sinh thái đa phương tiện: Text, Audio, Video YouTube.",
            "Ghi nhớ từ vựng tự nhiên thông qua bối cảnh câu chuyện.",
        ],
    },
    "core_values": {
        "tagline": "Giá trị cốt lõi",
        "title": "Những gì chúng tôi tin tưởng",
        "items": [
            {
                "title": "Tri thức mở",
                "description": "Mọi nội dung đều miễn phí, không cần đăng ký, không paywall. Kiến thức là quyền của tất cả.",
            },
            {
                "title": "Chất lượng cao",
                "description": "Bài viết được biên soạn kỹ lưỡng, song ngữ chuẩn xác, đúng ngữ pháp và phù hợp IELTS.",
            },
            {
                "title": "Truyền cảm hứng",
                "description": "Nội dung tích cực, khơi dậy động lực học tập và tinh thần vươn lên từ các tấm gương.",
            },
            {
                "title": "Đa dạng lĩnh vực",
                "description": "Từ khoa học, chính trị, nghệ thuật đến thể thao — phủ sóng mọi góc nhìn về nhân loại.",
            },
        ],
    },
    "audience": {
        "title": "Nền tảng này dành cho ai?",
        "description": "Không cần tạo tài khoản rườm rà. Hệ thống được mở hoàn toàn công khai để mang tri thức đến với tất cả mọi người.",
        "items": [
            {
                "title": "Người học IELTS",
                "description": "Đắm chìm trong từ vựng cao cấp (Advanced Vocabulary) và cấu trúc câu phức tạp một cách tự nhiên qua các bài viết học thuật mang tính tiểu sử.",
            },
            {
                "title": "Người yêu tiếng Anh",
                "description": "Cải thiện cả hai kỹ năng Reading và Listening đồng thời thông qua các bài đọc song ngữ kèm giọng đọc audio chuẩn xác.",
            },
            {
                "title": "Người tìm cảm hứng",
                "description": "Dành cho bất cứ ai muốn tìm kiếm năng lượng tích cực, sự kiên cường và động lực từ những con người đã làm thay đổi thế giới.",
            },
        ],
    },
    "cta": {
        "quote": "Đọc là để sống nhiều hơn một lần.",
        "headline": "Sẵn sàng để bắt đầu?",
        "description": "Hãy khám phá những câu chuyện đã truyền cảm hứng cho hàng triệu người trên thế giới — hoàn toàn miễn phí.",
    },
}


async def _run() -> None:
    settings = get_settings()
    async with build_worker_scope(settings) as container:
        if await container.users.get_by_email(_SUPERADMIN_EMAIL) is None:
            await container.users.add(
                User(
                    id=None,
                    name="Super Admin",
                    email=_SUPERADMIN_EMAIL,
                    password_hash=container.hasher.hash(_SUPERADMIN_PASSWORD),
                    role=Role.SUPERADMIN,
                )
            )
            typer.echo(f"Created superadmin: {_SUPERADMIN_EMAIL}")
        else:
            typer.echo(f"Superadmin already exists: {_SUPERADMIN_EMAIL}")

        existing_categories = {c.slug for c in await container.categories.list_all()}
        for name, slug in _CATEGORIES:
            if slug not in existing_categories:
                await container.categories.add(Category(id=None, name=name, slug=slug))
        typer.echo(f"Categories: {len(_CATEGORIES)} ensured")

        existing_page = await container.contacts.list_paginated(page=1, per_page=1000)
        existing_contacts = {(c.type, c.value) for c in existing_page.items}
        for contact_type, label, value, sort_order in _CONTACTS:
            if (contact_type, value) not in existing_contacts:
                await container.contacts.add(
                    Contact(
                        id=None,
                        type=contact_type,
                        label=label,
                        value=value,
                        icon=None,
                        sort_order=sort_order,
                        is_active=True,
                    )
                )
        typer.echo(f"Contacts: {len(_CONTACTS)} ensured")

        if await container.settings_repo.get("about_us_data") is None:
            await container.settings_repo.set(
                "about_us_data", json.dumps(_ABOUT_US_DATA, ensure_ascii=False)
            )
            typer.echo("About-us content seeded")


@app.command()
def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    app()
