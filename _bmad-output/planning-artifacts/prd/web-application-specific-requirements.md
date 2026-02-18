# Web Application Specific Requirements

### Project-Type Overview

bmad-demo is a **multi-page application (MPA)** — server-rendered HTML pages served by FastAPI with Jinja2 templates. No JavaScript SPA framework. Minimal client-side JS limited to interactive elements (search, filters, form validation). The browser extension is a separate Chromium/Edge extension that communicates with the FastAPI backend via REST API.

### Browser Support

| Browser | MVP | Post-MVP |
|---------|-----|----------|
| Chromium (Chrome) | ✅ Supported | ✅ |
| Microsoft Edge | ✅ Supported | ✅ |
| Firefox | ❌ Not in MVP | ✅ Target |
| Safari | ❌ Not in MVP | ✅ Target |

- Target latest stable versions only — no legacy browser support
- Web app and browser extension both target Chromium/Edge for MVP

### Responsive Design

- **Desktop:** Primary design target — full-width layout for browsing and managing bookmarks
- **Tablet:** Should be usable — responsive layout, no dedicated tablet UX
- **Mobile:** Not a target for MVP — acceptable if it degrades gracefully

### Performance Targets

See [Non-Functional Requirements — Performance](#performance) for measurable targets.

### SEO Strategy

No SEO requirements for MVP. Public shared list pages are accessible via direct URL but not optimized for search engine indexing. Shared lists are private-by-obscurity (not discoverable, but viewable by anyone with the link).

### Accessibility

Basic accessibility — reasonable defaults:
- Semantic HTML elements (nav, main, article, section, button)
- Keyboard navigable (tab order, focus indicators)
- Readable text contrast
- Form labels and ARIA attributes where needed
- No specific WCAG conformance level targeted for MVP

### Implementation Considerations

- **Templating:** Jinja2 templates rendered server-side by FastAPI
- **Static assets:** Served directly by FastAPI (CSS, minimal JS)
- **API layer:** RESTful JSON API endpoints for browser extension communication
- **Database:** SQLite with SQLAlchemy ORM or raw SQL — single-file database
- **Authentication:** Simple session-based or token-based single-user auth
- **Public routes:** Shared list pages served without authentication check
