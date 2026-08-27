# URD (User Requirements Document)

## 1. Bối cảnh & Vấn đề (Problem Statement)

Việc học tiếng Anh nâng cao và rèn luyện kỹ năng Đọc (Reading) & Nghe (Listening) phục vụ các kỳ thi học thuật như IELTS thường gặp phải rào cản:
- Các tài liệu học thuật truyền thống thường khô khan, nặng tính lý thuyết, thiếu tính kết nối cảm xúc.
- Người học nhanh chóng cảm thấy quá tải, mất động lực và gặp khó khăn trong việc ghi nhớ từ vựng nâng cao trong ngữ cảnh thực tế.

---

## 2. Giải pháp (Solution)

**The Admirable** ra đời nhằm biến hành trình học tiếng Anh thành trải nghiệm khám phá và truyền cảm hứng:
- Cung cấp các bài viết song ngữ Anh - Việt chất lượng cao về cuộc đời, sự nghiệp và tư tưởng của các nhân vật vĩ đại trong lịch sử.
- Tích hợp hệ sinh thái đa phương tiện: văn bản song ngữ, giọng đọc audio tự nhiên (có điều chỉnh tốc độ và khuếch đại âm lượng) và video minh họa.
- Giao diện tối giản, thanh lịch lấy cảm hứng từ Apple giúp người học tập trung tối đa vào nội dung.

---

## 3. Chân dung Người dùng & Yêu cầu chức năng (Personas & Requirements)

### 👤 1. Guest (Học viên / Người học tiếng Anh)
- **Mục tiêu:** Cải thiện vốn từ vựng, ngữ pháp và kỹ năng Reading/Listening IELTS một cách tự nhiên.
- **Hành vi & Trải nghiệm:**
  - Đọc bài viết song ngữ theo từng khối đoạn văn (`paragraph`, `heading`, `quote`).
  - Nghe audio bài viết với trình phát trực quan (tua nhanh/chậm, tăng âm lượng).
  - Xem video YouTube tư liệu liên quan đến nhân vật.
  - Tìm kiếm nhân vật theo tên, lĩnh vực hoặc từ khóa nội dung; khám phá các chủ đề xu hướng (Trending).
  - Đọc các mẩu chuyện ngắn truyền cảm hứng (Story Snippets).
  - Tìm hiểu về nền tảng qua trang "Về chúng tôi" và gửi thông tin phản hồi qua trang "Liên hệ".

### 👨‍💼 2. Admin (Biên tập viên / Quản trị nội dung)
- **Mục tiêu:** Soạn thảo, biên tập và xuất bản nội dung chất lượng cao với tốc độ nhanh chóng.
- **Hành vi & Trải nghiệm:**
  - Quản lý CRUD Lĩnh vực (Categories), Nhân vật (Figures), Mẩu chuyện ngắn (Stories), Kênh liên hệ (Contacts).
  - Sử dụng công cụ hỗ trợ AI: Sao chép Prompt mẫu để tạo bài viết với ChatGPT/Claude, sau đó dán (import) dữ liệu JSON trực tiếp vào form.
  - Kích hoạt tính năng tạo Audio tự động bằng AI (edge-tts), theo dõi tiến trình nền qua Queue Job và hủy tác vụ khi cần.
  - Tùy chỉnh danh sách nhân vật tiêu biểu hiển thị trên Trang chủ bằng thao tác kéo thả trực quan (SortableJS).
  - Cập nhật nội dung các khối giới thiệu động trên trang "Về chúng tôi".

### 🛡️ 3. Superadmin (Quản trị viên Hệ thống)
- **Mục tiêu:** Đảm bảo hệ sinh thái hoạt động ổn định, phân quyền và kiểm soát nhân sự.
- **Hành vi & Trải nghiệm:**
  - Sở hữu toàn bộ quyền hạn của Admin.
  - Quản lý tài khoản quản trị viên: Tạo mới, chỉnh sửa thông tin, đặt lại mật khẩu hoặc xóa tài khoản Admin.
  - Theo dõi thống kê tổng quan hệ thống trên Dashboard.
