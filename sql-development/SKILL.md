---
name: sql-development
version: "2.0"
last_updated: 2026-08-14
tags: [sql, development, testing, quality, automation]
description: "T-SQL, stored procedures, and MS SQL Server DBA practices. Use when writing SQL queries, designing schemas, tuning SQL Server performance, managing backups, configuring security, or using SQL Server 2025+ features."
---
# SQL Development

> Optimized for current PostgreSQL, MySQL, and SQL Server releases plus migration-first database workflows.

Comprehensive SQL development guidelines combining SQL coding standards, stored procedure generation, and MS SQL Server DBA best practices.

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Anti-Patterns

- Using `SELECT *` in production queries: It hides contract drift and pulls more data than the caller needs.
- Writing non-SARGable predicates: Functions on indexed columns turn otherwise cheap queries into table scans.
- Ignoring transaction and lock behavior: Correct SQL needs both logical correctness and concurrency safety.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The SQL Development implementation names the target runtime, framework version, and affected files.
2. Pass/fail: Build, lint, test, or equivalent local validation is run for the changed surface.
3. Pass/fail: Edge cases for errors, dependency drift, and environment differences are addressed or explicitly out of scope.
4. Pressure-test scenario: Apply the workflow to a change that passes happy-path tests but fails one boundary condition.
5. Success metric: Zero untested success claims; every implementation claim maps to a command or artifact.

## Before and After Example

```sql
-- Before
SELECT *
FROM Orders
WHERE YEAR(created_at) = 2026;

-- After
SELECT order_id, customer_id, created_at, total_amount
FROM Orders
WHERE created_at >= '2026-01-01'
  AND created_at < '2027-01-01';
```

Uses explicit columns and a SARGable date range so indexes can do their work.

## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

- Writing SQL queries and stored procedures
- Designing database schemas and table structures
- Working with MS SQL Server as a DBA
- Performance tuning and query optimization
- Database backup, restore, and security configuration
- SQL Server 2025+ feature adoption and migration

---

## Part 1: Database Schema Design

### Table Naming
- All table names in singular form
- All column names in singular form

### Required Columns
- All tables must have a primary key column named `id`
- All tables must have `created_at` for creation timestamp
- All tables must have `updated_at` for last update timestamp

### Constraints
- All tables must have a primary key constraint
- All foreign key constraints must have a name
- All foreign key constraints defined inline
- All foreign keys must have `ON DELETE CASCADE`
- All foreign keys must have `ON UPDATE CASCADE`
- All foreign keys must reference the primary key of the parent table

---

## Part 2: SQL Coding Style

### Formatting
- Uppercase for SQL keywords (`SELECT`, `FROM`, `WHERE`)
- Consistent indentation for nested queries
- Comments to explain complex logic
- Break long queries into multiple lines
- Organize clauses: `SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`

### Query Structure
- Use explicit column names, never `SELECT *`
- Qualify column names with table alias when using multiple tables
- Prefer JOINs over subqueries when possible
- Include `LIMIT`/`TOP` clauses to restrict result sets
- Use appropriate indexing for frequently queried columns
- Avoid functions on indexed columns in `WHERE` clauses

---

## Part 3: Stored Procedure Standards

### Naming Conventions
- Prefix with `usp_`
- Use PascalCase: `usp_GetCustomerOrders`
- Include plural noun for multiple records: `usp_GetProducts`
- Include singular noun for single record: `usp_GetProduct`

### Parameter Handling
- Prefix parameters with `@`
- Use camelCase: `@customerId`
- Provide default values for optional parameters
- Validate parameter values before use
- Document parameters with comments
- Required parameters first, optional later

### Structure
- Include header comment block with description, parameters, return values
- Return standardized error codes/messages
- Return result sets with consistent column order
- Use `OUTPUT` parameters for returning status information
- Prefix temporary tables with `tmp_`
- Include `SET NOCOUNT ON` for data-modifying procedures

---

## Part 4: Security Best Practices

### Query Security
- Parameterize all queries to prevent SQL injection
- Use prepared statements for dynamic SQL
- Avoid embedding credentials in SQL scripts
- Proper error handling without exposing system details
- Avoid dynamic SQL in stored procedures

### Transaction Management
- Explicitly begin and commit transactions
- Use appropriate isolation levels
- Avoid long-running transactions that lock tables
- Use batch processing for large data operations

---

## Part 5: MS SQL Server DBA

### Tooling
- Install and enable `ms-mssql.mssql` VS Code extension for full database management
- Use official Microsoft documentation for reference and troubleshooting

### DBA Responsibilities
- Database creation and configuration
- Backup and restore strategies
- Performance tuning and index optimization
- Security management and auditing
- Upgrades and compatibility planning (SQL Server 2025+)

### Best Practices
- Focus on tool-based database inspection over codebase analysis
- Highlight deprecated/discontinued features in SQL Server 2025+
- Encourage secure, auditable, performance-oriented solutions
- Reference official docs for troubleshooting
- Warn about deprecated features and suggest alternatives

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow queries | Check execution plan, add indexes, optimize JOINs |
| Deadlocks | Reduce transaction scope, consistent lock ordering |
| Missing data | Verify CASCADE rules, check transaction isolation |
| Permission errors | Review GRANT/REVOKE statements, check role membership |
| Connection issues | Verify firewall rules, connection strings, SQL auth settings |

---

## Common Pitfalls

- Using `SELECT *` in production queries: It hides contract drift and pulls more data than the caller actually needs.
- Writing non-SARGable predicates: Functions on indexed columns turn otherwise cheap queries into table scans.
- Skipping transaction and lock analysis: Correct SQL needs both logical correctness and concurrency safety.

## References & Resources

### Documentation
- [T-SQL Patterns](./references/tsql-patterns.md) — MERGE, CTEs, PIVOT, JSON operations, window functions, and error handling
- [Performance Tuning](./references/performance-tuning.md) — Execution plans, index tuning, Query Store, and anti-patterns

### Scripts
- [Stored Procedure Template](./scripts/stored-proc-template.sql) — Production-ready SP template with TRY/CATCH, pagination, and dynamic sorting

### Examples
- [Schema Design Example](./examples/schema-design-example.md) — Recipe Management System with 10 tables, stored procedures, and migrations

---

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/sql-development` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the SQL Development skill without MCP. Rely on the local `SKILL.md`, bundled references or scripts, and manual verification. Show the exact commands, evidence, and final checks you used before concluding."
- If the current host does not expose a matching server, use the bundled references, scripts, native toolchain, and manual workflow already described in this skill.
- Treat direct local verification, rendered output, logs, tests, or screenshots as the fallback evidence path before completion.

<!-- MCP:END -->

## Related Skills

- [php-development](../php-development/SKILL.md): Use it when the workflow also needs modern PHP backend implementation.
- [powerbi-modeling](../powerbi-modeling/SKILL.md): Use it when the workflow also needs Power BI semantic model design and DAX work.
- [code-quality](../code-quality/SKILL.md): Use it when the workflow also needs two-stage review (spec compliance first, then code quality), maintainability, and refactoring guidance.
- [systematic-debugging](../systematic-debugging/SKILL.md): Use it when the workflow also needs root-cause debugging before proposing fixes.
