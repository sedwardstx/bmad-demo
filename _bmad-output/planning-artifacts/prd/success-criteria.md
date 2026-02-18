# Success Criteria

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
