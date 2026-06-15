# Stitch Design-System Tool Schemas

These examples match the Stitch MCP design-system tools verified in this
workspace on 2026-06-15.

## `upload_design_md`

Uploads UTF-8 DESIGN.md content to a project. Base64-encode the file content
before calling the tool.

```json
{
  "projectId": "4044680601076201931",
  "designMdBase64": "IyBEZXNpZ24gU3lzdGVtOiBGb29kaWVIdWI..."
}
```

Expected result: a selected screen instance payload with:

```json
{
  "id": "screen-instance-id",
  "sourceScreen": "projects/4044680601076201931/screens/source-screen-id"
}
```

Pass those values directly to `create_design_system_from_design_md`.

## `create_design_system_from_design_md`

Creates and displays a design system from the uploaded DESIGN.md.

```json
{
  "projectId": "4044680601076201931",
  "deviceType": "DESKTOP",
  "selectedScreenInstance": {
    "id": "screen-instance-id",
    "sourceScreen": "projects/4044680601076201931/screens/source-screen-id"
  }
}
```

## `list_design_systems`

Lists design systems for a project.

```json
{
  "projectId": "4044680601076201931"
}
```

Use the returned asset name to derive `assetId` when applying a design system.
For example, `assets/15996705518239280238` means the `assetId` is
`15996705518239280238`.

## `apply_design_system`

Applies a design system to selected screen instances.

```json
{
  "projectId": "4044680601076201931",
  "assetId": "15996705518239280238",
  "selectedScreenInstances": [
    {
      "id": "screen-instance-id",
      "sourceScreen": "projects/4044680601076201931/screens/source-screen-id"
    }
  ]
}
```

Only include `id` and `sourceScreen` for each selected screen instance. Do not
include position, dimensions, title, or other project metadata.

## Large File Fallback

For large DESIGN.md files or non-markdown uploads, use
`stitch-upload-to-stitch/scripts/upload_to_stitch.py` only after the user has
approved the exact file, target project, and credential path. Never print,
store, or commit API keys.
