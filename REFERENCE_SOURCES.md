# Reference Sources

This document summarizes external and child-workspace provenance for skills in this workspace.
The canonical per-skill mapping is `scripts/skill-registry.json` under `reference_installs`.

## Snapshot (2026-07-11)

- `123` skills have source mappings.
- `65` source-mapped skills are part of the git-tracked catalog.
- `58` source-mapped skills are local-only overlays (`gws-*` and `recipe-*`).
- `0` tracked imports are pending provenance mapping.
- `0` source mappings point to missing local skill folders.
- `0` source mappings are missing required fields (`source_repo`, `source_commit`, `source_path`).
- `32` copied official Superpowers are tracked separately through `copied_official_superpowers`; they are intentionally excluded from `reference_installs`.

## Source Catalogs

- `https://github.com/ComposioHQ/awesome-codex-skills`
- `https://github.com/NVIDIA/skills`
- `https://github.com/Xquik-dev/x-twitter-scraper`
- `https://github.com/anthropics/skills`
- `https://github.com/conorbronsdon/avoid-ai-writing`
- `https://github.com/github/awesome-copilot`
- `https://github.com/google-labs-code/stitch-skills`
- `https://github.com/googleworkspace/cli`
- `https://github.com/obra/superpowers`
- `https://github.com/obra/superpowers-skills`
- `https://github.com/openai/skills`
- `https://github.com/travisvn/awesome-claude-skills`
- `https://github.com/zarazhangrui/codebase-to-course`

Local child-workspace imports use `local-workspace://` provenance plus a SHA-256 tree digest when no git commit owns the source folder.

## Source Commits

| Source | Repository | Commit |
|--------|------------|--------|
| `awesome_copilot` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` |
| `awesome_claude_skills` | `https://github.com/travisvn/awesome-claude-skills` | `1da55aa810f206d3fe2005e7e3989b15a275d942` |
| `anthropic_skills` | `https://github.com/anthropics/skills` | `9d2f1ae187231d8199c64b5b762e1bdf2244733d` |
| `awesome_codex_skills` | `https://github.com/ComposioHQ/awesome-codex-skills` | `9c9da64cf1bbea611d43dd14a10788d55369b353` |
| `googleworkspace_cli` | `https://github.com/googleworkspace/cli` | `a3768d0e82ad83cca2da97724e46bea4ff0e6dbd` |
| `avoid_ai_writing` | `https://github.com/conorbronsdon/avoid-ai-writing` | `500ff59006f19c27120c5ddbd9b56fc3d937b6bf` |
| `codebase_to_course` | `https://github.com/zarazhangrui/codebase-to-course` | `ff8837ecf8e9f6ce9874ffa42e42633394a52a00` |
| `nvidia_skills` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` |
| `stitch_skills` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` |
| `xquik_x_twitter_scraper` | `https://github.com/Xquik-dev/x-twitter-scraper` | `4b444b719b2022867b202788ca3df1305049f2d9` |
| `openai_skills` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` |
| `superpowers_skills` | `https://github.com/obra/superpowers-skills` | `cdcd624ad3fd8026deb692e565351854569798dd` |
| `superpowers_legacy` | `https://github.com/obra/superpowers` | `d884ae04edebef577e82ff7c4e143debd0bbec99` |

## Tracked Reference Installs

| Skill | Source Repo | Source Commit | Source Path |
|-------|-------------|---------------|-------------|
| `accelerated-computing-cudf` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` | `skills/accelerated-computing-cudf` |
| `agentic-eval` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/agentic-eval` |
| `avoid-ai-writing` | `https://github.com/conorbronsdon/avoid-ai-writing` | `500ff59006f19c27120c5ddbd9b56fc3d937b6bf` | `.` |
| `cloud-design-patterns` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/cloud-design-patterns` |
| `codebase-to-course` | `https://github.com/zarazhangrui/codebase-to-course` | `ff8837ecf8e9f6ce9874ffa42e42633394a52a00` | `.` |
| `competition-submission-checker` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:a42dbd44ac124d8ff639aa9eee834c589527eb66c2742ed1b4fba7444305b1a3` | `.agents/skills/competition-submission-checker` |
| `context-map` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/context-map` |
| `course-content-map` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:5ef9653ccffaf53b7698df234aa0e60c27f7832e16032a67980e819bb69c0b97` | `.agents/skills/course-content-map` |
| `csharp-xunit` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/csharp-xunit` |
| `deepstream-dev` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` | `skills/deepstream-dev` |
| `deepstream-import-vision-model` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` | `skills/deepstream-import-vision-model` |
| `doc` | `https://github.com/openai/skills` | `45d05d75363abf13f99d09e899d61e07b8010685` | `skills/.curated/doc` |
| `document-metadata-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:672f84e342056cf4d7c88b020dcdf96707ff0601ff9a5f15b546b368c166410c` | `.agents/skills/document-metadata-review` |
| `docx` | `https://github.com/anthropics/skills` | `9d2f1ae187231d8199c64b5b762e1bdf2244733d` | `skills/docx` |
| `dotnet-best-practices` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/dotnet-best-practices` |
| `ds-notebook-strict-code` | `local-workspace://C:/Assumption University/Finished/ITX2007/Assignments` | `sha256:f00f66afa472152180de748df6c54dde0db43d734004e8f79748e494f576f3e7` | `.agent/skills/ds-notebook-strict-code` |
| `ds-teaching-assistant` | `local-workspace://C:/Assumption University/Finished/ITX2007/Assignments` | `sha256:9bd3ee54bcbd541ab8210013b58313f81e02e5135016ff182806deaad8f511a2` | `.agent/skills/ds-teaching-assistant` |
| `figma` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/figma` |
| `figma-implement-design` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/figma-implement-design` |
| `final-assignment-citation-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:48da323567833f9009344e11e50f09406ca5066329cca1543e27c6c1a09ff894` | `.agents/skills/final-assignment-citation-review` |
| `frontend-skill` | `https://github.com/openai/skills` | `30444aed500c00c85294d12074f6e3ee794f808a` | `skills/.curated/frontend-skill` |
| `homework-notebook-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:6f97c5514c2bac5d6d2bcfb0af09f82cbdf43aeeabd90d9fcf505f023613e0ad` | `.agents/skills/homework-notebook-review` |
| `imagegen` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.system/imagegen` |
| `java-docs` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/java-docs` |
| `java-junit` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/java-junit` |
| `jupyter-notebook` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/jupyter-notebook` |
| `mcp-builder` | `https://github.com/anthropics/skills` | `9d2f1ae187231d8199c64b5b762e1bdf2244733d` | `skills/mcp-builder` |
| `nemo-retriever` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` | `skills/nemo-retriever` |
| `notebook-execution-safety` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:41e0a5ed117cd716119fafd29457ba39c1c69cb231adf3520535f0e03c0c8b9b` | `.agents/skills/notebook-execution-safety` |
| `pdf` | `https://github.com/travisvn/awesome-claude-skills` | `1da55aa810f206d3fe2005e7e3989b15a275d942` | `Official skill reference -> anthropics/skills/pdf` |
| `playwright` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/playwright` |
| `pptx` | `https://github.com/anthropics/skills` | `9d2f1ae187231d8199c64b5b762e1bdf2244733d` | `skills/pptx` |
| `premium-frontend-ui` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/premium-frontend-ui` |
| `rag-blueprint` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` | `skills/rag-blueprint` |
| `rag-eval` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` | `skills/rag-eval` |
| `rag-perf` | `https://github.com/NVIDIA/skills` | `f6075a5060ed3c86536055700d95eb68655162ee` | `skills/rag-perf` |
| `recommender-evaluation` | `local-workspace://C:/Assumption University/CSX4207/Project` | `sha256:e0b96811878f6a18d5f52745da5612b3a9cbcb9f044043388e22600460bb5bd2` | `.claude/skills/recommender-evaluation` |
| `screenshot` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/screenshot` |
| `secret-scanning` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/secret-scanning` |
| `security-best-practices` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/security-best-practices` |
| `security-ownership-map` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/security-ownership-map` |
| `security-review` | `https://github.com/github/awesome-copilot` | `30472ecf0fe34cc561df958c08501ecc5ca80ea4` | `skills/security-review` |
| `security-threat-model` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/security-threat-model` |
| `spreadsheet-formula-helper` | `https://github.com/ComposioHQ/awesome-codex-skills` | `9c9da64cf1bbea611d43dd14a10788d55369b353` | `spreadsheet-formula-helper` |
| `step-by-step-web-project-builder` | `local-workspace://C:/Assumption University/Finished/CSX4107/Assignments` | `sha256:cd3e1cf98bfffe548f8804d502a63a8d6fa2d9cc49cbb10f65dca7726131a0a3` | `.agent/skills/step_by_step_web_project_builder` |
| `stitch-code-to-design` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-design/skills/code-to-design` |
| `stitch-design` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `local router for plugins/stitch-design, plugins/stitch-build, and plugins/stitch-utilities` |
| `stitch-design-md` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-utilities/skills/design-md` |
| `stitch-enhance-prompt` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-utilities/skills/enhance-prompt` |
| `stitch-extract-design-md` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-design/skills/extract-design-md` |
| `stitch-extract-static-html` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-design/skills/extract-static-html` |
| `stitch-generate-design` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-design/skills/generate-design` |
| `stitch-loop` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-utilities/skills/stitch-loop` |
| `stitch-manage-design-system` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-design/skills/manage-design-system` |
| `stitch-react-components` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-build/skills/react-components` |
| `stitch-react-native` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-build/skills/react-native` |
| `stitch-remotion` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-build/skills/remotion` |
| `stitch-shadcn-ui` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-build/skills/shadcn-ui` |
| `stitch-taste-design` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-utilities/skills/taste-design` |
| `stitch-upload-to-stitch` | `https://github.com/google-labs-code/stitch-skills` | `3f64079d75d025bc5890c73669f27c26a2d80b31` | `plugins/stitch-design/skills/upload-to-stitch` |
| `tabular-eda-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:0bf5541310d362988bb8af9c50c6c553b8c1a57210fd1b7d273fc0b56903bc7d` | `.agents/skills/tabular-eda-review` |
| `vercel-deploy` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/vercel-deploy` |
| `web-dev-explainer` | `local-workspace://C:/Assumption University/Finished/CSX4107/Assignments` | `sha256:64302e7c5f9bd864c4e88cf4d1a8915ad9c69582ec417e1ff097f07f650c5cd0` | `.agent/skills/web_dev_explainer` |
| `x-twitter-scraper` | `https://github.com/Xquik-dev/x-twitter-scraper` | `4b444b719b2022867b202788ca3df1305049f2d9` | `skills/x-twitter-scraper` |
| `xlsx` | `https://github.com/anthropics/skills` | `9d2f1ae187231d8199c64b5b762e1bdf2244733d` | `skills/xlsx` |

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

- Import new or refreshed skills into `C:\Users\LOQ\.copilot\skills` first; downstream roots are deployment targets.
- Prefer canonical upstream sources over discovery catalogs and compare exact recorded paths before changing normalized skill content.
- Upstream HEAD movement alone is not a reason to rewrite a skill. On 2026-07-11, exact-path comparison showed no relevant changes for the tracked Awesome Copilot, Anthropic `mcp-builder`, NVIDIA, Google Workspace CLI, and several other imports.
- Real upstream changes were incorporated for `avoid-ai-writing`, five Stitch workflows and their upload helper, and `x-twitter-scraper` references and core workflow.
- The Stitch refresh preserved the previously verified project/design-system MCP boundary. Broader screen tools remain optional and must be rediscovered in the active host before use.
- Imported skills that handle third-party content retain prompt-injection, credential, approval, and private-data boundaries during normalization.
- Copied official Superpowers remain separately classified so maintained counts, sync routing, and provenance reporting stay honest.
