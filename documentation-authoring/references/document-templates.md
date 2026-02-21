# Document Templates Reference

Reusable templates for common technical documents. Each includes purpose, audience, standard sections, writing tips, and a fill-in skeleton.

---

## 1. Product Requirements Document (PRD)

**Purpose:** Define what to build and why, aligning stakeholders on scope, goals, and success criteria before development begins.

**Audience:** Product managers, engineers, designers, QA, leadership.

**Tips:**
- Lead with the problem, not the solution
- User stories should be testable — write acceptance criteria as concrete scenarios
- Quantify success metrics with baselines and targets
- Keep scope tight; link to separate docs for deep dives

### Skeleton

```markdown
# PRD: [Feature Name]

**Author:** [Name]
**Status:** Draft | In Review | Approved | Superseded
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

## 1. Problem Statement
What pain point exists? Who experiences it? What evidence do we have (data, feedback, research)?

## 2. Goals & Non-Goals
### Goals
- [Measurable outcome 1]
- [Measurable outcome 2]

### Non-Goals
- [Explicitly out of scope item 1]

## 3. User Stories
### Story 1: [Persona] — [Action]
> As a [persona], I want to [action] so that [benefit].

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

## 4. Success Metrics
| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|--------------------|
| [KPI]  | [Current]| [Goal] | [How measured]     |

## 5. Design & UX
Link to mockups or describe key screens/flows.

## 6. Technical Requirements
- Performance constraints
- Data requirements
- Integration points
- Security considerations

## 7. Dependencies
| Dependency | Owner | Status | Risk |
|------------|-------|--------|------|
| [Item]     | [Team]| [State]| [Impact if delayed] |

## 8. Rollout Plan
- Phase 1: [Internal/beta]
- Phase 2: [Gradual rollout]
- Phase 3: [GA]

## 9. Risks & Mitigations
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Action] |

## 10. Open Questions
- [ ] [Question needing resolution]

## Appendix
Supporting data, research links, or detailed specs.
```

---

## 2. Request For Comments (RFC)

**Purpose:** Propose a significant technical change, gather feedback from peers, and reach consensus before implementation.

**Audience:** Engineering team, architect leads, affected stakeholders.

**Tips:**
- Present alternatives honestly — show why the proposed approach wins
- Include a "non-goals" section to prevent scope creep in discussion
- Set a review deadline to avoid indefinite open RFCs
- Number your RFCs for easy reference

### Skeleton

```markdown
# RFC-[NNN]: [Title]

**Author:** [Name]
**Status:** Draft | Open for Review | Accepted | Rejected | Withdrawn
**Review Deadline:** YYYY-MM-DD
**Created:** YYYY-MM-DD

## Summary
One-paragraph description of the proposal.

## Motivation
Why is this change needed? What problem does it solve?

## Detailed Design

### Architecture
Describe the proposed system design with diagrams if helpful.

### API / Interface Changes
```
[code or schema changes]
```

### Data Model Changes
Describe any storage, schema, or migration requirements.

### Migration Plan
How do we transition from current state to proposed state?

## Alternatives Considered
| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| [Option A]  | ...  | ...  | ...            |
| [Option B]  | ...  | ...  | ...            |

## Risks & Open Questions
- [Risk or question 1]
- [Risk or question 2]

## Implementation Plan
- [ ] Phase 1: [Description] — [Estimated effort]
- [ ] Phase 2: [Description] — [Estimated effort]

## References
- [Link to related RFC, doc, or research]
```

---

## 3. Architecture Decision Record (ADR)

**Purpose:** Capture a single architectural decision with its context and consequences so future teams understand *why* a choice was made.

**Audience:** Current and future engineers, architects, tech leads.

**Tips:**
- Keep each ADR focused on one decision
- Write in present tense at the time of the decision
- Never delete ADRs — supersede them with new ones
- Store ADRs close to the code (e.g., `docs/adr/`)

### Skeleton

```markdown
# ADR-[NNN]: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-[NNN]
**Date:** YYYY-MM-DD
**Deciders:** [Names or roles]

## Context
What is the issue that we're seeing that motivates this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Tradeoff 2]

### Neutral
- [Observation]

## Alternatives Considered
1. **[Alternative A]** — [Brief description and why rejected]
2. **[Alternative B]** — [Brief description and why rejected]

## Related
- [Link to related ADRs, RFCs, or docs]
```

---

## 4. Technical Specification

**Purpose:** Provide implementation-level detail for a feature or system so that any engineer can build it without ambiguity.

**Audience:** Implementing engineers, code reviewers, QA.

**Tips:**
- Include sequence diagrams for multi-component flows
- Define error handling explicitly — do not leave it implicit
- Specify data formats (JSON schemas, DB columns) precisely
- Call out what is *not* changing

### Skeleton

```markdown
# Technical Specification: [Feature/System Name]

**Author:** [Name]
**Status:** Draft | Approved | Implemented
**Created:** YYYY-MM-DD
**Related PRD:** [Link]

## Overview
Brief description of what this spec covers.

## System Context
Where does this feature fit in the overall architecture? Include a diagram.

## Detailed Design

### Component A: [Name]
**Responsibility:** [What it does]

**Interface:**
```
[function signatures, API endpoints, or message formats]
```

**Behavior:**
1. [Step-by-step logic]
2. [Error handling paths]

### Component B: [Name]
[Same structure as above]

## Data Model
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| [name]| [type]| [nullable, unique, etc.] | [purpose] |

## API Contracts
### `METHOD /path`
**Request:**
```json
{ "field": "type" }
```
**Response (200):**
```json
{ "field": "type" }
```
**Error Responses:**
| Status | Body | When |
|--------|------|------|
| 400 | `{ "error": "..." }` | [condition] |

## Security Considerations
- Authentication/authorization requirements
- Input validation rules
- Data privacy implications

## Performance Considerations
- Expected load
- Latency requirements
- Caching strategy

## Testing Strategy
- Unit test focus areas
- Integration test scenarios
- Edge cases to cover

## Rollback Plan
How to revert if something goes wrong post-deployment.
```

---

## 5. Design Document

**Purpose:** Communicate a high-level design approach for a project or feature, bridging the gap between requirements and implementation.

**Audience:** Engineers, designers, product managers, technical leads.

**Tips:**
- Use diagrams liberally — architecture diagrams, flow charts, wireframes
- Balance detail: enough to evaluate the approach, not so much it becomes a spec
- Identify the hardest parts and address them directly
- Get feedback early before investing in implementation detail

### Skeleton

```markdown
# Design Document: [Project/Feature Name]

**Author:** [Name]
**Reviewers:** [Names]
**Status:** Draft | Under Review | Approved
**Created:** YYYY-MM-DD

## Background
Context and motivation. What problem are we solving?

## Goals
- [Goal 1]
- [Goal 2]

## High-Level Design
Describe the overall approach with architecture diagrams.

### System Architecture
[Diagram: show major components and their interactions]

### Key Flows
#### Flow 1: [Name]
[Sequence or flow diagram with numbered steps]

#### Flow 2: [Name]
[Sequence or flow diagram with numbered steps]

## Detailed Design

### Module/Component 1
- Purpose
- Key interfaces
- Important implementation notes

### Module/Component 2
- [Same structure]

## Trade-offs & Decisions
| Decision | Options Considered | Choice | Rationale |
|----------|--------------------|--------|-----------|
| [Topic]  | A, B, C            | B      | [Why]     |

## Timeline & Milestones
| Milestone | Target Date | Description |
|-----------|-------------|-------------|
| M1        | YYYY-MM-DD  | [What]      |

## Open Questions
- [ ] [Question]
```

---

## 6. Runbook

**Purpose:** Provide step-by-step procedures for operating, troubleshooting, or recovering a system. Written for the on-call engineer at 3 AM.

**Audience:** Operations engineers, SREs, on-call responders.

**Tips:**
- Write for someone unfamiliar with the system under stress
- Every step should be copy-pastable where possible
- Include expected output for each command
- Link to dashboards and alert configurations

### Skeleton

```markdown
# Runbook: [System/Service Name]

**Last Verified:** YYYY-MM-DD
**Owner:** [Team]
**On-Call Escalation:** [Contact info or PagerDuty link]

## Service Overview
- **What it does:** [Brief description]
- **Dashboard:** [Link]
- **Logs:** [Link or command]
- **Dependencies:** [Upstream/downstream services]

## Common Alerts

### Alert: [Alert Name]
**Severity:** P1 / P2 / P3
**Meaning:** [What triggered this alert]

**Diagnosis Steps:**
1. Check [metric/dashboard]: `[command or link]`
   - Expected: [normal range]
   - If abnormal: proceed to step 2
2. Check [logs]: `[command]`
   - Look for: [pattern]

**Resolution:**
1. `[command to fix]`
   - Expected output: `[output]`
2. Verify recovery: `[verification command]`

**Escalation:** If unresolved after [time], escalate to [team/person].

## Operational Procedures

### Procedure: [Name, e.g., "Scale Service"]
**When to use:** [Trigger condition]
1. `[step 1 command]`
2. `[step 2 command]`
3. Verify: `[command]` — expected: [output]

### Procedure: [Name, e.g., "Rollback Deployment"]
1. `[step 1]`
2. `[step 2]`
3. Verify: `[command]`

## Recovery Procedures

### Disaster Recovery
1. [Step-by-step recovery]
2. [Data restoration]
3. [Verification]

## Contacts
| Role | Name | Contact |
|------|------|---------|
| Service Owner | [Name] | [Email/Slack] |
| Escalation | [Name] | [Email/Phone] |
```

---

## 7. Postmortem

**Purpose:** Document an incident, its root cause, and action items to prevent recurrence. Blameless by design.

**Audience:** Engineering team, leadership, affected stakeholders.

**Tips:**
- Stick to facts and timelines — avoid blame language
- "5 Whys" is a useful technique for root cause analysis
- Every action item needs an owner and a deadline
- Publish widely to maximize organizational learning

### Skeleton

```markdown
# Postmortem: [Incident Title]

**Date of Incident:** YYYY-MM-DD
**Duration:** [Start time] – [End time] ([total duration])
**Severity:** P1 / P2 / P3
**Author:** [Name]
**Status:** Draft | Published

## Summary
One-paragraph description: what happened, who was affected, what was the impact.

## Impact
- **Users affected:** [Number or percentage]
- **Revenue impact:** [If applicable]
- **Data loss:** [If applicable]
- **SLA breach:** [Yes/No — details]

## Timeline (all times in UTC)
| Time | Event |
|------|-------|
| HH:MM | [First sign of issue] |
| HH:MM | [Alert fired / user report] |
| HH:MM | [Investigation started] |
| HH:MM | [Root cause identified] |
| HH:MM | [Fix deployed] |
| HH:MM | [Service restored] |

## Root Cause Analysis
### What happened
[Factual description of the technical failure chain]

### Why it happened (5 Whys)
1. Why? [Proximate cause]
2. Why? [Deeper cause]
3. Why? [Deeper cause]
4. Why? [Deeper cause]
5. Why? [Root cause]

### Contributing Factors
- [Factor 1]
- [Factor 2]

## What Went Well
- [Positive observation 1]
- [Positive observation 2]

## What Went Poorly
- [Issue 1]
- [Issue 2]

## Action Items
| ID | Action | Owner | Priority | Deadline | Status |
|----|--------|-------|----------|----------|--------|
| 1  | [Action] | [Name] | P1/P2 | YYYY-MM-DD | Open |
| 2  | [Action] | [Name] | P1/P2 | YYYY-MM-DD | Open |

## Lessons Learned
- [Key takeaway 1]
- [Key takeaway 2]
```

---

## 8. Knowledge Base Article

**Purpose:** Provide a self-contained answer to a recurring question or how-to guide for internal or external users.

**Audience:** Developers, users, support team — varies per article.

**Tips:**
- Start with the answer or solution, then explain context
- Use progressive disclosure: summary → details → deep dive
- Include "Related Articles" to build a connected knowledge base
- Test with someone unfamiliar — if they can follow it, it works

### Skeleton

```markdown
# [Title: Action-Oriented, e.g., "How to Configure SSO"]

**Last Updated:** YYYY-MM-DD
**Applies To:** [Product version, environment, etc.]
**Tags:** [tag1, tag2, tag3]

## Quick Answer
[1–3 sentence summary or the direct answer]

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## Step-by-Step Guide

### Step 1: [Action]
[Detailed instruction]

```
[command or code example]
```

### Step 2: [Action]
[Detailed instruction]

### Step 3: [Action]
[Detailed instruction]

## Verification
How to confirm the procedure worked:
```
[verification command or check]
```
Expected result: [description]

## Troubleshooting

### Problem: [Common issue]
**Cause:** [Why it happens]
**Solution:** [How to fix]

### Problem: [Another common issue]
**Cause:** [Why]
**Solution:** [Fix]

## Related Articles
- [Link to related KB article]
- [Link to related KB article]

## FAQ
**Q: [Common question]**
A: [Answer]
```
