---
phase: 12
title: "Deploy & Xoá Laravel"
status: pending
priority: P1
effort: "1.5d"
dependencies: [11]
---

# Phase 12: Deploy & Xoá Laravel

## Overview

Đưa hệ thống mới lên VPS, cutover production, rồi xoá sạch PHP/Laravel khỏi repo và cập nhật tài liệu. Thứ tự bắt buộc: **deploy và chạy ổn định trước, xoá sau**. Không bao giờ xoá Laravel trước khi bản Python đã phục vụ được lưu lượng thật.

## Requirements

**Functional**
- `docker compose up -d` trên VPS sạch dựng đủ hệ thống.
- HTTPS hoạt động, HTTP redirect sang HTTPS (giữ hành vi `.htaccess` cũ).
- Dữ liệu production được migrate trong cửa sổ downtime, verify pass.
- Backup tự động DB và media theo lịch.
- Repo không còn file PHP nào.
- Toàn bộ tài liệu phản ánh stack mới.

**Non-functional**
- Downtime cutover dưới 30 phút.
- Có đường lùi rõ ràng trong 24h đầu (DNS trỏ lại hosting cũ).
- Secret không nằm trong repo; `.env` production tạo trên VPS.

## Architecture

<!-- Updated: Validation Session 1 - merge branch migrate/fastapi -->
**Chuỗi cutover:**

```
0. Merge migrate/fastapi → main (Phase 11 đã pass)  → main giờ chứa CẢ Python lẫn Laravel
1. Dựng stack mới trên VPS, trỏ DB rỗng           → smoke test
2. Bật maintenance page trên site cũ              → bắt đầu downtime
3. Dump DB production + tar media từ hosting cũ
4. Chuyển sang VPS, chạy migrate_data.py + verify
5. Smoke test trên VPS bằng IP/host tạm
6. Đổi DNS sang VPS                               → kết thúc downtime
7. Theo dõi 24h                                   → điểm quyết định lùi
8. Sau 7 ngày ổn định: xoá Laravel khỏi main (commit riêng)
```

**Về việc merge (bước 0).** Merge trước khi deploy, không sau. Lý do: nếu deploy fail và phải rollback, `main` vẫn giữ nguyên code Laravel chạy được — bước xoá PHP mới là điểm không quay lại, và nó nằm tận bước 8. Dùng merge commit (`--no-ff`) để giữ ranh giới của toàn bộ đợt chuyển đổi trong lịch sử git. Sau khi merge, xoá branch từ xa nhưng **giữ tag**: `git tag migration/pre-removal` tại commit ngay trước bước 8, để quay lại trạng thái "cả hai stack cùng tồn tại" nếu cần.

**Backup định kỳ** bằng service `backup` trong compose (cron trong container hoặc systemd timer trên host): `mysqldump` hằng ngày giữ 14 bản, `tar` media hằng tuần giữ 4 bản, ghi ra volume riêng ngoài thư mục ứng dụng.

**Danh sách xoá ở bước 8:**

```
app/  bootstrap/  config/  database/  resources/  routes/  storage/  tests/(PHP)
public/index.php  artisan  composer.json  composer.lock  phpunit.xml  .htaccess
thư mục thư viện PHP (composer)
```

Giữ lại: `.git/`, `docs/`, `plans/`, `README.md`, `AGENTS.md`, `.editorconfig`, `.gitattributes`, `public/assets` (đã copy sang `static/` ở Phase 8 — xoá bản gốc), `public/robots.txt`, `public/favicon.ico`.

## Related Code Files

- Create: `deploy/{docker-compose.prod.yml,nginx/prod.conf,backup/backup.sh}`
- Create: `deploy/README.md` (runbook: dựng VPS, cutover, rollback, backup/restore)
- Create: `.github/workflows/deploy.yml` (tuỳ chọn — chỉ khi user muốn CD)
- Modify: `README.md` — viết lại toàn bộ mục Tech Stack và Hướng dẫn cài đặt
- Modify: `AGENTS.md` — thay deny-list PHP bằng quy ước Python; cập nhật lệnh test/format/run
- Modify: `docs/rules.md` — thay §1 Service Pattern bằng Clean Architecture; §3 Azure TTS bằng edge-tts; §4 giữ nguyên phần Tailwind/JS, cập nhật đường dẫn template; §5 thay Pint/Pest bằng Ruff/pytest
- Modify: `docs/page-sitemap.md` — cập nhật tên handler, giữ nguyên bảng URI
- Modify: `docs/superadmin_account.md` — thay lệnh `php artisan db:seed` bằng CLI Python
- Modify: `.gitignore`
- Delete: toàn bộ danh sách ở phần Architecture

## Implementation Steps

0. Merge `migrate/fastapi` vào `main`: `git checkout main && git merge --no-ff migrate/fastapi`. Chạy CI trên `main` xác nhận xanh. Đặt tag `migration/pre-removal` để đánh dấu trạng thái hai stack cùng tồn tại.
1. **Chuẩn bị VPS**: cài Docker + Compose plugin, tạo user không phải root, mở port 80/443, cấu hình firewall, bật swap nếu RAM < 2GB.
2. Viết `deploy/docker-compose.prod.yml`: kế thừa compose gốc, bỏ bind-mount source, bỏ `--reload`, thêm `restart: unless-stopped`, giới hạn tài nguyên, log driver `json-file` có `max-size`.
3. Viết `deploy/nginx/prod.conf`: server block HTTPS, HTTP→HTTPS redirect, `client_max_body_size 32M`, gzip, cache header cho `/static` và `/media`, header bảo mật (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`). Giữ nguyên quy tắc bỏ trailing slash của `.htaccess` cũ.
4. TLS: dùng `certbot` trong container hoặc Cloudflare proxy — **chốt theo câu trả lời của câu hỏi mở #2 trong `plan.md`**. Nếu Let's Encrypt: thêm service `certbot` với volume chia sẻ và cron gia hạn.
5. Tạo `.env` production **trên VPS** (không commit): `APP__SECRET_KEY` sinh bằng `python -c "import secrets;print(secrets.token_urlsafe(48))"`, `APP__ENV=production`, `APP__DEBUG=false`, DB credentials mới, `REDIS__URL`, `TTS__*`, `MAIL__*`.
6. Dựng stack với DB rỗng, chạy `alembic upgrade head`, chạy `create_superadmin`, smoke test đủ 8 trang client + đăng nhập admin.
7. Viết `deploy/backup/backup.sh` + service/cron. Test restore từ backup vào DB tạm **trước khi** cutover — backup chưa từng restore được thì không phải backup.
8. Viết `deploy/README.md`: runbook từng bước cho cutover và rollback, gồm lệnh cụ thể và tiêu chí quyết định.
9. **Cutover** (theo chuỗi ở phần Architecture):
   - Đặt trang bảo trì tĩnh trên hosting cũ.
   - Dump DB production + tar media, chuyển sang VPS (`scp`/`rsync`).
   - Nạp dump vào DB nguồn tạm trên VPS, chạy `migrate_data.py --with-media`, chạy `verify_migration.py`. **Nếu verify fail → dừng, rollback (gỡ trang bảo trì), điều tra.**
   - Smoke test qua `curl -H "Host: admirable.site"` tới IP VPS.
   - Đổi DNS. TTL nên hạ xuống 300s trước đó 24h.
10. Theo dõi 24h: log nginx (tỉ lệ 4xx/5xx), log app, trạng thái worker, dung lượng đĩa. Kiểm tra sinh audio thật ít nhất một lần trên production (xác nhận edge-tts không bị chặn từ IP datacenter — **đây là rủi ro chỉ lộ ra ở bước này**).
11. **Sau 7 ngày ổn định**, xoá Laravel trên `main`: `git rm -r` theo danh sách ở phần Architecture. Commit riêng, message rõ ràng. Tag `migration/pre-removal` (bước 0) vẫn trỏ về trạng thái trước đó nếu cần tra cứu nhanh mà không phải lần lịch sử.
12. Cập nhật `README.md`: Tech Stack (Python 3.14, FastAPI, Jinja2, SQLAlchemy, Taskiq, edge-tts, MySQL, Redis, Docker), hướng dẫn cài đặt (`uv sync`, `docker compose up`, `alembic upgrade head`, seed), lệnh chạy dev và worker, link tới `docs/database-schema.md` và `deploy/README.md`.
13. Cập nhật `AGENTS.md`: thay toàn bộ mục Tooling & Commands và Strict Deny-List. Deny-list mới giữ tinh thần cũ: không NPM/Vite (Tailwind vẫn qua CDN), không business logic trong router (phải ở use case), không thao tác file trực tiếp trong router (phải qua `FileStoragePort`), không import ngược chiều giữa các lớp.
14. Cập nhật `docs/rules.md` theo danh sách ở phần Related Code Files. Bổ sung mục mới: quy tắc phụ thuộc Clean Architecture và cách chạy test ranh giới lớp.
15. Cập nhật `docs/page-sitemap.md` (cột mô tả handler) và `docs/superadmin_account.md` (lệnh seed mới, ràng buộc xoá user giờ nằm ở `domain/entities/user.py`).
16. Cập nhật `.gitignore`: bỏ mục PHP, thêm `.venv/`, `media/`, `backups/`, `*.sqlite`.
17. Chạy `git ls-files '*.php'` xác nhận rỗng. Chạy CI lần cuối.
18. Giữ DB cũ ở hosting cũ ở chế độ chỉ đọc thêm 14 ngày rồi mới huỷ hợp đồng hosting.

## Success Criteria

- [ ] `docker compose -f deploy/docker-compose.prod.yml up -d` trên VPS sạch chạy được, `/healthz` trả OK.
- [ ] HTTPS hợp lệ, HTTP redirect 301 sang HTTPS.
- [ ] `verify_migration.py` trên dữ liệu production pass 100%.
- [ ] 8 trang client và toàn bộ admin hoạt động trên domain thật.
- [ ] Sinh audio bằng edge-tts thành công **từ VPS production** ít nhất một lần.
- [ ] Backup chạy tự động và đã restore thử thành công vào DB tạm.
- [ ] `migrate/fastapi` đã merge vào `main` bằng `--no-ff`; CI xanh trên `main`; tag `migration/pre-removal` tồn tại.
- [ ] `git ls-files '*.php'` trả về rỗng; `composer.json`, `artisan` không còn.
- [ ] `README.md`, `AGENTS.md`, `docs/rules.md`, `docs/page-sitemap.md`, `docs/superadmin_account.md` không còn nhắc Laravel/PHP như stack hiện hành.
- [ ] `deploy/README.md` chứa runbook cutover + rollback đầy đủ lệnh.
- [ ] CI xanh sau khi xoá PHP.

## Risk Assessment

**Rủi ro cao: edge-tts bị Microsoft chặn từ IP datacenter của VPS.** Đây là rủi ro **chỉ lộ ra ở production**, không thể phát hiện khi dev từ IP dân dụng.
- Tín hiệu: bước 10 sinh audio thất bại trong khi cùng code chạy được ở local.
- Phản ứng đã chốt: (1) thử proxy đầu ra qua một IP dân dụng/residential, (2) nếu không được, chuyển sang Piper TTS chạy offline trong container — chỉ cần viết adapter mới sau `TextToSpeechPort`, không đụng use case, ước tính nửa ngày. **Không cutover ngược vì lý do này** — sinh audio là chức năng admin, không chặn người dùng cuối.

**Rủi ro: xoá Laravel quá sớm khiến mất khả năng đối chiếu khi phát hiện lỗi.** Mitigation: bước 11 chờ 7 ngày, và `plans/reports/laravel-routes.json` cùng ảnh chụp giao diện được giữ vĩnh viễn trong repo. Lịch sử Git vẫn giữ toàn bộ code PHP nếu cần tra cứu.

**Rủi ro: mất dữ liệu phát sinh trong cửa sổ downtime.** Mitigation: đặt trang bảo trì **trước** khi dump, đảm bảo không ai ghi vào DB cũ trong lúc chuyển. Kiểm tra `SHOW PROCESSLIST` trước khi dump.

**Rủi ro: DNS propagation kéo dài, người dùng vẫn vào hosting cũ đã bảo trì.** Mitigation: hạ TTL xuống 300s trước 24h. Trang bảo trì có thông báo rõ và tự refresh.

**Rủi ro: `.env` production bị commit nhầm.** Mitigation: `.gitignore` chặn `.env`; chạy `git ls-files | grep -c "^\.env$"` = 0 trước khi push. Không bao giờ copy `.env` production về máy dev.

**Rủi ro: hosting cũ bị huỷ trước khi chắc chắn ổn định.** Mitigation: bước 18 chờ 14 ngày. Quyết định huỷ là của user, không tự động.
