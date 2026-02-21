# Stitch MCP Command Reference

Quick reference for all Stitch MCP tools available for design project management and screen generation.

## Commands

### `mcp_stitch_list_projects`

Lists all Stitch projects accessible to the user.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filter` | string | No | AIP-160 filter. `view=owned` (default), `view=shared` |

**Response Format:**
```json
{
  "projects": [
    {
      "name": "projects/4044680601076201931",
      "projectId": "4044680601076201931",
      "title": "My Design Project",
      "createTime": "2025-01-15T10:30:00Z",
      "updateTime": "2025-02-01T14:20:00Z"
    }
  ]
}
```

**Usage Examples:**
```
// List your own projects
mcp_stitch_list_projects()

// List projects shared with you
mcp_stitch_list_projects({ filter: "view=shared" })
```

---

### `mcp_stitch_get_project`

Retrieves detailed information about a specific project by name or title.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectName` | string | Yes | Project title or full resource name |

**Response Format:**
```json
{
  "name": "projects/4044680601076201931",
  "projectId": "4044680601076201931",
  "title": "FoodieHub",
  "screens": [...],
  "createTime": "2025-01-15T10:30:00Z"
}
```

**Usage Examples:**
```
// Get project by title
mcp_stitch_get_project({ projectName: "FoodieHub" })
```

---

### `mcp_stitch_list_screens`

Lists all screens within a specified project.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectId` | string | Yes | Project ID (numeric, without `projects/` prefix) |

**Response Format:**
```json
{
  "screens": [
    {
      "screenId": "98b50e2ddc9943efb387052637738f61",
      "name": "Home Page",
      "deviceType": "DESKTOP",
      "html": "<div>...</div>",
      "imageUrl": "https://..."
    }
  ]
}
```

**Usage Examples:**
```
// List all screens in a project
mcp_stitch_list_screens({ projectId: "4044680601076201931" })
```

---

### `mcp_stitch_create_project`

Creates a new Stitch project container for UI designs.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | No | Project title |

**Response Format:**
```json
{
  "name": "projects/5678901234567890123",
  "projectId": "5678901234567890123",
  "title": "New Project"
}
```

**Usage Examples:**
```
mcp_stitch_create_project({ title: "E-Commerce Redesign" })
```

---

### `mcp_stitch_edit_screens`

Edits existing screens using a text prompt. Can take several minutes to complete.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `projectId` | string | Yes | Project ID (without `projects/` prefix) |
| `selectedScreenIds` | string[] | Yes | Screen IDs to edit (without `screens/` prefix) |
| `prompt` | string | Yes | Text prompt describing desired changes |
| `deviceType` | string | No | `MOBILE`, `DESKTOP`, `TABLET`, `AGNOSTIC` |
| `modelId` | string | No | `GEMINI_3_PRO` or `GEMINI_3_FLASH` |

**Usage Examples:**
```
mcp_stitch_edit_screens({
  projectId: "4044680601076201931",
  selectedScreenIds: ["98b50e2ddc9943efb387052637738f61"],
  prompt: "Add a dark mode toggle in the top navigation bar",
  deviceType: "DESKTOP"
})
```

> **Warning:** This action can take several minutes. Do NOT retry on timeout.

---

## Workflow Patterns

### Discovery Workflow

Standard approach for exploring a Stitch workspace:

```
Step 1: List all projects
  mcp_stitch_list_projects()

Step 2: Get project details (use title from step 1)
  mcp_stitch_get_project({ projectName: "FoodieHub" })

Step 3: List screens (use projectId from step 2)
  mcp_stitch_list_screens({ projectId: "4044680601076201931" })

Step 4: Extract design tokens from screen HTML/JSON
  Parse colors, fonts, spacing from the screen response data
```

### Design Token Extraction

When screen data is returned, extract design tokens from the HTML content:

```
1. Colors:
   - Search for hex codes (#RRGGBB), rgb(), hsl() values
   - Look for Tailwind classes (bg-*, text-*, border-*)
   - Map to semantic roles (primary, secondary, accent, background)

2. Typography:
   - Extract font-family declarations
   - Identify heading sizes (text-xs through text-9xl)
   - Note font-weight patterns

3. Spacing:
   - Identify padding/margin patterns (p-*, m-*, gap-*)
   - Map to a consistent spacing scale

4. Components:
   - Identify recurring UI patterns (cards, buttons, nav items)
   - Note border-radius, shadow, and border patterns
```

### Iterative Edit Loop

For autonomous multi-screen editing:

```
1. List screens to get current state
2. Identify screens needing changes
3. Edit screens with specific prompt
4. Wait for completion (do not retry)
5. List screens again to verify changes
6. Repeat if further adjustments needed
```

## Tips for Reliable Data Extraction

- **Always list projects first** before attempting to get a specific project
- **Store project IDs** — use the numeric ID, not the full resource name
- **Screen IDs have no prefix** — strip `screens/` if present in any response
- **HTML parsing** — screen HTML can be large; focus on extracting class names and inline styles for design tokens
- **Timeout handling** — `edit_screens` is slow; never retry a timed-out call, check the project state instead
- **Device types** — always specify `deviceType` for consistent output; `DESKTOP` is safest for full layouts
- **Model selection** — `GEMINI_3_PRO` produces higher quality; `GEMINI_3_FLASH` is faster for iterative edits
