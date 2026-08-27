---
phase: 9
title: "Khu vực Client"
status: completed
priority: P1
effort: "2d"
dependencies: [8]
---

# Phase 9: Khu vực Client

## Overview

Chuyển toàn bộ 8 route công khai và ~30 template client. Đây là phần người dùng cuối nhìn thấy và là phần có ràng buộc SEO — **URL không được đổi một ký tự**.

Phase này có thể chạy song song với Phase 10 (Admin) vì hai bên không chạm file chung ngoài `templates/macros/` và `templates/layouts/` đã đóng băng ở Phase 8.

## Requirements

**Functional**
- 8 route giữ nguyên URI và tên: `/`, `/linh-vuc`, `/linh-vuc/{slug}`, `/nhan-vat/{slug}`, `/cau-chuyen/{id}`, `/tim-kiem`, `/ve-chung-toi`, `/lien-he`.
- Trang chủ giữ nguyên thuật toán chọn featured + bù figure mới nhất.
- Tìm kiếm giữ nguyên thứ tự ưu tiên featured và bộ lọc theo lĩnh vực.
- Trang chi tiết nhân vật: nội dung song ngữ theo block, key facts, audio player, YouTube nhúng, story snippets, nhân vật liên quan, thanh tiến độ đọc.
- Trang "Về chúng tôi" render động từ `settings.about_us_data`.
- Trang liên hệ hiển thị các kênh `is_active`, sắp xếp theo `sort_order`.
- Slug/id không tồn tại → 404 dùng template lỗi.

**Non-functional**
- Thẻ meta (title, description, OG) giữ nguyên nội dung như bản Laravel.
- Không truy vấn N+1 (đã enforce bằng `lazy="raise"` ở Phase 4).
- Trang chi tiết render dưới 200ms với dữ liệu hiện tại (local, không cache).

## Architecture

Mỗi router là một file mỏng: nhận request → gọi đúng use case của Phase 5 → trả `templates.TemplateResponse`. Không có logic nghiệp vụ nào trong router.

```python
@router.get("/nhan-vat/{slug}", name="client.figures.show")
async def show(request: Request, slug: str, uc: GetFigureDetailDep) -> Response:
    data = await uc.execute(slug)
    return templates.TemplateResponse(request, "client/figure/show.html", {"figure": data})
```

`EntityNotFoundError` do use case raise được error handler của Phase 7 chuyển thành 404 — router không cần try/except.

<!-- Updated: Validation Session 1 - SEO per-route -->
**SEO là trách nhiệm của router.** Mỗi router client dựng một `SeoMeta` (Phase 8) từ DTO rồi đưa vào context. Bản Laravel truyền các prop này qua `<x-client.layout.app :title="..." :jsonLd="..." />` ở từng trang, nên giá trị phải được **đọc từ chính file Blade tương ứng**, không suy đoán:

| Route | `og_type` | JSON-LD bổ sung (ngoài `WebSite` mặc định) |
|---|---|---|
| `client.home` | `website` | theo `client/home/index.blade.php` |
| `client.figures.show` | `article` | schema nhân vật + `published_time`/`modified_time`/`article_section`/`article_tags` |
| `client.stories.show` | `article` | schema mẩu chuyện |
| `client.categories.*`, `client.search`, `client.about-us`, `client.contact` | `website` | theo từng file Blade |

Nhánh `article:*` chỉ render khi `og_type == "article"` — giữ đúng điều kiện `@if($ogType === 'article')`.

**Ánh xạ router → use case → template:**

| Route | Use case | Template |
|---|---|---|
| `client.home` | `GetHomePage` | `client/home/index.html` |
| `client.categories.index` | `ListCategories` | `client/category/index.html` |
| `client.categories.show` | `GetCategoryPage` | `client/category/index.html` (cùng template, khác dữ liệu — giữ nguyên như hiện tại) |
| `client.figures.show` | `GetFigureDetail` | `client/figure/show.html` |
| `client.stories.show` | `GetStoryDetail` | `client/story/show.html` |
| `client.search` | `SearchFigures` | `client/search/index.html` |
| `client.about-us` | `GetAboutUsPage` | `client/about-us/index.html` |
| `client.contact` | `GetContactPage` | `client/contact/index.html` |

## Related Code Files

- Create: `src/admirable/presentation/web/routers/client/{home,categories,figures,stories,search,about_us,contact}.py`
- Create: `src/admirable/presentation/web/templates/client/home/{index,_how-it-works,_media-badges,_newsletter,_quote-section}.html`
- Create: `.../client/category/index.html`
- Create: `.../client/figure/{show,_key-facts,_reading-progress-script,_related-figures-section,_story-snippets-section}.html`
- Create: `.../client/story/{show,_other-stories-section}.html`
- Create: `.../client/search/{index,_category-pills,_popular-trending,_results,_search-form}.html`
- Create: `.../client/about-us/{index,_hero,_stats,_problem-solution,_core-values,_audience,_cta}.html`
- Create: `.../client/contact/{index,_hero,_contact-info,_services,_cta,_buy-me-a-coffee}.html`
- Modify: `src/admirable/presentation/web/main.py` (đăng ký router client)
- Modify: `docs/template-conversion-map.md` (đánh dấu hoàn thành)
- Nguồn tham chiếu: `resources/views/client/**`, `app/Http/Controllers/Client/*.php`, `routes/web.php`

## Implementation Steps

1. Đăng ký `client_router` trong `main.py`. **Thứ tự đăng ký quan trọng:** router client đăng ký sau router admin để `/admin/...` không bị route động nào nuốt. Thực tế các URI client đều có tiền tố tiếng Việt cố định nên không xung đột, nhưng giữ thứ tự này cho an toàn.
2. **Trước khi chuyển template:** đọc từng file `client/*/index.blade.php` và `show.blade.php`, trích ra chính xác bộ prop SEO mà nó truyền cho `<x-client.layout.app>` (title, description, ogType, ogImage, jsonLd, publishedTime…). Lập bảng trong `docs/template-conversion-map.md`. Đây là nguồn duy nhất để dựng `SeoMeta` ở mỗi router — không tự nghĩ ra giá trị.
3. Chuyển từng nhóm template theo `docs/template-conversion-map.md`, áp dụng bảng quy tắc của Phase 8. Thứ tự đề xuất (từ đơn giản tới phức tạp): contact → about-us → category → story → search → figure → home.
4. **Contact** (6 file): dữ liệu đơn giản, dùng để xác thực pipeline.
5. **About Us** (7 file): render từ `AboutUsContent` value object. Chú ý các mảng có số lượng cố định (stats 4, core values 4, audience 3, bullets 3) — template phải chịu được mảng thiếu phần tử (dữ liệu cũ có thể chưa điền đủ), dùng vòng lặp chứ không index cứng.
6. **Category** (1 file, 2 route): `index` không có slug → liệt kê mọi lĩnh vực; có slug → lọc figure. Xác nhận template hiện tại xử lý cả hai trường hợp trước khi chuyển.
7. **Story** (2 file): chi tiết mẩu chuyện + danh sách chuyện khác của cùng nhân vật. Dùng macro `content_blocks` và `audio_player`. `og_type = "article"`.
8. **Search** (5 file): form tìm kiếm, pill lĩnh vực, kết quả có phân trang giữ query string (`?q=...&category=...&page=2` — dùng helper dựng URL giữ tham số, thay `->appends($request->query())`), khối trending.
9. **Figure** (5 file, 113 dòng file chính): phần phức tạp nhất về giao diện. Gồm key facts, content blocks song ngữ, audio player, YouTube embed, story snippets, related figures, và script theo dõi tiến độ đọc. Chuyển `_reading-progress-script.blade.php` cẩn thận theo quy tắc `| tojson` của Phase 8. `og_type = "article"` kèm đủ nhánh `article:*`.
10. **Home** (5 file, 142 dòng file chính): hero featured figure, lưới 6 figure, danh sách lĩnh vực, khối thống kê, how-it-works, media badges, newsletter, quote section.
11. Viết functional test cho mỗi route: status 200, template đúng, biến then chốt có mặt. Với `/nhan-vat/khong-ton-tai` → 404.
12. Test thuật toán trang chủ ở mức HTTP: dựng 0/3/6/10 featured figure, khẳng định số card hiển thị đúng và không trùng lặp.
13. Test phân trang search giữ nguyên query string qua các trang.
14. **Test SEO cho cả 8 route:** parse HTML trả về, khẳng định `<title>`, `description`, `canonical`, `og:*`, `twitter:*` có giá trị đúng, và mỗi trang có ít nhất một khối JSON-LD parse được thành JSON hợp lệ. Trang figure/story phải có đủ nhánh `article:*`.
15. Chụp ảnh màn hình (thủ công) 8 trang ở cả hai hệ thống trên cùng dữ liệu, lưu vào `plans/reports/` để đối chiếu ở Phase 11.

## Success Criteria

- [x] 8 route trả 200 với dữ liệu thật đã migrate.
- [x] URI khớp chính xác `docs/page-sitemap.md` (kiểm bằng `app.url_path_for(...)` cho cả 8 tên route, xác nhận thủ công qua `curl` qua nginx).
- [x] Slug/id không tồn tại trả 404 với template lỗi, không phải traceback.
- [x] Audio player phát được file audio thật từ `/media/uploads/audio/...` (xác nhận qua `mark-zuckerberg`, `<audio>`/`<source>` trỏ đúng `media_url()`).
- [x] YouTube nhúng hiển thị đúng với các định dạng URL đang có trong DB (`watch?v=`, `watch?v=...&t=88s` đã test qua dữ liệu thật).
- [x] Nội dung song ngữ EN/VI hiển thị đúng thứ tự và định dạng như bản Laravel.
- [x] Phân trang search giữ `q` và `category` qua các trang.
- [x] Mỗi trang trong 8 route có `<title>`, `canonical`, `og:*`, `twitter:*` đúng giá trị và ≥1 khối JSON-LD parse được; figure/story có đủ `article:*`.
- [x] `pytest tests/functional/client` pass (23 test, dữ liệu dev DB thật + 1 story tạo/xoá trong fixture).
- [ ] Ảnh chụp 8 trang hai hệ thống được lưu để đối chiếu — **dời sang Phase 11**: hệ Laravel không còn chạy song song trong phiên làm việc này (không có worktree `main` dựng sẵn) và Playwright chưa có trong `pyproject.toml`. Phase 11 ("Testing & Parity Verification") là nơi sở hữu việc đối chiếu hai hệ thống theo đúng mô tả của chính bước 15; sẽ dựng cả hai hệ thống và chụp ảnh ở đó thay vì cài công cụ chụp ảnh tạm thời ở Phase 9.

## Implementation Notes

Thi công theo đúng thứ tự đề xuất (contact → about-us → category → story →
search → figure → home), đọc trực tiếp 31 file Blade + toàn bộ DTO/use case
Phase 5 trước khi viết router, không suy đoán giá trị SEO.

**Lỗi thật phát hiện và sửa trong lúc thi công (không phải style):**

1. `macros/cards.html` (viết ở Phase 8, trước khi DTO Phase 9 tồn tại)
   dùng `figure.categories[0].name` — sai, `FigureSummaryDTO.category_names`
   là `list[str]` phẳng, không phải object ORM. Sửa thành `figure.category_names[0]`.
2. `macros/cards.html`'s `story_card` gọi `route('client.stories.show', id=story.id)`
   — sai tên tham số, route thật dùng `story_id`. Sửa lại; phát hiện qua
   render-smoke-test trước khi lên Docker.
3. `story_card` có fallback `story.content | strip_tags | str_limit(100)` —
   `content` không tồn tại trên bất kỳ DTO nào truyền vào macro này
   (`StorySummaryLite` chỉ có subtitle; cột `content` đã bị Phase 3 drop
   thay bằng `search_text`). Sửa fallback thành chỉ dùng `subtitle`, cập
   nhật test tương ứng ở `tests/presentation/test_macros.py`.
4. `about-us/_core-values.html` và `_audience.html` dùng `about_us.core_values.items`
   — `items` va với method `dict.items()` built-in, Jinja's `getattr` trả
   về bound method thay vì list, gây `TypeError` khi render. Sửa thành
   bracket access `about_us.core_values['items']`.
5. Tất cả `{% from "macros/..." import ... %}` phải thêm `with context` —
   nếu không, các macro gọi `route()` (context-dependent global) bên trong
   sẽ `KeyError('request')` vì macro imported mặc định không kế thừa
   context của template gọi nó. Phát hiện qua render-smoke-test full-context
   (không chỉ syntax check).
6. `tests/presentation/conftest.py`'s dummy route cho `client.stories.show`
   khai tham số đường dẫn là `{id}`; route thật (Phase 9) dùng `{story_id}`.
   Sửa cho khớp.

**Phát hiện, không sửa trong Phase 9 (ngoài phạm vi lớp Presentation):**
tất cả 7 model SQLAlchemy (`figures`, `story_snippets`, `users`, `categories`,
`contacts`, `featured_figures`, `settings`) có cột `created_at`/`updated_at`
không có default ở DB lẫn Python, và mapper `apply_to_model` của ít nhất
`figure`/`story_snippet`/`user` không copy hai trường này khi ghi — nghĩa là
bản ghi tạo mới qua ứng dụng (chưa có route thật cho tới Phase 10) sẽ có
timestamp `NULL` vĩnh viễn, ảnh hưởng `article:published_time`/`modified_time`
và thứ tự `list_latest()`. Dữ liệu migrate thật (Phase 3) không bị ảnh hưởng
vì được set trực tiếp lúc migrate. Cần Phase 10 (khi các use case
`create_figure`/`create_story`/... thật sự được gọi qua route admin) xử lý —
đã ghi vào `phase-10-admin-area.md`.

Toàn bộ 31 template + 7 router đã verify sống qua Docker Compose thật
(`docker compose up -d --build`, MySQL/Redis/nginx thật, dữ liệu 30 figure
migrate từ Laravel), không chỉ unit test.

## Risk Assessment

**Rủi ro: dữ liệu `about_us_data` trong DB thiếu trường so với cấu trúc mặc định, gây lỗi template.** Đã có `AboutUsContent.merge()` ở Phase 2 xử lý. Mitigation bổ sung: bước 4 yêu cầu template lặp thay vì index cứng.
- Tín hiệu: `UndefinedError` hoặc `IndexError` khi render.
- Phản ứng: sửa template thành vòng lặp, không sửa dữ liệu.

**Rủi ro: định dạng URL YouTube trong DB đa dạng (watch?v=, youtu.be/, embed/) mà logic trích id inline trong Blade xử lý theo cách riêng.** Mitigation: đọc chính xác đoạn Blade hiện tại, port nguyên logic vào filter `youtube_embed_id` ở Phase 8. Test bằng **mọi giá trị `youtube_url` thật** trong DB, không phải giá trị bịa.

**Rủi ro: thanh tiến độ đọc phụ thuộc cấu trúc DOM cụ thể.** Mitigation: giữ nguyên id/class của phần tử. Kiểm chứng thủ công bằng cách cuộn trang.

<!-- Updated: Validation Session 1 - SEO risk cụ thể hoá -->
**Rủi ro: giá trị SEO của từng trang bị suy đoán thay vì đọc từ Blade.** Layout nhận 14 prop và mỗi trang truyền một bộ khác nhau; đoán sai một giá trị `title` hay `jsonLd` là mất SEO một trang mà HTML diff dễ bỏ qua nếu bộ chuẩn hoá lọc quá tay.
- Mitigation: bước 2 bắt buộc lập bảng prop SEO từ chính file Blade **trước khi** viết router; bước 14 test tự động; Phase 11 so sánh toàn bộ thẻ `<meta>`, `<title>` và JSON-LD giữa hai hệ thống trên 8 trang.
- Tín hiệu: HTML diff báo lệch ở `<head>`, hoặc test bước 14 fail.
- Phản ứng: sửa `SeoMeta` ở router theo giá trị Blade, không nới lỏng bộ so sánh.
