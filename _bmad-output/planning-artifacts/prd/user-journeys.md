# User Journeys

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
