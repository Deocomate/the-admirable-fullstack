# Quy chuẩn & Kiến trúc dự án (Rules)

## 1. Cấu trúc thư mục Backend (Service Pattern)
Dự án áp dụng Service Pattern để giảm tải logic cho Controller.
- **Controller** (`app/Http/Controllers`): Chỉ làm nhiệm vụ nhận Request, Validate (thông qua FormRequest) và trả về View/Response.
- **Service** (`app/Services`): Nơi xử lý Business Logic (Ví dụ: Upload file, format data, thao tác với Model).
- **Helper** (`app/Helpers/FileUploadHelper.php`): Xử lý chung các tác vụ xóa/upload file vật lý.

## 2. Xử lý Dữ liệu Nội dung (Content Blocks)
Để hỗ trợ nội dung song ngữ linh hoạt, bảng `figures` và `story_snippets` không dùng cột `text` lưu HTML thông thường mà dùng **cột kiểu JSON (`content_blocks`)**.

Cấu trúc JSON quy định gồm 3 type chính:
- `paragraph`: Gồm `text_en`, `text_vi`, `heading_en` (Tùy chọn).
- `heading`: Gồm `text_en`.
- `quote`: Gồm `text_en`, `author`.

*(Lưu ý: Có hàm fallback build lại cột `content` dạng text thuần để dễ search trong database).*

## 3. Quy chuẩn Frontend
- **TailwindCSS:** KHÔNG dùng build step phức tạp (Node.js/NPM), Tailwind được load qua script cdn tĩnh trong layout với custom config ở tag `<script>`.
- **UI/UX Design System:** Lấy cảm hứng từ thiết kế của Apple. Sử dụng các biến màu tự định nghĩa: `apple-black`, `apple-gray`, `apple-blue`, `apple-bg`.
- **JavaScript:** Chỉ dùng **Vanilla JS**. Không dùng framework. Các script (Scroll reveal, Audio Player, Drag & Drop) được quản lý ngay trong các file `.blade.php`.