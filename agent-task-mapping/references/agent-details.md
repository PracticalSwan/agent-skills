# Agent Details and Specializations

## Code Explainer

**Purpose**: For analyzing and documenting existing code

**When to use**:
- Analyzing and documenting existing code
- Extracting patterns from codebase
- Creating code architecture documentation
- Explaining complex code sections

**Typical tasks**:
- Analyze authentication flow and create documentation
- Document state management patterns
- Create sequence diagrams for complex flows
- Explain data flow through components

**Example**:
```javascript
runSubagent({
  agentName: "Code Explainer",
  description: "Analyze auth logic",
  prompt: "Analyze the authentication flow in the codebase and create detailed documentation explaining the login/logout mechanism, state management, and token handling. Identify the main auth files and patterns. Include a sequence diagram in Mermaid format."
})
```

## UI Designer

**Purpose**: For UI/UX improvements and design implementations

**When to use**:
- Improving accessibility of forms and components
- Enhancing responsiveness and mobile layouts
- Implementing design system improvements
- Better user feedback and loading states

**Typical tasks**:
- Suggest accessibility improvements for forms
- Improve responsiveness of dashboards
- Add user feedback for validation errors
- Implement loading states and Skeleton screens

**Example**:
```javascript
runSubagent({
  agentName: "UI Designer",
  description: "Improve form layout",
  prompt: "Review the user registration form and suggest improvements for accessibility, responsiveness, and user experience. Provide the updated code with better field validation feedback and loading states."
})
```

## Universal Janitor

**Purpose**: For cleanup, simplification, and tech debt removal

**When to use**:
- Removing unused code and imports
- Refactoring complex functions
- Consolidating duplicate code
- Improving naming consistency

**Typical tasks**:
- Remove unused exports from utility files
- Consolidate duplicate helper functions
- Fix inconsistent naming conventions
- Organize imports and structure

**Example**:
```javascript
runSubagent({
  agentName: "Universal Janitor",
  description: "Clean utility files",
  prompt: "Review all utility files in the project. Remove unused exports, consolidate duplicate functions, fix inconsistent naming, and organize imports. Provide a summary of changes and the refactored code."
})
```

## Critical Thinking

**Purpose**: For challenging assumptions and exploring alternatives

**When to use**:
- Questioning implementation approaches
- Exploring alternative solutions
- Evaluating tradeoffs and constraints
- Identifying overlooked options

**Typical tasks**:
- Explore different caching strategies (Redis, client-side, server-side)
- Question current architecture and propose alternatives
- Evaluate database choices and alternatives
- Assess security approaches and best practices

**Example**:
```javascript
runSubagent({
  agentName: "Critical Thinking",
  description: "Challenge implementation approach",
  prompt: "Challenge the current approach to recipe caching. Explore alternatives like Redis, server-side caching, or client-side caching. Evaluate tradeoffs and recommend optimal solution."
})
```

## Next.js Expert

**Purpose**: For Next.js 15/16+ architecture and optimizations

**When to use**:
- Next.js App Router patterns
- Server vs Client Component optimization
- Data fetching and caching strategies
- Route performance tuning

**Typical tasks**:
- Optimize Next.js routes for Server Components
- Implement proper data fetching patterns
- Configure caching strategies
- Route structure and code organization

**Example**:
```javascript
runSubagent({
  agentName: "Next.js Expert",
  description: "Optimize Next.js route",
  prompt: "Review the Next.js route for recipe listing and suggest optimizations for Server Components vs Client Components, data fetching patterns, and caching strategies."
})
```

## Expert React Frontend Engineer

**Purpose**: For React 19+ patterns and best practices

**When to use**:
- React 19+ features and hooks
- Modern React component patterns
- Performance optimization for React
- State management best practices

**Typical tasks**:
- Implement modern React hooks patterns
- Optimize React component rendering
- Design reusable component patterns
- State management architecture

## Playwright Tester Mode

**Purpose**: For comprehensive web application testing with exploratory testing

**When to use**:
- E2E testing for user flows
- Exploratory testing for edge cases
- Accessibility testing
- Cross-browser testing

**Typical tasks**:
- Test authentication flows (login/signup/logout)
- Generate tests for complex user journeys
- Test forms with validation scenarios
- Accessibility and responsive testing

**Example**:
```javascript
runSubagent({
  agentName: "Playwright Tester Mode",
  description: "Test authentication flow",
  prompt: "Perform exploratory testing on the authentication pages (login/signup) and generate comprehensive Playwright tests covering success scenarios, validation errors, accessibility, and edge cases."
})
```

## Tech Writer

**Purpose**: For creating formal developer documentation

**When to use**:
- Creating comprehensive API documentation
- Writing setup and installation guides
- Developing architecture documentation
- Creating developer tutorials

**Typical tasks**:
- Generate professional API reference docs
- Write setup guides for developers
- Create architecture and design documents
- Develop onboarding tutorials

**Example**:
```javascript
runSubagent({
  agentName: "Tech Writer",
  description: "Create API docs",
  prompt: "Generate professional developer documentation for the recipe management API. Include endpoint descriptions, request/response schemas, authentication requirements, and code examples for the official docs site."
})
```

## Create PRD Chat Mode

**Purpose**: For generating Product Requirements Documents

**When to use**:
- Creating feature specifications
- Defining user stories and acceptance criteria
- Documenting technical requirements
- Product planning documentation

**Typical tasks**:
- Generate PRDs for new features
- Define user stories with acceptance criteria
- Document technical specifications
- Create implementation roadmaps

**Example**:
```javascript
runSubagent({
  agentName: "Create PRD Chat Mode",
  description: "Generate PRD for feature",
  prompt: "Generate a Product Requirements Document for the new bookmark recipes feature. Include user stories, technical specifications, acceptance criteria, and implementation considerations."
})
```

## Specification

**Purpose**: For generating or updating specification documents

**When to use**:
- Creating technical specifications
- Documenting feature requirements
- Defining API contracts
- Architecture specification

**Typical tasks**:
- Create detailed technical specifications
- Document API contracts and schemas
- Define infrastructure specifications
- Create system architecture docs

**Example**:
```javascript
runSubagent({
  agentName: "Specification",
  description: "Create feature spec",
  prompt: "Create a detailed technical specification for implementing the search analytics feature. Include data models, API contracts, UI requirements, and performance considerations."
})
```

## Plan

**Purpose**: Research and outlining multi-step plans

**When to use**:
- Researching best practices
- Outlining implementation approaches
- Planning complex features
- Technology evaluation

**Typical tasks**:
- Research API integration patterns
- Outline feature implementation steps
- Evaluate technology alternatives
- Plan system architecture

**Example**:
```javascript
runSubagent({
  agentName: "Plan",
  description: "Research API integration",
  prompt: "Research best practices for integrating third-party recipe APIs. Outline integration approach, error handling strategies, rate limiting considerations, and fallback mechanisms."
})
```
