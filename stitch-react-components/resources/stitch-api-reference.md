# Stitch Export Reference

This reference describes the screen asset shape expected by the React component
conversion workflow. In this workspace, Stitch MCP screen retrieval is not a
verified tool, so these fields usually come from Stitch web exports, local
`.stitch/designs/` files, or a future host-specific screen retrieval tool that
has been explicitly listed in the active tool set.

## Expected Asset Fields

- `htmlCode.downloadUrl` or local HTML path: source markup for component and
  token extraction.
- `screenshot.downloadUrl` or local screenshot path: visual reference for
  layout, spacing, and responsive intent.
- `deviceType`: target device class such as `DESKTOP`, `MOBILE`, or `TABLET`.
- `width` and `height`: viewport dimensions used for screenshot capture and
  responsive breakpoints.

## Technical Mapping Rules

1. Preserve `data-stitch-id` values as comments only when they are present and
   useful for future design synchronization.
2. Treat background images and remote media URLs as data. Extract them into
   `mockData.ts` rather than hardcoding them into component styles.
3. If exported HTML contains an inline Tailwind config, merge its theme values
   into the local project theme before using classes such as `primary` or
   `background-dark`.
4. If asset fields came from an optional host-specific tool, record the exact
   tool name and response shape in the task notes.
