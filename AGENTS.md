# AGENTS.md

Process rules and operational memory for AI agents working on **The Admirable**.

## Tooling & Commands

- **Language & Runtime:** Python 3.14+, FastAPI, Jinja2, SQLAlchemy 2.0 (Async), Taskiq, Redis, MySQL.
- **Package Manager:** `uv` (Astral).
- **Run Tests:** `uv run pytest` (or single test: `uv run pytest tests/path/to/test.py` / `uv run pytest -k test_name`).
- **Architecture Tests:** `uv run pytest tests/architecture/` (enforces layer boundaries).
- **Code Formatter & Linter:** `uv run ruff check .` and `uv run ruff format .` (run before finishing changes).
- **Type Checker:** `uv run mypy src`
- **Run Server:** `uv run uvicorn admirable.presentation.web.main:app --reload --port 8000`
- **Run Queue Worker:** `uv run taskiq worker admirable.infrastructure.queue.tasks:broker` (required for async edge-tts audio generation).
- **Database Migrations:** `uv run alembic upgrade head` (or `uv run alembic revision --autogenerate -m "description"`).
- **Seed Database:** `uv run python -m admirable.presentation.cli.seed`

## Architectural Guidelines (Clean Architecture)

- **Clean Architecture 4 Layers with Inward Dependency Flow:**
  - `src/admirable/domain/`: Pure business entities, value objects, domain exceptions, and repository protocols. Zero third-party framework imports in domain.
  - `src/admirable/application/`: Application use cases, DTOs, and port interfaces (`FileStoragePort`, `TextToSpeechPort`, `TaskQueuePort`, `MailerPort`, `SessionStorePort`, `PasswordHasherPort`). Depends ONLY on `domain/` and standard library / Pydantic.
  - `src/admirable/infrastructure/`: SQLAlchemy models/repositories, Taskiq broker, edge-tts adapter, local file storage, bcrypt password hasher, Redis token store, Log/SMTP mailers.
  - `src/admirable/presentation/`: FastAPI web app, middleware (Session, CSRF, MethodOverride, ErrorHandler), Jinja2 templates, SEO builders, and CLI commands.
- **Frontend Architecture:**
  - Server-side rendered (SSR) with Jinja2 templates located in `src/admirable/presentation/web/templates/`.
  - Styling via Tailwind CSS CDN with Apple-inspired minimalism (`apple-black`, `apple-gray`, `apple-blue`, `apple-bg`).
  - Native Vanilla JavaScript for client-side interactions. No Node.js build step (no npm/vite).
- **Content Blocks Schema:** JSON array with objects typed as:
  - `paragraph`: `text_en`, `text_vi`, optional `heading_en`
  - `heading`: `text_en`
  - `quote`: `text_en`, `author`
- **Audio Generation:**
  - Handled asynchronously via Taskiq task `generate_audio_task` calling `EdgeTtsAdapter`.
  - State machine on entities/models: `audio_status` (`idle` → `processing` → `completed` | `failed` | `cancelled`), `audio_error`, `audio_path`.
- **Role Permissions:**
  - `superadmin`: Full access + User management (`/admin/users`).
  - `admin`: Content management only.

## Definition of Done (DoD)

1. Code adheres to Python 3.14 & Clean Architecture conventions with inward dependency flow.
2. Formatted and linted cleanly with `uv run ruff check .` and `uv run ruff format .` with 0 warnings.
3. Tested with `uv run pytest` with 100% pass rate (0 failures).
4. Architecture boundary tests pass (`uv run pytest tests/architecture/`).
5. Type checking passes with `uv run mypy src`.
