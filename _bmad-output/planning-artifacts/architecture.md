---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments: [prd.md, product-brief-bmad-demo-2026-02-18.md]
workflowType: 'architecture'
project_name: 'bmad-demo'
user_name: 'Steve'
date: '2026-02-18'
lastStep: 8
status: 'complete'
completedAt: '2026-02-18'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
41 FRs across 7 capability areas. The core architectural load falls on three areas: (1) Bookmark CRUD with hierarchical categorization (FR1–FR19), which defines the primary data model and most web UI routes; (2) Curated Shared Lists (FR20–FR27), which introduces a many-to-many relationship and a public-facing rendering path with no auth; and (3) Browser Extension (FR28–FR35), which requires a separate REST API surface and a distinct client codebase with its own build/packaging.

**Non-Functional Requirements:**
18 NFRs. The performance targets (sub-second page loads, sub-500ms search at 10k+ bookmarks) are easily achievable with SQLite + server-side rendering on localhost. Security requirements center on hashed credentials, session/token enforcement, non-guessable shared list URLs (UUID), and DB file isolation from web routes. Accessibility targets are basic semantic HTML + keyboard navigation — no WCAG conformance level specified. Reliability focuses on data integrity and graceful error handling.

**Scale & Complexity:**

- Primary domain: Full-stack web application + Chromium/Edge browser extension
- Complexity level: Low
- Estimated architectural components: 5–6 (web routes/controllers, template layer, data access layer, REST API for extension, browser extension, shared/public page renderer)

### Technical Constraints & Dependencies

- **SQLite** — Single-file database. No concurrent write scaling, but irrelevant for single-user. No external DB service to manage.
- **FastAPI + Jinja2** — Server-side rendering. No build toolchain for frontend. Static assets served directly by FastAPI.
- **Chromium/Edge extension** — Must conform to Manifest V3 extension APIs. Separate packaging and distribution from the web app.
- **Self-hosted** — No cloud services, no CDN, no managed infrastructure. Runs on localhost or a personal server.
- **Single-user** — No multi-tenant data isolation, no user management. Auth is a simple gate.
- **Minimal JavaScript** — Client-side JS limited to interactive elements (search, filters, form validation). No JS framework.

### Cross-Cutting Concerns Identified

- **Authentication boundary** — Every route must be classified as authenticated or public. Public routes: shared list pages, login page. Everything else requires valid session/token.
- **Input validation** — URL format validation, tag sanitization, category name constraints. Applies across web forms, API endpoints, and extension inputs.
- **Error handling** — Graceful handling of malformed URLs, invalid inputs, DB errors. Consistent user-facing error messages across web UI and extension.
- **Data access patterns** — All features touch the same SQLite database. Need a consistent data access layer (SQLAlchemy ORM or repository pattern) to avoid scattered raw SQL.
- **Extension API contract** — The REST API endpoints used by the browser extension must be versioned or at least stable. Changes to the API break the extension.

## Starter Template Evaluation

### Primary Technology Domain

Full-stack web application (FastAPI + SQLite + Jinja2 MPA) + Chromium/Edge browser extension, based on project requirements analysis.

### Starter Options Considered

**Option A: tiangolo/full-stack-fastapi-template**
The official FastAPI full-stack generator. Includes PostgreSQL, Docker, Celery, React frontend, Traefik, email-based auth, Alembic migrations. **Verdict: Too heavy.** Designed for production SaaS with multi-user, containerized deployments. 90% of scaffolding would need removal.

**Option B: `fastapi` CLI (`fastapi create`)**
FastAPI's built-in scaffolding. Creates a minimal package-style layout for API-only services. **Verdict: Too minimal and wrong direction.** No Jinja2 templating, no static asset serving, no browser extension structure.

**Option C: Custom lean structure**
A project-specific structure tailored to bmad-demo's exact needs. No unused scaffolding, no wrong patterns to undo.

### Selected Starter: Custom Lean Structure

**Rationale:**
This project has a specific, well-defined tech stack that doesn't match any popular FastAPI starter template. The available starters either include too much (PostgreSQL, Docker, React) or too little (no templating, no static assets). A custom structure gives us exactly what we need — nothing more.

**Proposed Project Structure:**

```
bmad-demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py             # App configuration
│   ├── database.py           # SQLAlchemy engine + session
│   ├── models/               # SQLAlchemy ORM models
│   ├── routers/              # FastAPI route handlers
│   ├── schemas/              # Pydantic request/response models
│   ├── services/             # Business logic layer
│   ├── templates/            # Jinja2 HTML templates
│   └── static/               # CSS, minimal JS
├── extension/                # Chromium/Edge browser extension
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   └── icons/
├── tests/
│   ├── conftest.py
│   └── ...
├── requirements.txt
└── README.md
```

**Architectural Decisions Provided by Starter:**

| Decision | Choice |
|----------|--------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| ORM | SQLAlchemy (sync, suitable for SQLite) |
| Database | SQLite (single file) |
| Templating | Jinja2 (FastAPI built-in support) |
| Package manager | pip + requirements.txt |
| Testing | pytest |
| Linting/Formatting | None (MVP) |
| Frontend JS framework | None — vanilla JS for interactive elements |
| Extension | Chromium/Edge Manifest V3 |
| Project generator | None — custom structure |

**Note:** Project initialization using this structure should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Data modeling approach (SQLAlchemy sync, `create_all()`)
- Authentication method (session/cookie + API token for extension)
- API design (RESTful JSON under `/api/v1/`)
- Shared list URL scheme (UUID4)

**Important Decisions (Shape Architecture):**
- CSS framework (classless — Pico CSS or Simple.css)
- CORS policy (FastAPI CORSMiddleware for extension)
- Error handling strategy (JSON for API, HTML for web)
- Environment configuration (`.env` + python-dotenv)

**Deferred Decisions (Post-MVP):**
- Database migration tooling (Alembic — add when schema stabilizes)
- Rate limiting (not needed for single-user)
- Monitoring/APM (not needed for self-hosted MVP)

### Data Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ORM | SQLAlchemy (sync) | SQLite doesn't benefit from async; sync is simpler with no concurrency needs |
| Database | SQLite (single file) | Self-hosted, single-user — no external DB service needed |
| Schema management | `create_all()` on startup | MVP simplicity; Alembic deferred until schema stabilizes |
| Data validation | Pydantic models | FastAPI native; validates request/response data automatically |

### Authentication & Security

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Web app auth | Session/cookie-based | Works natively with Jinja2 MPA — browser handles cookies automatically on page loads and form submissions |
| Extension auth | API token (stored in DB/config) | Extension stores token and sends via header; avoids JWT complexity |
| Password hashing | `passlib[bcrypt]` | Battle-tested, one-line hash/verify |
| CORS | FastAPI `CORSMiddleware` | Configured to allow the browser extension origin (`chrome-extension://...`) |
| Shared list URLs | UUID4 slug (`/shared/{uuid}`) | Non-guessable, no auth required, satisfies NFR9 |

### API & Communication Patterns

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Extension API | RESTful JSON under `/api/v1/` prefix | Clean separation from web page routes; stable contract for extension |
| Key endpoints | `GET /api/v1/categories`, `POST /api/v1/bookmarks`, `POST /api/v1/auth/token` | Minimum viable API surface for extension functionality |
| Error handling (API) | JSON error responses with status codes | Extension and API clients parse structured errors |
| Error handling (Web) | HTML error pages via Jinja2 templates | User-facing error display consistent with MPA pattern |
| Request validation | Pydantic schemas | FastAPI native validation with automatic 422 responses |

### Frontend Architecture

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CSS framework | Classless CSS (Pico CSS or Simple.css) | Instant decent styling with semantic HTML; no build step; aligns with accessibility NFRs |
| JavaScript | Vanilla JS — no framework | Minimal client-side interactivity (search, filters, form validation) |
| Templating | Jinja2 server-rendered | MPA pattern — all pages rendered server-side |
| Static assets | Served by FastAPI directly | No CDN or separate static server needed for self-hosted |

### Infrastructure & Deployment

| Decision | Choice | Rationale |
|----------|--------|-----------|
| App server | Uvicorn (direct) | Single-user; no need for Gunicorn process manager |
| Run command | `uvicorn app.main:app` | Simple entry point |
| Environment config | `.env` file + `python-dotenv` | Store DB path, secret key, API token, host/port |
| Logging | Python built-in `logging` module | FastAPI logs requests; add app-level logging for errors and key actions |
| Containerization | None (MVP) | Clone and run directly; Docker deferred to post-MVP |

### Decision Impact Analysis

**Implementation Sequence:**
1. Project scaffolding + DB setup (`create_all()`, SQLAlchemy models)
2. Auth (session/cookie login, API token generation)
3. Bookmark CRUD (web routes + Jinja2 templates)
4. Search & filtering
5. Interest/subcategory management
6. Extension API endpoints (`/api/v1/`)
7. Browser extension (Manifest V3)
8. Curated shared lists + public pages

**Cross-Component Dependencies:**
- Auth must be implemented before any protected routes (web or API)
- Data models must be defined before any CRUD operations
- `/api/v1/` endpoints and web routes share the same service/data layer — changes to business logic affect both
- Extension depends on API endpoints being stable; extension development should start after API contract is defined
- Shared list public routes bypass auth middleware — routing must be configured to exclude these paths

## Implementation Patterns & Consistency Rules

### Naming Patterns

**Database Naming Conventions:**
- Tables: snake_case, plural — `bookmarks`, `interests`, `curated_lists`
- Columns: snake_case — `created_at`, `interest_id`, `is_public`
- Foreign keys: `{referenced_table_singular}_id` — `interest_id`, `curated_list_id`
- Indexes: `ix_{table}_{column}` — `ix_bookmarks_title`

**API Naming Conventions:**
- Endpoints: lowercase, plural nouns — `/api/v1/bookmarks`, `/api/v1/categories`
- Route parameters: `{id}` style (FastAPI default)
- Query parameters: snake_case — `?interest_id=3&search_term=sourdough`

**Python Code Naming Conventions:**
- Files/modules: snake_case — `bookmark_service.py`, `auth_router.py`
- Classes: PascalCase — `Bookmark`, `CuratedList`
- Functions/variables: snake_case — `get_bookmark_by_id`, `tag_list`
- Constants: UPPER_SNAKE — `DATABASE_URL`, `SESSION_SECRET`

**Jinja2 Template Naming:**
- Files: snake_case — `bookmark_list.html`, `shared_list.html`
- Template blocks: snake_case — `{% block page_content %}`, `{% block page_title %}`

### Structure Patterns

**Project Organization:**
- Organized by layer (not by feature) — `models/`, `routers/`, `services/`, `schemas/` at top level inside `app/`
- Each layer gets one file per domain entity when it grows beyond ~100 lines (e.g., `routers/bookmarks.py`, `routers/auth.py`)
- Start with single files per layer; split when needed

**Test Organization:**
- Separate `tests/` directory mirroring `app/` structure — `tests/test_bookmarks.py`, `tests/test_auth.py`
- Test files prefixed with `test_`
- Fixtures in `tests/conftest.py`

**Template Organization:**
- Flat in `app/templates/` with a base layout — `base.html`, `login.html`, `bookmark_list.html`, `shared_list.html`
- Partials in `app/templates/partials/` if needed — `_bookmark_card.html` (underscore prefix for partials)

**Static Asset Organization:**
- `app/static/css/` — `style.css` (single file for MVP)
- `app/static/js/` — `app.js` (single file for MVP)

### Format Patterns

**API Response Formats:**
- Direct response — no wrapper. FastAPI returns Pydantic models directly as JSON.
- Success: `200` with data, `201` for created
- Errors: `{"detail": "Human-readable message"}` (FastAPI default)
- Validation errors: `422` with FastAPI's automatic Pydantic error format

**JSON Field Naming:**
- snake_case in API responses (Python convention; Pydantic outputs snake_case by default)

**Date/Time Formats:**
- Stored as UTC in SQLite (`datetime` columns)
- Returned as ISO 8601 strings in API responses (`2026-02-18T14:30:00Z`)
- Displayed in local format in Jinja2 templates via a template filter

### Process Patterns

**Error Handling:**
- Web routes: catch exceptions → render error template with message
- API routes: raise `HTTPException` with appropriate status code and `detail` message
- Database errors: catch at service layer, raise application-level exceptions
- Never expose stack traces to users

**Authentication Flow:**
- Web: check session cookie via FastAPI dependency → redirect to `/login` if missing
- API: check `Authorization: Bearer {token}` header via FastAPI dependency → return `401` JSON if invalid
- Both use FastAPI `Depends()` for clean injection

**Validation Strategy:**
- Pydantic schemas validate all incoming data (web forms via Form fields, API via JSON body)
- Service layer validates business rules (e.g., duplicate URL check, category exists)
- Database constraints as last line of defense (unique, not null)

**Logging:**
- Use `logging.getLogger(__name__)` in each module
- Levels: `INFO` for key actions (bookmark saved, list shared), `WARNING` for recoverable issues, `ERROR` for failures
- No `print()` statements

### Enforcement Guidelines

**All AI Agents MUST:**
- Follow snake_case for all Python code, database columns, API parameters, and JSON fields
- Use PascalCase only for Python class names
- Place tests in `tests/` directory with `test_` prefix
- Use FastAPI `Depends()` for auth checks — never inline auth logic in route handlers
- Return `HTTPException` for API errors, render templates for web errors
- Use `logging` module — never `print()`
- Validate input via Pydantic schemas before passing to service layer

## Project Structure & Boundaries

### Complete Project Directory Structure

```
bmad-demo/
├── README.md
├── requirements.txt
├── .env.example
├── .env
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app creation, middleware, startup events
│   ├── config.py                  # Settings loaded from .env (python-dotenv)
│   ├── database.py                # SQLAlchemy engine, SessionLocal, Base, create_all()
│   ├── dependencies.py            # FastAPI Depends: get_db, get_current_user, require_api_token
│   ├── exceptions.py              # Custom exception classes + exception handlers
│   ├── models/
│   │   ├── __init__.py
│   │   ├── bookmark.py            # Bookmark, BookmarkTag (many-to-many)
│   │   ├── interest.py            # Interest, Subcategory
│   │   ├── curated_list.py        # CuratedList, CuratedListItem (many-to-many)
│   │   ├── user.py                # User (single-user, stores hashed password + API token)
│   │   └── tag.py                 # Tag
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── bookmark.py            # BookmarkCreate, BookmarkUpdate, BookmarkResponse
│   │   ├── interest.py            # InterestCreate, SubcategoryCreate, etc.
│   │   ├── curated_list.py        # CuratedListCreate, CuratedListResponse, etc.
│   │   ├── auth.py                # LoginForm, TokenResponse
│   │   └── tag.py                 # TagCreate, TagResponse
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                # GET /login, POST /login, POST /logout
│   │   ├── bookmarks.py           # CRUD web routes for bookmarks
│   │   ├── interests.py           # CRUD web routes for interests/subcategories
│   │   ├── curated_lists.py       # CRUD web routes for curated lists
│   │   ├── shared.py              # GET /shared/{uuid} (public, no auth)
│   │   └── api/
│   │       ├── __init__.py
│   │       └── v1/
│   │           ├── __init__.py
│   │           ├── bookmarks.py   # POST /api/v1/bookmarks
│   │           ├── categories.py  # GET /api/v1/categories (interests + subcategories)
│   │           └── auth.py        # POST /api/v1/auth/token
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bookmark_service.py    # Bookmark business logic (CRUD, search, filtering)
│   │   ├── interest_service.py    # Interest/subcategory management
│   │   ├── curated_list_service.py # Curated list management + UUID generation
│   │   ├── auth_service.py        # Login, password hashing, session/token management
│   │   └── tag_service.py         # Tag parsing, creation, association
│   ├── templates/
│   │   ├── base.html              # Base layout (nav, head, footer, block structure)
│   │   ├── login.html             # Login form
│   │   ├── bookmark_list.html     # Main bookmark browsing/filtering page
│   │   ├── bookmark_form.html     # Add/edit bookmark form
│   │   ├── interest_list.html     # Manage interests and subcategories
│   │   ├── curated_list_list.html # List of curated lists
│   │   ├── curated_list_edit.html # Edit curated list (add/remove bookmarks)
│   │   ├── shared_list.html       # Public shared list page (no auth)
│   │   ├── error.html             # Error display page
│   │   ├── setup.html             # First-run credential setup
│   │   └── partials/
│   │       ├── _bookmark_card.html    # Single bookmark display component
│   │       ├── _search_bar.html       # Search + filter controls
│   │       └── _pagination.html       # Pagination controls (if needed)
│   └── static/
│       ├── css/
│       │   └── style.css          # Custom styles (on top of classless CSS framework)
│       └── js/
│           └── app.js             # Vanilla JS for search, filters, form interactions
├── extension/
│   ├── manifest.json              # Manifest V3 config
│   ├── popup.html                 # Extension popup UI
│   ├── popup.js                   # Popup logic (fetch categories, save bookmark)
│   ├── popup.css                  # Popup styling
│   ├── options.html               # Extension settings (server URL, API token)
│   ├── options.js                 # Settings logic
│   └── icons/
│       ├── icon-16.png
│       ├── icon-48.png
│       └── icon-128.png
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest fixtures (test DB, test client, auth helpers)
│   ├── test_bookmarks.py          # Bookmark CRUD + search tests
│   ├── test_interests.py          # Interest/subcategory management tests
│   ├── test_curated_lists.py      # Curated list + sharing tests
│   ├── test_auth.py               # Login, logout, session, API token tests
│   ├── test_shared.py             # Public shared list access tests
│   ├── test_api_bookmarks.py      # Extension API bookmark tests
│   ├── test_api_categories.py     # Extension API category tests
│   └── test_api_auth.py           # Extension API token auth tests
└── docs/
    └── (project documentation)
```

### Architectural Boundaries

**API Boundaries:**
- Web routes (`/login`, `/bookmarks`, `/interests`, `/lists`, `/shared/{uuid}`) → serve Jinja2 HTML
- Extension API routes (`/api/v1/*`) → return JSON
- Public routes (`/shared/{uuid}`, `/login`, static assets) → no auth required
- All other routes → require valid session cookie (web) or API token (API)

**Service Boundaries:**
- Routers call services — never access the database directly
- Services contain business logic and call SQLAlchemy models/queries
- Services return domain objects; routers decide the response format (HTML or JSON)
- Services raise custom exceptions; routers handle them appropriately per channel

**Data Boundaries:**
- All database access goes through SQLAlchemy session (injected via `Depends(get_db)`)
- Models define schema; schemas (Pydantic) define API contracts
- No raw SQL — use SQLAlchemy query API

### Requirements to Structure Mapping

| FR Category | Router(s) | Service | Model(s) | Templates |
|-------------|-----------|---------|----------|-----------|
| Bookmark Management (FR1–FR10) | `routers/bookmarks.py` | `bookmark_service.py` | `bookmark.py`, `tag.py` | `bookmark_list.html`, `bookmark_form.html` |
| Search & Discovery (FR11–FR13) | `routers/bookmarks.py` | `bookmark_service.py` | `bookmark.py` | `bookmark_list.html`, `_search_bar.html` |
| Interest Management (FR14–FR19) | `routers/interests.py` | `interest_service.py` | `interest.py` | `interest_list.html` |
| Curated Lists (FR20–FR27) | `routers/curated_lists.py`, `routers/shared.py` | `curated_list_service.py` | `curated_list.py` | `curated_list_list.html`, `curated_list_edit.html`, `shared_list.html` |
| Browser Extension (FR28–FR35) | `routers/api/v1/bookmarks.py`, `routers/api/v1/categories.py` | `bookmark_service.py`, `interest_service.py` | (shared) | N/A (extension UI) |
| Auth & Security (FR36–FR39) | `routers/auth.py`, `routers/api/v1/auth.py` | `auth_service.py` | `user.py` | `login.html` |
| Setup & Config (FR40–FR41) | `routers/auth.py` | `auth_service.py` | `user.py` | `setup.html` |

### Data Flow

```
Browser Extension                    Web Browser
     │                                    │
     ▼                                    ▼
/api/v1/* (JSON)                  Web Routes (HTML)
     │                                    │
     └──────────┐          ┌──────────────┘
                ▼          ▼
            Service Layer
            (business logic)
                  │
                  ▼
          SQLAlchemy ORM
                  │
                  ▼
            SQLite File
```

**Public access path (shared lists):**
```
Anyone with URL → GET /shared/{uuid} → curated_list_service → SQLAlchemy → SQLite
                                     → render shared_list.html (no auth check)
```

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
All technology choices are fully compatible. FastAPI natively supports Jinja2 templating, static file serving, Pydantic validation, and CORSMiddleware. SQLAlchemy sync works with SQLite out of the box. passlib[bcrypt], python-dotenv, and uvicorn operate independently of each other. Manifest V3 extension communicates via standard HTTP to `/api/v1/`. Classless CSS framework requires zero build tooling. No conflicts found.

**Pattern Consistency:**
Naming patterns (snake_case for Python code, database, API; PascalCase for classes) are standard Python convention and align with FastAPI/Pydantic defaults. Template naming follows the same snake_case convention. All patterns are internally consistent.

**Structure Alignment:**
The layer-based project structure (routers → services → models) maps directly to the service boundary decisions. The `routers/api/v1/` subdirectory cleanly separates extension API from web routes. Test structure mirrors app structure.

### Requirements Coverage Validation ✅

**Functional Requirements (41/41 covered):**

| FR Range | Covered By | Status |
|----------|-----------|--------|
| FR1–FR10 (Bookmark CRUD) | `routers/bookmarks.py` → `bookmark_service.py` → `bookmark.py` | ✅ |
| FR11–FR13 (Search) | `bookmark_service.py` search methods + `_search_bar.html` | ✅ |
| FR14–FR19 (Interests) | `routers/interests.py` → `interest_service.py` → `interest.py` | ✅ |
| FR20–FR27 (Curated Lists) | `routers/curated_lists.py`, `routers/shared.py` → `curated_list_service.py` | ✅ |
| FR28–FR35 (Extension) | `routers/api/v1/*` + `extension/` directory | ✅ |
| FR36–FR39 (Auth) | `routers/auth.py`, `dependencies.py` → `auth_service.py` | ✅ |
| FR40–FR41 (Setup) | `routers/auth.py` → `auth_service.py`, `database.py` create_all() | ✅ |

**Non-Functional Requirements (18/18 covered):**

| NFR | Architectural Support | Status |
|-----|----------------------|--------|
| NFR1–NFR6 (Performance) | SQLite + server-rendered pages on localhost — sub-second trivially achievable. SQL LIKE queries for search at 10k rows. | ✅ |
| NFR7–NFR11 (Security) | passlib/bcrypt for hashing, session cookies + API token via Depends(), UUID4 for shared URLs, static file config excludes DB file, extension CORS config | ✅ |
| NFR12–NFR15 (Accessibility) | Semantic HTML via Jinja2 templates + classless CSS framework, form labels, keyboard nav | ✅ |
| NFR16–NFR18 (Reliability) | SQLite file persistence, Pydantic validation + custom exceptions for graceful error handling, exception handlers for DB errors | ✅ |

### Implementation Readiness Validation ✅

**Decision Completeness:**
All critical decisions are documented with specific technology choices. No ambiguous "TBD" items remain. Implementation patterns cover naming, structure, formats, error handling, auth flow, validation, and logging.

**Structure Completeness:**
Every file and directory is listed with a description of its purpose. Every FR maps to a specific router, service, model, and template file.

**Pattern Completeness:**
All potential AI agent conflict points are addressed: naming (database, API, code, templates), structure (project organization, tests, templates, static assets), formats (API responses, JSON fields, dates), and processes (error handling, auth, validation, logging).

### Gap Analysis Results

**Critical Gaps:** None.

**Minor Implementation Notes:**
- **Search (FR11):** Use SQL `LIKE` for MVP search against title and URL columns. Sufficient for 10k bookmarks on SQLite. FTS5 deferred to post-MVP if needed.

### Architecture Completeness Checklist

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed (low)
- [x] Technical constraints identified (SQLite, self-hosted, single-user)
- [x] Cross-cutting concerns mapped (auth boundary, validation, error handling, data access, API contract)
- [x] Critical decisions documented (auth, data, API, CSS, infrastructure)
- [x] Technology stack fully specified (FastAPI, SQLAlchemy, SQLite, Jinja2, Pydantic, passlib, python-dotenv, uvicorn)
- [x] Naming conventions established (snake_case, PascalCase for classes)
- [x] Structure patterns defined (layer-based, tests/ mirroring app/)
- [x] Process patterns documented (error handling, auth flow, validation, logging)
- [x] Complete directory structure defined (all files listed)
- [x] Component boundaries established (router → service → model)
- [x] Requirements to structure mapping complete (41 FRs → specific files)

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High — low-complexity project with well-understood tech stack and clear boundaries.

**Key Strengths:**
- Simple, well-defined service boundaries — no ambiguity about where code goes
- Clean separation of web and API channels sharing the same service layer
- Every FR maps to a specific file — agents know exactly where to implement
- Standard Python/FastAPI patterns — no exotic choices that could confuse agents

**Areas for Future Enhancement:**
- Alembic migrations when schema stabilizes
- SQLite FTS5 if LIKE search becomes insufficient
- Docker containerization for easier deployment
- Rate limiting if exposed beyond localhost

