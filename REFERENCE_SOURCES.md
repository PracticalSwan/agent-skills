# Reference Sources

This document summarizes external and child-workspace provenance for skills in this workspace.
The canonical per-skill mapping is `scripts/skill-registry.json` under `reference_installs`.

## Snapshot (2026-08-31)

- `226` skills have source mappings.
- `168` source-mapped skills are part of the git-tracked catalog.
- `58` source-mapped skills are local-only overlays (`gws-*` and `recipe-*`).
- `0` tracked imports are pending provenance mapping.
- `0` source mappings point to missing local skill folders.
- `0` source mappings are missing required fields (`source_repo`, `source_commit`, `source_path`).
- `32` copied official Superpowers are tracked separately through `copied_official_superpowers`; they are intentionally excluded from `reference_installs`.
- `94` upstream Blender skills plus `1` separately protected local entry (`95` protected names total) are a Codex-only external overlay sourced from `arjun988/blender-skills`; they are not parent-catalog imports and must not sync to shared or Claude roots.

## Source Catalogs

- `https://github.com/ComposioHQ/awesome-codex-skills`
- `https://github.com/NVIDIA/skills`
- `https://github.com/Xquik-dev/x-twitter-scraper`
- `https://github.com/addyosmani/web-quality-skills`
- `https://github.com/anthropics/skills`
- `https://github.com/arjun988/blender-skills`
- `https://github.com/conorbronsdon/avoid-ai-writing`
- `https://github.com/figma/mcp-server-guide`
- `https://github.com/github/awesome-copilot`
- `https://github.com/google-gemini/gemini-skills`
- `https://github.com/google-labs-code/stitch-skills`
- `https://github.com/googleworkspace/cli`
- `https://github.com/huggingface/skills`
- `https://github.com/mattpocock/skills`
- `https://github.com/mongodb/agent-skills`
- `https://github.com/netlify/context-and-tools`
- `https://github.com/obra/superpowers`
- `https://github.com/obra/superpowers-skills`
- `https://github.com/openai/skills`
- `https://github.com/supabase/agent-skills`
- `https://github.com/tavily-ai/skills`
- `https://github.com/travisvn/awesome-claude-skills`
- `https://github.com/vercel-labs/agent-skills`
- `https://github.com/zarazhangrui/codebase-to-course`

Local child-workspace imports use `local-workspace://` provenance plus a SHA-256 tree digest when no git commit owns the source folder.

## Source Commits

| Source | Repository | Commit |
|--------|------------|--------|
| `awesome_copilot` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` |
| `awesome_claude_skills` | `https://github.com/travisvn/awesome-claude-skills` | `1da55aa810f206d3fe2005e7e3989b15a275d942` |
| `anthropic_skills` | `https://github.com/anthropics/skills` | `3b3fad96af16a10759d930941b4520ba0c40edae` |
| `awesome_codex_skills` | `https://github.com/ComposioHQ/awesome-codex-skills` | `0930e1373789d2eda449039f7ac154b33031de89` |
| `googleworkspace_cli` | `https://github.com/googleworkspace/cli` | `a3768d0e82ad83cca2da97724e46bea4ff0e6dbd` |
| `avoid_ai_writing` | `https://github.com/conorbronsdon/avoid-ai-writing` | `58a95fc9971d7af95f1f1324b8a6bc991eb8004d` |
| `codebase_to_course` | `https://github.com/zarazhangrui/codebase-to-course` | `ff8837ecf8e9f6ce9874ffa42e42633394a52a00` |
| `nvidia_skills` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` |
| `stitch_skills` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` |
| `xquik_x_twitter_scraper` | `https://github.com/Xquik-dev/x-twitter-scraper` | `dc5fa6037d700eb3a7721155e92dabeeb9e56894` |
| `openai_skills` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` |
| `superpowers_skills` | `https://github.com/obra/superpowers-skills` | `cdcd624ad3fd8026deb692e565351854569798dd` |
| `superpowers_legacy` | `https://github.com/obra/superpowers` | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` |
| `tavily_skills` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` |
| `matt_pocock_skills` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` |
| `supabase_agent_skills` | `https://github.com/supabase/agent-skills` | `8331f910845103c08d51f6ca1d86ebb7d1f745e3` |
| `gemini_skills` | `https://github.com/google-gemini/gemini-skills` | `d89e731a59ea7e9bf623e6358effe76458dd7f29` |
| `vercel_agent_skills` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` |
| `web_quality_skills` | `https://github.com/addyosmani/web-quality-skills` | `afa8da942115f2961fdbfa80807ea0b232ff6c00` |
| `netlify_context_and_tools` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` |
| `mongodb_agent_skills` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` |
| `figma_mcp_server_guide` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` |
| `huggingface_skills` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` |
| `blender_skills` | `https://github.com/arjun988/blender-skills` | `8f778d2405a214b508d4c7d80742be8e43acdd52` |

## Tracked Reference Installs

| Skill | Source Repo | Source Commit | Source Path |
|-------|-------------|---------------|-------------|
| `accelerated-computing-cudf` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` | `skills/accelerated-computing-cudf` |
| `accessibility` | `https://github.com/addyosmani/web-quality-skills` | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | `skills/accessibility` |
| `agentic-eval` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/agentic-eval` |
| `avoid-ai-writing` | `https://github.com/conorbronsdon/avoid-ai-writing` | `58a95fc9971d7af95f1f1324b8a6bc991eb8004d` | `.` |
| `best-practices` | `https://github.com/addyosmani/web-quality-skills` | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | `skills/best-practices` |
| `cloud-design-patterns` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/cloud-design-patterns` |
| `codebase-design` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/engineering/codebase-design` |
| `codebase-to-course` | `https://github.com/zarazhangrui/codebase-to-course` | `ff8837ecf8e9f6ce9874ffa42e42633394a52a00` | `.` |
| `codex-app-threads` | `local-workspace://C:/Users/LOQ/.codex/skills` | `sha256:76448b85d49f671eae1143aed4e977f57a9f8e26d906b9c0bb9c9aa68ba44488` | `codex-app-threads` |
| `codex-computer-use` | `local-workspace://C:/Users/LOQ/.codex/skills` | `sha256:84334e3fa919ee99ebecf1b23bb3f6fb98c82c95a19a79d769f5d6894fa704ac` | `codex-computer-use` |
| `codex-in-app-browser` | `local-workspace://C:/Users/LOQ/.codex/skills` | `sha256:3d0d53c7bc8c4ec5edf63e91e3427a95d29f4020096f705e46f6c619bb4870c5` | `codex-in-app-browser` |
| `codex-router` | `local-workspace://C:/Users/LOQ/.codex/skills` | `sha256:ab31386aa02537d45d7cd37b693eb7ff318a16eef2cc3a0361619a1bc2509af9` | `codex-router` |
| `codex-router-media` | `local-workspace://C:/Users/LOQ/.codex/skills` | `sha256:e3bbe2397d7c5b240ab98c3e6fab6d4afa40ab77468062d1e5076b03bcc87e06` | `codex-router-media` |
| `competition-submission-checker` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:a42dbd44ac124d8ff639aa9eee834c589527eb66c2742ed1b4fba7444305b1a3` | `.agents/skills/competition-submission-checker` |
| `composition-patterns` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/composition-patterns` |
| `context-map` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/context-map` |
| `core-web-vitals` | `https://github.com/addyosmani/web-quality-skills` | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | `skills/core-web-vitals` |
| `course-content-map` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:5ef9653ccffaf53b7698df234aa0e60c27f7832e16032a67980e819bb69c0b97` | `.agents/skills/course-content-map` |
| `csharp-xunit` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/csharp-xunit` |
| `deepstream-dev` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` | `skills/deepstream-dev` |
| `deepstream-import-vision-model` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` | `skills/deepstream-import-vision-model` |
| `deploy-to-vercel` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/deploy-to-vercel` |
| `doc` | `https://github.com/openai/skills` | `45d05d75363abf13f99d09e899d61e07b8010685` | `skills/.curated/doc` |
| `document-metadata-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:672f84e342056cf4d7c88b020dcdf96707ff0601ff9a5f15b546b368c166410c` | `.agents/skills/document-metadata-review` |
| `docx` | `https://github.com/anthropics/skills` | `3b3fad96af16a10759d930941b4520ba0c40edae` | `skills/docx` |
| `domain-modeling` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/engineering/domain-modeling` |
| `dotnet-best-practices` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/dotnet-best-practices` |
| `ds-notebook-strict-code` | `local-workspace://C:/Assumption University/Finished/ITX2007/Assignments` | `sha256:f00f66afa472152180de748df6c54dde0db43d734004e8f79748e494f576f3e7` | `.agent/skills/ds-notebook-strict-code` |
| `ds-teaching-assistant` | `local-workspace://C:/Assumption University/Finished/ITX2007/Assignments` | `sha256:9bd3ee54bcbd541ab8210013b58313f81e02e5135016ff182806deaad8f511a2` | `.agent/skills/ds-teaching-assistant` |
| `figma` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/figma` |
| `figma-code-connect` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-code-connect` |
| `figma-create-new-file` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-create-new-file` |
| `figma-design-to-code` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-design-to-code` |
| `figma-generate-design` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-generate-design` |
| `figma-generate-diagram` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-generate-diagram` |
| `figma-generate-library` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-generate-library` |
| `figma-implement-design` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/figma-implement-design` |
| `figma-implement-motion` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-implement-motion` |
| `figma-swiftui` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-swiftui` |
| `figma-use` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-use` |
| `figma-use-figjam` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-use-figjam` |
| `figma-use-motion` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-use-motion` |
| `figma-use-slides` | `https://github.com/figma/mcp-server-guide` | `7f6562c4900fafb46e5e8fd3cc8ced954779bab3` | `skills/figma-use-slides` |
| `final-assignment-citation-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:48da323567833f9009344e11e50f09406ca5066329cca1543e27c6c1a09ff894` | `.agents/skills/final-assignment-citation-review` |
| `frontend-design` | `https://github.com/openai/skills` | `30444aed500c00c85294d12074f6e3ee794f808a` | `skills/.curated/frontend-skill` |
| `gemini-api-dev` | `https://github.com/google-gemini/gemini-skills` | `d89e731a59ea7e9bf623e6358effe76458dd7f29` | `skills/gemini-api-dev` |
| `gemini-interactions-api` | `https://github.com/google-gemini/gemini-skills` | `d89e731a59ea7e9bf623e6358effe76458dd7f29` | `skills/gemini-interactions-api` |
| `handoff` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/productivity/handoff` |
| `hf-cloud-aws-context-discovery` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/hf-cloud-aws-context-discovery` |
| `hf-cloud-python-env-setup` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/hf-cloud-python-env-setup` |
| `hf-cloud-sagemaker-deployment-planner` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/hf-cloud-sagemaker-deployment-planner` |
| `hf-cloud-sagemaker-iam-preflight` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/hf-cloud-sagemaker-iam-preflight` |
| `hf-cloud-sagemaker-production-defaults` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/hf-cloud-sagemaker-production-defaults` |
| `hf-cloud-serving-image-selection` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/hf-cloud-serving-image-selection` |
| `hf-mcp` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `hf-mcp/skills/hf-mcp` |
| `homework-notebook-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:6f97c5514c2bac5d6d2bcfb0af09f82cbdf43aeeabd90d9fcf505f023613e0ad` | `.agents/skills/homework-notebook-review` |
| `huggingface-best` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-best` |
| `huggingface-community-evals` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-community-evals` |
| `huggingface-datasets` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-datasets` |
| `huggingface-gradio` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-gradio` |
| `huggingface-llm-trainer` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-llm-trainer` |
| `huggingface-local-models` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-local-models` |
| `huggingface-lora-space-builder` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-lora-space-builder` |
| `huggingface-paper-publisher` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-paper-publisher` |
| `huggingface-papers` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-papers` |
| `huggingface-spaces` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-spaces` |
| `huggingface-tool-builder` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-tool-builder` |
| `huggingface-trackio` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-trackio` |
| `huggingface-vision-trainer` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-vision-trainer` |
| `huggingface-zerogpu` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/huggingface-zerogpu` |
| `imagegen` | `local-workspace://C:/Users/LOQ/.codex/skills/.system` | `sha256:bf6877b61db77477b039f93a024b7369cce115ff31c2a05f928a81a0a89fc8b8` | `imagegen` |
| `improve-codebase-architecture` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/engineering/improve-codebase-architecture` |
| `java-docs` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/java-docs` |
| `java-junit` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/java-junit` |
| `jupyter-notebook` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/jupyter-notebook` |
| `mcp-builder` | `https://github.com/anthropics/skills` | `3b3fad96af16a10759d930941b4520ba0c40edae` | `skills/mcp-builder` |
| `mongodb-atlas-stream-processing` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` | `skills/mongodb-atlas-stream-processing` |
| `mongodb-connection` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` | `skills/mongodb-connection` |
| `mongodb-mcp-setup` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` | `skills/mongodb-mcp-setup` |
| `mongodb-natural-language-querying` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` | `skills/mongodb-natural-language-querying` |
| `mongodb-query-optimizer` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` | `skills/mongodb-query-optimizer` |
| `mongodb-schema-design` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` | `skills/mongodb-schema-design` |
| `mongodb-search-and-ai` | `https://github.com/mongodb/agent-skills` | `47cc46148f53145eb9b880d2bf1aa89bc9097818` | `skills/mongodb-search-and-ai` |
| `nemo-retriever` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` | `skills/nemo-retriever` |
| `netlify-access-control` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-access-control` |
| `netlify-agent-runner` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-agent-runner` |
| `netlify-ai-gateway` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-ai-gateway` |
| `netlify-blobs` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-blobs` |
| `netlify-caching` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-caching` |
| `netlify-config` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-config` |
| `netlify-database` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-database` |
| `netlify-deploy` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-deploy` |
| `netlify-edge-functions` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-edge-functions` |
| `netlify-forms` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-forms` |
| `netlify-frameworks` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-frameworks` |
| `netlify-functions` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-functions` |
| `netlify-identity` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-identity` |
| `netlify-image-cdn` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-image-cdn` |
| `netlify-mcp-servers` | `https://github.com/netlify/context-and-tools` | `4645e4c47ae4a42a3955c96c1389bbc16f10d457` | `skills/netlify-mcp-servers` |
| `notebook-execution-safety` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:41e0a5ed117cd716119fafd29457ba39c1c69cb231adf3520535f0e03c0c8b9b` | `.agents/skills/notebook-execution-safety` |
| `openai-docs` | `local-workspace://C:/Users/LOQ/.codex/skills/.system` | `sha256:43ba6399569a39bb3a4c42ac1150bae34a3e60098943290c558ac18045aeab1c` | `openai-docs` |
| `pdf` | `https://github.com/travisvn/awesome-claude-skills` | `1da55aa810f206d3fe2005e7e3989b15a275d942` | `Official skill reference -> anthropics/skills/pdf` |
| `performance` | `https://github.com/addyosmani/web-quality-skills` | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | `skills/performance` |
| `playwright` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/playwright` |
| `plugin-creator` | `local-workspace://C:/Users/LOQ/.codex/skills/.system` | `sha256:98b50f9092b509e29bbeda92c8427443e89817edd2512c85404ee435e415e9d8` | `plugin-creator` |
| `pptx` | `https://github.com/anthropics/skills` | `3b3fad96af16a10759d930941b4520ba0c40edae` | `skills/pptx` |
| `prototype` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/engineering/prototype` |
| `rag-blueprint` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` | `skills/rag-blueprint` |
| `rag-eval` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` | `skills/rag-eval` |
| `rag-perf` | `https://github.com/NVIDIA/skills` | `0bdc8f7f08afe9ac0f288c8d2c2de6e77df110a2` | `skills/rag-perf` |
| `react-best-practices` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/react-best-practices` |
| `react-native-skills` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/react-native-skills` |
| `react-view-transitions` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/react-view-transitions` |
| `recommender-evaluation` | `local-workspace://C:/Assumption University/CSX4207/Project` | `sha256:e0b96811878f6a18d5f52745da5612b3a9cbcb9f044043388e22600460bb5bd2` | `.claude/skills/recommender-evaluation` |
| `research` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/engineering/research` |
| `resolving-merge-conflicts` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/engineering/resolving-merge-conflicts` |
| `review-agent` | `local-workspace://C:/Users/LOQ/.codex/skills/.system` | `sha256:8e74c25fd7d12521b1196c0bbc4790dcbd90520630a19da512f9c806c817cdd8` | `review-agent` |
| `screenshot` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/screenshot` |
| `secret-scanning` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/secret-scanning` |
| `security-best-practices` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/security-best-practices` |
| `security-ownership-map` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/security-ownership-map` |
| `security-review` | `https://github.com/github/awesome-copilot` | `c956566a35c3c2e635f019e7a1bfa59d9497e8b1` | `skills/security-review` |
| `security-threat-model` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/security-threat-model` |
| `seo` | `https://github.com/addyosmani/web-quality-skills` | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | `skills/seo` |
| `skill-creator` | `local-workspace://C:/Users/LOQ/.codex/skills/.system` | `sha256:58c915c0b2a301c347808a193a11a6efc14c0e3dad77265432e1e6e2ac54cb41` | `skill-creator` |
| `skill-installer` | `local-workspace://C:/Users/LOQ/.codex/skills/.system` | `sha256:e1c6b6ce82a779080284a89f0578482913cf8eb865be0620c95a0ce795fc1f8c` | `skill-installer` |
| `spreadsheet-formula-helper` | `https://github.com/ComposioHQ/awesome-codex-skills` | `0930e1373789d2eda449039f7ac154b33031de89` | `spreadsheet-formula-helper` |
| `step-by-step-web-project-builder` | `local-workspace://C:/Assumption University/Finished/CSX4107/Assignments` | `sha256:cd3e1cf98bfffe548f8804d502a63a8d6fa2d9cc49cbb10f65dca7726131a0a3` | `.agent/skills/step_by_step_web_project_builder` |
| `stitch-code-to-design` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-design/skills/code-to-design` |
| `stitch-design` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `local router for plugins/stitch-design, plugins/stitch-build, and plugins/stitch-utilities` |
| `stitch-design-md` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-utilities/skills/design-md` |
| `stitch-enhance-prompt` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-utilities/skills/enhance-prompt` |
| `stitch-extract-design-md` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-design/skills/extract-design-md` |
| `stitch-extract-static-html` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-design/skills/extract-static-html` |
| `stitch-generate-design` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-design/skills/generate-design` |
| `stitch-loop` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-utilities/skills/stitch-loop` |
| `stitch-manage-design-system` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-design/skills/manage-design-system` |
| `stitch-react-components` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-build/skills/react-components` |
| `stitch-react-native` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-build/skills/react-native` |
| `stitch-react-vite-dashboard` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-build/skills/react-vite-dashboard` |
| `stitch-remotion` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-build/skills/remotion` |
| `stitch-shadcn-ui` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-build/skills/shadcn-ui` |
| `stitch-taste-design` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-utilities/skills/taste-design` |
| `stitch-upload-to-stitch` | `https://github.com/google-labs-code/stitch-skills` | `0337446dadde6f8c94210444e2aa9d546126480f` | `plugins/stitch-design/skills/upload-to-stitch` |
| `supabase` | `https://github.com/supabase/agent-skills` | `8331f910845103c08d51f6ca1d86ebb7d1f745e3` | `skills/supabase` |
| `supabase-postgres-best-practices` | `https://github.com/supabase/agent-skills` | `8331f910845103c08d51f6ca1d86ebb7d1f745e3` | `skills/supabase-postgres-best-practices` |
| `tabular-eda-review` | `local-workspace://C:/Assumption University/Outside Courses/GCI World 2026` | `sha256:0bf5541310d362988bb8af9c50c6c553b8c1a57210fd1b7d273fc0b56903bc7d` | `.agents/skills/tabular-eda-review` |
| `tavily-best-practices` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-best-practices` |
| `tavily-cli` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-cli` |
| `tavily-crawl` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-crawl` |
| `tavily-dynamic-search` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-dynamic-search` |
| `tavily-extract` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-extract` |
| `tavily-map` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-map` |
| `tavily-research` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-research` |
| `tavily-search` | `https://github.com/tavily-ai/skills` | `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2` | `skills/tavily-search` |
| `train-sentence-transformers` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/train-sentence-transformers` |
| `transformers-js` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/transformers-js` |
| `trl-training` | `https://github.com/huggingface/skills` | `cead19e10754e773bad24fecef83cb64be24094e` | `skills/trl-training` |
| `vercel-cli-with-tokens` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/vercel-cli-with-tokens` |
| `vercel-deploy` | `https://github.com/openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` | `skills/.curated/vercel-deploy` |
| `vercel-optimize` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/vercel-optimize` |
| `web-design-guidelines` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/web-design-guidelines` |
| `web-dev-explainer` | `local-workspace://C:/Assumption University/Finished/CSX4107/Assignments` | `sha256:64302e7c5f9bd864c4e88cf4d1a8915ad9c69582ec417e1ff097f07f650c5cd0` | `.agent/skills/web_dev_explainer` |
| `web-quality-audit` | `https://github.com/addyosmani/web-quality-skills` | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | `skills/web-quality-audit` |
| `writing-for-agents` | `https://github.com/mattpocock/skills` | `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` | `skills/productivity/writing-for-agents` |
| `writing-guidelines` | `https://github.com/vercel-labs/agent-skills` | `063bee94c3f4df8453406c830b0a7df0f2860278` | `skills/writing-guidelines` |
| `x-twitter-scraper` | `https://github.com/Xquik-dev/x-twitter-scraper` | `dc5fa6037d700eb3a7721155e92dabeeb9e56894` | `skills/x-twitter-scraper` |
| `xlsx` | `https://github.com/anthropics/skills` | `3b3fad96af16a10759d930941b4520ba0c40edae` | `skills/xlsx` |

## Local-Only Overlay Reference Installs

These source-mapped overlays are intentionally local-only in this workspace and are not tracked in git:

- `gws-*`: `26` skills sourced from `https://github.com/googleworkspace/cli`.
- `recipe-*`: `32` skills sourced from `https://github.com/googleworkspace/cli`.

Use `scripts/skill-registry.json` for each overlay's exact source path, commit, and rationale.

## Codex-Only Blender Overlay

- `arjun988/blender-skills` is installed only under `C:\Users\LOQ\.codex\skills` from the pinned checkout at `C:\Users\LOQ\.codex\vendor\blender-skills`.
- Its skill names are recorded in `codex_local_only_skill_names` and are excluded from parent promotion. They must never be synchronized into `C:\Users\LOQ\.agents\skills` or `C:\Users\LOQ\.claude\skills`.
- Parent maintenance runs update this overlay with `scripts/update-codex-local-blender-skills.ps1`; the updater refreshes the local Codex copy, manifest, source commit, and protected-name list.

## Child-Path Promotion Notes

- The 2026-08-31 continuation re-audited the personal `.codex`, `.agents`,
  and `.claude` skill roots and found no eligible child-only skills. Protected
  Blender/local-only names, Codex `.system`, copied Superpowers, and project
  paths remained outside promotion and sync ownership.
- The 2026-08-29 continuation re-audited only the personal `.codex`, `.agents`,
  and `.claude` skill roots. No eligible child-only skills remained. A missing
  top-level Codex `doc` mirror was restored by the approved sync script; the
  protected Blender/local-only set and Codex `.system` remained untouched.
- The 2026-08-24 maintenance pass compared only the personal `.codex`,
  `.agents`, and `.claude` skill roots. It promoted five Codex Router-managed
  skills (`codex-app-threads`, `codex-computer-use`, `codex-in-app-browser`,
  `codex-router`, and `codex-router-media`) after omitting their local
  `.codex-router-managed` marker files. Their source package and tree-digest
  provenance is recorded in `scripts/skill-registry.json`.
- Codex `.system` skills, the `94`-skill Blender overlay
  plus `1` separately protected local entry, copied official
  Superpowers, and all project-specific paths under `C:\Assumption University`
  remain excluded from promotion and shared-catalog ownership. No eligible
  child-only skills were found in `.agents` or `.claude` after promotion.
- The 2026-07-29 maintenance pass compared the parent catalog only with the
  personal Codex and Claude skill roots. Project-specific roots under
  `C:\Assumption University` were not scanned or changed.
- Five Codex system-only skills were promoted into normalized parent copies.
  The Codex-owned system copies remain authoritative inside Codex and are
  excluded from top-level Codex mirror writes; the parent copies deploy to the
  shared and Claude roots.
- The existing parent `imagegen` copy was refreshed from the newer Codex
  system bundle without overwriting Codex's managed `.system` copy.
- The 2026-07-11 project-local imports remain cataloged with their original
  provenance, but were not refreshed from project paths during this pass.
- The official `obra/superpowers-skills` catalog was flattened from categorized
  child paths into top-level folders. `using-superpowers` remains as a
  documented compatibility copy from `obra/superpowers`, while `using-skills`
  is the current canonical entrypoint.
- `docx`, `pptx`, and `xlsx` now map to `anthropics/skills`;
  `jupyter-notebook` now maps to `openai/skills`. Their support trees matched
  the current canonical sources, with only the catalog-normalized `SKILL.md`
  wrappers differing.
- Eight Tavily skills map to the official `tavily-ai/skills` repository at
  commit `ea5e8201b0d3ed9c10b70b71187589bd761fe2d2`. Their operational guidance
  is retained with catalog metadata, reviewed installation choices,
  cross-client fallbacks, and the removed-client integration excluded.
- The 2026-08-02 frontend consolidation maps the canonical `frontend-design`
  skill to the historical OpenAI `frontend-skill` source at commit
  `30444aed500c00c85294d12074f6e3ee794f808a`. The canonical folder preserves
  its original MIT license, the modified OpenAI Apache-2.0 material, and the
  reviewed Awesome Copilot MIT attribution. `frontend-skill` and
  `premium-frontend-ui` are retired names, not separate reference installs.
- The 2026-08-08 Matt Pocock audit inspected all `35` live upstream skill
  entrypoints at commit `84fdeffd12f2ee307994d1eb6feb48173b6e0502` and
  imported only eight cross-client gaps: architecture, domain modeling,
  prototypes, primary-source research, conflict resolution, handoffs, and
  agent-document writing. The source MIT license is retained in each imported
  folder.
- The 2026-08-16 child reconciliation compared the eleven newly installed
  skill trees byte-for-byte with their exact current paths in the official
  Supabase, Google Gemini, Vercel, and web-quality repositories. It imported
  `supabase`, `supabase-postgres-best-practices`, `gemini-api-dev`,
  `gemini-interactions-api`, `react-best-practices`, and the five web-quality
  audit leaves without collapsing their distinct activation boundaries.

## Selection And Refresh Notes

- Import new or refreshed skills into `C:\Users\LOQ\.copilot\skills` first;
  downstream roots are deployment targets.
- Prefer canonical upstream sources over discovery catalogs and compare exact
  recorded paths before changing normalized skill content.
- Upstream HEAD movement alone is not a reason to rewrite a skill. On
  2026-07-29, exact-path comparison showed no relevant changes for the tracked
  Awesome Copilot skills, Awesome Codex formula helper, Anthropic
  `mcp-builder`, Google Workspace CLI, OpenAI skills, and the current
  Superpowers catalog.
- Real upstream changes were incorporated for Anthropic document helpers,
  `avoid-ai-writing`, two NVIDIA skills, Stitch workflows and validators, and
  `x-twitter-scraper`.
- The 2026-08-24 source audit compared every recorded source head with its
  exact mapped path. Material mapped changes were refreshed for
  `avoid-ai-writing`, the eight selected Matt Pocock skills, and
  `x-twitter-scraper`; unrelated upstream movement was recorded in the source
  table without rewriting unchanged mapped paths. The catalog baseline and
  per-skill changelogs now use `2026-08-24`.
- The 2026-08-29 source audit refreshed exact mapped paths for
  `avoid-ai-writing`, `x-twitter-scraper`, `gemini-api-dev`,
  `gemini-interactions-api`, `react-view-transitions`, and the current
  web-quality support trees. `awesome-copilot`, NVIDIA, Netlify, MongoDB,
  and Hugging Face heads moved outside installed paths and were recorded in
  provenance without broad rewrites. The catalog baseline now uses
  `2026-08-29`.
- The current Xquik source removed its MCP setup documents and metadata. The
  registry therefore removes the stale preferred Xquik MCP mapping and lets
  the normalized skill state its REST/SDK fallback honestly.
- The 2026-08-31 source audit refreshed the changed `avoid-ai-writing` corpus
  manifest and extraction helper/tests at its current head. `awesome-copilot`
  and NVIDIA heads moved outside installed paths and received provenance-only
  updates.
- The Stitch refresh preserved the previously verified project/design-system
  MCP boundary. Broader screen tools remain optional and must be rediscovered
  in the active host before use.
- Imported skills that handle third-party content retain prompt-injection,
  credential, approval, and private-data boundaries during normalization.
- The 2026-08-16 web-quality import keeps `web-quality-audit` as the aggregate
  router and retains separate `performance`, `core-web-vitals`,
  `accessibility`, `seo`, and `best-practices` leaves; React performance remains
  separate from `react-development`, `nextjs-development`, and `frontend-design`.
- The 2026-08-16 related-skill consolidation audit compared the maintained
  parent with plugin-managed Supabase and React copies. The parent remains
  canonical because it carries catalog metadata, cross-client safeguards,
  explicit fallbacks, and the maintained support trees; plugin copies remain
  external rather than becoming duplicate tracked installs.
- Overlapping upstream TDD, debugging, code review, implementation, planning,
  and skill-authoring workflows remain represented by the stronger existing
  catalog skills rather than being duplicated.
- Copied official Superpowers remain separately classified so maintained
  counts, sync routing, and provenance reporting stay honest.
