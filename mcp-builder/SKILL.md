---
name: mcp-builder
version: "2.0"
last_updated: 2026-07-29
tags: [mcp, builder, workflow, quality, planning]
description: "Build high-quality MCP servers with strong tool design, structured outputs, clear error handling, and realistic evaluations. Use when creating or improving MCP servers in TypeScript or Python for external APIs, services, or internal platforms."
---
# MCP Builder

Design MCP servers that are easy for agents to discover, compose, and trust.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- You are creating a new MCP server around an external API or internal platform.
- An existing MCP server needs better tool naming, schemas, pagination, or error handling.
- You need a workflow for evaluating whether an MCP server is actually useful for real agent tasks.
- You are deciding between TypeScript and Python MCP implementations.

## Glossary

- MCP Inspector: An interactive client for browsing registered tools, schemas, inputs, and outputs while you validate a server.
- Structured outputs: Predictable JSON or schema-backed payloads that downstream agents can parse safely instead of scraping prose.
- Workflow tool: A higher-level tool that coordinates several lower-level API steps into one agent-friendly operation.

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

## Shared Infrastructure Before and After

### Pagination Helper
```typescript
// Before
async function listTickets(page = 1) {
  return api.get(`/tickets?page=${page}`)
}

// After
export async function paginate<T>(fetchPage: (cursor?: string) => Promise<{ items: T[]; nextCursor?: string }>) {
  const items: T[] = [];
  let cursor: string | undefined;
  do {
    const page = await fetchPage(cursor);
    items.push(...page.items);
    cursor = page.nextCursor;
  } while (cursor);
  return items;
}
```

### Error Formatter
```typescript
// Before
throw new Error(`Request failed: ${response.status}`)

// After
throw formatToolError({
  code: 'tickets.list_failed',
  message: 'Unable to list tickets for the requested project.',
  status: response.status,
  nextAction: 'Check the project id and retry with a smaller page size.',
})
```

### Schema Utilities
```typescript
// Before
server.tool('create_ticket', { title: z.string(), priority: z.string() }, handler)

// After
const prioritySchema = z.enum(['low', 'medium', 'high']);
const ticketInput = buildToolSchema({
  title: z.string().min(1),
  priority: prioritySchema.default('medium'),
});
server.tool('create_ticket', ticketInput, handler)
```

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

## Security, Observability, Auth Handling, Logging, and Versioning

### Security

Minimize scopes, redact secrets from errors, and keep authorization checks inside shared request middleware instead of duplicating them per tool.

### Observability

Log request identifiers, tool names, latency, and retry counts so agent failures can be traced without replaying everything manually.

### Auth Handling

Support token refresh or credential reload paths explicitly so agents get actionable failures instead of opaque 401 loops.

### Logging

Prefer structured logs with stable fields such as `tool`, `resource`, `status`, and `duration_ms` over free-form strings.

### Versioning

Treat tool names, schemas, and error contracts as public interfaces; add versions or deprecation notes before changing them in place.

## Anti-Patterns

- Starting work before the plan or gate is clear: Execution drifts when success criteria are implied instead of explicit.
- Treating verification as optional cleanup: The last mile is where regressions and missing updates are usually hiding.
- Mixing planning, implementation, and release work in one jump: You lose the causal chain that explains why a change is safe.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Mcp Builder workflow names the agent boundary, delegated scope, and expected return artifact.
2. Pass/fail: Context passed to helpers is minimal, task-local, and free of hidden expected answers.
3. Pass/fail: Results are integrated only after evidence, diffs, or citations are checked by the controller.
4. Pressure-test scenario: Run the workflow on two similar tasks that must not share assumptions or leaked context.
5. Success metric: Zero context leakage; every delegated output is independently reviewable.

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

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/mcp-builder` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the MCP Builder skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [development-workflow](../development-workflow/SKILL.md): Use it when the workflow also needs planning, quality gates, and delivery tracking.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
- [test-driven-development](../test-driven-development/SKILL.md): Use it when the workflow also needs test-first implementation and regression safety.
