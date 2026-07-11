---
name: java-junit
version: "1.3"
last_updated: 2026-07-11
tags: [java, testing, development, quality, automation]
description: "JUnit 5 testing patterns and parameterized-test guidance. Use when writing or reviewing Java unit tests."
---
# JUnit 5+ Best Practices

> Optimized for current Java LTS releases, JUnit 5.x, Mockito 5.x, and modern Maven or Gradle builds.

Your goal is to help me write effective unit tests with JUnit 5, covering both standard and data-driven testing approaches.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Anti-Patterns

- Combining multiple behaviors in one test: A single failure should map cleanly to one broken contract.
- Using sleeps for asynchronous behavior: Time-based tests stay flaky even when the implementation is correct.
- Testing implementation details instead of behavior: Refactors become noisy because the tests are coupled to internals.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Java Junit implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.

## Before and After Example

```java
// Before
@Test
void shouldWork() {
    assertTrue(service.create(user));
}

// After
@Test
void create_WhenEmailAlreadyExists_ThrowsConflictException() {
    // Arrange
    repository.save(existingUser);

    // Act + Assert
    assertThrows(ConflictException.class, () -> service.create(duplicateUser));
}
```

Shifts from a vague happy-path assertion to a precise behavioral test that captures the contract.

## Project Setup

- Use a standard Maven or Gradle project structure.
- Place test source code in `src/test/java`.
- Include dependencies for `junit-jupiter-api`, `junit-jupiter-engine`, and `junit-jupiter-params` for parameterized tests.
- Use build tool commands to run tests: `mvn test` or `gradle test`.

## Test Structure

- Test classes should have a `Test` suffix, e.g., `CalculatorTest` for a `Calculator` class.
- Use `@Test` for test methods.
- Follow the Arrange-Act-Assert (AAA) pattern.
- Name tests using a descriptive convention, like `methodName_should_expectedBehavior_when_scenario`.
- Use `@BeforeEach` and `@AfterEach` for per-test setup and teardown.
- Use `@BeforeAll` and `@AfterAll` for per-class setup and teardown (must be static methods).
- Use `@DisplayName` to provide a human-readable name for test classes and methods.

## Standard Tests

- Keep tests focused on a single behavior.
- Avoid testing multiple conditions in one test method.
- Make tests independent and idempotent (can run in any order).
- Avoid test interdependencies.

## Data-Driven (Parameterized) Tests

- Use `@ParameterizedTest` to mark a method as a parameterized test.
- Use `@ValueSource` for simple literal values (strings, ints, etc.).
- Use `@MethodSource` to refer to a factory method that provides test arguments as a `Stream`, `Collection`, etc.
- Use `@CsvSource` for inline comma-separated values.
- Use `@CsvFileSource` to use a CSV file from the classpath.
- Use `@EnumSource` to use enum constants.

## Assertions

- Use the static methods from `org.junit.jupiter.api.Assertions` (e.g., `assertEquals`, `assertTrue`, `assertNotNull`).
- For more fluent and readable assertions, consider using a library like AssertJ (`assertThat(...).is...`).
- Use `assertThrows` or `assertDoesNotThrow` to test for exceptions.
- Group related assertions with `assertAll` to ensure all assertions are checked before the test fails.
- Use descriptive messages in assertions to provide clarity on failure.

## Mocking and Isolation

- Use a mocking framework like Mockito to create mock objects for dependencies.
- Use `@Mock` and `@InjectMocks` annotations from Mockito to simplify mock creation and injection.
- Use interfaces to facilitate mocking.

## Test Organization

- Group tests by feature or component using packages.
- Use `@Tag` to categorize tests (e.g., `@Tag("fast")`, `@Tag("integration")`).
- Use `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` and `@Order` to control test execution order when strictly necessary.
- Use `@Disabled` to temporarily skip a test method or class, providing a reason.
- Use `@Nested` to group tests in a nested inner class for better organization and structure.

## Common Pitfalls

- Combining multiple behaviors in one test: Failures become ambiguous and the test no longer documents a single contract.
- Using sleeps instead of deterministic setup: Time-based tests stay flaky even when the production code is correct.
- Asserting only that no exception occurred: A test without a meaningful assertion cannot prove the behavior is right.

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:java-junit` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py java-junit` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the JUnit 5+ Best Practices skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [java-docs](../java-docs/SKILL.md): Use it when the workflow also needs Java API and JavaDoc documentation guidance.
- [test-driven-development](../test-driven-development/SKILL.md): Use it when the workflow also needs test-first implementation and regression safety.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
