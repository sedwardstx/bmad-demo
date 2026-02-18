# Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-solving MVP — deliver the smallest feature set that solves the core problem (saving, organizing, and retrieving bookmarks) and validates the sharing concept.

**Resource Requirements:** Solo developer. FastAPI + SQLite + Jinja2 templates + Chromium extension. No external services, no infrastructure dependencies.

### MVP Feature Set (Phase 1)

**Core User Journeys Supported:**
- Journey 1: Save a link via browser extension (happy path)
- Journey 2: Search and find a previously saved link
- Journey 3: Create and share a curated list
- Journey 4: Friend views shared list (public HTML page)
- Journey 5: Self-hoster clones and runs the app

**Must-Have Capabilities:**

| Capability | Rationale |
|-----------|----------|
| Single-user auth (login) | Protects the instance |
| Bookmark CRUD (URL, title, interest, subcategory, tags) | Core value proposition |
| Interest category & subcategory management | Hierarchical organization |
| Full-text search (title, URL) | Retrieval is the core problem |
| Filter by interest, subcategory, tag | Browsing and discovery |
| Browser extension (Chromium/Edge) | Fast capture = primary differentiator |
| Curated list creation & management | Sharing feature |
| Public shared list page (no auth) | Zero-friction recipient experience |
| Simple HTML front-end (Jinja2) | Clean, functional UI |

**Explicitly NOT in MVP:**
- Multi-user accounts
- Bookmark import
- Dead link detection
- Auto-metadata extraction
- Export (PDF/CSV/Markdown)
- Firefox/Safari extensions
- Mobile-optimized UI
- API for third-party integrations

### Post-MVP Features

**Phase 2 (Growth):**
- Multi-user support with optional accounts
- Browser bookmark import (Chrome/Edge exports)
- Link health monitoring (dead link detection)
- Auto-metadata extraction (description, favicon, preview image)
- Export curated lists (PDF, CSV, Markdown)

**Phase 3 (Expansion):**
- Firefox/Safari browser extensions
- Mobile-friendly responsive UI redesign
- RESTful API for third-party integrations
- Collaborative lists (friends contribute links)
- Smart suggestions / duplicate detection

### Risk Mitigation Strategy

**Technical Risks:**
- *SQLite scaling* — Low risk. SQLite handles 10,000+ rows easily. If scaling becomes an issue in the future, migrate to PostgreSQL. MVP doesn't need to solve this.
- *Browser extension complexity* — Medium risk. Extension APIs can be finicky. Mitigate by keeping the extension simple (popup form + API call) and testing early.

**Market Risks:**
- *Minimal* — This is a personal tool. No market validation needed. If it works for Steve, it works.

**Resource Risks:**
- *Solo developer* — Mitigate by keeping MVP scope tight. Every feature above is achievable by one person. No external dependencies or services to integrate.
