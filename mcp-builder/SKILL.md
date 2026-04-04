---
name: mcp-builder
description: Build high-quality MCP servers with strong tool design, structured outputs, clear error handling, and realistic evaluations. Use when creating or improving MCP servers in TypeScript or Python for external APIs, services, or internal platforms.
license: Complete terms in LICENSE.txt
---
# MCP Builder

Design MCP servers that are easy for agents to discover, compose, and trust.

## When to Use

- You are creating a new MCP server around an external API or internal platform.
- An existing MCP server needs better tool naming, schemas, pagination, or error handling.
- You need a workflow for evaluating whether an MCP server is actually useful for real agent tasks.
- You are deciding between TypeScript and Python MCP implementations.

## Core Workflow

### 1. Research First

Before implementation:

1. Read the current MCP protocol documentation.
2. Read the relevant SDK guide for your implementation language.
3. Review the target service API and list the highest-value operations.
4. Decide which operations should stay low-level and which deserve dedicated workflow tools.

### 2. Design Agent-Friendly Tools

Prefer tools that are easy to discover and compose:

- use clear action-oriented names
- keep schemas explicit and constrained
- support pagination and filters where lists can grow
- return structured content whenever the client can benefit from it
- write error messages that tell the agent what to do next

### 3. Implement Shared Infrastructure

Build common pieces before individual tools:

- authenticated API client
- error formatter
- response normalizer
- pagination helpers
- reusable schema utilities

### 4. Test the Server Like an Agent Would

Verify more than syntax:

- build or type-check the server
- inspect tool registration and descriptions
- run the server through MCP Inspector or an equivalent client
- confirm that common read and write flows behave predictably

### 5. Create Real Evaluations

A strong MCP server needs realistic read-only evaluations:

- write questions that require multiple tool calls
- keep answers stable and verifiable
- prefer realistic operator tasks over toy examples
- store the evaluation set with the server so regressions are visible later

## Language Guidance

### TypeScript

Prefer TypeScript when you want the strongest SDK ergonomics and schema-heavy tool definitions.

Primary references:

- [TypeScript MCP Guide](./reference/node_mcp_server.md)
- [MCP Best Practices](./reference/mcp_best_practices.md)

### Python

Prefer Python when the target ecosystem or existing service code is already Python-heavy.

Primary references:

- [Python MCP Guide](./reference/python_mcp_server.md)
- [MCP Best Practices](./reference/mcp_best_practices.md)

## Included Assets

- [MCP Best Practices](./reference/mcp_best_practices.md)
- [TypeScript Implementation Guide](./reference/node_mcp_server.md)
- [Python Implementation Guide](./reference/python_mcp_server.md)
- [Evaluation Guide](./reference/evaluation.md)
- `scripts/connections.py`
- `scripts/evaluation.py`
- `scripts/example_evaluation.xml`

## Practical Rules

- Comprehensive API coverage is usually safer than a handful of overly clever workflow tools.
- Add workflow tools only when they remove real friction for agents.
- Keep tool descriptions concise enough to stay readable in tool lists.
- Structured outputs beat prose when downstream automation matters.
- Evaluation quality is part of the server quality, not a separate optional step.

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:mcp-builder` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py mcp-builder` and then run `/commands reload` inside Gemini CLI.

## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- Use the bundled reference library, local SDK documentation, and the included helper scripts even when the current host has no live MCP inspection surface.
- If MCP Inspector or equivalent tooling is unavailable, fall back to build checks, schema review, and scripted evaluation fixtures before calling the server ready.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [codexer](../codexer/SKILL.md) | Useful when researching Python libraries or API clients for the server implementation |
| [javascript-development](../javascript-development/SKILL.md) | Supports TypeScript or JavaScript MCP implementations |
| [development-workflow](../development-workflow/SKILL.md) | Helps turn server research into an implementable plan or spec |
