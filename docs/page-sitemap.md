# Cấu trúc Sitemap & Danh sách Routes (FastAPI Clean Architecture)

Dự án được phân chia thành 2 không gian định tuyến chính: **Client (Công khai)** và **Admin (Quản trị)**.

---

## 🌍 Khách hàng (Client Routes)

| Phương thức | URI | Tên Route | Handler Python | Mô tả chức năng |
|---|---|---|---|---|
| `GET` | `/` | `client.home` | `admirable.presentation.web.routers.client.home` | Trang chủ (Featured Figures, Latest Stories, Danh mục, Thống kê) |
| `GET` | `/linh-vuc` | `client.categories.index` | `admirable.presentation.web.routers.client.categories:list_categories` | Danh sách tất cả các lĩnh vực hoạt động |
| `GET` | `/linh-vuc/{slug}` | `client.categories.show` | `admirable.presentation.web.routers.client.categories:show_category` | Lọc danh sách nhân vật theo một lĩnh vực cụ thể |
| `GET` | `/nhan-vat/{slug}` | `client.figures.show` | `admirable.presentation.web.routers.client.figures:show_figure` | Chi tiết nhân vật (Nội dung song ngữ, Media, Fact, Story Snippets) |
| `GET` | `/cau-chuyen/{id}` | `client.stories.show` | `admirable.presentation.web.routers.client.stories:show_story` | Chi tiết mẩu chuyện ngắn |
| `GET` | `/tim-kiem` | `client.search` | `admirable.presentation.web.routers.client.search:search` | Tìm kiếm nhân vật theo từ khóa & lĩnh vực |
| `GET` | `/ve-chung-toi` | `client.about-us` | `admirable.presentation.web.routers.client.about_us:about_us` | Trang giới thiệu nền tảng ("About Us") |
| `GET` | `/lien-he` | `client.contact` | `admirable.presentation.web.routers.client.contact:contact` | Trang thông tin liên hệ và biểu mẫu hợp tác |

---

## 🔒 Quản trị (Admin Routes)

### 1. Xác thực (Authentication) - `guest` dependency
| Phương thức | URI | Tên Route | Handler Python | Mô tả chức năng |
|---|---|---|---|---|
| `GET` / `POST` | `/admin/login` | `admin.auth.login` / `admin.auth.login.submit` | `admirable.presentation.web.routers.admin.auth:login_*` | Đăng nhập tài khoản quản trị |
| `GET` / `POST` | `/admin/forgot-password` | `admin.auth.forgot-password` / `.submit` | `admirable.presentation.web.routers.admin.auth:forgot_password_*` | Yêu cầu gửi link đặt lại mật khẩu |
| `GET` / `POST` | `/admin/reset-password/{token}` | `admin.auth.reset-password` / `.submit` | `admirable.presentation.web.routers.admin.auth:reset_password_*` | Thực hiện đặt lại mật khẩu mới |

### 2. Không gian Quản trị chung - `require_role("admin")`
| Phương thức | URI | Tên Route | Handler Python | Mô tả chức năng |
|---|---|---|---|---|
| `GET` | `/admin` / `/admin/dashboard` | `admin.home` / `admin.dashboard` | `admirable.presentation.web.routers.admin.dashboard` | Bảng điều khiển, thống kê số liệu tổng quan |
| `POST` | `/admin/logout` | `admin.auth.logout` | `admirable.presentation.web.routers.admin.auth:logout` | Đăng xuất khỏi hệ thống |
| Resource | `/admin/categories` | `admin.categories.*` | `admirable.presentation.web.routers.admin.categories` | Quản lý Lĩnh vực (Index, Create, Store, Edit, Update, Destroy) |
| Resource | `/admin/figures` | `admin.figures.*` | `admirable.presentation.web.routers.admin.figures` | Quản lý Nhân vật (Form hỗ trợ Prompt AI & Import JSON) |
| `GET` / `POST` / `DELETE` | `/admin/featured-figures` | `admin.featured-figures.*` | `admirable.presentation.web.routers.admin.featured_figures` | Quản lý danh sách nhân vật tiêu biểu hiển thị trang chủ |
| `POST` | `/admin/featured-figures/reorder` | `admin.featured-figures.reorder` | `admirable.presentation.web.routers.admin.featured_figures:reorder` | API lưu lại thứ tự kéo thả nhân vật tiêu biểu |
| Resource | `/admin/stories` | `admin.stories.*` | `admirable.presentation.web.routers.admin.stories` | Quản lý Mẩu chuyện ngắn (Story Snippets) |
| Resource | `/admin/contacts` | `admin.contacts.*` | `admirable.presentation.web.routers.admin.contacts` | Quản lý kênh liên hệ và thông tin phản hồi |
| `GET` / `POST` | `/admin/settings/about-us` | `admin.settings.about-us` / `.submit` | `admirable.presentation.web.routers.admin.settings` | Chỉnh sửa nội dung động trang "Về chúng tôi" |

### 3. Tác vụ AI Audio (Text-to-Speech) - `require_role("admin")`
| Phương thức | URI | Tên Route | Handler Python | Mô tả chức năng |
|---|---|---|---|---|
| `POST` | `/admin/audio/generate/{type}/{id}` | `admin.audio.generate` | `admirable.presentation.web.routers.admin.audio:generate_audio` | Kích hoạt dispatch job sinh audio nền qua Taskiq (`figure` hoặc `story`) |
| `POST` | `/admin/audio/cancel/{type}/{id}` | `admin.audio.cancel` | `admirable.presentation.web.routers.admin.audio:cancel_audio` | Hủy tác vụ sinh audio đang chờ/chạy |
| `GET` | `/admin/audio/status/{type}/{id}` | `admin.audio.status` | `admirable.presentation.web.routers.admin.audio:get_audio_status` | Polling trạng thái sinh audio (`idle`, `processing`, `completed`, `failed`, `cancelled`) |

### 4. Quản lý Nhân sự - `require_role("superadmin")`
| Phương thức | URI | Tên Route | Handler Python | Mô tả chức năng |
|---|---|---|---|---|
| Resource | `/admin/users` | `admin.users.*` | `admirable.presentation.web.routers.admin.users` | Quản lý tài khoản Admin (Index, Create, Store, Edit, Update, Destroy) |
