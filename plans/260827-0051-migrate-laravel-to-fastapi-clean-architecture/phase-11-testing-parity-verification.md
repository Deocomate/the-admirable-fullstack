---
phase: 11
title: "Kiểm thử & Đối chiếu ngang bằng"
status: completed
priority: P1
effort: "2d"
dependencies: [9, 10]
---

# Phase 11: Kiểm thử & Đối chiếu ngang bằng

## Overview

Chứng minh bằng bằng chứng — không phải bằng cảm nhận — rằng hệ thống FastAPI hành xử giống hệ thống Laravel. Ba trục kiểm chứng: **route parity** (đủ route, đúng method), **HTML parity** (đúng giao diện), và **architecture parity** (ranh giới lớp không bị vi phạm).

Đây là cổng chặn trước khi được phép xoá Laravel ở Phase 12. Không đạt cổng này thì không cutover.

## Requirements

**Functional**
- Bảng đối chiếu route: mọi route Laravel có route FastAPI tương ứng, và ngược lại không thừa route lạ.
- So sánh HTML render của hai hệ thống trên cùng dữ liệu, cho toàn bộ trang client và các trang admin chính.
- Đối chiếu kết quả tìm kiếm giữa hai hệ thống trên bộ truy vấn mẫu.
- Test tự động kiểm tra ranh giới phụ thuộc giữa 4 lớp.

**Non-functional**
- Toàn bộ test suite chạy dưới 5 phút.
- Coverage: `domain` ≥ 90%, `application` ≥ 85%, **`presentation` ≥ 70%**, tổng thể ≥ 75%. <!-- Updated: Validation Session 1 - thêm ngưỡng presentation -->
- CI chạy được (GitHub Actions), gồm lint + typecheck + test.

## Architecture

<!-- Updated: Validation Session 1 - hai worktree do branch riêng -->
**Chuẩn bị hai worktree.** Vì code Python nằm ở branch `migrate/fastapi` còn Laravel nằm ở `main`, việc chạy song song cần hai thư mục làm việc:

```bash
git worktree add ../admirable-laravel main       # bản Laravel để đối chiếu
# thư mục hiện tại vẫn ở branch migrate/fastapi
```

Worktree `admirable-laravel` cần `composer install` và `.env` trỏ DB cũ. **Xoá worktree này ngay sau khi Phase 11 kết thúc** (`git worktree remove ../admirable-laravel`) để không bỏ quên process `php artisan serve` chạy nền.

**Cách so sánh HTML.** Chạy song song: Laravel ở `localhost:8000` (worktree `admirable-laravel`), FastAPI ở `localhost:8001` (Docker, branch hiện tại), cùng trỏ vào dữ liệu tương đương (Laravel → DB cũ, FastAPI → DB mới đã migrate). Script `scripts/compare_html.py`:

1. Fetch cùng đường dẫn ở cả hai.
2. Chuẩn hoá: parse bằng BeautifulSoup, loại bỏ nhiễu đã biết — CSRF token, timestamp, session cookie, khoảng trắng thừa, thứ tự thuộc tính HTML.
3. So sánh cây DOM đã chuẩn hoá; xuất diff dạng HTML vào `plans/reports/html-parity/`.
4. Ngoài ra so riêng: danh sách `<meta>`, `<title>`, và tập class Tailwind theo từng phần tử.

Kết quả chấp nhận được: **khác biệt bằng 0 sau chuẩn hoá**, hoặc mọi khác biệt còn lại được liệt kê và giải thích trong báo cáo (ví dụ URL asset đổi từ `/storage/` sang `/media/` — đây là thay đổi có chủ đích).

**Test ranh giới lớp** dùng phân tích AST, không phụ thuộc thư viện ngoài:

```python
FORBIDDEN = {
    "admirable.domain": [
        "fastapi",
        "sqlalchemy",
        "pydantic",
        "redis",
        "taskiq",
        "jinja2",
        "admirable.application",
        "admirable.infrastructure",
        "admirable.presentation",
    ],
    "admirable.application": [
        "fastapi",
        "sqlalchemy",
        "redis",
        "taskiq",
        "jinja2",
        "admirable.infrastructure",
        "admirable.presentation",
    ],
    "admirable.infrastructure": ["admirable.presentation"],
}
```

Duyệt mọi file `.py`, parse `ast`, thu `Import`/`ImportFrom`, fail nếu vi phạm.

**Route parity.** Xuất route Laravel bằng `php artisan route:list --json` (chạy lần cuối trước khi xoá), xuất route FastAPI từ `app.routes`, so hai tập theo `(method, path_pattern, name)`. Lưu snapshot Laravel vào `plans/reports/laravel-routes.json` để còn đối chiếu được sau khi PHP bị xoá.

## Related Code Files

- Create: `scripts/compare_html.py`, `scripts/export_routes.py`, `scripts/compare_routes.py`, `scripts/compare_search_results.py`
- Create: `tests/architecture/test_layer_boundaries.py`
- Create: `tests/functional/test_route_parity.py`
- Create: `.github/workflows/ci.yml`
- Create: `plans/reports/parity-260827-{slug}.md` (báo cáo tổng hợp)
- Create: `plans/reports/laravel-routes.json` (snapshot, giữ vĩnh viễn)
- Modify: `pyproject.toml` (cấu hình coverage threshold)

## Implementation Steps

0. Dựng worktree `../admirable-laravel` từ `main` theo phần Architecture; `composer install` và cấu hình `.env` trỏ DB cũ; khởi động `php artisan serve --port=8000`. Ghi lại PID để dọn ở bước cuối.
1. Xuất snapshot route Laravel: chạy trong worktree đó `php artisan route:list --json`, lưu về `plans/reports/laravel-routes.json` trên branch `migrate/fastapi` và commit. **Làm ngay, trước khi đụng đến việc xoá bất cứ thứ gì** — sau Phase 12 sẽ không còn `artisan` để chạy lại.
2. `scripts/export_routes.py`: duyệt `app.routes`, xuất `(methods, path, name)` ra JSON.
3. `scripts/compare_routes.py`: so hai file, in bảng ba cột — chỉ có ở Laravel / có ở cả hai / chỉ có ở FastAPI. Chuẩn hoá cú pháp tham số (`{slug}` vs `{slug}`) và bỏ qua các route hạ tầng Laravel không còn ý nghĩa (`sanctum/*`, `storage/*`, `_ignition/*`).
4. `tests/architecture/test_layer_boundaries.py`: theo thiết kế trên. Chạy nhanh, đưa vào CI.
5. `scripts/compare_html.py`: theo thiết kế trên. Danh sách đường dẫn cần so:
   - Client: 8 route, mỗi route với 2-3 tham số thật (slug figure có audio, slug figure không audio, story id, category slug, search có/không kết quả).
   - Admin: dashboard, và trang index của categories/figures/stories/contacts/featured/users, form create + edit của figures và stories, settings about-us. Cần đăng nhập ở cả hai hệ thống — script tự login và giữ cookie.
   - **So `<head>` riêng, không gộp vào diff thân trang:** toàn bộ `<meta>`, `<title>`, `<link rel="canonical">`, và từng khối `<script type="application/ld+json">` (parse thành dict rồi so sâu, không so chuỗi — thứ tự khoá JSON có thể khác). Đây là nơi tầng SEO của Phase 8/9 được nghiệm thu.
6. `scripts/compare_search_results.py`: chạy 20 truy vấn mẫu (gồm từ khoá tiếng Việt có dấu, không dấu, tên riêng, cụm 1 ký tự, cụm dài) ở cả hai hệ thống, so danh sách slug và thứ tự. Đây là cổng quyết định cho rủi ro FULLTEXT ở Phase 3.
7. Chạy toàn bộ và ghi báo cáo `plans/reports/parity-260827-{slug}.md` gồm: bảng route diff, bảng HTML diff theo trang (số node khác biệt), bảng search diff, và danh sách khác biệt được chấp nhận kèm lý do.
8. Xử lý mọi khác biệt: sửa code FastAPI cho khớp, hoặc ghi nhận là thay đổi có chủ đích. Lặp lại từ bước 5 tới khi báo cáo sạch.
9. **Cổng quyết định FULLTEXT:** nếu bước 6 cho thấy >10% truy vấn khác kết quả, áp dụng phản ứng đã chốt ở Phase 3 — chuyển search về `LIKE '%q%'` hoàn toàn, chạy lại bước 6.
10. Bổ sung test còn thiếu để đạt ngưỡng coverage. Thứ tự ưu tiên: nhánh chưa phủ trong `application`, rồi `presentation` (ngưỡng ≥70%). Với `presentation`, tập trung vào phần HTML parity **không** kiểm được: nhánh lỗi validation, phân quyền `require_role`, redirect sau POST, mã trạng thái của 3 endpoint audio, và `build_seo_context`. Không viết test chỉ để nâng con số trên các router mỏng đã được parity phủ.
11. Viết `.github/workflows/ci.yml`: job `lint` (`ruff check`, `ruff format --check`), job `typecheck` (`mypy src`), job `test` (service MySQL + Redis, `alembic upgrade head`, `pytest --cov`). Đánh dấu skip test `@pytest.mark.network`.
12. Chạy kiểm thử thủ công theo checklist: đăng nhập, tạo/sửa/xoá figure có upload, sinh audio và huỷ, kéo thả featured, sửa About Us, xem trang client tương ứng. Ghi kết quả vào báo cáo.
13. Kiểm tra hiệu năng thô: `ab -n 200 -c 10` trên trang chủ và trang chi tiết ở cả hai hệ thống, ghi số liệu vào báo cáo (không phải cổng chặn, chỉ để biết).
14. **Dọn dẹp:** dừng `php artisan serve` (PID ghi ở bước 0) rồi `git worktree remove ../admirable-laravel`. Xác nhận không còn process PHP nào chạy nền.

## Success Criteria

- [x] `compare_routes.py`: cột "chỉ có ở Laravel" rỗng (sau khi loại route hạ tầng).
- [x] `compare_html.py`: 0 khác biệt sau chuẩn hoá, hoặc mọi khác biệt được liệt kê và chấp nhận tường minh trong báo cáo.
- [x] Thẻ `<title>` và `<meta>` khớp 100% trên 8 trang client.
- [x] Mọi khối JSON-LD khớp 100% sau khi parse và so sâu (không so chuỗi).
- [x] `compare_search_results.py`: ≥90% truy vấn cho cùng tập kết quả và cùng thứ tự (hoặc đã áp dụng phương án `LIKE` và đạt 100%).
- [x] `tests/architecture/test_layer_boundaries.py` pass.
- [x] Coverage đạt ngưỡng: domain ≥90%, application ≥85%, presentation ≥70%, tổng ≥75%.
- [x] CI xanh trên GitHub Actions.
- [x] Checklist thủ công hoàn tất, có ảnh chụp lưu trong `plans/reports/`.
- [x] Worktree `../admirable-laravel` đã gỡ, không còn process `php artisan serve` chạy nền.
- [x] Báo cáo `plans/reports/parity-*.md` tồn tại và không còn mục "chưa giải quyết".

## Risk Assessment

**Rủi ro: so sánh HTML sinh ra quá nhiều nhiễu, đội ngũ bỏ qua kết quả.** Mitigation: đầu tư vào bước chuẩn hoá trước khi chạy hàng loạt — thử trên một trang, tinh chỉnh bộ lọc nhiễu tới khi diff sạch, rồi mới mở rộng.
- Tín hiệu: >200 node khác biệt trên một trang đơn giản như `/lien-he`.
- Phản ứng: dừng, sửa bộ chuẩn hoá, không nới lỏng tiêu chí chấp nhận.

**Rủi ro: không dựng được hai hệ thống song song trên cùng máy (xung đột port, DB).** Mitigation: Laravel chạy trong worktree `../admirable-laravel` với `php artisan serve --port=8000` trỏ DB cũ; FastAPI chạy Docker map `8001` trỏ DB mới. Cả hai đọc cùng bộ file media (FastAPI đọc bản copy) nên hình ảnh giống nhau.

<!-- Updated: Validation Session 1 - worktree orphan process -->
**Rủi ro: worktree Laravel bị xoá mà `php artisan serve` vẫn chạy nền, thành process mồ côi giữ port 8000.** Mitigation: bước 0 ghi PID, bước 14 dừng process **trước** khi `git worktree remove`. Đưa vào tiêu chí nghiệm thu.

**Rủi ro: dữ liệu hai DB lệch nhau trong lúc so sánh (ai đó sửa nội dung ở bản cũ).** Mitigation: đóng băng bản Laravel (chỉ đọc) trong suốt phase này; thông báo cho người dùng admin. Nếu không thể đóng băng, chạy lại `migrate_data.py` ngay trước khi so sánh.

**Rủi ro: đạt "0 khác biệt HTML" nhưng hành vi JavaScript vẫn sai.** So sánh HTML tĩnh không bắt được lỗi runtime JS. Mitigation: bước 12 kiểm thử thủ công là bắt buộc, không được bỏ — đặc biệt editor content blocks, kéo thả, audio player, polling.
