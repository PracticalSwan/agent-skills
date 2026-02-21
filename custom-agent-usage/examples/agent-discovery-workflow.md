# Custom Agent Usage Examples

## Example 1: Finding and Using a Testing Agent

### Step 1: Discover Available Agents

Search for `.agent.md` files in your workspace:

```bash
# Using command line
find . -name "*.agent.md"

# Or using search in your editor
# Search for: *.agent.md
```

### Step 2: Check Agent Frontmatter

Read the `.agent.md` file to verify it can be invoked:

```yaml
---
name: "Playwright Tester Mode"
description: Comprehensive testing with exploratory testing, Playwright test generation
disable-model-invocation: false  # Must be false for subagent delegation
tools: [Read, Write, Bash, WebSearch]
---
```

### Step 3: Use the Agent

```javascript
// Delegate with exact name from frontmatter
runSubagent({
  agentName: "Playwright Tester Mode",
  description: "Test checkout flow",
  prompt: "Perform exploratory testing on the checkout flow: product selection → cart → payment confirmation. Generate comprehensive Playwright tests covering success scenarios, validation errors, edge cases (empty cart, payment failures), and accessibility."
});
```

## Example 2: Finding and Using a Documentation Agent

### Discovery Workflow

```javascript
// 1. Find all .agent.md files
const agentFiles = glob("*.agent.md");

// 2. Read each file's frontmatter
for (const file of agentFiles) {
  const content = readFileSync(file, 'utf8');
  const frontmatter = parseFrontmatter(content);

  console.log({
    name: frontmatter.name,
    description: frontmatter.description,
    invocable: frontmatter.disableModelInvocation === false
  });
}

// 3. Select appropriate agent
// Found: Tech Writer with disable-model-invocation: false

// 4. Delegate task
runSubagent({
  agentName: "Tech Writer",
  description: "Create API documentation",
  prompt: "Create comprehensive API documentation for the authentication endpoints. Include request/response schemas, authentication requirements, error codes, and usage examples."
});
```

## Example 3: Checking Invocability

```javascript
/**
 * Check if an agent can be invoked as a subagent
 */
function isAgentInvocable(agentFilePath) {
  const content = fs.readFileSync(agentFilePath, 'utf8');
  const match = content.match(/disable-model-invocation:\s*(true|false)/);

  if (!match) {
    return false; // Cannot determine if invocable
  }

  return match[1] === 'false';
}

// Usage
const playwrightTester = './agents/Playwright-Tester.agent.md';
if (isAgentInvocable(playwrightTester)) {
  console.log('This agent can be invoked as a subagent');
} else {
  console.log('This agent cannot be invoked as a subagent');
}
```

## Example 4: Getting Agent Name

```javascript
/**
 * Extract agent name from .agent.md frontmatter
 */
function getAgentName(agentFilePath) {
  const content = fs.readFileSync(agentFilePath, 'utf8');

  // Try to extract name from frontmatter
  const nameMatch = content.match(/name:\s*["']([^"']+)["']/);
  if (nameMatch) {
    return nameMatch[1]; // Use name from frontmatter
  }

  // Fallback to filename
  return path.basename(agentFilePath)
    .replace('.agent.md', '')
    .replace('.md', '');
}

// Usage
const agentName = getAgentName('./agents/Code-Explainer.agent.md');
// Returns: "Code Explainer" (from frontmatter)
// or: "Code-Explainer" (from filename if no frontmatter name)
```

## Example 5: Complete Workflow

```javascript
/**
 * Find and use appropriate agent for a task
 */
function delegateToAppropriateAgent(taskDescription) {
  // 1. Find all agent files
  const agentFiles = glob('**/*.agent.md');

  // 2. Extract agent info
  const agents = agentFiles.map(file => ({
    file,
    name: getAgentName(file),
    description: extractDescription(file),
    invocable: isAgentInvocable(file)
  }));

  // 3. Filter invocable agents
  const invocableAgents = agents.filter(a => a.invocable);

  // 4. Find matching agent (simplified matching logic)
  const matchingAgent = invocableAgents.find(agent =>
    taskDescription.toLowerCase().includes(agent.description.toLowerCase().split(' ')[0])
  );

  if (!matchingAgent) {
    console.log('No matching agent found');
    return;
  }

  // 5. Delegate to agent
  runSubagent({
    agentName: matchingAgent.name,
    description: taskDescription,
    prompt: `Handle this task: ${taskDescription}`
  });
}

// Usage
delegateToAppropriateAgent("Test the shopping cart functionality");
// Would find and delegate to "Playwright Tester Mode"
```
