---
phase: 10
title: "Khu vực Admin"
status: pending
priority: P1
effort: "3.5d"
dependencies: [8]
---

# Phase 10: Khu vực Admin

## Overview

Chuyển toàn bộ 30+ route quản trị và ~37 template admin. Đây là phase nặng nhất về khối lượng: form nhiều bước, editor content blocks bằng JavaScript (582 dòng), kéo thả sắp xếp, polling trạng thái audio, và trang settings dạng block.

Có thể chạy song song với Phase 9.

## Requirements

**Functional**
- Mọi route trong `routes/web.php` (phần admin) có route tương ứng cùng tên, cùng method, cùng URI.
- CRUD đầy đủ: categories, figures, stories, contacts, users.
- Editor content blocks: thêm/xoá/sắp xếp block, import JSON, copy prompt AI — JavaScript giữ nguyên.
- Featured figures: thêm/xoá + kéo thả sắp xếp (SortableJS) lưu qua endpoint reorder.
- Audio: 3 endpoint JSON (`generate`, `cancel`, `status`) với polling từ giao diện.
- Settings About Us: form 7 section, lưu vào `settings.about_us_data`.
- Users: chỉ superadmin truy cập; ràng buộc không tự xoá và không xoá superadmin cuối cùng.
- Dashboard: thống kê tổng quan.

**Non-functional**
- Upload file giới hạn kích thước và loại (hiện chưa có giới hạn tường minh — bổ sung theo `StoreFigureRequest`).
- Endpoint audio trả đúng mã HTTP mà JS đang xử lý: **200 khi OK, 409 khi đang chạy**. Không còn nhánh 422 — đó là mã riêng của lỗi cấu hình Azure, và JS chưa từng xử lý nó (xác minh ở Validation Session 1). <!-- Updated: Validation Session 1 - bỏ 422 khỏi requirements -->
- Lỗi sinh audio (edge-tts hỏng) là bất đồng bộ: worker đặt `audio_status='failed'` + `audio_error`, giao diện thấy qua endpoint `status`.
- Form giữ dữ liệu đã nhập khi validation lỗi (kể cả content blocks).

## Architecture

**Bảng route đích** (khớp `routes/web.php`, tiền tố `/admin`, tên tiền tố `admin.`):

| Method | URI | Tên | Use case |
|---|---|---|---|
| GET | `/` | `admin.home` | redirect dashboard |
| GET | `/dashboard` | `admin.dashboard` | `GetDashboard` |
| GET/POST/PUT/DELETE | `/categories*` | `admin.categories.{index,create,store,edit,update,destroy}` | nhóm `categories` |
| GET/POST/PUT/DELETE | `/figures*` | `admin.figures.*` | nhóm `figures` |
| GET/POST/DELETE | `/featured-figures*` | `admin.featured-figures.{index,store,destroy}` | nhóm `featured` |
| POST | `/featured-figures/reorder` | `admin.featured-figures.reorder` | `ReorderFeatured` |
| GET/POST/PUT/DELETE | `/stories*` | `admin.stories.*` | nhóm `stories` |
| GET/POST/PUT/DELETE | `/contacts*` | `admin.contacts.*` | nhóm `contacts` |
| GET/POST | `/settings/about-us` | `admin.settings.about-us{,.submit}` | `GetAboutUs`, `UpdateAboutUs` |
| POST | `/audio/generate/{kind}/{id}` | `admin.audio.generate` | `RequestAudioGeneration` |
| POST | `/audio/cancel/{kind}/{id}` | `admin.audio.cancel` | `CancelAudioGeneration` |
| GET | `/audio/status/{kind}/{id}` | `admin.audio.status` | `GetAudioStatus` |
| GET/POST/PUT/DELETE | `/users*` | `admin.users.*` (superadmin) | nhóm `users` |

`Route::resource(...)->except(['show'])` của Laravel = 6 route: index, create, store, edit, update, destroy. Viết một helper `register_resource(router, prefix, name, handlers)` để không lặp 6 lần cho 4 nhóm (DRY).

**Route order.** `/figures/create` phải đăng ký **trước** `/figures/{id}`, nếu không `create` sẽ bị bắt như id. Áp dụng cho cả 4 resource.

**Form phức tạp.** Form figures gửi cấu trúc lồng: `key_facts[0][label]`, `content_blocks[2][text_vi]`. Hàm `unflatten_form_data` của Phase 7 xử lý. Pydantic model `FigureFormData` validate sau khi unflatten.

**Giữ dữ liệu khi lỗi.** Content blocks là mảng lồng, `old()` mặc định không xử lý được. Giải pháp: khi validation lỗi, lưu **toàn bộ payload đã unflatten** vào session `_old` dưới dạng JSON, template đọc lại và JS dựng lại editor từ đó — đúng cách bản Blade đang làm (`old('content_blocks', $figure->content_blocks)`).

**Endpoint audio là JSON**, không HTML. Dùng `response_model` Pydantic, và CSRF vẫn áp dụng (JS hiện gửi token qua header — kiểm tra `audio-generator.blade.php` để xác nhận cách gửi và giữ nguyên).

## Related Code Files

- Create: `src/admirable/presentation/web/routers/admin/{dashboard,categories,figures,featured_figures,stories,contacts,settings,users,audio}.py`
- Create: `src/admirable/presentation/web/routers/resource_helper.py`
- Create: `src/admirable/presentation/web/forms/{figure,story,category,contact,user,about_us}_form.py`
- Create: `.../templates/admin/dashboard.html`
- Create: `.../templates/admin/categories/{index,form}.html`
- Create: `.../templates/admin/figures/{index,form}.html` + `partials/{actions-card,basic-info-card,categories-card,content-blocks-card,content-blocks-script,copy-prompt-card,key-facts-card,media-card}.html`
- Create: `.../templates/admin/featured-figures/index.html`
- Create: `.../templates/admin/stories/{index,form}.html` + `partials/{actions-card,basic-info-card,content-blocks-card,content-blocks-script,media-card}.html`
- Create: `.../templates/admin/contacts/{index,form}.html`
- Create: `.../templates/admin/settings/about-us.html` + `partials/{hero,stats,problem-solution,core-values,audience,cta}-section.html`
- Create: `.../templates/admin/users/{index,create,edit}.html`
- Create: `.../templates/admin/partials/audio-generator.html`
- Modify: `main.py`, `docs/template-conversion-map.md`
- Nguồn tham chiếu: `resources/views/admin/**`, `app/Http/Controllers/Admin/*.php`, `app/Http/Requests/*.php`

## Implementation Steps

1. `resource_helper.py`: hàm đăng ký 6 route chuẩn với tên đúng quy ước, `create` trước `{id}`.
2. Chuyển 8 Form Request của Laravel thành Pydantic model trong `forms/`. Đọc từng file `app/Http/Requests/*.php` để lấy **chính xác** rule (required, max length, mimes, unique). Rule `unique` cần truy vấn → xử lý ở use case, không ở Pydantic.
3. **Dashboard**: use case `GetDashboard` đếm figures/categories/stories/contacts/users + danh sách mới nhất. Template 125 dòng.
4. **Categories** (2 template): CRUD đơn giản, làm trước để xác thực `resource_helper` và macro form.
5. **Contacts** (2 template, 121 + 103 dòng): CRUD + toggle `is_active` + `sort_order`.
6. **Users** (3 template): gắn `require_role('superadmin')` ở mức router. Form create/edit khác nhau ở chỗ mật khẩu bắt buộc/tuỳ chọn. Nút xoá hiển thị có điều kiện theo `can_be_deleted_by`.
7. **Stories** (2 + 5 template): form có content blocks editor (285 dòng JS). Chuyển JS theo quy tắc `| tojson` của Phase 8. Select nhân vật liên kết.
8. **Figures** (2 + 8 template): phần lớn nhất.
   - `index.html` (178 dòng): bảng có tìm kiếm, lọc theo lĩnh vực, phân trang, trạng thái audio.
   - `form.html` + 8 partial: basic info, key facts (mảng động), categories (multi-select), content blocks (582 dòng JS — thêm/xoá/sắp xếp/import JSON), copy prompt AI (176 dòng), media (avatar + audio upload), actions.
   - Chuyển `content-blocks-script` **nguyên xi**, chỉ đổi điểm nội suy dữ liệu khởi tạo sang `{{ blocks | tojson }}`.
9. **Featured figures** (1 template, 176 dòng): danh sách kéo thả SortableJS. Endpoint `reorder` nhận mảng id JSON, trả 204. Giữ nguyên JS.
10. **Settings About Us** (1 + 6 template): form 7 section. Payload lồng sâu → dùng `unflatten_form_data`. Sau khi lưu, redirect back kèm flash success.
11. **Audio** (3 endpoint + `audio-generator.html` 268 dòng):
    - `generate` → 200 hoặc 409 (đang chạy). **Bỏ nhánh 422 "Azure key not configured"** — edge-tts không cần key; nếu edge-tts lỗi thì trạng thái chuyển `failed` qua worker, không phải lỗi đồng bộ.
    - `cancel` → 200 hoặc 409.
    - `status` → `{status, error, audio_url}` — `audio_url` dùng `media_url()`.
    - <!-- Updated: Validation Session 1 - JS audio đã xác minh --> **JS polling không cần sửa một dòng nào.** Đã xác minh ở Verification Session 1: `audio-generator.blade.php` chỉ xử lý mã 409 (`:219`, `:249`) và các giá trị `status` là `processing` (`:164`), `completed` (`:171`), `failed` (`:180`), `cancelled` (`:186`) — **không hề có nhánh nào xử lý 422**. Việc bỏ Azure vì thế trong suốt với giao diện. Chỉ cần giữ nguyên hợp đồng JSON và thẻ `<meta name="csrf-token">` mà JS đọc ở `:215` và `:245`.
    - Lưu ý hệ quả: `cancelled` là trạng thái UI chính thức mà JS đã xử lý → ENUM 5 giá trị ở Phase 3 là bắt buộc, không phải tuỳ chọn.
12. Đăng ký toàn bộ router admin trong `main.py`, đặt trước router client.
13. Viết functional test cho mọi route admin: quyền truy cập (chưa đăng nhập → redirect; admin thường vào `/admin/users` → 403), CRUD end-to-end cho figures (tạo có upload avatar → sửa → xoá, kiểm tra file bị xoá thật), reorder featured, và 3 endpoint audio với các trạng thái.
14. Test đặc thù: tạo figure với content blocks lồng nhau từ payload thật; validation lỗi giữ nguyên content blocks đã nhập.

## Success Criteria

- [ ] Danh sách route sinh ra khớp 1:1 với `php artisan route:list` của bản cũ (phần admin) — bảng đối chiếu ở Phase 11.
- [ ] CRUD figures hoạt động đầy đủ, kể cả upload và xoá file vật lý.
- [ ] Editor content blocks thêm/xoá/sắp xếp/import JSON hoạt động như cũ (kiểm thủ công + ảnh chụp).
- [ ] Kéo thả featured figures lưu đúng thứ tự sau khi tải lại trang.
- [ ] Sinh audio bằng edge-tts chạy hết vòng đời và giao diện polling cập nhật đúng.
- [ ] Huỷ sinh audio giữa chừng trả trạng thái đúng và không để lại file mồ côi.
- [ ] Superadmin không thể tự xoá mình; không thể xoá superadmin cuối cùng — thông điệp lỗi giữ nguyên.
- [ ] Validation lỗi ở form figures giữ nguyên mọi content block đã nhập.
- [ ] Lưu About Us và xem lại trang `/ve-chung-toi` thấy nội dung mới.
- [ ] `pytest tests/functional/admin` pass.

## Risk Assessment

**Rủi ro cao nhất: 582 dòng JS của content-blocks editor phụ thuộc chặt vào tên field và cấu trúc DOM Blade sinh ra.** Đây là nơi dễ vỡ nhất của toàn dự án.
- Mitigation: đọc kỹ file trước khi chuyển, liệt kê mọi tên field JS sinh ra, và viết fixture payload thật cho `unflatten_form_data` từ Phase 7. Không viết lại JS.
- Tín hiệu hỏng: submit form mất block, hoặc block sai thứ tự, hoặc import JSON không điền được form.
- Phản ứng: đối chiếu payload gửi đi giữa hai hệ thống bằng DevTools Network, sửa `unflatten_form_data` chứ không sửa JS.

**Rủi ro: `Route::resource` sinh ra ràng buộc route model binding (`{user}` tự nạp User) mà FastAPI không có.** Mitigation: viết dependency `get_user_or_404(user_id)` tương đương và dùng nhất quán. Đảm bảo id không tồn tại → 404 chứ không 500.

<!-- Updated: Validation Session 1 - rủi ro 422 đã xác minh, loại bỏ -->
**~~Rủi ro JS polling xử lý riêng mã 422 của Azure~~ — ĐÃ XÁC MINH, KHÔNG TỒN TẠI.** `grep` toàn bộ `audio-generator.blade.php` cho thấy chỉ có nhánh 409, không có 422. Bỏ Azure không tạo nhánh chết nào trong JS.

**Rủi ro còn lại về audio: thiếu `<meta name="csrf-token">` làm gãy cả sinh audio lẫn kéo thả featured.** JS đọc thẳng thẻ này ở 3 nơi (`audio-generator.blade.php:215,245`, `featured-figures/index.blade.php:156`) và không có nhánh dự phòng — thiếu thẻ sẽ ném `TypeError` trên `.content` của `null`.
- Tín hiệu: console báo `Cannot read properties of null`, nút sinh audio và kéo thả im lặng không phản hồi.
- Phản ứng: đã đưa thành tiêu chí nghiệm thu bắt buộc ở Phase 7 và Phase 8.

**Rủi ro: upload file không giới hạn kích thước gây DoS.** Hiện tại Laravel dựa vào `post_max_size` của PHP. FastAPI không có mặc định tương đương.
- Phản ứng đã chốt: đặt `client_max_body_size 32M` trong nginx và kiểm tra kích thước trong `LocalFileStorage`. Ghi vào `docs/rules.md` ở Phase 12.

**Rủi ro: khối lượng phase quá lớn, dễ bỏ sót template.** Mitigation: `docs/template-conversion-map.md` là checklist bắt buộc; PR không được merge khi còn dòng chưa đánh dấu.

<!-- Phát hiện ở Phase 9, cần xử lý ở Phase 10 -->
**Rủi ro: `created_at`/`updated_at` không được set khi tạo/sửa bản ghi qua ứng dụng.** Phát hiện khi viết functional test SEO cho Phase 9 (`tests/functional/client/test_seo.py`): cả 7 model SQLAlchemy (`figures`, `story_snippets`, `users`, `categories`, `contacts`, `featured_figures`, `settings`) khai `created_at`/`updated_at` không có `server_default`/Python `default`, và mapper `apply_to_model` của ít nhất `figure_mapper.py`/`story_snippet_mapper.py`/`user_mapper.py` không copy hai trường này khi ghi (chỉ đọc ở `to_entity`). Dữ liệu migrate thật (Phase 3) không bị ảnh hưởng vì được set trực tiếp lúc migrate; nhưng bất kỳ `create_figure`/`create_story`/`update_*` nào gọi qua route admin thật của Phase 10 sẽ để `NULL` vĩnh viễn.
- Ảnh hưởng: `article:published_time`/`modified_time` (SEO figure/story) sẽ bị bỏ qua cho nội dung tạo mới; `list_latest()`/`ORDER BY created_at DESC` sắp xếp không ổn định cho các bản ghi cùng `NULL`.
- Mitigation: khi viết `add()`/`update()` cho từng repository ở Phase 10 (hoặc sớm hơn nếu chạm trước), set `model.created_at`/`model.updated_at` tường minh (ví dụ qua `infrastructure/clock.py`'s `SystemClock` đã có sẵn) thay vì dựa vào default ẩn.
- Tín hiệu: figure/story tạo mới qua admin panel không có `<meta property="article:published_time">`, hoặc xuất hiện ở cuối danh sách "mới nhất" thay vì đầu.
