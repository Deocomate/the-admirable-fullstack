---
phase: 8
title: "Nền tảng Template Jinja2"
status: completed
priority: P1
effort: "2d"
dependencies: [7]
---

# Phase 8: Nền tảng Template Jinja2

## Overview

Chuyển 17 file layout/component dùng chung trong `resources/views/components/` sang Jinja2, cùng bảng quy tắc chuyển đổi Blade→Jinja2 áp dụng cho toàn bộ 84 file. Phase này quyết định chất lượng của Phase 9 và 10: mọi file trang chỉ việc `{% extends %}` và gọi macro.

Nguyên tắc tuyệt đối: **HTML output phải giống hệt**. Tailwind class, cấu trúc DOM, và JavaScript inline được copy nguyên xi. Chỉ cú pháp template thay đổi.

## Requirements

**Functional**
- Layout client và admin render đúng: navbar, footer, sidebar, back-to-top, styles, scripts.
- Component dùng chung có macro tương đương: figure-card, story-card, category-pills, content-blocks, audio-player, pagination, share-buttons.
- Toàn bộ JavaScript inline (Web Audio API, SortableJS, reading progress, scroll reveal) hoạt động nguyên vẹn.
- Tailwind CDN + cấu hình theme inline giữ nguyên (không thêm build step Node).

**Non-functional**
- Không component nào phụ thuộc biến toàn cục ẩn — mọi dữ liệu truyền qua tham số macro tường minh.
- Template không chứa logic nghiệp vụ; mọi tính toán đã làm ở use case.

## Architecture

**Bảng chuyển đổi Blade → Jinja2:**

| Blade | Jinja2 |
|---|---|
| `@extends('layout')` / `@section('content')` | `{% extends "layout.html" %}` / `{% block content %}` |
| `@include('partial', [...])` | `{% include "partial.html" %}` (context kế thừa) hoặc `{% with %}` |
| `<x-client.layout.app>` (component có slot) | `{% extends %}` + `{% block %}` |
| `<x-client.shared.figure-card :figure="$f" />` | `{{ figure_card(figure=f) }}` (macro) |
| `@foreach ($xs as $x)` | `{% for x in xs %}` |
| `@if / @elseif / @else` | `{% if / elif / else %}` |
| `@empty` sau `@forelse` | `{% for %}...{% else %}...{% endfor %}` |
| `{{ $x }}` | `{{ x }}` (cả hai đều escape mặc định) |
| `{!! $x !!}` | Chỉ có **đúng 2 chỗ** trong toàn bộ 84 file, cả hai đã xác minh an toàn — xem Risk Assessment. Không phát sinh `\| safe` nào khác |
| `@csrf` | `{{ csrf_field() }}` |
| `@method('PUT')` | `<input type="hidden" name="_method" value="PUT">` |
| `route('admin.figures.index')` | `route('admin.figures.index')` (Jinja global, cú pháp giữ nguyên) |
| `route('client.figures.show', $f->slug)` | `route('client.figures.show', slug=f.slug)` |
| `asset('assets/images/logo.svg')` | `asset('assets/images/logo.svg')` |
| `asset('storage/' . $path)` | `media_url(path)` |
| `old('name', $figure->name)` | `old('name', figure.name)` |
| `$errors->has('name')` / `->first('name')` | `'name' in errors` / `errors['name'][0]` |
| `session('success')` | `flash('success')` |
| `@auth` / `auth()->user()` | `{% if current_user %}` / `current_user` |
| `$figures->links()` | `{{ pagination(page_obj) }}` (macro) |
| `Str::limit($t, 100)` | `t \| truncate_words(...)` hoặc filter riêng |
| `number_format($n)` | filter `number_format` |
| `$f->created_at->format('d/m/Y')` | `f.created_at \| date_vi` |

**Cây template đích** phản chiếu cây Blade để việc đối chiếu dễ dàng:

```
templates/
├── layouts/
│   ├── client.html          ← components/client/layout/app.blade.php
│   └── admin.html           ← components/admin/layout/app.blade.php
│   └── admin_auth.html      ← components/admin/layout/auth.blade.php
├── partials/
│   ├── client/{navbar,footer,styles,scripts,back-to-top}.html
│   └── admin/sidebar.html
├── macros/
│   ├── cards.html           ← figure-card, story-card
│   ├── content.html         ← content-blocks
│   ├── media.html           ← audio-player
│   ├── nav.html             ← category-pills, pagination, share-buttons
│   └── forms.html           ← input/textarea/select/error, dùng chung cho mọi form admin
├── client/**                ← client/**
├── admin/**                 ← admin/**
└── errors/{403,404,419,500}.html
```

**Macro form (`macros/forms.html`) là thứ mới, không có trong Blade** — nhưng cần thiết: các form admin hiện lặp lại y hệt khối `<label> + <input> + @error` hàng chục lần. Gom thành macro giảm ~30% dòng template và loại rủi ro sao chép sai. Đây là DRY, không phải thay đổi giao diện — HTML sinh ra phải giống hệt.

**Static asset.** `public/assets/` → `static/assets/`, phục vụ bởi nginx tại `/static/`. Global `asset(path)` trả `/static/{path}`. Riêng `favicon.ico` và `robots.txt` đặt ở gốc `static/` và nginx map thẳng `/favicon.ico`, `/robots.txt`.

<!-- Updated: Validation Session 1 - SEO module -->
**Tầng SEO (`presentation/web/seo.py`).** Layout client hiện tại nhận 14 prop SEO rồi tự tính trong khối `@php` (`app.blade.php:1-40`). Logic đó chuyển sang Python, không nằm trong template:

```python
@dataclass(frozen=True)
class SeoMeta:
    title: str = "The Admirable — Những tấm gương đáng ngưỡng mộ"
    description: str = "Khám phá những câu chuyện truyền cảm hứng..."   # copy nguyên default của Blade
    active_page: str = ""
    canonical_url: str | None = None      # None → dùng URL hiện tại
    og_type: str = "website"
    og_image: str | None = None           # None → asset('assets/images/logo.png')
    robots: str = "index,follow"
    keywords: str | None = None
    published_time: str | None = None
    modified_time: str | None = None
    article_section: str | None = None
    article_tags: tuple[str, ...] = ()
    json_ld: tuple[dict, ...] = ()

def build_seo_context(request, meta: SeoMeta) -> dict: ...
```

`build_seo_context` tái tạo đúng ba phép tính của Blade: `seo_canonical` = `canonical_url` hoặc URL hiện tại; `seo_image` = `og_image` hoặc logo mặc định, và **nếu không phải URL tuyệt đối thì bọc qua `asset()`** (khớp nhánh `filter_var(..., FILTER_VALIDATE_URL)`); `seo_locale` = locale thay `_` bằng `-`. Sau đó ghép schema `WebSite` mặc định (gồm `potentialAction`/`SearchAction` trỏ `route('client.search') + '?q={search_term_string}'`) lên đầu danh sách `json_ld` của trang — đúng thứ tự `array_merge([$defaultJsonLd], $jsonLd)`.

Template chỉ nhận kết quả đã tính và render. Mỗi khối JSON-LD render bằng `{{ schema | tojson | safe }}` bên trong `<script type="application/ld+json">`; `tojson` của Jinja2 đã escape an toàn cho ngữ cảnh script.

## Related Code Files

- Create: `src/admirable/presentation/web/seo.py` (`SeoMeta` + `build_seo_context`)
- Create: `src/admirable/presentation/web/templates/partials/client/seo-head.html` (render meta + JSON-LD)
- Create: `src/admirable/presentation/web/templates/layouts/{client,admin,admin_auth}.html`
- Create: `src/admirable/presentation/web/templates/partials/**` (6 file)
- Create: `src/admirable/presentation/web/templates/macros/{cards,content,media,nav,forms}.html`
- Create: `src/admirable/presentation/web/templates/errors/419.html`
- Create: `static/assets/images/{logo.svg,logo.png,logo.ico}`, `static/favicon.ico`, `static/robots.txt`
- Modify: `src/admirable/presentation/web/templating.py` (thêm filter `number_format`, `date_vi`, `truncate_words`, `nl2br`)
- Modify: `deploy/nginx/default.conf` (map `/favicon.ico`, `/robots.txt`)
- Create: `docs/template-conversion-map.md` (bảng đối chiếu 84 file Blade → Jinja2, dùng làm checklist ở Phase 9/10 và bằng chứng ở Phase 11)
- Nguồn tham chiếu (đọc, copy HTML, không sửa): toàn bộ `resources/views/components/**`

## Implementation Steps

1. Copy `public/assets/**`, `public/favicon.ico`, `public/robots.txt` sang `static/`. Giữ nguyên tên file.
2. Viết `docs/template-conversion-map.md`: liệt kê đủ 84 file Blade, cột "file Jinja2 đích", cột "trạng thái", cột "ghi chú". Đây là checklist thi công cho Phase 9/10.
3. Bổ sung filter vào `templating.py`: `number_format` (dấu phẩy ngăn nghìn), `date_vi` (`d/m/Y`), `truncate_words`, `nl2br`, `youtube_embed_id` (trích id từ URL YouTube — hiện đang làm inline trong Blade).
4. Viết `seo.py` theo thiết kế trên, rồi `partials/client/seo-head.html` render đủ: `<title>`, `description`, `keywords`, `robots`, `canonical`, toàn bộ `og:*`, `twitter:*`, nhánh `article:*` khi `og_type == "article"`, các khối JSON-LD, và 2 thẻ `<link rel="icon">` trỏ `assets/images/logo.ico`. Đối chiếu từng thẻ với `app.blade.php:45-90`.
5. `layouts/client.html` ← `components/client/layout/app.blade.php` (146 dòng). Định nghĩa block: `title`, `meta`, `head_extra`, `content`, `scripts_extra`. Include `seo-head`, navbar/footer/styles/scripts/back-to-top.
6. `partials/client/styles.html` ← `styles.blade.php` (191 dòng): copy nguyên khối `<style>` và cấu hình `tailwind.config` inline (bảng màu `apple-black`, `apple-gray`, `apple-blue`, `apple-bg`). **Không đụng một ký tự CSS nào.**
7. `partials/client/scripts.html` ← `scripts.blade.php` (496 dòng): copy nguyên JavaScript. Chú ý: nếu có chỗ Blade nội suy biến vào JS (`{{ }}` bên trong `<script>`), chuyển sang truyền qua `data-*` attribute hoặc `{{ x | tojson }}` để tránh lỗi escape. Rà từng chỗ nội suy.
8. `partials/client/{navbar,footer,back-to-top}.html`.
9. `layouts/admin.html` ← `components/admin/layout/app.blade.php` (119 dòng) + `partials/admin/sidebar.html` ← `sidebar.blade.php` (158 dòng). **Phải giữ `<meta name="csrf-token">` ở `<head>`** (`app.blade.php:6`). Sidebar đánh dấu mục đang active dựa trên tên route hiện tại — dùng `request.scope['route'].name` thay `request()->routeIs()`.
10. `layouts/admin_auth.html` ← `components/admin/layout/auth.blade.php`, cũng giữ `<meta name="csrf-token">` (`auth.blade.php:6`). Sau bước này, 3 template auth của Phase 7 chuyển sang `{% extends %}` layout thật.
11. `macros/cards.html`: `figure_card(figure, featured=False)` ← `figure-card.blade.php` (41 dòng); `story_card(story)` ← `story-card.blade.php`.
12. `macros/content.html`: `content_blocks(blocks)` ← `content-blocks.blade.php` (106 dòng) — render 3 loại block EN/VI đan xen. Đây là component quan trọng nhất về mặt giao diện; đối chiếu HTML từng loại block.
13. `macros/media.html`: `audio_player(src, title)` ← `audio-player.blade.php` — giữ nguyên JS Web Audio API tăng âm lượng và điều chỉnh tốc độ.
14. `macros/nav.html`: `category_pills(categories, active_slug)`, `pagination(page)` ← `pagination.blade.php` (36 dòng, dùng `Page.window()` của Phase 2), `share_buttons(url, title)`.
15. `macros/forms.html`: `text_input(name, label, value, errors, **attrs)`, `textarea(...)`, `select(...)`, `file_input(...)`, `checkbox(...)`, `error_text(name, errors)`. HTML sinh ra phải khớp chính xác markup hiện tại trong `admin/*/form.blade.php`.
16. `errors/419.html` (CSRF hết hạn) theo phong cách các trang lỗi khác.
17. Viết test render: mỗi layout và mỗi macro được render với dữ liệu giả, khẳng định không lỗi và chứa các class Tailwind then chốt. Riêng `seo-head.html`: test đối chiếu từng thẻ meta với danh sách trích từ `app.blade.php`, và test `build_seo_context` cho 4 tình huống — mặc định, có `canonical_url`, `og_image` tương đối, `og_image` là URL tuyệt đối.

## Success Criteria

- [x] `docs/template-conversion-map.md` liệt kê đủ 84 file Blade, không thiếu file nào.
- [x] 3 template auth của Phase 7 chạy trên `layouts/admin_auth.html` thật, giao diện khớp ảnh chụp bản Laravel.
- [x] Mọi macro render được với dữ liệu giả, test pass (52 test mới trong `tests/presentation/`).
- [x] `seo-head.html` render đủ mọi thẻ có trong `app.blade.php:45-90`; test đối chiếu danh sách thẻ pass.
- [x] `build_seo_context` có test cho 4 tình huống ảnh OG (mặc định / canonical tuỳ chỉnh / ảnh tương đối / ảnh URL tuyệt đối). Phát hiện và sửa 1 bug thật: ảnh mặc định bị bọc `asset()` hai lần (xem NOTES).
- [x] `layouts/admin.html` và `layouts/admin_auth.html` đều có `<meta name="csrf-token">`.
- [x] `curl /static/assets/images/logo.svg` trả 200 qua nginx (xác minh qua Docker Compose thật, không chỉ unit test).
- [x] Diff CSS: `partials/client/styles.html` so với `styles.blade.php` — nội dung `<style>` giống hệt byte-for-byte (test `test_css_parity.py`).
- [x] JavaScript trong `partials/client/scripts.html` giống hệt bản Blade — 0 điểm nội suy Blade tồn tại trong file gốc (`diff` xác nhận chỉ khác dòng trống cuối file), nên không cần `| tojson` nào ở đây.
- [x] `grep -r "| safe" templates/` chỉ trả về đúng 1 kết quả: khối JSON-LD trong `seo-head.html` (test `test_exactly_one_safe_filter_usage_in_template_tree`). `story_card`'s SVG icon được viết lại thành nhánh `{% if/elif %}` với markup literal thay vì biến `| safe`, để giữ đúng số lượng này.

### NOTES (Phase 8 — bằng chứng xác minh thật)

- **Bug thật tìm thấy qua test, không phải qua đọc code:** `build_seo_context` bọc `asset_url()` hai lần lên ảnh OG mặc định, sinh `/static/static/assets/images/logo.png`. Nguyên nhân: Blade's `asset()` trả URL tuyệt đối (nên nhánh `FILTER_VALIDATE_URL` không bọc lại), còn `asset_url()` của bản port trả đường dẫn tương đối gốc — không bao giờ "tuyệt đối", nên logic port-1:1 ban đầu luôn bọc lại. Sửa bằng cách tách rõ 3 nhánh (`None` / URL tuyệt đối / tương đối) thay vì "hoặc rồi kiểm tra tuyệt đối".
- **Xác minh qua Docker Compose thật** (không chỉ pytest): rebuild `web`+`worker`, restart `nginx`, curl qua nginx cho `/healthz`, `/static/assets/images/logo.svg`, `/favicon.ico`, `/robots.txt`, đăng nhập admin thật (`admin@gmail.com`), xác nhận CSRF 419 trả về trang lỗi có style thay vì HTML nội tuyến.
- **Khoảng trống đã biết, sẽ tự đóng ở Phase 9/10:** `partials/admin/sidebar.html` (layout thật) gọi `route()` cho 7 route admin CRUD (`admin.users.index`, `admin.categories.index`, v.v.) chưa tồn tại cho tới khi Phase 10 dựng router thật — nên `/admin/dashboard` trả 500 (`NoMatchFound`) khi đăng nhập thật cho tới khi Phase 9/10 hoàn tất. Đây là hệ quả tất yếu của việc nối `dashboard.html` vào layout thật (đúng như bước 10 của phase này yêu cầu) trước khi các route đó tồn tại — không phải lỗi phát sinh từ code Phase 8. Không thêm route giả để né tránh vì sẽ là code vứt đi.
- **Bổ sung ngoài danh sách bước 3 gốc:** thêm filter `str_limit` và `strip_tags` (không chỉ `number_format`/`youtube_embed_id`) vì `macros/cards.html`'s `story_card` (một deliverable của chính phase này) cần chúng để khớp `Str::limit(strip_tags(...))` của Blade.
- **Sửa kèm ngoài phạm vi template thuần tuý nhưng bắt buộc để đạt criterion "curl qua nginx trả 200":** `deploy/nginx/default.conf` trước đó alias `/static/` tới `/app/static/` — một đường dẫn không tồn tại trong container nginx (không có volume nào mount vào đó). Sửa bằng cách bỏ alias hỏng, để `/static/`, `/favicon.ico`, `/robots.txt` rơi qua `proxy_pass` tới `web` — FastAPI tự phục vụ (đã có `StaticFiles` mount sẵn từ Phase 7; thêm 2 route mới cho favicon/robots ở gốc).

## Risk Assessment

**Rủi ro cao: nội suy Blade bên trong `<script>` bị Jinja2 escape khác đi, làm hỏng JS.** Ví dụ `{{ $figure->name }}` bên trong chuỗi JS: Blade escape HTML, Jinja2 cũng escape HTML, nhưng dấu nháy và ký tự đặc biệt tiếng Việt có thể khác.
- Tín hiệu: lỗi JS console, audio player không chạy, SortableJS không kéo được.
- Phản ứng đã chốt: mọi giá trị đưa vào JS phải qua `| tojson`, không dùng `{{ }}` trần trong `<script>`. Bước 7 rà soát toàn bộ và ghi danh sách vào PR.

<!-- Updated: Validation Session 1 - rủi ro {!! !!} đã xác minh, hạ cấp -->
**~~Rủi ro `{!! !!}` mang theo lỗ hổng XSS~~ — ĐÃ XÁC MINH, KHÔNG TỒN TẠI.** Verification Session 1 quét toàn bộ 84 file Blade và chỉ tìm thấy 2 chỗ, cả hai đều không nhận dữ liệu người dùng:
- `components/client/layout/app.blade.php:85` — JSON-LD qua `json_encode`, chuyển sang `{{ schema | tojson | safe }}`.
- `components/client/shared/story-card.blade.php:16` — `{!! $icon !!}` lấy từ mảng SVG hardcode ngay trong template (`story-card.blade.php:4`), chọn bằng `$snippet->id % count($icons)`. Chuyển thành macro trả SVG cố định, không cần `| safe` cho dữ liệu DB.

Nội dung `content_blocks` do admin nhập **luôn được escape**, không bao giờ dùng `| safe`. Nếu trong lúc thi công phát hiện thêm chỗ cần HTML thô từ DB, dừng lại và báo cáo — đó sẽ là vấn đề bảo mật mới, cần quyết định riêng.

**Rủi ro: tầng SEO tính sai `og:image` khi giá trị là URL tuyệt đối.** Blade có nhánh `filter_var(..., FILTER_VALIDATE_URL)` để không bọc `asset()` lên URL đã tuyệt đối. Bỏ sót nhánh này sẽ sinh ra URL kiểu `/static/https://...`.
- Tín hiệu: thẻ `og:image` trong HTML diff ở Phase 11 lệch.
- Phản ứng: bước 17 bắt buộc có test cho cả 4 tình huống ảnh OG.

**Rủi ro: macro form sinh HTML lệch so với markup thủ công hiện tại, làm giao diện form admin đổi.** Mitigation: viết macro bằng cách copy-paste markup thật từ một form, rồi tham số hoá — không viết lại từ đầu. Xác minh bằng HTML diff ở Phase 11.

**Rủi ro: `request.scope['route'].name` không có trong một số ngữ cảnh (trang lỗi).** Mitigation: helper `is_route(name)` phải xử lý `None` an toàn, trả `False`.
