# The Admirable - Học tiếng Anh qua những tầm cao nhân loại

The Admirable là một nền tảng giáo dục trực tuyến nhằm biến quá trình học tiếng Anh (đặc biệt là kỹ năng Reading & Listening IELTS) từ khô khan trở nên đầy cảm hứng thông qua các bài viết song ngữ về những nhân vật vĩ đại trên thế giới.

## 🚀 Tính năng nổi bật

### Client (Giao diện người dùng)
- **Đọc hiểu song ngữ:** Các bài viết được cấu trúc theo dạng đoạn văn Anh - Việt đan xen.
- **Hệ sinh thái đa phương tiện:** Hỗ trợ Audio player (đọc bài viết) điều chỉnh được tốc độ, và nhúng Video Youtube.
- **Mảnh ghép câu chuyện (Story Snippets):** Các mẩu chuyện ngắn xoay quanh nhân vật.
- **Tìm kiếm thông minh:** Tìm kiếm theo tên, lĩnh vực và nội dung; có gợi ý xu hướng (Trending).
- **Giao diện chuẩn Apple:** UI/UX tinh tế, thiết kế tối giản, hỗ trợ responsive hoàn hảo bằng TailwindCSS + Vanilla JS.

### Admin Panel
- **Mô hình Service Pattern:** Code clean, dễ bảo trì (`Controller` gọi `Service`).
- **Tích hợp AI tạo nội dung:** Form thêm nhân vật hỗ trợ xuất prompt cho AI (ChatGPT/Claude) và import trực tiếp từ JSON do AI tạo ra.
- **Quản lý linh hoạt:** Quản lý Lĩnh vực, Nhân vật, Mẩu chuyện, Liên hệ.
- **Trang Giới thiệu động (Settings):** Chỉnh sửa nội dung trang "Về chúng tôi" thông qua giao diện dạng Form block thay vì hardcode.
- **Phân quyền:** Superadmin (toàn quyền + quản lý tài khoản) và Admin (chỉ quản lý nội dung).

## 🛠 Tech Stack
- **Backend:** Laravel 12, PHP 8.2+
- **Frontend:** TailwindCSS, Vanilla JavaScript, Blade Templates.
- **Database:** MySQL / SQLite.
- **Khác:** Web Audio API (xử lý âm lượng vượt 100%), SortableJS (kéo thả thứ tự nhân vật tiêu biểu).

## 💻 Hướng dẫn cài đặt (Local Development)

1. **Clone repository và cài đặt thư viện:**
   ```bash
   git clone <repo-url>
   cd the-admirable
   composer install
   ```

2. **Cấu hình môi trường:**
   ```bash
   cp .env.example .env
   php artisan key:generate
   ```
   *Thiết lập thông tin Database trong file `.env`.*

3. **Chạy Migration và Seed dữ liệu:**
   *(Cần thiết để tạo tài khoản Superadmin và thiết lập giao diện)*
   ```bash
   php artisan migrate --seed
   ```

4. **Tạo Symlink cho storage (Rất quan trọng cho Media):**
   ```bash
   php artisan storage:link
   ```

5. **Chạy server:**
   ```bash
   php artisan serve
   ```
   *Truy cập Client tại: `http://localhost:8000`*
   *Truy cập Admin tại: `http://localhost:8000/admin/login`*
