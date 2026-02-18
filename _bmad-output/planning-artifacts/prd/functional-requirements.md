# Functional Requirements

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
