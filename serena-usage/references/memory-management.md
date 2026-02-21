# Serena Memory Management Reference

## Overview

Serena's memory system provides persistent project context across AI agent sessions. Memories store architectural decisions, active context, progress tracking, and project intelligence that survives session resets.

## Memory Naming Conventions

Use standardized names for core memories to ensure consistency:

| Memory Name | Purpose | Update Frequency |
|---|---|---|
| `project-brief` | Core requirements, goals, project scope | Rarely (foundation document) |
| `active-context` | Current work focus, recent changes, next steps | Every session |
| `system-patterns` | Architecture, design patterns, component relationships | When patterns change |
| `tech-context` | Technologies, setup, constraints, dependencies | When stack changes |
| `progress` | What works, what's left, known issues | After significant work |
| `task-index` | Master list of all tasks with statuses | When tasks change |
| `task-{id}` | Individual task details (e.g. `task-001-auth`) | During task work |

### Custom Memory Names

For project-specific memories beyond the core set:

- Use lowercase kebab-case: `api-contracts`, `deployment-config`
- Prefix with domain: `db-schema-decisions`, `ui-component-inventory`
- Be descriptive but concise: `auth-flow-decisions` not `decisions-about-authentication-flow`

## Memory Lifecycle

### Create (`write_memory`)

Create a new memory when:

- Starting a new project (core memories)
- Discovering a pattern worth preserving
- Making an architectural decision
- Beginning a new task or feature
- Establishing a convention that should persist

```
Tool: write_memory
Parameters:
  name: "active-context"
  content: |
    ## Current Focus
    Implementing user authentication with OAuth2.

    ## Recent Changes
    - Set up project structure with Next.js 15
    - Configured MongoDB Atlas connection

    ## Next Steps
    - Implement login/signup pages
    - Set up JWT token handling
```

### Read (`read_memory`)

Read memories at the start of every session and when:

- Resuming work after a break
- Starting a task that may relate to past decisions
- Checking what patterns are established
- Verifying current project status

```
Tool: read_memory
Parameters:
  name: "system-patterns"
```

### Update (`edit_memory`)

Update (not replace) a memory when:

- Adding new information to existing context
- Correcting outdated details
- Marking tasks as complete
- Recording new decisions alongside existing ones

```
Tool: edit_memory
Parameters:
  name: "progress"
  content: |
    ## What Works
    - User authentication (login, signup, logout)
    - Recipe CRUD operations
    - Search with filters

    ## In Progress
    - Rating system
    - Comment moderation

    ## Known Issues
    - Session timeout not handled gracefully
```

### Delete (`delete_memory`)

Delete a memory when:

- A task is fully complete and archived
- Information has been consolidated into another memory
- The memory is no longer relevant to the project

```
Tool: delete_memory
Parameters:
  name: "task-003-deprecated-feature"
```

## Memory Content Structure Guidelines

### project-brief

```markdown
## Project Name
Kitchen Odyssey - Recipe Management Application

## Core Requirements
- User authentication and profiles
- Recipe CRUD with rich media
- Search and filtering
- Social features (comments, ratings)

## Goals
- Responsive, accessible UI
- Sub-200ms API response times
- Support 1000+ concurrent users

## Scope Boundaries
- No payment processing
- No real-time collaboration (v1)
```

### active-context

```markdown
## Current Focus
[One sentence describing the primary task]

## Recent Changes
- [Change 1 with date]
- [Change 2 with date]

## Active Decisions
- Chose [X] over [Y] because [reason]

## Blockers
- [Any blocking issues]

## Next Steps
1. [Immediate next action]
2. [Follow-up action]
```

### system-patterns

```markdown
## Architecture
[High-level architecture description]

## Design Patterns
- Repository pattern for data access
- Context providers for shared state
- Compound components for complex UI

## Component Relationships
- AuthContext wraps all protected routes
- RootLayout provides navigation and sidebar

## Conventions
- File naming: PascalCase for components, camelCase for utilities
- API routes follow REST conventions
```

### task-{id}

```markdown
## Task: [Title]
**Status:** In Progress
**Priority:** High

## Description
[What needs to be done]

## Approach
[How it will be implemented]

## Subtasks
- [x] Subtask 1
- [ ] Subtask 2
- [ ] Subtask 3

## Progress Log
### 2026-02-11
- Started implementation of feature X
- Discovered dependency on module Y
```

## Best Practices

### Session Continuity

1. **Always read core memories first**: Start every session by reading `active-context` and `progress`
2. **Update before ending**: Write session accomplishments to `active-context` and `progress` before finishing
3. **Record decisions immediately**: Don't wait — write architectural decisions to `system-patterns` as they happen
4. **Link related memories**: Reference other memory names in content (e.g., "See `system-patterns` for architecture details")

### Memory Size Considerations

- Keep individual memories focused and under 2000 words
- Split large memories into related sub-memories (e.g., `api-contracts-auth`, `api-contracts-recipes`)
- Use bullet points and tables over prose for scannability
- Remove resolved items from `active-context` — move completed work to `progress`

### Linking Related Memories

Reference other memories by name within content:

```markdown
## Authentication Decision
Chose JWT over sessions. Full rationale in `tech-context`.
Implementation tracked in `task-005-auth`.
Related patterns documented in `system-patterns` under "Auth Flow".
```

### Anti-Patterns

- **Stale memories**: Forgetting to update `active-context` leads to confusion next session
- **Duplicate information**: Store facts in one canonical memory, reference it from others
- **Overly broad memories**: A single memory covering everything becomes hard to parse
- **Missing task memories**: Not creating `task-{id}` memories means losing implementation context
- **No progress log**: Without dated entries, you can't reconstruct the timeline of decisions
