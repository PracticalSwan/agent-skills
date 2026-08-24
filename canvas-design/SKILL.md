---
name: canvas-design
version: "2.0"
last_updated: 2026-08-24
tags: [canvas, design, frontend, ui, visual]
description: "Design philosophy docs and canvas-based visual creation. Use when articulating design principles, crafting multi-page design documents, or exploring aesthetic philosophy with intentional design thinking."
---
# Canvas Design

A two-step design workflow: first articulate a design philosophy, then create visual designs on canvas. Based on the [anthropics/skills canvas-design](https://github.com/anthropics/skills) approach.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## When to Use This Skill

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Creating design philosophy documents (.md)
- Generating visual canvas designs (.png/.pdf)
- Articulating design principles and aesthetic rationale
- Crafting multi-page design documents
- Exploring design thinking and intentional visual communication


---

## Step 1: Design Philosophy Document

Create a markdown document that articulates the design philosophy before any visual creation.

### Philosophy Document Structure
```markdown


## Core Intent
What is this design trying to communicate? What feeling should it evoke?

## Guiding Principles
1. **[Principle Name]** — Explanation of how this shapes decisions
2. **[Principle Name]** — Explanation
3. **[Principle Name]** — Explanation

## Aesthetic Direction
- **Color Philosophy**: Why these colors, what they represent
- **Typography Philosophy**: What the type choices communicate
- **Spatial Philosophy**: How whitespace and layout serve the intent
- **Material/Texture**: Physical or digital texture decisions

## Inspirations & References
- [Reference 1]: What specifically resonates and why
- [Reference 2]: The element to borrow vs. what to avoid

## Step 2: Canvas Creation

After establishing the philosophy, create visual designs that embody those principles.

### Canvas Workflow
1. **Review philosophy** — Reread the design philosophy document
2. **Define canvas** — Set dimensions, background, grid system
3. **Establish hierarchy** — Place primary elements first
4. **Apply philosophy** — Every decision references a stated principle
5. **Refine** — Remove anything that doesn't serve the core intent

### Essential Design Principles

| Principle | Description |
|-----------|-------------|
| **Intentionality** | Every element exists for a reason |
| **Hierarchy** | Guide the eye through deliberate contrast and spacing |
| **Consistency** | Repeated patterns build trust and comprehension |
| **Restraint** | Fewer elements, each carrying more weight |
| **Craftsmanship** | Pixel-perfect alignment, harmonious proportions |

### Multi-Page Documents
For multi-page designs:
- Maintain consistent margins and grid across pages
- Use a master color palette derived from the philosophy
- Create a visual rhythm — varying density to prevent monotony
- Include breathing pages (minimal content) between dense sections

## Anti-Patterns

- Starting from a generic template without adapting it: The output may look polished but still miss the real audience or medium.
- Ignoring final render or export review: Layout bugs often appear only after the asset is opened in its destination tool.
- Fixing content and presentation in one pass: It becomes hard to tell whether a problem is structural or visual.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Canvas Design implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.


### Quality Checklist
- [ ] Every element traces back to a stated principle
- [ ] Color choices align with the documented philosophy
- [ ] Typography serves the content hierarchy
- [ ] Whitespace is intentional, not leftover
- [ ] The design could be explained purely through its philosophy doc
- [ ] Nothing decorative exists without purpose

---

## Craftsmanship Emphasis

Design is a craft. The difference between good and great design:

- **Alignment**: Not "close enough" but mathematically precise
- **Spacing**: Consistent rhythm using a base unit (4px, 8px)
- **Color**: Not just "looks nice" but optically balanced, accessible (WCAG AA+)
- **Typography**: Line height, letter spacing, and measure all tuned for readability
- **Details**: Transitions, hover states, focus indicators — the invisible work

> "The details are not the details. They make the design." — Charles Eames
---

## References & Resources

### Documentation
- [Design Principles](./references/design-principles.md) — Gestalt principles, visual hierarchy, typography pairing, golden ratio, and grid systems
- [Color Psychology](./references/color-psychology.md) — Color emotional associations, harmony types, industry palettes, and accessibility

### Scripts
- [Palette Generator](./scripts/generate-palette.py) — Python script to generate color palettes with WCAG contrast ratio checking

### Examples
- [Kitchen Odyssey Design Philosophy](./examples/design-philosophy-example.md) — Complete design philosophy document example for a recipe sharing platform


---

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/canvas-design` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Canvas Design skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [frontend-design](../frontend-design/SKILL.md): Use it when the workflow also needs UI composition and front-end design direction.
- [web-design-reviewer](../web-design-reviewer/SKILL.md): Use it when the workflow also needs browser-based UI review and responsive QA.
- [stitch-design](../stitch-design/SKILL.md): Use it when the workflow also needs turning interface designs into implementation-ready assets.
