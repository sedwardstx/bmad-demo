---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories, step-04-final-validation]
inputDocuments:
  - planning-artifacts/prd/index.md
  - planning-artifacts/prd/functional-requirements.md
  - planning-artifacts/prd/non-functional-requirements.md
  - planning-artifacts/prd/executive-summary.md
  - planning-artifacts/prd/product-scope.md
  - planning-artifacts/prd/project-scoping-phased-development.md
  - planning-artifacts/prd/user-journeys.md
  - planning-artifacts/prd/success-criteria.md
  - planning-artifacts/prd/project-classification.md
  - planning-artifacts/prd/web-application-specific-requirements.md
  - planning-artifacts/architecture/index.md
  - planning-artifacts/architecture/project-context-analysis.md
  - planning-artifacts/architecture/starter-template-evaluation.md
  - planning-artifacts/architecture/core-architectural-decisions.md
  - planning-artifacts/architecture/implementation-patterns-consistency-rules.md
  - planning-artifacts/architecture/project-structure-boundaries.md
  - planning-artifacts/architecture/architecture-validation-results.md
---

# bmad-demo - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for bmad-demo, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**Bookmark Management**

- FR1: User can save a bookmark by providing a URL and custom title
- FR2: User can assign an interest category to a bookmark
- FR3: User can optionally assign a subcategory within an interest to a bookmark
- FR4: User can add freeform tags to a bookmark
- FR5: User can edit a previously saved bookmark's title, category, subcategory, and tags
- FR6: User can delete a saved bookmark
- FR7: User can view a list of all saved bookmarks
- FR8: User can view bookmarks grouped or filtered by interest category
- FR9: User can view bookmarks filtered by subcategory within an interest
- FR10: User can view bookmarks filtered by tag

**Search & Discovery**

- FR11: User can search bookmarks by keyword matching against title and URL
- FR12: User can combine search with interest/subcategory/tag filters
- FR13: User can see search results with bookmark title, URL, interest, and tags displayed

**Interest & Category Management**

- FR14: User can create a new interest category
- FR15: User can rename an interest category
- FR16: User can delete an interest category
- FR17: User can create subcategories within an interest category
- FR18: User can rename a subcategory
- FR19: User can delete a subcategory

**Curated Shared Lists**

- FR20: User can create a named curated list
- FR21: User can add bookmarks to a curated list
- FR22: User can remove bookmarks from a curated list
- FR23: User can edit the name of a curated list
- FR24: User can delete a curated list
- FR25: User can generate a public shareable URL for a curated list
- FR26: Anyone with the public URL can view the curated list without authentication
- FR27: Public curated list page displays bookmark titles and clickable URLs

**Browser Extension**

- FR28: User can activate the extension from the browser toolbar
- FR29: Extension auto-fills the current page's title when activated
- FR30: Extension auto-fills the current page's URL when activated
- FR31: User can select an interest category from the extension
- FR32: User can select a subcategory from the extension
- FR33: User can enter freeform tags from the extension
- FR34: User can save the bookmark from the extension without leaving the current page
- FR35: Extension confirms successful save to the user

**Authentication & Security**

- FR36: User can log in with credentials to access the application
- FR37: Unauthenticated users are redirected to the login page
- FR38: Public shared list pages are accessible without authentication
- FR39: User can log out of the application

**Setup & Configuration**

- FR40: Self-hoster can set up initial login credentials on first run
- FR41: Application creates and initializes the SQLite database on first run

### NonFunctional Requirements

**Performance**

- NFR1: Web UI pages load in < 1 second on localhost
- NFR2: Full-text search returns results in < 500ms with 10,000+ bookmarks
- NFR3: Browser extension save action completes in < 1 second round-trip
- NFR4: Public shared list pages render in < 1 second
- NFR5: Filtering by interest/subcategory/tag responds in < 500ms
- NFR6: Application remains responsive with 10,000+ stored bookmarks

**Security**

- NFR7: User credentials are hashed — never stored in plaintext
- NFR8: All authenticated routes require valid session/token
- NFR9: Public shared list URLs use non-guessable identifiers (UUID or similar)
- NFR10: SQLite database file is not accessible via web routes
- NFR11: Browser extension communicates with backend over the configured host only

**Accessibility**

- NFR12: All pages use semantic HTML elements (nav, main, section, button, etc.)
- NFR13: All interactive elements are keyboard navigable with visible focus indicators
- NFR14: Text meets minimum contrast ratios for readability
- NFR15: All form inputs have associated labels

**Reliability**

- NFR16: SQLite data persists reliably — no data loss under normal operation
- NFR17: Application handles malformed URLs and invalid inputs gracefully with user-friendly error messages
- NFR18: Application recovers cleanly from database connection errors

### Additional Requirements

**From Architecture — Project Structure & Scaffolding:**

- Custom lean project structure (no starter template — project-specific custom scaffolding)
- Python 3.11+, FastAPI, SQLAlchemy (sync), SQLite, Jinja2
- Layer-based project organization: `models/`, `routers/`, `services/`, `schemas/` inside `app/`
- Separate `extension/` directory for Chromium/Edge Manifest V3 browser extension
- Separate `tests/` directory mirroring `app/` structure
- `.env.example` and `.env` for environment configuration
- `requirements.txt` for Python dependencies

**From Architecture — Authentication & Security:**

- Session/cookie-based auth for web application routes
- API token (stored in DB/config) for browser extension auth via `Authorization: Bearer` header
- `passlib[bcrypt]` for password hashing
- FastAPI `CORSMiddleware` configured for browser extension origin
- UUID4 slugs for public shared list URLs (`/shared/{uuid}`)
- FastAPI `Depends()` for auth injection — no inline auth logic

**From Architecture — API & Communication:**

- RESTful JSON API under `/api/v1/` prefix for extension
- Key endpoints: `GET /api/v1/categories`, `POST /api/v1/bookmarks`, `POST /api/v1/auth/token`
- JSON error responses with status codes for API, HTML error pages for web
- Pydantic schemas for request/response validation

**From Architecture — Frontend:**

- Classless CSS framework (Pico CSS or Simple.css) — no build step
- Vanilla JavaScript — no framework (search, filters, form validation only)
- Jinja2 server-rendered templates (MPA pattern)
- Static assets served by FastAPI directly

**From Architecture — Infrastructure & Deployment:**

- Uvicorn as app server (direct, no Gunicorn)
- `.env` file + `python-dotenv` for config (DB path, secret key, API token, host/port)
- Python `logging` module — no `print()` statements
- `create_all()` schema management on startup (Alembic deferred to post-MVP)
- pytest for testing with fixtures in `tests/conftest.py`

**From Architecture — Implementation Patterns:**

- snake_case for all Python code, database columns, API parameters, JSON fields
- PascalCase for Python class names only
- Database tables: snake_case, plural (`bookmarks`, `interests`, `curated_lists`)
- Foreign keys: `{referenced_table_singular}_id`
- Routers call services — never access the database directly
- Services contain business logic and call SQLAlchemy models/queries
- Services raise custom exceptions; routers handle them per channel

**From Architecture — Implementation Sequence:**

1. Project scaffolding + DB setup
2. Auth (session/cookie login, API token generation)
3. Bookmark CRUD (web routes + Jinja2 templates)
4. Search & filtering
5. Interest/subcategory management
6. Extension API endpoints (`/api/v1/`)
7. Browser extension (Manifest V3)
8. Curated shared lists + public pages

### FR Coverage Map

- FR1: Epic 3 - Save a bookmark by providing URL and title
- FR2: Epic 3 - Assign an interest category to a bookmark
- FR3: Epic 3 - Optionally assign a subcategory to a bookmark
- FR4: Epic 3 - Add freeform tags to a bookmark
- FR5: Epic 3 - Edit a bookmark's title, category, subcategory, and tags
- FR6: Epic 3 - Delete a saved bookmark
- FR7: Epic 3 - View a list of all saved bookmarks
- FR8: Epic 3 - View bookmarks filtered by interest category
- FR9: Epic 3 - View bookmarks filtered by subcategory
- FR10: Epic 3 - View bookmarks filtered by tag
- FR11: Epic 4 - Search bookmarks by keyword against title and URL
- FR12: Epic 4 - Combine search with interest/subcategory/tag filters
- FR13: Epic 4 - See search results with title, URL, interest, and tags
- FR14: Epic 3 - Create a new interest category
- FR15: Epic 3 - Rename an interest category
- FR16: Epic 3 - Delete an interest category
- FR17: Epic 3 - Create subcategories within an interest
- FR18: Epic 3 - Rename a subcategory
- FR19: Epic 3 - Delete a subcategory
- FR20: Epic 5 - Create a named curated list
- FR21: Epic 5 - Add bookmarks to a curated list
- FR22: Epic 5 - Remove bookmarks from a curated list
- FR23: Epic 5 - Edit the name of a curated list
- FR24: Epic 5 - Delete a curated list
- FR25: Epic 5 - Generate a public shareable URL for a curated list
- FR26: Epic 5 - Anyone with URL can view curated list without auth
- FR27: Epic 5 - Public list displays bookmark titles and clickable URLs
- FR28: Epic 6 - Activate extension from browser toolbar
- FR29: Epic 6 - Extension auto-fills current page title
- FR30: Epic 6 - Extension auto-fills current page URL
- FR31: Epic 6 - Select interest category from extension
- FR32: Epic 6 - Select subcategory from extension
- FR33: Epic 6 - Enter freeform tags from extension
- FR34: Epic 6 - Save bookmark from extension without leaving page
- FR35: Epic 6 - Extension confirms successful save
- FR36: Epic 2 - Log in with credentials
- FR37: Epic 2 - Unauthenticated users redirected to login
- FR38: Epic 2 - Public shared list pages accessible without auth
- FR39: Epic 2 - Log out of the application
- FR40: Epic 1 - Set up initial login credentials on first run
- FR41: Epic 1 - Application creates and initializes SQLite database on first run

## Epic List

### Epic 1: Project Foundation & First-Run Setup
Users can clone the project, run it for the first time, set up their credentials, and see the application running with an empty state. The database initializes automatically and the user lands on a functional (if empty) home page.
**FRs covered:** FR40, FR41
**NFR coverage:** NFR7, NFR10, NFR16

### Epic 2: User Authentication
Users can log in to protect their instance, stay authenticated across page loads, and log out. Unauthenticated visitors are redirected to login. Public shared list pages remain accessible without auth.
**FRs covered:** FR36, FR37, FR38, FR39
**NFR coverage:** NFR8, NFR9

### Epic 3: Bookmark Management
Users can save, view, edit, and delete bookmarks with titles, URLs, interest categories, subcategories, and tags. Users can browse all bookmarks and filter by interest, subcategory, or tag.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9, FR10, FR14, FR15, FR16, FR17, FR18, FR19
**NFR coverage:** NFR1, NFR5, NFR6, NFR12, NFR13, NFR14, NFR15, NFR17

### Epic 4: Search & Discovery
Users can search bookmarks by keyword against title and URL, combine search with existing filters, and see rich results with all relevant metadata displayed.
**FRs covered:** FR11, FR12, FR13
**NFR coverage:** NFR2

### Epic 5: Curated Shared Lists
Users can create named curated lists, add/remove bookmarks, edit/delete lists, generate public shareable URLs, and anyone with the URL can view the curated list without logging in.
**FRs covered:** FR20, FR21, FR22, FR23, FR24, FR25, FR26, FR27
**NFR coverage:** NFR4, NFR9

### Epic 6: Browser Extension
Users can install a Chromium/Edge extension that auto-fills the current page's title and URL, lets them select a category/subcategory and enter tags, and saves the bookmark without leaving the page — with confirmation feedback.
**FRs covered:** FR28, FR29, FR30, FR31, FR32, FR33, FR34, FR35
**NFR coverage:** NFR3, NFR11

---

## Epic 1: Project Foundation & First-Run Setup

Users can clone the project, run it for the first time, set up their credentials, and see the application running with an empty state. The database initializes automatically and the user lands on a functional (if empty) home page.

### Story 1.1: Project Scaffolding & Database Initialization

As a **self-hoster**,
I want to clone the repository, install dependencies, and run the application so that it starts up successfully with an auto-initialized database,
So that I have a working application foundation ready for use.

**Acceptance Criteria:**

**Given** the user has cloned the repository and has Python 3.11+ installed
**When** they install dependencies via `pip install -r requirements.txt`
**Then** all required packages install successfully (FastAPI, SQLAlchemy, uvicorn, python-dotenv, passlib[bcrypt], Jinja2)

**Given** a `.env.example` file exists in the project root
**When** the user copies it to `.env`
**Then** the file contains documented configuration for `DATABASE_URL`, `SECRET_KEY`, `HOST`, and `PORT` with sensible defaults

**Given** the application is started via `uvicorn app.main:app`
**When** no SQLite database file exists yet
**Then** the application creates the database file and initializes all tables via `create_all()`

**Given** the application is running
**When** the user navigates to the root URL
**Then** they see a functional page (setup page or redirect to setup if no user exists)

**Given** the project structure exists
**When** examining the directory layout
**Then** it follows the architecture specification: `app/` with `models/`, `routers/`, `services/`, `schemas/`, `templates/`, `static/` subdirectories, plus `extension/`, `tests/`, `requirements.txt`, `.env.example`, `.gitignore`

**Given** the application is running
**When** attempting to access the SQLite database file via any web route
**Then** the file is not served or accessible (NFR10)

### Story 1.2: First-Run Credential Setup

As a **self-hoster**,
I want to create my login credentials on first run,
So that my bookmark manager instance is protected from unauthorized access.

**Acceptance Criteria:**

**Given** the application is running and no user account exists in the database
**When** the user navigates to any page
**Then** they are redirected to the `/setup` page

**Given** the user is on the `/setup` page
**When** they enter a username and password and submit the form
**Then** a user account is created with the password hashed using bcrypt (NFR7)
**And** the user is redirected to the `/login` page with a success message

**Given** a user account already exists in the database
**When** someone navigates to `/setup`
**Then** they are redirected away from setup (setup is a one-time operation)

**Given** the user is on the `/setup` page
**When** they submit the form with an empty username or password
**Then** they see a validation error message and the account is not created

**Given** the user has completed setup
**When** the application is restarted
**Then** the credentials persist in the SQLite database and setup is not shown again (NFR16)

---

## Epic 2: User Authentication

Users can log in to protect their instance, stay authenticated across page loads, and log out. Unauthenticated visitors are redirected to login. Public shared list pages remain accessible without auth.

### Story 2.1: User Login

As a **user**,
I want to log in with my credentials,
So that I can access my bookmark manager securely.

**Acceptance Criteria:**

**Given** the user navigates to `/login`
**When** the login page loads
**Then** a form is displayed with username and password fields and a submit button
**And** the page uses semantic HTML with proper labels for all inputs (NFR12, NFR15)

**Given** the user enters valid credentials and submits the login form
**When** the password matches the bcrypt-hashed password in the database
**Then** a session cookie is created for the user
**And** the user is redirected to the home page

**Given** the user enters invalid credentials
**When** they submit the login form
**Then** an error message is displayed ("Invalid username or password")
**And** no session is created
**And** the user remains on the login page

**Given** the user enters empty fields
**When** they submit the login form
**Then** a validation error is shown and no authentication attempt is made

### Story 2.2: Session Enforcement & Logout

As a **user**,
I want unauthenticated requests to be blocked and to be able to log out,
So that my bookmarks are protected and I can end my session securely.

**Acceptance Criteria:**

**Given** a user is not logged in (no valid session cookie)
**When** they navigate to any protected route (e.g., `/`, `/bookmarks`, `/interests`, `/lists`)
**Then** they are redirected to `/login` (FR37)

**Given** a user is logged in with a valid session cookie
**When** they navigate to any protected route
**Then** the page loads normally with their authenticated context (NFR8)

**Given** a user is logged in
**When** they click the logout action
**Then** their session cookie is cleared
**And** they are redirected to `/login`
**And** subsequent requests to protected routes redirect to login (FR39)

**Given** a user has an expired or tampered session cookie
**When** they navigate to a protected route
**Then** they are redirected to `/login`

### Story 2.3: API Token Authentication for Extension

As a **user**,
I want to generate an API token and authenticate API requests with it,
So that my browser extension can securely communicate with the backend.

**Acceptance Criteria:**

**Given** a user is logged in to the web application
**When** an API token does not yet exist
**Then** a token is auto-generated, stored in the database, and displayed to the user on a settings or profile page for copying into the extension

**Given** the browser extension sends a request to `/api/v1/*` with a valid `Authorization: Bearer {token}` header
**When** the token matches the stored API token
**Then** the request is authenticated and processed normally

**Given** the browser extension sends a request to `/api/v1/*` with an invalid or missing token
**When** the server validates the token
**Then** a `401 Unauthorized` JSON response is returned (`{"detail": "Invalid or missing API token"}`)

**Given** any user (authenticated or not) navigates to `/shared/{uuid}`
**When** the UUID corresponds to a valid public shared list
**Then** the page renders without requiring any authentication (FR38)
**And** no session cookie or API token is checked

**Given** a shared list URL uses a UUID4 identifier
**When** examining the URL pattern
**Then** the identifier is non-guessable (NFR9)

---

## Epic 3: Bookmark Management

Users can save, view, edit, and delete bookmarks with titles, URLs, interest categories, subcategories, and tags. Users can browse all bookmarks and filter by interest, subcategory, or tag.

### Story 3.1: Interest & Subcategory Management

As a **user**,
I want to create, rename, and delete interest categories and subcategories,
So that I can organize my bookmarks into a meaningful hierarchy before saving them.

**Acceptance Criteria:**

**Given** the user navigates to the interests management page
**When** the page loads
**Then** all existing interest categories are displayed with their subcategories
**And** the page uses semantic HTML elements (NFR12)

**Given** the user enters a new interest category name and submits
**When** the name is valid and non-empty
**Then** the interest category is created and appears in the list (FR14)

**Given** the user clicks rename on an existing interest category
**When** they enter a new name and confirm
**Then** the category name is updated (FR15)

**Given** the user clicks delete on an interest category
**When** they confirm the deletion
**Then** the category and all its subcategories are removed (FR16)
**And** bookmarks previously assigned to it have their category cleared

**Given** the user selects an interest category
**When** they enter a new subcategory name and submit
**Then** the subcategory is created within that interest (FR17)

**Given** the user clicks rename on a subcategory
**When** they enter a new name and confirm
**Then** the subcategory name is updated (FR18)

**Given** the user clicks delete on a subcategory
**When** they confirm the deletion
**Then** the subcategory is removed (FR19)
**And** bookmarks previously assigned to it have their subcategory cleared

**Given** the user submits an empty name for a category or subcategory
**When** the form is validated
**Then** an error message is displayed and no change is made (NFR17)

### Story 3.2: Bookmark Creation with Categorization

As a **user**,
I want to save a bookmark with a URL, title, interest category, optional subcategory, and tags,
So that I can capture and organize links I want to keep.

**Acceptance Criteria:**

**Given** the user navigates to the add bookmark page
**When** the page loads
**Then** a form is displayed with fields for URL, title, interest category (dropdown), subcategory (dropdown, optional), and tags (freeform text input)
**And** all form inputs have associated labels (NFR15)

**Given** the user fills in a URL and title, selects an interest category, and submits
**When** the data is valid
**Then** the bookmark is saved to the database with the provided details (FR1, FR2)

**Given** the user optionally selects a subcategory
**When** they submit the form
**Then** the bookmark is saved with the subcategory association (FR3)

**Given** the user enters comma-separated tags in the tags field
**When** they submit the form
**Then** each tag is created (if new) and associated with the bookmark (FR4)
**And** tags are trimmed of whitespace and stored in lowercase

**Given** the user submits a bookmark with an empty URL or title
**When** the form is validated
**Then** a user-friendly error message is shown and the bookmark is not saved (NFR17)

**Given** the user submits a bookmark with a malformed URL
**When** the form is validated
**Then** a user-friendly error message indicates the URL is invalid (NFR17)

**Given** the subcategory dropdown
**When** the user selects an interest category
**Then** the subcategory dropdown updates to show only subcategories belonging to that interest

### Story 3.3: Bookmark List & Viewing

As a **user**,
I want to view all my saved bookmarks in a list,
So that I can browse and access my saved links.

**Acceptance Criteria:**

**Given** the user navigates to the bookmarks page
**When** bookmarks exist in the database
**Then** all bookmarks are displayed in a list showing title, URL (clickable), interest category, and tags (FR7)
**And** the page loads in under 1 second (NFR1)

**Given** the user navigates to the bookmarks page
**When** no bookmarks exist
**Then** a friendly empty state message is displayed with a link to add a bookmark

**Given** the bookmark list page
**When** examining the HTML structure
**Then** it uses semantic HTML elements (`nav`, `main`, `section`, etc.) (NFR12)
**And** all interactive elements are keyboard navigable with visible focus indicators (NFR13)
**And** text meets minimum contrast ratios (NFR14)

**Given** the base layout template
**When** any authenticated page loads
**Then** a consistent navigation bar is displayed with links to Bookmarks, Interests, Curated Lists, and Logout

### Story 3.4: Bookmark Editing & Deletion

As a **user**,
I want to edit or delete my saved bookmarks,
So that I can keep my bookmark collection accurate and up to date.

**Acceptance Criteria:**

**Given** the user clicks edit on a bookmark
**When** the edit form loads
**Then** it is pre-populated with the bookmark's current title, URL, interest category, subcategory, and tags (FR5)

**Given** the user modifies bookmark fields and submits the edit form
**When** the data is valid
**Then** the bookmark is updated in the database with the new values
**And** the user is redirected to the bookmark list with a success message

**Given** the user changes the interest category on an existing bookmark
**When** they submit the edit form
**Then** the subcategory is cleared if it doesn't belong to the new category

**Given** the user changes tags on an existing bookmark
**When** they submit the edit form
**Then** old tag associations are removed and new ones are created

**Given** the user clicks delete on a bookmark
**When** they confirm the deletion
**Then** the bookmark and its tag associations are removed from the database (FR6)
**And** the user is returned to the bookmark list with a confirmation message

**Given** the user submits an edit with invalid data (empty title, malformed URL)
**When** the form is validated
**Then** an error message is shown and the bookmark is not updated (NFR17)

### Story 3.5: Bookmark Filtering

As a **user**,
I want to filter my bookmarks by interest category, subcategory, or tag,
So that I can quickly find bookmarks related to a specific topic.

**Acceptance Criteria:**

**Given** the user is on the bookmarks page
**When** they select an interest category from the filter controls
**Then** only bookmarks assigned to that interest are displayed (FR8)
**And** the filter responds in under 500ms (NFR5)

**Given** the user has filtered by interest category
**When** they further select a subcategory filter
**Then** only bookmarks matching both the interest and subcategory are displayed (FR9)

**Given** the user selects a tag from the filter controls
**When** the filter is applied
**Then** only bookmarks with that tag are displayed (FR10)

**Given** the user has active filters applied
**When** they clear the filters
**Then** all bookmarks are displayed again

**Given** the user applies a filter that matches no bookmarks
**When** the results load
**Then** a message indicates no bookmarks match the current filter

**Given** the database contains 10,000+ bookmarks
**When** the user applies any filter
**Then** the application remains responsive (NFR6)

---

## Epic 4: Search & Discovery

Users can search bookmarks by keyword against title and URL, combine search with existing filters, and see rich results with all relevant metadata displayed.

### Story 4.1: Keyword Search with Filter Combination

As a **user**,
I want to search my bookmarks by keyword and combine search with filters,
So that I can quickly find specific bookmarks by name or URL even in a large collection.

**Acceptance Criteria:**

**Given** the user is on the bookmarks page
**When** they enter a keyword in the search bar and submit
**Then** only bookmarks whose title or URL contain the keyword are displayed (FR11)
**And** results are returned in under 500ms even with 10,000+ bookmarks (NFR2)

**Given** the user has entered a search keyword
**When** they also select an interest category, subcategory, or tag filter
**Then** results are narrowed to bookmarks matching both the keyword and the active filters (FR12)

**Given** search results are displayed
**When** viewing each result
**Then** the bookmark title, URL (clickable), interest category, and tags are all shown (FR13)

**Given** the user enters a keyword that matches no bookmarks
**When** the search completes
**Then** a message indicates no results were found for the search term

**Given** the user has an active search
**When** they clear the search bar
**Then** the full bookmark list (with any active filters) is displayed again

**Given** the search uses SQL `LIKE` matching
**When** the user enters a partial word
**Then** bookmarks containing that substring in title or URL are returned

---

## Epic 5: Curated Shared Lists

Users can create named curated lists, add/remove bookmarks, edit/delete lists, generate public shareable URLs, and anyone with the URL can view the curated list without logging in.

### Story 5.1: Curated List CRUD

As a **user**,
I want to create, rename, and delete curated lists,
So that I can organize themed collections of bookmarks to share.

**Acceptance Criteria:**

**Given** the user navigates to the curated lists page
**When** the page loads
**Then** all existing curated lists are displayed with their names and bookmark counts

**Given** the user enters a new list name and submits
**When** the name is valid and non-empty
**Then** a new curated list is created and appears in the list (FR20)

**Given** the user clicks rename on a curated list
**When** they enter a new name and confirm
**Then** the list name is updated (FR23)

**Given** the user clicks delete on a curated list
**When** they confirm the deletion
**Then** the curated list and all its bookmark associations are removed (FR24)
**And** the bookmarks themselves are not deleted

**Given** the user submits an empty name for a curated list
**When** the form is validated
**Then** an error message is displayed and no list is created (NFR17)

### Story 5.2: Manage List Bookmarks

As a **user**,
I want to add and remove bookmarks from my curated lists,
So that I can compose the perfect collection to share.

**Acceptance Criteria:**

**Given** the user opens a curated list for editing
**When** the edit page loads
**Then** the current bookmarks in the list are displayed
**And** available bookmarks not yet in the list are shown or searchable

**Given** the user selects a bookmark to add to the curated list
**When** they confirm the addition
**Then** the bookmark is associated with the curated list and appears in the list contents (FR21)

**Given** the user clicks remove on a bookmark within the curated list
**When** they confirm the removal
**Then** the bookmark is disassociated from the curated list (FR22)
**And** the bookmark itself is not deleted from the user's collection

**Given** a curated list has multiple bookmarks
**When** viewing the list edit page
**Then** bookmarks are displayed with their titles and URLs for easy identification

### Story 5.3: Public Shared List Page

As a **user**,
I want to generate a public shareable URL for my curated list so anyone can view it,
So that I can share my curated bookmarks with friends without requiring them to log in.

**Acceptance Criteria:**

**Given** the user is viewing a curated list
**When** they click the share/generate link action
**Then** a UUID4-based public URL is generated and displayed for copying (FR25)
**And** the URL follows the pattern `/shared/{uuid}` (NFR9)

**Given** any person (authenticated or not) navigates to `/shared/{uuid}`
**When** the UUID corresponds to a valid curated list
**Then** the page renders without requiring any authentication (FR26)
**And** the page displays the list name, bookmark titles, and clickable URLs (FR27)
**And** the page renders in under 1 second (NFR4)

**Given** a person navigates to `/shared/{uuid}`
**When** the UUID does not correspond to any curated list
**Then** a 404 error page is displayed

**Given** a curated list already has a generated public URL
**When** the user views the list
**Then** the existing shareable URL is displayed (not regenerated)

**Given** the user deletes a curated list that has a public URL
**When** someone later visits that URL
**Then** a 404 error page is displayed

---

## Epic 6: Browser Extension

Users can install a Chromium/Edge extension that auto-fills the current page's title and URL, lets them select a category/subcategory and enter tags, and saves the bookmark without leaving the page — with confirmation feedback.

### Story 6.1: Extension Setup & Configuration

As a **user**,
I want to install the browser extension and configure it with my server URL and API token,
So that the extension can communicate securely with my self-hosted bookmark manager.

**Acceptance Criteria:**

**Given** the user loads the extension into Chrome/Edge as an unpacked extension
**When** the extension is installed
**Then** an extension icon appears in the browser toolbar (FR28)
**And** the extension uses Manifest V3 format

**Given** the user opens the extension options page
**When** the options page loads
**Then** fields are displayed for server URL and API token

**Given** the user enters a server URL and API token and saves
**When** the settings are saved
**Then** the values are persisted in extension storage
**And** the extension uses only the configured host for all communication (NFR11)

**Given** the extension has no configured server URL or API token
**When** the user clicks the extension icon
**Then** a message directs them to configure the extension via the options page

### Story 6.2: Extension Popup & Auto-Fill

As a **user**,
I want the extension popup to auto-fill the current page's title and URL and let me categorize the bookmark,
So that I can quickly capture a bookmark with minimal manual entry.

**Acceptance Criteria:**

**Given** the user clicks the extension icon on any web page
**When** the popup opens
**Then** the current page's title is auto-filled in the title field (FR29)
**And** the current page's URL is auto-filled in the URL field (FR30)

**Given** the popup is open and the extension is configured
**When** the popup loads category data
**Then** interest categories are fetched from `GET /api/v1/categories` and displayed in a dropdown (FR31)

**Given** the user selects an interest category
**When** that category has subcategories
**Then** a subcategory dropdown is populated with the relevant subcategories (FR32)

**Given** the popup is open
**When** the user views the form
**Then** a freeform text input for tags is available (FR33)

**Given** the extension cannot reach the server or the API token is invalid
**When** the popup tries to load categories
**Then** an error message is displayed in the popup

### Story 6.3: Save Bookmark from Extension

As a **user**,
I want to save a bookmark from the extension without leaving the current page,
So that I can capture links seamlessly as I browse.

**Acceptance Criteria:**

**Given** the user has filled in the bookmark details in the popup
**When** they click the save button
**Then** the bookmark is submitted to `POST /api/v1/bookmarks` with the title, URL, interest, subcategory, and tags
**And** the save completes without navigating away from the current page (FR34)

**Given** the bookmark is saved successfully
**When** the API returns a success response
**Then** the extension displays a success confirmation message in the popup (FR35)
**And** the round-trip completes in under 1 second (NFR3)

**Given** the save fails (network error, server error, validation error)
**When** the API returns an error response
**Then** a user-friendly error message is displayed in the popup
**And** the user can correct the input and retry

**Given** the user submits with an empty URL or title
**When** the form is validated client-side
**Then** a validation error is shown before any API call is made

**Given** the API returns a 401 Unauthorized response
**When** the extension displays the error
**Then** the message indicates the API token may be invalid and directs the user to check extension settings
