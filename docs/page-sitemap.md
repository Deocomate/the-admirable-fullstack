# Cấu trúc Sitemap (Route Map)

Dự án được chia thành 2 không gian chính: Client (Public) và Admin (Quản trị).

## 🌍 Khách hàng (Client)
- `/` - Trang chủ (Featured, Latest, Danh mục, Stat)
- `/linh-vuc` - Danh sách tất cả nhân vật theo lĩnh vực
- `/linh-vuc/{slug}` - Lọc nhân vật theo 1 lĩnh vực cụ thể
- `/tim-kiem?q={key}&category={slug}` - Tìm kiếm nhân vật
- `/nhan-vat/{slug}` - Chi tiết nhân vật (Nội dung song ngữ, Media, Fact, Story Snippets liên quan)
- `/cau-chuyen/{id}` - Chi tiết mẩu chuyện
- `/ve-chung-toi` - Trang giới thiệu nền tảng
- `/lien-he` - Thông tin liên hệ và CTA hợp tác

## 🔒 Quản trị (Admin)
- `/admin/login` - Đăng nhập
- `/admin/forgot-password` & `/admin/reset-password` - Quên mật khẩu
- `/admin/dashboard` - Bảng điều khiển, thống kê số liệu
- `/admin/categories` - CRUD Lĩnh vực
- `/admin/figures` - CRUD Nhân vật (Form hỗ trợ tạo AI Prompt & Import JSON)
- `/admin/featured-figures` - Quản lý danh sách nhân vật ghim lên Trang chủ (Hỗ trợ kéo thả)
- `/admin/stories` - CRUD Mẩu chuyện ngắn (Snippet)
- `/admin/contacts` - Quản lý kênh liên hệ
- `/admin/settings/about-us` - Chỉnh sửa nội dung động của trang "Về chúng tôi"
- `/admin/users` - Quản lý tài khoản Admin (Chỉ Superadmin mới truy cập được)
