---
name: csharp-xunit
description: 'xUnit testing patterns and data-driven test guidance. Use when writing or reviewing .NET unit tests.'
---
# XUnit Best Practices

Your goal is to help me write effective unit tests with XUnit, covering both standard and data-driven testing approaches.

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

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:csharp-xunit` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py csharp-xunit` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks an equivalent tool surface, use the bundled scripts, standard shell or editor tooling, and the manual workflow already described in this skill.
- Treat local verification as the fallback evidence path before closing the task.

<!-- MCP:END -->
