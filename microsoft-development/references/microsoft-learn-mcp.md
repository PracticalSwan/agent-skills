# Microsoft Learn MCP

This reference summarizes the currently documented Microsoft Learn Docs MCP server workflow as of March 2026.

## Install

```bash
npx -y @microsoft/learn-docs-mcp
```

## Publicly Documented Tool Names

- `microsoft_docs_search`
- `microsoft_docs_fetch`
- `microsoft_docs_extract_code_examples`
- `microsoft_docs_search_by_product`

## Suggested Usage Order

1. `microsoft_docs_search` for broad discovery
2. `microsoft_docs_search_by_product` when the product family matters
3. `microsoft_docs_fetch` for the full document
4. `microsoft_docs_extract_code_examples` when implementation examples are needed

## Good Product Filters

- `azure`
- `dotnet`
- `power-bi`
- `microsoft-graph`
- `windows`
- `microsoft-365`

## Practical Tips

- Include version numbers when relevant, for example `.NET 9`, `Azure Functions v4`, or `ASP.NET Core 9`.
- Search for exact class names when verifying SDK usage.
- Use the fetched page when limits, pricing, or configuration details matter.
