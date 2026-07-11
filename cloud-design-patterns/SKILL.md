---
name: cloud-design-patterns
version: "1.3"
last_updated: 2026-07-11
tags: [cloud, design, patterns, architecture, operations]
description: "Choose and compare cloud design patterns for distributed systems. Use when reviewing architecture, selecting workload patterns, or mapping reliability, performance, messaging, security, and migration concerns to concrete design options."
---
# Cloud Design Patterns

Use proven distributed-systems patterns to choose safer architectures and surface trade-offs early.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- You are designing or reviewing a cloud or distributed-system architecture.
- A workload has reliability, latency, scaling, messaging, migration, or security concerns.
- You need to shortlist patterns before writing an ADR, design doc, or implementation plan.
- You want a technology-agnostic pattern discussion before choosing platform services.

## Pattern Selection Workflow

1. State the main workload goal and the main constraint.
2. Identify the top concerns: reliability, performance, messaging, migration, deployment, security, or eventing.
3. Use the concern-to-pattern map below to shortlist candidates.
4. Compare trade-offs instead of looking for a single perfect pattern.
5. Document why the chosen pattern fits the workload better than the obvious alternatives.

## Concern-To-Pattern Map

| Concern | Common patterns | Reference |
|---------|-----------------|-----------|
| reliability and fault tolerance | Bulkhead, Circuit Breaker, Retry, Health Endpoint Monitoring, Saga | [Reliability And Resilience](./references/reliability-resilience.md) |
| performance and scale | Cache-Aside, CQRS, Queue-Based Load Leveling, Rate Limiting, Sharding | [Performance](./references/performance.md) |
| messaging and workflow coordination | Publisher-Subscriber, Pipes and Filters, Competing Consumers, Choreography | [Messaging And Integration](./references/messaging-integration.md) |
| architecture boundaries and API shape | Anti-Corruption Layer, Backends for Frontends, Gateway patterns, Sidecar, Strangler Fig | [Architecture And Design](./references/architecture-design.md) |
| deployment and operations | Deployment Stamps, External Configuration Store, Geode, Static Content Hosting | [Deployment And Operational](./references/deployment-operational.md) |
| security and controlled access | Federated Identity, Quarantine, Valet Key | [Security](./references/security.md) |
| event sourcing and auditability | Event Sourcing | [Event-Driven](./references/event-driven.md) |

## Pattern Review Questions

Ask these before locking in a pattern:

- What failure mode is this pattern reducing?
- What cost, complexity, or operational burden does it add?
- Does the team have the observability needed to operate it?
- Is the pattern local to one subsystem or does it create a cross-cutting contract?
- What simpler alternative did we reject, and why?

## Anti-Patterns

- Changing infrastructure before inspecting the current state: Cloud drift and hidden dependencies make blind edits risky.
- Hardcoding credentials or environment assumptions: Rollouts stop being reproducible and secrets become harder to rotate.
- Skipping rollback, observability, or validation planning: You only notice the missing safeguards after the deployment is already live.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Cloud Design Patterns workflow starts from explicit success criteria, constraints, and stop conditions.
2. Pass/fail: Required evidence is collected before any completion, approval, or readiness claim.
3. Pass/fail: The next action follows the documented gate order without skipping review or verification steps.
4. Pressure-test scenario: Apply the workflow under time pressure with one failing check and one tempting shortcut.
5. Success metric: Zero rationalizations; blocked, failed, or unverified work is reported as such.

## Scripts And References

- [Pattern Shortlist Helper](./scripts/pattern-shortlist.py)
- [Reliability And Resilience](./references/reliability-resilience.md)
- [Performance](./references/performance.md)
- [Messaging And Integration](./references/messaging-integration.md)
- [Architecture And Design](./references/architecture-design.md)
- [Deployment And Operational](./references/deployment-operational.md)
- [Security](./references/security.md)
- [Event-Driven](./references/event-driven.md)
- [Best Practices](./references/best-practices.md)
- [Azure Service Mappings](./references/azure-service-mappings.md)

## Practical Guidance

- Prefer a small pattern set that directly addresses the workload constraints.
- Pair each selected pattern with explicit observability and rollback thinking.
- Technology choice comes after pattern choice, not before it.
- If a migration is underway, keep the transitional pattern and the target steady-state pattern separate in your notes.

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:cloud-design-patterns` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py cloud-design-patterns` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Cloud Design Patterns skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [azure-integrations](../azure-integrations/SKILL.md): Use it when the workflow also needs Azure deployment and infrastructure automation.
- [powerbi-modeling](../powerbi-modeling/SKILL.md): Use it when the workflow also needs Power BI semantic model design and DAX work.
- [microsoft-development](../microsoft-development/SKILL.md): Use it when the workflow also needs microsoft development guidance.
- [sql-development](../sql-development/SKILL.md): Use it when the workflow also needs SQL query, schema, and performance tuning work.
