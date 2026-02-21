# Context7 MCP Integration Reference

## Overview

Context7 provides up-to-date library documentation via two MCP tools:
1. **resolve-library-id** — Resolves a library/package name into a Context7-compatible library ID
2. **get-library-docs** — Fetches documentation using the resolved library ID

Always resolve first, then fetch. Never guess library IDs.

---

## Tool 1: resolve-library-id

### Purpose
Converts a human-readable library name into the internal Context7 library ID required by `get-library-docs`.

### How It Works
- Analyzes the query to match against known libraries
- Ranks results by: name similarity, description relevance, documentation coverage, source reputation, benchmark scores
- Returns a list of candidate matches with IDs and confidence scores

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `libraryName` | string | Yes | Library or package name to resolve |

### Query Best Practices

**Be specific with the ecosystem:**
```
Good:  "python pandas"
Bad:   "pandas"          (could be confused with other ecosystems)
```

**Include the language when ambiguous:**
```
Good:  "javascript express"
Good:  "python flask"
Bad:   "flask"            (usually fine, but explicit is better)
```

**Use the canonical package name:**
```
Good:  "python pydantic"
Bad:   "python data validation"   (too generic)
```

**For scoped packages, use full name:**
```
Good:  "typescript @tanstack/react-query"
Good:  "python scikit-learn"
```

### Response Handling
- Results are ranked by relevance — pick the top match unless context dictates otherwise
- If multiple results appear (e.g., `pandas` vs `pandas-stubs`), choose based on your goal
- Store the resolved ID for subsequent `get-library-docs` calls

---

## Tool 2: get-library-docs

### Purpose
Fetches up-to-date documentation for a library using its Context7 ID.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `context7CompatibleLibraryID` | string | Yes | The ID returned by resolve-library-id |
| `topic` | string | No | Specific topic to focus documentation on |
| `tokens` | number | No | Max tokens of documentation to return (default varies) |

### Usage Patterns

**General documentation:**
```
get-library-docs(
  context7CompatibleLibraryID: "/python/pandas",
  tokens: 5000
)
```

**Topic-focused:**
```
get-library-docs(
  context7CompatibleLibraryID: "/python/fastapi",
  topic: "dependency injection",
  tokens: 3000
)
```

**Minimal lookup:**
```
get-library-docs(
  context7CompatibleLibraryID: "/python/pydantic",
  topic: "model validators",
  tokens: 1500
)
```

### Token Budget Guidelines
- **Quick reference** (API signature, single concept): 1000–2000 tokens
- **Feature overview** (multiple related concepts): 3000–5000 tokens
- **Comprehensive guide** (full API surface): 8000–10000 tokens
- Larger budgets return more content but cost more context window space

---

## Standard Workflow: Resolve Then Fetch

### Step 1: Resolve
```
resolve-library-id(libraryName: "python httpx")
→ Returns: { id: "/python/encode/httpx", ... }
```

### Step 2: Fetch
```
get-library-docs(
  context7CompatibleLibraryID: "/python/encode/httpx",
  topic: "async client usage",
  tokens: 3000
)
→ Returns: Documentation content about async client patterns
```

### Step 3: Apply
Use the returned documentation to:
- Answer user questions with current API details
- Generate code using up-to-date patterns
- Verify deprecated vs current approaches
- Cross-reference version-specific behavior

---

## Edge Cases & Troubleshooting

### Library Not Found
**Symptoms:** resolve-library-id returns empty or no confident matches.

**Recovery strategies:**
1. Try alternate names: `scikit-learn` vs `sklearn`, `Pillow` vs `PIL`
2. Add ecosystem prefix: `"python requests"` instead of `"requests"`
3. Use the PyPI package name exactly: `"python-dateutil"` not `"dateutil"`
4. For newer libraries, documentation may not be indexed yet — fall back to web search

### Ambiguous Names
**Symptoms:** Multiple results with similar confidence scores.

**Resolution:**
- Add context: `"python click CLI"` to disambiguate from other `click` packages
- Check the description field in results to identify the correct library
- When in doubt, pick the result with higher documentation coverage

### Stale Documentation
**Symptoms:** Returned docs reference outdated API or missing new features.

**Mitigation:**
- Specify the topic precisely to get the most relevant (likely updated) section
- Cross-reference with the library's official changelog
- Use web search as a fallback for brand-new features

### Rate Limiting / Timeouts
- Space out rapid successive calls
- Cache resolved library IDs within a session (they don't change frequently)
- Use smaller token budgets when you only need a quick answer

---

## Example Queries for Popular Libraries

### Python Web
```
resolve-library-id("python fastapi")
get-library-docs(id, topic: "path parameters and query parameters")

resolve-library-id("python django")
get-library-docs(id, topic: "class-based views")

resolve-library-id("python flask")
get-library-docs(id, topic: "blueprints")
```

### Python Data
```
resolve-library-id("python pandas")
get-library-docs(id, topic: "groupby aggregation")

resolve-library-id("python polars")
get-library-docs(id, topic: "lazy frame expressions")

resolve-library-id("python numpy")
get-library-docs(id, topic: "broadcasting rules")
```

### Python Testing
```
resolve-library-id("python pytest")
get-library-docs(id, topic: "fixtures and parametrize")

resolve-library-id("python hypothesis")
get-library-docs(id, topic: "strategies and composite")
```

### Python Validation
```
resolve-library-id("python pydantic")
get-library-docs(id, topic: "model validators and field validators")

resolve-library-id("python msgspec")
get-library-docs(id, topic: "struct types and decoding")
```

### Python HTTP
```
resolve-library-id("python httpx")
get-library-docs(id, topic: "async client and transports")

resolve-library-id("python aiohttp")
get-library-docs(id, topic: "client session and connection pooling")
```

### Python CLI
```
resolve-library-id("python typer")
get-library-docs(id, topic: "commands and options")

resolve-library-id("python rich")
get-library-docs(id, topic: "tables and console markup")
```
