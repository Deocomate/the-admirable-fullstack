---
phase: 6
title: "Adapter: TTS, Queue, Storage, Security"
status: pending
priority: P1
effort: "2d"
dependencies: [5]
---

# Phase 6: Adapter — TTS, Queue, Storage, Security

## Overview

Hiện thực hoá 7 Port của Phase 5. Trọng tâm là hai thay đổi công nghệ lớn: **Azure Cognitive Speech → edge-tts** và **Laravel database queue → Taskiq + Redis**. Cả hai đều nằm sau Port, nên nếu sau này phải đổi lại thì chỉ đụng thư mục này.

## Requirements

**Functional**
- Sinh audio tiếng Anh từ `content_blocks` bằng edge-tts, không cần API key, xuất MP3.
- Worker Taskiq nhận task, chạy use case `GenerateAudio`, cập nhật state machine.
- Huỷ task giữa chừng hoạt động đúng như bản Laravel (3 lần kiểm tra trạng thái).
- Xác thực mật khẩu bcrypt `$2y$` sinh bởi Laravel vẫn đúng.
- Token reset mật khẩu lưu Redis, TTL 60 phút, dùng một lần.

**Non-functional**
- Task có timeout 180s và `max_retries=0` (khớp `$tries = 1` hiện tại — sinh lại audio là hành động do người dùng chủ động, không tự retry).
- Adapter TTS chia văn bản dài thành nhiều đoạn và ghép, tránh giới hạn độ dài của endpoint.
- Không ghi secret vào log.

## Architecture

**edge-tts vs Azure — khác biệt cần xử lý:**

| | Azure (cũ) | edge-tts (mới) |
|---|---|---|
| Xác thực | `Ocp-Apim-Subscription-Key` | Không cần |
| Đầu vào | SSML đầy đủ | Văn bản thuần + tham số `rate`/`volume`/`pitch` |
| Giọng | `en-US-AriaNeural` | Cùng danh mục giọng, giữ nguyên `en-US-AriaNeural` |
| Đầu ra | MP3 theo `X-Microsoft-OutputFormat` | MP3 (mặc định) |
| Giới hạn | ~10 phút/request | Nên chia đoạn, ghép stream |

Hệ quả: **bỏ toàn bộ code dựng SSML** (`buildSsml`, escape XML). Thay bằng `extract_english_text()` đã viết ở domain Phase 2 — trả về văn bản thuần nối bằng xuống dòng. Đơn giản hơn hẳn và ít điểm hỏng hơn.

`EdgeTtsAdapter.synthesize(text)` chia text theo đoạn (giới hạn ~3000 ký tự mỗi chunk, cắt ở ranh giới câu), gọi `edge_tts.Communicate(chunk, voice, rate, volume, pitch)` cho từng chunk, gom byte của các event `"audio"` từ `stream()`, nối lại. MP3 nối trực tiếp ở mức byte là hợp lệ cho playback trong trình duyệt.

**Cấu hình TTS mới** (`.env`): `TTS__VOICE=en-US-AriaNeural`, `TTS__RATE=+0%`, `TTS__VOLUME=+0%`, `TTS__PITCH=+0Hz`, `TTS__MAX_CHARS_PER_CHUNK=3000`. Các biến `AZURE_TTS_*` bị loại bỏ.

**Taskiq.** Broker `ListQueueBroker` của `taskiq-redis` + `RedisAsyncResultBackend`. Worker là process riêng trong compose. Task định nghĩa ở `infrastructure/queue/tasks.py`, nhận `(kind: str, entity_id: int)` — **chỉ truyền định danh, không truyền entity** (khớp cách `GenerateAudioJob` chỉ giữ `type` và `id`; tránh vấn đề serialize và dữ liệu cũ).

Worker phải tự dựng dependency (session DB, repository, adapter) — dùng cùng một hàm factory với web app, đặt ở `infrastructure/container.py`, để tránh hai đường dây DI lệch nhau.

**Bcrypt tương thích Laravel.** Laravel sinh hash tiền tố `$2y$`. Thư viện `bcrypt` của Python xác thực được `$2y$` (nó chỉ là biến thể ký hiệu của `$2b$`); nếu gặp vấn đề, chuẩn hoá tiền tố `$2y$` → `$2b$` trước khi `checkpw`, đây là phép biến đổi an toàn về mặt mật mã. Hash mới dùng `$2b$` với `rounds=12` khớp `BCRYPT_ROUNDS=12` hiện tại. `needs_rehash` trả `True` khi cost khác 12.

**Storage.** `LocalFileStorage` ghi vào `settings.media.root` (`/app/media`), trả về path tương đối (`uploads/avatars/x_123.jpg`) — **đúng định dạng đang lưu trong DB**, nên dữ liệu cũ dùng được ngay. Đặt tên file theo công thức hiện tại: `{slug}_{unix_timestamp}.{ext}`. Chống path traversal: chuẩn hoá và khẳng định đường dẫn cuối nằm trong media root.

## Related Code Files

- Create: `src/admirable/infrastructure/tts/edge_tts_adapter.py`, `text_chunker.py`
- Create: `src/admirable/infrastructure/queue/broker.py`, `tasks.py`
- Create: `src/admirable/infrastructure/storage/local_storage.py`
- Create: `src/admirable/infrastructure/security/password_hasher.py`, `redis_token_store.py`
- Create: `src/admirable/infrastructure/mail/{smtp_mailer,log_mailer}.py`
- Create: `src/admirable/infrastructure/clock.py`
- Create: `src/admirable/infrastructure/container.py` (factory dependency dùng chung web + worker)
- Create: `tests/unit/infrastructure/**`, `tests/integration/queue/**`
- Modify: `docker-compose.yml` (entrypoint worker), `.env.example` (bỏ `AZURE_TTS_*`, thêm `TTS__*`)
- Nguồn tham chiếu (đọc, không sửa): `app/Services/AzureTextToSpeechService.php`, `app/Jobs/GenerateAudioJob.php`, `app/Helpers/FileUploadHelper.php`

## Implementation Steps

1. `clock.py`: `SystemClock` trả `datetime.now(UTC)`.
2. `local_storage.py`: hiện thực `FileStoragePort`.
   - `save(file, directory, slug)` → tên `{slug or random16}_{int(time())}.{ext}`, tạo thư mục nếu thiếu, ghi bằng `aiofiles`, trả path tương đối.
   - `delete(path)` — no-op nếu file không tồn tại (khớp `FileUploadHelper::delete`).
   - `replace(file, old_path, directory, slug)` — xoá cũ rồi lưu mới.
   - Validate: khẳng định `(root / path).resolve()` là con của `root.resolve()`, ngược lại raise. Giới hạn extension theo whitelist ảnh/audio.
3. `text_chunker.py`: `chunk_text(text, max_chars)` cắt ở ranh giới câu (`.`, `!`, `?`, xuống dòng), không cắt giữa từ. Test với văn bản 20k ký tự.
4. `edge_tts_adapter.py`: hiện thực `TextToSpeechPort.synthesize(text) -> bytes`.
   - Chia chunk, với mỗi chunk tạo `edge_tts.Communicate(chunk, voice=..., rate=..., volume=..., pitch=...)`, duyệt `communicate.stream()`, gom `chunk["data"]` khi `chunk["type"] == "audio"`.
   - Timeout tổng thể qua `asyncio.timeout(150)`.
   - Raise `TtsSynthesisError` (ngoại lệ hạ tầng riêng) khi rỗng hoặc lỗi mạng; use case bắt và chuyển thành `audio_status=failed` + thông điệp cắt 500 ký tự.
   - Retry mức chunk: 2 lần, backoff 0.5s — khớp `->retry(2, 500)` của bản Azure.
5. `broker.py`: khởi tạo `ListQueueBroker(settings.redis.url)` + result backend. Ở môi trường test dùng `InMemoryBroker`.
6. `tasks.py`: `@broker.task(task_name="generate_audio")` async function `(kind: str, entity_id: int)`. Bên trong: mở session mới qua `container.build_worker_scope()`, dựng use case `GenerateAudio`, `await uc.execute(...)`. Bọc try/except ghi log; không để exception làm chết worker.
7. `TaskiqQueue` hiện thực `TaskQueuePort.enqueue_audio_generation(kind, id)` → `generate_audio.kiq(kind, id)`.
8. `container.py`: hai hàm factory — `build_request_scope(session)` cho web (Phase 7 dùng), `build_worker_scope()` cho worker. Cả hai trả về cùng một dataclass chứa mọi use case đã dựng sẵn dependency.
9. `password_hasher.py`: hiện thực `PasswordHasherPort` bằng `bcrypt`. `verify` chuẩn hoá tiền tố `$2y$`→`$2b$`. `hash` dùng `gensalt(rounds=12)`. Viết test dùng **hash thật lấy từ DB** (tài khoản `admin@gmail.com`, mật khẩu `Admin@123` theo `docs/superadmin_account.md`) để chứng minh tương thích ngược.
10. `redis_token_store.py`: hiện thực `TokenStorePort`. `issue(email)` sinh token `secrets.token_urlsafe(32)`, lưu `SETEX pwreset:{token} 3600 {email}`. `consume(token)` dùng Lua script `GET` + `DEL` nguyên tử để token dùng một lần.
11. `mail/`: `LogMailer` (mặc định dev, ghi link reset ra log — khớp `MAIL_MAILER=log` hiện tại) và `SmtpMailer` dùng `aiosmtplib` khi có cấu hình SMTP. Chọn adapter theo `settings.mail.driver`.
12. Cập nhật `docker-compose.yml`: service `worker` với `command: taskiq worker admirable.infrastructure.queue.broker:broker --workers 1`, cùng env và volume media như `web`.
13. Cập nhật `.env.example`: bỏ toàn bộ `AZURE_TTS_*`, thêm `TTS__*`, `REDIS__URL`, `MAIL__DRIVER`.
14. Viết integration test: dùng `InMemoryBroker`, enqueue → chạy → khẳng định `audio_status` chuyển `processing → completed` và file xuất hiện trong media root. Test huỷ: set `cancelled` giữa chừng bằng fake TTS chậm, khẳng định file tạm bị xoá.
15. Viết một smoke test **có mạng**, đánh dấu `@pytest.mark.network` (mặc định skip trong CI): gọi edge-tts thật với 1 câu, khẳng định trả về >1KB byte MP3.

## Success Criteria

- [ ] `pytest tests/unit/infrastructure tests/integration/queue` pass.
- [ ] Test tương thích bcrypt pass với hash `$2y$` thật từ DB hiện tại.
- [ ] Smoke test edge-tts (chạy tay) sinh được file MP3 phát được trong trình duyệt.
- [ ] Test huỷ chứng minh không để lại file mồ côi.
- [ ] `grep -ri "azure" src/` chỉ còn xuất hiện trong comment lịch sử (hoặc rỗng).
- [ ] Path traversal test: `save(..., directory="../../etc")` bị chặn.
- [ ] Worker container khởi động và nhận task khi `docker compose up`.

## Risk Assessment

**Rủi ro: edge-tts dùng endpoint không chính thức của Microsoft — có thể đổi giao thức, giới hạn tốc độ, hoặc chặn IP datacenter của VPS.** Đây là rủi ro thật và không kiểm soát được.
- Tín hiệu: tỉ lệ `audio_status=failed` vượt 20% trong 24h, hoặc smoke test mạng fail liên tục 3 ngày.
- Phản ứng đã chốt: vì đã có `TextToSpeechPort`, viết adapter thay thế mà không đụng use case. Thứ tự ưu tiên: (1) nâng phiên bản `edge-tts`, (2) `AzureTtsAdapter` (giữ code cũ, cần key trả phí), (3) Piper TTS chạy offline trong container (không phụ thuộc mạng, giọng kém tự nhiên hơn).

**Rủi ro: nối byte MP3 từ nhiều chunk gây lỗi metadata/thời lượng ở một số trình phát.** Mitigation: test bằng file nhiều chunk, kiểm tra bằng `ffprobe` trong container hoặc phát thử. Phản ứng nếu hỏng: thêm `ffmpeg` vào image và dùng `ffmpeg -f concat` để ghép đúng chuẩn — chi phí thấp, đã lường trước.

**Rủi ro: worker và web dùng hai đường DI khác nhau, gây lệch hành vi.** Mitigation: `container.py` là điểm dựng duy nhất, cả hai đều gọi. Test khẳng định `build_worker_scope()` dựng được cùng tập use case.

**Rủi ro: `$2y$` không verify được bằng `bcrypt` của Python.** Mitigation: bước 9 test bằng hash thật *trước khi* viết tiếp phần còn lại. Nếu chuẩn hoá tiền tố cũng không đủ, phản ứng: buộc reset mật khẩu cho toàn bộ admin ở lần cutover và thông báo cho user — chỉ có 1-2 tài khoản nên chi phí chấp nhận được, nhưng phải quyết định *trước* Phase 12.
