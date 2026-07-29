---
name: dotnet-best-practices
version: "2.0"
last_updated: 2026-07-29
tags: [dotnet, development, testing, quality, automation]
description: "Ensure .NET/C# code follows maintainable, modern best practices. Use when reviewing or improving C# code, solution structure, async patterns, dependency injection, or testability."
---
# .NET/C# Best Practices

> Optimized for current .NET SDK-style projects, C# 12+, ASP.NET Core LTS, and current xUnit, NUnit, or MSTest workflows.

Your task is to ensure .NET/C# code in the selected scope or current solution meets the best practices specific to this project. This includes:

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Documentation & Structure

- Create comprehensive XML documentation comments for all public classes, interfaces, methods, and properties
- Include parameter descriptions and return value descriptions in XML comments
- Follow the established namespace structure: {Core|Console|App|Service}.{Feature}

## Design Patterns & Architecture

- Use primary constructor syntax for dependency injection (e.g., `public class MyClass(IDependency dependency)`)
- Implement the Command Handler pattern with generic base classes (e.g., `CommandHandler<TOptions>`)
- Use interface segregation with clear naming conventions (prefix interfaces with 'I')
- Follow the Factory pattern for complex object creation.

## Dependency Injection & Services

- Use constructor dependency injection with null checks via ArgumentNullException
- Register services with appropriate lifetimes (Singleton, Scoped, Transient)
- Use Microsoft.Extensions.DependencyInjection patterns
- Implement service interfaces for testability

## Resource Management & Localization

- Use ResourceManager for localized messages and error strings
- Separate LogMessages and ErrorMessages resource files
- Access resources via `_resourceManager.GetString("MessageKey")`

## Async/Await Patterns

- Use async/await for all I/O operations and long-running tasks
- Return Task or Task<T> from async methods
- Use ConfigureAwait(false) where appropriate
- Handle async exceptions properly

## Testing Standards

- Use MSTest framework with FluentAssertions for assertions
- Follow AAA pattern (Arrange, Act, Assert)
- Use Moq for mocking dependencies
- Test both success and failure scenarios
- Include null parameter validation tests

## Configuration & Settings

- Use strongly-typed configuration classes with data annotations
- Implement validation attributes (Required, NotEmptyOrWhitespace)
- Use IConfiguration binding for settings
- Support appsettings.json configuration files

## Semantic Kernel & AI Integration

- Use Microsoft.SemanticKernel for AI operations
- Implement proper kernel configuration and service registration
- Handle AI model settings (ChatCompletion, Embedding, etc.)
- Use structured output patterns for reliable AI responses

## Error Handling & Logging

- Use structured logging with Microsoft.Extensions.Logging
- Include scoped logging with meaningful context
- Throw specific exceptions with descriptive messages
- Use try-catch blocks for expected failure scenarios

## Performance & Security

- Use C# 12+ features and .NET 8 optimizations where applicable
- Implement proper input validation and sanitization
- Use parameterized queries for database operations
- Follow secure coding practices for AI/ML operations

## Code Quality

- Ensure SOLID principles compliance
- Avoid code duplication through base classes and utilities
- Use meaningful names that reflect domain concepts
- Keep methods focused and cohesive
- Implement proper disposal patterns for resources

## Anti-Patterns

- Constructing infrastructure inside business code: It defeats dependency injection and makes testing or observability much harder.
- Skipping cancellation and logging in I/O paths: Modern .NET services need both operational visibility and cooperative shutdown behavior.
- Hiding configuration behind magic strings: Options drift across environments when the contract is not explicit.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Dotnet Best Practices implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.

## Before and After Example

```csharp
// Before
public sealed class WeatherService
{
    public async Task<string> GetAsync()
    {
        using var client = new HttpClient();
        return await client.GetStringAsync("https://api.example.com/weather");
    }
}

// After
public sealed class WeatherService(HttpClient client, ILogger<WeatherService> logger)
{
    public async Task<string> GetAsync(CancellationToken cancellationToken)
    {
        logger.LogInformation("Fetching weather data");
        return await client.GetStringAsync("weather", cancellationToken);
    }
}
```

Uses dependency injection, logging, and cancellation instead of constructing infrastructure per call.

## Common Pitfalls

- Constructing infrastructure inside business code: It defeats dependency injection and makes testing or observability much harder.
- Treating async methods like fire-and-forget work: Exceptions and cancellations disappear unless the call chain is designed for them.
- Burying configuration in magic strings: Runtime behavior drifts across environments when options are not strongly typed.

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/dotnet-best-practices` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the .NET/C# Best Practices skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [csharp-xunit](../csharp-xunit/SKILL.md): Use it when the workflow also needs modern xUnit test design in C#.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [development-workflow](../development-workflow/SKILL.md): Use it when the workflow also needs planning, quality gates, and delivery tracking.
- [microsoft-development](../microsoft-development/SKILL.md): Use it when the workflow also needs microsoft development guidance.
