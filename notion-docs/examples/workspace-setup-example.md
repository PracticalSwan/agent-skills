# Example: Dev Team Notion Workspace Setup

Complete walkthrough for setting up a development team workspace in Notion using MCP tools.
Creates a project tracker, documentation wiki, meeting notes database, and decision log.

---

## 1. Create the Team Hub Page

Start with a top-level page that acts as the workspace root.

```json
// Tool: notion-create-pages
{
  "pages": [
    {
      "properties": { "title": "Engineering Team Hub" },
      "content": "# Engineering Team Hub\n\nCentral workspace for the engineering team.\n\n---\n\n## Quick Links\n\n- **Project Tracker** — All active projects and tasks\n- **Documentation Wiki** — Technical docs and guides\n- **Meeting Notes** — Weekly syncs and retrospectives\n- **Decision Log** — Architecture and process decisions"
    }
  ]
}
```

Save the returned `page_id` — it will be the parent for all databases below.

---

## 2. Create the Project Tracker Database

A full-featured task/issue tracker with status, priority, assignee, sprint, and type.

```json
// Tool: notion-create-database
{
  "parent": { "page_id": "<hub-page-id>" },
  "title": [{ "type": "text", "text": { "content": "Project Tracker" } }],
  "properties": {
    "Task": {
      "type": "title",
      "title": {}
    },
    "Status": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Backlog", "color": "default" },
          { "name": "To Do", "color": "blue" },
          { "name": "In Progress", "color": "yellow" },
          { "name": "In Review", "color": "purple" },
          { "name": "Done", "color": "green" },
          { "name": "Blocked", "color": "red" }
        ]
      }
    },
    "Priority": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Critical", "color": "red" },
          { "name": "High", "color": "orange" },
          { "name": "Medium", "color": "yellow" },
          { "name": "Low", "color": "green" }
        ]
      }
    },
    "Assignee": {
      "type": "people",
      "people": {}
    },
    "Sprint": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Sprint 1", "color": "blue" },
          { "name": "Sprint 2", "color": "purple" },
          { "name": "Sprint 3", "color": "pink" },
          { "name": "Backlog", "color": "default" }
        ]
      }
    },
    "Type": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Feature", "color": "blue" },
          { "name": "Bug", "color": "red" },
          { "name": "Tech Debt", "color": "orange" },
          { "name": "Documentation", "color": "gray" },
          { "name": "Research", "color": "purple" }
        ]
      }
    },
    "Story Points": {
      "type": "number",
      "number": { "format": "number" }
    },
    "Due Date": {
      "type": "date",
      "date": {}
    },
    "Tags": {
      "type": "multi_select",
      "multi_select": {
        "options": [
          { "name": "frontend", "color": "blue" },
          { "name": "backend", "color": "green" },
          { "name": "database", "color": "brown" },
          { "name": "infrastructure", "color": "gray" },
          { "name": "testing", "color": "yellow" }
        ]
      }
    },
    "ID": {
      "type": "unique_id",
      "unique_id": { "prefix": "ENG" }
    }
  }
}
```

### Add Sample Tasks

After creation, use the `data_source_id` from the response to add pages.

```json
// Tool: notion-create-pages
{
  "parent": { "data_source_id": "<tracker-data-source-id>" },
  "pages": [
    {
      "properties": {
        "Task": "Set up CI/CD pipeline",
        "Status": "To Do",
        "Priority": "High",
        "Sprint": "Sprint 1",
        "Type": "Feature",
        "Story Points": 5,
        "Tags": "infrastructure",
        "date:Due Date:start": "2025-02-20",
        "date:Due Date:is_datetime": 0
      },
      "content": "## Description\n\nConfigure GitHub Actions for automated testing and deployment.\n\n## Acceptance Criteria\n\n- [ ] Tests run on every PR\n- [ ] Auto-deploy to staging on merge to develop\n- [ ] Auto-deploy to production on merge to main"
    },
    {
      "properties": {
        "Task": "Implement user authentication",
        "Status": "In Progress",
        "Priority": "Critical",
        "Sprint": "Sprint 1",
        "Type": "Feature",
        "Story Points": 8,
        "Tags": "backend, frontend",
        "date:Due Date:start": "2025-02-18",
        "date:Due Date:is_datetime": 0
      },
      "content": "## Description\n\nJWT-based login and registration flow.\n\n## Tasks\n\n- [x] Design auth API endpoints\n- [x] Implement backend routes\n- [ ] Build login/signup UI\n- [ ] Add token refresh logic\n- [ ] Write integration tests"
    },
    {
      "properties": {
        "Task": "Fix mobile navigation overflow",
        "Status": "To Do",
        "Priority": "Medium",
        "Sprint": "Sprint 1",
        "Type": "Bug",
        "Story Points": 2,
        "Tags": "frontend"
      },
      "content": "## Bug Report\n\nNavigation menu overflows on screens narrower than 375px.\n\n## Steps to Reproduce\n\n1. Open app on iPhone SE\n2. Tap hamburger menu\n3. Observe horizontal scroll\n\n## Expected\n\nMenu fits within viewport width."
    }
  ]
}
```

---

## 3. Create the Documentation Wiki

A page-based wiki for technical documentation.

```json
// Tool: notion-create-pages
{
  "parent": { "page_id": "<hub-page-id>" },
  "pages": [
    {
      "properties": { "title": "Documentation Wiki" },
      "content": "# Documentation Wiki\n\n> ℹ️ Central technical documentation for the engineering team.\n\n---\n\n## Sections\n\n- **Architecture** — System design and component diagrams\n- **API Reference** — REST endpoint documentation\n- **Getting Started** — Onboarding and local setup\n- **Deployment** — CI/CD and release procedures\n- **Coding Standards** — Style guides and conventions"
    }
  ]
}
```

### Add Wiki Sub-Pages

Use the wiki page ID as the parent.

```json
// Tool: notion-create-pages
{
  "parent": { "page_id": "<wiki-page-id>" },
  "pages": [
    {
      "properties": { "title": "Architecture Overview" },
      "content": "# Architecture Overview\n\n## System Diagram\n\n| Layer | Technology | Description |\n|-------|-----------|-------------|\n| Frontend | React 19 + Vite | SPA with Tailwind CSS |\n| API | Next.js 15 | App Router REST endpoints |\n| Database | MongoDB Atlas | Document store |\n| Auth | JWT + bcrypt | Token-based authentication |\n| Hosting | Azure | Static Web Apps + App Service |\n\n---\n\n## Data Flow\n\n1. Client sends HTTP request\n2. Next.js API route handles request\n3. Mongoose model queries MongoDB\n4. Response returns through the chain\n\n---\n\n## Key Design Decisions\n\n▶ Why MongoDB over PostgreSQL?\n\tFlexible schema suits our rapidly evolving data model.\n\tNested document structure maps naturally to our domain.\n\n▶ Why Next.js for API?\n\tUnified deployment, built-in API routes, and server components for future SSR."
    },
    {
      "properties": { "title": "Getting Started" },
      "content": "# Getting Started\n\n## Prerequisites\n\n- Node.js 18+\n- pnpm (recommended) or npm\n- Git\n- MongoDB Atlas account (or local MongoDB)\n\n## Setup\n\n```bash\ngit clone https://github.com/team/project.git\ncd project\npnpm install\ncp .env.example .env.local\npnpm dev\n```\n\n## Environment Variables\n\n| Variable | Description | Example |\n|----------|-------------|---------|\n| `MONGODB_URI` | Atlas connection string | `mongodb+srv://...` |\n| `JWT_SECRET` | Token signing key | `your-secret-key` |\n| `NEXT_PUBLIC_API_URL` | API base URL | `http://localhost:3000` |\n\n---\n\n## Verification\n\nAfter starting the dev server:\n\n- [ ] App loads at http://localhost:5173\n- [ ] API responds at http://localhost:3000/api\n- [ ] Database connection succeeds (check terminal logs)"
    },
    {
      "properties": { "title": "Coding Standards" },
      "content": "# Coding Standards\n\n## Language & Framework\n\n- **JavaScript/TypeScript** with ES2022+ features\n- **React 19** functional components only\n- **Tailwind CSS** for styling (no CSS modules)\n\n## Naming Conventions\n\n| Item | Convention | Example |\n|------|-----------|----------|\n| Components | PascalCase | `UserProfile.jsx` |\n| Hooks | camelCase, `use` prefix | `useAuth.js` |\n| Utilities | camelCase | `formatDate.js` |\n| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |\n| API routes | kebab-case | `/api/user-profile` |\n\n## Git Workflow\n\n- Branch from `develop`\n- PRs require 1 approval\n- Squash merge to `develop`\n- Conventional commits required"
    }
  ]
}
```

---

## 4. Create the Meeting Notes Database

A database to store recurring meeting notes with date, type, and attendees.

```json
// Tool: notion-create-database
{
  "parent": { "page_id": "<hub-page-id>" },
  "title": [{ "type": "text", "text": { "content": "Meeting Notes" } }],
  "properties": {
    "Meeting": {
      "type": "title",
      "title": {}
    },
    "Date": {
      "type": "date",
      "date": {}
    },
    "Type": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Weekly Sync", "color": "blue" },
          { "name": "Sprint Planning", "color": "purple" },
          { "name": "Sprint Review", "color": "green" },
          { "name": "Retrospective", "color": "orange" },
          { "name": "Ad Hoc", "color": "default" },
          { "name": "1-on-1", "color": "pink" }
        ]
      }
    },
    "Attendees": {
      "type": "people",
      "people": {}
    },
    "Action Items": {
      "type": "number",
      "number": { "format": "number" }
    }
  }
}
```

### Add a Sample Meeting Entry

```json
// Tool: notion-create-pages
{
  "parent": { "data_source_id": "<meetings-data-source-id>" },
  "pages": [
    {
      "properties": {
        "Meeting": "Sprint 1 Planning",
        "date:Date:start": "2025-02-10",
        "date:Date:is_datetime": 0,
        "Type": "Sprint Planning",
        "Action Items": 4
      },
      "content": "## Agenda\n\n1. Review backlog priorities\n2. Assign sprint tasks\n3. Estimate story points\n4. Identify risks and blockers\n\n---\n\n## Discussion\n\n> 📝 Key decisions from planning session\n\n- Agreed to prioritize authentication and CI/CD\n- Deferred analytics dashboard to Sprint 2\n- Mobile bug fix fits within sprint capacity\n\n---\n\n## Action Items\n\n- [ ] Create sprint board view — **Owner:** PM\n- [ ] Set up staging environment — **Owner:** DevOps\n- [ ] Draft auth API spec — **Owner:** Backend Lead\n- [ ] Share design mockups — **Owner:** Designer"
    }
  ]
}
```

---

## 5. Create the Decision Log Database

Track architectural and process decisions with context.

```json
// Tool: notion-create-database
{
  "parent": { "page_id": "<hub-page-id>" },
  "title": [{ "type": "text", "text": { "content": "Decision Log" } }],
  "properties": {
    "Decision": {
      "type": "title",
      "title": {}
    },
    "Status": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Proposed", "color": "yellow" },
          { "name": "Accepted", "color": "green" },
          { "name": "Superseded", "color": "gray" },
          { "name": "Rejected", "color": "red" }
        ]
      }
    },
    "Category": {
      "type": "select",
      "select": {
        "options": [
          { "name": "Architecture", "color": "blue" },
          { "name": "Technology", "color": "purple" },
          { "name": "Process", "color": "orange" },
          { "name": "Security", "color": "red" },
          { "name": "Infrastructure", "color": "gray" }
        ]
      }
    },
    "Date Decided": {
      "type": "date",
      "date": {}
    },
    "Decided By": {
      "type": "people",
      "people": {}
    },
    "ID": {
      "type": "unique_id",
      "unique_id": { "prefix": "ADR" }
    }
  }
}
```

### Add Sample Decisions

```json
// Tool: notion-create-pages
{
  "parent": { "data_source_id": "<decisions-data-source-id>" },
  "pages": [
    {
      "properties": {
        "Decision": "Use MongoDB Atlas for primary datastore",
        "Status": "Accepted",
        "Category": "Technology",
        "date:Date Decided:start": "2025-01-15",
        "date:Date Decided:is_datetime": 0
      },
      "content": "## Context\n\nWe need a database for our full-stack application. The data model is evolving rapidly with nested structures.\n\n## Options Considered\n\n| Option | Pros | Cons |\n|--------|------|------|\n| MongoDB Atlas | Flexible schema, native JSON, managed service | No joins, eventual consistency |\n| PostgreSQL | ACID, mature, relational | Rigid schema during rapid iteration |\n| DynamoDB | Serverless, auto-scaling | Vendor lock-in, complex query patterns |\n\n## Decision\n\nAdopt MongoDB Atlas as the primary datastore.\n\n## Rationale\n\n- Schema flexibility matches our evolving data model\n- Mongoose ODM provides good validation layer\n- Atlas free tier sufficient for development\n- Team has prior MongoDB experience\n\n## Consequences\n\n- Must design aggregation pipelines for complex queries\n- Need to handle schema migrations manually\n- Will use Mongoose for schema validation at the application layer"
    },
    {
      "properties": {
        "Decision": "Adopt conventional commits for all repositories",
        "Status": "Accepted",
        "Category": "Process",
        "date:Date Decided:start": "2025-01-20",
        "date:Date Decided:is_datetime": 0
      },
      "content": "## Context\n\nCommit messages are inconsistent across the team, making changelogs and release notes difficult to generate.\n\n## Decision\n\nAll repositories must use [Conventional Commits](https://www.conventionalcommits.org/) specification.\n\n## Format\n\n```\ntype(scope): description\n\n[optional body]\n[optional footer]\n```\n\n## Types\n\n- `feat` — new feature\n- `fix` — bug fix\n- `docs` — documentation changes\n- `refactor` — code restructuring\n- `test` — adding/updating tests\n- `chore` — maintenance tasks\n\n## Enforcement\n\n- commitlint checks in CI\n- Husky pre-commit hooks locally\n- PR titles must follow the convention"
    }
  ]
}
```

---

## Complete Setup Summary

After executing all the above MCP calls, the workspace structure looks like:

```
Engineering Team Hub
├── Project Tracker (database)
│   ├── ENG-1: Set up CI/CD pipeline
│   ├── ENG-2: Implement user authentication
│   └── ENG-3: Fix mobile navigation overflow
├── Documentation Wiki (page)
│   ├── Architecture Overview
│   ├── Getting Started
│   └── Coding Standards
├── Meeting Notes (database)
│   └── Sprint 1 Planning
└── Decision Log (database)
    ├── ADR-1: Use MongoDB Atlas for primary datastore
    └── ADR-2: Adopt conventional commits for all repositories
```

### Tool Call Sequence

| Step | MCP Tool | Creates |
|------|----------|---------|
| 1 | `notion-create-pages` | Hub page |
| 2 | `notion-create-database` | Project Tracker |
| 3 | `notion-create-pages` | Sample tasks (3 pages) |
| 4 | `notion-create-pages` | Documentation Wiki root |
| 5 | `notion-create-pages` | Wiki sub-pages (3 pages) |
| 6 | `notion-create-database` | Meeting Notes |
| 7 | `notion-create-pages` | Sample meeting (1 page) |
| 8 | `notion-create-database` | Decision Log |
| 9 | `notion-create-pages` | Sample decisions (2 pages) |

**Total:** 3 database creations + 6 page creation calls = 9 MCP tool invocations.

### Tips

- **Fetch after creating databases** to get the `data_source_id` (from `<data-source url="collection://...">` tags) needed for adding pages.
- **Use `notion-search`** to find existing pages/databases before creating duplicates.
- **Batch page creation** — the `create-pages` tool accepts up to 100 pages per call.
- **Properties named `id` or `url`** must use the `userDefined:` prefix (e.g., `"userDefined:URL"`).
- **Date properties** use expanded format: `"date:Due Date:start"`, `"date:Due Date:end"`, `"date:Due Date:is_datetime"`.
- **Checkbox values** use `"__YES__"` and `"__NO__"` strings, not booleans.
