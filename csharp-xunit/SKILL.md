---
name: csharp-xunit
version: "2.0"
last_updated: 2026-08-14
tags: [dotnet, testing, development, quality, automation]
description: "xUnit testing patterns and data-driven test guidance. Use when writing or reviewing .NET unit tests."
---
# XUnit Best Practices

> Optimized for current .NET SDK releases, C# 12+, xUnit 2.x, and FluentAssertions 6+.

Your goal is to help me write effective unit tests with XUnit, covering both standard and data-driven testing approaches.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Anti-Patterns

- Treating fixtures as hidden setup: Readers lose sight of the behavior under test when too much state is shared implicitly.
- Asserting only the happy path: Unit tests miss the contract if failure and edge cases are not explicit.
- Using vague test names: A failing test should explain the broken behavior before anyone opens the body.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Csharp Xunit implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.

## Before and After Example

```csharp
// Before
[Fact]
public async Task SavesOrder()
{
    var id = await service.SaveAsync(order);
    Assert.True(id > 0);
}

// After
[Fact]
public async Task SaveAsync_WhenOrderIsValid_PersistsAndReturnsId()
{
    // Arrange
    var order = new Order("ORD-42", 3);

    // Act
    var id = await service.SaveAsync(order);

    // Assert
    id.Should().BeGreaterThan(0);
}
```

Moves from a vague assertion to an explicit Arrange-Act-Assert flow with a descriptive name.

## Project Setup

- Use a separate test project with naming convention `[ProjectName].Tests`
- Reference Microsoft.NET.Test.Sdk, xunit, and xunit.runner.visualstudio packages
- Create test classes that match the classes being tested (e.g., `CalculatorTests` for `Calculator`)
- Use .NET SDK test commands: `dotnet test` for running tests

## Test Structure

- No test class attributes required (unlike MSTest/NUnit)
- Use fact-based tests with `[Fact]` attribute for simple tests
- Follow the Arrange-Act-Assert (AAA) pattern
- Name tests using the pattern `MethodName_Scenario_ExpectedBehavior`
- Use constructor for setup and `IDisposable.Dispose()` for teardown
- Use `IClassFixture<T>` for shared context between tests in a class
- Use `ICollectionFixture<T>` for shared context between multiple test classes

## Standard Tests

- Keep tests focused on a single behavior
- Avoid testing multiple behaviors in one test method
- Use clear assertions that express intent
- Include only the assertions needed to verify the test case
- Make tests independent and idempotent (can run in any order)
- Avoid test interdependencies

## Data-Driven Tests

- Use `[Theory]` combined with data source attributes
- Use `[InlineData]` for inline test data
- Use `[MemberData]` for method-based test data
- Use `[ClassData]` for class-based test data
- Create custom data attributes by implementing `DataAttribute`
- Use meaningful parameter names in data-driven tests

## Assertions

- Use `Assert.Equal` for value equality
- Use `Assert.Same` for reference equality
- Use `Assert.True`/`Assert.False` for boolean conditions
- Use `Assert.Contains`/`Assert.DoesNotContain` for collections
- Use `Assert.Matches`/`Assert.DoesNotMatch` for regex pattern matching
- Use `Assert.Throws<T>` or `await Assert.ThrowsAsync<T>` to test exceptions
- Use fluent assertions library for more readable assertions

## Mocking and Isolation

- Consider using Moq or NSubstitute alongside XUnit
- Mock dependencies to isolate units under test
- Use interfaces to facilitate mocking
- Consider using a DI container for complex test setups

## Test Organization

- Group tests by feature or component
- Use `[Trait("Category", "CategoryName")]` for categorization
- Use collection fixtures to group tests with shared dependencies
- Consider output helpers (`ITestOutputHelper`) for test diagnostics
- Skip tests conditionally with `Skip = "reason"` in fact/theory attributes

## Common Pitfalls

- Using vague test names: It becomes hard to tell which behavior failed without opening the test body.
- Hiding setup inside fixtures: Large shared fixtures make tests brittle and obscure the actual cause of a failure.
- Skipping async-specific assertions: Awaitable code often fails in different ways than synchronous code and needs explicit coverage.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/csharp-xunit` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the XUnit Best Practices skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [dotnet-best-practices](../dotnet-best-practices/SKILL.md): Use it when the workflow also needs .NET architecture and maintainability guidance.
- [test-driven-development](../test-driven-development/SKILL.md): Use it when the workflow also needs test-first implementation and regression safety.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
