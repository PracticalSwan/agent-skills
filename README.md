<div align="center">

# Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills Count](https://img.shields.io/badge/Skills-40%2B-blue.svg)](https://github.com/copilot-skills/repository)

A curated collection of domain-specific skill definitions for GitHub Copilot, Claude Code, and Codex agents. Each skill encapsulates specialized knowledge, patterns, scripts, and references for specific technologies and domains.

[Features](#features) • [Available Skills](#available-skills) • [Skill Structure](#skill-structure) • [Getting Started](#getting-started) • [Usage](#usage) • [Contributing](#contributing)

</div>

## Overview

Copilot Skills transform how GitHub Copilot, Claude Code, and Codex agents understand and work with specific technologies. By activating relevant skills, agents gain domain expertise, apply best practices, and follow established patterns automatically.

Skills are activated automatically based on keyword matching in user prompts, enabling context-aware assistance without manual configuration.

## Features

- **Automatic Activation** - Skills trigger based on relevant keywords in your prompts
- **Domain Expertise** - Specialized knowledge for 40+ technologies and domains
- **Consistent Patterns** - Standardized structure with references, examples, and scripts
- **MCP Integration** - Many skills integrate with Model Context Protocol servers
- **Customizable** - Add project-specific skills to `.github/skills/` for team conventions
- **Dual Loading** - Workspace-specific and global skill locations

## Available Skills

### Frontend Development
- **react-development** - React 19+, hooks, TypeScript, Tailwind CSS
- **frontend-design** - Color theory, responsive design, accessibility (WCAG)
- **stitch-design** - Design systems, shadcn/ui component conversion
- **vite-development** - Vite 6+ build tooling and optimization
- **web-design-reviewer** - Visual inspection and responsive design testing

### Backend Development
- **nestjs** - NestJS framework, decorators, dependency injection
- **php-development** - PHP 8.0+, XAMPP, REST APIs, PDO
- **sql-development** - T-SQL, stored procedures, SQL Server DBA practices
- **mongodb-mongoose** - Mongoose models, aggregation pipelines, schemas

### Microsoft Technologies
- **microsoft-development** - Azure, .NET, Microsoft 365, Windows
- **azure-integrations** - Azure deployment, SWA, App Service, Bicep, GitHub Actions
- **powerbi-modeling** - Data models, DAX measures, star schemas, RLS

### Office Documents (via MCP)
- **excel-sheet** - Excel (.xlsx) manipulation via MCP server
- **powerpoint-ppt** - PowerPoint (.pptx) manipulation via MCP server
- **word-document** - Word (.docx) manipulation via MCP server

### DevOps & Tooling
- **devops-tooling** - Git workflows, shell scripting, CI/CD pipelines
- **web-testing** - Playwright testing, browser automation, DevTools integration

### Documentation & Design
- **documentation-authoring** - PRDs, specs, design docs, knowledge bases
- **documentation-automation** - JSDoc/TSDoc, linters, pre-commit hooks
- **documentation-patterns** - API docs, feature docs, templates
- **documentation-quality** - Quality standards, formatting guidelines
- **documentation-verification** - Review, validation, quality checks
- **excalidraw-diagram-generator** - Diagrams from natural language
- **canvas-design** - Design philosophy and canvas-based visual creation

### Code Quality
- **code-quality** - Refactoring, code review, self-critique workflows
- **breaking-changes-management** - Migration guides, deprecation, versioning
- **code-examples-sync** - Example verification and synchronization

### Development Workflow
- **development-workflow** - Spec-driven development, EARS notation, Git workflow
- **javascript-development** - ES2024+, async patterns, DOM manipulation
- **codexer** - Python research assistant with Context7 MCP
- **serena-usage** - Project memory, code navigation, intelligent refactoring

### Agent Delegation & Orchestration
- **agent-task-mapping** - Mapping tasks to specialized subagents
- **custom-agent-usage** - Discovering and using custom .agent.md files
- **subagent-delegation** - Core delegation patterns for utilities

### Superpowers (Workflow Skills)
- **brainstorming** - Pre-implementation design exploration
- **dispatching-parallel-agents** - Parallel task execution
- **executing-plans** - Implementation plan execution with checkpoints
- **finishing-a-development-branch** - Completion and merge decisions
- **receiving-code-review** - Code review feedback processing
- **requesting-code-review** - Pre-merge verification
- **subagent-driven-development** - Implementation with independent tasks
- **systematic-debugging** - Bug diagnosis before proposing fixes
- **test-driven-development** - TDD before implementation
- **using-git-worktrees** - Isolated feature workspace creation
- **using-superpowers** - Skill discovery and usage
- **verification-before-completion** - Pre-completion verification
- **writing-plans** - Implementation plan creation from specs
- **writing-skills** - Creating and verifying new skills

### Specialized
- **legacy-circuit-mockups** - Breadboard circuit diagrams and visual mockups
- **notion-docs** - Notion workspace management via MCP
- **notebooklm-management** - NotebookLM MCP server management

## Skill Structure

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md              # Main skill definition with activation triggers
├── LICENSE.txt           # License terms (typically MIT)
├── CHANGELOG.md          # Optional: Version history and breaking changes
├── SKILL.md.bak          # Backup of previous version
├── references/           # Domain reference documentation
│   └── *.md            # Technical references, patterns, quick guides
├── examples/            # Code examples and workflows
│   └── *.md            # Implementation examples
└── scripts/             # Utility scripts and templates
    ├── *.ps1           # PowerShell scripts
    ├── *.py            # Python scripts
    ├── *.sql           # SQL templates
    └── README.md       # Script documentation
```

### SKILL.md Format

Every skill file includes YAML frontmatter:

```yaml
---
name: skill-name
description: Comprehensive description with use cases and trigger keywords
license: Complete terms in LICENSE.txt
---
```

The description field contains activation keywords that trigger the skill when matched in user prompts.

## Getting Started

### Skill Loading Order

Skills are loaded from two locations (in order):

1. **Workspace skills**: `.github/skills/` (project-specific)
2. **Global skills**: `C:/Users/LOQ/.copilot/skills/` or `C:/Users/LOQ/.agents/skills/` (user-specific)

Workspace-specific skills override global skills when they share the same name.

### Using Skills

Simply use keywords related to your task. Copilot, Claude Code, or Codex will automatically activate relevant skills:

- "Help me refactor this React component" → Activates `react-development`
- "Create a PRD for the authentication feature" → Activates `documentation-authoring`
- "Set up Azure deployment for this Next.js app" → Activates `azure-integrations`
- "Debug failing tests before implementing the fix" → Activates `systematic-debugging`

> [!TIP]
> Use the `using-superpowers` skill to discover available skills and learn how to activate them intentionally.

## Usage

### Reading a Skill

Before editing any skill, read the `SKILL.md` file to understand:
- Activation triggers and keywords
- Domain-specific knowledge (organized by numbered Parts)
- Quick reference tables
- Code examples and patterns

### Creating a New Skill

1. Create a new directory following the `skill-name` pattern
2. Create `SKILL.md` with proper YAML frontmatter
3. Add `LICENSE.txt` (MIT recommended)
4. Create `references/` and `examples/` subdirectories as needed
5. Add `scripts/` if the skill includes utilities or templates

### Modifying an Existing Skill

1. Always read `SKILL.md` first to understand the full context
2. Create `SKILL.md.bak` backup before major changes
3. Update the `description` field if adding new trigger keywords
4. Maintain the Part-based organization structure
5. Update `CHANGELOG.md` if the skill has one
6. Update related reference files and examples as needed

### Content Guidelines

- **Be specific to the domain** - Avoid generic advice
- **Include actionable patterns** - Code snippets, templates, workflows
- **Maintain consistency** - Use similar organization across skills
- **Document MCP tools** - Include tool activation patterns for MCP-enabled skills
- **Keep examples current** - Ensure code examples use latest syntax

## MCP Server Integration

Many skills integrate with Model Context Protocol (MCP) servers for enhanced capabilities:

- `office-documents` - Word, PowerPoint, Excel MCP servers
- `notion-docs` - Notion MCP tools
- `notebooklm-management` - NotebookLM MCP server
- `serena-usage` - Serena MCP tools
- `codexer` - Context7 MCP integration

Working with MCP-enabled skills:
1. Read the skill's quick reference table for tool names
2. Activate tool groups before using (e.g., `activate_document_creation_and_styling()`)
3. Follow MCP-specific parameter structures
4. Handle MCP server errors gracefully

## Script Files

Skills include automation scripts:

- **PowerShell (.ps1)** - Windows-native automation
- **Python (.py)** - Cross-platform utilities
- **SQL (.sql)** - Database scaffolding templates
- **Excalidraw (.excalidraw)** - JSON diagram templates

Example script usage:
```bash
# PowerShell
powershell -File script.ps1

# Python
python script.py
```

## File Encoding

All skill files use UTF-8 without BOM:
- `.md` files - Documentation
- `.ps1`, `.py`, `.sql` files - Scripts and templates
- `.excalidraw` files - Diagram templates (JSON)

## Contributing

We welcome contributions! When adding or modifying skills:

1. Follow the established skill structure
2. Include comprehensive descriptions with trigger keywords
3. Add a `LICENSE.txt` file (MIT recommended)
4. Provide relevant examples and references
5. Test activation triggers thoroughly

Contributions should enhance agent capabilities in specific domains while maintaining consistency with existing skills.
