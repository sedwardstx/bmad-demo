---
project_name: 'bmad-demo'
user_name: 'Steve'
date: '2026-02-18'
sections_completed: ['technology_stack', 'architecture_rules', 'python_fastapi_rules', 'database_rules', 'api_rules', 'frontend_rules', 'testing_rules', 'search_rules', 'critical_rules']
status: 'complete'
rule_count: 42
optimized_for_llm: true
---

# Project Context for AI Agents

_Critical rules and patterns for implementing bmad-demo. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | latest stable | Web framework + API |
| SQLAlchemy | latest stable (sync) | ORM |
| SQLite | built-in | Database (single file) |
| Jinja2 | FastAPI built-in | Server-side templates |
| Pydantic | FastAPI built-in | Validation + schemas |
| passlib[bcrypt] | latest | Password hashing |
| python-dotenv | latest | Environment config |
| uvicorn | latest | ASGI server |
| pytest | latest | Testing |
| Pico CSS or Simple.css | latest | Classless CSS framework |

**Browser Extension:** Chromium/Edge Manifest V3 (vanilla JS)
**No linting/formatting tools.** No build toolchain. No JS framework.

---

## Critical Implementation Rules

### Architecture Rules

- **Layer architecture is mandatory:** Router → Service → Model. Routers NEVER access the database directly.
- **Services return domain objects.** Routers decide the format (HTML template or JSON response).
- **Two auth mechanisms coexist:** Session/cookie for web app, `Authorization: Bearer {token}` for extension API. Both injected via `Depends()`.
- **Public routes bypass auth:** `/shared/{uuid}`, `/login`, static assets. Everything else requires authentication.
- **Shared list URLs use UUID4** — non-guessable, no auth check.
- **Project organized by layer** (not feature): `models/`, `routers/`, `services/`, `schemas/` inside `app/`.

### Python/FastAPI Rules

- **All naming is snake_case** except class names (PascalCase) and constants (UPPER_SNAKE).
- **Use `Depends()` for all cross-cutting concerns** — DB sessions, auth checks. Never inline auth logic in route handlers.
- **Use `logging.getLogger(__name__)`** in every module. Never use `print()`.
- **Pydantic schemas validate all input** — web forms via Form fields, API via JSON body.
- **Service layer validates business rules** (duplicate URL check, category exists). Database constraints are last line of defense.
- **API errors:** Raise `HTTPException` with status code + `detail` message.
- **Web errors:** Catch exceptions, render `error.html` template. Never expose stack traces.
- **Config via `.env`** loaded with python-dotenv. Stores: DB path, secret key, API token, host, port.
- **Run command:** `uvicorn app.main:app`

### Database Rules

- **Tables:** snake_case, plural — `bookmarks`, `interests`, `curated_lists`
- **Columns:** snake_case — `created_at`, `interest_id`
- **Foreign keys:** `{referenced_table_singular}_id` — e.g., `interest_id`, `curated_list_id`
- **Indexes:** `ix_{table}_{column}` — e.g., `ix_bookmarks_title`
- **Schema init:** `Base.metadata.create_all()` on startup. No Alembic for MVP.
- **No raw SQL.** Use SQLAlchemy query API exclusively.
- **Dates stored as UTC.** ISO 8601 in API responses. Local format in templates via filter.

### API Rules

- **Extension API lives under `/api/v1/` prefix** — separate from web routes.
- **Endpoints:** lowercase, plural nouns — `/api/v1/bookmarks`, `/api/v1/categories`
- **Query params:** snake_case — `?interest_id=3&search_term=sourdough`
- **JSON fields:** snake_case (Pydantic default).
- **Responses:** Direct Pydantic model output, no wrapper. `200` success, `201` created, `422` validation error.
- **Error format:** `{"detail": "Human-readable message"}` (FastAPI default).

### Frontend Rules

- **Jinja2 templates are server-rendered.** No SPA, no frontend framework.
- **Template files:** snake_case — `bookmark_list.html`
- **Partials prefixed with underscore** — `_bookmark_card.html` in `partials/` subfolder.
- **Template blocks:** snake_case — `{% block page_content %}`, `{% block page_title %}`
- **Classless CSS framework** (Pico or Simple.css) + one custom `style.css`.
- **Vanilla JS only** — one `app.js` for search, filters, form interactions.

### Testing Rules

- **Tests in `tests/` directory** with `test_` prefix — `test_bookmarks.py`, `test_auth.py`
- **Fixtures in `conftest.py`** — test DB, test client, auth helpers.
- **Separate test files for web and API** — `test_bookmarks.py` vs `test_api_bookmarks.py`
- **Framework:** pytest only.

### Search Implementation

- **Use SQL `LIKE` for MVP search** against title and URL columns. No FTS5.

### Critical Don't-Miss Rules

- **Auth must be implemented before any protected route.**
- **Data models must be defined before any CRUD operations.**
- **Extension API must be stable before extension development starts.**
- **Web routes and `/api/v1/` share the same service layer** — business logic changes affect both channels.
- **CORS must allow `chrome-extension://...` origin** via FastAPI `CORSMiddleware`.
- **First-run setup flow:** App detects no user exists → shows setup page → creates credentials.
- **Database file must NOT be accessible via web routes.**

---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option
- Refer to architecture docs at `_bmad-output/planning-artifacts/architecture/` for detailed decisions

**For Humans:**
- Keep this file lean and focused on agent needs
- Update when technology stack or patterns change
- Remove rules that become obvious over time

Last Updated: 2026-02-18
