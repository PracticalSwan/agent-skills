/**
 * Subagent Delegation Template
 *
 * This is a template file for creating subagent delegation calls.
 * Copy and modify this template for your specific use case.
 */

/**
 * Template for delegating a task to a subagent
 *
 * @param {string} agentName - The name of the agent to delegate to
 * @param {string} description - Brief description of the task
 * @param {string} prompt - Detailed prompt for the subagent
 */
function delegationTemplate(agentName, description, prompt) {
  return {
    agentName,
    description,
    prompt
  };
}

/**
 * Example: Delegating boilerplate generation
 */
function exampleBoilerplateDelegation() {
  return delegationTemplate(
    "Universal Janitor", // or appropriate agent name
    "Generate CRUD boilerplate",
    `Create REST API endpoints for the Product model:
    - id: string (UUID)
    - name: string
    - price: number
    - description: string
    - stock: number

    Generate: GET, POST, PUT, DELETE endpoints with Express.js,
    proper error handling, and input validation.`
  );
}

/**
 * Example: Delegating documentation generation
 */
function exampleDocumentationDelegation() {
  return delegationTemplate(
    "Tech Writer",
    "Generate API documentation",
    `Create API documentation for the authentication endpoints.
    Include request/response examples, error codes, and
    authentication requirements. Output in Markdown format.`
  );
}

/**
 * Example: Delegating code analysis
 */
function exampleCodeAnalysisDelegation() {
  return delegationTemplate(
    "Code Explainer",
    "Analyze component architecture",
    `Analyze the React components in src/components/.
    Identify:
    1. Component hierarchy and relationships
    2. Props passing patterns
    3. State management approach
    4. Shared code that could be extracted

    Provide a summary with recommendations.`
  );
}

/**
 * Checklist before delegating:
 *
 * - [ ] Task is routine/repetitive (not core architecture)
 * - [ ] Task is well-defined with clear acceptance criteria
 * - [ ] Instructions are specific and actionable
 * - [ ] Output format is specified
 * - [ ] Integration plan exists for the output
 * - [ ] Quality criteria are defined
 * - [ ] Security-sensitive logic is NOT being delegated
 */

module.exports = {
  delegationTemplate,
  exampleBoilerplateDelegation,
  exampleDocumentationDelegation,
  exampleCodeAnalysisDelegation
};
