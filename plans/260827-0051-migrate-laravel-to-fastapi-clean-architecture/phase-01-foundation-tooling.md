---
phase: 1
title: "Nền tảng & Tooling"
status: completed
priority: P1
effort: "1.5d"
dependencies: []
---

# Phase 1: Nền tảng & Tooling

## Overview

Dựng bộ khung Python 3.14 chạy được: quản lý dependency bằng `uv`, khung thư mục Clean Architecture rỗng, cấu hình bằng `pydantic-settings`, và Docker Compose dựng đủ 5 service. Kết thúc phase, `docker compose up` trả về 200 ở `/healthz` — chưa có nghiệp vụ nào.

Phase này chốt lockfile **trước khi** viết code, để mọi rủi ro về wheel Python 3.14 lộ ra ngay lập tức thay vì ở phase 8.

## Requirements

**Functional**
- Ứng dụng FastAPI khởi động được, có endpoint `/healthz` kiểm tra kết nối MySQL và Redis.
- Cấu hình đọc từ biến môi trường, có validate và fail-fast khi thiếu giá trị bắt buộc.
- `docker compose up -d` dựng: `web`, `worker`, `mysql`, `redis`, `nginx`.

**Non-functional**
- Chạy đúng trên Python 3.14 (`requires-python = ">=3.14"`).
- Image production không chứa dev dependency; dùng multi-stage build.
- Container `web` chạy bằng user không phải root.

## Architecture

Chọn `uv` thay pip/poetry: nhanh, có lockfile chuẩn (`uv.lock`), hỗ trợ `--python 3.14` trực tiếp. Máy dev hiện **chưa cài uv** — bước đầu tiên là cài.

Cấu hình dùng `pydantic-settings.BaseSettings` đặt ở `src/admirable/config.py`. Đây là ngoại lệ được phép nằm ngoài 4 lớp: nó là cross-cutting concern, được inject vào lớp `infrastructure` và `presentation`, **không được import từ `domain` hay `application`**.

Cấu trúc Docker: mỗi service một trách nhiệm. `worker` và `web` dùng chung image, khác entrypoint.

```
web    → uvicorn admirable.presentation.web.main:app
worker → taskiq worker admirable.infrastructure.queue.broker:broker
nginx  → reverse proxy + phục vụ /static và /media trực tiếp (không qua Python)
```

Volume: `mysql_data` (DB), `media_data` mount vào `/app/media` (thay `storage/app/public`).

## Related Code Files

- Create: `pyproject.toml`, `uv.lock`, `.python-version`
- Create: `Dockerfile`, `docker-compose.yml`, `docker-compose.override.yml` (dev), `.dockerignore`
- Create: `deploy/nginx/default.conf`
- Create: `src/admirable/__init__.py`, `src/admirable/config.py`
- Create: khung thư mục rỗng có `__init__.py`: `domain/{entities,value_objects,repositories}`, `application/{use_cases,dto,ports}`, `infrastructure/{db,tts,storage,queue,security,mail}`, `presentation/{web,cli}`
- Create: `src/admirable/presentation/web/main.py` (app factory tối thiểu + `/healthz`)
- Create: `.env.example` (bản Python), `ruff.toml` hoặc mục `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` trong `pyproject.toml`
- Create: `tests/conftest.py`
- Modify: `.gitignore` (thêm `.venv/`, `__pycache__/`, `.ruff_cache/`, `.mypy_cache/`, `media/`)
- Không xoá gì ở phase này — Laravel vẫn còn nguyên để đối chiếu.

## Implementation Steps

<!-- Updated: Validation Session 1 - branch migrate/fastapi -->

0. Tạo và chuyển sang branch làm việc: `git checkout -b migrate/fastapi`. **Toàn bộ Phase 1-11 diễn ra trên branch này**; `main` giữ nguyên bản Laravel đang chạy production cho tới khi merge ở Phase 12.
1. Cài `uv`: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`. Xác nhận `uv --version`.
2. `uv init --python 3.14` tại repo root; đặt `.python-version` = `3.14`.
3. Khai báo dependency trong `pyproject.toml` và chạy `uv lock`. Nếu bất kỳ package nào không có wheel cp314, **dừng lại và báo cáo** trước khi đi tiếp.

   Runtime: `fastapi`, `uvicorn[standard]`, `jinja2`, `python-multipart`, `sqlalchemy>=2.0.52`, `alembic`, `asyncmy>=0.2.14`, `pydantic>=2.13`, `pydantic-settings`, `taskiq`, `taskiq-redis`, `redis`, `edge-tts`, `bcrypt`, `itsdangerous`, `aiofiles`, `python-slugify`, `typer`
   Dev: `pytest`, `pytest-asyncio`, `httpx`, `ruff`, `mypy`, `types-aiofiles`, `beautifulsoup4` (dùng cho HTML diff ở Phase 11)

4. Tạo khung thư mục Clean Architecture với `__init__.py` ở mọi package.
5. Viết `config.py`: `Settings(BaseSettings)` với các nhóm — `app` (name, env, debug, secret_key, base_url), `db` (host, port, user, password, database, pool size), `redis` (url), `tts` (voice, rate, volume, pitch), `media` (root path, url prefix), `session` (cookie name, lifetime seconds, secure flag), `mail`. Dùng `model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")`. `secret_key` bắt buộc, độ dài tối thiểu 32.
6. Viết `main.py`: hàm `create_app() -> FastAPI` tối thiểu, lifespan mở/đóng engine DB và Redis pool, endpoint `GET /healthz` trả `{"db": "ok", "redis": "ok"}` bằng cách `SELECT 1` và `PING`.
7. Viết `Dockerfile` multi-stage: stage `builder` cài uv + `uv sync --frozen --no-dev`; stage `runtime` dùng `python:3.14-slim`, copy `.venv` và `src`, tạo user `app`, `USER app`, `EXPOSE 8000`.
8. Viết `docker-compose.yml`: 5 service như mô tả ở trên; `mysql:8.4` với `--character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`; healthcheck cho mysql/redis; `web` và `worker` `depends_on` với `condition: service_healthy`.
9. Viết `docker-compose.override.yml` cho dev: bind-mount `./src`, bật `--reload`, expose port 8000 trực tiếp.
10. Viết `deploy/nginx/default.conf`: `location /static/` và `location /media/` phục vụ file tĩnh với `expires 30d`; còn lại `proxy_pass http://web:8000` kèm `X-Forwarded-Proto`/`X-Forwarded-For`. Giữ redirect HTTPS và bỏ trailing slash để khớp hành vi `.htaccess` cũ.
11. Cấu hình Ruff (line-length 100, chọn rule set `E,F,I,N,UP,B,SIM,RUF`), mypy (`strict = true` cho `src/admirable/domain` và `src/admirable/application`, nới hơn cho các lớp ngoài), pytest (`asyncio_mode = "auto"`).
12. Viết một smoke test gọi `/healthz` qua `httpx.ASGITransport`.

## Success Criteria

- [ ] `uv lock` thành công, `uv.lock` được commit, không package nào phải build từ source.
- [ ] `uv run pytest` pass smoke test.
- [ ] `docker compose up -d` → `curl localhost/healthz` trả `{"db":"ok","redis":"ok"}`.
- [ ] `ruff check src tests` và `mypy src` pass trên khung rỗng.
- [ ] Container `web` chạy bằng non-root (`docker compose exec web whoami` ≠ `root`).
- [ ] Cây thư mục 4 lớp tồn tại đầy đủ.
- [ ] Đang ở branch `migrate/fastapi`; `main` không có commit nào của Python.

## Risk Assessment

**Rủi ro: package thiếu wheel cp314.** Đã xác minh 8/2026: SQLAlchemy 2.0.52, asyncmy 0.2.14, pydantic-core, FastAPI đều có. Chưa xác minh: `taskiq-redis`, `edge-tts`, `asyncmy` trên môi trường Windows dev.
- Tín hiệu: `uv lock` phải build từ source, hoặc `uv sync` lỗi compile.
- Phản ứng đã chốt: với `edge-tts` (pure Python) — không thể xảy ra. Với `asyncmy` (Rust/Cython) — nếu Windows thiếu wheel, dev trên Windows chuyển sang chạy hoàn toàn trong Docker (Linux), không cài local venv. Với `taskiq-redis` — nếu hỏng, đổi sang `taskiq` + broker Redis tự viết trên `redis-py` (30 dòng), giữ nguyên interface.

**Rủi ro: Python 3.14 free-threading (GIL-free) build gây lỗi thư viện.** Phản ứng: dùng bản `cp314` thường (`python:3.14-slim`), **không** dùng `3.14t`. Ghi rõ trong Dockerfile.

**Rủi ro: nginx phục vụ `/media` không khớp đường dẫn DB.** DB lưu path tương đối dạng `uploads/audio/x.mp3`. Media root trong container là `/app/media`, URL prefix `/media/`. Kiểm chứng ngay ở phase này bằng cách đặt một file test và `curl`.
