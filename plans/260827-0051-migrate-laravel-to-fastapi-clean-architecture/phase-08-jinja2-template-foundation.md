---
phase: 8
title: "Nền tảng Template Jinja2"
status: pending
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

- [ ] `docs/template-conversion-map.md` liệt kê đủ 84 file Blade, không thiếu file nào.
- [ ] 3 template auth của Phase 7 chạy trên `layouts/admin_auth.html` thật, giao diện khớp ảnh chụp bản Laravel.
- [ ] Mọi macro render được với dữ liệu giả, test pass.
- [ ] `seo-head.html` render đủ mọi thẻ có trong `app.blade.php:45-90`; test đối chiếu danh sách thẻ pass.
- [ ] `build_seo_context` có test cho 4 tình huống ảnh OG (mặc định / canonical tuỳ chỉnh / ảnh tương đối / ảnh URL tuyệt đối).
- [ ] `layouts/admin.html` và `layouts/admin_auth.html` đều có `<meta name="csrf-token">`.
- [ ] `curl /static/assets/images/logo.svg` trả 200 qua nginx.
- [ ] Diff CSS: `partials/client/styles.html` so với `styles.blade.php` chỉ khác ở thẻ bọc, phần `<style>` giống hệt (kiểm bằng `diff` sau khi bóc thẻ).
- [ ] JavaScript trong `partials/client/scripts.html` giống hệt bản Blade sau khi thay các điểm nội suy (danh sách điểm nội suy được liệt kê trong PR).
- [ ] `grep -r "| safe" templates/` chỉ trả về đúng 1 kết quả: khối JSON-LD trong `seo-head.html`. Bất kỳ `| safe` nào khác phải được giải trình trong PR.

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
