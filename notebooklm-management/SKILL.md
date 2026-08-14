---
name: notebooklm-management
version: "2.0"
last_updated: 2026-08-14
tags: [research, management, documents, automation, productivity]
description: "NotebookLM MCP server management - query notebooks, add from share links, handle auth, reset sessions. Use when working with Google NotebookLM notebooks for conversational research tasks."
---
# NotebookLM MCP Management

> Tech Stack Target / Version: NotebookLM current web release, Markdown session capture, and URL-tracked research workflows.

Use this skill when research should be grounded in NotebookLM notebooks instead of a generic web search.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Current MCP Reality

This repository already targets a real NotebookLM MCP workflow. The concrete tool surface available in this environment includes:

- `get_health`
- `list_notebooks`, `search_notebooks`, `select_notebook`
- `ask_question`
- `add_notebook`, `update_notebook`, `remove_notebook`
- `list_sessions`, `reset_session`, `close_session`
- `setup_auth`, `re_auth`, `cleanup_data`

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Querying a specific NotebookLM notebook
- Adding a notebook from a share URL
- Managing a notebook library or switching active notebooks
- Recovering authentication or cleaning NotebookLM state
- Continuing a multi-turn research session

## Recommended Workflow

1. Call `get_health` first to confirm authentication and server readiness.
2. Reuse an existing session when the task is the same.
3. Prefer `search_notebooks` or `list_notebooks` before asking the user to restate what is already in the library.
4. Use `ask_question` iteratively in the same session for deep work.
5. Use `setup_auth` or `re_auth` only when health indicates auth problems.

## Library Management Rules

- Do not add or remove notebooks without explicit user confirmation.
- When adding a notebook, collect URL, description, topics, and use cases first.
- Update metadata instead of creating duplicates when the notebook already exists.

## Troubleshooting

- Auth broken: `get_health` -> `re_auth`
- Stale browser state: `cleanup_data(preserve_library=true)` after closing browsers
- Wrong context: `reset_session` or switch notebooks
- Ambiguous notebook choice: search the library before creating a new one

## Anti-Patterns

- Treating source content as already clean: Formatting automation will happily preserve broken or inconsistent input.
- Skipping an open-file verification pass: Documents and spreadsheets often fail in the destination app, not in the script output.
- Automating irreversible edits without checkpoints: A small mapping mistake can affect an entire workbook or document.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Notebooklm Management workflow names the agent boundary, delegated scope, and expected return artifact.
2. Pass/fail: Context passed to helpers is minimal, task-local, and free of hidden expected answers.
3. Pass/fail: Results are integrated only after evidence, diffs, or citations are checked by the controller.
4. Pressure-test scenario: Run the workflow on two similar tasks that must not share assumptions or leaked context.
5. Success metric: Zero context leakage; every delegated output is independently reviewable.

## References & Resources

### Documentation
- [MCP Tool Reference](./references/mcp-tool-reference.md) - Current NotebookLM MCP operations and parameters
- [Troubleshooting Guide](./references/troubleshooting.md) - Auth recovery, cleanup, and session issues
- [Workflows](./references/workflows.md) - Library, query, and maintenance workflows

### Scripts
- [NotebookLM Helper](./scripts/notebooklm-helper.py) - Local helper for library exports and reporting when MCP access is unavailable
- [Scripts README](./scripts/README.md) - Quick commands for the helper script

### Examples
- [simple-query.py](./examples/simple-query.py) - Basic query pattern
- [multi-turn-conversation.py](./examples/multi-turn-conversation.py) - Session reuse pattern
- [library-management.py](./examples/library-management.py) - Library search and organization

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/notebooklm-management` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: NotebookLM MCP

- Fallback prompt: "Use the NotebookLM MCP Management skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use the NotebookLM web UI directly, capture answers in Markdown, and store session notes locally when the MCP server is unavailable.
- Preserve notebook URLs, prompt history, and manual research notes so the workflow remains reproducible.

<!-- MCP:END -->

## Related Skills

- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
- [notion-docs](../notion-docs/SKILL.md): Use it when the workflow also needs Notion page and database publishing workflows.
- [pdf](../pdf/SKILL.md): Use it when the workflow also needs PDF extraction, generation, and layout-aware review.
- [word-document](../word-document/SKILL.md): Use it when the workflow also needs Word document authoring and formatting workflows.
