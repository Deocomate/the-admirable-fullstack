# Quy chuẩn & Kiến trúc dự án (Architecture & Rules)

## 1. Kiến trúc Backend (Clean Architecture)

Dự án tuân thủ nghiêm ngặt mô hình **Clean Architecture** gồm 4 phân lớp đồng tâm với quy tắc phụ thuộc một chiều đi vào trong:

- **Domain Layer (`src/admirable/domain/`):**
  - Trung tâm nghiệp vụ thuần túy Python, **tuyệt đối không phụ thuộc vào bất kỳ framework bên ngoài nào** (không import FastAPI, SQLAlchemy, Starlette, Taskiq...).
  - Chứa các thực thể chính (`Figure`, `Category`, `StorySnippet`, `Contact`, `User`, `Setting`, `FeaturedFigure`), Value Objects (`ContentBlock`, `KeyFact`, `Slug`, `AudioStatus`, `Role`, `AboutUsContent`), Exception nghiệp vụ và giao diện Repository Protocols.
- **Application Layer (`src/admirable/application/`):**
  - Đóng gói các Use Cases ứng dụng, thực thi các luồng nghiệp vụ cụ thể.
  - Định nghĩa các Port Interfaces (`FileStoragePort`, `TextToSpeechPort`, `TaskQueuePort`, `MailerPort`, `SessionStorePort`, `PasswordHasherPort`) và Data Transfer Objects (DTOs).
  - **Chỉ phụ thuộc vào Domain Layer và thư viện chuẩn / Pydantic**.
- **Infrastructure Layer (`src/admirable/infrastructure/`):**
  - Hiện thực hóa các Repository Protocols và Port Interfaces:
    - `db/`: SQLAlchemy 2.0 Async models, session factory, mappers và concrete repositories.
    - `tts/`: `EdgeTtsAdapter` sử dụng Microsoft `edge-tts`.
    - `storage/`: `LocalFileStorage` quản lý upload và xóa file media an toàn.
    - `queue/`: Taskiq task broker và asynchronous tasks.
    - `security/`: `BcryptPasswordHasher`, `RedisTokenStore`, `CsrfTokenManager`.
    - `mail/`: `LogMailer` và `SmtpMailer`.
- **Presentation Layer (`src/admirable/presentation/`):**
  - `web/`: FastAPI application factory, middleware stack (Session, CSRF, MethodOverride, ErrorHandler), Jinja2 templating engine, SEO builders và routers (Client & Admin).
  - `cli/`: Các lệnh điều khiển dòng lệnh (`seed`, `create_superadmin`).

---

## 2. Cấu trúc Dữ liệu Nội dung (Content Blocks Schema)

Bảng `figures` và `story_snippets` lưu trữ nội dung theo định dạng mảng JSON trong cột `content_blocks` (kèm cột `search_text` dạng text thuần hỗ trợ MySQL FULLTEXT search với ngram parser).

Cấu trúc các khối block được định nghĩa như sau:

```json
[
  {
    "type": "heading",
    "text_en": "Early Life & Education"
  },
  {
    "type": "paragraph",
    "heading_en": "The Beginning",
    "text_en": "English paragraph content...",
    "text_vi": "Nội dung đoạn văn tiếng Việt..."
  },
  {
    "type": "quote",
    "text_en": "Stay hungry, stay foolish.",
    "author": "Steve Jobs"
  }
]
```

---

## 3. Hệ thống Xử lý Audio Tự động (edge-tts & Taskiq Queue Architecture)

Hệ thống hỗ trợ tự động chuyển đổi văn bản song ngữ sang giọng đọc tiếng Anh chuẩn:

- **Engine TTS:** `EdgeTtsAdapter` sử dụng thư viện `edge-tts` (Python async, miễn phí, không yêu cầu API key) để trích xuất text từ các khối `heading`, `paragraph`, `quote` tiếng Anh và sinh file MP3 chất lượng cao.
- **Xử lý Bất đồng bộ (Taskiq):** Tác vụ sinh audio được đưa vào hàng đợi Taskiq với Redis broker (`admirable.infrastructure.queue.tasks:generate_audio_task`) để tránh nghẽn luồng HTTP.
- **Vòng đời trạng thái (State Machine):**
  - `idle`: Chưa tạo hoặc đã sẵn sàng cho lần tạo tiếp theo.
  - `processing`: Đang trong hàng đợi hoặc đang gọi engine tổng hợp audio.
  - `completed`: Hoàn tất, cập nhật đường dẫn `audio_path` và dọn dẹp file cũ.
  - `failed`: Gặp lỗi, lưu thông báo chi tiết vào cột `audio_error`.
  - `cancelled`: Người dùng chủ động hủy tác vụ đang chạy.
- **Cơ chế hủy an toàn:** Khi người dùng gửi yêu cầu hủy qua `/admin/audio/cancel/{type}/{id}`, worker kiểm tra cờ trạng thái trước và sau khi sinh file để tự động huỷ bỏ việc lưu trữ file thừa.

---

## 4. Quy chuẩn Frontend & Giao diện

- **Server-Side Rendering (SSR):** Giao diện chạy với Jinja2 templates, không cần bước build Node.js.
- **Tailwind CSS:** Được nạp trực tiếp qua CDN `<script src="https://cdn.tailwindcss.com"></script>`. Tùy biến theme và bảng màu được khai báo inline trong layout templates.
- **Apple Design System:** Hệ thống màu sắc và phong cách tối giản dựa trên các biến theme: `apple-black`, `apple-gray`, `apple-blue`, `apple-bg`.
- **Jinja2 Templates:** Toàn bộ giao diện được đặt tại `src/admirable/presentation/web/templates/` với cây thư mục tách biệt giữa `client/`, `admin/`, `layouts/`, `macros/`, `partials/` và `errors/`.
- **JavaScript:** Sử dụng **Vanilla JS** thuần được tổ chức gọn gàng bên trong các template Jinja2 (xử lý Audio player, Web Audio API boost, kéo thả SortableJS, audio generation polling).

---

## 5. Tiêu chuẩn Kiểm thử & Định dạng Code

- **Định dạng & Linting Code:** Bắt buộc chạy `uv run ruff check .` và `uv run ruff format .` trước khi hoàn tất thay đổi mã nguồn.
- **Kiểm tra Kiểu dữ liệu Tĩnh:** Chạy `uv run mypy src` để đảm bảo an toàn kiểu dữ liệu.
- **Kiểm thử Tự động (Pytest):**
  - Chạy toàn bộ test suite: `uv run pytest`
  - Chạy test ranh giới kiến trúc: `uv run pytest tests/architecture/` (đảm bảo không có import vi phạm Clean Architecture).
  - Độ phủ tối thiểu: Domain ≥ 90%, Application ≥ 85%, Presentation ≥ 70%, Tổng thể ≥ 75%.