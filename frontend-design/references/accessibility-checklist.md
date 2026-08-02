# WCAG 2.2 Accessibility Checklist

Use this reference for interface work that needs more detail than the core `frontend-design` workflow. WCAG 2.2 Level AA is the baseline. Automated tools help find defects but do not replace keyboard, screen-reader, zoom, and rendered-state checks.

Primary references:

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- Target Size (Minimum), Level AA: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum
- Target Size (Enhanced), Level AAA: https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced

## Semantics and Structure

- [ ] Use native HTML elements and controls before custom roles.
- [ ] Provide one clear page title, language declaration, landmarks, and logical heading structure.
- [ ] Preserve a DOM and reading order that matches the visual and focus order.
- [ ] Use real lists, tables, fieldsets, legends, labels, and buttons when those semantics fit.
- [ ] Give informative images useful alternatives and decorative images empty alternatives.
- [ ] Give every interactive control an accurate accessible name; add a description only when the name is insufficient.
- [ ] Validate IDs, element nesting, ARIA roles, states, properties, and references.

## Keyboard and Focus

- [ ] Reach and operate every interactive control with the keyboard.
- [ ] Use Enter, Space, arrow, Home, End, and Escape behavior appropriate to the native control or documented widget pattern.
- [ ] Do not create keyboard traps.
- [ ] Keep focus visible against adjacent colors and surfaces.
- [ ] Keep focus order logical when CSS changes visual order.
- [ ] Move focus deliberately when a new context requires it; do not move focus for routine updates.
- [ ] Trap focus only inside a true modal interaction.
- [ ] Return focus to the invoking control, the next logical control, or a stable recovery point after a dialog, deletion, or temporary overlay closes.
- [ ] Provide a skip path when repeated navigation precedes the main content.

For complex widgets such as comboboxes, menus, tabs, grids, trees, and modal dialogs, follow the relevant WAI-ARIA APG pattern and verify the implementation. APG examples are illustrative, not a production UI library.

## Names, Labels, Errors, and Status

- [ ] Keep visible labels associated with their controls; do not use placeholder text as the only label.
- [ ] Identify required fields in text or semantics, not by color alone.
- [ ] Connect instructions, hints, errors, and units to the relevant control.
- [ ] Identify errors in text and provide a correction path when one is known.
- [ ] Preserve entered data after validation or service errors whenever safe.
- [ ] Announce meaningful asynchronous results, errors, progress, and completion without stealing focus unnecessarily.
- [ ] Prevent duplicate submission and expose busy or disabled state accurately.
- [ ] Do not announce success until the operation has succeeded.

## Contrast and Color

- [ ] Normal text and images of text meet at least 4.5:1 contrast.
- [ ] Large text and images of large text meet at least 3:1 contrast.
- [ ] Active UI components, meaningful graphics, and focus indicators meet applicable 3:1 non-text contrast requirements.
- [ ] Color is not the only way to communicate state, category, validation, or selection.
- [ ] Text over images remains readable across responsive crops and image-loading states.
- [ ] Forced-colors and high-contrast modes preserve meaning and focus where the target platform supports them.

Inactive controls are excepted from WCAG text contrast requirements, but they must still be understandable as unavailable. Do not misstate a stronger visual recommendation as a Level AA requirement.

Use `../scripts/contrast-checker.py` for deterministic color-pair calculations. Confirm the sampled colors match the rendered foreground, background, opacity, and state.

## Zoom, Reflow, and Text

- [ ] Resize text to 200% without loss of content or functionality.
- [ ] Check browser zoom and the WCAG reflow condition relevant to the surface.
- [ ] Avoid fixed heights that clip translated, enlarged, or user-generated text.
- [ ] Test long labels, long words, URLs, error messages, and localization expansion.
- [ ] Keep essential controls and content available without two-dimensional scrolling except where the content itself requires it, such as maps or wide data tables.
- [ ] Preserve a readable line length and spacing without disabling user overrides.

## Pointer and Target Size

- [ ] Meet the WCAG 2.2 Level AA target-size requirement: at least 24 by 24 CSS pixels or a valid spacing, equivalent, inline, user-agent, or essential exception.
- [ ] Prefer at least 44 by 44 CSS pixels for frequent, risky, edge-positioned, or touch-primary actions when practical. Treat this as stronger guidance, not the Level AA minimum.
- [ ] Keep adjacent destructive and safe actions distinct and difficult to trigger accidentally.
- [ ] Support coarse and fine pointers without relying on hover.
- [ ] Make drag operations optional or provide a non-drag alternative where WCAG requires one.
- [ ] Avoid path-based gestures unless a simpler alternative exists.

## Motion and Time

- [ ] Honor `prefers-reduced-motion` with a designed alternative.
- [ ] Remove non-essential parallax, auto-animation, and scroll-linked motion in reduced-motion mode.
- [ ] Preserve necessary state transitions; do not use a blanket zero-duration rule that breaks visibility or focus behavior.
- [ ] Provide pause, stop, or hide controls for moving, blinking, scrolling, or auto-updating content when required.
- [ ] Avoid flashes that can trigger seizures.
- [ ] Let users extend or disable time limits unless an exception applies.

## Media and Visual Content

- [ ] Provide captions for prerecorded synchronized media and other alternatives required by the content.
- [ ] Provide transcripts or descriptions where they are needed to convey equivalent information.
- [ ] Avoid autoplay with sound; provide obvious playback controls.
- [ ] Preserve media controls at zoomed and narrow layouts.
- [ ] Do not encode essential text inside imagery when real text can be used.

## State Coverage

Verify accessibility in every relevant state, not only the happy path:

- [ ] initial, loading, busy, and progressive content;
- [ ] empty, no-results, and first-use;
- [ ] validation, permission, authentication, and server errors;
- [ ] success, partial success, stale, offline, and retry;
- [ ] hover, focus, active, selected, disabled, and read-only;
- [ ] modal, drawer, popover, toast, and temporary overlay;
- [ ] confirmation, cancellation, undo, and post-deletion focus recovery.

## Representative Manual Verification

1. Navigate the complete primary workflow with the keyboard only.
2. Repeat the workflow with a screen reader appropriate to the target platform.
3. Inspect accessible names, roles, states, relationships, and announcements.
4. Test 200% text size, browser zoom, narrow reflow, and long content.
5. Check normal, focus, hover, disabled, error, and success colors.
6. Test reduced motion and coarse-pointer behavior.
7. Run an automated accessibility scanner and investigate each relevant result.
8. Recheck after fixes and report which checks were manual, automated, measured, or unverified.

## Completion Evidence

Record the routes or components checked, representative widths, input methods, assistive technology and versions when used, automated tools, confirmed failures fixed, remaining limitations, and any WCAG exception relied upon. Do not claim WCAG conformance from a single score or static source review.
