---
name: web-design-reviewer
version: "1.2"
last_updated: 2026-04-25
tags: [web, design, reviewer, frontend, ui]
description: "Visual inspection of live websites to find and fix design issues. Use when reviewing UI layout/design, checking responsive design visually, detecting visual inconsistencies, or diagnosing CSS/accessibility problems at the source code level. Not for automated E2E testing."
---

# Web Design Reviewer

Use this skill for visual QA and source-level fixes after a page is already running. This is not the right skill for functional automation or regression suites.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Reviewing a live page for layout or spacing defects
- Checking responsive behavior at a few critical widths
- Comparing a page to a design system or visual target
- Tracing a visible issue back to CSS, Tailwind classes, or component structure

## Recommended Workflow

1. Open the page with a browser-capable MCP client such as Playwright MCP.
2. Capture the current state before editing.
3. Test desktop and mobile widths.
4. Fix the source code, then re-check the same viewports.

## Playwright MCP Mapping

These tool names are current in the Playwright MCP server used by Codex:

- `browser_navigate` to open the page
- `browser_snapshot` to inspect accessible structure
- `browser_take_screenshot` for before and after captures
- `browser_resize` for responsive review
- `browser_console_messages` and `browser_network_requests` to catch front-end breakage

## Anti-Patterns

- Starting from a generic template without adapting it: The output may look polished but still miss the real audience or medium.
- Ignoring final render or export review: Layout bugs often appear only after the asset is opened in its destination tool.
- Fixing content and presentation in one pass: It becomes hard to tell whether a problem is structural or visual.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Web Design Reviewer guidance is tied to a concrete route, component, screen, or design artifact.
2. Pass/fail: Component states cover loading, empty, error, success, and responsive breakpoints where applicable.
3. Pass/fail: Accessibility, visual hierarchy, and interaction behavior are reviewed against the shared component rubric.
4. Pressure-test scenario: Review the component on a narrow mobile viewport, keyboard-only path, and slow-loading state.
5. Success metric: Zero generic UI approval; every approval cites rendered behavior or source evidence.


## Review Checklist

- [ ] No overflow or clipped content at target widths
- [ ] Interactive controls remain visible and reachable
- [ ] Text contrast and focus states are acceptable
- [ ] Repeated components use consistent spacing, typography, and color
- [ ] Fixes were verified visually after the code change

## References & Resources

### Documentation
- [Visual Checklist](./references/visual-checklist.md) - High-signal items for layout, contrast, spacing, and responsive review
- [Framework Fixes](./references/framework-fixes.md) - Typical fix locations for CSS, Tailwind, CSS modules, and component styles

### Scripts
- [CSS Risk Audit](./scripts/css-risk-audit.py) - Scan CSS and front-end source for risky fixed widths, viewport traps, and overflow patterns

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:web-design-reviewer` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py web-design-reviewer` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Playwright MCP

- Fallback prompt: "Use the Web Design Reviewer skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use Playwright CLI, browser devtools, screenshots, and manual responsive checks when MCP browser tools are unavailable.
- Capture console or network issues with the browser or terminal before proposing visual fixes.

<!-- MCP:END -->

## Related Skills

- [frontend-design](../frontend-design/SKILL.md): Use it when the workflow also needs UI composition and front-end design direction.
- [premium-frontend-ui](../premium-frontend-ui/SKILL.md): Use it when the workflow also needs high-fidelity UI polish and interaction detail.
- [stitch-design](../stitch-design/SKILL.md): Use it when the workflow also needs turning interface designs into implementation-ready assets.
- [canvas-design](../canvas-design/SKILL.md): Use it when the workflow also needs visual composition and presentation-ready diagram work.
