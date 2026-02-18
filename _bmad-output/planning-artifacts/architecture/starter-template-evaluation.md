# Starter Template Evaluation

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
