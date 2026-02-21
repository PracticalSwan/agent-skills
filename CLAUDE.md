# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Overview

This is a **Copilot Skills repository** - a collection of domain-specific skill definitions for GitHub Copilot/Claude Code agents. Each skill directory contains specialized knowledge, patterns, scripts, and references for a specific technology or domain.

### Repository Structure

Each skill follows a consistent structure:
```
skill-name/
├── SKILL.md              # Main skill definition with activation triggers
├── LICENSE.txt           # License terms
├── CHANGELOG.md          # Optional: version history and breaking changes
├── SKILL.md.bak          # Backup of previous version
├── references/           # Domain reference documentation
│   └── *.md             # Technical references, patterns, quick guides
├── examples/            # Code examples and workflows
│   └── *.md             # Implementation examples
└── scripts/             # Utility scripts and templates
    ├── *.ps1            # PowerShell scripts
    ├── *.py             # Python scripts
    ├── *.sql            # SQL templates
    └── README.md        # Script documentation
```

### Skill Path Resolution

Skills are loaded from two locations (in order):
1. **Workspace skills**: `.github/skills/` (project-specific)
2. **Global skills**: `C:/Users/LOQ/.agents/skills/` or `C:/Users/LOQ/.copilot/skills/` (user-specific)

---

## Working with Skills

### Reading a Skill

Before editing any skill, **read the SKILL.md file first**. Each skill contains:
- YAML frontmatter with `name`, `description`, `license`
- Activation conditions and trigger keywords
- Domain-specific knowledge organized by "Parts"
- Quick reference tables
- Code examples and patterns

### SKILL.md Format

Every skill file follows this structure:

```yaml
---
name: skill-name
description: [Comprehensive description with use cases and trigger keywords]
license: Complete terms in LICENSE.txt
---
```

The skill content is organized into numbered Parts (Part 1, Part 2, etc.) covering different aspects of the domain.

### Activation Triggers

Skills are activated by keyword matching in user prompts. The `description` field in YAML frontmatter contains the trigger keywords. When editing skills, ensure:
- New trigger keywords are added to the `description` field
- Related technologies are mentioned
- Use cases are clearly described

---

## Common Development Tasks

### Adding a New Skill

1. Create a new directory following the skill-name pattern
2. Create SKILL.md with proper YAML frontmatter
3. Add LICENSE.txt (MIT recommended)
4. Create references/ and examples/ subdirectories as needed
5. Add scripts/ if the skill includes utilities or templates

### Modifying an Existing Skill

1. **Always read SKILL.md first** to understand the full context
2. Create SKILL.md.bak backup before major changes
3. Update the `description` field if adding new trigger keywords
4. Maintain the Part-based organization structure
5. Update CHANGELOG.md if the skill has one
6. Update related reference files and examples as needed

### Skill Content Guidelines

- **Be specific to the domain** - Avoid generic advice that applies everywhere
- **Include actionable patterns** - Code snippets, templates, workflows
- **Maintain consistency** - Use similar organization across skills
- **Document MCP tools** - For skills using MCP servers, include tool activation patterns and quick reference tables
- **Keep examples current** - Ensure code examples use latest syntax and patterns

---

## Skill Categories

### AI & Claude Platform
- `claude-developer-platform` - Claude API, Anthropic SDK, AI/LLM integration

### Frontend Development
- `react-development` - React 19+, hooks, TypeScript, Tailwind CSS
- `frontend-design` - Color theory, responsive design, accessibility
- `stitch-design` - Design systems, shadcn/ui components
- `vite-development` - Vite 6+ build tooling
- `web-design-reviewer` - Visual inspection, responsive design testing

### Backend Development
- `nestjs` - NestJS framework, decorators, dependency injection
- `php-development` - PHP 8.0+, XAMPP, REST APIs, PDO
- `sql-development` - T-SQL, stored procedures, DBA practices
- `mongodb-mongoose` - Mongoose models, aggregation, schemas

### Microsoft Technologies
- `microsoft-development` - Azure, .NET, Microsoft 365, Windows
- `powerbi-modeling` - Data models, DAX measures, star schemas
- `azure-integrations` - SWA, App Service, Bicep, GitHub Actions

### Office Documents (via MCP)
- `excel-sheet` - Excel (.xlsx) manipulation via MCP server
- `powerpoint-ppt` - PowerPoint (.pptx) manipulation via MCP server
- `word-document` - Word (.docx) manipulation via MCP server

### DevOps & Tooling
- `devops-tooling` - Git workflows, shell scripting, CI/CD
- `web-testing` - Playwright testing, browser automation

### Documentation & Design
- `documentation-authoring` - PRDs, specs, design docs
- `documentation-automation` - JSDoc/TSDoc, linters
- `documentation-patterns` - Templates and patterns
- `documentation-quality` - Quality standards, formatting guidelines
- `documentation-verification` - Verification, validation, quality checks
- `excalidraw-diagram-generator` - Diagram generation
- `canvas-design` - Design philosophy, visual creation

### Code Quality
- `code-quality` - Refactoring, code review patterns
- `breaking-changes-management` - Migration guides, versioning
- `code-examples-sync` - Example verification

### Development Workflow
- `development-workflow` - Spec-driven development, EARS notation
- `javascript-development` - ES2024+, async patterns, Node.js
- `codexer` - Python research assistant with Context7 MCP
- `serena-usage` - Project memory, code navigation

### Agent Delegation & Orchestration
- `agent-task-mapping` - Mapping tasks to specialized subagents
- `custom-agent-usage` - Discovering and using custom .agent.md files
- `subagent-delegation` - Core delegation patterns for boilerplate and utilities

### Superpowers (Workflow Skills)
- `brainstorming` - Pre-implementation design exploration
- `dispatching-parallel-agents` - Parallel task execution
- `executing-plans` - Implementation plan execution with checkpoints
- `finishing-a-development-branch` - Completion and merge decisions
- `receiving-code-review` - Code review feedback processing
- `requesting-code-review` - Pre-merge code review verification
- `subagent-driven-development` - Implementation with independent tasks
- `systematic-debugging` - Bug diagnosis before proposing fixes
- `test-driven-development` - TDD before implementation code
- `using-git-worktrees` - Isolated feature workspace creation
- `using-superpowers` - Skill discovery and usage
- `verification-before-completion` - Pre-completion verification
- `writing-plans` - Implementation plan creation from specs
- `writing-skills` - Creating and verifying new skills

### Specialized
- `legacy-circuit-mockups` - Breadboard circuit diagrams
- `notion-docs` - Notion workspace management
- `notebooklm-management` - NotebookLM MCP server management

---

## Script Files

Scripts are included in skills for automation and scaffolding:

### PowerShell Scripts (.ps1)
- Windows-native automation
- Common in `react-development`, `azure-integrations`
- Use `powershell -File script.ps1` to run

### Python Scripts (.py)
- Cross-platform utilities
- Common in `canvas-design`, `codexer`, `office-documents`
- Use `python script.py` to run

### SQL Templates (.sql)
- Database scaffolding templates
- Common in `sql-development`
- Stored procedure templates with standard patterns

### Excalidraw Templates (.excalidraw)
- Diagram templates in JSON format
- Located in `excalidraw-diagram-generator/templates/`
- Flowcharts, sequence diagrams, ER diagrams, mind maps

---

## MCP Server Integration

Many skills integrate with MCP (Model Context Protocol) servers:

### Skills Using MCP Tools
- `office-documents` - Word, PowerPoint, Excel MCP servers
- `notion-docs` - Notion MCP tools
- `notebooklm-management` - NotebookLM MCP server
- `serena-usage` - Serena MCP tools
- `codexer` - Context7 MCP integration

### MCP Tool Activation Patterns

When working with MCP-enabled skills:
1. Read the skill's quick reference table for tool names
2. Activate tool groups before using (e.g., `activate_document_creation_and_styling()`)
3. Follow MCP-specific parameter structures
4. Handle MCP server errors gracefully

---

## File Encoding Standards

**MUST:**
- All skill files (.md): UTF-8 without BOM
- Scripts (.ps1, .py, .sql): UTF-8 without BOM
- Excalidraw templates (.excalidraw): UTF-8 (JSON)

---

## License

Each skill directory contains its own LICENSE.txt file. Most skills use MIT License. When contributing:
- Preserve existing license files
- Add LICENSE.txt to new skills
- Include license reference in YAML frontmatter

---

## Quick Reference for Common Operations

| Task | Command/Action |
|------|----------------|
| Find skill by keyword | Search SKILL.md description fields |
| View skill structure | List skill directory contents |
| Run PowerShell script | `powershell -File script.ps1` |
| Run Python script | `python script.py` |
| Create new skill | Copy structure from existing skill |
| Backup before edit | Copy SKILL.md to SKILL.md.bak |
| Update activation keywords | Edit `description` in YAML frontmatter |
