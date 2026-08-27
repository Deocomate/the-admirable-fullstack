---
phase: 2
title: "Lớp Domain"
status: completed
priority: P1
effort: "2d"
dependencies: [1]
---

# Phase 2: Lớp Domain

## Overview

Xây lớp trong cùng của Clean Architecture: entity nghiệp vụ, value object, và interface repository. Toàn bộ phase này là Python thuần — **không import bất kỳ framework nào** (không FastAPI, không SQLAlchemy, không Pydantic). Đây là nơi các quy tắc nghiệp vụ hiện đang nằm rải rác trong Eloquent model và Laravel service được viết lại thành code tường minh, test được mà không cần database.

## Requirements

**Functional**
- Mọi khái niệm nghiệp vụ hiện có đều có entity tương ứng: Figure, Category, StorySnippet, FeaturedFigure, Contact, User, Setting.
- Cấu trúc `content_blocks` (đang là JSON tự do) trở thành value object có kiểu và có validate.
- Quy tắc nghiệp vụ được đưa vào entity: state machine audio, ràng buộc xoá superadmin cuối cùng, sinh slug duy nhất, dựng `search_text` từ content blocks.
- Interface repository định nghĩa đủ mọi truy vấn mà use case ở Phase 5 sẽ cần.

**Non-functional**
- `mypy --strict` pass 100% trên thư mục `domain`.
- Test chạy được không cần DB, Redis, hay network.
- Không có `import` nào ngoài stdlib (`dataclasses`, `datetime`, `enum`, `typing`, `re`, `abc`).

## Architecture

**Entity** dùng `@dataclass` (không Pydantic — Pydantic là chi tiết hạ tầng). Entity mang định danh (`id`) và hành vi. Ví dụ `Figure.request_audio_generation()` tự kiểm tra state machine và raise `AudioAlreadyProcessingError` thay vì để controller kiểm tra.

**Value object** bất biến (`@dataclass(frozen=True)`). `ContentBlock` là discriminated union theo `type`:

```python
@dataclass(frozen=True)
class HeadingBlock:
    text_en: str


@dataclass(frozen=True)
class ParagraphBlock:
    text_en: str
    text_vi: str | None = None
    heading_en: str | None = None


@dataclass(frozen=True)
class QuoteBlock:
    text_en: str
    author: str | None = None


ContentBlock = HeadingBlock | ParagraphBlock | QuoteBlock
```

Giữ đúng schema JSON hiện tại (xem `docs/rules.md` §2) để dữ liệu cũ đọc được không cần chuyển đổi. Hàm `parse_content_blocks(raw: list[dict]) -> list[ContentBlock]` bỏ qua block sai định dạng thay vì raise — khớp hành vi `normalizeContentBlocks` hiện tại của `FigureService`.

**AudioStatus** là `StrEnum` với 5 giá trị. State machine hợp lệ:

```
idle       → processing
processing → completed | failed | cancelled
completed  → processing   (sinh lại)
failed     → processing   (thử lại)
cancelled  → processing
```

Phương thức chuyển trạng thái nằm trên entity, mọi chuyển trạng thái không hợp lệ raise `InvalidAudioTransitionError`.

**Repository interface** dùng `typing.Protocol` (không `ABC`) — cho phép hiện thực ở `infrastructure` mà không cần kế thừa, giữ phụ thuộc một chiều tuyệt đối.

## Related Code Files

- Create: `src/admirable/domain/entities/{figure,category,story_snippet,featured_figure,contact,user,setting}.py`
- Create: `src/admirable/domain/value_objects/{content_block,key_fact,audio_status,role,slug,about_us_content,pagination}.py`
- Create: `src/admirable/domain/repositories/{figure,category,story_snippet,featured_figure,contact,user,setting}_repository.py`
- Create: `src/admirable/domain/services/slug_generator.py` (domain service: sinh slug duy nhất, cần hỏi repository)
- Create: `src/admirable/domain/exceptions.py`
- Create: `tests/unit/domain/**`
- Nguồn tham chiếu (đọc, không sửa): `app/Models/*.php`, `app/Services/FigureService.php`, `app/Services/UserService.php`, `app/Services/SettingService.php`, `docs/rules.md`

## Implementation Steps

1. `exceptions.py`: cây ngoại lệ gốc `DomainError`, các nhánh `EntityNotFoundError`, `ValidationError`, `BusinessRuleViolation` và các lỗi cụ thể (`InvalidAudioTransitionError`, `LastSuperAdminDeletionError`, `SelfDeletionError`, `DuplicateSlugError`).
2. `value_objects/audio_status.py`: `AudioStatus(StrEnum)` + bảng chuyển trạng thái + hàm `can_transition(src, dst) -> bool`.
3. `value_objects/role.py`: `Role(StrEnum)` = `SUPERADMIN`, `ADMIN`.
4. `value_objects/content_block.py`: 3 dataclass + union + `parse_content_blocks()` + `serialize_content_blocks()` (trả về `list[dict]` để lưu JSON). Thêm `extract_english_text(blocks) -> str` (dùng cho TTS ở Phase 6) và `build_search_text(blocks) -> str` (gộp cả EN + VI, thay `buildPlainContent` của `FigureService`).
5. `value_objects/key_fact.py`: `KeyFact(label, value)` + `parse_key_facts()` lọc bỏ entry rỗng (khớp `normalizeKeyFacts`).
6. `value_objects/slug.py`: `Slug` frozen, validate `^[a-z0-9]+(?:-[a-z0-9]+)*$`, classmethod `from_text()` dùng thuật toán tương đương `Str::slug` (bỏ dấu tiếng Việt → ASCII → kebab).
7. `value_objects/about_us_content.py`: dataclass lồng nhau phản ánh đúng cấu trúc trong `SettingService::getDefaultAboutUsData()` (hero, stats[4], problem, solution+bullets[3], core_values+items[4], audience+items[3], cta). Có `default()` và `merge(raw: dict)` tương đương `array_replace_recursive`.
8. `value_objects/pagination.py`: `Page[T]` generic — `items`, `total`, `page`, `per_page`, thuộc tính suy ra `last_page`, `has_prev`, `has_next`, `window(size)` cho macro phân trang ở Phase 8. Thay `LengthAwarePaginator`.
9. `entities/figure.py`: `Figure` với các trường khớp cột DB sau khi dọn (`id, name, slug, avatar_path, short_description, key_facts, content_blocks, search_text, audio_path, audio_status, audio_error, youtube_url, created_at, updated_at`) + quan hệ `category_ids: list[int]`. Hành vi: `rebuild_search_text()`, `request_audio_generation()`, `mark_audio_completed(path)`, `mark_audio_failed(msg)` (cắt 500 ký tự như code cũ), `cancel_audio()`, `attach_audio_upload(path)` (set thẳng `completed`).
10. `entities/story_snippet.py`: tương tự Figure, thêm `figure_id`, `subtitle`, `image_path`; dùng chung mixin `AudioCapable` để không lặp state machine (DRY).
11. `entities/user.py`: `User` + `is_superadmin()`, `is_admin()`, `can_be_deleted_by(actor, superadmin_count)` gói cả hai ràng buộc an toàn hiện có trong `UserService` (không tự xoá mình, không xoá superadmin cuối cùng).
12. `entities/{category,featured_figure,contact,setting}.py`: đơn giản; `Contact` giữ `is_active`, `sort_order`.
13. `repositories/*.py`: Protocol cho từng aggregate. Phương thức phải phủ hết truy vấn hiện có — đọc `app/Services/*.php` và các Client controller để liệt kê. Bắt buộc có:
    - `FigureRepository`: `get_by_id`, `get_by_slug`, `list_paginated(search, category_id, page, per_page)`, `search(query, category_slug, page, per_page)` (có sắp xếp ưu tiên featured như `SearchController` hiện tại), `list_latest(limit, exclude_ids)`, `list_trending(limit)` (nhiều story snippet nhất), `count`, `slug_exists(slug, exclude_id)`, `add`, `update`, `delete`, `sync_categories`.
    - `UserRepository`: `get_by_id`, `get_by_email`, `list_all`, `count_superadmins`, `add`, `update`, `delete`.
    - `SettingRepository`: `get(key)`, `set(key, value)`.
    - `FeaturedFigureRepository`: `list_ordered_with_figure(limit)`, `add`, `remove`, `reorder(ids_in_order)`.
    - `StorySnippetRepository`, `CategoryRepository`, `ContactRepository`: tương ứng.
14. `domain/services/slug_generator.py`: `ensure_unique(base: Slug, exists: Callable[[str], Awaitable[bool]]) -> Slug` — vòng lặp thêm hậu tố `-1`, `-2`… khớp `FigureService::uniqueSlug`.
15. Viết unit test cho: state machine audio (mọi cặp chuyển hợp lệ và không hợp lệ), `parse_content_blocks` với dữ liệu thật lấy từ DB hiện tại, `build_search_text`, `Slug.from_text` với tên tiếng Việt có dấu, ràng buộc xoá user, `AboutUsContent.merge` với dữ liệu thiếu trường.

## Success Criteria

- [ ] `mypy --strict src/admirable/domain` pass, 0 lỗi.
- [ ] `grep -rE "^(from|import) (fastapi|sqlalchemy|pydantic|redis|taskiq)" src/admirable/domain` trả về rỗng.
- [ ] `pytest tests/unit/domain` pass, coverage ≥ 90% trên thư mục domain.
- [ ] `parse_content_blocks` chạy được trên toàn bộ giá trị `content_blocks` trích từ DB production mà không mất block nào (script kiểm chứng dùng dump JSON của Phase 3).
- [ ] Mọi truy vấn xuất hiện trong `app/Services/*.php` và `app/Http/Controllers/Client/*.php` đều có phương thức repository tương ứng (bảng đối chiếu kèm trong PR).

## Risk Assessment

**Rủi ro: interface repository thiếu phương thức, phát hiện muộn ở Phase 5/9/10 gây sửa ngược lên domain.** Mitigation: bước 13 bắt buộc lập bảng đối chiếu từ code Laravel hiện tại trước khi viết. Tín hiệu hỏng: phải thêm phương thức repository trong khi làm Phase 9/10. Phản ứng: chấp nhận thêm (chi phí thấp), nhưng nếu phải thêm >5 phương thức thì dừng và rà soát lại toàn bộ interface một lượt thay vì vá lẻ.

**Rủi ro: `Slug.from_text` bỏ dấu tiếng Việt khác `Str::slug` của Laravel, gây slug mới khác slug cũ → vỡ URL/SEO.** Mitigation: slug của bản ghi cũ **được giữ nguyên khi migrate** (Phase 3 copy nguyên cột), hàm mới chỉ áp dụng cho bản ghi tạo mới. Thêm test đối chiếu 20 slug thật trong DB với kết quả `Slug.from_text(name)` và ghi nhận sai lệch nếu có, nhưng không sửa dữ liệu cũ.

**Rủi ro: trạng thái `cancelled` không có trong tài liệu nhưng có trong code.** Đã xác nhận bằng đọc `app/Http/Controllers/Admin/AudioController.php:53` — code set `'cancelled'`. Quyết định: đưa vào enum chính thức và cập nhật `docs/rules.md` ở Phase 12.
