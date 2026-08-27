# Sổ tay Triển khai & Vận hành Production (Deployment Runbook)

Tài liệu hướng dẫn toàn diện về quy trình triển khai, chuyển đổi hạ tầng (cutover), sao lưu phục hồi (backup/restore), và xử lý sự cố cho hệ thống **The Admirable** trên môi trường Production (VPS + Docker).

---

## 1. Yêu cầu Hệ thống & Kiến trúc Hạ tầng

### Yêu cầu Phần cứng VPS
- **Hệ điều hành:** Ubuntu 22.04 LTS hoặc 24.04 LTS (x86_64 / ARM64).
- **CPU:** Tối thiểu 1 vCPU (khuyến nghị 2 vCPU).
- **RAM:** Tối thiểu 1 GB (khuyến nghị 2 GB trở lên; nếu RAM < 2GB **bắt buộc bật 2GB Swap**).
- **Ổ cứng:** Tối thiểu 20 GB SSD khả dụng.
- **Mạng:** IP tĩnh công khai (IPv4), mở các port: `22` (SSH), `80` (HTTP), `443` (HTTPS).

### Sơ đồ Kiến trúc Container Production

```
                                  [ Internet / User ]
                                           │
                                  Port 80 / 443 (HTTPS)
                                           ▼
                            ┌──────────────────────────────┐
                            │     nginx (Reverse Proxy)    │
                            │  - SSL Termination          │
                            │  - /media/ static cache      │
                            │  - Security Headers / Gzip   │
                            └──────────────┬───────────────┘
                                           │ http://web:8000
                                           ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  Docker Network: default                                                     │
│                                                                              │
│  ┌────────────────────────┐                   ┌───────────────────────────┐  │
│  │   web (FastAPI / ASGI) │                   │  worker (Taskiq Worker)   │  │
│  │   - Uvicorn            │                   │  - Async TTS Audio Gen    │  │
│  │   - Clean Architecture │                   │  - edge-tts engine        │  │
│  └───────────┬────────────┘                   └─────────────┬─────────────┘  │
│              │                                              │                │
│              ├──────────────────────┬───────────────────────┤                │
│              ▼                      ▼                       ▼                │
│  ┌───────────────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │   mysql (MySQL 8.4)   │  │ redis (v7)   │  │ backup (Automated Cron)   │  │
│  │   - utf8mb4           │  │ - Session    │  │ - Daily mysqldump (14d)   │  │
│  │   - Volume persistent │  │ - Task Broker│  │ - Weekly media tar (4w)   │  │
│  └───────────────────────┘  └──────────────┘  └───────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Chuẩn bị VPS & Cài đặt Môi trường ban đầu

### Bước 2.1: Cấu hình Firewall & Swap (nếu RAM < 2GB)
Đăng nhập vào VPS với quyền root:

```bash
# 1. Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git ufw fail2ban jq

# 2. Tạo Swap 2GB (bắt buộc nếu RAM <= 2GB)
if [ $(free -m | awk '/^Mem:/{print $2}') -lt 2000 ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    sudo sysctl vm.swappiness=10
    echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
fi

# 3. Cấu hình UFW Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

### Bước 2.2: Cài đặt Docker & Docker Compose Plugin
```bash
# Cài đặt Docker official
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Thêm user quản trị vào docker group (không dùng root chạy docker)
sudo usermod -aG docker $USER
newgrp docker
```

---

## 3. Cấu hình Ứng dụng & File `.env` Production

Clone repo về thư mục deploy trên VPS (ví dụ `/var/www/admirable.site`):

```bash
sudo mkdir -p /var/www/admirable.site
sudo chown -R $USER:$USER /var/www/admirable.site
git clone <repo-url> /var/www/admirable.site
cd /var/www/admirable.site
```

Tạo file `.env` production với các giá trị bảo mật cao (**tuyệt đối không commit file này**):

```bash
# Sinh secret key 64-bit ngẫu nhiên cho session và CSRF
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(48))")
DB_PASS=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")
DB_ROOT_PASS=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

cat <<EOF > .env
APP__NAME="The Admirable"
APP__ENV="production"
APP__DEBUG=false
APP__SECRET_KEY="${SECRET_KEY}"
APP__URL="https://admirable.site"

DB__HOST="mysql"
DB__PORT=3306
DB__DATABASE="admirable"
DB__USER="admirable"
DB__PASSWORD="${DB_PASS}"
DB_ROOT_PASSWORD="${DB_ROOT_PASS}"

REDIS__URL="redis://redis:6379/0"

SESSION__COOKIE_NAME="admirable_session"
SESSION__LIFETIME_SECONDS=7200
SESSION__SECURE=true

TTS__VOICE_EN="en-US-JennyNeural"
TTS__OUTPUT_FORMAT="audio-24khz-48kbitrate-mono-mp3"

MAIL__DRIVER="log"
EOF
```

---

## 4. Thiết lập SSL / TLS (Let's Encrypt Certbot)

### Cách 1: Tự động qua Let's Encrypt & Certbot (Khuyến nghị)
1. Đảm bảo DNS domain `admirable.site` và `www.admirable.site` đã trỏ về IP của VPS.
2. Khởi tạo chứng chỉ lần đầu:
```bash
# Tạo thư mục chứng chỉ
mkdir -p deploy/certbot/conf deploy/certbot/www

# Khởi động Nginx tạm thời để xác thực ACME Challenge
docker compose -f deploy/docker-compose.prod.yml up -d nginx

# Chạy Certbot xin cấp chứng chỉ
docker compose -f deploy/docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    -d admirable.site -d www.admirable.site \
    --email admin@admirable.site \
    --agree-tos \
    --no-eff-email

# Reload Nginx để nạp chứng chỉ mới
docker compose -f deploy/docker-compose.prod.yml exec nginx nginx -s reload
```

### Cách 2: Sử dụng Cloudflare Proxy (Flexible / Full SSL)
Nếu sử dụng Cloudflare SSL Proxy:
- Có thể đặt SSL Mode trên Cloudflare thành **Full (Strict)** sau khi đã có chứng chỉ Origin Certificate từ Cloudflare.
- Đặt file `origin.pem` và `origin.key` vào `deploy/certbot/conf/live/admirable.site/` và cấu hình `prod.conf`.

---

## 5. Quy trình Chuyển đổi Production (Cutover Sequence)

Mục tiêu: Đưa hệ thống mới vào phục vụ với thời gian gián đoạn (downtime) dưới 15-30 phút và bảo toàn 100% dữ liệu.

```
0. Hạ DNS TTL xuống 300s (trước 24h)
1. Bật trang bảo trì trên hệ thống cũ ────► [Bắt đầu Downtime]
2. Dump MySQL DB & nén thư mục media từ host cũ
3. Chuyển dump + media sang VPS (rsync / scp)
4. Nạp dump vào DB staging trên VPS
5. Chạy migrate_data.py --with-media
6. Chạy verify_migration.py ────────────► [Pass 100%? Không -> Rollback]
7. Khởi động toàn bộ stack trên VPS
8. Smoke test qua IP/Host nội bộ
9. Chuyển DNS trỏ về IP VPS mới ────────► [Kết thúc Downtime]
10. Theo dõi 24h đầu & test audio edge-tts
```

### Chi tiết các bước thực hiện:

#### Bước 1: Chuẩn bị trước 24 giờ
- Đăng nhập nhà cung cấp DNS, hạ **TTL** của domain `admirable.site` xuống `300` (5 phút).

#### Bước 2: Bật bảo trì & Xuất dữ liệu từ hosting cũ
Trên server cũ (cPanel / SSH):
```bash
# Đặt file bảo trì tĩnh hoặc chặn ghi
# Dump dữ liệu MySQL cũ
mysqldump -u <db_user> -p --single-transaction --routines <db_name> > /tmp/laravel_dump.sql

# Nén toàn bộ media/uploads
tar -czf /tmp/laravel_media.tar.gz -C /path/to/laravel/storage/app/public .
```

#### Bước 3: Chuyển dữ liệu sang VPS
Trên VPS mới:
```bash
scp user@old-server:/tmp/laravel_dump.sql /var/www/admirable.site/laravel_dump.sql
scp user@old-server:/tmp/laravel_media.tar.gz /var/www/admirable.site/laravel_media.tar.gz
```

#### Bước 4: Chạy Migration dữ liệu & Xác minh
```bash
# 1. Khởi động MySQL & Redis
docker compose -f deploy/docker-compose.prod.yml up -d mysql redis

# 2. Tạo database staging và nạp dữ liệu cũ vào
docker compose -f deploy/docker-compose.prod.yml exec -T mysql mysql -u root -p"$DB_ROOT_PASS" -e "CREATE DATABASE IF NOT EXISTS admirable_legacy;"
docker compose -f deploy/docker-compose.prod.yml exec -T mysql mysql -u root -p"$DB_ROOT_PASS" admirable_legacy < laravel_dump.sql

# 3. Chạy Alembic migration trên database mới
docker compose -f deploy/docker-compose.prod.yml run --rm web alembic upgrade head

# 4. Giải nén media vào thư mục tạm
mkdir -p /tmp/legacy_media
tar -xzf laravel_media.tar.gz -C /tmp/legacy_media

# 5. Chạy migration dữ liệu
docker compose -f deploy/docker-compose.prod.yml run --rm \
    -v /tmp/legacy_media:/legacy_media:ro \
    web python scripts/migrate_data.py \
        --source-url="mysql+asyncmy://root:${DB_ROOT_PASS}@mysql/admirable_legacy" \
        --with-media \
        --legacy-media-dir=/legacy_media

# 6. Chạy verify_migration để đối chiếu 100% số lượng và tính toàn vẹn
docker compose -f deploy/docker-compose.prod.yml run --rm \
    web python scripts/verify_migration.py \
        --legacy-url="mysql+asyncmy://root:${DB_ROOT_PASS}@mysql/admirable_legacy"
```
> [!IMPORTANT]
> Nếu `verify_migration.py` phát hiện sai lệch: **DỪNG LẠI NGAY LẬP TỨC**, gỡ bỏ bảo trì trên server cũ và điều tra log.

#### Bước 5: Khởi động hệ thống & Smoke Test
```bash
# Khởi động toàn bộ dịch vụ
docker compose -f deploy/docker-compose.prod.yml up -d

# Kiểm tra healthcheck
curl -f http://127.0.0.1:8000/healthz

# Smoke test các route chính
curl -H "Host: admirable.site" http://127.0.0.1/
curl -H "Host: admirable.site" http://127.0.0.1/linh-vuc
curl -H "Host: admirable.site" http://127.0.0.1/admin/login
```

#### Bước 6: Chuyển đổi DNS
- Trỏ bản ghi `A` của `admirable.site` và `www.admirable.site` sang IP của VPS mới.
- Sau khi DNS lan truyền, kiểm tra truy cập trên trình duyệt qua HTTPS.

---

## 6. Theo dõi 24 giờ sau Cutover

1. **Kiểm tra Logs:**
   ```bash
   # Theo dõi log web server
   docker compose -f deploy/docker-compose.prod.yml logs -f web

   # Theo dõi log worker xử lý audio
   docker compose -f deploy/docker-compose.prod.yml logs -f worker

   # Theo dõi log Nginx (tỉ lệ 4xx / 5xx)
   docker compose -f deploy/docker-compose.prod.yml logs -f nginx
   ```
2. **Kiểm tra Sinh Audio bằng edge-tts:**
   - Đăng nhập vào trang quản trị (`/admin/figures` hoặc `/admin/stories`).
   - Bấm **Tạo Audio** cho một nhân vật hoặc mẩu chuyện.
   - Xác nhận tiến trình chuyển từ `idle → processing → completed` và phát audio nghe rõ ràng.
   *(Nếu IP datacenter của VPS bị chặn edge-tts, xem mục Xử lý sự cố bên dưới).*

---

## 7. Kế hoạch Lùi (Rollback Procedure)

Trong 24-48 giờ đầu tiên, nếu phát sinh sự cố nghiêm trọng không thể khắc phục:
1. Đổi lại bản ghi DNS `A` trỏ về IP của hosting cũ.
2. Gỡ bỏ trang thông báo bảo trì trên hosting cũ.
3. Chờ DNS lan truyền (5 phút do TTL đã hạ xuống 300s).
4. Dừng container trên VPS: `docker compose -f deploy/docker-compose.prod.yml down`.
5. Đánh giá nguyên nhân lỗi và lên kế hoạch cutover lại.

---

## 8. Sao lưu & Khôi phục (Backup & Disaster Recovery)

### Sao lưu Tự động
Service `backup` trong `docker-compose.prod.yml` chạy ngầm định kỳ:
- **MySQL Backup:** Chạy mỗi ngày lúc 00:00, lưu 14 bản gần nhất tại volume `backups_data`.
- **Media Backup:** Chạy hằng tuần (Chủ nhật), lưu 4 bản gần nhất.

### Sao lưu Thủ công (On-Demand)
```bash
# Thực hiện backup ngay lập tức (kèm media)
docker compose -f deploy/docker-compose.prod.yml exec backup /usr/local/bin/backup.sh --with-media
```

### Khôi phục từ Bản sao lưu (Restore Rehearsal)
```bash
# 1. Khôi phục database từ file backup
docker compose -f deploy/docker-compose.prod.yml exec backup /usr/local/bin/restore.sh \
    --db /backups/db_admirable_20260827_000000.sql.gz

# 2. Khôi phục media từ file backup
docker compose -f deploy/docker-compose.prod.yml exec backup /usr/local/bin/restore.sh \
    --media /backups/media_20260827_000000.tar.gz
```

---

## 9. Xử lý Sự cố Thường gặp (Troubleshooting & FAQs)

| Vấn đề | Nguyên nhân | Hướng xử lý |
|---|---|---|
| **Audio TTS báo `failed`** | IP của VPS bị Microsoft chặn tạm thời | 1. Thử cấu hình egress proxy qua IP dân dụng.<br>2. Hoặc cấu hình adapter Piper TTS offline. |
| **Lỗi 502 Bad Gateway trên Nginx** | Service `web` chưa khởi động xong hoặc bị crash | Chạy `docker compose -f deploy/docker-compose.prod.yml logs web` để xem traceback lỗi. |
| **Không tải được ảnh `/media/...`** | Volume `media_data` chưa được mount đúng quyền | Chạy `docker compose -f deploy/docker-compose.prod.yml exec web chown -R app:app /app/media`. |
| **Hết bộ nhớ / OOM Killer** | RAM không đủ và chưa bật Swap | Tạo swap 2GB theo hướng dẫn ở Bước 2.1. |
