# Agent Task Mapping Examples

## Example 1: Delegating Code Analysis

When you need to analyze existing code patterns in a large codebase:

```javascript
// Task: Analyze authentication flow across multiple files
runSubagent({
  agentName: "Code Explainer",
  description: "Analyze authentication flow",
  prompt: "Analyze the authentication flow in this codebase. Focus on: 1) How users log in, 2) Token management, 3) Session handling, 4) Security patterns. Search for files related to auth, login, session, and tokens. Provide a comprehensive explanation of the flow."
})
```

## Example 2: Delegating Testing

When you need comprehensive test coverage for a feature:

```javascript
// Task: Generate comprehensive Playwright tests
runSubagent({
  agentName: "Playwright Tester Mode",
  description: "Test shopping cart functionality",
  prompt: "Perform exploratory testing on the shopping cart: add items → modify quantities → remove items → checkout. Generate comprehensive Playwright tests covering success scenarios, validation errors, edge cases (empty cart, invalid quantities), and accessibility."
})
```

## Example 3: Delegating Documentation

When you need formal developer documentation:

```javascript
// Task: Create API documentation
runSubagent({
  agentName: "Tech Writer",
  description: "Create API documentation",
  prompt: "Create comprehensive API documentation for the user management endpoints. Include request/response schemas, authentication requirements, error codes, and usage examples."
})
```

## Example 4: Delegating Code Cleanup

When you need to clean up technical debt:

```javascript
// Task: Refactor and simplify code
runSubagent({
  agentName: "Universal Janitor",
  description: "Clean up user service module",
  prompt: "Review the user service module for code quality issues. Refactor to improve readability, remove duplication, add error handling, and ensure consistent patterns. Preserve all functionality while simplifying the code."
})
```

## Example 5: Delegating React Development

When you need React 19+ component implementation:

```javascript
// Task: Build React component with hooks
runSubagent({
  agentName: "Expert React Frontend Engineer",
  description: "Build data table component",
  prompt: "Create a reusable data table component using React 19+ with hooks. Features: sorting, filtering, pagination, virtualization for large datasets. Use TypeScript and follow existing project patterns."
})
```
