"""Pinned vendor skill sources selected from the VoltAgent discovery catalog.

The VoltAgent repository is an index, not a source tree.  Keep the canonical
vendor repositories and the exact skill paths here so imports, provenance, and
future refreshes use one reviewed selection.
"""

from __future__ import annotations

from typing import TypedDict


SNAPSHOT_DATE = "2026-08-31"

SOURCE_COMMITS = {
    "vercel_agent_skills": (
        "https://github.com/vercel-labs/agent-skills",
        "063bee94c3f4df8453406c830b0a7df0f2860278",
    ),
    "netlify_context_and_tools": (
        "https://github.com/netlify/context-and-tools",
        "4645e4c47ae4a42a3955c96c1389bbc16f10d457",
    ),
    "mongodb_agent_skills": (
        "https://github.com/mongodb/agent-skills",
        "47cc46148f53145eb9b880d2bf1aa89bc9097818",
    ),
    "supabase_agent_skills": (
        "https://github.com/supabase/agent-skills",
        "8331f910845103c08d51f6ca1d86ebb7d1f745e3",
    ),
    "figma_mcp_server_guide": (
        "https://github.com/figma/mcp-server-guide",
        "7f6562c4900fafb46e5e8fd3cc8ced954779bab3",
    ),
    "huggingface_skills": (
        "https://github.com/huggingface/skills",
        "cead19e10754e773bad24fecef83cb64be24094e",
    ),
}


class SkillSpec(TypedDict):
    source_key: str
    source_path: str
    vendor: str
    mcp_server: str | None
    copy_repo_license: bool
    related: tuple[str, ...]


def _spec(
    source_key: str,
    source_path: str,
    *,
    vendor: str,
    mcp_server: str | None = None,
    copy_repo_license: bool = False,
    related: tuple[str, ...] = (),
) -> SkillSpec:
    return {
        "source_key": source_key,
        "source_path": source_path,
        "vendor": vendor,
        "mcp_server": mcp_server,
        "copy_repo_license": copy_repo_license,
        "related": related,
    }


def _group(
    names: tuple[str, ...],
    source_key: str,
    source_prefix: str,
    *,
    vendor: str,
    mcp_server: str | None = None,
    copy_repo_license: bool = False,
    related: tuple[str, ...] = (),
) -> dict[str, SkillSpec]:
    return {
        name: _spec(
            source_key,
            f"{source_prefix}/{name}",
            vendor=vendor,
            mcp_server=mcp_server,
            copy_repo_license=copy_repo_license,
            related=related,
        )
        for name in names
    }


PLATFORM_SKILLS: dict[str, SkillSpec] = {
    **_group(
        (
            "composition-patterns",
            "deploy-to-vercel",
            "react-native-skills",
            "react-view-transitions",
            "vercel-cli-with-tokens",
            "vercel-optimize",
            "web-design-guidelines",
            "writing-guidelines",
        ),
        "vercel_agent_skills",
        "skills",
        vendor="Vercel",
        related=("react-best-practices", "frontend-design", "vercel-deploy"),
    ),
    **_group(
        (
            "netlify-access-control",
            "netlify-agent-runner",
            "netlify-ai-gateway",
            "netlify-blobs",
            "netlify-caching",
            "netlify-config",
            "netlify-database",
            "netlify-deploy",
            "netlify-edge-functions",
            "netlify-forms",
            "netlify-frameworks",
            "netlify-functions",
            "netlify-identity",
            "netlify-image-cdn",
            "netlify-mcp-servers",
        ),
        "netlify_context_and_tools",
        "skills",
        vendor="Netlify",
        copy_repo_license=True,
        related=("netlify-deploy", "netlify-config", "verification-before-completion"),
    ),
    **_group(
        (
            "mongodb-atlas-stream-processing",
            "mongodb-connection",
            "mongodb-mcp-setup",
            "mongodb-natural-language-querying",
            "mongodb-query-optimizer",
            "mongodb-schema-design",
            "mongodb-search-and-ai",
        ),
        "mongodb_agent_skills",
        "skills",
        vendor="MongoDB",
        mcp_server="MongoDB MCP Server",
        copy_repo_license=True,
        related=("mongodb-mongoose", "verification-before-completion"),
    ),
    **_group(
        (
            "figma-code-connect",
            "figma-create-new-file",
            "figma-design-to-code",
            "figma-generate-design",
            "figma-generate-diagram",
            "figma-generate-library",
            "figma-implement-motion",
            "figma-swiftui",
            "figma-use",
            "figma-use-figjam",
            "figma-use-motion",
            "figma-use-slides",
        ),
        "figma_mcp_server_guide",
        "skills",
        vendor="Figma",
        mcp_server="Figma MCP Server",
        related=("figma", "figma-implement-design", "verification-before-completion"),
    ),
}


_HF_SKILLS = (
    "hf-cloud-aws-context-discovery",
    "hf-cloud-python-env-setup",
    "hf-cloud-sagemaker-deployment-planner",
    "hf-cloud-sagemaker-iam-preflight",
    "hf-cloud-sagemaker-production-defaults",
    "hf-cloud-serving-image-selection",
    "huggingface-best",
    "huggingface-community-evals",
    "huggingface-datasets",
    "huggingface-gradio",
    "huggingface-llm-trainer",
    "huggingface-local-models",
    "huggingface-lora-space-builder",
    "huggingface-paper-publisher",
    "huggingface-papers",
    "huggingface-spaces",
    "huggingface-tool-builder",
    "huggingface-trackio",
    "huggingface-vision-trainer",
    "huggingface-zerogpu",
    "train-sentence-transformers",
    "transformers-js",
    "trl-training",
)

PLATFORM_SKILLS.update(
    _group(
        _HF_SKILLS,
        "huggingface_skills",
        "skills",
        vendor="Hugging Face",
        copy_repo_license=True,
        related=("research", "huggingface-gradio", "transformers-js"),
    )
)
PLATFORM_SKILLS["hf-mcp"] = _spec(
    "huggingface_skills",
    "hf-mcp/skills/hf-mcp",
    vendor="Hugging Face",
    mcp_server="Hugging Face MCP Server",
    copy_repo_license=True,
    related=("huggingface-tool-builder", "research", "verification-before-completion"),
)


# These are deliberately absent from PLATFORM_SKILLS because the requested
# local-runtime gate was not met on 2026-08-20: `hf`/`huggingface-cli` and
# `hf-mem`'s command-line runtime are not installed on this laptop.
CLI_SKILLS_NOT_INSTALLED = ("hf-cli", "hf-mem")


SOURCE_CLONE_DIRS = {
    "vercel_agent_skills": "vercel-agent",
    "netlify_context_and_tools": "netlify",
    "mongodb_agent_skills": "mongodb",
    "figma_mcp_server_guide": "figma",
    "huggingface_skills": "huggingface",
}


MCP_FALLBACKS = {
    "MongoDB MCP Server": (
        "Use the official MongoDB documentation, drivers, Atlas UI, or local read-only fixtures when the MongoDB MCP Server is unavailable.",
        "Do not request, paste, or commit connection strings, service-account secrets, or API keys.",
    ),
    "Figma MCP Server": (
        "Use user-provided Figma exports, screenshots, variables, local design-system files, or official Figma documentation when Figma MCP is unavailable.",
        "Do not claim node metadata, screenshots, assets, or canvas writes unless the active host exposed and completed those calls.",
    ),
    "Hugging Face MCP Server": (
        "Use official huggingface.co documentation, APIs, and local fixtures when the Hugging Face MCP Server is unavailable.",
        "Keep Hub tokens in an approved secret store and never paste or commit them.",
    ),
}


def tags_for(name: str, vendor: str) -> str:
    values = [vendor.lower().replace(" ", "-")]
    values.extend(part for part in name.split("-") if part not in values)
    return "[" + ", ".join(dict.fromkeys(values)) + "]"
