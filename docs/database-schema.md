# Database Schema (target: `admirable`)

Defined by `migrations/versions/0001_baseline_schema.py` (Alembic). Charset
`utf8mb4`, collation `utf8mb4_unicode_ci`, engine InnoDB on every table.

## Tables

### `categories`
| Column | Type | Notes |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| name | VARCHAR(255) NOT NULL | |
| slug | VARCHAR(255) UNIQUE NOT NULL | |
| created_at, updated_at | DATETIME | |

### `figures`
| Column | Type | Notes |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| name | VARCHAR(255) NOT NULL | |
| slug | VARCHAR(255) UNIQUE NOT NULL | |
| avatar_path | VARCHAR(255) NULL | relative to `media/` |
| short_description | TEXT NULL | |
| key_facts | JSON NULL | `[{"label":..,"value":..}]` |
| content_blocks | JSON NULL | `[{"type":"heading"\|"paragraph"\|"quote", ...}]` |
| search_text | TEXT NULL | rebuilt from `content_blocks` (EN+VI), not copied from the old `content` column |
| audio_path | VARCHAR(255) NULL | relative to `media/` |
| audio_status | ENUM(idle,processing,completed,failed,cancelled) NOT NULL DEFAULT idle | |
| audio_error | VARCHAR(500) NULL | truncated to 500 chars |
| youtube_url | VARCHAR(255) NULL | |
| created_at, updated_at | DATETIME | |

FULLTEXT `ft_figures_search (name, short_description, search_text)` with the
`ngram` parser. See `docs/rules.md` for the query fallback strategy (`LIKE`
for short queries).

### `category_figure`
Composite PK (`category_id`, `figure_id`), both `ON DELETE CASCADE`.

### `story_snippets`
Same shape as `figures` minus `avatar_path`/`key_facts`, plus `figure_id`
(`ON DELETE CASCADE`), `title`, `subtitle`, `image_path`. FULLTEXT
`ft_story_snippets_search (title, subtitle, search_text)` with `ngram`.

### `featured_figures`
| Column | Type | Notes |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| figure_id | BIGINT UNIQUE, FK → figures.id ON DELETE CASCADE | one row per figure |
| priority | INT NOT NULL DEFAULT 0 | lower sorts first |
| created_at, updated_at | DATETIME | |

### `users`
| Column | Type | Notes |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| name | VARCHAR(255) NOT NULL | |
| email | VARCHAR(255) UNIQUE NOT NULL | |
| password | VARCHAR(255) NOT NULL | bcrypt `$2y$`, copied verbatim — old hashes still verify |
| role | ENUM(superadmin,admin) NOT NULL | |
| created_at, updated_at | DATETIME | |

### `settings`
| Column | Type | Notes |
|---|---|---|
| key | VARCHAR(255) PK | e.g. `about_us_data` |
| value | TEXT NULL | JSON-encoded payload |
| created_at, updated_at | DATETIME | |

### `contacts`
| Column | Type | Notes |
|---|---|---|
| id | BIGINT PK AUTO_INCREMENT | |
| type | VARCHAR(255) NOT NULL | |
| label | VARCHAR(255) NOT NULL | |
| value | VARCHAR(255) NOT NULL | |
| icon | VARCHAR(255) NULL | |
| sort_order | INT NOT NULL DEFAULT 0 | |
| is_active | TINYINT(1) NOT NULL DEFAULT 1 | |
| created_at, updated_at | DATETIME | |

## Đã loại bỏ (removed from Laravel schema)

**7 bảng hạ tầng bị drop hoàn toàn** (không tồn tại trong schema mới):
`cache`, `cache_locks`, `jobs`, `job_batches`, `failed_jobs`, `sessions`,
`password_reset_tokens`. Lý do: session chuyển sang Redis (`SESSION__*` config),
password-reset token chuyển sang Redis key có TTL 60 phút, queue chuyển sang
Taskiq + Redis — không còn cần bảng SQL cho các cơ chế này.

**4 cột bị bỏ:**
- `figures.content`, `story_snippets.content` (longtext) — bản sao text thuần
  của `content_blocks`, chỉ dùng để search. Thay bằng `search_text`, được
  dựng lại từ `content_blocks` qua `build_search_text()` nên bao phủ nhiều
  hơn (gồm cả heading/quote, bản `content` cũ chỉ có paragraph).
- `users.email_verified_at` — không có luồng xác minh email.
- `users.remember_token` — "remember me" chuyển sang TTL của Redis session,
  không cần cột riêng.

## Migration scripts

- `scripts/backup_source.sh` — dump nguồn (gzip) + tar media, chạy trước mọi
  lần migrate.
- `scripts/migrate_data.py` — Typer CLI, đọc nguồn bằng user chỉ có quyền
  `SELECT`, ghi đích idempotent (`ON DUPLICATE KEY UPDATE`), giữ nguyên `id`.
  Cờ `--dry-run` (rollback transaction đích cuối cùng) và `--with-media`
  (copy `storage/app/public/uploads` → `media/uploads`).
- `scripts/verify_migration.py` — đối chiếu `COUNT(*)` từng bảng, kiểm tra
  `U+FFFD`, orphan FK, `search_text` rỗng bất thường, FULLTEXT MATCH mẫu, và
  liệt kê media thiếu vào `backups/missing-media.txt`.
- `scripts/rollback_migration.sh` — `DROP DATABASE` + `CREATE DATABASE` trên
  DB **đích** (DB nguồn không bao giờ bị đụng tới).
