# Notion MCP Quickstart

This reference captures the current public setup patterns documented by Notion as of March 2026.

## Connection Options

### Hosted Remote Server

- Endpoint: `https://mcp.notion.com/mcp`
- Auth: OAuth
- Best for clients that support remote MCP servers directly

### Local Stdio Server

- Package: `@notionhq/notion-mcp-server`
- Auth: Notion integration token
- Best for local tooling and clients that only support stdio MCP servers

## Supported Capability Areas

Notion's public MCP docs describe support for:

- Search and retrieval
- Pages
- Databases
- Comments
- Users
- Agent actions and templates

The exact exposed tool names depend on the MCP host, so inspect the connected server in your client before assuming names.

## Operational Guidance

- Prefer search before page creation to avoid duplicates.
- Use databases for structured work tracking.
- Use standalone pages for long-form documents and specs.
- Keep database schemas small and stable.

## Rate Limits

Notion currently documents an average limit of 20 requests per second for integrations.

## Fallback Pattern

If Notion MCP is unavailable:

1. Draft the document locally.
2. Use `scripts/notion-templates.js` to standardize structure.
3. Paste or import into Notion manually when access is restored.
