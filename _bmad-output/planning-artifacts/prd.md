---
stepsCompleted: [step-01-init, step-02-discovery, step-02b-vision, step-02c-executive-summary, step-03-success, step-04-journeys, step-05-domain, step-06-innovation, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish, step-12-complete]
inputDocuments: [product-brief-bmad-demo-2026-02-18.md]
workflowType: 'prd'
briefCount: 1
researchCount: 0
brainstormingCount: 0
projectDocsCount: 0
classification:
  projectType: web_app
  domain: general
  complexity: low
  projectContext: greenfield
  notes: "Dual-nature product (private management + public content display) with browser extension as separate deliverable"
---

# Product Requirements Document - bmad-demo

**Author:** Steve
**Date:** 2026-02-18

## Executive Summary

bmad-demo is a self-hosted personal bookmark management tool that replaces chaotic browser bookmarks with fast capture, structured organization, and frictionless sharing. Built on FastAPI + SQLite with a simple HTML front-end and a Chromium/Edge browser extension, it targets anyone with diverse interests who saves web content for later reference — and consistently fails to find it again.

The core problem: browser bookmarks were designed for navigation shortcuts, not knowledge management. They auto-generate cryptic titles, offer no tagging, and bury links in flat folder hierarchies that become unsearchable graveyards. bmad-demo solves this with a purpose-built UX for saving, categorizing, and retrieving links — plus the ability to curate and share link collections as clean public HTML pages requiring zero setup from recipients.

Single-user, self-hosted, no subscriptions, no vendor lock-in. Clone it, run it, own your data.

### What Makes This Special

Three capabilities that no single existing tool combines well:

1. **Speed of capture** — Browser extension auto-fills the page title, lets you pick an interest category and add tags, and saves in under 5 seconds without leaving the page
2. **Hierarchical organization with dual tagging** — Interest areas with optional subcategories provide structure; freeform tags provide flexibility. Both are searchable and filterable.
3. **Zero-friction shareable lists** — Curate a collection, generate a public URL, send it to a friend. They click and see a clean HTML page. No sign-up, no install, no app required.

The core insight: saving a link "for later" is a different activity than navigating to a favorite site. It deserves its own tool — one built around retrieval, not repetition.

## Project Classification

| Attribute | Value |
|-----------|-------|
| **Project Type** | Web application + Chromium/Edge browser extension |
| **Domain** | General (personal productivity) |
| **Complexity** | Low |
| **Project Context** | Greenfield |
| **Tech Stack** | FastAPI, SQLite, HTML front-end |
| **Auth Model** | Single-user login |
| **Deployment** | Self-hosted |

## Success Criteria

### User Success

- **Fast capture:** Saving a bookmark via the browser extension takes < 5 seconds from click to save
- **Instant retrieval:** Any previously saved link can be found within 10 seconds using search, tag filter, or interest category browsing
- **Effortless sharing:** Creating a curated list and generating a shareable URL takes < 2 minutes
- **Replaces bookmarks:** The tool becomes the user's default "save for later" action, replacing browser bookmarks entirely
- **Zero-friction recipients:** Shared list viewers see a clean HTML page with no sign-up, no install, and no confusion

### Business Success

N/A — This is a personal/open-source project. Success is measured by personal utility: the tool is functional, used regularly, and solves the bookmark chaos problem.

### Technical Success

- **Performance:** App handles 10,000+ bookmarks without perceptible slowdown on search or browsing
- **Reliability:** SQLite data persists reliably; no data loss under normal operation
- **Fast page loads:** Web UI pages load in < 1 second on localhost
- **Easy setup:** A new self-hoster can go from clone to first saved bookmark in under 10 minutes
- **Extension stability:** Browser extension works reliably on Chromium and Edge without errors or crashes

### Measurable Outcomes

| Outcome | Target | How to Measure |
|---------|--------|----------------|
| Save a bookmark | < 5 seconds | Extension click → save confirmation |
| Find a saved link | < 10 seconds | Open app → locate target link |
| Create a shared list | < 2 minutes | Select links → generate public URL |
| Self-hoster setup | < 10 minutes | Clone repo → first bookmark saved |
| Bookmark capacity | 10,000+ links | No perceptible slowdown in search/browse |
| Page load time | < 1 second | Localhost page render |

## Product Scope

See [Project Scoping & Phased Development](#project-scoping--phased-development) for the complete MVP feature set, growth roadmap, and risk mitigation strategy.

## User Journeys

### Journey 1: Steve Saves a Link (Primary User — Happy Path)

Steve is watching a YouTube video about building a custom mechanical keyboard. Halfway through, the creator links to a parts list on a niche supplier site. Steve knows he'll want this later. He clicks the bmad-demo extension icon in his browser toolbar. The popup appears pre-filled with the page title. He picks "Mechanical Keyboards" under his "Hardware" interest, types "parts, build-guide" as tags, and hits Save. Three seconds. Done. He goes back to the video.

Two weeks later, Steve's ready to order parts. He opens bmad-demo, clicks "Hardware" → "Mechanical Keyboards" and there it is — the parts list, clearly titled, right where he expected it. He clicks through and starts shopping.

### Journey 2: Steve Can't Remember What He Saved (Primary User — Search/Recovery)

Steve remembers saving an article about sourdough starter maintenance but can't remember the title, the site, or which interest he filed it under. He opens bmad-demo and types "sourdough" in the search bar. Three results appear — one is the article, saved six months ago with the tag "baking." He clicks it, the link works, and he's back on track.

### Journey 3: Steve Shares a Curated List (Primary User — Sharing)

Steve's friend asks him for good resources on getting started with 3D printing. Steve opens bmad-demo, creates a new curated list called "3D Printing Starter Guide," browses his "3D Printing" interest, and checks off 8 links — beginner tutorials, filament guides, and a printer comparison review. He clicks "Generate Link," copies the public URL, and pastes it into Discord. Done in under 2 minutes.

### Journey 4: Friend Views a Shared List (Secondary User — Recipient)

Steve's friend clicks the Discord link. A clean HTML page loads in their browser — no login prompt, no pop-ups, no app to install. The page shows "3D Printing Starter Guide — curated by Steve" with 8 links, each with a title and brief description. They scroll through, click a couple that look interesting, and bookmark the page itself for later. Total friction: zero.

### Journey 5: A Developer Sets Up Their Own Instance (Secondary User — Self-Hoster)

A developer sees bmad-demo mentioned on Reddit. They click through to the GitHub repo, read the README, and clone it. They run `pip install -r requirements.txt`, then `python main.py`. The app starts on localhost:8000. They open it, set up their login credentials, create their first interest category ("Programming"), and save their first bookmark via the web form. Total time from clone to first bookmark: 7 minutes. Next, they install the browser extension and start capturing links on the fly.

### Journey Requirements Summary

| Journey | Capabilities Revealed |
|---------|----------------------|
| Save a Link | Browser extension, auto-fill title, category/subcategory picker, tag input, save API endpoint |
| Search/Recovery | Full-text search across titles and URLs, filter by tag and interest, results display |
| Share a Curated List | Create/edit curated lists, select bookmarks into lists, generate public URL |
| View Shared List | Public route (no auth), clean read-only HTML rendering, link display |
| Self-Hoster Setup | Simple install process, first-run credential setup, README documentation |

## Web Application Specific Requirements

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

## Project Scoping & Phased Development

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

## Functional Requirements

### Bookmark Management

- **FR1:** User can save a bookmark by providing a URL and custom title
- **FR2:** User can assign an interest category to a bookmark
- **FR3:** User can optionally assign a subcategory within an interest to a bookmark
- **FR4:** User can add freeform tags to a bookmark
- **FR5:** User can edit a previously saved bookmark's title, category, subcategory, and tags
- **FR6:** User can delete a saved bookmark
- **FR7:** User can view a list of all saved bookmarks
- **FR8:** User can view bookmarks grouped or filtered by interest category
- **FR9:** User can view bookmarks filtered by subcategory within an interest
- **FR10:** User can view bookmarks filtered by tag

### Search & Discovery

- **FR11:** User can search bookmarks by keyword matching against title and URL
- **FR12:** User can combine search with interest/subcategory/tag filters
- **FR13:** User can see search results with bookmark title, URL, interest, and tags displayed

### Interest & Category Management

- **FR14:** User can create a new interest category
- **FR15:** User can rename an interest category
- **FR16:** User can delete an interest category
- **FR17:** User can create subcategories within an interest category
- **FR18:** User can rename a subcategory
- **FR19:** User can delete a subcategory

### Curated Shared Lists

- **FR20:** User can create a named curated list
- **FR21:** User can add bookmarks to a curated list
- **FR22:** User can remove bookmarks from a curated list
- **FR23:** User can edit the name of a curated list
- **FR24:** User can delete a curated list
- **FR25:** User can generate a public shareable URL for a curated list
- **FR26:** Anyone with the public URL can view the curated list without authentication
- **FR27:** Public curated list page displays bookmark titles and clickable URLs

### Browser Extension

- **FR28:** User can activate the extension from the browser toolbar
- **FR29:** Extension auto-fills the current page's title when activated
- **FR30:** Extension auto-fills the current page's URL when activated
- **FR31:** User can select an interest category from the extension
- **FR32:** User can select a subcategory from the extension
- **FR33:** User can enter freeform tags from the extension
- **FR34:** User can save the bookmark from the extension without leaving the current page
- **FR35:** Extension confirms successful save to the user

### Authentication & Security

- **FR36:** User can log in with credentials to access the application
- **FR37:** Unauthenticated users are redirected to the login page
- **FR38:** Public shared list pages are accessible without authentication
- **FR39:** User can log out of the application

### Setup & Configuration

- **FR40:** Self-hoster can set up initial login credentials on first run
- **FR41:** Application creates and initializes the SQLite database on first run

## Non-Functional Requirements

### Performance

- **NFR1:** Web UI pages load in < 1 second on localhost
- **NFR2:** Full-text search returns results in < 500ms with 10,000+ bookmarks
- **NFR3:** Browser extension save action completes in < 1 second round-trip
- **NFR4:** Public shared list pages render in < 1 second
- **NFR5:** Filtering by interest/subcategory/tag responds in < 500ms
- **NFR6:** Application remains responsive with 10,000+ stored bookmarks

### Security

- **NFR7:** User credentials are hashed — never stored in plaintext
- **NFR8:** All authenticated routes require valid session/token
- **NFR9:** Public shared list URLs use non-guessable identifiers (UUID or similar)
- **NFR10:** SQLite database file is not accessible via web routes
- **NFR11:** Browser extension communicates with backend over the configured host only

### Accessibility

- **NFR12:** All pages use semantic HTML elements (nav, main, section, button, etc.)
- **NFR13:** All interactive elements are keyboard navigable with visible focus indicators
- **NFR14:** Text meets minimum contrast ratios for readability
- **NFR15:** All form inputs have associated labels

### Reliability

- **NFR16:** SQLite data persists reliably — no data loss under normal operation
- **NFR17:** Application handles malformed URLs and invalid inputs gracefully with user-friendly error messages
- **NFR18:** Application recovers cleanly from database connection errors
