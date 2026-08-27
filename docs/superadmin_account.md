# Quản lý Tài khoản & Phân quyền (Roles & Permissions)

## 1. Cấp độ phân quyền (Roles)

Hệ thống quản trị sử dụng enum `Role` (`superadmin`, `admin`) được định nghĩa tại `src/admirable/domain/value_objects/role.py` và lưu trữ trong bảng `users`.
Việc bảo vệ routes được thực hiện qua FastAPI Dependency `require_role(Role.ADMIN)` hoặc `require_role(Role.SUPERADMIN)` trong `src/admirable/presentation/web/dependencies.py`.

### Superadmin
- Có toàn quyền quản trị nội dung và cấu hình trên toàn hệ thống.
- Là vai trò duy nhất có quyền truy cập module Quản lý Tài khoản (`/admin/users`) để tạo, phân quyền, cập nhật hoặc xóa tài khoản Admin.
- **Ràng buộc an toàn:** Hệ thống ngăn chặn việc xóa tài khoản Superadmin duy nhất hoặc tự xóa chính mình thông qua các điều kiện kiểm tra nghiệp vụ trong domain entity `User` (`src/admirable/domain/entities/user.py`) và use case `DeleteUserUseCase` (`src/admirable/application/use_cases/users/delete_user.py`).

### Admin
- Quản lý toàn bộ nội dung nghiệp vụ: Lĩnh vực, Nhân vật, Mẩu chuyện, Danh sách tiêu biểu, Kênh liên hệ, Cấu hình trang Giới thiệu.
- Bị chặn truy cập các route yêu cầu quyền Superadmin (`/admin/users`) và tự động chuyển hướng hoặc trả về mã lỗi 403 Forbidden.

---

## 2. Tài khoản Mặc định khi Khởi tạo (CLI Seeder)

Khi thực thi lệnh `uv run python -m admirable.presentation.cli.seed`, hệ thống sẽ tự động tạo một tài khoản Superadmin mặc định:

| Thuộc tính | Giá trị mặc định |
|---|---|
| **Họ & tên** | `Super Admin` |
| **Email** | `admin@gmail.com` |
| **Mật khẩu** | `Admin@123` |
| **Vai trò (Role)** | `superadmin` |

> [!TIP]
> Khi triển khai môi trường thực tế (Production), hãy đăng nhập và đổi ngay mật khẩu hoặc cập nhật tài khoản quản trị mới thông qua trang Quản lý tài khoản (`/admin/users`).