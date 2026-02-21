/**
 * Notion content templates for use with Notion MCP tools.
 *
 * Each function returns a structured object with `properties` and `content`
 * fields ready for Notion MCP `create-pages` calls.
 */

function createMeetingNotes(title, attendees = []) {
  const date = new Date().toISOString().split("T")[0];
  const attendeeList = attendees.length
    ? attendees.map((a) => `- ${a}`).join("\n")
    : "- *(add attendees)*";

  const content = `## Details

**Date:** ${date}
**Attendees:**
${attendeeList}

---

## Agenda

1. *(Topic 1)*
2. *(Topic 2)*
3. *(Topic 3)*

---

## Discussion Notes

> 📝 Capture key points from the meeting

*(Add notes here)*

---

## Action Items

- [ ] *(Action item 1)* — **Owner:** TBD — **Due:** TBD
- [ ] *(Action item 2)* — **Owner:** TBD — **Due:** TBD
- [ ] *(Action item 3)* — **Owner:** TBD — **Due:** TBD

---

## Decisions Made

| Decision | Rationale | Owner |
|----------|-----------|-------|
| *(Decision 1)* | *(Why)* | *(Who)* |

---

## Follow-Up

▶ Items for next meeting
\tCarry-over items and topics to revisit.`;

  return {
    properties: { title },
    content,
  };
}

function createProjectBrief(projectName) {
  const date = new Date().toISOString().split("T")[0];

  const content = `## Overview

> 💡 Brief summary of what this project is and why it exists.

*(Describe the project purpose and goals here)*

---

## Problem Statement

What problem does this project solve? Who is affected?

*(Define the problem clearly)*

---

## Goals & Success Criteria

### Goals
1. *(Primary goal)*
2. *(Secondary goal)*
3. *(Tertiary goal)*

### Success Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| *(Metric 1)* | *(Target)* | *(Method)* |
| *(Metric 2)* | *(Target)* | *(Method)* |

---

## Scope

### In Scope
- *(Feature/deliverable 1)*
- *(Feature/deliverable 2)*
- *(Feature/deliverable 3)*

### Out of Scope
- *(Explicitly excluded item 1)*
- *(Explicitly excluded item 2)*

---

## Timeline

| Phase | Start | End | Deliverables |
|-------|-------|-----|--------------|
| Discovery | ${date} | TBD | Requirements doc |
| Design | TBD | TBD | Design specs |
| Implementation | TBD | TBD | Working software |
| Testing | TBD | TBD | Test reports |
| Launch | TBD | TBD | Production release |

---

## Team

| Role | Person | Responsibilities |
|------|--------|-----------------|
| Project Lead | TBD | Overall coordination |
| Developer | TBD | Implementation |
| Designer | TBD | UI/UX design |
| QA | TBD | Testing & validation |

---

## Technical Approach

▶ Architecture Overview
\t*(High-level architecture description)*

▶ Technology Stack
\t*(List of technologies and frameworks)*

▶ Key Risks & Mitigations
\t| Risk | Impact | Mitigation |
\t|------|--------|------------|
\t| *(Risk 1)* | High | *(Mitigation)* |

---

## References

- *(Link to related documents)*
- *(Link to design files)*
- *(Link to prior art)*`;

  return {
    properties: { title: `${projectName} — Project Brief` },
    content,
  };
}

function createSprintBoard(sprintNumber) {
  const today = new Date();
  const startDate = today.toISOString().split("T")[0];
  const endDate = new Date(today.getTime() + 14 * 24 * 60 * 60 * 1000)
    .toISOString()
    .split("T")[0];

  const content = `## Sprint Info

**Sprint:** ${sprintNumber}
**Duration:** ${startDate} → ${endDate}
**Goal:** *(Define the sprint goal)*

---

## Sprint Goal

> 🎯 What the team commits to achieving this sprint.

*(Describe the sprint goal in 1-2 sentences)*

---

## Capacity

| Team Member | Available Days | Focus Area |
|-------------|----------------|------------|
| *(Name)* | 10 | *(Area)* |
| *(Name)* | 10 | *(Area)* |
| *(Name)* | 8 | *(Area)* |

**Total Capacity:** *(X)* story points

---

## Sprint Backlog

### 🔴 High Priority
- [ ] *(Task 1)* — **SP:** 5 — **Assignee:** TBD
- [ ] *(Task 2)* — **SP:** 3 — **Assignee:** TBD

### 🟡 Medium Priority
- [ ] *(Task 3)* — **SP:** 3 — **Assignee:** TBD
- [ ] *(Task 4)* — **SP:** 2 — **Assignee:** TBD

### 🟢 Low Priority
- [ ] *(Task 5)* — **SP:** 1 — **Assignee:** TBD

---

## Daily Standup Log

### ${startDate}
| Person | Yesterday | Today | Blockers |
|--------|-----------|-------|----------|
| *(Name)* | — | *(Plan)* | None |

---

## Sprint Review

▶ Demo Notes
\t*(Record what was demonstrated)*

▶ Stakeholder Feedback
\t*(Capture feedback from stakeholders)*

---

## Sprint Retrospective

### What Went Well
- *(Item)*

### What Could Improve
- *(Item)*

### Action Items
- [ ] *(Action)* — **Owner:** TBD`;

  return {
    properties: { title: `Sprint ${sprintNumber}` },
    content,
  };
}

function createDocWiki(projectName) {
  const content = `## About

> ℹ️ Central documentation hub for **${projectName}**.

This wiki contains all technical documentation, guides, and references for the project.
Use the sidebar or links below to navigate.

---

## Quick Links

- **Getting Started** — Setup guide for new team members
- **Architecture** — System design and component overview
- **API Reference** — Endpoint documentation
- **Deployment** — CI/CD and release process
- **Contributing** — Code standards and PR workflow

---

## Getting Started

### Prerequisites
- Node.js 18+
- Package manager (npm / pnpm)
- Git
- *(Additional requirements)*

### Local Setup
1. Clone the repository
2. Install dependencies
3. Configure environment variables
4. Start the development server

▶ Detailed Setup Steps
\t\`\`\`bash
\tgit clone https://github.com/org/${projectName.toLowerCase().replace(/\s+/g, "-")}.git
\tcd ${projectName.toLowerCase().replace(/\s+/g, "-")}
\tnpm install
\tcp .env.example .env.local
\tnpm run dev
\t\`\`\`

---

## Architecture

### System Overview
*(High-level description of the system architecture)*

### Component Diagram

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | React + Vite | User interface |
| API | Next.js API Routes | REST endpoints |
| Database | MongoDB Atlas | Data persistence |
| Auth | JWT | Authentication |

▶ Data Flow
\t1. Client sends request to API
\t2. API validates and processes
\t3. Database operations execute
\t4. Response returned to client

---

## API Reference

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| \`/api/auth/login\` | **POST** | User login |
| \`/api/auth/signup\` | **POST** | User registration |
| \`/api/auth/me\` | **GET** | Current user profile |

### Resources
| Endpoint | Method | Description |
|----------|--------|-------------|
| \`/api/items\` | **GET** | List all items |
| \`/api/items/:id\` | **GET** | Get item by ID |
| \`/api/items\` | **POST** | Create new item |
| \`/api/items/:id\` | **PUT** | Update item |
| \`/api/items/:id\` | **DELETE** | Delete item |

---

## Deployment

### Environments
| Environment | URL | Branch | Auto-deploy |
|-------------|-----|--------|------------|
| Development | localhost:3000 | feature/* | — |
| Staging | staging.example.com | develop | Yes |
| Production | app.example.com | main | Yes |

### Release Process
1. Merge feature branch into \`develop\`
2. Verify on staging
3. Create release PR to \`main\`
4. Production deployment triggers automatically

---

## Contributing

### Branch Naming
- \`feature/description\` — New features
- \`fix/description\` — Bug fixes
- \`docs/description\` — Documentation updates

### Commit Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- \`feat:\` new feature
- \`fix:\` bug fix
- \`docs:\` documentation
- \`refactor:\` code refactoring
- \`test:\` tests

### Pull Request Checklist
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Changelog entry added`;

  return {
    properties: { title: `${projectName} Wiki` },
    content,
  };
}

module.exports = {
  createMeetingNotes,
  createProjectBrief,
  createSprintBoard,
  createDocWiki,
};
