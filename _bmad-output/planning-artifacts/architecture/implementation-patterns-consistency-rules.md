# Implementation Patterns & Consistency Rules

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
