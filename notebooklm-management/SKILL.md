---
name: notebooklm-management
description: Comprehensive toolkit for managing NotebookLM MCP server and its tools. Use when asked to query NotebookLM notebooks, add new notebooks from share links, manage notebook library, handle authentication issues, reset sessions, or work with Google's NotebookLM conversational research service. Covers notebook discovery, question-answering, session management, and metadata updates.
license: MIT
---

# NotebookLM MCP Management

Advanced toolkit for managing NotebookLM MCP server integration with GitHub Copilot. This skill enables effective use of NotebookLM's conversational AI research capabilities through MCP tools.

## When to Use This Skill

Activate this skill when:
- User mentions "NotebookLM", "notebook.lm", or "Google's AI research notebooks"
- Asked to query information from existing NotebookLM notebooks
- Requested to add a new notebook from a Google share link
- Need to manage notebook library (list, search, select notebooks)
- Troubleshooting NotebookLM authentication or session issues
- Working with knowledge bases stored in NotebookLM
- Performing conversational research or RAG-based queries
- Managing session context and chat history
- Updating notebook metadata (topics, descriptions, tags)

## Capabilities

### Core Operations

- **Notebook Discovery**: List library notebooks, search by topics/tags
- **Query Interface**: Ask questions about notebook content with contextual understanding
- **Notebook Integration**: Add notebooks via Google share URLs
- **Session Management**: Reset sessions, manage authentication state
- **Metadata Management**: Update notebook information (name, description, topics, use cases)

### Authentication Handling

- Initial Google authentication setup via browser
- Session recovery and refresh
- Cookie management for persistent access
- Rate limit handling and troubleshooting

## Prerequisites

### Required Accounts
- Google account with NotebookLM access (free tier or subscription)
- Existing NotebookLM notebooks or share links

### MCP Server Configuration
Ensure NotebookLM MCP server is properly configured in your MCP settings.

### Browser Access
- Google Chrome or compatible browser for OAuth flow

### Understanding of Limits
- Free tier: 100 notebooks, 50 sources each, 500k words, 50 daily queries
- Pro/Ultra: 5x higher limits

## Quick Reference Workflows

For detailed step-by-step workflows, see [workflows.md](./references/workflows.md).

### Quick Actions

| Action | Key Steps | Details |
|--------|-----------|---------|
| Add Notebook | Gather info → Propose → Confirm | Full flow in [workflows.md](./references/workflows.md#workflow-1-adding-a-new-notebook) |
| Query Notebook | Select → Formulate → Execute | Full flow in [workflows.md](./references/workflows.md#workflow-2-querying-notebooks) |
| Manage Library | List → Search → Update | Full flow in [workflows.md](./references/workflows.md#workflow-3-managing-notebook-library) |
| Update Metadata | Identify → Verify → Apply | Full flow in [workflows.md](./references/workflows.md) |
| Troubleshoot Auth | Diagnose → Repair → Verify | Full guide in [troubleshooting.md](./references/troubleshooting.md) |
| Reset Session | Identify → Confirm → Reset | Full guide in [workflows.md](./references/workflows.md) |

### Common Patterns

**Add Notebook**: See [examples/add-notebook.py](./examples/add-notebook.py) for usage patterns
**Query Notebook**: See [examples/simple-query.py](./examples/simple-query.py) for basic queries
**Multi-Turn**: See [examples/multi-turn-conversation.py](./examples/multi-turn-conversation.py) for conversation flow
**Library Management**: See [examples/library-management.py](./examples/library-management.py) for management tasks
**Ad-Hoc Queries**: See [examples/adhoc-query.py](./examples/adhoc-query.py) for temporary queries

## MCP Tool Reference

For complete tool documentation, see [MCP Tool Reference](./references/mcp-tool-reference.md).

### Quick Reference

| Tool | Purpose | Required Params | Key Options |
|------|---------|----------------|-------------|
| `add_notebook` | Add from share link | url, name, description, topics | content_types, use_cases, tags |
| `ask_question` | Query notebooks | question | notebook_id, session_id, notebook_url |
| `list_notebooks` | Show all notebooks | None | - |
| `search_notebooks` | Search library | query | - |
| `update_notebook` | Update metadata | id | name, description, topics, etc. |
| `reset_session` | Clear chat history | session_id | - |

See [mcp-tool-reference.md](./references/mcp-tool-reference.md) for detailed parameters, examples, and best practices.

## Interactive Workflows

### Common Scenarios

**First-Time User**: User mentions NotebookLM → Check Library → Decide needed action

**Conversational Research**: Select notebook → Query → Explore with follow-ups → Reset if needed

**Library Management**: Audit library → Organize topics → Update metadata → Remove outdated notes

For detailed implementation of these flows, see [workflows.md](./references/workflows.md)

## Best Practices Quick Guide

| Area | Best Practice | Details |
|------|---------------|---------|
| Query Formulation | Be specific and contextual | Use follow-up questions, leverage sessions |
| Metadata Quality | Descriptive names, good topics | 3-5 topics, clear use cases |
| Authentication | Check before queries | Handle rate limits gracefully |
| Library Organization | Group by topic, use tags | Update regularly, remove outdated |

## Troubleshooting Quick Reference

For comprehensive troubleshooting guide, see [troubleshooting.md](./references/troubleshooting.md)

| Issue | Quick Fix | Details |
|-------|----------|---------|
| Auth Required | `notebooklm.auth-setup` | See [Auth Issues](./references/troubleshooting.md#authentication-issues) |
| Query Timeout | Check network, simplify query | See [Query Issues](./references/troubleshooting.md#query-issues) |
| Session Expired | `reset_session` or new session | See [Session Issues](./references/troubleshooting.md#session-management-issues) |
| Rate Limit | Wait or upgrade account | See [Rate Limit](./references/troubleshooting.md#rate-limit-issues) |

## Common Code Patterns

For full examples with context, see [examples/](./examples) folder.

### Simple Query
```python
# Single question to a notebook
response = ask_question(
    question="How do I use useEffect?",
    notebook_id="react-docs-123"
)
```
Details: [simple-query.py](./examples/simple-query.py)

### Add Notebook
```python
# Add with good metadata
add_notebook(
    url="https://notebooklm.google/share/abc",
    name="React Guide",
    description="Complete React guide",
    topics=["React", "Frontend", "JavaScript"]
)
```
Details: [add-notebook.py](./examples/add-notebook.py)

## Additional Resources

### Documentation

- **[MCP Tool Reference](./references/mcp-tool-reference.md)** - Complete tool documentation
- **[Troubleshooting Guide](./references/troubleshooting.md)** - Issue diagnosis and resolution
- **[Workflows](./references/workflows.md)** - Detailed step-by-step procedures

### Code Examples

- **[simple-query.py](./examples/simple-query.py)** - Basic query patterns
- **[add-notebook.py](./examples/add-notebook.py)** - Adding notebooks with metadata
- **[multi-turn-conversation.py](./examples/multi-turn-conversation.py)** - Conversation flows
- **[library-management.py](./examples/library-management.py)** - Library operations
- **[adhoc-query.py](./examples/adhoc-query.py)** - Temporary notebook queries

### Utility Scripts

- **[notebooklm-helper.py](./scripts/notebooklm-helper.py)** - Management utility
  - Library quality analysis
  - Fuzzy search
  - Export functionality
  - See [scripts/README.md](./scripts/README.md) for usage

### External References

- [NotebookLM Official Site](https://notebooklm.google/)
- [Agent Skills Specification](https://agentskills.io/)

## Script Quick Start

```bash
# List all notebooks
python scripts/notebooklm-helper.py list

# Search for notebooks
python scripts/notebooklm-helper.py search --query "react"

# Generate quality report
python scripts/notebooklm-helper.py report

# Export library
python scripts/notebooklm-helper.py export --output backup.json
```

See [scripts/README.md](./scripts/README.md) for complete usage guide.

## Encoding

All files are UTF-8 encoded without BOM. Ensure all modifications maintain this encoding standard.
