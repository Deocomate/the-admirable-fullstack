# The Admirable - Học tiếng Anh qua những tầm cao nhân loại

The Admirable là nền tảng giáo dục trực tuyến hỗ trợ nâng cao kỹ năng Reading & Listening (đặc biệt phù hợp luyện thi IELTS) thông qua các bài viết song ngữ truyền cảm hứng về những nhân vật vĩ đại trong lịch sử.

---

## 🚀 Tính năng nổi bật

### Client (Giao diện người dùng)
- **Đọc hiểu song ngữ:** Nội dung bài viết hiển thị theo dạng các khối đoạn văn Anh - Việt đan xen trực quan.
- **Hệ sinh thái đa phương tiện:** Tích hợp Audio player (tùy chỉnh tốc độ, khuếch đại âm lượng qua Web Audio API) và nhúng Video YouTube.
- **Mảnh ghép câu chuyện (Story Snippets):** Những mẩu chuyện ngắn, bài học sâu sắc xoay quanh nhân vật.
- **Tìm kiếm thông minh:** Tìm kiếm đa tiêu chí (theo tên nhân vật, lĩnh vực, từ khóa nội dung với MySQL FULLTEXT ngram) cùng gợi ý từ khóa nổi bật (Trending).
- **Giao diện chuẩn Apple:** Phong cách tối giản, thanh lịch, tương thích trên mọi thiết bị bằng Tailwind CSS (CDN) + Vanilla JS.
- **SEO toàn diện:** Tự động sinh thẻ Meta, Canonical, Open Graph, Twitter Cards và cấu trúc Schema.org JSON-LD cho mọi trang.

### Admin Panel
- **Kiến trúc Clean Architecture:** Phân tách ranh giới 4 lớp rõ ràng (`domain` → `application` → `infrastructure` → `presentation`).
- **Tạo Audio tự động bằng AI:** Tích hợp engine `edge-tts` (không cần API key) xử lý bất đồng bộ qua Taskiq worker & Redis broker, theo dõi tiến trình và hỗ trợ hủy tác vụ an toàn.
- **Hỗ trợ tạo nội dung AI:** Trình soạn thảo cung cấp tính năng sao chép Prompt mẫu cho AI (ChatGPT/Claude) và import nhanh dữ liệu JSON vào form.
- **Quản lý nội dung đa dạng:** CRUD Nhân vật, Lĩnh vực, Mẩu chuyện ngắn, Kênh liên hệ.
- **Sắp xếp tiêu biểu trực quan:** Quản lý và kéo thả thứ tự hiển thị nhân vật trên Trang chủ (SortableJS).
- **Trang Giới thiệu động (Settings):** Tùy biến toàn bộ nội dung trang "Về chúng tôi" qua giao diện quản trị dạng block.
- **Phân quyền người dùng:** Superadmin (toàn quyền + quản lý tài khoản) và Admin (quản lý nội dung).

---

## 🛠 Tech Stack

- **Backend:** Python 3.14, FastAPI, Jinja2 Templates (SSR)
- **Kiến trúc:** Clean Architecture (Domain Driven, Ports & Adapters)
- **ORM & Database:** SQLAlchemy 2.0 (Async), Alembic, MySQL 8.4 (utf8mb4)
- **Cache & Queue:** Redis 7, Taskiq (Async Task Broker)
- **Text-to-Speech:** Microsoft edge-tts (Python asynchronous TTS)
- **Frontend:** Tailwind CSS (qua CDN - *không sử dụng Node.js/npm*), Vanilla JavaScript
- **Tooling & Package Manager:** `uv` (Astral), Ruff (Linter & Formatter), Mypy, Pytest
- **Containerization & Deployment:** Docker, Docker Compose, Nginx Reverse Proxy, Let's Encrypt Certbot

---

## 💻 Hướng dẫn cài đặt (Local Development)

### 1. Yêu cầu môi trường
- Python 3.14+
- [`uv`](https://docs.astral.sh/uv/) (Trình quản lý package Python siêu tốc)
- Docker & Docker Compose (cho MySQL và Redis)

### 2. Cài đặt dependencies
```bash
# Clone repository
git clone <repo-url>
cd admirable.site

# Cài đặt môi trường ảo và thư viện với uv
uv sync
```

### 3. Cấu hình môi trường
```bash
cp .env.example .env
```
*Tạo secret key ngẫu nhiên và cập nhật vào `APP__SECRET_KEY` trong `.env`:*
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### 4. Khởi động MySQL & Redis (Docker)
```bash
docker compose up -d mysql redis
```

### 5. Chạy Database Migrations & Seed dữ liệu
```bash
# Nạp schema database mới nhất qua Alembic
uv run alembic upgrade head

# Nạp dữ liệu mẫu ban đầu và tài khoản Superadmin
uv run python -m admirable.presentation.cli.seed
```
*(Tài khoản Superadmin mặc định: `admin@gmail.com` / `Admin@123`).*

### 6. Khởi chạy ứng dụng

- **Khởi chạy Web Server (Development mode với auto-reload):**
  ```bash
  uv run uvicorn admirable.presentation.web.main:app --reload --port 8000
  ```

- **Khởi chạy Background Worker (để xử lý sinh audio TTS):**
  ```bash
  uv run taskiq worker admirable.infrastructure.queue.tasks:broker
  ```

*Truy cập Client tại:* `http://localhost:8000`  
*Truy cập Admin tại:* `http://localhost:8000/admin/login`

---

## 🧪 Kiểm thử & Tiêu chuẩn Mã nguồn (Testing & Quality)

```bash
# Chạy toàn bộ test suite (300+ tests)
uv run pytest

# Chạy test ranh giới kiến trúc (Clean Architecture boundaries)
uv run pytest tests/architecture/

# Kiểm tra định dạng và linting code với Ruff
uv run ruff check .
uv run ruff format --check .

# Kiểm tra tĩnh kiểu dữ liệu với Mypy
uv run mypy src
```

---

## 🚢 Hướng dẫn Triển khai Production (Deployment)

Chi tiết quy trình triển khai VPS, cutover dữ liệu, sao lưu và xử lý sự cố được ghi lại đầy đủ trong:
- **[Sổ tay Triển khai Production (deploy/README.md)](deploy/README.md)**

---

## 📚 Tài liệu chi tiết (Documentation)

- [URD (Yêu cầu người dùng & Personas)](docs/urd.md)
- [Kiến trúc & Quy chuẩn dự án](docs/rules.md)
- [Sitemap & Danh sách Routes](docs/page-sitemap.md)
- [Quản lý tài khoản & Phân quyền](docs/superadmin_account.md)
- [Quy trình Triển khai Production](deploy/README.md)
