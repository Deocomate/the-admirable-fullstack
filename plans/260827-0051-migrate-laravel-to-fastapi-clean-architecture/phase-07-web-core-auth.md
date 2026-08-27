---
phase: 7
title: "Web core & Auth"
status: completed
priority: P1
effort: "2.5d"
dependencies: [5]
---

# Phase 7: Web core & Auth

## Overview

Dựng lớp presentation: app factory, dây DI, và **các tiện ích mà Laravel cho không nhưng FastAPI thì không có** — session, CSRF, method spoofing (`@method('PUT')`), flash message, old input, và hiển thị lỗi validation. Không có lớp này thì việc chuyển 84 template Blade ở Phase 8 sẽ phải viết lại logic form từ đầu.

Kết thúc phase: đăng nhập/đăng xuất/quên mật khẩu hoạt động đầy đủ với template thật.

## Requirements

**Functional**
- Session lưu ở Redis, cookie ký, TTL 120 phút (khớp `SESSION_LIFETIME=120`).
- CSRF token bắt buộc cho mọi request POST/PUT/PATCH/DELETE.
- Form HTML gửi `_method=PUT|DELETE` được định tuyến đúng (Laravel `@method`).
- Flash message và old input sống qua đúng một redirect (khớp `->with('success', ...)` và `old()`).
- Lỗi validation hiển thị lại đúng ô nhập, giữ dữ liệu đã nhập.
- Dependency `current_user`, `require_auth`, `require_role('superadmin')`.
- 4 trang auth admin hoạt động: login, forgot-password, reset-password, logout.

**Non-functional**
- Cookie session: `HttpOnly`, `SameSite=Lax`, `Secure` khi không phải môi trường local.
- Session ID được sinh lại sau khi đăng nhập thành công (chống session fixation — khớp `session()->regenerate()` của Laravel).
- Trang lỗi 403/404/500 render bằng template, không lộ traceback ở production.

## Architecture

**Session.** Middleware tự viết `RedisSessionMiddleware` (không dùng `SessionMiddleware` của Starlette, vì nó nhồi toàn bộ state vào cookie — không huỷ được từ server, không phù hợp khi đã bỏ bảng `sessions` nhưng vẫn cần logout thực sự).

- Cookie chứa **chỉ session id** đã ký bằng `itsdangerous`.
- Dữ liệu session nằm ở Redis key `sess:{sid}`, TTL trượt 120 phút.
- `request.state.session` là dict-like, ghi lại Redis cuối request nếu bị thay đổi.
- `regenerate()` sinh sid mới, copy dữ liệu, xoá key cũ.
- `invalidate()` xoá key và cookie.

**CSRF.** Token sinh mỗi session, lưu trong session. Middleware kiểm tra request không an toàn: đọc `_token` từ form hoặc header `X-CSRF-Token`, so bằng `secrets.compare_digest`. Jinja global `csrf_field()` render `<input type="hidden" name="_token" value="...">` — thay thế trực tiếp `@csrf` trong template.

<!-- Updated: Validation Session 1 - meta csrf-token -->
**Bắt buộc:** layout admin phải render `<meta name="csrf-token" content="{{ csrf_token() }}">` trong `<head>`. Đã xác minh JS đọc thẳng thẻ này ở 3 chỗ: `admin/featured-figures/index.blade.php:156`, `admin/partials/audio-generator.blade.php:215` và `:245`. Thiếu thẻ này thì kéo thả sắp xếp và sinh audio đều gãy. Tên header JS đang gửi là `X-CSRF-TOKEN` (chữ hoa) — middleware phải so tên header không phân biệt hoa thường.

**Method override.** Middleware đọc `_method` trong form body của POST và ghi đè `scope["method"]`. Bắt buộc, vì các route `admin.figures.update` (PUT) và `admin.*.destroy` (DELETE) hiện được gọi từ form HTML.

**Flash & old input.** Lưu trong session dưới key `_flash` và `_old`, đọc-và-xoá ở đầu request kế tiếp. Jinja global: `flash()`, `old(field, default='')`, `errors` (dict field → list message).

**Named route.** FastAPI có `request.url_for(name)`. Đăng ký mọi route với `name=` khớp tên Laravel nhưng dùng dấu chấm không hợp lệ trong Python identifier → dùng thẳng chuỗi: `@router.get("/nhan-vat/{slug}", name="client.figures.show")`. Jinja global `route(name, **params)` bọc `request.url_for` để template gần như giữ nguyên cú pháp cũ.

**DI.** `dependencies.py` cung cấp: `get_session` (AsyncSession theo request), `get_container` (dựng `build_request_scope(session)` của Phase 6), rồi các dependency nhỏ lấy từng use case ra. Router không bao giờ tự `new` repository.

**Xử lý ngoại lệ.** Exception handler ánh xạ:

| Ngoại lệ domain | HTTP |
|---|---|
| `EntityNotFoundError` | 404 + template `errors/404.html` |
| `BusinessRuleViolation` | 422 (form) hoặc 409 (JSON API audio) |
| `InvalidAudioTransitionError` | 409 JSON (khớp mã hiện tại của `AudioController`) |
| `ValidationError` | redirect back + flash errors + old input |
| Chưa đăng nhập | redirect `admin.auth.login` |
| Sai quyền | 403 + template, message giữ nguyên "Bạn không có quyền truy cập trang này." |

## Related Code Files

- Create: `src/admirable/presentation/web/main.py` (mở rộng từ Phase 1)
- Create: `src/admirable/presentation/web/dependencies.py`
- Create: `src/admirable/presentation/web/middleware/{session,csrf,method_override,error_handler}.py`
- Create: `src/admirable/presentation/web/security/{auth_dependencies,csrf_token}.py`
- Create: `src/admirable/presentation/web/templating.py` (Jinja2 environment + globals + filters)
- Create: `src/admirable/presentation/web/forms/base.py` (parse form → Pydantic, chuyển `ValidationError` thành dict lỗi theo field)
- Create: `src/admirable/presentation/web/routers/admin/auth.py`
- Create: `src/admirable/presentation/web/templates/admin/auth/{login,forgot-password,reset}.html`
- Create: `src/admirable/presentation/web/templates/errors/{403,404,500}.html`
- Create: `src/admirable/presentation/cli/{seed,create_superadmin}.py`
- Create: `tests/functional/test_auth.py`, `tests/functional/test_csrf.py`, `tests/functional/test_session.py`
- Nguồn tham chiếu: `app/Http/Controllers/Admin/AuthController.php`, `app/Http/Middleware/RoleMiddleware.php`, `routes/web.php`, `resources/views/admin/auth/*.blade.php`

## Implementation Steps

1. `templating.py`: `Jinja2Templates` với `autoescape=True`, `trim_blocks`, `lstrip_blocks`. Đăng ký globals: `route`, `csrf_field`, `csrf_token`, `old`, `errors`, `flash`, `current_user`, `asset`, `media_url`, `config` (chỉ expose các giá trị an toàn). Filter: `nl2br`, `truncate_words`, `date_vi` (định dạng ngày kiểu Việt).
2. `middleware/session.py`: `RedisSessionMiddleware` theo thiết kế trên. Viết class `Session` (MutableMapping) có `regenerate()`, `invalidate()`, `flash(key, value)`, `pull(key)`. Đặt vào `request.state.session`.
3. `middleware/method_override.py`: chỉ áp dụng khi `content-type` là `application/x-www-form-urlencoded` hoặc `multipart/form-data`, và `_method` nằm trong `{PUT, PATCH, DELETE}`. Phải đọc body mà không tiêu thụ nó (cache lại `receive`).
4. `middleware/csrf.py`: bỏ qua GET/HEAD/OPTIONS. Với các method khác, lấy token từ form/header, so với session. Thiếu hoặc sai → 419 (giữ mã của Laravel) render template lỗi thân thiện. Đặt sau method_override trong chuỗi middleware.
5. `middleware/error_handler.py`: đăng ký exception handler theo bảng ở trên. Với request `Accept: application/json` (các endpoint audio) trả JSON, còn lại trả HTML.
6. `security/auth_dependencies.py`:
   - `get_current_user(request) -> AuthenticatedUserDTO | None` đọc `user_id` từ session, nạp user.
   - `require_auth` → raise `NotAuthenticatedError` nếu None.
   - `require_role(*roles)` factory → raise `ForbiddenError`. Thay `RoleMiddleware`.
7. `dependencies.py`: `get_db_session` (async generator, commit khi thành công / rollback khi lỗi), `get_container`, và các provider use case (`get_login_uc`, `get_create_figure_uc`, …). Dùng `Annotated[X, Depends(...)]` cho gọn.
8. `forms/base.py`: `async def parse_form(request, model: type[T]) -> T` — đọc `await request.form()`, chuyển `ValidationError` của Pydantic thành `dict[str, list[str]]` theo tên field, raise `FormValidationError` để error handler bắt và redirect-back. Hỗ trợ field mảng kiểu `content_blocks[0][text_en]` (định dạng form của Laravel) — viết hàm `unflatten_form_data()` chuyển ký hiệu ngoặc vuông thành dict/list lồng nhau. **Bắt buộc**, vì form figures/stories hiện dùng đúng cú pháp này.
9. `routers/admin/auth.py`: 7 route khớp `routes/web.php` — `admin.auth.login` (GET/POST), `admin.auth.forgot-password` (GET/POST), `admin.auth.reset-password` (GET/POST), `admin.auth.logout` (POST). Sau login thành công: `session.regenerate()`, lưu `user_id`, redirect `admin.dashboard`.
10. Guest guard: dependency `require_guest` redirect về dashboard nếu đã đăng nhập (khớp middleware `guest`).
11. Chuyển 3 template auth từ Blade sang Jinja2 (đây là bộ template đầu tiên, dùng để xác minh toàn bộ helper hoạt động trước khi làm hàng loạt ở Phase 8).
12. Template lỗi 403/404/500 theo phong cách hiện có của site.
13. `cli/seed.py` (Typer): port `UserSeeder`, `CategorySeeder`, `ContactSeeder`, `SettingSeeder`. `cli/create_superadmin.py`: tạo superadmin tương tác, dùng cho VPS mới.
14. Test functional: login đúng/sai, session regenerate (sid đổi sau login), logout xoá key Redis, CSRF thiếu → 419, `_method=DELETE` gọi đúng handler, old input giữ giá trị sau lỗi validation, `require_role` chặn admin thường vào `/admin/users`.

## Success Criteria

- [ ] Đăng nhập bằng `admin@gmail.com` (hash bcrypt cũ) thành công, vào được dashboard.
- [ ] Session id thay đổi sau khi đăng nhập; key Redis cũ bị xoá.
- [ ] Logout xoá session ở Redis, truy cập lại `/admin/dashboard` bị redirect về login.
- [ ] POST không có `_token` → 419, không thực thi hành động.
- [ ] `<meta name="csrf-token">` có mặt trong `<head>` của layout admin và layout admin-auth; request gửi header `X-CSRF-TOKEN` được chấp nhận.
- [ ] Form với `_method=DELETE` gọi đúng route DELETE.
- [ ] `unflatten_form_data` parse đúng payload thật copy từ DevTools của form figures hiện tại (test có fixture payload thật).
- [ ] Tài khoản role `admin` truy cập `/admin/users` nhận 403 với đúng thông điệp tiếng Việt cũ.
- [ ] `uv run python -m admirable.presentation.cli.seed` tạo được superadmin và dữ liệu mẫu.
- [ ] Không có traceback lộ ra khi `APP__ENV=production`.

## Risk Assessment

**Rủi ro: middleware method-override đọc body làm hỏng việc đọc form ở router.** Đây là lỗi kinh điển trong Starlette. Mitigation: cache body và thay `receive` bằng closure phát lại body. Test bắt buộc: một route PUT nhận `multipart/form-data` có file upload phải đọc được cả file lẫn field.
- Tín hiệu hỏng: request treo hoặc form rỗng ở router.
- Phản ứng: nếu cache body gây vấn đề với file lớn, giới hạn method-override chỉ áp dụng cho `application/x-www-form-urlencoded` và đổi các form DELETE sang gửi qua `fetch()` với header `X-HTTP-Method-Override` (chỉ ảnh hưởng vài nút xoá).

**Rủi ro: `unflatten_form_data` không phủ hết cú pháp form Laravel đang dùng.** Mitigation: bước 8 phải lấy payload **thật** từ form figures và stories hiện tại làm fixture, không tự bịa. Đọc `resources/views/admin/figures/partials/content-blocks-script.blade.php` (582 dòng) để nắm chính xác tên field mà JS sinh ra.

**Rủi ro: thứ tự middleware sai gây CSRF kiểm tra trước khi method-override chạy.** Mitigation: ghi rõ thứ tự trong `main.py` kèm comment: `ErrorHandler → Session → MethodOverride → CSRF → router`. Có test khẳng định form `_method=DELETE` kèm `_token` hợp lệ đi lọt.

**Rủi ro: bỏ `remember_token` làm mất tính năng "ghi nhớ đăng nhập".** Đã chốt ở Phase 3. Thay thế: khi tick "remember", session TTL đặt 30 ngày thay vì 120 phút. Hành vi người dùng tương đương, không cần cột DB.
