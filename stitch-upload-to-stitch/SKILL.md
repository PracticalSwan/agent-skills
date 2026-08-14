---
name: stitch-upload-to-stitch
version: "2.0"
last_updated: 2026-08-14
tags: [stitch, upload, assets, html, mcp]
description: "Upload approved local HTML, markdown, or image assets to a Stitch project using direct MCP for small DESIGN.md files or the bundled API script for larger files."
license: "Apache-2.0"
---
# Upload-to-Stitch

Upload local assets (images, mockups, HTML, and markdown files) to a Stitch project using the
provided upload script, which bypasses the MCP tool's base64 output token limits.

> [!NOTE]
> The AI model cannot upload files via MCP tools directly because the base64
> encoding of even a small file exceeds the model's output token limit (~16K
> tokens). This script reads the file and sends it directly over HTTP.

## Steps

### 1. Identify Target Project

Use `list_projects` to find the correct `projectId`.

### 2. Get the API Key

Locate the active Stitch MCP configuration or approved secret store and use
the configured API key without printing or copying it into chat. Claude Code
typically keeps its MCP configuration in `~/.claude.json`; Codex and other
hosts may expose an equivalent active configuration or environment secret.

Extract:
- **API Key**: From the `X-Goog-Api-Key` header or auth argument
- **MCP URL** (optional): From the `httpUrl` or endpoint argument (defaults to
  `https://stitch.googleapis.com`)

> [!IMPORTANT]
> If no approved secret source is available, stop and report the blocker. Do
> not ask the user to paste an API key into chat and do not proceed with a
> guessed or exposed credential.

### 3. Run Upload Script

> [!WARNING]
> **Checkpoint — User Confirmation Required.**
> Before running the upload script, you **MUST** pause and present the file(s)
> to be uploaded (paths, sizes, and types) to the user and wait for explicit
> approval. Do **NOT** execute the upload script until the user confirms.

Use `run_command` to execute the Python script:

```bash
python3 <SKILL_DIR>/scripts/upload_to_stitch.py \
  --project-id <PROJECT_ID> \
  --file-path <PATH_TO_FILE> \
  --api-key <API_KEY> \
  [--api-url <STITCH_API_URL>] \
  [--title <SCREEN_TITLE>] \
  [--generated-by <GENERATED_BY>]
```

> [!TIP]
> **macOS / SSL Certificate Troubleshooting:**
> If the upload fails with `ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] unable to get local issuer certificate`, this means your Python installation does not have root certificate authorities configured.
>
> The script automatically attempts to use the `certifi` package to load the CA bundle if it is installed in your python environment. If `certifi` is not installed, you can either install it (`pip install certifi`) or manually supply the `SSL_CERT_FILE` environment variable when running the script:
> ```bash
> SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())") python3 <SKILL_DIR>/scripts/upload_to_stitch.py \
>   --project-id <PROJECT_ID> \
>   --file-path <PATH_TO_FILE> \
>   --api-key <API_KEY> \
>   [--api-url <STITCH_API_URL>] \
>   [--title <SCREEN_TITLE>] \
>   [--generated-by <GENERATED_BY>]
> ```

### Supported File Types

| Extension | MIME Type |
|:---|:---|
| `.png` | `image/png` |
| `.jpg`, `.jpeg` | `image/jpeg` |
| `.webp` | `image/webp` |
| `.html`, `.htm` | `text/html` |
| `.md` | `text/markdown` |

The script auto-detects MIME type from the file extension.

### Script Options

- `--project-id`: **Required**. The Stitch project ID.
- `--file-path`: **Required**. Path to the local file to upload.
- `--api-key`: **Required**. API key for Stitch authorization.
- `--api-url`: Optional. Base URL of the Stitch API. Defaults to `https://stitch.googleapis.com`.
- `--title`: Optional. Title for the uploaded screen. When uploading extracted HTML from a web app, set this to the **route path** of the page (e.g., `'/dashboard'`, `'/settings/profile'`, `'/inbox'`) so that the screen name/title in Stitch clearly identifies the route.
- `--generated-by`: Optional. Specify how the uploaded file was generated (for
  example, `stitch::extract-static-html`, `Claude Code`, or `Codex`).

## Anti-Patterns

- Claiming a Stitch screen-generation, screen-editing, or screen-retrieval MCP call succeeded when the active host does not expose that tool.
- Uploading files, screenshots, HTML, markdown, or design assets to Stitch without user-approved destination and artifact details.
- Reading, printing, storing, or committing Stitch API keys, MCP config secrets, cookies, or credential-bearing files.
- Treating generated design or code as final without local render, syntax, or artifact verification.
- Collapsing this workflow into a broader frontend/design skill when Stitch-specific files, project IDs, or design-system assets matter.

## Verification Protocol

Before claiming this skill was applied successfully:

1. Pass/fail: The file type is supported: `.html`, `.htm`, `.md`, `.png`, `.jpg`, `.jpeg`, or `.webp`.
2. Pass/fail: User approval covers the actual file and destination project.
3. Pass/fail: The response returned expected IDs, or the failure response is captured without leaking secrets.
4. Pass/fail: Local metadata was updated without credentials.
5. Pressure-test scenario: Repeat the workflow with Stitch MCP screen tools unavailable and confirm the fallback path remains honest and actionable.
6. Success metric: The user can identify the exact artifact, project/design-system target, and verification evidence without relying on unstated MCP behavior.

<!-- MCP:START -->

<!-- PORTABILITY:START -->

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/stitch-upload-to-stitch` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: Stitch MCP

- Fallback prompt: "Use the Stitch Upload To Stitch skill without Stitch MCP. Use the Stitch web UI for manual upload when API credentials are unavailable or external upload risk needs review. Show the exact files, commands, manual Stitch UI steps, and verification evidence used before concluding."
- Verified Stitch MCP tools in this workspace are design-system/project oriented; use broader screen tools only when the current host exposes them.
- Use local scripts, exported HTML/screenshots, the Stitch web UI, and project metadata files as the fallback evidence path.

<!-- MCP:END -->

## Related Skills

- [stitch-code-to-design](../stitch-code-to-design/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-manage-design-system](../stitch-manage-design-system/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
- [stitch-extract-static-html](../stitch-extract-static-html/SKILL.md): Use when the task also needs this adjacent Stitch workflow.
