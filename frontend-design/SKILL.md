---
name: frontend-design
version: "2.0"
last_updated: 2026-08-02
tags: [frontend, design, ui, ux, accessibility, responsive]
license: "MIT AND Apache-2.0"
description: "Design and implement context-fit frontend interfaces with deliberate art direction, accessible interaction, responsive behavior, complete states, and rendered verification. Use when creating or substantially reworking pages, components, product workspaces, dashboards, marketing sites, editorial surfaces, commerce flows, or justified immersive experiences."
---
# Frontend Design

Create interfaces that are fit for their users, tasks, content, product category, and technical constraints. "Best" means fitness for context, not adherence to one visual style.

Accessibility, functional correctness, valid implementation examples, and usable responsive behavior are hard gates. Do not approve a visually impressive result that creates keyboard traps, inaccessible controls, unreadable content, broken states, severe responsive defects, or unjustified performance costs.

## Operational Decision Rubric

Use these weights to compare viable design choices. They are an operational decision rubric, not a universal mathematical standard, and they never compensate for a hard-gate failure.

| Criterion | Weight |
|---|---:|
| User and task fit | 20% |
| Accessibility | 20% |
| Usability and information architecture | 15% |
| Visual coherence and appropriate distinctiveness | 15% |
| Responsive and adaptive behavior | 10% |
| Performance and resilience | 10% |
| Interaction and state completeness | 5% |
| Maintainability and verification | 5% |

When criteria conflict, protect the primary task and hard gates first. Record any deliberate compromise that remains.

## Compact Workflow

1. Inspect the existing product, project conventions, design system, components, content, and constraints.
2. Identify the target users, primary task, content type, product category, brand constraints, required platforms, and input modes.
3. Select one primary design mode. Add at most one secondary influence when it improves fit.
4. Establish a one-sentence visual thesis, a compact content or information plan, and an interaction thesis only when meaningful interaction or motion is needed.
5. Reuse the project's established design system and components before creating new ones.
6. Design and implement the complete state model and the real content hierarchy.
7. Verify the rendered result at representative widths and with the relevant input methods.
8. Report evidence and unresolved limitations honestly.

Keep planning proportional. A small component change may need a few explicit decisions, not a lengthy design document.

## Design Mode Router

Choose the mode from the product's purpose, not from a fashionable aesthetic.

### Product or workspace

Use for applications, admin tools, and operational interfaces.

- Prefer utility-first copy and readable information density.
- Define clear workspace, navigation, and contextual regions.
- Keep colors and chrome restrained.
- Use cards only when grouping, containment, or interaction semantics justify them.
- Do not add a landing-page hero by default.

### Marketing or brand

Use for landing pages, launches, portfolios, and promotional sites.

- Establish a clear visual thesis and strong brand or product presence.
- Give each section one dominant visual idea.
- Keep the narrative concise and the conversion path clear.
- Use imagery purposefully and motion only when it supports the story.

### Data or dashboard

Use for analytics, monitoring, and decision-support interfaces.

- Optimize scanning, comparison, and status visibility.
- Structure filters, tables, charts, and drill-down paths around decisions.
- Keep dense layouts readable.
- Show freshness, units, scope, and empty or error states.
- Avoid decorative dashboard-card mosaics.

### Editorial or content

Use for articles, publications, documentation, and media-rich content.

- Maintain readable line length and strong typographic hierarchy.
- Provide clear content navigation.
- Place media deliberately.
- Use rhythm and whitespace to support sustained reading.

### Commerce or service

Use for shopping, booking, applications, onboarding, and transactional services.

- Prioritize trust, clarity, and familiar category structure.
- Make discovery, pricing, steps, commitments, and primary actions explicit.
- Prevent errors and provide recovery.
- Minimize distraction during critical flows.

### Immersive or experimental

Use only when the request and product context justify an expressive experience.

- Establish strong art direction and progressive enhancement.
- Apply animation and advanced effects selectively.
- Provide complete reduced-motion behavior.
- Preserve usable mobile, touch, and keyboard fallbacks.

Preloaders, smooth-scroll libraries, custom cursors, magnetic buttons, parallax, pinned sections, horizontal scroll journeys, WebGL, GSAP, Lenis, Framer Motion, and React Three Fiber are optional techniques, not quality requirements. Introduce one only when it materially supports the design objective and the project can afford its accessibility, performance, and maintenance cost.

## Universal Quality Rules

### Purpose, hierarchy, and content

- Make the page purpose and primary action clear.
- Preserve a logical reading order and familiar interaction patterns.
- Write content for the actual product surface; do not put prompt language or design commentary into the UI.
- Give each section or region a distinct job.
- Use progressive disclosure when complexity is necessary.
- Do not fabricate metrics, testimonials, claims, inventory, or user data.
- Make destructive actions reversible when possible and otherwise confirmable and recoverable.

### Visual coherence and distinctiveness

- Build one coherent system from typography, spacing, color, imagery, shape, and motion.
- Prefer useful distinctiveness over generic templates or decoration that competes with the task.
- Use visual complexity deliberately and remove elements that add no information, affordance, hierarchy, or atmosphere.
- Use cards only for meaningful grouping, containment, or interaction.
- Treat the 60-30-10 color rule as an optional palette-balancing heuristic, never a universal rule.
- For image-led work, select imagery that carries meaning, supports readable overlays, and fits the brand and content.
- Keep motion bounded, purposeful, and consistent with the interaction thesis.

## Accessibility Baseline

Use WCAG 2.2 Level AA as the baseline. Distinguish normative requirements from stronger recommendations.

### Normative baseline

- Prefer semantic HTML before ARIA.
- Provide accurate accessible names and descriptions.
- Make all functionality operable by keyboard with logical, visible focus and no keyboard traps.
- Restore focus after dialogs, deletion flows, and temporary overlays.
- Associate labels, instructions, validation errors, and status announcements with the controls or regions they describe.
- Meet text contrast of at least 4.5:1 for normal text and 3:1 for large text, plus 3:1 non-text contrast where WCAG requires it.
- Do not communicate meaning by color alone.
- Support reflow, 200% text resize, and zoom without losing content or functionality.
- Make pointer targets at least 24 by 24 CSS pixels or satisfy an applicable WCAG 2.2 AA exception such as spacing, inline, equivalent, user-agent, or essential presentation.
- Support touch, mouse, and keyboard when the product requires them.
- Honor reduced-motion preferences without using a blanket rule that breaks state-dependent transitions.
- Do not put essential information or actions behind hover alone.
- Make loading, empty, error, disabled, and success states perceivable and understandable.

### Stronger recommendations

- Prefer 44 by 44 CSS pixel targets for frequent, risky, or touch-primary actions when the layout permits it. This is stronger than the WCAG 2.2 AA 24-pixel minimum and aligns with the enhanced target-size criterion.
- Test with a real screen reader for important or complex workflows.
- Use the WAI-ARIA Authoring Practices Guide for complex widgets, then verify the implementation instead of treating an example as production-ready code.

Read [Accessibility Checklist](./references/accessibility-checklist.md) when the task includes forms, dialogs, complex widgets, destructive actions, dense data, or an accessibility review.

## Responsive and Adaptive Behavior

Design from content and available space rather than device names alone.

- Check a narrow mobile width, a wider mobile or tablet width, and a desktop width.
- Check zoom or enlarged text, coarse and fine pointers, and keyboard-only operation.
- Test long content, missing content, and localization expansion.
- Preserve reading order, priority, and controls as regions stack or reflow.
- Avoid a large mandatory breakpoint list. Add breakpoints where the content or interaction actually needs them.
- Do not hide essential functionality merely to make a narrow screenshot look clean.

## Performance and Resilience

When the application can be measured, use the current Core Web Vitals "good" targets as operational goals:

- LCP at or below 2.5 seconds.
- INP at or below 200 milliseconds.
- CLS at or below 0.1.
- Evaluate field results at the 75th percentile when field data exists.

Do not claim these targets passed without measurement. Distinguish lab observations from field evidence.

- Budget images, fonts, client JavaScript, third-party code, and animation dependencies.
- Reserve media dimensions and keep loading transitions stable.
- Prefer transform and opacity for animation where appropriate; avoid unnecessary layout work and scroll hijacking.
- Use progressive enhancement and preserve core tasks when optional media, scripts, or effects fail.
- Verify slow-loading, offline, stale-data, and retry behavior when relevant.

## Interaction and State Completeness

Model the states that users can actually encounter. Depending on the feature, cover:

- initial, loading, skeleton, and progressive states;
- empty, no-results, filtered-empty, and first-use states;
- success, partial success, stale, offline, and retry states;
- validation, permission, authentication, and server errors;
- hover, focus, active, selected, disabled, and busy controls;
- confirmation, cancellation, undo, and recovery for destructive actions.

Keep state transitions understandable. Announce meaningful asynchronous changes, prevent duplicate submission, retain recoverable user input, and never show success before the operation succeeds.

## Design Systems and Maintainability

- Reuse established components, spacing, typography, color, and interaction tokens.
- Add tokens when they reduce drift or support repeated themes and components; do not require a formal multi-tier token architecture for a small isolated surface.
- Avoid raw-value duplication, but do not refactor an entire application merely to satisfy this skill.
- Preserve existing brand and component contracts unless replacement is explicitly in scope.
- Keep framework mechanics in the React, Next.js, Vite, JavaScript, Tailwind, Figma, Stitch, or testing skill that owns them.
- Keep implementation examples short, syntactically valid, conceptually correct, and materially useful.

## Component Review Rubric

Apply this compact rubric before approving a component in React, Next.js, Vite, or another frontend stack:

1. **Contract and data ownership:** Props, events, state, side effects, validation, errors, and ownership boundaries are explicit.
2. **Complete states:** Relevant loading, empty, error, success, disabled, permission, stale, and responsive states exist.
3. **Accessibility and input methods:** Semantics, names, keyboard behavior, focus, contrast, touch, pointer, and reduced motion meet the baseline.
4. **Visual hierarchy and craft:** Typography, spacing, color, imagery, density, and motion support the component's job.
5. **Responsive behavior:** Content reflows without clipping, lost actions, broken order, or unjustified hiding.
6. **Performance implications:** Rendering, bundle cost, media, hydration, and animation costs are understood and proportionate.
7. **Project consistency:** The component reuses the project's system and does not introduce avoidable parallel patterns.
8. **Rendered verification:** The actual component is inspected at representative widths, states, and input methods.

## Resources

- [Accessibility Checklist](./references/accessibility-checklist.md): focused WCAG 2.2 AA checks and state-level verification.
- [Contrast Checker](./scripts/contrast-checker.py): local, standard-library color contrast calculations for individual colors or files.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/frontend-design` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the frontend-design skill without MCP. Inspect the local project and design system, implement the context-fit interface, then verify the rendered states, representative widths, accessibility, and performance evidence before concluding."
- Use an available browser or design MCP only when it improves inspection or verification; never invent a host capability.
- Without MCP, use the local source, project toolchain, browser developer tools, screenshots, the bundled contrast checker, and manual keyboard and responsive checks.

<!-- MCP:END -->

## Anti-Patterns

- Choosing a fashionable mode before understanding the users, task, content, and constraints.
- Replacing an established design system automatically.
- Treating landing-page heroes, cards, gradients, glass, or dark themes as universal defaults.
- Requiring expensive effects, animation libraries, custom cursors, smooth scrolling, or 3D for "premium" quality.
- Using decorative UI that competes with the primary task.
- Approving fake data, incomplete states, inaccessible controls, broken examples, or unmeasured performance claims.
- Treating a static screenshot, source inspection, or automated score as proof of complete rendered behavior.

## Verification Protocol

Before claiming the frontend-design workflow succeeded:

1. Pass/fail: The primary mode, visual thesis, content plan, and relevant constraints are explicit and fit the request.
2. Pass/fail: Functional correctness, WCAG 2.2 AA, valid examples, and responsive behavior clear every hard gate.
3. Pass/fail: The relevant component and page states are implemented with honest content and recoverable failure behavior.
4. Pass/fail: The actual rendered result was checked at representative widths and with keyboard plus relevant pointer or touch input.
5. Pass/fail: Performance costs were measured when possible and otherwise reported as unverified, not assumed.
6. Pressure test: Repeat the primary task with long content, enlarged text, reduced motion, a slow or failed dependency, and the narrowest supported width.
7. Success metric: Every approval cites rendered, behavioral, test, or measurement evidence and lists any remaining limitation.

## Related Skills

- [web-design-reviewer](../web-design-reviewer/SKILL.md): Use after implementation for browser-based visual QA and responsive defect diagnosis.
- [react-development](../react-development/SKILL.md): Use for React-specific component architecture and implementation.
- [nextjs-development](../nextjs-development/SKILL.md): Use for Next.js routing, rendering, data, and framework behavior.
- [vite-development](../vite-development/SKILL.md): Use for Vite configuration, build behavior, and app integration.
- [stitch-design](../stitch-design/SKILL.md): Use for Stitch-specific design and implementation workflows.
- [figma-implement-design](../figma-implement-design/SKILL.md): Use when implementation must follow a Figma source of truth.
