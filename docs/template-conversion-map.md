# Bảng đối chiếu Blade → Jinja2

Checklist thi công cho Phase 9 (Client Area) và Phase 10 (Admin Area), và bằng
chứng phạm vi cho Phase 11 (Testing & Parity Verification). Liệt kê đủ 84 file
`.blade.php` trong `resources/views/` tính đến khi Phase 8 bắt đầu
(`find resources/views -name "*.blade.php" | wc -l` → 84).

Cây đích phản chiếu cây Blade — xem `plans/260827-0051-migrate-laravel-to-fastapi-clean-architecture/phase-08-jinja2-template-foundation.md`.

## Layout & component dùng chung (17 file) — Phase 8, đã xong

| Blade | Jinja2 đích | Trạng thái | Ghi chú |
|---|---|---|---|
| `components/client/layout/app.blade.php` | `layouts/client.html` + `partials/client/seo-head.html` | Xong | SEO `@php` block chuyển sang `presentation/web/seo.py` |
| `components/client/layout/navbar.blade.php` | `partials/client/navbar.html` | Xong | |
| `components/client/layout/footer.blade.php` | `partials/client/footer.html` | Xong | Bỏ query DB ẩn trong `@php`; `categories`/`contacts` nay là biến ngữ cảnh tường minh — route/use case của Phase 9 phải truyền vào |
| `components/client/layout/back-to-top.blade.php` | `partials/client/back-to-top.html` | Xong | Copy nguyên, không có Blade directive |
| `components/client/layout/styles.blade.php` | `partials/client/styles.html` | Xong | Copy CSS nguyên văn, chỉ đổi tên file |
| `components/client/layout/scripts.blade.php` | `partials/client/scripts.html` | Xong | Copy JS nguyên văn — không có điểm nội suy Blade nào trong file gốc |
| `components/admin/layout/app.blade.php` | `layouts/admin.html` | Xong | Giữ `<meta name="csrf-token">`; header title dùng `self.title()` |
| `components/admin/layout/auth.blade.php` | `layouts/admin_auth.html` | Xong | 3 template auth Phase 7 đã retrofit sang layout này |
| `components/admin/layout/sidebar.blade.php` | `partials/admin/sidebar.html` | Xong | `request()->routeIs()` → global `is_route()` |
| `components/client/shared/figure-card.blade.php` | `macros/cards.html` (`figure_card`) | Xong | `featured` nay là tham số tường minh, không tự suy luận relation |
| `components/client/shared/story-card.blade.php` | `macros/cards.html` (`story_card`) | Xong | 1 trong 2 chỗ `\| safe` đã xác minh an toàn (SVG hardcode) |
| `components/client/shared/content-blocks.blade.php` | `macros/content.html` (`content_blocks`) | Xong | |
| `components/client/shared/audio-player.blade.php` | `macros/media.html` (`audio_player`) | Xong | |
| `components/client/shared/category-pills.blade.php` | `macros/nav.html` (`category_pills`) | Xong | |
| `components/client/shared/pagination.blade.php` | `macros/nav.html` (`pagination`) | Xong | Dùng `Page.window()` (Phase 2) thay vì hiện toàn bộ số trang như bản gốc |
| `components/client/shared/share-buttons.blade.php` | `macros/nav.html` (`share_buttons`) | Xong | URL nội suy qua `\| tojson`, không dùng `{{ }}` trần trong JS attribute |
| — (mới, không có trong Blade) | `macros/forms.html` | Xong | DRY cho form admin — copy markup thật từ `admin/categories/form.blade.php` v.v. rồi tham số hoá |

## Trang Client (31 file) — Phase 9, chờ thi công

| Blade | Jinja2 đích | Trạng thái |
|---|---|---|
| `client/home/index.blade.php` | `client/home/index.html` | Chờ Phase 9 |
| `client/home/_how-it-works.blade.php` | `client/home/_how-it-works.html` | Chờ Phase 9 |
| `client/home/_media-badges.blade.php` | `client/home/_media-badges.html` | Chờ Phase 9 |
| `client/home/_newsletter.blade.php` | `client/home/_newsletter.html` | Chờ Phase 9 |
| `client/home/_quote-section.blade.php` | `client/home/_quote-section.html` | Chờ Phase 9 |
| `client/category/index.blade.php` | `client/category/index.html` | Chờ Phase 9 |
| `client/figure/show.blade.php` | `client/figure/show.html` | Chờ Phase 9 |
| `client/figure/_key-facts.blade.php` | `client/figure/_key-facts.html` | Chờ Phase 9 |
| `client/figure/_reading-progress-script.blade.php` | `client/figure/_reading-progress-script.html` | Chờ Phase 9 |
| `client/figure/_related-figures-section.blade.php` | `client/figure/_related-figures-section.html` | Chờ Phase 9 |
| `client/figure/_story-snippets-section.blade.php` | `client/figure/_story-snippets-section.html` | Chờ Phase 9 |
| `client/story/show.blade.php` | `client/story/show.html` | Chờ Phase 9 |
| `client/story/_other-stories-section.blade.php` | `client/story/_other-stories-section.html` | Chờ Phase 9 |
| `client/search/index.blade.php` | `client/search/index.html` | Chờ Phase 9 |
| `client/search/_category-pills.blade.php` | `client/search/_category-pills.html` | Chờ Phase 9 |
| `client/search/_popular-trending.blade.php` | `client/search/_popular-trending.html` | Chờ Phase 9 |
| `client/search/_results.blade.php` | `client/search/_results.html` | Chờ Phase 9 |
| `client/search/_search-form.blade.php` | `client/search/_search-form.html` | Chờ Phase 9 |
| `client/about-us/index.blade.php` | `client/about-us/index.html` | Chờ Phase 9 |
| `client/about-us/_audience.blade.php` | `client/about-us/_audience.html` | Chờ Phase 9 |
| `client/about-us/_core-values.blade.php` | `client/about-us/_core-values.html` | Chờ Phase 9 |
| `client/about-us/_cta.blade.php` | `client/about-us/_cta.html` | Chờ Phase 9 |
| `client/about-us/_hero.blade.php` | `client/about-us/_hero.html` | Chờ Phase 9 |
| `client/about-us/_problem-solution.blade.php` | `client/about-us/_problem-solution.html` | Chờ Phase 9 |
| `client/about-us/_stats.blade.php` | `client/about-us/_stats.html` | Chờ Phase 9 |
| `client/contact/index.blade.php` | `client/contact/index.html` | Chờ Phase 9 |
| `client/contact/_buy-me-a-coffee.blade.php` | `client/contact/_buy-me-a-coffee.html` | Chờ Phase 9 |
| `client/contact/_contact-info.blade.php` | `client/contact/_contact-info.html` | Chờ Phase 9 |
| `client/contact/_cta.blade.php` | `client/contact/_cta.html` | Chờ Phase 9 |
| `client/contact/_hero.blade.php` | `client/contact/_hero.html` | Chờ Phase 9 |
| `client/contact/_services.blade.php` | `client/contact/_services.html` | Chờ Phase 9 |

## Trang Admin (36 file) — Phase 10, chờ thi công (trừ auth + dashboard)

| Blade | Jinja2 đích | Trạng thái |
|---|---|---|
| `admin/auth/login.blade.php` | `admin/auth/login.html` | Xong (Phase 7, retrofit layout ở Phase 8) |
| `admin/auth/forgot-password.blade.php` | `admin/auth/forgot-password.html` | Xong (Phase 7, retrofit layout ở Phase 8) |
| `admin/auth/reset.blade.php` | `admin/auth/reset.html` | Xong (Phase 7, retrofit layout ở Phase 8) |
| `admin/dashboard.blade.php` | `admin/dashboard.html` | Khung xong (Phase 8: layout đúng); thống kê thật ở Phase 10 |
| `admin/categories/form.blade.php` | `admin/categories/form.html` | Chờ Phase 10 |
| `admin/categories/index.blade.php` | `admin/categories/index.html` | Chờ Phase 10 |
| `admin/contacts/form.blade.php` | `admin/contacts/form.html` | Chờ Phase 10 |
| `admin/contacts/index.blade.php` | `admin/contacts/index.html` | Chờ Phase 10 |
| `admin/featured-figures/index.blade.php` | `admin/featured-figures/index.html` | Chờ Phase 10 |
| `admin/figures/form.blade.php` | `admin/figures/form.html` | Chờ Phase 10 |
| `admin/figures/index.blade.php` | `admin/figures/index.html` | Chờ Phase 10 |
| `admin/figures/partials/actions-card.blade.php` | `admin/figures/partials/actions-card.html` | Chờ Phase 10 |
| `admin/figures/partials/basic-info-card.blade.php` | `admin/figures/partials/basic-info-card.html` | Chờ Phase 10 |
| `admin/figures/partials/categories-card.blade.php` | `admin/figures/partials/categories-card.html` | Chờ Phase 10 |
| `admin/figures/partials/content-blocks-card.blade.php` | `admin/figures/partials/content-blocks-card.html` | Chờ Phase 10 |
| `admin/figures/partials/content-blocks-script.blade.php` | `admin/figures/partials/content-blocks-script.html` | Chờ Phase 10 — JS nội suy cần rà theo rủi ro Phase 8 |
| `admin/figures/partials/copy-prompt-card.blade.php` | `admin/figures/partials/copy-prompt-card.html` | Chờ Phase 10 |
| `admin/figures/partials/key-facts-card.blade.php` | `admin/figures/partials/key-facts-card.html` | Chờ Phase 10 |
| `admin/figures/partials/media-card.blade.php` | `admin/figures/partials/media-card.html` | Chờ Phase 10 |
| `admin/partials/audio-generator.blade.php` | `admin/partials/audio-generator.html` | Chờ Phase 10 — dùng `@json()`, cần `\| tojson` |
| `admin/settings/about-us.blade.php` | `admin/settings/about-us.html` | Chờ Phase 10 |
| `admin/settings/partials/audience-section.blade.php` | `admin/settings/partials/audience-section.html` | Chờ Phase 10 |
| `admin/settings/partials/core-values-section.blade.php` | `admin/settings/partials/core-values-section.html` | Chờ Phase 10 |
| `admin/settings/partials/cta-section.blade.php` | `admin/settings/partials/cta-section.html` | Chờ Phase 10 |
| `admin/settings/partials/hero-section.blade.php` | `admin/settings/partials/hero-section.html` | Chờ Phase 10 |
| `admin/settings/partials/problem-solution-section.blade.php` | `admin/settings/partials/problem-solution-section.html` | Chờ Phase 10 |
| `admin/settings/partials/stats-section.blade.php` | `admin/settings/partials/stats-section.html` | Chờ Phase 10 |
| `admin/stories/form.blade.php` | `admin/stories/form.html` | Chờ Phase 10 |
| `admin/stories/index.blade.php` | `admin/stories/index.html` | Chờ Phase 10 |
| `admin/stories/partials/actions-card.blade.php` | `admin/stories/partials/actions-card.html` | Chờ Phase 10 |
| `admin/stories/partials/basic-info-card.blade.php` | `admin/stories/partials/basic-info-card.html` | Chờ Phase 10 |
| `admin/stories/partials/content-blocks-card.blade.php` | `admin/stories/partials/content-blocks-card.html` | Chờ Phase 10 |
| `admin/stories/partials/content-blocks-script.blade.php` | `admin/stories/partials/content-blocks-script.html` | Chờ Phase 10 |
| `admin/stories/partials/media-card.blade.php` | `admin/stories/partials/media-card.html` | Chờ Phase 10 |
| `admin/users/create.blade.php` | `admin/users/create.html` | Chờ Phase 10 |
| `admin/users/edit.blade.php` | `admin/users/edit.html` | Chờ Phase 10 |
| `admin/users/index.blade.php` | `admin/users/index.html` | Chờ Phase 10 |

## Tổng kết

- 84/84 file đã liệt kê.
- 17/17 file layout & component dùng chung: xong (Phase 8).
- 3/3 template auth + khung dashboard: xong (Phase 7 nội dung, Phase 8 layout).
- 31 trang client + 33 trang/partial admin còn lại (không tính auth+dashboard): chờ Phase 9/10.
- `macros/forms.html` là bổ sung mới (DRY), không map 1-1 với file Blade nào.
