---
name: sql-development
description: T-SQL, stored procedures, and MS SQL Server DBA practices. Use when writing SQL queries, designing schemas, tuning SQL Server performance, managing backups, configuring security, or using SQL Server 2025+ features.
license: Complete terms in LICENSE.txt
---
# SQL Development

Comprehensive SQL development guidelines combining SQL coding standards, stored procedure generation, and MS SQL Server DBA best practices.


## Activation Conditions

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

## References & Resources

### Documentation
- [T-SQL Patterns](./references/tsql-patterns.md) — MERGE, CTEs, PIVOT, JSON operations, window functions, and error handling
- [Performance Tuning](./references/performance-tuning.md) — Execution plans, index tuning, Query Store, and anti-patterns

### Scripts
- [Stored Procedure Template](./scripts/stored-proc-template.sql) — Production-ready SP template with TRY/CATCH, pagination, and dynamic sorting

### Examples
- [Schema Design Example](./examples/schema-design-example.md) — Recipe Management System with 10 tables, stored procedures, and migrations

---

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, Codex, and Gemini CLI.

- GitHub Copilot: keep the folder in a Copilot-visible skill or plugin path, or wrap the workflow as project instructions if the host does not support portable skill folders directly.
- Claude Code: keep the folder in a local skills directory or a compatible plugin or marketplace source.
- Codex: install or sync the folder into `$CODEX_HOME/skills/<skill-name>` and restart Codex after major changes.
- Gemini CLI: this repository generates a project command named `/skills:sql-development` from this skill. Rebuild commands with `python scripts/export-gemini-skill.py sql-development` and then run `/commands reload` inside Gemini CLI.

<!-- PORTABILITY:END -->

<!-- MCP:START -->
## MCP Availability And Fallback

No dedicated MCP server is required for the normal workflow in this skill.

- If the current host lacks an equivalent tool surface, use the bundled scripts, standard shell or editor tooling, and the manual workflow already described in this skill.
- Treat local verification as the fallback evidence path before closing the task.

<!-- MCP:END -->

## Related Skills
| Skill | Relationship |
|-------|-------------|
| [javascript-development](../javascript-development/SKILL.md) | JavaScript and TypeScript database integration patterns |
| [php-development](../php-development/SKILL.md) | PDO/MySQL database access from PHP |
| [mongodb-mongoose](../mongodb-mongoose/SKILL.md) | Alternative NoSQL database approach |
| [powerbi-modeling](../powerbi-modeling/SKILL.md) | SQL sources for Power BI semantic models |
