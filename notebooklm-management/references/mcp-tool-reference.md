# NotebookLM MCP Tool Reference

Complete reference for all NotebookLM MCP server tools.

## add_notebook

Adds a notebook to your library from a Google share link.

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `url` | string | NotebookLM share URL | `https://notebooklm.google/share/xyz` |
| `name` | string | Display name for notebook | `React Documentation` |
| `description` | string | What knowledge/content is in this notebook | `Complete API docs and examples` |
| `topics` | array | Topics covered (3-5 recommended) | `["React", "API", "Frontend"]` |

### Optional Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `content_types` | array | Types of content | `["documentation", "examples"]` |
| `use_cases` | array | When to consult this notebook | `["API integration", "Debugging"]` |
| `tags` | array | Organizational tags | `["official", "v2.0", "core"]` |

### Best Practices for Metadata

**Names**: 
- Descriptive and specific
- Use version numbers if applicable
- Example: "React Documentation` or "n8n v2.0"

**Descriptions**:
- 1-2 sentences max
- Focus on content purpose
- Example: "Complete API documentation with examples and troubleshooting guides"

**Topics**:
- 3-5 topics optimal
- Use searchable keywords
- Include both broad and specific terms
- Example: `["React", "Hooks", "State Management", "Performance"]`

**Use Cases**:
- Describe when this notebook is helpful
- Be specific and actionable
- Example: `["Learning React hooks", "Solving state issues", "Performance optimization"]`

### Usage Example

```python
add_notebook(
    url="https://notebooklm.google/share/abc123",
    name="React Hooks Guide",
    description="Complete guide to React hooks with examples",
    topics=["React", "Hooks", "State Management"],
    content_types=["documentation", "examples"],
    use_cases=["Learning hooks", "Troubleshooting", "Best practices"],
    tags=["react", "hooks", "tutorial"]
)
```

## ask_question

Query NotebookLM with a natural language question.

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `question` | string | Natural language question | `How do I use useEffect?` |

### Optional Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `notebook_id` | string | Specific notebook to query | `notebook-abc-123` |
| `notebook_url` | string | Ad-hoc query URL (overrides notebook_id) | `https://notebooklm.google/share/xyz` |
| `session_id` | string | Continue existing conversation | `session-xyz-789` |
| `show_browser` | boolean | Display browser for debugging | `true` |
| `browser_options` | object | Advanced browser control | See below |

### Browser Options

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `headless` | boolean | Run browser in headless mode | `false` |
| `timeout` | integer | Timeout in milliseconds | `30000` |
| `viewport_width` | integer | Browser viewport width | `1280` |
| `viewport_height` | integer | Browser viewport height | `720` |

### Query Strategy

**Good Questions**:
- Specific: "How do I handle state cleanup in useEffect?"
- Contextual: "What are the best practices for error handling?"
- Focused: "Compare React Context vs Redux"

**Poor Questions**:
- Too vague: "Tell me about React"
- Multiple topics: "How do I use React, Vue, and Angular together?"
- No context: "Fix my code"

### Response Format

```json
{
  "answer": "The main features are...",
  "sources": ["Source 1", "Source 2"],
  "session_id": "session-abc-123",
  "confidence": 0.95
}
```

### Usage Examples

**Simple Query**:
```python
response = ask_question(
    question="What are the core benefits of using hooks?",
    notebook_id="react-hooks-123"
)
```

**Multi-Turn Conversation**:
```python
# First query
r1 = ask_question(
    question="What is React Context?",
    notebook_id="react-docs-123"
)
session_id = r1.session_id

# Follow-up
r2 = ask_question(
    question="How does it differ from Redux?",
    notebook_id="react-docs-123",
    session_id=session_id
)
```

**Ad-Hoc Query**:
```python
response = ask_question(
    question="Summarize the key concepts",
    notebook_url="https://notebooklm.google/share/public-notebook"
)
```

## list_notebooks

Shows all library notebooks with metadata.

### Parameters

None required.

### Response Format

```json
[
  {
    "id": "notebook-abc-123",
    "name": "React Documentation",
    "description": "Complete API documentation",
    "topics": ["React", "API", "Frontend"],
    "url": "https://notebooklm.google/share/abc",
    "created_at": "2026-02-16T10:00:00Z"
  }
]
```

### Usage Example

```python
notebooks = list_notebooks()
for notebook in notebooks:
    print(f"{notebook.name}")
    print(f"  Topics: {notebook.topics}")
    print(f"  Description: {notebook.description}")
```

## search_notebooks

Search library by query (name, description, topics, tags).

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `query` | string | Search term | `"react"` |

### Search Strategy

Queries search across:
- Notebook names
- Descriptions
- Topics
- Tags

**Good Search Queries**:
- Specific technology: `"react"`
- Concept: `"authentication"`
- Content type: `"tutorial"`
- Combined: `"react hooks"`

### Response Format

Same as `list_notebooks` but filtered results.

### Usage Examples

```python
# Find React notebooks
react_notebooks = search_notebooks(query="react")

# Find authentication docs
auth_docs = search_notebooks(query="authentication")

# Find tutorials
tutorials = search_notebooks(query="tutorial")
```

## update_notebook

Update notebook metadata.

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `id` | string | Notebook ID to update | `notebook-abc-123` |

### Optional Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `name` | string | New name | `Updated React Docs` |
| `description` | string | New description | `Enhanced documentation` |
| `topics` | array | Updated topics | `["React", "Hooks"]` |
| `content_types` | array | Updated content types | `["docs", "examples"]` |
| `use_cases` | array | Updated use cases | `["Learning", "Debugging"]` |
| `tags` | array | Updated tags | `["official", "v2.5"]` |
| `url` | string | Updated URL | New share link |

### When to Update

- Add new topics discovered
- Update description to be more accurate
- Add use cases based on experience
- Update version in tags
- Fix typos or clarify names

### Usage Example

```python
update_notebook(
    id="react-docs-123",
    name="React Hooks Deep Dive",
    description="Comprehensive guide to React hooks",
    topics=["React", "Hooks", "Performance", "Best Practices"],
    use_cases=["Learning hooks", "Optimizing performance", "Solving issues"],
    tags=["react", "hooks", "tutorial", "advanced"]
)
```

## reset_session

Reset session chat history (keeps same session ID).

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `session_id` | string | Session to reset | `session-xyz-789` |

### When to Reset

- Starting a completely new topic
- Session context is confusing
- Want fresh conversation context
- Too much history in session

### What Reset Does

- Clears chat history
- Keeps same session_id
- Maintains notebook context
- Allows new conversation flow

### Usage Example

```python
# After many questions on topic A
# Reset before moving to topic B
reset_session(session_id="session-abc-123")

# Now ask questions about topic B in same notebook
new_response = ask_question(
    question="Tell me about component lifecycle",
    notebook_id="react-docs-123",
    session_id="session-abc-123"
)
```

## Tool Selection Guide

| Task | Tool | Key Parameters |
|------|------|----------------|
| Add new notebook | `add_notebook` | `url`, `name`, `description`, `topics` |
| Ask a question | `ask_question` | `question`, optional `notebook_id` or `notebook_url` |
| Continue conversation | `ask_question` | `question`, `notebook_id`, `session_id` |
| Browse library | `list_notebooks` | None |
| Find specific notebook | `search_notebooks` | `query` |
| Update metadata | `update_notebook` | `id`, fields to update |
| Fresh conversation | `reset_session` | `session_id` |

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Authentication required | Not logged in | Run authentication flow |
| Notebook not found | Invalid notebook_id | Verify ID exists in library |
| Session expired | Old session_id | Use `reset_session` or create new |
| Rate limit exceeded | Too many queries | Wait or upgrade account |
| Invalid URL | Bad notebook share link | Verify share URL is valid |

### Best Practices

1. Always check authentication before operations
2. Store session_ids for multi-turn conversations
3. Handle rate limits gracefully
4. Validate notebook IDs before queries
5. Use descriptive metadata from the start
