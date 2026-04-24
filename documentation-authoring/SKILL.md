---
name: documentation-authoring
version: "1.2"
last_updated: 2026-04-25
tags: [documentation, authoring, docs, writing, quality]
description: "Create structured docs from scratch — PRDs, technical specs, design docs, decision records, knowledge bases. Use when drafting documentation, writing proposals, defining requirements, or planning features."
---

# Documentation Authoring Master

Expert guidance for creating structured, high-quality documentation across all types of technical and business documents.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.



## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

**Trigger Conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User asks to "create an implementation plan", "document requirements", "plan a feature"
- Creating technical specifications or business requirements
- Starting a new product or feature development cycle
- Translating vague ideas into concrete technical specifications
- Stakeholders need unified "source of truth" for project scope

## Part 2: Context Gathering

### Initial Questions

Start by asking for meta-context about the document:

1. **What type of document is this?**
   - Technical spec, decision doc, proposal, RFC, PRD, knowledge base

2. **Who's the primary audience?**
   - Developers, executives, stakeholders, end-users? Understanding affects tone and depth

3. **What's the desired impact when someone reads this?**
   - Make a decision, implement a feature, understand a concept?

4. **Is there a template or specific format to follow?**
   - Company templates, industry standards, regulatory requirements

5. **Any other constraints or context to know?**
   - Deadlines, sensitive information, existing related documents

**Inform them they can answer in shorthand or dump information however works best for them.**

### Template Handling

**If user provides a template:**
- Analyze structure and requirements
- Adapt co-authoring workflow to template format
- Ensure all required sections are covered

**If user mentions editing an existing document:**
- Fetch the existing document
- Understand current state and gaps
- Plan revisions strategically

---

## Part 3: Refinement & Structure

### Collaborative Building

**Process:**
1. **Brainstorm each section** together - let ideas flow without judgment
2. **Organize and refine** - structure ideas into coherent sections
3. **Edit for clarity** - improve readability and flow
4. **Add professional polish** - formatting, consistency, tone

**Guiding Principles:**
- **Active voice**: Use direct, clear language
- **Show, don't just tell**: Use examples and scenarios
- **Progressive disclosure**: Start with overview, then dive deeper
- **Visual aids**: Include diagrams, tables, and examples where helpful

### Section-by-Section Approach

Work through document methodically:

```markdown
## Recommended Section Structure

### 1. Executive Summary (for decision-makers)
- What is this about?
- Why does it matter?
- What are we recommending/deciding?

### 2. Background & Context (for implementers)
- What led us here?
- What problem are we solving?
- What constraints exist?

### 3. Requirements/Objectives
- What must we achieve?
- What are success criteria?
- What are non-goals?

### 4. Proposed Solution/Design
- What are we proposing?
- How does it work?
- What are alternatives considered?

### 5. Implementation Plan
- How do we build this?
- What are the steps?
- Who needs to do what?

### 6. Risks & Considerations
- What could go wrong?
- How do we mitigate?
- What decisions are still needed?
```

---

## Part 4: Reader Testing

### The Fresh Eye Test

Before finalizing, put yourself in the reader's shoes:

**Test Questions:**
1. Can I understand the goal without knowing context?
2. Are technical terms explained or linked?
3. Is there a logical flow from problem to solution?
4. Would a skeptical reader be convinced?
5. Is action clear - what should I do next?

### Blind Spot Detection

Common issues to catch:
- **Context assumptions**: "We already discussed this" but wasn't documented
- **Missing alternatives**: Only one option presented (shows lack of thoroughness)
- **Unanswered questions**: Reader left with "what about X?"
- **Unclear responsibilities**: Who needs to do what is vague
- **Missing examples**: Abstract concepts without concrete illustration

---

## Part 5: Product Requirements Document (PRD)

### PRD Structure

When users specifically request PRDs or feature planning, use this structure:

```markdown
# [Feature/Product Name] - PRD

## Executive Summary
**Goal**: [What problem are we solving?]
**Impact**: [Why does this matter now?]
**Success Metrics**: [How will we know it worked?]

## Background
**Current State**: [What's the situation today?]
**Problem Statement**: [What pain points exist?]
**Constraints**: [Budget, timeline, tech stack limitations?]

## Requirements

### Functional Requirements
- User stories with acceptance criteria
- Core features and capabilities
- Integration requirements

### Non-Functional Requirements
- Performance requirements
- Security requirements
- Compliance and regulatory needs

### User Stories
```
As a [persona],
I want to [action],
So that [benefit].
```
**Acceptance Criteria**:
- [ ] [Specific, measurable criterion]
- [ ] [Another criterion]
```

## Proposed Solution

### Architecture Overview
[High-level system architecture or approach]

### Technical Specifications
[API contracts, data models, interfaces]

### UI/UX Requirements
[Wireframes or flow descriptions if applicable]

## Implementation Plan

### Phases
| Phase | Tasks | Owners | Timeline |
|-------|--------|---------|----------|
| Phase 1 | | | |
| Phase 2 | | | |

### Dependencies
- [ ] External APIs or services
- [ ] Other teams or systems
- [ ] Third-party libraries

## Risk Analysis

| Risk | Impact | Probability | Mitigation |
|-------|---------|--------------|-------------|
| [Risk] | High/Med/Low | High/Med/Low | [Mitigation] |

## Alternatives Considered

| Option | Pros | Cons | Why Not Chosen |
|--------|-------|-------|-----------------|
| Alt 1 | | | |

## Success Criteria

### Quantitative
- [ ] [Measurable metric: e.g., "reduce load time by 50%"]
- [ ] [Another metric]

### Qualitative
- [ ] [User feedback threshold]
- [ ] [Stakeholder alignment]

## Open Questions
- [ ] [Decision still needed]
- [ ] [Information to gather]
```

### PRD Creation Workflow

**Phase 1: Discovery (The Interview)**
Before writing a single line, you **MUST** interrogate user to fill knowledge gaps. Do not assume context.

**Ask about:**
- **The Core Problem**: Why are we building this now?
- **Success Metrics**: How do we know it worked?
- **Constraints**: Budget, tech stack, or deadline?
- **Stakeholders**: Who needs to approve? Who will use?

**Phase 2: Analysis & Scoping**
Synthesize user input. Identify dependencies and hidden complexities.
- **Map out User Flow**
- **Define Non-Goals** to protect timeline

**Phase 3: Technical Drafting**
Generate document using strict structure above.

---

## Part 6: Common Document Types

### Implementation Plans

**Purpose**: Guide building process with clear phases, responsibilities, and timeline.

**Structure:**
- **Overview**: What are we building and why?
- **Phases**: Break into logical chunks with dependencies
- **Tasks**: Trackable, specific implementation items
- **Timeline**: Realistic dates with buffers
- **Dependencies**: What must happen before what?

### Design Docs

**Purpose**: Document technical decisions and architecture.

**Structure:**
- **Problem Statement**: What problem are we solving?
- **Alternatives**: What did we consider?
- **Decision**: What did we choose and why?
- **Implications**: What does this mean for the system?
- **Risks**: What could go wrong?

### Decision Records

**Purpose**: Capture important decisions for future reference.

**Template:**
```markdown
### Decision - [DATE]
**Decision**: [What was decided]
**Context**: [Situation and driving data]
**Options**: [Alternatives with pros/cons]
**Rationale**: [Why selected option is superior]
**Impact**: [Anticipated consequences]
**Review**: [Reassessment conditions/trigger]
```

### Knowledge Base Articles

**Purpose**: Reusable reference material, not project-specific docs.

**Structure:**
- **Quick Reference**: TL;DR summary at top
- **Problem**: What question does this answer?
- **Solution**: How do you solve it?
- **Examples**: Concrete, runnable examples
- **Common Pitfalls**: What mistakes do people make?
- **Related Topics**: Links to related info

---

## Part 7: Best Practices

### For All Documentation

✅ **DO**:
- Use active voice and clear language
- Structure information progressively (simple to complex)
- Include examples and concrete scenarios
- Define terms before using them
- Add diagrams for complex systems
- Maintain consistent formatting and style

❌ **DON'T**:
- Write without clear audience in mind
- Mix jargon without explanation
- Skip alternatives or trade-offs analysis
- Assume readers have context they don't
- Create long paragraphs without breaks

### For Technical Docs

- Include code snippets that actually run
- Link to external references for deeper dives
- Use standard terminology when possible
- Version specific code/commands (e.g., "for node v16+")

### For Business/Stakeholder Docs

- Start with executive summary
- Use business impact metrics
- Hide unnecessary technical detail
- Include clear next steps or approvals needed
- Highlight risks and mitigations prominently

---

## Part 8: Action Documentation Format

Use this format for tracking implementation work and decisions:

### [TYPE] - [ACTION] - [TIMESTAMP]

**Objective**: [Goal being accomplished]

**Context**: [Current state, requirements, reference to prior steps]

**Decision**: [Approach chosen and rationale]

**Execution**: [Steps taken with parameters and commands]

**Output**: [Complete results, logs, metrics]

**Validation**: [Success verification and results]

**Next**: [Continuation plan to next action]

---

## Part 9: Summary Formats

### Streamlined Action Log (for changelogs)
`[TYPE][TIMESTAMP] Goal: [X] → Action: [Y] → Result: [Z] → Next: [W]`

### Quick Summary (for updates)
**What**: [Brief description]
**Why**: [Context/rationale]
**How**: [Approach taken]
**Status**: [Current state]
**Next**: [Upcoming step]

---

## Documentation Stack Reference

Inherit the shared stack from [documentation-patterns](../documentation-patterns/SKILL.md#shared-documentation-stack): source-of-truth discovery, audience framing, structure selection, verification, and freshness checks. Keep this skill focused on drafting and refinement instead of restating the full stack.

## Anti-Patterns

- Writing for the author instead of the reader: It bakes in unstated context and leaves the actual audience unsure what to do next.
- Skipping concrete examples or commands: Abstract guidance is easy to approve and hard to apply correctly.
- Letting links, screenshots, or versions drift: Polished formatting does not help if the instructions are no longer true.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Documentation Authoring output identifies audience, purpose, source of truth, and freshness requirements.
2. Pass/fail: Shared documentation-stack guidance is referenced instead of duplicating another documentation skill.
3. Pass/fail: Claims, links, commands, examples, and screenshots are verified or explicitly marked unverified.
4. Pressure-test scenario: Apply the skill to a doc request with a stale command, missing owner, and conflicting audience.
5. Success metric: Zero undocumented assumptions; every reader-facing claim is sourced or scoped.


## Documentation Quality Checklist

### Completeness
- [ ] All required sections filled
- [ ] Context and background provided
- [ ] Alternatives considered where applicable
- [ ] Examples and diagrams included where helpful

### Clarity
- [ ] Language is clear and direct
- [ ] Technical terms defined or linked
- [ ] Flowlogical and easy to follow
- [ ] Active voice used consistently

### Accuracy
- [ ] Technical details are correct
- [ ] Links work and are up-to-date
- [ ] Code examples actually run
- [ ] No contradictory information

### Accessibility
- [ ] Multiple levels of detail for different readers
- [ ] Executive summary for decision-makers
- [ ] Deep-dive sections for implementers
- [ ] Visual aids for complex concepts

---

## References & Resources

### Documentation
- [Document Templates](./references/document-templates.md) — Templates for PRD, RFC, ADR, Tech Spec, Design Doc, Runbook, Postmortem, KB Article
- [Writing Style Guide](./references/writing-style-guide.md) — Technical writing best practices, formatting conventions, and readability

### Scripts
- [Doc Structure Validator](./scripts/doc-structure-validator.py) — Python script to validate markdown document quality

### Examples
- [PRD Example](./examples/prd-example.md) — Complete PRD for Recipe Search Enhancement in Kitchen Odyssey

---

## Cross-Skill Workflow

- Start in this skill when you need to draft or reshape the document itself.
- Pull in [documentation-patterns](../documentation-patterns/SKILL.md) when the structure or template is the main decision.
- Finish with [documentation-quality](../documentation-quality/SKILL.md) when the draft needs an explicit review against quality bars.

## Agent Prompt Template

```text
Use the documentation-authoring skill to draft a [document type] for [audience].
Goal: [decision, rollout, implementation, or explanation target].
Required sections: [list].
Constraints: [scope, timeline, compliance, or tooling notes].
Include open questions, trade-offs, and next steps at the end.
```

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:documentation-authoring` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py documentation-authoring` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Documentation Authoring Master skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [documentation-patterns](../documentation-patterns/SKILL.md): Use it when the workflow also needs reusable documentation structures and templates.
- [documentation-quality](../documentation-quality/SKILL.md): Use it when the workflow also needs documentation review standards and quality gates.
- [documentation-verification](../documentation-verification/SKILL.md): Use it when the workflow also needs final documentation validation before publishing.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
