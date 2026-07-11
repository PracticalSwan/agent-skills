---
name: jupyter-notebook
version: "1.3"
last_updated: 2026-07-11
tags: [jupyter, notebook, python, experiments, tutorials]
description: "Use when the user asks to create, scaffold, or edit Jupyter notebooks (`.ipynb`) for experiments, explorations, or tutorials; prefer the bundled templates and helper script for reproducible notebook structure and safer editing."
---
# Jupyter Notebook Skill

Create clean, reproducible Jupyter notebooks for two primary modes:

- Experiments and exploratory analysis
- Tutorials and teaching-oriented walkthroughs

Prefer the bundled templates and the helper script for consistent structure and fewer JSON mistakes.

## When to use
- Create a new `.ipynb` notebook from scratch.
- Convert rough notes or scripts into a structured notebook.
- Refactor an existing notebook to be more reproducible and skimmable.
- Build experiments or tutorials that will be read or re-run by other people.

## Decision tree
- If the request is exploratory, analytical, or hypothesis-driven, choose `experiment`.
- If the request is instructional, step-by-step, or audience-specific, choose `tutorial`.
- If editing an existing notebook, treat it as a refactor: preserve intent and improve structure.

## Skill path (set once)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export JUPYTER_NOTEBOOK_CLI="$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py"
```

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).

## Workflow
1. Lock the intent.
Identify the notebook kind: `experiment` or `tutorial`.
Capture the objective, audience, and what "done" looks like.

2. Scaffold from the template.
Use the helper script to avoid hand-authoring raw notebook JSON.

```bash
uv run --python 3.12 python "$JUPYTER_NOTEBOOK_CLI" \
  --kind experiment \
  --title "Compare prompt variants" \
  --out output/jupyter-notebook/compare-prompt-variants.ipynb
```

```bash
uv run --python 3.12 python "$JUPYTER_NOTEBOOK_CLI" \
  --kind tutorial \
  --title "Intro to embeddings" \
  --out output/jupyter-notebook/intro-to-embeddings.ipynb
```

3. Fill the notebook with small, runnable steps.
Keep each code cell focused on one step.
Add short markdown cells that explain the purpose and expected result.
Avoid large, noisy outputs when a short summary works.

4. Apply the right pattern.
For experiments, follow `references/experiment-patterns.md`.
For tutorials, follow `references/tutorial-patterns.md`.

5. Edit safely when working with existing notebooks.
Preserve the notebook structure; avoid reordering cells unless it improves the top-to-bottom story.
Prefer targeted edits over full rewrites.
If you must edit raw JSON, review `references/notebook-structure.md` first.

6. Validate the result.
Run the notebook top-to-bottom when the environment allows.
If execution is not possible, say so explicitly and call out how to validate locally.
Use the final pass checklist in `references/quality-checklist.md`.

## Templates and helper script
- Templates live in `assets/experiment-template.ipynb` and `assets/tutorial-template.ipynb`.
- The helper script loads a template, updates the title cell, and writes a notebook.

Script path:
- `$JUPYTER_NOTEBOOK_CLI` (installed default: `$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py`)

## Temp and output conventions
- Use `tmp/jupyter-notebook/` for intermediate files; delete when done.
- Write final artifacts under `output/jupyter-notebook/` when working in this repo.
- Use stable, descriptive filenames (for example, `ablation-temperature.ipynb`).

## Dependencies (install only when needed)
Prefer `uv` for dependency management.

Optional Python packages for local notebook execution:

```bash
uv pip install jupyterlab ipykernel
```

The bundled scaffold script uses only the Python standard library and does not require extra dependencies.

## Environment
No required environment variables.

## Reference map
- `references/experiment-patterns.md`: experiment structure and heuristics.
- `references/tutorial-patterns.md`: tutorial structure and teaching flow.
- `references/notebook-structure.md`: notebook JSON shape and safe editing rules.
- `references/quality-checklist.md`: final validation checklist.

## Anti-Patterns

- Hand-authoring raw notebook JSON when the bundled scaffold or a targeted cell edit would avoid avoidable formatting mistakes.
- Packing large exploratory leaps into one noisy cell instead of building small, runnable notebook steps with short narrative bridges.
- Presenting a notebook as validated when it has not been run top-to-bottom or the execution limitation has not been disclosed.

## Verification Protocol

1. Pass/fail: the notebook opens successfully and the structure, title, and requested sections match the chosen experiment or tutorial pattern.
2. Pressure test: execute the notebook top-to-bottom when the environment allows, or validate the JSON plus template structure and call out any runtime gap explicitly.
3. Success metric: no malformed notebook JSON and a clear top-to-bottom flow with runnable or clearly marked cells.

## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or mirror the workflow in repository instructions when folder-based skills are unavailable.
- Claude Code: keep the folder in a local skills directory and preserve any bundled scripts or references the workflow depends on.
- Codex: sync the folder into `$CODEX_HOME/skills/jupyter-notebook` from this maintained catalog instead of editing downstream copies directly.
- Gemini CLI: regenerate the matching `/skills:jupyter-notebook` command with `python scripts/export-gemini-skill.py jupyter-notebook` after meaningful updates.

## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

Preferred MCP Server: None required
Fallback prompt: Use the bundled `new_notebook.py` scaffold, local Jupyter tooling, and notebook execution logs as the fallback evidence path when no notebook-aware MCP surface is available.

## Related Skills

- `codebase-to-course`
- `notebooklm-management`
- `excel-sheet`
- `documentation-authoring`
