# Project Context Analysis

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
