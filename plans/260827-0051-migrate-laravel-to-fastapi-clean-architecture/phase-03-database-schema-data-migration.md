---
phase: 3
title: "Schema sạch & Migrate dữ liệu"
status: completed
priority: P1
effort: "2.5d"
dependencies: [2]
---

# Phase 3: Schema sạch & Migrate dữ liệu

## Overview

Định nghĩa schema đích đã làm sạch bằng Alembic, và viết script migrate chuyển 100% dữ liệu nghiệp vụ từ DB Laravel hiện tại sang DB mới. Đây là phase rủi ro cao nhất của toàn kế hoạch — nguyên tắc bất di bất dịch: **không bao giờ ghi vào DB nguồn**.

Kết thúc phase, có một DB `admirable` mới chứa đầy đủ dữ liệu, chạy dry-run được lặp lại nhiều lần, và có báo cáo đối chiếu số lượng bản ghi.

## Requirements

**Functional**
- Alembic baseline tạo được toàn bộ schema đích từ DB rỗng.
- Script `scripts/migrate_data.py` đọc DB nguồn (read-only), ghi vào DB đích, idempotent (chạy lại cho kết quả giống nhau).
- Script sao chép media từ `storage/app/public/uploads/` sang `media/uploads/` giữ nguyên cấu trúc thư mục.
- Có báo cáo đối chiếu: số bản ghi mỗi bảng nguồn vs đích, danh sách file media thiếu.
- Có đường lùi: `scripts/rollback_migration.sh` khôi phục từ dump.

**Non-functional**
- DB nguồn được mở bằng user chỉ có quyền `SELECT` (tự tạo user read-only trước khi chạy).
- Toàn bộ dữ liệu giữ `utf8mb4_unicode_ci`, không lỗi dấu tiếng Việt.
- Migrate 100% dữ liệu hiện tại xong dưới 5 phút.

## Architecture

**Schema đích (8 bảng nghiệp vụ):**

| Bảng | Thay đổi so với Laravel |
|---|---|
| `users` | Bỏ `email_verified_at`, `remember_token`. `role` → ENUM(`superadmin`,`admin`). Giữ `password` nguyên xi (bcrypt `$2y$`) |
| `categories` | Không đổi |
| `figures` | Bỏ `content`; thêm `search_text TEXT` + `FULLTEXT KEY ft_figures_search (name, short_description, search_text) WITH PARSER ngram`. `audio_status` → ENUM 5 giá trị. `key_facts`/`content_blocks` giữ kiểu JSON |
| `category_figure` | Không đổi (khoá chính composite) |
| `story_snippets` | Bỏ `content`; thêm `search_text TEXT`. `audio_status` → ENUM 5 giá trị |
| `settings` | Không đổi (`key` PK, `value` LONGTEXT) |
| `contacts` | Không đổi |
| `featured_figures` | Không đổi |

**7 bảng bị loại bỏ hoàn toàn** (không tạo trong schema mới): `cache`, `cache_locks`, `jobs`, `job_batches`, `failed_jobs`, `sessions`, `password_reset_tokens`. Session và reset token chuyển sang Redis (Phase 7).

**Chiến lược migrate:** DB *mới* riêng biệt (`admirable`), không `ALTER TABLE` trên DB cũ. Cho phép chạy song song hai hệ thống trong giai đoạn đối chiếu ở Phase 11.

**`search_text` được dựng lại từ `content_blocks`** bằng đúng hàm `build_search_text()` ở Phase 2 — không copy cột `content` cũ. Điều này vừa loại bỏ trùng lặp, vừa cải thiện: cột `content` cũ chỉ chứa EN+VI của paragraph, cột mới bao gồm cả heading và quote, nên search sẽ tìm được nhiều hơn chứ không ít hơn.

**Về FULLTEXT ngram và tiếng Việt:** MySQL ngram parser cắt token theo n-gram cố định (mặc định `ngram_token_size=2`), hoạt động cho tiếng Việt nhưng ngữ nghĩa khác `LIKE '%q%'`. Chiến lược truy vấn ở Phase 5:
- Truy vấn dài ≥ `ngram_token_size` ký tự → `MATCH(...) AGAINST(... IN BOOLEAN MODE)`.
- Truy vấn ngắn hơn → fallback `LIKE '%q%'` như hiện tại.
Kết quả hai nhánh được đối chiếu với hệ Laravel ở Phase 11.

## Related Code Files

- Create: `alembic.ini`, `migrations/env.py`, `migrations/script.py.mako`
- Create: `migrations/versions/0001_baseline_schema.py`
- Create: `scripts/migrate_data.py`, `scripts/backup_source.sh`, `scripts/rollback_migration.sh`, `scripts/verify_migration.py`
- Create: `docs/database-schema.md` (tài liệu schema đích — sẽ được link từ README ở Phase 12)
- Nguồn tham chiếu (đọc, không sửa): toàn bộ `database/migrations/*.php`
- Không sửa: DB nguồn, `storage/app/public/**`

## Implementation Steps

1. **Backup trước tiên.** Viết và chạy `scripts/backup_source.sh`:
   `mysqldump --single-transaction --routines --triggers <src_db> | gzip > backups/src-$(date +%F-%H%M).sql.gz`
   và `tar czf backups/media-$(date +%F-%H%M).tar.gz storage/app/public/uploads`.
   Xác minh dump giải nén được và `zcat ... | head` đọc được trước khi đi tiếp.
2. Tạo MySQL user read-only cho DB nguồn: `GRANT SELECT ON <src_db>.* TO 'migrate_ro'@'%'`. Script migrate **chỉ** dùng user này cho nguồn.
3. Cài Alembic, cấu hình `migrations/env.py` trỏ tới `Base.metadata` (metadata thực sự được định nghĩa ở Phase 4 — ở phase này viết migration bằng tay dạng `op.create_table`, Phase 4 sẽ đối chiếu ORM model khớp với schema này bằng `alembic check`).
4. Viết `0001_baseline_schema.py`: tạo 8 bảng theo bảng ở trên, đúng thứ tự khoá ngoại (`categories`, `figures`, `category_figure`, `story_snippets`, `featured_figures`, `users`, `settings`, `contacts`). Đặt `mysql_charset='utf8mb4'`, `mysql_collate='utf8mb4_unicode_ci'`, `mysql_engine='InnoDB'` cho mọi bảng. FULLTEXT index tạo bằng `op.execute` với `WITH PARSER ngram`.
5. Chạy `alembic upgrade head` trên DB rỗng; xác nhận `SHOW CREATE TABLE` từng bảng khớp thiết kế.
6. Viết `scripts/migrate_data.py` (Typer CLI, có cờ `--dry-run` và `--batch-size`). Thứ tự migrate tôn trọng khoá ngoại:
   1. `users` — copy `id, name, role, email, password, created_at, updated_at`. Bỏ 2 cột. Cảnh báo nếu `role` có giá trị lạ.
   2. `categories` — copy nguyên.
   3. `figures` — copy nguyên trừ `content`; `search_text` = `build_search_text(parse_content_blocks(content_blocks))`; nếu `content_blocks` rỗng/null thì `search_text` = cột `content` cũ (fallback bảo toàn dữ liệu). `audio_status` map giá trị lạ → `idle` và ghi log.
   4. `category_figure` — copy nguyên.
   5. `story_snippets` — như `figures`.
   6. `featured_figures`, `settings`, `contacts` — copy nguyên.
   Ghi theo batch, `INSERT ... ON DUPLICATE KEY UPDATE` để idempotent. Bảo toàn `id` gốc (tắt auto-increment gap bằng cách chèn id tường minh) — bắt buộc, vì `featured_figures.figure_id` và `story_snippets.figure_id` tham chiếu id cũ, và slug/URL công khai không đổi.
7. Sau khi ghi xong, đặt lại `AUTO_INCREMENT` mỗi bảng = `MAX(id)+1`.
8. Viết phần copy media trong cùng script (`--with-media`): `shutil.copytree('storage/app/public/uploads', 'media/uploads', dirs_exist_ok=True)`. Sau đó quét mọi `avatar_path`, `audio_path`, `image_path` trong DB đích, kiểm tra file tồn tại, xuất danh sách thiếu ra `backups/missing-media.txt`.
9. Viết `scripts/verify_migration.py`: in bảng đối chiếu `COUNT(*)` từng bảng nguồn vs đích; so `MD5` của các cột text quan trọng trên mẫu ngẫu nhiên 50 bản ghi `figures`; kiểm tra không có ký tự thay thế `U+FFFD` (dấu hiệu hỏng encoding); kiểm tra mọi `figure_id` trong `story_snippets`/`featured_figures`/`category_figure` đều tồn tại.
10. Viết `scripts/rollback_migration.sh`: `DROP DATABASE admirable; CREATE DATABASE admirable ...` rồi hướng dẫn chạy lại. Vì DB nguồn không bị đụng, rollback = xoá DB đích.
11. Chạy dry-run đủ 3 lần liên tiếp; kết quả `verify_migration.py` phải giống hệt nhau ở lần 2 và 3 (chứng minh idempotent).
12. Viết `docs/database-schema.md`: bảng cột từng entity, quan hệ, và mục "Đã loại bỏ" liệt kê 7 bảng + 4 cột đã bỏ kèm lý do.

## Success Criteria

- [ ] `alembic upgrade head` trên DB rỗng tạo đủ 8 bảng, `alembic downgrade base` xoá sạch.
- [ ] `verify_migration.py` báo `COUNT(*)` khớp 100% cho cả 8 bảng.
- [ ] Chạy `migrate_data.py` lần 2 không tạo bản ghi trùng, không thay đổi số lượng.
- [ ] `id` của mọi bản ghi được bảo toàn (spot-check 10 `figures` theo slug).
- [ ] Không bản ghi nào chứa `U+FFFD`; tiếng Việt hiển thị đúng khi `SELECT`.
- [ ] `backups/missing-media.txt` rỗng, hoặc mọi mục trong đó cũng thiếu ở hệ thống cũ (nghĩa là lỗi có sẵn, không do migrate).
- [ ] Truy vấn `MATCH ... AGAINST` chạy được trên `figures` và trả kết quả cho một từ khoá tiếng Việt mẫu.
- [ ] `docs/database-schema.md` tồn tại và khớp với `SHOW CREATE TABLE` thực tế.

## Risk Assessment

**Rủi ro cao nhất: mất hoặc hỏng dữ liệu.** Mitigation nhiều lớp: (a) dump + tar trước mỗi lần chạy, (b) user read-only trên nguồn khiến việc ghi nhầm là bất khả thi về mặt kỹ thuật, (c) DB đích tách biệt nên rollback là `DROP DATABASE`, (d) verify script chạy sau mỗi lần.
- Tín hiệu hỏng: `COUNT(*)` lệch, xuất hiện `U+FFFD`, hoặc FK không khớp.
- Phản ứng đã chốt: rollback DB đích, sửa script, chạy lại. Không bao giờ "vá tay" dữ liệu trong DB đích.

**Rủi ro: `content_blocks` trong DB có bản ghi sai định dạng khiến `build_search_text` trả rỗng, làm mất khả năng tìm kiếm bản ghi đó.** Mitigation: nhánh fallback ở bước 6.3 dùng lại cột `content` cũ. Thêm kiểm tra ở `verify_migration.py`: đếm số bản ghi có `search_text` rỗng nhưng `content_blocks` không rỗng — phải bằng 0.

**Rủi ro: FULLTEXT ngram cho kết quả tệ hơn `LIKE` với tiếng Việt.** Đây là rủi ro nghiệp vụ có thật, không thể loại trừ ở phase này.
- Tín hiệu: đối chiếu ở Phase 11 cho thấy kết quả search khác biệt đáng kể (>10% truy vấn mẫu).
- Phản ứng đã chốt: giữ nguyên cột `search_text` nhưng **bỏ nhánh MATCH, dùng `LIKE '%q%'` cho mọi truy vấn** — giống hệt hành vi Laravel hiện tại. Index FULLTEXT để lại, không gây hại. Mục tiêu "bỏ cột trùng lặp" vẫn đạt.

**Rủi ro: bảo toàn `id` xung đột với auto-increment.** Mitigation: chèn `id` tường minh và reset `AUTO_INCREMENT` ở bước 7. Kiểm chứng bằng cách tạo thử một `figure` mới sau migrate và xác nhận id mới không đụng id cũ.

**Rủi ro: DB nguồn thay đổi giữa lúc dev migrate và lúc cutover thật.** Phản ứng: script phải chạy lại được từ đầu; ở Phase 12 chạy lại toàn bộ trên dữ liệu mới nhất trong cửa sổ downtime, không dùng lại kết quả dev.
