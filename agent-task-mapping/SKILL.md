---
name: agent-task-mapping
description: Map tasks to specialist agents. Use when choosing which agent for a job, comparing agent capabilities, or routing to React/Next.js/Playwright/docs/code-quality experts. Keywords: which agent, best agent for this, delegate to expert, agent capability mapping.
license: Complete terms in LICENSE.txt
---

# Agent Task Mapping

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.copilot/skills/`

## Activation Conditions

Use this skill when:
- Determining which specialized agent to delegate a task to
- Reviewing agent capabilities and expertise areas
- Trying to match a specific task to an appropriate specialist
- Needing quick reference for available agents and their purposes

## Available Agents

See [Agent Details](./references/agent-details.md) for comprehensive information about each agent:
- Description and specialization areas
- When to use each agent
- Typical tasks handled by each

## Examples & Scripts

- [Delegation Examples](./examples/delegation-example.md) — Code examples for delegating to different agents
- [Agent Discovery Script](./scripts/agent-discovery.js) — Node.js script to discover available agents

## Quick Reference

| Agent Name | Best For |
|------------|-----------|
| Code Explainer | Analyzing and documenting existing code |
| UI Designer | UI/UX improvements and design implementations |
| Universal Janitor | Code cleanup, simplification, and tech debt removal |
| Critical Thinking | Challenging assumptions and exploring alternatives |
| Next.js Expert | Next.js 15/16+ architecture and optimizations |
| Expert React Frontend Engineer | React 19+ patterns and best practices |
| Playwright Tester Mode | Comprehensive testing with exploratory testing |
| Tech Writer | Creating formal developer documentation |
| Create PRD Chat Mode | Generating Product Requirements Documents |
| Specification | Generating or updating specification documents |
| Plan | Research and outlining multi-step plans |

## Decision Framework

When choosing an agent for delegation:

1. **Identify task type**: Is it documentation, testing, code review, or development?
2. **Match to specialization**: Find agent whose description aligns with task
3. **Check availability**: Verify agent exists and has proper frontmatter configuration
4. **Use specific agentName**: Delegate using exact name from agent's frontmatter

## Task Categories

### Code Analysis & Documentation
- Use **Code Explainer** for analyzing existing code patterns
- Use **Tech Writer** for formal developer documentation
- Use **Specification** for generating feature specifications

### Code Quality & Maintenance
- Use **Universal Janitor** for cleanup and tech debt remediation
- Use **Critical Thinking** for challenging assumptions

### Development Work
- Use **Next.js Expert** for Next.js 15/16+ architecture and optimizations
- Use **Expert React Frontend Engineer** for React 19+ patterns

### Testing
- Use **Playwright Tester Mode** for comprehensive web application testing

### Planning & Requirements
- Use **Plan** for research and outlining multi-step plans
- Use **Create PRD Chat Mode** for generating Product Requirements Documents

### Design
- Use **UI Designer** for UI/UX improvements and design implementations


---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [custom-agent-usage](../custom-agent-usage/SKILL.md) | Discover and validate .agent.md files before mapping tasks |
| [subagent-delegation](../subagent-delegation/SKILL.md) | Execute delegated work after mapping to the right agent |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [custom-agent-usage](../custom-agent-usage/SKILL.md) | Discover and validate .agent.md files before mapping tasks |
| [subagent-delegation](../subagent-delegation/SKILL.md) | Execute delegated work after mapping to the right agent |
