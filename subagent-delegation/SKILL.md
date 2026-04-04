---
name: subagent-delegation
description: Delegate routine work to subagents — boilerplate generation, data transformation, file analysis, documentation drafting. Use when splitting tasks into independent subtasks for parallel subagent execution.
license: Complete terms in LICENSE.txt
---
# Subagent Delegation Patterns

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.codex/skills/` for Codex or `C:/Users/LOQ/.agents/skills/` for the shared mirror

## Activation Conditions

Activate this skill when:
- Creating repetitive code structures or boilerplate
- Performing data transformation tasks
- Analyzing codebase for patterns or information
- Generating documentation from existing code
- Creating simple utility functions
- Breaking down complex features into manageable subtasks

## Core Delegation Patterns

See [Delegation Patterns](./references/patterns.md) for detailed examples of:
- Boilerplate generation (API routes, CRUD operations, component structures)
- Data transformations between formats
- File analysis and pattern extraction
- Documentation generation from code
- Utility function creation

## Examples & Scripts

- [Delegation Pattern Examples](./examples/delegation-patterns-examples.md) — Code examples of common delegation patterns
- [Delegation Template](./scripts/delegation-template.js) — JavaScript template for structuring delegation calls

## Integration Workflow

For delegating tasks to subagents, follow this 5-step process:

- **Step 1: Plan** - Analyze problem, design solution, identify routine subtasks
- **Step 2: Delegate** - Use `runSubagent` for routine or repetitive work
- **Step 3: Review** - Check output for correctness, completeness, integration compatibility
- **Step 4: Integrate** - Incorporate output into codebase, handle conflicts
- **Step 5: Validate** - Test integrated code, debug issues, ensure quality

## Quality Control

Before integrating subagent results, verify:
- [ ] Code follows project conventions (style, naming, structure)
- [ ] Matches specified interfaces and contracts
- [ ] Includes necessary error handling
- [ ] Has appropriate comments/documentation
- [ ] No security vulnerabilities or obvious performance issues
- [ ] Compatible with existing codebase (imports, dependencies)

## Anti-Patterns

- ❌ Over-delegation: Don't delegate critical security logic or core business rules
- ❌ Vague instructions: Always provide specific, actionable prompts
- ❌ No integration plan: Have clear plan for using subagent output
- ❌ Delegating planning: Never ask subagents to decide what to do

## Combining with Sequential Thinking

For complex tasks, use Sequential Thinking first to plan architecture, then delegate routine parts:

```javascript
// Use Sequential Thinking to plan
mcp_sequentialthi_sequentialthinking({
  thought: "Breaking down feature...identifying repetitive CRUD for delegation",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true
})

// Then delegate boilerplate
runSubagent({
  description: "Generate CRUD API",
  prompt: "Create CRUD functions matching data model..."
})

// Main agent implements core logic
```


---

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:subagent-delegation` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py subagent-delegation` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks an equivalent tool surface, use the bundled scripts, standard shell or editor tooling, and the manual workflow already described in this skill.
- Treat local verification as the fallback evidence path before closing the task.

<!-- MCP:END -->

## Related Skills
| Skill | Relationship |
|-------|-------------|
| [agent-task-mapping](../agent-task-mapping/SKILL.md) | Map tasks to the right specialist agent |
| [custom-agent-usage](../custom-agent-usage/SKILL.md) | Discover and invoke custom .agent.md agents |
