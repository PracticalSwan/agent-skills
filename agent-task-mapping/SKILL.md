---
name: agent-task-mapping
version: "1.3"
last_updated: 2026-07-11
tags: [task, mapping, agents, delegation, workflow]
description: "Map tasks to specialist agents. Use when choosing which agent for a job, comparing agent capabilities, or routing to React/Next.js/Playwright/docs/code-quality experts. Keywords: which agent, best agent for this, delegate to expert, agent capability mapping."
---
# Agent Task Mapping

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

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

## Anti-Patterns

- Delegating or evaluating without a scoped success condition: The output becomes hard to review and easy to overbuild.
- Skipping the evidence step: A workflow that cannot be re-checked quickly is not ready for handoff.
- Bundling unrelated subtasks together: It creates noisy prompts, weaker ownership, and avoidable integration risk.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Agent Task Mapping workflow names the agent boundary, delegated scope, and expected return artifact.
2. Pass/fail: Context passed to helpers is minimal, task-local, and free of hidden expected answers.
3. Pass/fail: Results are integrated only after evidence, diffs, or citations are checked by the controller.
4. Pressure-test scenario: Run the workflow on two similar tasks that must not share assumptions or leaked context.
5. Success metric: Zero context leakage; every delegated output is independently reviewable.

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

1. **Identify task type**: Is it documentation, testing, two-stage review (spec compliance first, then code quality), or development?
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

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:agent-task-mapping` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py agent-task-mapping` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Agent Task Mapping skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [custom-agent-usage](../custom-agent-usage/SKILL.md): Use it when the workflow also needs loading and invoking custom agent definitions safely.
- [subagent-delegation](../subagent-delegation/SKILL.md): Use it when the workflow also needs safe, scoped delegation to helper agents.
- [subagent-driven-development](../subagent-driven-development/SKILL.md): Use it when the workflow also needs plan-driven implementation with reviewer loops.
- [agentic-eval](../agentic-eval/SKILL.md): Use it when the workflow also needs rubric-driven evaluation loops.
