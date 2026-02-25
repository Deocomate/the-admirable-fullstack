# Coding Rules

## Code Flow (Bắt buộc)
Luồng code phải tuân thủ chặt chẽ theo thứ tự sau:

`/routes/web.php` → `/app/Models` → `/app/Services` → `/app/Http/Controllers` → `/resources/views`

## Helpers
- Tạo helper khi cần thiết.
- Vị trí helper: `/app/Helpers`.

## Quy tắc phân tách component tái sử dụng
- Component tái sử dụng phải tách rõ theo ngữ cảnh `admin` và `client`.
- Không dùng chung lẫn lộn giữa hai khu vực nếu không có lý do rõ ràng.

## Quy tắc đặt tên View
Khi tạo view, bắt buộc tuân thủ pattern:

- `admin.{module_name}.{action}.blade.php`
- `client.{module_name}.{action}.blade.php`

## Quy tắc đặt tên Component
Khi tạo component, bắt buộc tuân thủ pattern:

- `components.admin.{component_group_name}.{component_name}.blade.php`
- `components.client.{component_group_name}.{component_name}.blade.php`

## Quy tắc Layout
- Layout của `admin` và `client` phải được tách thành các component tái sử dụng.
- Vị trí lưu:
	- `/resources/views/components/admin`
	- `/resources/views/components/client`

## Tiêu chuẩn chất lượng code
- Code sạch, chuẩn, dễ đọc, dễ bảo trì, dễ tái sử dụng.
- Tuân thủ đúng quy tắc và cú pháp của PHP/Laravel.

## TailwindCSS
- Luôn luôn sử dụng cdn.
- Không sử dụng vite, npm, ... các tiện ích mà chỉ sử dụng thư viện từ link cdn.