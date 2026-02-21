# Subagent Delegation Examples

## Example 1: Boilerplate CRUD Generation

When creating multiple similar API endpoints:

```javascript
// Main agent plans the architecture
const dataModel = {
  users: { fields: ['id', 'name', 'email', 'role'], primaryKey: 'id' },
  products: { fields: ['id', 'name', 'price', 'stock'], primaryKey: 'id' },
  orders: { fields: ['id', 'userId', 'productId', 'quantity'], primaryKey: 'id' }
};

// Delegate CRUD boilerplate generation
runSubagent({
  description: "Generate CRUD API endpoints",
  prompt: `Create REST API endpoints for CRUD operations on these data models:
  ${JSON.stringify(dataModel, null, 2)}

  For each model, generate:
  - GET /api/{resource} - List all items with pagination
  - GET /api/{resource}/:id - Get single item
  - POST /api/{resource} - Create new item
  - PUT /api/{resource}/:id - Update item
  - DELETE /api/{resource}/:id - Delete item

  Use Express.js with async/await, proper error handling, and input validation.`
});
```

## Example 2: Data Transformation

When converting data between formats:

```javascript
// Task: Convert CSV data to JSON schema
runSubagent({
  description: "Transform CSV to JSON schema",
  prompt: `Convert this CSV data to a TypeScript interface and JSON schema:

  CSV Headers: firstName, lastName, email, age, signupDate

  Generate:
  1. TypeScript interface with proper types
  2. JSON Schema for validation
  3. Zod schema for runtime validation
  4. Migration function to convert existing CSV data`
});
```

## Example 3: Code Analysis

When analyzing codebase for patterns:

```javascript
// Task: Find all error handling patterns
runSubagent({
  description: "Analyze error handling patterns",
  prompt: `Search the codebase for error handling patterns. Look for:
  1. Try-catch blocks and their structure
  2. Custom error classes
  3. Error logging approaches
  4. Error response formats in API routes

  Summarize the current patterns and identify inconsistencies.`
});
```

## Example 4: Documentation Generation

When generating docs from existing code:

```javascript
// Task: Generate API documentation
runSubagent({
  description: "Generate API documentation",
  prompt: `Analyze all API route files in src/routes/ and generate:
  1. OpenAPI/Swagger specification
  2. Markdown documentation for each endpoint
  3. Example requests/responses
  4. Authentication requirements

  Include all query parameters, request bodies, and response schemas.`
});
```

## Example 5: Utility Creation

When creating reusable utility functions:

```javascript
// Task: Create validation utilities
runSubagent({
  description: "Create validation utilities",
  prompt: `Create TypeScript validation utilities for common data types:
  1. Email validation with regex
  2. Phone number validation (international)
  3. Password strength checker
  4. URL validation
  5. UUID validation

  Each function should return { valid: boolean, errors: string[] }.
  Include unit tests for each utility.`
});
```
