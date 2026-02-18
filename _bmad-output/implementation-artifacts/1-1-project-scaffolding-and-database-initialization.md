# Story 1.1: Project Scaffolding & Database Initialization

Status: ready-for-dev

## Story

As a **self-hoster**,
I want to clone the repository, install dependencies, and run the application so that it starts up successfully with an auto-initialized database,
So that I have a working application foundation ready for use.

## Acceptance Criteria

1. **Given** the user has cloned the repository and has Python 3.11+ installed, **When** they install dependencies via `pip install -r requirements.txt`, **Then** all required packages install successfully (FastAPI, SQLAlchemy, uvicorn, python-dotenv, passlib[bcrypt], Jinja2).

2. **Given** a `.env.example` file exists in the project root, **When** the user copies it to `.env`, **Then** the file contains documented configuration for `DATABASE_URL`, `SECRET_KEY`, `HOST`, and `PORT` with sensible defaults.

3. **Given** the application is started via `uvicorn app.main:app`, **When** no SQLite database file exists yet, **Then** the application creates the database file and initializes all tables via `Base.metadata.create_all()`.

4. **Given** the application is running, **When** the user navigates to the root URL, **Then** they see a functional page (redirect to setup page if no user exists, or redirect to login if user exists).

5. **Given** the project structure exists, **When** examining the directory layout, **Then** it follows the architecture specification: `app/` with `models/`, `routers/`, `services/`, `schemas/`, `templates/`, `static/` subdirectories, plus `extension/`, `tests/`, `requirements.txt`, `.env.example`, `.gitignore`.

6. **Given** the application is running, **When** attempting to access the SQLite database file via any web route, **Then** the file is not served or accessible (NFR10 — security).

## Tasks / Subtasks

- [ ] **Task 1: Create project directory structure** (AC: #5)
  - [ ] 1.1 Create `app/__init__.py`
  - [ ] 1.2 Create `app/models/__init__.py`
  - [ ] 1.3 Create `app/routers/__init__.py`
  - [ ] 1.4 Create `app/services/__init__.py`
  - [ ] 1.5 Create `app/schemas/__init__.py`
  - [ ] 1.6 Create `app/templates/` directory (with `base.html` placeholder)
  - [ ] 1.7 Create `app/static/css/` and `app/static/js/` directories
  - [ ] 1.8 Create `extension/` directory (empty, placeholder for Epic 6)
  - [ ] 1.9 Create `tests/__init__.py` and `tests/conftest.py`

- [ ] **Task 2: Create `requirements.txt`** (AC: #1)
  - [ ] 2.1 Add all dependencies with version constraints:
    - `fastapi`
    - `uvicorn[standard]`
    - `sqlalchemy`
    - `python-dotenv`
    - `passlib[bcrypt]`
    - `jinja2`
    - `python-multipart` (required by FastAPI for form handling)
    - `pytest` (dev dependency)
    - `httpx` (dev dependency — for FastAPI TestClient)

- [ ] **Task 3: Create `.env.example` and `app/config.py`** (AC: #2)
  - [ ] 3.1 Create `.env.example` with documented variables:
    ```
    # Database — path to SQLite file
    DATABASE_URL=sqlite:///./bmad_demo.db
    # Secret key for session management (change in production)
    SECRET_KEY=change-me-to-a-random-secret
    # Server bind
    HOST=127.0.0.1
    PORT=8000
    ```
  - [ ] 3.2 Create `app/config.py` — load settings from `.env` using `python-dotenv` and expose as module-level constants (`DATABASE_URL`, `SECRET_KEY`, `HOST`, `PORT`)

- [ ] **Task 4: Create `app/database.py`** (AC: #3)
  - [ ] 4.1 Create synchronous SQLAlchemy engine from `DATABASE_URL` with `connect_args={"check_same_thread": False}` (required for SQLite with FastAPI's threaded request handling)
  - [ ] 4.2 Create `SessionLocal` sessionmaker
  - [ ] 4.3 Create `Base` declarative base
  - [ ] 4.4 Create `init_db()` function that calls `Base.metadata.create_all(bind=engine)`

- [ ] **Task 5: Create placeholder models** (AC: #3)
  - [ ] 5.1 Create `app/models/user.py` with `User` model (id, username, hashed_password, api_token, created_at) — needed for first-run detection in Story 1.2
  - [ ] 5.2 Import all models in `app/models/__init__.py` so `create_all()` discovers them

- [ ] **Task 6: Create `app/dependencies.py`** (AC: #3, #4)
  - [ ] 6.1 Create `get_db()` generator that yields `SessionLocal()` and closes after request

- [ ] **Task 7: Create `app/main.py`** (AC: #3, #4, #6)
  - [ ] 7.1 Create FastAPI app instance
  - [ ] 7.2 Mount static files using absolute path: `StaticFiles(directory=Path(__file__).parent / "static")` mounted at `/static` — serves only from `app/static/`, preventing SQLite DB access. Use `from pathlib import Path`.
  - [ ] 7.3 Configure Jinja2 templates using absolute path: `Jinja2Templates(directory=Path(__file__).parent / "templates")`
  - [ ] 7.4 Call `init_db()` on startup using FastAPI `lifespan` context manager (NOT deprecated `@app.on_event`). Example: `@asynccontextmanager async def lifespan(app): init_db(); yield` then `app = FastAPI(lifespan=lifespan)`
  - [ ] 7.5 Add root route `/` that uses `Depends(get_db)` to check if any user exists — if no user, redirect to `/setup`; if user exists, redirect to `/login`. Return `RedirectResponse` with status 302.
  - [ ] 7.6 Configure `logging.basicConfig(level=logging.INFO)` at module level
  - [ ] 7.7 Include routers (`auth_router` from `app.routers.auth`)

- [ ] **Task 8: Create `app/routers/auth.py` with placeholder setup route** (AC: #4)
  - [ ] 8.1 Create `app/routers/auth.py` with a single `GET /setup` route that renders `setup.html` (placeholder for Story 1.2). This is the route that `/` redirects to when no user exists.

- [ ] **Task 9: Create minimal templates** (AC: #4)
  - [ ] 9.1 Create `app/templates/base.html` with Pico CSS CDN link: `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">`. Include `{% block page_title %}`, `{% block page_content %}` blocks. Wrap content in `<main class="container">`.
  - [ ] 9.2 Create `app/templates/setup.html` extending base — placeholder "Setup coming in Story 1.2"

- [ ] **Task 10: Create `.gitignore`** (AC: #5, #6)
  - [ ] 10.1 Standard Python `.gitignore` plus: `*.db`, `.env`, `__pycache__/`, `*.pyc`, `.pytest_cache/`

- [ ] **Task 11: Create initial tests** (AC: #1, #3, #4)
  - [ ] 11.1 Create `tests/conftest.py` with test DB fixture (in-memory SQLite or temp file)
  - [ ] 11.2 Create `tests/test_app.py`:
    - Test that app starts and root URL returns redirect (302)
    - Test that `init_db()` creates tables
    - Test that static files are served from `/static/`

## Dev Notes

### Architecture Constraints

- **Layer architecture**: Router → Service → Model. This story creates the skeleton for all layers but only implements the database and root redirect logic.
- **Sync SQLAlchemy only** — no async. Use `create_engine()` not `create_async_engine()`.
- **Single-user app** — the User model holds one row. First-run detection = `SELECT COUNT(*) FROM users == 0`.
- **No Alembic** — schema managed via `Base.metadata.create_all()` on every startup.
- **Use `logging.getLogger(__name__)`** in every module. Never `print()`.

### Security: SQLite File Protection (AC #6 / NFR10)

The SQLite database file (`bmad_demo.db`) is created in the project root. Static files are served ONLY from `app/static/` via `StaticFiles(directory="app/static/")`. This means the DB file is never in a served directory. Do NOT mount the project root as a static path.

### Scope Boundaries

This story creates the project skeleton and database init ONLY. Not included: login/logout (Story 2.1), credential setup form (Story 1.2), bookmark/interest/list models (Epic 3+), API routes (Epic 6). Only the `User` model is created (needed for first-run detection).

### Key Implementation Details

- **FastAPI form support** requires `python-multipart` — include in requirements.txt.
- **Pico CSS v2** — load via CDN: `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">`. No npm needed.
- **`uvicorn app.main:app`** is the run command — `app` object must be in `app/main.py`.
- **python-dotenv**: Use `load_dotenv()` at top of `config.py`, then `os.getenv()` for each variable.
- **Database URL format**: `sqlite:///./bmad_demo.db` (three slashes = relative path).

### Project Structure Notes

This story creates the **complete directory skeleton** matching the architecture spec. All `__init__.py` files should be empty (or simple imports). The structure must be:

```
bmad-demo/
├── requirements.txt
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── templates/
│   │   ├── base.html
│   │   └── setup.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── extension/          (empty placeholder)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_app.py
└── docs/
```

### References

- [Architecture: Project Structure](planning-artifacts/architecture/project-structure-boundaries.md#Complete-Project-Directory-Structure)
- [Architecture: Core Decisions — Data Architecture](planning-artifacts/architecture/core-architectural-decisions.md#Data-Architecture)
- [Architecture: Core Decisions — Infrastructure](planning-artifacts/architecture/core-architectural-decisions.md#Infrastructure-Decisions)
- [Architecture: Implementation Patterns](planning-artifacts/architecture/implementation-patterns-consistency-rules.md)
- [Architecture: Starter Template Evaluation](planning-artifacts/architecture/starter-template-evaluation.md)
- [PRD: Functional Requirements FR40, FR41](planning-artifacts/prd/functional-requirements.md)
- [PRD: Non-Functional Requirements NFR10](planning-artifacts/prd/non-functional-requirements.md)
- [Project Context](project-context.md)
- [Epics: Epic 1 — Story 1.1](planning-artifacts/epics.md#Story-1.1)

## Dev Agent Record

### Agent Model Used

<!-- To be filled by dev agent -->

### Debug Log References

### Completion Notes List

### File List

