---
title: "Migrate Laravel to FastAPI Clean Architecture"
description: "Thay toàn bộ stack PHP/Laravel 12 bằng Python 3.14 + FastAPI + Jinja2 theo Clean Architecture, giữ nguyên 100% giao diện, luồng nghiệp vụ và dữ liệu; làm sạch schema database và loại bỏ hoàn toàn PHP."
status: pending
priority: P1
effort: "20-26d"
branch: "migrate/fastapi"
tags: [migration, fastapi, python314, clean-architecture, jinja2, database-cleanup]
created: 2026-08-27
blockedBy: []
blocks: []
---

# Migrate Laravel to FastAPI Clean Architecture

## Overview

The Admirable hiện chạy Laravel 12 / PHP 8.2 với Service Pattern, Blade templates, Tailwind CDN, Vanilla JS, MySQL và Laravel database queue cho Azure TTS. Kế hoạch này thay toàn bộ stack sang **Python 3.14 + FastAPI + Jinja2**, tổ chức lại theo **Clean Architecture** 4 lớp, giữ **nguyên vẹn giao diện và mọi route công khai**, giữ **100% dữ liệu và media hiện có**, làm sạch schema database, và xoá sạch mọi dấu vết PHP/Laravel khỏi repo.

Đây là một cuộc thay thế toàn bộ (rewrite), không phải refactor tăng dần. Ranh giới nghiệp vụ được giữ nguyên 1:1; chỉ thay đổi công nghệ thực thi và cách phân lớp.

## Quyết định đã chốt

| Hạng mục | Quyết định | Nguồn |
|---|---|---|
| Runtime | Python 3.14 (`py -3.14`, đã có sẵn 3.14.6 trên máy dev) | User |
| Web framework | FastAPI + Jinja2 (server-rendered, không SPA) | User |
| Kiến trúc | Clean Architecture: `domain` → `application` → `infrastructure` → `presentation` | User |
| Deploy | VPS + Docker Compose (nginx + uvicorn + worker + MySQL + Redis) | User |
| Dữ liệu | Giữ nguyên 100%; script migrate có backup + rollback | User |
| Background job | **Taskiq + Redis** (ARQ đã chuyển sang maintenance-only) | User (sau research) |
| TTS | **edge-tts** (Python, miễn phí, không cần API key) thay Azure Cognitive Speech | User |
| DB cleanup | Drop 7 bảng hạ tầng Laravel + gộp cột trùng lặp | User |
| ORM | SQLAlchemy 2.0 async + `asyncmy` + Alembic | Plan (xem Phase 4) |
| Git | Cùng repo, branch riêng `migrate/fastapi`, merge vào `main` ở Phase 12 | User (Validation S1) |
| Tầng SEO | `presentation/web/seo.py` — `SeoMeta` dataclass + builder JSON-LD | User (Validation S1) |
| Email | `LogMailer` (giữ hiện trạng `MAIL_MAILER=log`); `SmtpMailer` viết sẵn, bật bằng env | User (Validation S1) |
| Coverage | domain ≥90%, application ≥85%, **presentation ≥70%**, tổng ≥75% | User (Validation S1) |

## Goals

| # | Goal | Priority |
|---|------|----------|
| 1 | Loại bỏ hoàn toàn PHP/Laravel khỏi repo và runtime | P1 |
| 2 | Giữ nguyên 100% giao diện, URL, và hành vi người dùng (client + admin) | P1 |
| 3 | Giữ nguyên 100% dữ liệu nghiệp vụ và file media hiện có | P1 |
| 4 | Áp dụng Clean Architecture với ranh giới lớp được kiểm chứng bằng test | P1 |
| 5 | Làm sạch schema: drop bảng hạ tầng, gộp cột trùng lặp | P1 |
| 6 | Thay Azure TTS bằng edge-tts, giữ nguyên state machine sinh audio | P2 |
| 7 | Deploy được bằng một lệnh `docker compose up` trên VPS | P2 |

## Non-goals

- Không thay đổi thiết kế UI, bảng màu, hay bố cục trang nào.
- Không thêm tính năng nghiệp vụ mới.
- Không chuyển sang SPA / build tool Node (giữ Tailwind CDN + Vanilla JS như hiện tại).
- Không đổi cấu trúc URL công khai (SEO phải giữ nguyên).
- Không gộp `featured_figures` vào `figures` (đã loại ở bước scope challenge).

## Kiến trúc đích

```
src/admirable/
├── domain/              # Lớp 1 — thuần Python, ZERO import framework
│   ├── entities/        # Figure, Category, StorySnippet, Contact, User, Setting, FeaturedFigure
│   ├── value_objects/   # ContentBlock, KeyFact, Slug, AudioStatus, Role, AboutUsContent
│   ├── repositories/    # Interface (Protocol) cho mỗi aggregate
│   └── exceptions.py
├── application/         # Lớp 2 — use case, chỉ phụ thuộc domain
│   ├── use_cases/       # thay thế 9 class trong app/Services
│   ├── dto/             # Pydantic input/output model
│   └── ports/           # TextToSpeechPort, FileStoragePort, TaskQueuePort, PasswordHasherPort, MailerPort, SessionStorePort
├── infrastructure/      # Lớp 3 — hiện thực hoá port + repository
│   ├── db/              # SQLAlchemy models, session, repositories, mappers
│   ├── tts/             # EdgeTtsAdapter
│   ├── storage/         # LocalFileStorage
│   ├── queue/           # Taskiq broker + task
│   ├── security/        # BcryptPasswordHasher, RedisSessionStore, CSRF
│   └── mail/            # LogMailer (mặc định) + SmtpMailer
└── presentation/        # Lớp 4 — HTTP + template
    ├── web/
    │   ├── main.py, dependencies.py, middleware/, forms/
    │   ├── seo.py       # SeoMeta + builder JSON-LD (thay khối @php trong layout Blade)
    │   ├── routers/client/  ·  routers/admin/
    │   └── templates/       # Jinja2, ánh xạ 1:1 cây Blade hiện tại
    └── cli/             # seed, create-superadmin, reindex-search
```

**Quy tắc phụ thuộc (bắt buộc, có test enforce ở Phase 11):** mũi tên phụ thuộc chỉ đi vào trong. `domain` không import gì ngoài stdlib. `application` chỉ import `domain`. `infrastructure` và `presentation` được import mọi thứ nhưng không import lẫn nhau ngược chiều.

## Phases

| # | Phase | Trọng tâm | Status |
|---|-------|-----------|--------|
| 1 | [Nền tảng & Tooling](./phase-01-foundation-tooling.md) | Python 3.14, uv, Docker Compose, khung thư mục, config | Completed |
| 2 | [Lớp Domain](./phase-02-domain-layer.md) | Entity, value object, repository interface | Pending |
| 3 | [Schema sạch & Migrate dữ liệu](./phase-03-database-schema-data-migration.md) | Alembic baseline, drop bảng, script migrate + rollback | Pending |
| 4 | [Hạ tầng Persistence](./phase-04-persistence-infrastructure.md) | SQLAlchemy async, ORM model, repository impl | Pending |
| 5 | [Lớp Application](./phase-05-application-use-cases.md) | Toàn bộ use case thay 9 Laravel service | Pending |
| 6 | [Adapter: TTS, Queue, Storage](./phase-06-adapters-tts-queue-storage.md) | edge-tts, Taskiq worker, file storage, bcrypt | Pending |
| 7 | [Web core & Auth](./phase-07-web-core-auth.md) | App factory, DI, session, CSRF, method-override, auth | Pending |
| 8 | [Nền tảng Template Jinja2](./phase-08-jinja2-template-foundation.md) | Layout, macro, component dùng chung, helper | Pending |
| 9 | [Khu vực Client](./phase-09-client-area.md) | 8 route công khai + template | Pending |
| 10 | [Khu vực Admin](./phase-10-admin-area.md) | Toàn bộ CRUD + audio endpoint + settings | Pending |
| 11 | [Kiểm thử & Đối chiếu ngang bằng](./phase-11-testing-parity-verification.md) | pytest, route parity, HTML diff, kiểm tra ranh giới lớp | Pending |
| 12 | [Deploy & Xoá Laravel](./phase-12-deploy-and-laravel-removal.md) | Nginx, cutover production, xoá PHP, cập nhật docs | Pending |

**Phụ thuộc:** 1 → 2 → {3, 4} → 5 → {6, 7} → 8 → {9, 10} → 11 → 12.
Phase 3 và 4 có thể chạy song song sau Phase 2. Phase 9 và 10 có thể chạy song song sau Phase 8.

## Bản đồ chuyển đổi (Laravel → FastAPI)

| Laravel | Thay bằng | Ghi chú |
|---|---|---|
| `app/Http/Controllers/**` | `presentation/web/routers/**` | Giữ nguyên tên route (`admin.figures.index`, ...) |
| `app/Services/**` (9 class) | `application/use_cases/**` | Tách nhỏ theo hành động, không còn god-service |
| `app/Models/**` (Eloquent) | `domain/entities` + `infrastructure/db/models` | Tách entity nghiệp vụ khỏi bảng DB |
| `app/Http/Requests/**` (8 class) | `presentation/web/forms/**` | Pydantic model + hàm parse form |
| `app/Http/Middleware/RoleMiddleware` | FastAPI dependency `require_role(...)` | |
| `app/Jobs/GenerateAudioJob` | `infrastructure/queue/tasks.py` | Taskiq task |
| `app/Services/AzureTextToSpeechService` | `infrastructure/tts/edge_tts_adapter.py` | Không cần API key |
| `app/Helpers/FileUploadHelper` | `infrastructure/storage/local_storage.py` | Hiện thực `FileStoragePort` |
| `resources/views/**` (84 file Blade) | `presentation/web/templates/**` | Cấu trúc thư mục giữ nguyên |
| `database/migrations/**` | `migrations/versions/**` (Alembic) | Baseline mới, không port từng migration |
| `database/seeders/**` | `presentation/cli/seed.py` | |
| Laravel database queue | Taskiq + Redis | |
| Laravel session (bảng `sessions`) | Redis session store | Cho phép drop bảng `sessions` |
| Laravel `password_reset_tokens` | Redis key có TTL 60 phút | Cho phép drop bảng |
| `php artisan serve` | `uvicorn` (dev: `--reload`) | |
| `php artisan queue:listen` | `taskiq worker` | |
| Pest 3 | pytest + pytest-asyncio | |
| Laravel Pint | Ruff (format + lint) + mypy | |

## Thay đổi Database

**Drop hoàn toàn (7 bảng hạ tầng Laravel):**
`cache`, `cache_locks`, `jobs`, `job_batches`, `failed_jobs`, `sessions`, `password_reset_tokens`

**Bảng nghiệp vụ giữ lại (8):** `users`, `categories`, `figures`, `category_figure`, `story_snippets`, `settings`, `contacts`, `featured_figures`

**Gộp/dọn cột:**

| Bảng | Thay đổi | Lý do |
|---|---|---|
| `figures` | Bỏ `content` (longtext) → thay bằng `search_text` (text, do app duy trì) + FULLTEXT index (ngram parser) | `content` là bản sao text thuần của `content_blocks`, chỉ dùng để search |
| `story_snippets` | Tương tự: `content` → `search_text` | Như trên |
| `users` | Bỏ `email_verified_at`, `remember_token` | Không có luồng xác minh email; "remember me" chuyển sang TTL của Redis session |
| `figures`, `story_snippets` | `audio_status` chuyển sang ENUM chuẩn `idle\|processing\|completed\|failed\|cancelled` | Code hiện tại set `'cancelled'` nhưng tài liệu chỉ ghi 4 trạng thái — chuẩn hoá lại |

## Success Criteria

- [ ] Không còn file `.php`, `composer.json`, thư mục thư viện PHP, `artisan` trong repo (kiểm chứng bằng `git ls-files '*.php'` trả về rỗng).
- [ ] Toàn bộ 8 route client và 30+ route admin phản hồi đúng status code và render đúng template (bảng đối chiếu ở Phase 11).
- [ ] So sánh HTML render của cả hai hệ thống trên cùng bộ dữ liệu: khác biệt chỉ ở whitespace/CSRF token (Phase 11).
- [ ] Số bản ghi mỗi bảng nghiệp vụ sau migrate khớp 100% với DB nguồn; mọi file trong `uploads/` đều truy cập được.
- [ ] Đăng nhập bằng mật khẩu bcrypt cũ vẫn hoạt động, không cần reset.
- [ ] Sinh audio bằng edge-tts chạy được đủ vòng đời `idle → processing → completed`, và huỷ được giữa chừng.
- [ ] Test ranh giới lớp pass: `domain` không import `sqlalchemy`/`fastapi`; `application` không import `infrastructure`.
- [ ] Thẻ SEO khớp 100%: `<title>`, OG, Twitter card, `article:*`, canonical, và mọi khối JSON-LD (Phase 9).
- [ ] Coverage đạt: domain ≥90%, application ≥85%, presentation ≥70%, tổng ≥75%.
- [ ] `docker compose up -d` dựng được toàn bộ hệ thống từ zero trên VPS sạch.
- [ ] `ruff check`, `ruff format --check`, `mypy src` đều pass.
- [ ] Branch `migrate/fastapi` merge sạch vào `main` sau khi Phase 11 pass.
- [ ] Docs (`README.md`, `AGENTS.md`, `docs/rules.md`, `docs/page-sitemap.md`, `docs/superadmin_account.md`) phản ánh đúng stack mới.

## Rủi ro chính

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Mất dữ liệu khi cutover | Cao | Dump full DB + `tar` media trước mỗi lần chạy; migrate vào DB *mới* (không ghi đè DB cũ); giữ DB cũ read-only tối thiểu 14 ngày |
| Giao diện lệch sau khi chuyển Blade→Jinja2 | Cao | Chuyển đổi cơ học từng file + so sánh HTML tự động ở Phase 11 |
| edge-tts phụ thuộc endpoint không chính thức của Microsoft, có thể đổi/chặn IP | Trung bình | Bọc sau `TextToSpeechPort`; nếu hỏng, thay adapter mà không đụng use case. Tín hiệu: tỉ lệ `failed` > 20% trong 24h → cân nhắc quay lại Azure hoặc Piper (offline) |
| FULLTEXT tiếng Việt tokenize khác `LIKE %...%` hiện tại | Trung bình | Dùng ngram parser + giữ nhánh fallback `LIKE` cho truy vấn ngắn; đối chiếu kết quả search hai hệ thống ở Phase 11 |
| Thư viện chưa có wheel cho Python 3.14 | Thấp | Đã xác minh: SQLAlchemy 2.0.52, asyncmy 0.2.14, pydantic 2.13, FastAPI đều có wheel cp314 (8/2026). Phase 1 chốt lockfile trước khi viết code |
| Hosting hiện tại (cPanel) không chạy được ASGI | Đã xử lý | Chuyển sang VPS + Docker (quyết định đã chốt) |

## Câu hỏi còn mở

Cả ba câu còn lại đều chỉ chặn Phase 12, không chặn Phase 1-11.

1. VPS đích đã có sẵn chưa (IP, OS, RAM)? Cần biết trước Phase 12 để viết đúng file compose/nginx.
2. Tên miền production và chứng chỉ TLS xử lý ở đâu (Let's Encrypt qua nginx, hay Cloudflare proxy)?
3. Chấp nhận downtime bao lâu cho cutover ở Phase 12?

~~Có cần gửi email thật không?~~ → Đã chốt ở Validation Session 1: giữ `LogMailer`.

## Validation Log

### Session 1 — 2026-08-27
**Trigger:** `/ak-plan validate` ngay sau khi tạo plan, trước khi implement.
**Tier:** Full (12 phases, 4 verification roles)
**Questions asked:** 4

#### Verification Results

- **Claims checked:** 62
- **Verified:** 62 | **Failed:** 0 | **Unverified:** 0

Không có claim nào sai, nhưng 4 phát hiện làm plan phải sửa:

1. **[Fact Checker] Tầng SEO bị bỏ sót hoàn toàn.** `resources/views/components/client/layout/app.blade.php:1-40` khai báo 14 `@props` SEO (`canonicalUrl`, `ogType`, `ogImage`, `robots`, `keywords`, `publishedTime`, `modifiedTime`, `articleSection`, `articleTags`, `jsonLd`…) rồi tính `$seoCanonical`, `$seoImage`, `$seoLocale` và merge schema JSON-LD `WebSite` mặc định (kèm `SearchAction`) với schema riêng từng trang (`app.blade.php:85`). Plan gốc chỉ ghi "giữ nguyên thẻ meta".
2. **[Fact Checker] `<meta name="csrf-token">` chưa được liệt kê.** Có ở `components/admin/layout/app.blade.php:6` và `auth.blade.php:6`; JS đọc trực tiếp tại `admin/featured-figures/index.blade.php:156`, `admin/partials/audio-generator.blade.php:215,245`.
3. **[Flow Tracer] Rủi ro `{!! !!}` ở Phase 8 không tồn tại.** Chỉ có 2 chỗ trong toàn bộ 84 file Blade: `app.blade.php:85` (JSON-LD qua `json_encode`) và `story-card.blade.php:16` (`$icon` lấy từ mảng SVG hardcode tại `story-card.blade.php:4`, chọn bằng `$snippet->id % count($icons)`). Không có dữ liệu người dùng nào được render thô → không có vector XSS.
4. **[Flow Tracer] `audio-generator.blade.php` không xử lý mã 422.** Chỉ xử lý 409 (`:219`, `:249`) và các giá trị `status` gồm `'cancelled'` (`:186`). Việc bỏ Azure **không cần sửa JS dòng nào**; đồng thời xác nhận `cancelled` là trạng thái UI chính thức, củng cố quyết định đưa vào ENUM.

Các claim đã xác minh khác: 84 file Blade, 9 service, 8 Form Request, 17 file controller; `@method(...)` dùng ở 11 chỗ (`categories`, `contacts`, `featured-figures`, `figures`, `stories`, `users`); `asset('storage/...)` dùng 17 chỗ; `AudioController.php:58` set `'cancelled'`; `HomeController.php:24,37,43` chứa thuật toán bù featured; `SearchController.php:22,40,53` chứa toàn bộ logic search; `BCRYPT_ROUNDS=12`, `SESSION_LIFETIME=120`, `MAIL_MAILER=log` trong `.env.example`; JS sinh field `content_blocks[${idx}][text_en]` và `key_facts[${idx}][label]` đúng như giả định của `unflatten_form_data`.

#### Questions & Answers

1. **[Architecture]** Tầng SEO (14 prop + JSON-LD schema) nên đặt ở đâu trong Clean Architecture?
   - Options: `presentation/web/seo.py` (Recommended) | Giữ nguyên trong template Jinja2 | Đưa vào read-model DTO của use case
   - **Answer:** `presentation/web/seo.py`
   - **Rationale:** SEO là chi tiết trình bày HTML, không phải nghiệp vụ. Đặt ở presentation giữ được ranh giới lớp mà vẫn test tự động được — khác với phương án để trong template.

2. **[Scope]** Code Python dựng ở đâu trong giai đoạn chuyển đổi?
   - Options: Cùng repo, cùng branch main (Recommended) | Cùng repo, branch riêng | Repo mới hoàn toàn
   - **Answer:** Cùng repo, branch riêng `migrate/fastapi`
   - **Rationale:** `main` luôn giữ được bản Laravel chạy production trong suốt 3-4 tuần chuyển đổi. Đổi lại, việc đối chiếu song song ở Phase 11 phải dùng hai git worktree, và Phase 12 có thêm bước merge.

3. **[Assumptions]** Ngưỡng coverage domain ≥90% / application ≥85% / tổng ≥75% là giả định của planner.
   - Options: Giữ nguyên (Recommended) | Hạ xuống: chỉ domain ≥90% | Nâng lên: thêm ngưỡng cho presentation
   - **Answer:** Nâng lên — thêm ngưỡng presentation ≥70%
   - **Rationale:** Phủ cả router và template render. Đội thêm ~2 ngày (effort 18-24d → 20-26d) nhưng bắt được lỗi mà HTML parity không thấy: nhánh lỗi, phân quyền, validation.

4. **[Risks]** Chức năng quên mật khẩu có cần gửi email thật không?
   - Options: Giữ LogMailer (Recommended) | Cần SMTP thật | Bỏ luôn luồng quên mật khẩu
   - **Answer:** Giữ LogMailer
   - **Rationale:** Giữ đúng hiện trạng, không cắt tính năng nào. `SmtpMailer` vẫn được viết ở Phase 6 và bật được bằng `MAIL__DRIVER` mà không cần đụng code.

#### Confirmed Decisions

- **SEO** → module `presentation/web/seo.py`, mỗi router client dựng `SeoMeta` từ DTO.
- **Git** → branch `migrate/fastapi`, merge vào `main` ở Phase 12 sau khi Phase 11 pass.
- **Coverage** → thêm ngưỡng presentation ≥70%; effort tổng tăng lên 20-26 ngày.
- **Email** → `LogMailer` mặc định, `SmtpMailer` viết sẵn nhưng không bật.
- **JS audio** → không cần sửa (đã xác minh không phụ thuộc mã 422 của Azure).
- **`{!! !!}`** → cả 2 chỗ an toàn, không phải rủi ro bảo mật.

#### Impact on Phases

- **Phase 1:** thêm bước tạo branch `migrate/fastapi`.
- **Phase 6:** xác nhận `LogMailer` là mặc định (không đổi nội dung).
- **Phase 7:** layout admin phải render `<meta name="csrf-token">`.
- **Phase 8:** thêm `seo.py` + `<meta name="csrf-token">`; hạ cấp rủi ro `{!! !!}` thành đã xác minh an toàn.
- **Phase 9:** mỗi route client dựng `SeoMeta`; thêm tiêu chí đối chiếu JSON-LD.
- **Phase 10:** ghi rõ JS audio không cần sửa.
- **Phase 11:** thêm ngưỡng coverage presentation; parity dùng hai git worktree; so `<head>` và JSON-LD riêng; bước dọn worktree.
- **Phase 12:** thêm bước merge branch vào `main` (bước 0) + tag `migration/pre-removal`.

### Whole-Plan Consistency Sweep

- **Files reread:** `plan.md` + 12 file `phase-*.md`
- **Decision deltas checked:** 6 (SEO module, branch riêng, coverage presentation, LogMailer, JS audio không đổi, `{!! !!}` an toàn)
- **Reconciled stale references:** 3
  1. `phase-10:32` — mục Requirements vẫn ghi *"Endpoint audio trả đúng mã HTTP hiện tại: 409 khi đang chạy, **422 khi lỗi cấu hình**, 200 khi OK"*, mâu thuẫn với bước 11 cùng file (bỏ nhánh 422). Đã sửa thành 200/409 và tách rõ lỗi edge-tts là bất đồng bộ.
  2. `phase-08:44` — bảng chuyển đổi vẫn ghi `{!! !!}` → `| safe` kèm *"rà từng chỗ, chỉ dùng khi thật sự cần"*, ngụ ý còn nhiều chỗ chưa rõ. Đã sửa thành "đúng 2 chỗ, cả hai đã xác minh".
  3. `phase-08` Success Criteria — tiêu chí cũ dựa trên việc "ghi chú lý do cho từng `| safe`" nay vô nghĩa. Thay bằng tiêu chí kiểm được: `grep "| safe"` chỉ được trả về 1 kết quả (JSON-LD).
- **Unresolved contradictions:** 0

Đã kiểm tra và xác nhận **không** stale: ngưỡng coverage (nhất quán ở `plan.md` và `phase-11`), tham chiếu `LogMailer`/`MAIL__DRIVER` (`phase-05`, `phase-06`), branch `migrate/fastapi` (`phase-01`, `phase-11`, `phase-12`), `<meta name="csrf-token">` (`phase-07`, `phase-08`, `phase-10`), tầng SEO (`phase-08`, `phase-09`, `phase-11`). Mã `422` còn lại ở `phase-07:62` là cho lỗi validation form — không liên quan Azure, giữ nguyên đúng.

<!-- slug: migrate-laravel-to-fastapi-clean-architecture -->
