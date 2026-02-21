# Subagent Delegation Patterns

## Pattern 1: Boilerplate Generation

**Scenario**: Creating repetitive code structures

```javascript
runSubagent({
  description: "Generate API routes",
  prompt: `Create RESTful API route handlers with these endpoints:
  - GET /api/items - list all
  - GET /api/items/:id - get by ID
  - POST /api/items - create new
  - PUT /api/items/:id - update
  - DELETE /api/items/:id - delete
  
  Adapt to the project's framework (Next.js API Routes, Express, etc.). Include input validation, error handling, and JSDoc comments. Use async/await. Match the style of existing route handlers. Return the complete code.`
})
```

## Pattern 2: Data Transformation

**Scenario**: Converting data formats

```javascript
runSubagent({
  description: "Transform API response",
  prompt: `Write a function transformApiData(apiResponse) that converts the API response format to match the application data model:
  
  Input: { id, title, desc, tags: "comma,separated", metadata: "key:value|pairs" }
  Output: { id, name, description, tags: string[], metadata: Record<string, string> }
  
  Include TypeScript types if used, handle edge cases (nulls, empty strings, malformed data). Return the complete function with error handling.`
})
```

## Pattern 3: File Analysis

**Scenario**: Gathering information from codebase

```javascript
runSubagent({
  description: "Analyze component props",
  prompt: `Search all components in the project and create a list of all prop types/inputs used. For each component, extract: component name, file path, props/inputs (name and type), and typing method (PropTypes/TypeScript/JSDoc/etc.). Detect the framework (React/Vue/Angular/Svelte). Return as a structured JSON array.`
})
```

## Pattern 4: Documentation Generation

**Scenario**: Creating or updating docs

```javascript
runSubagent({
  description: "Generate API docs",
  prompt: `Analyze the API endpoints in the codebase and generate comprehensive API documentation in Markdown format. Document all CRUD operations with: HTTP method, endpoint path, request body schema, response examples, status codes, and error scenarios. Format as a proper API reference for README.md or docs/.`
})
```

## Pattern 5: Utility Function Creation

**Scenario**: Simple helper functions

```javascript
runSubagent({
  description: "Create string utilities",
  prompt: `Create a utilities module with these functions:
  1. truncate(str, maxLength, suffix='...') - truncate with ellipsis
  2. capitalize(str) - capitalize first letter
  3. kebabCase(str) - convert to kebab-case
  4. randomId(length=8) - generate random alphanumeric ID
  
  Use TypeScript, include JSDoc, add input validation. Return the code for src/lib/stringUtils.ts.`
})
```

## Parallel Delegation

For independent tasks, delegate in parallel:

```javascript
// Delegate multiple independent tasks
const task1 = runSubagent({
  description: "Generate types",
  prompt: "Create TypeScript interfaces or type definitions for the main entities (User, Post, Comment, etc.) based on the API schema..."
})

const task2 = runSubagent({
  description: "Create utilities",
  prompt: "Create date/time formatting utilities: formatRelativeTime, formatDuration, parseISO..."
})

const task3 = runSubagent({
  description: "Generate mock data",
  prompt: "Create a mock data generator for the main entities, generating realistic test data (20+ items)..."
})

// Main agent integrates all results
```
