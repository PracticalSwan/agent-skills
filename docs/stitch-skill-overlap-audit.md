# Stitch Skill Overlap Audit

Date: 2026-06-15

Source: `https://github.com/google-labs-code/stitch-skills` at commit
`1544aa4a3be93e7515b0c27d32722f7ca5a2f691`.

## Outcome

All upstream Stitch skills were installed as folder-safe `stitch-*` maintained
skills. The previous local `stitch-design` skill overlapped with all of them,
so it was converted into a router instead of keeping duplicated long-form
workflow instructions.

No permission stop was required for the completed consolidation because no
important workflow was deleted. The broad duplicated sections were moved into
narrower dedicated skills, and the old entrypoint now points to those skills.

## Verified MCP Correction

The active Stitch MCP surface in this workspace exposes:

- `create_project`
- `upload_design_md`
- `create_design_system_from_design_md`
- `list_design_systems`
- `apply_design_system`

The upstream skills referenced additional screen lookup, generation, editing,
and variant tools. Those were corrected in the local `SKILL.md` files and
support references: agents may use those broader tools only when the current
host explicitly exposes them.

## Safe Consolidation Applied

| Skill | What it does | Overlap found | What changed | Why this is better |
|---|---|---|---|---|
| `stitch-design` | Routes Google Stitch tasks to the right workflow. | The old file repeated design-md, React conversion, stitch-loop, prompt enhancement, Remotion, and shadcn/ui details. | Removed duplicated workflow bodies and replaced them with route selection plus shared Stitch MCP safety rules. | The entrypoint is now small, less ambiguous, and points agents to the narrowest skill. |
| `stitch-code-to-design` | Orchestrates static HTML extraction, DESIGN.md extraction, design-system creation, and upload. | Overlaps with `stitch-extract-static-html`, `stitch-extract-design-md`, `stitch-manage-design-system`, and `stitch-upload-to-stitch`. | Kept as an orchestrator and linked to those narrower skills instead of duplicating their full instructions. | End-to-end migration remains available while each step stays independently verifiable. |

## Installed Stitch Skills

| Skill | What it does | Overlap or redundancy judgment |
|---|---|---|
| `stitch-code-to-design` | Converts an existing frontend into Stitch-ready assets. | Intentional orchestrator over four narrower skills; kept separate because it defines sequence and handoffs. |
| `stitch-generate-design` | Prepares Stitch generation, edit, image-to-design, and variant prompts. | Overlaps with `stitch-enhance-prompt` and `stitch-loop`; kept separate for single-screen generation/editing. |
| `stitch-manage-design-system` | Creates, lists, and applies Stitch design systems from DESIGN.md. | Overlaps with DESIGN.md-producing skills; kept separate because it is the verified MCP-backed upload/create/apply workflow. |
| `stitch-extract-design-md` | Extracts DESIGN.md from frontend source code. | Overlaps with `stitch-design-md`; kept separate because its input is source code, not Stitch project evidence. |
| `stitch-extract-static-html` | Captures self-contained static HTML from a running app or mock state. | Overlaps with `stitch-code-to-design`; kept separate because local capture must be verified before upload. |
| `stitch-upload-to-stitch` | Uploads approved HTML, markdown, or image assets. | Overlaps with design-system creation; kept separate because it centralizes external upload and credential safety. |
| `stitch-react-components` | Converts Stitch exports into React/TypeScript components. | Overlaps with `react-development` and `frontend-design`; kept separate because Stitch asset mapping and `.stitch/` evidence are specific. |
| `stitch-react-native` | Converts Stitch HTML into React Native screens. | Overlaps with `stitch-react-components`; kept separate because native primitives and platform checks differ materially. |
| `stitch-remotion` | Builds Remotion walkthrough videos from Stitch screens. | Overlaps with screen export workflows; kept separate because the output is a video artifact, not app code. |
| `stitch-shadcn-ui` | Implements Stitch-derived UI with shadcn/ui components. | Overlaps with general React and frontend skills; kept separate because shadcn has its own CLI, registry, and ownership model. |
| `stitch-design-md` | Synthesizes DESIGN.md from Stitch project evidence. | Overlaps with `stitch-extract-design-md`; kept separate because it starts from Stitch exports/screenshots/metadata. |
| `stitch-enhance-prompt` | Turns vague UI requests into structured Stitch prompts. | Overlaps with `stitch-generate-design`; kept separate because prompt polishing is reusable without generation. |
| `stitch-loop` | Runs a baton-based multi-page Stitch website loop. | Overlaps with `stitch-generate-design`; kept separate because it manages continuity, SITE.md, and next-prompt handoff. |
| `stitch-taste-design` | Drafts opinionated premium DESIGN.md guidance. | Overlaps with `premium-frontend-ui`; kept separate because it outputs Stitch-ready design-system language. |

## Permission-Gated Merge Candidates

These were identified as overlaps but not combined because doing so would
remove important behavior or blur activation boundaries.

| Candidate merge | Why removal would be risky | Current decision |
|---|---|---|
| Merge `stitch-design-md` into `stitch-extract-design-md`. | One analyzes Stitch project evidence; the other reads source code. Combining them would hide the input distinction and could cause unsupported claims. | Keep separate; cross-link both. |
| Merge `stitch-generate-design` into `stitch-loop`. | Single-screen generation/editing and multi-page baton iteration have different completion criteria. | Keep separate; `stitch-loop` calls `stitch-generate-design` when needed. |
| Merge `stitch-react-components` and `stitch-react-native`. | React DOM and React Native have different primitives, styling, accessibility, and validation paths. | Keep separate. |
| Merge `stitch-shadcn-ui` into `react-development` or `frontend-design`. | shadcn/ui uses copied component ownership, registry setup, and Tailwind CSS variable rules that general skills should not absorb. | Keep separate. |
| Merge `stitch-taste-design` into `premium-frontend-ui`. | The Stitch skill produces DESIGN.md semantic language and upload-ready constraints; the general skill gives broader UI direction. | Keep separate. |
| Delete `stitch-design` entirely. | Existing prompts may activate `stitch-design`; removing it would break discoverability. | Keep as router. |

## User-Facing Notes

- The completed combination is non-lossy: important guidance moved from one
  broad skill into dedicated skills.
- Future destructive consolidation, such as deleting one of the dedicated
  skills above, should ask the user first and explain what behavior would be
  lost.
- Stitch MCP verification should be framed precisely: current MCP verification
  can prove project/design-system workflows, while screen generation workflows
  need host-specific tools or the Stitch web UI.
