# Stitch MCP Tool Reference

This reference records the Stitch MCP surface verified in this workspace on
2026-06-15. Treat any broader screen lookup, screen generation, screen editing,
or variant tools as host-specific optional tools. Use them only when they appear
in the active tool list for the current session.

## Verified Tools

### `create_project`

Creates a Stitch project container.

```json
{
  "title": "Catalog Verification"
}
```

Expected result: a project resource name such as `projects/1234567890`, plus a
numeric project ID that can be used by the other Stitch tools.

### `upload_design_md`

Uploads UTF-8 DESIGN.md content to a project. The markdown must be base64
encoded before the tool call.

```json
{
  "projectId": "1234567890",
  "designMdBase64": "IyBEZXNpZ24gU3lzdGVt..."
}
```

Expected result: a selected screen instance payload containing `id` and
`sourceScreen`. Pass those values directly to
`create_design_system_from_design_md`.

### `create_design_system_from_design_md`

Creates a Stitch design system from a previously uploaded DESIGN.md screen.

```json
{
  "projectId": "1234567890",
  "deviceType": "DESKTOP",
  "selectedScreenInstance": {
    "id": "screen-instance-id",
    "sourceScreen": "projects/1234567890/screens/source-screen-id"
  }
}
```

### `list_design_systems`

Lists design-system assets. Pass `projectId` to scope the list to one project,
or omit it only when the current task explicitly needs global design systems.

```json
{
  "projectId": "1234567890"
}
```

### `apply_design_system`

Applies an existing design-system asset to selected screen instances.

```json
{
  "projectId": "1234567890",
  "assetId": "9876543210",
  "selectedScreenInstances": [
    {
      "id": "screen-instance-id",
      "sourceScreen": "projects/1234567890/screens/source-screen-id"
    }
  ]
}
```

Only pass `id` and `sourceScreen` inside each selected screen instance. Do not
include canvas position, width, height, or other project metadata.

## Optional Host-Specific Tools

Some upstream Stitch skill references mention tools for listing projects,
listing screens, reading screen HTML, generating screens, editing screens, or
generating variants. Those tools are not part of the verified Stitch MCP surface
in this workspace. If a future host exposes them, verify the exact names and
schemas from that host before use.

## Fallback Pattern

When a needed Stitch action is outside the verified MCP surface:

1. Use local `.stitch/` artifacts, screenshots, exported HTML, or DESIGN.md
   files as evidence.
2. Use the Stitch web UI or an approved API script for screen generation,
   screen editing, or asset upload.
3. State clearly which parts were MCP-backed, local-only, or manual.
4. Never claim an optional screen tool ran unless it was present and actually
   called.
