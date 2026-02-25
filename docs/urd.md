# Tài liệu Yêu cầu Người dùng (URD)

- **Tên dự án:** Trang web "The Admirable"
- **Phiên bản:** 1.0
- **Ngày tạo:** 24/02/2026

## 1. Giới thiệu (Introduction)

### 1.1 Mục đích tài liệu

Tài liệu này định nghĩa chi tiết các yêu cầu từ góc độ người dùng cho trang web "The Admirable". Tài liệu sẽ đóng vai trò là cơ sở để thiết kế giao diện (UI/UX), phát triển tính năng (Development), và kiểm thử (Testing) nhằm đảm bảo sản phẩm cuối cùng đáp ứng đúng tầm nhìn và mục tiêu đã đề ra.

### 1.2 Tóm tắt dự án

"The Admirable" là một nền tảng nội dung cung cấp các bài viết chất lượng cao về những tấm gương nổi tiếng, đáng ngưỡng mộ trên toàn thế giới trong nhiều lĩnh vực khác nhau (văn hóa, kinh tế, chính trị, đời sống...).

### 1.3 Mục tiêu dự án (Problem & Solution)

- **Vấn đề:** Người học IELTS thường cảm thấy chán nản, buồn ngủ và khó ghi nhớ kiến thức khi phải tiếp xúc với các bài báo học thuật khô khan.
- **Giải pháp:** Xây dựng một trang web cung cấp các bài đọc tiếng Anh (song ngữ) mang tính truyền cảm hứng, tích cực. Các bài viết được thiết kế đa phương tiện (có text, audio, video và các mẩu chuyện nhỏ) giúp việc tiếp thu từ vựng và luyện kỹ năng đọc (Reading) - nghe (Listening) trở nên tự nhiên, thú vị và đọng lại sâu sắc hơn.

## 2. Tổng quan hệ thống (System Overview)

### 2.1 Đối tượng người dùng

Hệ thống có 2 nhóm người dùng chính:

- **Người đọc (Khách truy cập - Guest):** Những người học IELTS, người muốn trau dồi tiếng Anh hoặc tìm kiếm nguồn cảm hứng tích cực. Không cần tạo tài khoản.
- **Quản trị viên (Admin):** Người sở hữu, quản lý nội dung trang web (đăng bài, chỉnh sửa, xóa bài, quản lý danh mục).

### 2.2 Phạm vi hệ thống

- **Frontend (Giao diện người dùng):** Cho phép người đọc duyệt bài viết, đọc chữ, nghe audio, xem video Youtube và các mẩu chuyện liên quan.
- **Backend (Hệ thống quản trị):** Nơi Admin đăng nhập bảo mật và quản trị toàn bộ dữ liệu nội dung của nền tảng.

## 3. Yêu cầu chức năng (Functional Requirements)

### 3.1 Dành cho Người đọc (Guest)

Vì trang web không có tính năng đăng ký/đăng nhập cho người dùng thường, mọi tính năng dưới đây đều được mở công khai.

#### F.G.01 - Xem Trang chủ (Homepage)

- Hiển thị các bài viết nổi bật hoặc mới nhất về các nhân vật đáng ngưỡng mộ.
- Hiển thị danh sách các lĩnh vực (Tags/Categories) để người dùng dễ dàng lọc nội dung.

#### F.G.02 - Phân loại & Tìm kiếm (Filter & Search)

- Người dùng có thể bấm vào các Tag (Ví dụ: Kinh tế, Chính trị, Khoa học, Nghệ thuật) để xem danh sách các nhân vật thuộc lĩnh vực đó.
- Lưu ý: Một nhân vật có thể xuất hiện ở nhiều lĩnh vực khác nhau (Ví dụ: Một chính trị gia cũng có thể thuộc lĩnh vực kinh tế).
- Có thanh tìm kiếm (Search bar) để tìm tên nhân vật hoặc từ khóa.

#### F.G.03 - Xem chi tiết Hồ sơ Nhân vật (Article Detail Page)

Đây là trang quan trọng nhất, bao gồm các thành phần:

- **Phần Bài đọc chính:** Văn bản trình bày rõ ràng, phân đoạn tốt, cung cấp tiểu sử và những thành tựu truyền cảm hứng của nhân vật.
- **Phần Nghe (Audio Player):** Trình phát âm thanh có các nút Play/Pause/Tua lại/Chỉnh tốc độ. Nội dung audio là giọng đọc lại chính bài viết đó, giúp người dùng luyện Listening và Pronunciation.
- **Phần Video (YouTube Embed):** Trình chiếu video liên quan đến nhân vật (phỏng vấn, phim tài liệu ngắn...) được nhúng trực tiếp từ link YouTube (giảm tải cho server).
- **Phần Mảnh ghép câu chuyện (Story Snippets):** Các thẻ (cards) hoặc dòng thời gian (timeline) ngắn kể về những giai thoại, câu chuyện nhỏ thú vị, hoặc trích dẫn (quotes) nổi tiếng của nhân vật.

#### F.G.04 - Mảnh ghép câu chuyện (Story Snippets)

Trang kể chi tiết về từng mẩu chuyện riêng lẻ kèm theo của nhân vật đó:

- **Phần Bài đọc chính:** Bà đọc về câu chuyện đó kể thật chi tiết.
- **Phần Nghe (Audio Player):** Trình phát âm thanh có các nút Play/Pause/Tua lại/Chỉnh tốc độ. Nội dung audio là giọng đọc lại chính bài viết đó, giúp người dùng luyện Listening và Pronunciation.
- **Phần Video (YouTube Embed):** Trình chiếu video liên quan đến nhân vật (phỏng vấn, phim tài liệu ngắn...) được nhúng trực tiếp từ link YouTube (giảm tải cho server).

### 3.2 Dành cho Quản trị viên (Admin)

#### F.A.01 - Đăng nhập (Admin Login)

- Trang đăng nhập ẩn (chỉ có form nhập Username/Password).

#### F.A.02 - Quản lý Danh mục/Lĩnh vực (Manage Categories)

- Admin có thể Thêm, Sửa, Xóa các lĩnh vực (Văn hóa, Chính trị...).

#### F.A.03 - Quản lý Hồ sơ Nhân vật (Manage Figures/Articles)

- Tạo bài viết mới với các trường dữ liệu: Tên nhân vật, Ảnh đại diện, Nội dung bài viết (Rich text editor).
- Gắn Tags lĩnh vực (Có thể chọn nhiều Tags cùng lúc - Multi-select).
- Tải lên file Audio (mp3) hoặc chèn link Audio.
- Chèn Link YouTube.
- Thêm/Sửa/Xóa các "Mảnh câu chuyện liên quan" (Story Snippets) cho nhân vật đó.

#### F.A.04 - Quản lý Mẩu chuyện của Nhân vật

- Thêm/Sửa/Xóa các "Mảnh câu chuyện liên quan" (Story Snippets) cho nhân vật đó một cách chi tiết.

#### F.A.05 - Đăng xuất (Logout)

- Đăng xuất khỏi hệ thống quản trị.

## 4. Yêu cầu phi chức năng (Non-Functional Requirements)

### 4.1 Thiết kế Giao diện & Trải nghiệm (UI/UX)

- **Phong cách:** Trang trọng (Formal), Tối giản (Minimalist), Hài hòa (Harmonious). Phong cách thiết kế chuẩn Apple

### 4.2 Khả năng tương thích (Responsiveness)

- Website phải hoạt động hoàn hảo và giao diện tự động thích ứng trên mọi thiết bị: Máy tính bàn (Desktop), Máy tính bảng (Tablet), và Điện thoại di động (Mobile). Trải nghiệm vuốt/đọc trên mobile phải được tối ưu cao nhất.

### 4.3 Hiệu suất & Tốc độ (Performance)

- Vì có chứa audio và video nhúng, trang web cần áp dụng Lazy Loading (chỉ tải hình ảnh/video khi người dùng cuộn tới) để đảm bảo tốc độ tải trang ban đầu dưới 3 giây.
- Tối ưu hóa hình ảnh tải lên để không làm chậm website.

### 4.4 Bảo mật (Security)

- Khu vực Admin (Backend) phải được bảo vệ bằng mật khẩu mạnh.
- Bảo vệ trang web khỏi các cuộc tấn công cơ bản (SQL Injection, XSS).
- Website cần được cài đặt chứng chỉ SSL (HTTPS) để đảm bảo an toàn kết nối.

## 5. Mô hình dữ liệu cơ bản (Data Model)

Để phục vụ việc trao đổi với lập trình viên, hệ thống sẽ bao gồm các thực thể chính sau:

- **Figure (Nhân vật):** ID, Tên, Ảnh đại diện, Nội dung bài chính, File Audio, Video (YouTube URL), Ngày tạo.
- **Category/Field (Lĩnh vực):** ID, Tên lĩnh vực.
- **Mối quan hệ:** Nhiều - Nhiều (Một nhân vật có nhiều lĩnh vực, một lĩnh vực có nhiều nhân vật).
- **Story Snippet (Mảnh câu chuyện):** ID, ID Nhân vật (Khóa ngoại), Tiêu đề mẩu chuyện, Nội dung mẩu chuyện, Hình ảnh đi kèm (nếu có), File audio, Video (Youtube URL), ....
- **Admin:** Username, Password (mã hóa).

## 6. Lộ trình triển khai đề xuất (Suggested Roadmap)

- **Giai đoạn 1 - Thiết kế UI/UX (Figma):** Lên thiết kế Wireframe và Mockup cho Trang chủ và Trang chi tiết nhân vật đảm bảo phong cách tối giản, trang trọng.
- **Giai đoạn 2 - Lập trình Frontend & Backend:** Xây dựng khung website, trang admin và kết nối cơ sở dữ liệu.
- **Giai đoạn 3 - Nhập liệu (Content Entry):** Quản trị viên đưa lên 5-10 nhân vật đầu tiên để test giao diện thực tế (cần có đủ Text, Audio, Video YouTube, Snippets).
- **Giai đoạn 4 - Kiểm thử & Ra mắt (Testing & Launch):** Kiểm tra lỗi hiển thị trên mobile, kiểm tra tốc độ tải trang và ra mắt chính thức.
