# Non-Functional Requirements

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
