# Page Sitemap

## 1. Phân hệ Giao diện Người đọc (Thư mục: `/client` hoặc root `/`)

Đây là khu vực public, nơi người dùng cuối sẽ truy cập. Cấu trúc này được thiết kế để dễ dàng chuyển đổi thành các route (tuyến đường) tĩnh hoặc động trong tương lai.

- `index.html` — Màn hình Trang chủ (Homepage).
- `search.html` — Màn hình Kết quả Tìm kiếm (Search Results).
- `category.html` — Màn hình Danh sách theo Lĩnh vực.  
	Lưu ý: Khi ghép code thực tế, trang này thường sẽ nhận tham số ID hoặc slug của lĩnh vực.
- `figure-detail.html` — Màn hình Chi tiết Hồ sơ Nhân vật. Nơi chứa audio bài đọc chính và video YouTube tổng quan.
- `story-detail.html` — Màn hình Chi tiết Mẩu chuyện. Dành riêng cho từng giai thoại nhỏ với audio/video riêng lẻ.
- `about-us.html` — Giới thiệu về project này, mục đích hướng tới.

## 2. Phân hệ Hệ thống Quản trị (Thư mục: `/admin`)

Khu vực này dành riêng cho quản trị viên, cần một bố cục (layout) riêng biệt, thường bao gồm một Sidebar (thanh bên) bên trái và Topbar (thanh trên) cố định.

- `login.html` — Màn hình Đăng nhập (Admin Login). Layout độc lập, không chứa sidebar.
- `index.html` (hoặc `dashboard.html`) — Màn hình Bảng điều khiển trung tâm (Dashboard).
- `categories.html` — Màn hình Quản lý Danh mục/Lĩnh vực (Bảng danh sách).
- `figures.html` — Màn hình Quản lý Hồ sơ Nhân vật (Bảng danh sách).
- `figure-form.html` — Màn hình Thêm mới hoặc Chỉnh sửa Nhân vật.  
	Gộp chung giao diện Add/Edit vào một form, chỉ khác trạng thái nút Lưu.
- `stories.html` — Màn hình Quản lý Mẩu chuyện (Bảng danh sách).
- `story-form.html` — Màn hình Thêm mới hoặc Chỉnh sửa Mẩu chuyện.
- `about-us-form.html` — Quản lý phần About Us.
