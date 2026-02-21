# Notion-Flavored Markdown Specification

Reference for the enhanced Markdown format used by Notion MCP tools (`create-pages`, `update-page`, `fetch`).
Notion Markdown extends standard Markdown with additional block types, inline formatting, and structural elements.

---

## Block Elements

### Headings

Notion supports three heading levels. Headings can include color attributes.

```markdown
# Heading 1
## Heading 2
### Heading 3

# Colored Heading {color="blue"}
## Another Heading {color="red"}
```

Heading 4–6 (`####`, `#####`, `######`) are **not supported** — they render as bold text or are ignored.

### Paragraphs

Plain text separated by blank lines. Inline formatting applies within paragraphs.

```markdown
This is a paragraph with **bold** and *italic* text.

This is another paragraph.
```

### Bullet Lists

Standard unordered lists using `-`, `*`, or `+`. Nesting via indentation (tab or 2–4 spaces).

```markdown
- Item one
- Item two
  - Nested item
  - Another nested item
    - Deeply nested
- Item three
```

### Numbered Lists

Ordered lists using `1.`, `2.`, etc. Nesting supported.

```markdown
1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step
```

### To-Do Lists

Checkbox items using `- [ ]` (unchecked) and `- [x]` (checked).

```markdown
- [ ] Unchecked task
- [x] Completed task
- [ ] Another pending task
```

### Code Blocks

Fenced code blocks with optional language identifier.

````markdown
```javascript
const greeting = "Hello, Notion!";
console.log(greeting);
```

```python
def greet(name):
    return f"Hello, {name}!"
```

```
Plain code block (no language)
```
````

### Callouts

Callout blocks use the `>` prefix followed by an emoji icon. Content follows on subsequent indented lines.

```markdown
> 💡 This is a tip callout
> Additional content inside the callout

> ⚠️ Warning callout
> Be careful with this operation

> ℹ️ Info callout with **bold** text inside
```

Common callout icons: `💡` (tip), `⚠️` (warning), `ℹ️` (info), `🔥` (important), `📝` (note), `✅` (success), `❌` (error).

### Toggle Blocks

Collapsible content using the `▶` character followed by the summary, with indented body content.

```markdown
▶ Click to expand
	Hidden content inside the toggle
	More hidden content

▶ Another toggle
	- Nested list inside toggle
	- Second item
```

The toggle body **must be indented with a tab** character.

### Tables

Standard Markdown table syntax. Header row required.

```markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

Alignment syntax is supported:

```markdown
| Left     | Center   | Right    |
|:---------|:--------:|---------:|
| aligned  | aligned  | aligned  |
```

### Dividers

Horizontal rules using `---`, `***`, or `___`.

```markdown
---
```

### Block Quotes

Standard blockquote syntax. Without an emoji prefix, renders as a Notion quote block (not a callout).

```markdown
> This is a block quote.
> It can span multiple lines.
```

### Bookmarks

Link bookmarks display as rich link previews.

```markdown
[bookmark](https://example.com)
```

Or as a standalone URL on its own line, which Notion may auto-convert to a bookmark.

### Embeds

Embedded content from supported services (YouTube, Figma, Google Maps, etc.).

```markdown
[embed](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
[embed](https://www.figma.com/file/abc123)
```

### Images

Standard Markdown image syntax.

```markdown
![Alt text](https://example.com/image.png)
```

---

## Inline Formatting

### Bold

```markdown
**bold text**
__also bold__
```

### Italic

```markdown
*italic text*
_also italic_
```

### Strikethrough

```markdown
~~strikethrough text~~
```

### Inline Code

```markdown
`inline code`
```

### Links

```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title")
```

### Mentions

Reference Notion pages, databases, users, or dates inline.

```markdown
@[Page Title](page-id-here)
```

User mentions and date mentions are typically inserted via API properties, not raw Markdown.

### Colors and Backgrounds

Apply inline colors using annotation syntax:

```markdown
**bold red text**{color="red"}
*italic blue*{color="blue"}
Text with background{bg="yellow"}
```

Available colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`.
Background colors use the same names with `_background` suffix or `bg` attribute.

---

## Page and Database Reference Tags

Notion Markdown uses special HTML-like tags to reference child pages and databases.

### Page References

```markdown
<page url="https://notion.so/workspace/Page-Title-abc123">Page Title</page>
```

When updating page content, preserving `<page>` tags prevents accidental deletion of child pages.

### Database References

```markdown
<database url="https://notion.so/workspace/DB-Title-abc123">Database Title</database>
```

### Data Source Tags

Returned by the `fetch` tool to identify collections within databases:

```markdown
<data-source url="collection://f336d0bc-b841-465b-8045-024475c079dd">Source Name</data-source>
```

Use the UUID from `collection://` URLs as `data_source_id` in MCP tool calls.

---

## Database-Specific Markdown

When creating pages inside a database, properties are passed as a JSON map — not as Markdown content.
The Markdown `content` field is for the page body only.

### Property Value Formats

| Property Type | Format |
|---------------|--------|
| Title | `"Task Name": "My Task"` |
| Text | `"Notes": "Some text"` |
| Number | `"Priority": 5` |
| Select | `"Status": "In Progress"` |
| Multi-select | `"Tags": "frontend, urgent"` |
| Checkbox | `"Done": "__YES__"` or `"Done": "__NO__"` |
| Date (start) | `"date:Due Date:start": "2024-12-25"` |
| Date (end) | `"date:Due Date:end": "2025-01-15"` |
| Date (is datetime) | `"date:Due Date:is_datetime": 0` |
| Place (name) | `"place:Office:name": "HQ"` |
| Place (coords) | `"place:Office:latitude": 37.77` |
| URL | `"userDefined:URL": "https://..."` |
| ID | `"userDefined:id": "PROJ-001"` |

Properties named `id` or `url` (case-insensitive) must be prefixed with `userDefined:`.

---

## Limitations vs Standard Markdown

| Feature | Standard Markdown | Notion Markdown |
|---------|-------------------|-----------------|
| Heading levels | h1–h6 | h1–h3 only |
| HTML tags | Supported | Not supported (except `<page>`, `<database>`, `<data-source>`) |
| Footnotes | Supported (some flavors) | Not supported |
| Definition lists | Supported (some flavors) | Not supported |
| Auto-linked URLs | Varies | Supported |
| LaTeX/math | Varies | Inline `$...$` and block `$$...$$` via equation blocks |
| Nested blockquotes | Supported | Limited support |
| Reference-style links | Supported | Not supported |
| Task lists in blockquotes | Supported | Not supported |
| Toggle blocks | N/A | Notion-specific (`▶` syntax) |
| Callouts with icons | N/A | Notion-specific (emoji + `>`) |
| Color annotations | N/A | Notion-specific (`{color="..."}`) |

---

## Common Formatting Patterns

### Section with Callout and Toggle

```markdown
# Project Overview

> 📝 This document outlines the project scope and timeline.

## Architecture

▶ System Components
	- Frontend: React + Vite
	- Backend: Next.js API Routes
	- Database: MongoDB Atlas

---

## Tasks

- [x] Set up repository
- [x] Configure CI/CD
- [ ] Implement authentication
- [ ] Deploy to staging
```

### Table with Inline Formatting

```markdown
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users` | **GET** | List all users |
| `/api/users/:id` | **GET** | Get user by ID |
| `/api/users` | **POST** | Create user |
| `/api/users/:id` | **DELETE** | *Admin only* — Delete user |
```

### Rich Page with Multiple Block Types

```markdown
# Sprint 12 Retrospective

**Date:** 2025-01-20
**Facilitator:** Alex

---

## What Went Well

> ✅ Highlights from this sprint

1. Shipped the new dashboard
2. Reduced API response time by 40%
3. Zero critical bugs in production

## What Could Improve

- [ ] Better test coverage for edge cases
- [ ] Earlier design reviews
- [ ] More async communication

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Add integration tests | Sarah | Jan 27 |
| Schedule design syncs | Mike | Jan 22 |

▶ Discussion Notes
	Detailed notes from the retrospective discussion go here.
	These are collapsed by default.
```
