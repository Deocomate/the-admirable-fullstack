---
phase: 5
title: "Lớp Application — Use Cases"
status: completed
priority: P1
effort: "3d"
dependencies: [4]
---

# Phase 5: Lớp Application — Use Cases

## Overview

Chuyển toàn bộ business logic từ 9 class trong `app/Services/` thành use case. Mỗi use case là một class có một phương thức `execute()`, nhận DTO vào, trả DTO ra, phụ thuộc vào Protocol repository và Port — không bao giờ vào SQLAlchemy, FastAPI, hay filesystem trực tiếp.

Đây là nơi "dễ bảo trì" thực sự thành hiện thực: mỗi hành vi nghiệp vụ có một file, một test, không phụ thuộc hạ tầng.

## Requirements

**Functional**
- Mọi hành động nghiệp vụ hiện có đều có use case tương ứng (bảng ánh xạ ở phần Architecture).
- DTO đầu vào/ra bằng Pydantic v2, không lộ ORM model hay entity ra ngoài khi không cần.
- Port được định nghĩa ở đây, hiện thực ở Phase 6.

**Non-functional**
- `mypy --strict` pass trên toàn bộ `application`.
- Unit test dùng fake repository in-memory, không cần DB.
- Không use case nào import `infrastructure` hoặc `presentation`.

## Architecture

**Ports định nghĩa ở phase này** (`application/ports/`):

| Port | Dùng cho | Hiện thực ở Phase 6 |
|---|---|---|
| `FileStoragePort` | `save(file, directory, slug) -> str`, `delete(path)`, `exists(path)` | `LocalFileStorage` |
| `TextToSpeechPort` | `synthesize(text: str) -> bytes` | `EdgeTtsAdapter` |
| `TaskQueuePort` | `enqueue_audio_generation(kind, id)` | `TaskiqQueue` |
| `PasswordHasherPort` | `hash(pw)`, `verify(pw, hash)`, `needs_rehash(hash)` | `BcryptPasswordHasher` |
| `MailerPort` | `send_password_reset(email, token)` | `SmtpMailer` / `LogMailer` |
| `TokenStorePort` | `issue(email) -> token`, `consume(token) -> email \| None` | `RedisTokenStore` |
| `ClockPort` | `now() -> datetime` | `SystemClock` (giúp test tất định) |

**Ánh xạ Laravel Service → Use Case:**

| Laravel | Use cases mới |
|---|---|
| `FigureService` | `figures/list_figures`, `get_figure`, `create_figure`, `update_figure`, `delete_figure` |
| `StorySnippetService` | `stories/` — 5 use case tương tự |
| `CategoryService` | `categories/` — 5 use case |
| `ContactService` | `contacts/` — 5 use case |
| `FeaturedFigureService` | `featured/list_featured`, `add_featured`, `remove_featured`, `reorder_featured` |
| `UserService` | `users/list_users`, `create_user`, `update_user`, `delete_user` |
| `SettingService` | `settings/get_about_us`, `update_about_us` |
| `AuthService` | `auth/login`, `logout`, `request_password_reset`, `reset_password` |
| `AzureTextToSpeechService` + `GenerateAudioJob` | `audio/request_generation`, `cancel_generation`, `get_generation_status`, `generate_audio` (chạy trong worker) |
| Client controllers (logic truy vấn) | `public/get_home_page`, `search_figures`, `get_figure_detail`, `get_story_detail`, `list_categories`, `get_category_page`, `get_about_us_page`, `get_contact_page` |

**Quy ước:** một file = một use case, tên file snake_case khớp tên class. Constructor nhận dependency, `execute()` nhận input DTO.

```python
class CreateFigure:
    def __init__(self, figures: FigureRepository, storage: FileStoragePort) -> None: ...
    async def execute(self, cmd: CreateFigureCommand) -> FigureDetailDTO: ...
```

**Xử lý file upload.** Logic hiện nằm trong `FigureService` (upload avatar/audio, replace, delete khi xoá figure) chuyển sang use case và gọi qua `FileStoragePort`. Use case nhận đối tượng file đã trừu tượng hoá (`UploadedFileDTO` gồm `filename`, `content_type`, `stream`), không nhận `UploadFile` của FastAPI.

**Xử lý xoá cascade + file.** `DeleteFigure` phải: đọc figure kèm story snippets → xoá file avatar/audio của figure và image/audio của mọi snippet → gọi `repo.delete(id)` (DB tự cascade). Đúng thứ tự như `FigureService::delete` hiện tại.

## Related Code Files

- Create: `src/admirable/application/ports/*.py` (7 file)
- Create: `src/admirable/application/dto/*.py`
- Create: `src/admirable/application/use_cases/{figures,stories,categories,contacts,featured,users,settings,auth,audio,public}/*.py`
- Create: `tests/unit/application/**`, `tests/fakes/**` (fake repository + fake port)
- Nguồn tham chiếu (đọc, không sửa): toàn bộ `app/Services/*.php`, `app/Http/Controllers/Client/*.php`, `app/Http/Controllers/Admin/*.php`, `app/Jobs/GenerateAudioJob.php`

## Implementation Steps

1. Viết 7 Port dưới dạng `Protocol` trong `application/ports/`. Kèm `UploadedFileDTO` trong `application/dto/files.py`.
2. Viết DTO: command (đầu vào, ứng với từng form) và read model (đầu ra, ứng với từng template). Ví dụ `HomePageDTO(categories, featured_figure, latest_figures, stats)` khớp chính xác biến mà `client.home.index` cần.
3. Viết fake repository in-memory trong `tests/fakes/` cho mọi Protocol — dùng dict, không DB. Đây là nền cho toàn bộ unit test của phase.
4. **Nhóm `figures`** — port từ `FigureService`:
   - `CreateFigure`: sinh slug duy nhất qua `SlugGenerator`, normalize key_facts và content_blocks (đã có ở domain), `rebuild_search_text()`, upload avatar/audio nếu có, `sync_categories`.
   - `UpdateFigure`: chỉ đổi slug khi tên đổi (giữ logic `$figure->slug !== $slug` hiện tại — quan trọng cho SEO), replace file, sync categories.
   - `DeleteFigure`: theo thứ tự ở phần Architecture.
   - `ListFigures`, `GetFigure`.
5. **Nhóm `stories`** — tương tự, thêm ràng buộc `figure_id` phải tồn tại.
6. **Nhóm `categories`, `contacts`** — CRUD đơn giản. `DeleteCategory` chỉ detach quan hệ, không xoá figure.
7. **Nhóm `featured`** — `AddFeatured` chặn trùng (`figure_id` unique), gán `priority` = max+1; `ReorderFeatured` nhận list id, ghi lại priority theo thứ tự.
8. **Nhóm `users`** — `DeleteUser` gọi `User.can_be_deleted_by(actor, superadmin_count)` ở domain; use case chỉ lấy `count_superadmins()` rồi gọi. `CreateUser`/`UpdateUser` hash mật khẩu qua `PasswordHasherPort`; `UpdateUser` chỉ đổi mật khẩu khi trường được điền (khớp hành vi form hiện tại).
9. **Nhóm `settings`** — `GetAboutUs` đọc key `about_us_data`, parse JSON, merge với `AboutUsContent.default()`. `UpdateAboutUs` serialize với `ensure_ascii=False` (tương đương `JSON_UNESCAPED_UNICODE`).
10. **Nhóm `auth`**:
    - `Login`: lấy user theo email, `hasher.verify`, nếu `needs_rehash` thì hash lại và lưu (đường nâng cấp bcrypt→argon2 trong tương lai). Trả về `AuthenticatedUserDTO` hoặc raise `InvalidCredentialsError`. **Việc tạo session là của lớp presentation**, không phải use case.
    - `RequestPasswordReset`: `TokenStorePort.issue(email)` → `MailerPort.send_password_reset`. Không tiết lộ email có tồn tại hay không (trả cùng một kết quả).
    - `ResetPassword`: `consume(token)` → hash mật khẩu mới → lưu. Token dùng một lần.
11. **Nhóm `audio`** — port từ `AudioController` + `GenerateAudioJob`:
    - `RequestAudioGeneration(kind, id)`: nạp entity, gọi `entity.request_audio_generation()` (state machine ở domain sẽ raise nếu đang `processing`), lưu, rồi `queue.enqueue_audio_generation(kind, id)`. **Bỏ hoàn toàn kiểm tra "Azure TTS key is not configured"** — edge-tts không cần key.
    - `CancelAudioGeneration(kind, id)`: gọi `entity.cancel_audio()`, lưu.
    - `GetAudioStatus(kind, id)`: trả `status`, `error`, `audio_url`.
    - `GenerateAudio(kind, id)` — chạy trong worker, port từ `GenerateAudioJob::handle`. Giữ nguyên **cả 3 lần kiểm tra trạng thái** của bản Laravel: trước khi gọi TTS, sau khi gọi TTS, và sau khi ghi file (nếu đã bị huỷ thì xoá file vừa ghi). Đây là cơ chế huỷ an toàn, không được lược bỏ.
12. **Nhóm `public`** — port từ các Client controller:
    - `GetHomePage`: featured 7 bản ghi → phần tử đầu là `featured_figure`, 6 phần tử sau là `latest_figures`; nếu chưa đủ 6 thì bù bằng figure mới nhất chưa nằm trong danh sách (giữ nguyên thuật toán `HomeController`). Kèm `stats` (đếm figures/categories/stories).
    - `SearchFigures`: uỷ quyền cho `repo.search()`, kèm `trending_figures` (4 bản ghi nhiều snippet nhất) và danh sách category.
    - `GetFigureDetail(slug)`: figure + categories + story snippets + related figures (cùng category).
    - `GetStoryDetail(id)`, `GetCategoryPage(slug)`, `ListCategories`, `GetAboutUsPage`, `GetContactPage` (contacts active + ordered).
13. Viết unit test cho mọi use case bằng fake. Bắt buộc phủ: ràng buộc xoá user (2 trường hợp), state machine audio (bao gồm huỷ giữa chừng), thuật toán bù figure ở trang chủ (0/3/6/10 featured), slug không đổi khi tên không đổi, xoá figure có xoá đúng file.

## Success Criteria

- [ ] Mọi phương thức public trong `app/Services/*.php` có use case tương ứng (bảng đối chiếu trong PR).
- [ ] `grep -rE "^(from|import) admirable\.(infrastructure|presentation)" src/admirable/application` rỗng.
- [ ] `mypy --strict src/admirable/application` pass.
- [ ] `pytest tests/unit/application` pass, coverage ≥ 85%.
- [ ] `GenerateAudio` có test chứng minh: huỷ sau khi TTS trả về nhưng trước khi cập nhật DB → file tạm bị xoá, `audio_path` không đổi.
- [ ] `GetHomePage` có test cho cả 4 tình huống số lượng featured.

## Risk Assessment

**Rủi ro: bỏ sót một nhánh logic ẩn trong controller Laravel (không nằm trong Service).** Đã phát hiện một số ví dụ khi scout: `HomeController` chứa thuật toán bù figure, `SearchController` chứa toàn bộ logic search — cả hai **không** nằm trong service. Mitigation: bước 12 đọc trực tiếp controller, không chỉ đọc service. Tín hiệu bỏ sót: một trang render thiếu dữ liệu ở Phase 9/10. Phản ứng: bổ sung use case, không nhét logic vào router.

**Rủi ro: DTO phình to, lặp lại entity.** Mitigation: read-model DTO được thiết kế theo *template cần gì*, không theo *bảng có gì*. Nếu một DTO có >15 trường, tách theo section của trang.

**Rủi ro: use case gọi `datetime.now()` trực tiếp làm test không tất định.** Mitigation: `ClockPort` bắt buộc cho mọi chỗ cần thời gian. Test enforce bằng `grep` cấm `datetime.now(` trong `application/`.
