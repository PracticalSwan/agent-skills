# Custom Agent Discovery Workflow

## Frontmatter Structure

Proper `.agent.md` frontmatter:

```yaml
---
name: "Display Name"
description: Brief description of what this agent does
disable-model-invocation: false  # Required: must be false for subagent delegation
tools: [List of tools available]
---
```

## Key Fields Explained

### `name`
- **Purpose**: Display name used when calling `runSubagent`
- **Required**: Not strictly required, but highly recommended for clear delegation
- **Usage**: Use this exact value in `agentName` parameter
- **Format**: Can include spaces, should be descriptive

### `description`
- **Purpose**: Explains what the agent specializes in
- **Required**: Recommended for agent discoverability
- **Content**: Should describe purpose and use cases

### `disable-model-invocation`
- **Purpose**: Controls whether agent can be invoked via `runSubagent`
- **Required**: Yes, for subagent delegation
- **Value**: Must be `false` for subagent invocation
- **When `true`**: Agent cannot be delegated to directly

### `tools`
- **Purpose**: Lists tools available to the agent
- **Required**: Optional
- **Format**: Array of tool names
- **Usage**: Helps understand agent capabilities

## Discoverable Agents

Examples of properly configured agents:

```yaml
---
name: "Code Explainer"
description: For analyzing and documenting existing code
disable-model-invocation: false
tools: [Read, Search, Symbol]
---
```

```yaml
---
name: "Playwright Tester Mode"
description: For comprehensive web application testing
disable-model-invocation: false
tools: [Browser, Page, Locator]
---
```

## Search Patterns

### Command Line

```bash
# Find all agent files
find . -name "*.agent.md"

# Find in specific directory
find .github/copilot/agents -name "*.agent.md"
```

### VS Code Search

- Use file search with pattern: `*.agent.md`
- Include: `**/*.agent.md`
- Exclude: `node_modules/**`

## Validation Checklist

Before using an agent as a subagent, verify:

- [ ] File follows `.agent.md` naming convention
- [ ] Has valid YAML frontmatter with `---` delimiters
- [ ] `disable-model-invocation` is explicitly set to `false`
- [ ] `name` field is present and meaningful
- [ ] `description` explains agent's purpose clearly
- [ ] File is in discoverable location (project or system directory)
