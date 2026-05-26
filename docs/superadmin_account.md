# Quản lý tài khoản và Phân quyền

## 1. Cấp độ phân quyền (Roles)
Hệ thống sử dụng cột `role` kiểu `enum('superadmin', 'admin')` trong bảng `users`.
Việc bảo vệ routes được thực hiện qua `App\Http\Middleware\RoleMiddleware` (đã đăng ký alias `role` trong `bootstrap/app.php`).

- **Superadmin:**
  - Có toàn quyền truy cập toàn bộ hệ thống.
  - Là role duy nhất có thể truy cập `/admin/users` để tạo/sửa/xóa các tài khoản Admin khác.
  - Không thể bị xóa khỏi hệ thống thông qua giao diện (đã hardcode check trong `UserService`).

- **Admin:**
  - Có thể quản lý toàn bộ nội dung (Nhân vật, bài viết, cài đặt trang).
  - Bị chặn truy cập trang Quản lý nhân sự.

## 2. Tài khoản Default (Seeder)
Khi chạy lệnh `php artisan db:seed`, một tài khoản Superadmin mặc định sẽ được tạo. 
*(Vui lòng tham khảo file `database/seeders/UserSeeder.php` trong code để biết thông tin đăng nhập cụ thể, hoặc thay đổi `.env` tùy theo logic seeder hiện tại của bạn).*

Gợi ý tài khoản test nội bộ (nếu có):
- **Email:** `admin@theadmirable.com` (hoặc email của bạn)
- **Password:** `password`