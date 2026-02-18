# Project Structure & Boundaries

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
