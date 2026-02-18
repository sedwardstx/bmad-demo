---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments: []
date: 2026-02-18
author: Steve
---

# Product Brief: bmad-demo

## Executive Summary

bmad-demo is a personal bookmark management tool designed for people with diverse interests who save lots of web content for later reference. Unlike browser bookmarks — which suffer from poor default naming, flat organization, and no meaningful tagging — bmad-demo provides fast URL capture with user-defined titles, flexible tagging, and hierarchical organization by interest area and subcategory. Built on FastAPI + SQLite with a simple HTML front-end and a browser extension for frictionless saving, it's a lightweight, self-hosted solution that puts the user in full control of their data. Beyond personal use, it supports curated shareable link collections that can be viewed via public link or exported for sharing with friends.

---

## Core Vision

### Problem Statement

People who actively save web content — articles to re-read, videos to rewatch, references to revisit — quickly accumulate hundreds or thousands of bookmarks across a dozen or more interest areas. Browser bookmark systems fail them: links are saved with cryptic auto-generated names, there's no tagging system, and hierarchical folder structures are clunky to maintain and painful to search. The result is a growing graveyard of "saved" content that's effectively lost.

### Problem Impact

Valuable content that was intentionally saved becomes unfindable. Users waste time re-searching for things they already found. Knowledge that could be organized and shared remains trapped in chaotic browser bookmark bars. The friction of poor organization discourages saving altogether, leading to lost references and missed opportunities to share curated knowledge with others.

### Why Existing Solutions Fall Short

Existing bookmark tools like Pocket, Raindrop.io, and Pinboard add complexity, subscriptions, or vendor lock-in. Browser-native bookmarks lack tagging, smart search, and sharing capabilities. There's a gap for a simple, self-hosted tool that combines fast capture, structured tagging, hierarchical interest-based organization, and easy link curation and sharing — without the bloat.

### Proposed Solution

A self-hosted bookmark management app with three key components:
1. **Browser Extension** — One-click capture of the current page URL with fields for custom title, tags, interest category, and optional subcategory
2. **Web Application** — FastAPI + SQLite backend serving a simple HTML front-end for browsing, searching, and filtering saved links by tag, interest, or keyword
3. **Shareable Curated Lists** — Ability to assemble and share themed link collections via public viewable URLs or exportable formats

### Key Differentiators

- **Speed of capture** — Browser extension makes saving a link a 5-second interaction
- **Hierarchical organization** — Interest areas with subcategories, not just flat tags
- **Dual tagging model** — Both structured categories and freeform tags for maximum findability
- **Self-hosted simplicity** — FastAPI + SQLite means zero dependencies, zero subscriptions, full data ownership
- **Shareable by design** — Both the tool itself (open for others to deploy) and curated collections (shareable with friends)

---

## Target Users

### Primary Users

**"The Collector" — Active Link Saver**

*Example: Steve, a developer with 12+ hobbies*

A person who actively browses the web across many interests — gaming, cooking, woodworking, programming, whatever. They constantly stumble across articles, videos, tutorials, and references they want to revisit later. Their browser bookmarks are a mess: hundreds of links with auto-generated names they can't search, buried in folders they forgot existed.

- **Motivation:** Never lose a useful link again; find things fast when they need them
- **Context:** Browsing during downtime, researching a hobby, watching videos — the "save this for later" moment happens multiple times per day
- **Ideal flow:** Click browser extension → auto-fills page title → pick interest category, optionally a subcategory → add a few tags → save. Total time: ~5 seconds
- **Success moment:** Searching for "that sourdough video I saved" and finding it instantly by tag or interest area
- **Pain today:** Browser bookmarks are unsearchable, untaggable, and unorganized. Content that was intentionally saved is effectively lost.

### Secondary Users

**"The Recipient" — Shared Link Viewer**

*Example: Steve's friend who gets a Discord message saying "check out my gaming links"*

A person who receives a URL to a curated link collection. They have zero relationship with the tool itself — they just click a link and see a clean, browsable HTML page of curated links organized by the sharer. No sign-up, no install, no friction.

- **Motivation:** Browse interesting links someone curated for them
- **Context:** Receives a link via text, email, Discord, etc.
- **Ideal flow:** Click link → see a nicely formatted HTML page with the curated collection → click any link that interests them
- **Success moment:** "Oh cool, this is a great list" — finds something useful immediately

**"The Self-Hoster" — Clone & Run User**

*Example: A developer who sees the project and wants their own instance*

Someone who discovers the project (GitHub, word of mouth) and wants to run their own instance. They clone the repo, follow a few setup steps, and they're up and running.

- **Motivation:** Wants their own personal bookmark manager
- **Context:** Technically capable enough to clone a repo and run a Python app
- **Ideal flow:** Clone repo → install dependencies → run → start saving links
- **Success moment:** Their own instance is running and they're saving bookmarks within minutes

### User Journey

1. **Discovery:** Primary user finds the project on GitHub or hears about it from a friend
2. **Setup:** Clone repo, install dependencies, run the app — up in minutes
3. **First Save:** Install the browser extension, save their first link with a title, tags, and interest category
4. **Building the Collection:** Over days/weeks, capturing links becomes second nature — the extension is always one click away
5. **The "Aha!" Moment:** User searches for something they saved weeks ago and finds it instantly via tags or interest filter
6. **Sharing:** User curates a collection of their best gaming links and shares the public URL with friends
7. **Routine:** The tool becomes the default "save for later" action, replacing browser bookmarks entirely

---

## Success Metrics

### User Success Metrics

- **Effortless capture:** Saving a link takes no more than 5 seconds via the browser extension — title auto-fills, category selection is fast, tags are optional but easy
- **Findability:** User can locate any previously saved link within seconds using search, tag filter, or interest category browsing
- **Zero-friction sharing:** Creating and sharing a curated list is as simple as selecting links, generating a public URL, and sending it
- **Adoption signal:** The tool becomes the user's default "save for later" action, replacing browser bookmarks entirely

### Business Objectives

N/A — This is a personal/open-source project. Success is measured by personal utility and ease of use, not revenue or growth targets.

### Key Performance Indicators

| KPI | Target | Measurement |
|-----|--------|-------------|
| Time to save a link | < 5 seconds | From extension click to save |
| Time to find a saved link | < 10 seconds | From opening the app to locating the link |
| Time to create a shared list | < 2 minutes | From selecting links to generating a shareable URL |
| Setup time for self-hosters | < 10 minutes | Clone to first saved bookmark |
| Shared list recipient experience | Zero clicks to view | No sign-up, no install — just a clean HTML page |

---

## MVP Scope

### Core Features

1. **Web Application (FastAPI + SQLite)**
   - Single-user authentication (basic login to protect the instance)
   - Add bookmarks: URL, custom title, interest category, optional subcategory, optional freeform tags
   - Browse all saved bookmarks with filtering by interest, subcategory, and tag
   - Full-text search by title and URL
   - Edit and delete saved bookmarks
   - Manage interest categories and subcategories

2. **Browser Extension (Chromium/Edge)**
   - One-click capture of current page URL
   - Auto-fills page title from the active tab
   - Dropdown for interest category and subcategory selection
   - Freeform tag input
   - Save in ~5 seconds without leaving the current page

3. **Curated Shared Lists**
   - Select bookmarks into named collections
   - Generate a public URL for each curated list
   - Public URL renders a clean, read-only HTML page — no login required for viewers
   - Manage (create, edit, delete) curated lists from the main app

4. **Simple HTML Front-End**
   - Clean, functional UI — no framework bloat
   - Responsive enough for desktop and tablet use
   - Fast page loads, minimal JavaScript

### Out of Scope for MVP

- Multi-user / account management — single-user only
- Export shared lists to PDF, CSV, or other formats
- Import bookmarks from browser bookmark files
- Dead link detection / link health checking
- Auto-tagging or automatic URL metadata extraction
- Mobile-native app or mobile-optimized UI
- Firefox or Safari browser extension support
- Analytics or usage tracking dashboards
- API access for third-party integrations

### MVP Success Criteria

- A single user can save, tag, categorize, search, and retrieve bookmarks effortlessly
- Browser extension works on Chromium and Edge browsers for fast link capture
- Curated shared lists render as clean public HTML pages accessible to anyone with the link
- Self-hosters can clone the repo and be up and running in under 10 minutes
- The tool is simple enough to become the default "save for later" workflow

### Future Vision

- **Multi-user support** — optional accounts so multiple people can use a shared instance
- **Browser bookmark import** — bulk import from Chrome/Edge bookmark exports
- **Link health monitoring** — periodic checks for dead or moved links
- **Auto-metadata extraction** — pull page description, favicon, and preview image automatically
- **Export options** — PDF, CSV, and Markdown export of curated lists
- **Firefox/Safari extensions** — broader browser support
- **Mobile-friendly UI** — responsive redesign for phone-sized screens
- **API access** — RESTful API for third-party integrations and automation
- **Collaborative lists** — allow friends to contribute links to shared collections
