---
phase: 4
title: "Hạ tầng Persistence"
status: completed
priority: P1
effort: "2.5d"
dependencies: [2]
---

# Phase 4: Hạ tầng Persistence

## Overview

Hiện thực hoá các interface repository của Phase 2 bằng SQLAlchemy 2.0 async trên MySQL. Phase này chứa toàn bộ SQL của hệ thống. Lớp `application` ở Phase 5 sẽ chỉ nhìn thấy Protocol, không bao giờ thấy `Session` hay `select()`.

Điểm mấu chốt: **ORM model không phải entity**. Có một lớp mapper tường minh chuyển đổi hai chiều. Đây là chi phí gõ phím đổi lấy việc domain không bị ràng buộc vào schema — đúng yêu cầu "dễ bảo trì".

## Requirements

**Functional**
- Mỗi Protocol repository ở Phase 2 có đúng một class hiện thực trong `infrastructure/db/repositories/`.
- Mọi truy vấn hiện có của Laravel được tái tạo với cùng ngữ nghĩa: eager loading, đếm quan hệ, sắp xếp ưu tiên featured, phân trang.
- Quản lý transaction theo unit-of-work: một request = một session = một transaction.

**Non-functional**
- Không có truy vấn N+1 ở bất kỳ trang nào (kiểm chứng bằng test đếm số câu SQL).
- Session async, engine dùng pool có kích thước cấu hình được.
- `alembic check` xác nhận ORM metadata khớp migration của Phase 3.

## Architecture

**Engine & session.** `async_sessionmaker` với `expire_on_commit=False`. Session được tạo mỗi request qua FastAPI dependency (Phase 7) và inject xuống repository qua constructor.

**Eager loading thay thế `with()` của Eloquent:**

| Laravel | SQLAlchemy |
|---|---|
| `Figure::with('categories')` | `selectinload(FigureModel.categories)` |
| `withCount('storySnippets')` | subquery `func.count()` + `.label('story_snippets_count')` |
| `whereHas('categories', ...)` | `.join(...).where(...)` hoặc `.where(FigureModel.categories.any(...))` |

Dùng `selectinload` (không `joinedload`) cho quan hệ many-to-many để tránh nhân bản hàng khi phân trang — đây chính là bẫy tương đương với `LengthAwarePaginator` + `joinedload`.

**Mapper.** Mỗi aggregate có một module `mappers/figure_mapper.py` với `to_entity(model) -> Figure` và `apply_to_model(entity, model) -> None`. Không dùng SQLAlchemy imperative mapping lên dataclass domain — làm vậy sẽ kéo SQLAlchemy vào domain qua cửa sau.

**Truy vấn search có ưu tiên featured** (tái tạo `SearchController` hiện tại):

```sql
LEFT JOIN featured_figures ff ON ff.figure_id = figures.id
ORDER BY (ff.id IS NULL), ff.priority, figures.created_at DESC
```

Giữ nguyên thứ tự này để kết quả trang tìm kiếm không đổi.

**Phân trang.** Repository trả `Page[Entity]` (value object Phase 2). Đếm tổng bằng một query `COUNT(*)` riêng trên cùng điều kiện WHERE — tương đương cách `paginate()` của Laravel hoạt động.

## Related Code Files

- Create: `src/admirable/infrastructure/db/base.py` (`DeclarativeBase`, naming convention cho constraint)
- Create: `src/admirable/infrastructure/db/session.py` (engine factory, `async_sessionmaker`, `get_session` context manager)
- Create: `src/admirable/infrastructure/db/models/{user,category,figure,story_snippet,featured_figure,contact,setting}.py`
- Create: `src/admirable/infrastructure/db/models/associations.py` (`category_figure`)
- Create: `src/admirable/infrastructure/db/mappers/*.py`
- Create: `src/admirable/infrastructure/db/repositories/*.py`
- Create: `src/admirable/infrastructure/db/types.py` (TypeDecorator cho cột JSON ↔ `list[ContentBlock]`, và cho `AudioStatus` enum)
- Create: `tests/integration/db/**`, `tests/integration/conftest.py`
- Modify: `migrations/env.py` (trỏ `target_metadata` vào `Base.metadata` thật)

## Implementation Steps

1. `base.py`: `class Base(DeclarativeBase)` + `metadata = MetaData(naming_convention={...})` để tên index/FK sinh ra ổn định và khớp Phase 3.
2. `session.py`: `create_async_engine(url, pool_size, max_overflow, pool_pre_ping=True, echo=settings.db.echo)`. URL dạng `mysql+asyncmy://user:pass@host:port/db?charset=utf8mb4`. Hàm `dispose_engine()` cho lifespan shutdown.
3. `types.py`: `ContentBlocksType(TypeDecorator)` bọc `JSON`, `process_bind_param` gọi `serialize_content_blocks`, `process_result_value` gọi `parse_content_blocks`. Tương tự `KeyFactsType`. `AudioStatus` map bằng `sa.Enum(AudioStatus, native_enum=True)`.
4. Viết 7 ORM model khớp **chính xác** schema Phase 3. `FigureModel.categories` là `relationship(secondary=category_figure_table, lazy="raise")` — đặt `lazy="raise"` để mọi truy cập không eager-load sẽ nổ ngay ở test thay vì âm thầm gây N+1.
5. Chạy `alembic check`. Nếu báo lệch, sửa **ORM model** cho khớp migration (migration Phase 3 là chuẩn), không sửa migration.
6. Viết mapper cho từng aggregate. `to_entity` phải nhận cả các trường tính toán tuỳ chọn (ví dụ `story_snippets_count`, `is_featured`) — dùng tham số keyword mặc định `None`.
7. `FigureRepositoryImpl`: hiện thực đủ các phương thức Protocol.
   - `list_paginated(search, category_id, page, per_page)` ← `FigureService::getAll`, giữ `latest()` = `ORDER BY created_at DESC`.
   - `search(...)` ← `SearchController::index`, gồm cả nhánh MATCH/LIKE mô tả ở Phase 3, cờ `is_featured` gắn vào entity.
   - `list_trending(limit)` ← `withCount('storySnippets')->orderByDesc(...)->limit(4)`.
   - `list_latest(limit, exclude_ids)` ← nhánh fallback trong `HomeController`.
   - `sync_categories(figure_id, category_ids)` ← `->categories()->sync()`: xoá hàng thừa, chèn hàng thiếu, không đụng hàng đã đúng.
   - `delete(id)` — dựa vào `ON DELETE CASCADE` sẵn có cho `story_snippets`, `category_figure`, `featured_figures`. Việc xoá **file vật lý** không thuộc repository, thuộc use case ở Phase 5.
8. `UserRepositoryImpl`: `get_by_email` (dùng cho login), `count_superadmins` (dùng cho ràng buộc xoá), `list_all` sắp xếp theo `created_at`.
9. `SettingRepositoryImpl`: `get`/`set` với `INSERT ... ON DUPLICATE KEY UPDATE` (tương đương `updateOrCreate`).
10. `FeaturedFigureRepositoryImpl`: `list_ordered_with_figure(limit)` sắp xếp theo `priority` rồi `id`, eager-load figure và `story_snippets_count`; `reorder(ids)` cập nhật `priority` theo chỉ số mảng trong một transaction.
11. `StorySnippetRepositoryImpl`, `CategoryRepositoryImpl`, `ContactRepositoryImpl` (có scope `active` + `ordered`).
12. Viết `tests/integration/conftest.py`: fixture dựng MySQL container (dùng service `mysql` của compose, DB riêng `admirable_test`), chạy `alembic upgrade head`, mỗi test chạy trong transaction rồi rollback.
13. Viết integration test cho mỗi repository: CRUD cơ bản, và **test đếm SQL** — dùng event listener `before_cursor_execute` đếm câu lệnh, khẳng định `list_paginated(per_page=15)` phát sinh ≤ 3 câu (data + count + selectinload categories).
14. Viết test riêng cho `search()` khẳng định thứ tự featured-first đúng như hệ Laravel.

## Success Criteria

- [ ] `alembic check` báo "No new upgrade operations detected".
- [ ] Mọi Protocol ở `domain/repositories` có class hiện thực; `mypy src/admirable/infrastructure/db` pass.
- [ ] `pytest tests/integration/db` pass toàn bộ.
- [ ] Test đếm SQL xác nhận không có N+1 ở: danh sách figures admin, trang chủ, trang search, trang chi tiết figure.
- [ ] `grep -r "lazy=\"select\"" src/admirable/infrastructure/db/models` rỗng (mọi relationship là `raise` hoặc được eager-load tường minh).
- [ ] Thứ tự kết quả `search()` khớp hệ Laravel trên cùng dữ liệu (so sánh danh sách slug).

## Risk Assessment

**Rủi ro: `lazy="raise"` gây nổ runtime ở đường dẫn hiếm (ví dụ trang lỗi, template component).** Đây là đánh đổi có chủ đích — nổ sớm ở test tốt hơn N+1 âm thầm ở production.
- Tín hiệu: `MissingGreenlet` hoặc `InvalidRequestError` khi render một trang.
- Phản ứng đã chốt: thêm eager-load tường minh vào đúng truy vấn của trang đó. Không đổi `lazy` thành `select`.

**Rủi ro: `asyncmy` gặp lỗi với cột JSON hoặc charset utf8mb4 trên MySQL 8.4.** Mitigation: test integration ở bước 13 phải bao gồm ghi/đọc `content_blocks` có tiếng Việt có dấu và emoji.
- Phản ứng nếu hỏng: đổi driver sang `aiomysql` (cùng được SQLAlchemy 2.0 hỗ trợ, chỉ đổi một dòng URL). Ghi lại lý do trong `docs/database-schema.md`.

**Rủi ro: mapper thủ công sinh lỗi lặp lại (quên map một trường mới).** Mitigation: viết một test tham số hoá dùng `dataclasses.fields(Entity)` khẳng định mọi field của entity đều được `to_entity` gán giá trị khác `None` (trừ danh sách nullable được whitelist tường minh).
