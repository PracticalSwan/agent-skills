---
name: cloud-design-patterns
description: Choose and compare cloud design patterns for distributed systems. Use when reviewing architecture, selecting workload patterns, or mapping reliability, performance, messaging, security, and migration concerns to concrete design options.
---
# Cloud Design Patterns

Use proven distributed-systems patterns to choose safer architectures and surface trade-offs early.

## When to Use

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

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:cloud-design-patterns` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py cloud-design-patterns` and then run `/commands reload` inside Gemini CLI.

## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks architecture-specific tooling, use the bundled reference set and shortlist helper to narrow the decision.
- Treat the resulting design doc, ADR, or pattern comparison note as the fallback evidence path for why a pattern was selected.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [development-workflow](../development-workflow/SKILL.md) | Turn shortlisted patterns into ADRs, specs, and implementation plans |
| [azure-integrations](../azure-integrations/SKILL.md) | Map chosen patterns onto Azure deployment and service choices |
| [breaking-changes-management](../breaking-changes-management/SKILL.md) | Useful when patterns imply migrations or compatibility boundaries |
