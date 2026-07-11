#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


SOURCE_COMMITS = {
    "awesome_copilot": ("https://github.com/github/awesome-copilot", "30472ecf0fe34cc561df958c08501ecc5ca80ea4"),
    "awesome_claude_skills": ("https://github.com/travisvn/awesome-claude-skills", "1da55aa810f206d3fe2005e7e3989b15a275d942"),
    "anthropic_skills": ("https://github.com/anthropics/skills", "9d2f1ae187231d8199c64b5b762e1bdf2244733d"),
    "awesome_codex_skills": ("https://github.com/ComposioHQ/awesome-codex-skills", "9c9da64cf1bbea611d43dd14a10788d55369b353"),
    "googleworkspace_cli": ("https://github.com/googleworkspace/cli", "a3768d0e82ad83cca2da97724e46bea4ff0e6dbd"),
    "avoid_ai_writing": ("https://github.com/conorbronsdon/avoid-ai-writing", "500ff59006f19c27120c5ddbd9b56fc3d937b6bf"),
    "codebase_to_course": ("https://github.com/zarazhangrui/codebase-to-course", "ff8837ecf8e9f6ce9874ffa42e42633394a52a00"),
    "nvidia_skills": ("https://github.com/NVIDIA/skills", "f6075a5060ed3c86536055700d95eb68655162ee"),
    "stitch_skills": ("https://github.com/google-labs-code/stitch-skills", "3f64079d75d025bc5890c73669f27c26a2d80b31"),
    "xquik_x_twitter_scraper": ("https://github.com/Xquik-dev/x-twitter-scraper", "4b444b719b2022867b202788ca3df1305049f2d9"),
    "openai_skills": ("https://github.com/openai/skills", "49f948faa9258a0c61caceaf225e179651397431"),
    "superpowers_skills": ("https://github.com/obra/superpowers-skills", "cdcd624ad3fd8026deb692e565351854569798dd"),
    "superpowers_legacy": ("https://github.com/obra/superpowers", "d884ae04edebef577e82ff7c4e143debd0bbec99"),
}

SUPERPOWERS = {
    "brainstorming",
    "collision-zone-thinking",
    "condition-based-waiting",
    "defense-in-depth",
    "dispatching-parallel-agents",
    "executing-plans",
    "finishing-a-development-branch",
    "gardening-skills-wiki",
    "inversion-exercise",
    "meta-pattern-recognition",
    "preserving-productive-tensions",
    "pulling-updates-from-skills-repository",
    "receiving-code-review",
    "remembering-conversations",
    "requesting-code-review",
    "root-cause-tracing",
    "scale-game",
    "sharing-skills",
    "simplification-cascades",
    "subagent-driven-development",
    "systematic-debugging",
    "test-driven-development",
    "testing-anti-patterns",
    "testing-skills-with-subagents",
    "tracing-knowledge-lineages",
    "using-git-worktrees",
    "using-skills",
    "using-superpowers",
    "verification-before-completion",
    "when-stuck",
    "writing-plans",
    "writing-skills",
}

OPENAI_CURRENT = {
    "figma": "skills/.curated/figma",
    "figma-implement-design": "skills/.curated/figma-implement-design",
    "imagegen": "skills/.system/imagegen",
    "jupyter-notebook": "skills/.curated/jupyter-notebook",
    "playwright": "skills/.curated/playwright",
    "screenshot": "skills/.curated/screenshot",
    "security-best-practices": "skills/.curated/security-best-practices",
    "security-ownership-map": "skills/.curated/security-ownership-map",
    "security-threat-model": "skills/.curated/security-threat-model",
    "vercel-deploy": "skills/.curated/vercel-deploy",
}

LOCAL_IMPORTS = {
    "recommender-evaluation": (
        "local-workspace://C:/Assumption University/CSX4207/Project",
        "sha256:e0b96811878f6a18d5f52745da5612b3a9cbcb9f044043388e22600460bb5bd2",
        ".claude/skills/recommender-evaluation",
        "Preserves the project-specific recommender evaluation protocol while making its activation boundary explicit in the shared catalog.",
    ),
    "step-by-step-web-project-builder": (
        "local-workspace://C:/Assumption University/Finished/CSX4107/Assignments",
        "sha256:cd3e1cf98bfffe548f8804d502a63a8d6fa2d9cc49cbb10f65dca7726131a0a3",
        ".agent/skills/step_by_step_web_project_builder",
        "Promotes a learning-oriented phased web-project workflow from a child skill root with a folder-safe name.",
    ),
    "web-dev-explainer": (
        "local-workspace://C:/Assumption University/Finished/CSX4107/Assignments",
        "sha256:64302e7c5f9bd864c4e88cf4d1a8915ad9c69582ec417e1ff097f07f650c5cd0",
        ".agent/skills/web_dev_explainer",
        "Promotes the workspace's web-development teaching workflow with a folder-safe catalog name.",
    ),
    "ds-notebook-strict-code": (
        "local-workspace://C:/Assumption University/Finished/ITX2007/Assignments",
        "sha256:f00f66afa472152180de748df6c54dde0db43d734004e8f79748e494f576f3e7",
        ".agent/skills/ds-notebook-strict-code",
        "Preserves the explicit code-only notebook output mode as an opt-in, course-oriented workflow.",
    ),
    "ds-teaching-assistant": (
        "local-workspace://C:/Assumption University/Finished/ITX2007/Assignments",
        "sha256:9bd3ee54bcbd541ab8210013b58313f81e02e5135016ff182806deaad8f511a2",
        ".agent/skills/ds-teaching-assistant",
        "Promotes the undergraduate data-science teaching workflow while retaining its course-scope boundary.",
    ),
    "competition-submission-checker": (
        "local-workspace://C:/Assumption University/Outside Courses/GCI World 2026",
        "sha256:a42dbd44ac124d8ff639aa9eee834c589527eb66c2742ed1b4fba7444305b1a3",
        ".agents/skills/competition-submission-checker",
        "Keeps the GCI competition submission schema and leakage checks available as a narrowly activated workflow.",
    ),
    "course-content-map": (
        "local-workspace://C:/Assumption University/Outside Courses/GCI World 2026",
        "sha256:5ef9653ccffaf53b7698df234aa0e60c27f7832e16032a67980e819bb69c0b97",
        ".agents/skills/course-content-map",
        "Promotes the GCI course inventory workflow without broadening it to unrelated workspaces.",
    ),
    "document-metadata-review": (
        "local-workspace://C:/Assumption University/Outside Courses/GCI World 2026",
        "sha256:672f84e342056cf4d7c88b020dcdf96707ff0601ff9a5f15b546b368c166410c",
        ".agents/skills/document-metadata-review",
        "Adds a local-first document metadata and hidden-content review workflow.",
    ),
    "final-assignment-citation-review": (
        "local-workspace://C:/Assumption University/Outside Courses/GCI World 2026",
        "sha256:48da323567833f9009344e11e50f09406ca5066329cca1543e27c6c1a09ff894",
        ".agents/skills/final-assignment-citation-review",
        "Preserves a course-specific citation, disclosure, and reproducibility review workflow.",
    ),
    "homework-notebook-review": (
        "local-workspace://C:/Assumption University/Outside Courses/GCI World 2026",
        "sha256:6f97c5514c2bac5d6d2bcfb0af09f82cbdf43aeeabd90d9fcf505f023613e0ad",
        ".agents/skills/homework-notebook-review",
        "Adds a bounded notebook review workflow for completeness, reproducibility, and academic-integrity risks.",
    ),
    "notebook-execution-safety": (
        "local-workspace://C:/Assumption University/Outside Courses/GCI World 2026",
        "sha256:41e0a5ed117cd716119fafd29457ba39c1c69cb231adf3520535f0e03c0c8b9b",
        ".agents/skills/notebook-execution-safety",
        "Promotes a reusable notebook side-effect and execution-safety preflight.",
    ),
    "tabular-eda-review": (
        "local-workspace://C:/Assumption University/Outside Courses/GCI World 2026",
        "sha256:0bf5541310d362988bb8af9c50c6c553b8c1a57210fd1b7d273fc0b56903bc7d",
        ".agents/skills/tabular-eda-review",
        "Promotes a concise tabular-data quality, leakage, and modeling-readiness review workflow.",
    ),
}


def write_reference_sources(repo_root: Path, data: dict) -> None:
    refs = data["reference_installs"]
    tracked = sorted(
        (name, metadata)
        for name, metadata in refs.items()
        if not name.startswith(("gws-", "recipe-"))
    )
    local_overlays = sorted(
        name for name in refs if name.startswith(("gws-", "recipe-"))
    )
    source_catalogs = sorted(
        {metadata["source_repo"] for metadata in refs.values() if metadata["source_repo"].startswith("https://")}
        | {metadata["repo"] for metadata in data["source_commits"].values()}
    )

    source_rows = "\n".join(
        f"| `{key}` | `{metadata['repo']}` | `{metadata['commit']}` |"
        for key, metadata in data["source_commits"].items()
    )
    tracked_rows = "\n".join(
        f"| `{name}` | `{metadata['source_repo']}` | `{metadata['source_commit']}` | `{metadata['source_path']}` |"
        for name, metadata in tracked
    )
    catalog_lines = "\n".join(f"- `{source}`" for source in source_catalogs)

    content = f"""# Reference Sources

This document summarizes external and child-workspace provenance for skills in this workspace.
The canonical per-skill mapping is `scripts/skill-registry.json` under `reference_installs`.

## Snapshot (2026-07-11)

- `{len(refs)}` skills have source mappings.
- `{len(tracked)}` source-mapped skills are part of the git-tracked catalog.
- `{len(local_overlays)}` source-mapped skills are local-only overlays (`gws-*` and `recipe-*`).
- `0` tracked imports are pending provenance mapping.
- `0` source mappings point to missing local skill folders.
- `0` source mappings are missing required fields (`source_repo`, `source_commit`, `source_path`).
- `32` copied official Superpowers are tracked separately through `copied_official_superpowers`; they are intentionally excluded from `reference_installs`.

## Source Catalogs

{catalog_lines}

Local child-workspace imports use `local-workspace://` provenance plus a SHA-256 tree digest when no git commit owns the source folder.

## Source Commits

| Source | Repository | Commit |
|--------|------------|--------|
{source_rows}

## Tracked Reference Installs

| Skill | Source Repo | Source Commit | Source Path |
|-------|-------------|---------------|-------------|
{tracked_rows}

## Local-Only Overlay Reference Installs

These source-mapped overlays are intentionally local-only in this workspace and are not tracked in git:

- `gws-*`: `26` skills sourced from `https://github.com/googleworkspace/cli`.
- `recipe-*`: `32` skills sourced from `https://github.com/googleworkspace/cli`.

Use `scripts/skill-registry.json` for each overlay's exact source path, commit, and rationale.

## Child-Path Promotion Notes

- The 2026-07-11 maintenance pass compared the parent catalog with the Codex, shared, Claude, Gemini, and discovered workspace-local skill roots.
- Eleven Codex-only skills were promoted; current OpenAI sources were preferred where available, while the retired `doc` and `frontend-skill` copies were matched byte-for-byte to their last canonical historical commits.
- Twelve workspace-local skills were promoted. Invalid underscore or title-style names were normalized to lowercase hyphen-case in the parent catalog while their original source paths remain recorded.
- The official `obra/superpowers-skills` catalog was flattened from categorized child paths into top-level folders. `using-superpowers` remains as a documented compatibility copy from `obra/superpowers`, while `using-skills` is the current canonical entrypoint.
- `docx`, `pptx`, and `xlsx` now map to `anthropics/skills`; `jupyter-notebook` now maps to `openai/skills`. Their support trees matched the current canonical sources, with only the catalog-normalized `SKILL.md` wrappers differing.

## Selection And Refresh Notes

- Import new or refreshed skills into `C:\\Users\\LOQ\\.copilot\\skills` first; downstream roots are deployment targets.
- Prefer canonical upstream sources over discovery catalogs and compare exact recorded paths before changing normalized skill content.
- Upstream HEAD movement alone is not a reason to rewrite a skill. On 2026-07-11, exact-path comparison showed no relevant changes for the tracked Awesome Copilot, Anthropic `mcp-builder`, NVIDIA, Google Workspace CLI, and several other imports.
- Real upstream changes were incorporated for `avoid-ai-writing`, five Stitch workflows and their upload helper, and `x-twitter-scraper` references and core workflow.
- The Stitch refresh preserved the previously verified project/design-system MCP boundary. Broader screen tools remain optional and must be rediscovered in the active host before use.
- Imported skills that handle third-party content retain prompt-injection, credential, approval, and private-data boundaries during normalization.
- Copied official Superpowers remain separately classified so maintained counts, sync routing, and provenance reporting stay honest.
"""
    (repo_root / "REFERENCE_SOURCES.md").write_text(content, encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    path = repo_root / "scripts" / "skill-registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    data["source_commits"] = {
        key: {"repo": repo, "commit": commit}
        for key, (repo, commit) in SOURCE_COMMITS.items()
    }
    data["copied_official_superpowers"] = sorted(SUPERPOWERS)

    current_by_repo = {repo: commit for repo, commit in SOURCE_COMMITS.values()}
    refs = data.setdefault("reference_installs", {})
    for metadata in refs.values():
        source_repo = metadata.get("source_repo")
        if source_repo in current_by_repo:
            metadata["source_commit"] = current_by_repo[source_repo]

    refs.update(
        {
            "doc": {
                "source_repo": "https://github.com/openai/skills",
                "source_commit": "45d05d75363abf13f99d09e899d61e07b8010685",
                "source_path": "skills/.curated/doc",
                "reason": "Preserves the exact historical OpenAI DOCX skill found in the Codex child root after the curated source was retired.",
            },
            "frontend-skill": {
                "source_repo": "https://github.com/openai/skills",
                "source_commit": "30444aed500c00c85294d12074f6e3ee794f808a",
                "source_path": "skills/.curated/frontend-skill",
                "reason": "Preserves the exact historical OpenAI frontend art-direction skill found in the Codex child root after the curated source was retired.",
            },
            "docx": {
                "source_repo": "https://github.com/anthropics/skills",
                "source_commit": SOURCE_COMMITS["anthropic_skills"][1],
                "source_path": "skills/docx",
                "reason": "Matches the current Anthropic DOCX asset and helper tree while retaining the catalog-normalized SKILL.md wrapper.",
            },
            "pptx": {
                "source_repo": "https://github.com/anthropics/skills",
                "source_commit": SOURCE_COMMITS["anthropic_skills"][1],
                "source_path": "skills/pptx",
                "reason": "Matches the current Anthropic PPTX asset and helper tree while retaining the catalog-normalized SKILL.md wrapper.",
            },
            "xlsx": {
                "source_repo": "https://github.com/anthropics/skills",
                "source_commit": SOURCE_COMMITS["anthropic_skills"][1],
                "source_path": "skills/xlsx",
                "reason": "Matches the current Anthropic XLSX asset and helper tree while retaining the catalog-normalized SKILL.md wrapper.",
            },
        }
    )
    for name, source_path in OPENAI_CURRENT.items():
        refs[name] = {
            "source_repo": "https://github.com/openai/skills",
            "source_commit": SOURCE_COMMITS["openai_skills"][1],
            "source_path": source_path,
            "reason": "Promoted from the Codex child root and refreshed from the current canonical OpenAI skills source.",
        }
    for name, (source_repo, source_commit, source_path, reason) in LOCAL_IMPORTS.items():
        refs[name] = {
            "source_repo": source_repo,
            "source_commit": source_commit,
            "source_path": source_path,
            "reason": reason,
        }

    figma_fallback = [
        "Use user-provided Figma exports, screenshots, variables, and local design-system files when Figma MCP is unavailable.",
        "Do not claim node metadata, screenshots, or assets were fetched unless the active host exposed and completed those calls.",
    ]
    for name in ("figma", "figma-implement-design"):
        data.setdefault("mcp_skills", {})[name] = {
            "mode": "Primary",
            "servers": ["Figma MCP"],
            "fallback": figma_fallback,
        }

    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    write_reference_sources(repo_root, data)
    print(
        json.dumps(
            {
                "source_commits": len(data["source_commits"]),
                "copied_official_superpowers": len(data["copied_official_superpowers"]),
                "reference_installs": len(data["reference_installs"]),
                "mcp_skills": len(data["mcp_skills"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
