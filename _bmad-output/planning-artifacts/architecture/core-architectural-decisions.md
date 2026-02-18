# Core Architectural Decisions

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
