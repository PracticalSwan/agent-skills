---
name: notion-docs
description: Notion workspace management via MCP — create databases, pages, comments, and knowledge bases. Use when building Notion documentation, organizing project wikis, or managing Notion content.
license: Complete terms in LICENSE.txt
---

# Notion Documentation

Effective documentation and review workflows using Notion MCP tools for structured knowledge management.

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

## Activation Conditions

- Creating and organizing documentation in Notion
- Building Notion databases for project tracking
- Managing knowledge bases and wikis
- Setting up review workflows with comments
- Structuring team documentation and onboarding guides

## Prerequisites

- Notion MCP tools activated (database/page creation, comment management, team/user management)
- Notion workspace with appropriate permissions
- Integration token configured for API access

---

## Creating Documentation Pages

### Page Structure Patterns

**Technical Documentation Page**:
```
# [Feature/Component Name]

## Overview
Brief description of what this covers.

## Architecture
System design and component relationships.

## API Reference
Endpoints, parameters, response schemas.

## Usage Examples
Code snippets and practical usage.

## Troubleshooting
Common issues and solutions.

## Changelog
Recent changes and version history.
```

**Meeting Notes Template**:
```
# [Meeting Title] — [Date]

## Attendees
- Person 1 (Role)
- Person 2 (Role)

## Agenda
1. Topic A
2. Topic B

## Discussion & Decisions
### Topic A
- Discussion points...
- **Decision**: [What was decided]
- **Action Item**: [Task] → @Owner by [Date]

## Next Steps
- [ ] Action item 1
- [ ] Action item 2
```

**Project Brief**:
```
# [Project Name]

## Problem Statement
What problem are we solving?

## Goals & Success Metrics
- Goal 1: Metric
- Goal 2: Metric

## Scope
### In Scope
### Out of Scope

## Timeline
| Phase | Dates | Deliverables |
|-------|-------|-------------|

## Dependencies & Risks
```

---

## Database Patterns

### Documentation Database Properties

| Property | Type | Purpose |
|----------|------|---------|
| Title | Title | Document name |
| Status | Select | Draft / In Review / Published / Archived |
| Category | Select | API / Guide / Architecture / Runbook |
| Owner | Person | Document author/maintainer |
| Last Reviewed | Date | When last reviewed for accuracy |
| Tags | Multi-select | Technology, feature, or team tags |
| Priority | Select | High / Medium / Low |

### Project Tracker Database

| Property | Type | Purpose |
|----------|------|---------|
| Task | Title | Task description |
| Status | Select | Not Started / In Progress / Done / Blocked |
| Assignee | Person | Who is responsible |
| Sprint | Select | Current sprint/iteration |
| Due Date | Date | Deadline |
| Priority | Select | P0 / P1 / P2 / P3 |
| Estimate | Number | Story points or hours |

---

## MCP Tool Workflows

### Creating a Knowledge Base
1. Use `Create a new Notion database` with documentation properties
2. Use `Create pages` to populate with initial documents
3. Use `Add a comment to a page` for review requests
4. Use `Get all comments of a page` to check review status

### Review Workflow
1. Author creates page with status "Draft"
2. Author adds comment tagging reviewer: "@Reviewer — ready for review"
3. Reviewer reads page and adds inline comments
4. Author addresses feedback, updates status to "Published"
5. Set "Last Reviewed" date

### Organizing Content
- Use database views (Table, Board, Calendar) for different perspectives
- Create linked databases for cross-referencing
- Use relation properties to connect related pages
- Tag consistently for filtering and search

---

## Best Practices

### Content Organization
- **One topic per page** — avoid mega-documents
- **Use headings** — H1 for title, H2 for sections, H3 for subsections
- **Link liberally** — connect related pages within Notion
- **Use callouts** — highlight warnings, tips, and important notes
- **Add a TOC** — for pages longer than 3 screens

### Maintenance
- Set quarterly review reminders for critical docs
- Archive outdated content instead of deleting
- Use "Last Reviewed" dates to identify stale pages
- Assign document owners for accountability

### Collaboration
- Use comments for async discussion and review
- Tag people in comments for notifications
- Create templates for recurring document types
- Establish naming conventions for consistency

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Page not found | Check page ID and permissions |
| Cannot create database | Verify integration has workspace access |
| Comments not appearing | Ensure comment permissions are enabled |
| Slow page loads | Reduce embedded content, split large pages |
| Permission denied | Check integration token scope and sharing settings |

---

## References & Resources

### Documentation
- [Notion Markdown Spec](./references/notion-markdown-spec.md) — Notion-flavored Markdown blocks, inline formatting, and limitations
- [Database Properties](./references/database-properties.md) — All 20 Notion property types with API formats and examples

### Scripts
- [Notion Templates](./scripts/notion-templates.js) — JavaScript template functions for common Notion page structures

### Examples
- [Workspace Setup Example](./examples/workspace-setup-example.md) — Complete dev team workspace setup with 9 MCP tool calls

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [notebooklm-management](../notebooklm-management/SKILL.md) | Alternative research/knowledge tool |
| [documentation-authoring](../documentation-authoring/SKILL.md) | Create structured docs to store in Notion |
