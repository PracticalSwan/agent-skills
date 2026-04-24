---
name: code-quality
version: "1.2"
last_updated: 2026-04-25
tags: [code, quality, workflow, planning, delivery]
description: "two-stage review (spec compliance first, then code quality), refactoring, and quality improvement. Use when reviewing code, eliminating code smells, reducing technical debt, refactoring methods, running self-critique loops, or improving maintainability and readability."
---

# Code Quality Management

Comprehensive skill for improving code quality through two-stage review (spec compliance first, then code quality), surgical refactoring, and self-evaluation loops.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.



## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

**two-stage review (spec compliance first, then code quality):**
- Performing two-stage reviews (spec compliance first, then code quality), analyzing pull requests
- Checking code quality, security auditing, performance reviews
- Examining code for bugs, vulnerabilities, best practices violations
- "Review code", "check for issues", "audit code", "analyze PR"

**Refactoring:**
- Code is hard to understand or maintain
- Functions/classes are too large, code smells need addressing
- Adding features is difficult due to code structure
- User asks "clean up this code", "refactor this", "improve this"

**Self-Evaluation:**
- Implementing self-critique and reflection loops for agent outputs
- Building evaluator-optimizer pipelines for quality-critical generation
- Creating test-driven code refinement workflows
- Designing rubric-based or LLM-as-judge evaluation systems
- Adding iterative improvement to agent outputs (code, reports, analysis)
- Measuring and improving agent response quality

## Part 1: two-stage review (spec compliance first, then code quality)

### Review Priorities

When performing a two-stage review (spec compliance first, then code quality), prioritize issues in this order:

#### 🔴 CRITICAL (Block merge)
- **Security**: Vulnerabilities, exposed secrets, authentication/authorization issues
- **Correctness**: Logic errors, data corruption risks, race conditions
- **Breaking Changes**: API contract changes without versioning
- **Data Loss**: Risk of data loss or corruption

#### 🟡 IMPORTANT (Requires discussion)
- **Code Quality**: Severe violations of SOLID principles, excessive duplication
- **Test Coverage**: Missing tests for critical paths or new functionality
- **Performance**: Obvious performance bottlenecks (N+1 queries, memory leaks)
- **Architecture**: Significant deviations from established patterns

#### 🟢 SUGGESTION (Non-blocking improvements)
- **Readability**: Poor naming, complex logic that could be simplified
- **Optimization**: Performance improvements without functional impact
- **Best Practices**: Minor deviations from conventions
- **Documentation**: Missing or incomplete comments/documentation

### Review Principles

1. **Be specific**: Reference exact lines, files, and provide concrete examples
2. **Provide context**: Explain WHY something is an issue and potential impact
3. **Suggest solutions**: Show corrected code when applicable, not just what's wrong
4. **Be constructive**: Focus on improving code, not criticizing the author
5. **Recognize good practices**: Acknowledge well-written code and smart solutions
6. **Be pragmatic**: Not every suggestion needs immediate implementation
7. **Group related comments**: Avoid multiple comments about the same topic

## Part 2: Refactoring

### The Golden Rules

1. **Behavior is preserved** - Refactoring doesn't change what code does, only how
2. **Small steps** - Make tiny changes, test after each
3. **Version control is your friend** - Commit before and after each safe state
4. **Tests are essential** - Without tests, you're not refactoring, you're editing
5. **One thing at a time** - Don't mix refactoring with feature changes

### When NOT to Refactor

- Code that works and won't change again (if it ain't broke...)
- Critical production code without tests (add tests first)
- When you're under a tight deadline
- "Just because" - need a clear purpose

### Refactoring Techniques

#### Extract Method
```javascript
// Before
function processOrder(order) {
    if (order.status === 'pending') {
        // 20 lines of validation logic
        // 15 lines of calculation logic
        // 10 lines of notification logic
    }
}

// After
function processOrder(order) {
    if (order.status === 'pending') {
        validateOrder(order);
        calculateTotals(order);
        sendNotification(order);
    }
}
```

#### Rename Variable/Function
Use meaningful names that describe purpose:
```javascript
// Before
const d = new Date();
process(v, u);

// After
const currentDate = new Date();
processValidation(validatedValue, userId);
```

#### Extract Class
```javascript
// Before
function calculateCartTotal(cart, user, shippingMethod, taxRate) {
    // Complex logic mixing user details, cart items, shipping, tax
}

// After
class OrderCalculator {
    constructor(cart, user) {
        this.cart = cart;
        this.user = user;
    }

    calculate(shippingMethod, taxRate) {
        const subtotal = this.calculateSubtotal();
        const shipping = this.calculateShipping(shippingMethod);
        const tax = this.calculateTax(taxRate);
        return subtotal + shipping + tax;
    }
}
```

### Common Code Smells and Fixes

#### Long Method
**Problem**: Methods longer than 30-50 lines
**Fix**: Extract smaller, focused methods

#### Duplicate Code
**Problem**: Same logic in multiple places
**Fix**: Extract to shared function/method

#### Large Class
**Problem**: Classes with too many responsibilities
**Fix**: Extract smaller, focused classes

#### Magic Numbers
**Problem**: Unnamed numeric literals
```javascript
// Before
if (status > 3) { ... }

// After
const MAX_PENDING_DURATION_DAYS = 3;
if (status > MAX_PENDING_DURATION_DAYS) { ... }
```

#### Feature Envy
**Problem**: Method uses data from another class more than its own
**Fix**: Move method to class it's envious of

---

## Part 3: Self-Evaluation Patterns

### Pattern 1: Basic Reflection

Agent evaluates and improves its own output through self-critique.

```python
def reflect_and_refine(task: str, criteria: list[str], max_iterations: int = 3) -> str:
    """Generate with reflection loop."""
    output = llm(f"Complete this task:\n{task}")

    for i in range(max_iterations):
        # Self-critique
        critique = llm(f"""
        Evaluate this output against criteria: {criteria}
        Output: {output}
        Rate each: PASS/FAIL with feedback as JSON.
        """)

        critique_data = json.loads(critique)
        all_pass = all(c["status"] == "PASS" for c in critique_data.values())
        if all_pass:
            return output

        # Refine based on critique
        failed = {k: v["feedback"] for k, v in critique_data.items() if v["status"] == "FAIL"}
        output = llm(f"Improve to address: {failed}\nOriginal: {output}")

    return output
```

**Key insight**: Use structured JSON output for reliable parsing of critique results.

### Pattern 2: Evaluator-Optimizer

Separate generation and evaluation into distinct components for clearer responsibilities.

```python
class EvaluatorOptimizer:
    def __init__(self, score_threshold: float = 0.8):
        self.score_threshold = score_threshold

    def generate(self, task: str) -> str:
        return llm(f"Complete: {task}")

    def evaluate(self, output: str, task: str) -> dict:
        return json.loads(llm(f"""
        Evaluate output for task: {task}
        Output: {output}
        Return JSON: {{"overall_score": 0-1, "dimensions": {{"accuracy": ..., "clarity": ...}}}
        """))

    def optimize(self, output: str, feedback: dict) -> str:
        return llm(f"Improve based on feedback: {feedback}\nOutput: {output}")

    def run(self, task: str, max_iterations: int = 3) -> str:
        output = self.generate(task)
        for _ in range(max_iterations):
            evaluation = self.evaluate(output, task)
            if evaluation["overall_score"] >= self.score_threshold:
                break
            output = self.optimize(output, evaluation)
        return output
```

### Pattern 3: Code-Specific Reflection

Test-driven refinement loop for code generation.

```python
class CodeReflector:
    def reflect_and_fix(self, spec: str, max_iterations: int = 3) -> str:
        code = llm(f"Write Python code for: {spec}")
        tests = llm(f"Generate pytest tests for: {spec}\nCode: {code}")

        for _ in range(max_iterations):
            result = run_tests(code, tests)
            if result["success"]:
                return code
            code = llm(f"Fix error: {result['error']}\nCode: {code}")
        return code
```

### Evaluation Strategies

#### Outcome-Based
Evaluate whether output achieves expected result.

```python
def evaluate_outcome(task: str, output: str, expected: str) -> str:
    return llm(f"Does output achieve expected outcome? Task: {task}, Expected: {expected}, Output: {output}")
```

#### LLM-as-Judge
Use LLM to compare and rank outputs.

```python
def llm_judge(output_a: str, output_b: str, criteria: str) -> str:
    return llm(f"Compare outputs A and B for {criteria}. Which is better and why?")
```

#### Rubric-Based
Score outputs against weighted dimensions.

```python
RUBRIC = {
    "accuracy": {"weight": 0.4},
    "clarity": {"weight": 0.3},
    "completeness": {"weight": 0.3}
}

def evaluate_with_rubric(output: str, rubric: dict) -> float:
    scores = json.loads(llm(f"Rate 1-5 for each dimension: {list(rubric.keys())}\nOutput: {output}"))
    return sum(scores[d] * rubric[d]["weight"] for d in rubric) / 5
```

---

## Anti-Patterns

- Starting work before the plan or gate is clear: Execution drifts when success criteria are implied instead of explicit.
- Treating verification as optional cleanup: The last mile is where regressions and missing updates are usually hiding.
- Mixing planning, implementation, and release work in one jump: You lose the causal chain that explains why a change is safe.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Code Quality workflow starts from explicit success criteria, constraints, and stop conditions.
2. Pass/fail: Required evidence is collected before any completion, approval, or readiness claim.
3. Pass/fail: The next action follows the documented gate order without skipping review or verification steps.
4. Pressure-test scenario: Apply the workflow under time pressure with one failing check and one tempting shortcut.
5. Success metric: Zero rationalizations; blocked, failed, or unverified work is reported as such.


## Multi-Language Review Examples

### Python
```python
# Before
def approve(order, notifier):
    if order.total > 1000:
        notifier.send(order.customer_email, order.total)
    return order.total

# After
def calculate_total(order: Order) -> int:
    return order.total

def notify_high_value_order(order: Order, notifier: Notifier) -> None:
    if order.total > HIGH_VALUE_THRESHOLD:
        notifier.send(order.customer_email, order.total)
```

### C#
```csharp
// Before
public decimal Process(Order order)
{
    if (order.Total > 1000) _email.Send(order.CustomerEmail, order.Total);
    return order.Total;
}

// After
public decimal CalculateTotal(Order order) => order.Total;

public void NotifyHighValueCustomer(Order order)
{
    if (order.Total > HighValueThreshold)
    {
        _email.Send(order.CustomerEmail, order.Total);
    }
}
```

### Java
```java
// Before
BigDecimal process(Order order) {
    if (order.total().compareTo(THRESHOLD) > 0) {
        email.send(order.customerEmail(), order.total());
    }
    return order.total();
}

// After
BigDecimal calculateTotal(Order order) {
    return order.total();
}

void notifyHighValueCustomer(Order order) {
    if (order.total().compareTo(THRESHOLD) > 0) {
        email.send(order.customerEmail(), order.total());
    }
}
```

### Go
```go
// Before
func Process(order Order, notifier Notifier) int {
    if order.Total > highValueThreshold {
        notifier.Send(order.CustomerEmail, order.Total)
    }
    return order.Total
}

// After
func CalculateTotal(order Order) int {
    return order.Total
}

func NotifyHighValueCustomer(order Order, notifier Notifier) {
    if order.Total > highValueThreshold {
        notifier.Send(order.CustomerEmail, order.Total)
    }
}
```

## AI-Generated Code Specific Checks

- Hallucinated APIs or options: Verify every imported type, method, CLI flag, and config field against the real dependency version before trusting the sample.
- Inconsistent style drift: AI often mixes naming, file structure, or error-handling styles from different codebases, so compare the output against local conventions before merging.
- Over-engineering for a simple requirement: Generated code commonly adds abstractions, wrappers, or extension points that the current task does not need.
- Hidden edge-case gaps: AI can produce convincing happy-path logic while skipping null handling, retries, authorization checks, or cleanup paths.

## Automated Tooling Integration

### ESLint and Prettier
```json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx --max-warnings=0",
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

### SonarQube Scan
```yaml
- name: SonarQube scan
  run: |
    sonar-scanner \
      -Dsonar.projectKey=my-app \
      -Dsonar.sources=src \
      -Dsonar.tests=tests \
      -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
```

### CI Quality Gates

Use CI quality gates to enforce linting, formatting, test coverage, and static-analysis thresholds before review or merge.

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npm test -- --coverage
      - run: sonar-scanner
```

Use the gate to fail fast on lint errors, formatting drift, coverage regressions, and maintainability warnings before review starts.

## Best Practices

### For two-stage reviews (spec compliance first, then code quality)
- Focus on code behavior, not personal style preferences
- Provide actionable feedback with examples
- Balance critique with recognition of good work
- Consider project context and constraints

### For Refactoring
- Always have tests before refactoring
- Commit frequently to maintain safety
- Keep changes small and verifiable
- Document non-obvious refactoring decisions

### For Self-Evaluation
- Define clear, measurable evaluation criteria upfront
- Set iteration limits (3-5) to prevent infinite loops
- Add convergence detection if scores aren't improving
- Log full iteration trajectory for debugging and analysis
- Use structured output (JSON) for reliable parsing

---

## Quality Improvement Checklist

### two-stage review (spec compliance first, then code quality) Checklist
```markdown
## two-stage review (spec compliance first, then code quality) Assessment

### Functionality
- [ ] Logic is correct and achieves intended purpose
- [ ] Edge cases are handled appropriately
- [ ] Error handling is comprehensive
- [ ] No obvious bugs or race conditions

### Code Quality
- [ ] Code is readable and maintainable
- [ ] Naming is descriptive and consistent
- [ ] Functions/classes have single responsibility
- [ ] No unnecessary complexity or obfuscation

### Architecture
- [ ] Follows established project patterns
- [ ] Appropriate use of design patterns
- [ ] Proper separation of concerns
- [ ] No tight coupling or hidden dependencies
```

### Refactoring Checklist
```markdown
## Refactoring Safety Checklist

### Pre-Refactoring
- [ ] Tests exist and pass
- [ ] Version control branch is clean
- [ ] Understand current behavior thoroughly

### During Refactoring
- [ ] Making small, incremental changes
- [ ] Running tests after each change
- [ ] Committing each working intermediate state
- [ ] Preserving external behavior

### Post-Refactoring
- [ ] All tests still pass
- [ ] Code is simpler and clearer
- [ ] No new bugs introduced
- [ ] Documentation updated if needed
```

### Self-Evaluation Checklist
```markdown
## Evaluation Implementation Checklist

### Setup
- [ ] Define evaluation criteria/rubric
- [ ] Set score threshold for "good enough"
- [ ] Configure max iterations (default: 3)

### Implementation
- [ ] Implement generate() function
- [ ] Implement evaluate() function with structured output
- [ ] Implement optimize() function
- [ ] Wire up to refinement loop

### Safety
- [ ] Add convergence detection
- [ ] Log all iterations for debugging
- [ ] Handle evaluation parse failures gracefully

---

## References & Resources

### Documentation
- [Refactoring Catalog](./references/refactoring-catalog.md) — 12 refactoring techniques with before/after code examples and pitfalls
- [Code Smells](./references/code-smells.md) — 17 code smells organized by category with detection signals and remedies

### Scripts
- [Review Checklist](./scripts/review-checklist.py) — Python script for automated static analysis of JS/TS files

### Examples
- [Refactoring Walkthrough](./examples/refactoring-walkthrough.md) — Step-by-step React component refactoring from 160 lines to clean architecture

---

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:code-quality` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py code-quality` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Code Quality Management skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [development-workflow](../development-workflow/SKILL.md): Use it when the workflow also needs planning, quality gates, and delivery tracking.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
- [test-driven-development](../test-driven-development/SKILL.md): Use it when the workflow also needs test-first implementation and regression safety.
- [verification-before-completion](../verification-before-completion/SKILL.md): Use it when the workflow also needs final evidence checks before claiming completion.
