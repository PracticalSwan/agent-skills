---
name: custom-agent-usage
description: Discovering and using custom agents (.agent.md files) for specialized tasks. Use when finding available .agent.md files, checking agent invocability, understanding agent frontmatter, or using specific custom agent with the agentName parameter. Triggered by keywords like custom agent, .agent.md file, agent discovery, agentName parameter, disable-model-invocation.
license: Complete terms in LICENSE.txt
---

# Custom Agent Usage

## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.copilot/skills/`

## Activation Conditions

**SHOULD activate when delegation requires:**
- Picking a specific custom agent
- Discovering `.agent.md` files
- Verifying invocability (`disable-model-invocation`)

**SHOULD activate when:**
- Discovering available custom agents in workspace
- Understanding .agent.md file structure and frontmatter
- Checking if an agent can be invoked as a subagent
- Learning which agentName to use for delegation
- Understanding agent tools and capabilities

## Non-Activation Conditions

**Do NOT activate this skill when:**
- No custom-agent discovery/selection is needed
- Using purpose-built agents with clear documentation and usage patterns
- Task requires directly implementing solution rather than delegation
- Need to consult documentation about core agents (not custom agents)
- User wants to learn about built-in agents instead of custom ones
- Task is simple enough that delegation would add unnecessary complexity
- Working with agents that don't follow the .agent.md file structure

## Custom Agent Discovery

Custom agents are defined in `.agent.md` files in:
- System prompts directory: `~/.copilot/agents/` or similar
- Project repository: `.copilot/agents/` or `.github/copilot/agents/`

**To discover agents:**
1. Search for `.agent.md` files in the workspace
2. Read frontmatter of each agent file to understand capabilities

## Agent Frontmatter

Key frontmatter fields in `.agent.md`:

| Field | Purpose | Required? |
|--------|-----------|-----------|
| `name` | Display name used in `agentName` parameter | Recommended |
| `description` | What the agent specializes in | Recommended |
| `tools` | Tools available to the agent | Optional |
| `disable-model-invocation` | If false, agent can be invoked as subagent | Required |

## Invocability Check

**CRITICAL**: Only agents with `disable-model-invocation: false` in frontmatter can be invoked as subagents.

Check frontmatter:
```yaml
---
name: "Code Explainer"
description: For analyzing and documenting existing code
disable-model-invocation: false  # Must be false for subagent delegation
tools: [Read, Search]
---
```

## Using Custom Agents

### Step 1: Discover Available Agents

Search for `.agent.md` files:
```bash
# Find agent files in project
find . -name "*.agent.md"

# Or in workspace directory
.search("*.agent.md")
```

### Step 2: Check Invocability

Verify `disable-model-invocation: false` is set.

### Step 3: Get Agent Name

Use the `name` field from frontmatter exactly as is.
- If frontmatter has `name` field value, use that value in quotes
- If name not specified, use filename without `.agent.md` or `.md` extension

### Step 4: Delegate Task

```javascript
runSubagent({
  agentName: "Playwright Tester Mode",  // Must match 'name' from frontmatter exactly
  description: "Test checkout flow",
  prompt: "Perform exploratory testing on the checkout flow: product selection → cart → payment confirmation. Generate comprehensive Playwright tests covering success scenarios, validation errors, edge cases (empty cart, payment failures), and accessibility."
})
```

## Workflow Example

```javascript
// Step 1: Main agent analyzes task and identifies need for testing
// "I need comprehensive testing for the checkout flow"

// Step 2: Discover custom testing agent
// Found: Playwright-Tester.agent.md with disable-model-invocation: false and name: "Playwright Tester Mode"

// Step 3: Delegate to custom agent
runSubagent({
  agentName: "Playwright Tester Mode",
  description: "Test checkout flow",
  prompt: "Perform exploratory testing on the checkout flow: product selection → cart → payment confirmation. Generate comprehensive Playwright tests covering success scenarios, validation errors, edge cases (empty cart, payment failures), and accessibility."
})

// Step 4: Review test output and integrate into test suite
```

## Examples & Scripts

- [Agent Discovery Workflow](./examples/agent-discovery-workflow.md) — Examples of finding and using custom agents
- [Agent Finder Script](./scripts/agent-finder.js) — Node.js script to discover and inspect custom agents
