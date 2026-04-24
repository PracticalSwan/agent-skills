---
name: subagent-delegation
version: "1.2"
last_updated: 2026-04-25
tags: [subagent, delegation, agents, workflow, automation]
description: "Delegate routine work to subagents — boilerplate generation, data transformation, file analysis, documentation drafting. Use when splitting tasks into independent subtasks for parallel subagent execution."
---

# Subagent Delegation Patterns

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

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

## Anti-Patterns

- Delegating or evaluating without a scoped success condition: The output becomes hard to review and easy to overbuild.
- Skipping the evidence step: A workflow that cannot be re-checked quickly is not ready for handoff.
- Bundling unrelated subtasks together: It creates noisy prompts, weaker ownership, and avoidable integration risk.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Subagent Delegation workflow names the agent boundary, delegated scope, and expected return artifact.
2. Pass/fail: Context passed to helpers is minimal, task-local, and free of hidden expected answers.
3. Pass/fail: Results are integrated only after evidence, diffs, or citations are checked by the controller.
4. Pressure-test scenario: Run the workflow on two similar tasks that must not share assumptions or leaked context.
5. Success metric: Zero context leakage; every delegated output is independently reviewable.


## Examples & Scripts

- [Delegation Pattern Examples](./examples/delegation-patterns-examples.md) — Code examples of common delegation patterns
- [Delegation Template](./scripts/delegation-template.js) — JavaScript template for structuring delegation calls

## Self-Verification Phase-Gate Questions

Before you mark delegated work complete, the coordinating agent must ask:

- Did the subagent receive a scoped task, owned files or responsibilities, and a clear definition of done?
- Did I review the returned output for correctness, integration fit, and missing edge cases instead of forwarding it blindly?
- Did I preserve the evidence trail showing what was delegated, what changed, and what still needs local ownership?
- Are any follow-up fixes, risks, or unresolved assumptions now explicit to the next reviewer?

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

Preferred MCP Server: None required

- Fallback prompt: "Use the Subagent Delegation Patterns skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [agent-task-mapping](../agent-task-mapping/SKILL.md): Use it when the workflow also needs task-to-agent routing decisions.
- [custom-agent-usage](../custom-agent-usage/SKILL.md): Use it when the workflow also needs loading and invoking custom agent definitions safely.
- [subagent-driven-development](../subagent-driven-development/SKILL.md): Use it when the workflow also needs plan-driven implementation with reviewer loops.
- [agentic-eval](../agentic-eval/SKILL.md): Use it when the workflow also needs rubric-driven evaluation loops.
