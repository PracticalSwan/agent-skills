---
name: microsoft-development
version: "1.3"
last_updated: 2026-07-11
tags: [microsoft, cloud, architecture, operations, quality]
description: "Microsoft docs lookup, code samples, and SDK reference for Azure, .NET, Microsoft 365, Windows, and Power Platform via Microsoft Learn MCP. Use for API reference or official MS documentation retrieval."
---
# Microsoft Development

> Optimized for current Microsoft Graph, Entra ID, PowerShell 7.x, and Microsoft 365 integration workflows.

Use this skill when the answer should come from Microsoft documentation rather than memory or third-party summaries.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Current MCP Reality

Microsoft's Learn Docs MCP server is publicly documented and currently exposes these core tools:

- `microsoft_docs_search`
- `microsoft_docs_fetch`
- `microsoft_docs_extract_code_examples`
- `microsoft_docs_search_by_product`

Microsoft's getting-started docs also describe installation through `npx -y @microsoft/learn-docs-mcp`.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Verifying Azure SDK usage, limits, or configuration
- Looking up .NET, Graph, Windows, or Microsoft 365 APIs
- Pulling official code examples before implementation
- Checking product-specific guidance for Azure, Power BI, or Power Platform

## Recommended Workflow

1. Search first with `microsoft_docs_search`.
2. Narrow by product with `microsoft_docs_search_by_product` when results are broad.
3. Fetch the relevant page with `microsoft_docs_fetch` for details.
4. Extract code examples with `microsoft_docs_extract_code_examples` if the user needs working snippets.
5. Prefer official code and limits over recollection.

## Query Patterns

- `"Azure Container Apps scale rules"`
- `"BlobClient UploadAsync Azure.Storage.Blobs"`
- `product="power-bi" query="row level security dax"`
- `product="microsoft-graph" query="send mail application permissions"`

## Guardrails

- Use Microsoft Learn MCP for Microsoft-specific answers before browsing elsewhere.
- Treat package versions, quotas, and service capabilities as time-sensitive.
- If Learn MCP is unavailable in the current client, use the included scripts and references as local fallbacks, then browse official docs.

## Anti-Patterns

- Changing infrastructure before inspecting the current state: Cloud drift and hidden dependencies make blind edits risky.
- Hardcoding credentials or environment assumptions: Rollouts stop being reproducible and secrets become harder to rotate.
- Skipping rollback, observability, or validation planning: You only notice the missing safeguards after the deployment is already live.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Microsoft Development implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.

## Before and After Example

```powershell
# Before
az deployment group create `
  --resource-group app-rg `
  --template-file main.bicep

# After
$deploymentName = "api-$(Get-Date -Format yyyyMMddHHmmss)"
az deployment group create `
  --name $deploymentName `
  --resource-group app-rg `
  --template-file main.bicep `
  --parameters environment=prod `
  --what-if
```

Moves from an opaque deployment command to a traceable and reviewable workflow with named deployments, explicit parameters, and a preflight diff.

## Common Pitfalls

- Treating vendor examples as drop-in production code: Official snippets usually prove an API, not your project’s retry, logging, or auth requirements.
- Skipping service-specific limits and permissions review: Azure and Microsoft 365 failures often come from quotas or scopes rather than syntax.
- Relying on memory instead of current docs: Microsoft SDK behavior and surface area change often enough that stale recall is risky.

## References & Resources

### Documentation
- [Azure Services Quick Reference](./references/azure-services-quickref.md) - Common Azure services, SDK packages, and decision points
- [.NET Patterns](./references/dotnet-patterns.md) - Practical .NET design and dependency-injection patterns
- [Microsoft Learn MCP](./references/microsoft-learn-mcp.md) - Current tool names, install command, and query workflow

### Scripts
- [Azure Health Check](./scripts/azure-health-check.ps1) - Validate Azure login and inspect common resource health in a resource group

### Examples
- [Azure Function API Example](./examples/azure-function-api-example.md) - Example serverless API workflow tied back to official Microsoft docs

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:microsoft-development` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py microsoft-development` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: Microsoft Learn Docs MCP

- Fallback prompt: "Use the Microsoft Development skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- Use Microsoft Learn in a browser and local SDK or CLI documentation when the docs MCP server is unavailable.
- Verify generated commands or samples with the native toolchain (`dotnet`, `az`, PowerShell, etc.) before shipping them.

<!-- MCP:END -->

## Related Skills

- [azure-integrations](../azure-integrations/SKILL.md): Use it when the workflow also needs Azure deployment and infrastructure automation.
- [powerbi-modeling](../powerbi-modeling/SKILL.md): Use it when the workflow also needs Power BI semantic model design and DAX work.
- [sql-development](../sql-development/SKILL.md): Use it when the workflow also needs SQL query, schema, and performance tuning work.
- [documentation-authoring](../documentation-authoring/SKILL.md): Use it when the workflow also needs drafting structured technical or product documents.
