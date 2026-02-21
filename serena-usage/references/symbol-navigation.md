# Symbol-Based Code Navigation Guide

## Overview

Serena provides semantic code navigation through symbol-aware tools. Instead of reading entire files line-by-line, you navigate by symbol names (classes, functions, methods, variables) — dramatically reducing token usage and improving precision.

## Core Tools

### get_symbols_overview

Get a high-level map of all symbols in a file. Always start here when exploring an unfamiliar file.

```
Tool: get_symbols_overview
Parameters:
  relative_path: "src/services/AuthService.ts"
  depth: 0  # 0 = top-level only (default)
```

**Return format**: Symbols grouped by kind (classes, functions, variables, interfaces) in compact JSON.

**depth parameter**:
- `0` — Top-level symbols only (class names, standalone functions)
- `1` — One level deep (class + its methods)
- `2` — Two levels deep (class + methods + nested items)

Use `depth: 1` when you need to see a class's API surface without reading implementations.

### find_symbol

Locate and optionally read a specific symbol by its name path.

```
Tool: find_symbol
Parameters:
  name_path_pattern: "AuthService/login"
  include_body: true
  relative_path: "src/services/AuthService.ts"  # optional, speeds up search
```

**Name path patterns**:

| Pattern | Matches |
|---|---|
| `AuthService` | The class/module `AuthService` |
| `AuthService/login` | The `login` method inside `AuthService` |
| `AuthService/__init__` | Python constructor of `AuthService` |
| `AuthService/constructor` | TypeScript/JS constructor |
| `*Service` | Any symbol ending in `Service` (substring match) |
| `Auth*` | Any symbol starting with `Auth` |
| `*/login` | Method named `login` in any class |

**Key parameters**:
- `include_body: false` — Returns signature/declaration only (saves tokens)
- `include_body: true` — Returns full implementation
- `depth: 1` — Also returns immediate children (methods of a class)
- `relative_path` — Scope search to a specific file or directory

### find_referencing_symbols

Find all places where a symbol is used across the codebase.

```
Tool: find_referencing_symbols
Parameters:
  name_path_pattern: "AuthService/login"
  relative_path: "src/services/AuthService.ts"  # file containing the definition
```

Returns:
- File paths where the symbol is referenced
- Code snippets around each reference
- Symbolic context (which function/class contains the reference)

## Practical Workflows

### Exploring a Class Hierarchy

**Goal**: Understand a class, its API, and how it's used.

```
Step 1: Get file overview
  get_symbols_overview(relative_path="src/models/User.ts", depth=1)
  → See class name, all methods, properties

Step 2: Read specific methods of interest
  find_symbol(name_path_pattern="User/validatePassword", include_body=true)
  → Full implementation of validatePassword

Step 3: Check inheritance/implementation
  find_symbol(name_path_pattern="User", include_body=false, depth=0)
  → See class declaration with extends/implements

Step 4: Find subclasses
  search_for_pattern(substring_pattern="extends User", restrict_search_to_code_files=true)
  → All classes that extend User
```

### Finding All Callers of a Function

**Goal**: Understand the impact of changing a function's signature.

```
Step 1: Locate the function
  find_symbol(name_path_pattern="calculateTax", include_body=false)
  → Find where it's defined, see its signature

Step 2: Find all references
  find_referencing_symbols(name_path_pattern="calculateTax", relative_path="src/utils/tax.ts")
  → Every file and location that calls calculateTax

Step 3: Understand each call site
  For each reference, find_symbol on the containing function with include_body=true
  → See context of how calculateTax is called
```

### Understanding Module Dependencies

**Goal**: Map how modules connect before restructuring.

```
Step 1: Overview of the module
  get_symbols_overview(relative_path="src/services/", depth=1)
  → All exported symbols across service files

Step 2: Pick key exports and trace usage
  find_referencing_symbols(name_path_pattern="RecipeService")
  → Who imports and uses RecipeService

Step 3: Check internal dependencies
  search_for_pattern(
    substring_pattern="import.*from",
    relative_path="src/services/RecipeService.ts"
  )
  → What RecipeService itself depends on
```

### Targeted Reading of a Large File

**Goal**: Understand a 500+ line file without reading it all.

```
Step 1: Get the map
  get_symbols_overview(relative_path="src/components/DataTable.tsx", depth=1)
  → See all components, hooks, helpers in the file

Step 2: Read only what matters
  find_symbol(name_path_pattern="DataTable/handleSort", include_body=true)
  find_symbol(name_path_pattern="DataTable/renderHeader", include_body=true)
  → Read just the 2 methods relevant to your task

Step 3: Skip the rest
  → No need to read 400 lines of unrelated rendering code
```

### Safe Refactoring Workflow

**Goal**: Rename a method ensuring no breakage.

```
Step 1: Find the symbol
  find_symbol(name_path_pattern="UserService/getUser", include_body=true)
  → See current implementation

Step 2: Find all call sites
  find_referencing_symbols(name_path_pattern="UserService/getUser")
  → Every location that calls getUser

Step 3: Plan the change
  Review each call site to confirm the rename is safe

Step 4: Execute replacement
  replace_symbol_body(name_path_pattern="UserService/getUser", new_body="...")
  → Replace the method definition

Step 5: Update references
  For each call site, use appropriate edit tools to update the name

Step 6: Verify
  find_referencing_symbols for the OLD name → should return nothing
  find_referencing_symbols for the NEW name → should match expected count
```

## search_for_pattern (Fallback)

When you don't know exact symbol names, use pattern search as a discovery step:

```
Tool: search_for_pattern
Parameters:
  substring_pattern: "async.*fetch.*recipe"
  restrict_search_to_code_files: true
  relative_path: "src/"  # scope to src directory
  context_lines_before: 2
  context_lines_after: 2
```

**Tips**:
- Use non-greedy quantifiers: `.*?` instead of `.*`
- Scope with `relative_path` to avoid huge result sets
- Set `restrict_search_to_code_files: true` to skip config/data files
- Use `context_lines_before/after` to see surrounding code

## Performance Tips

1. **Always scope searches with `relative_path`** — Searching the entire repo is slow
2. **Use `include_body: false` first** — Read signatures before implementations
3. **Start with `depth: 0`** — Drill deeper only when needed
4. **Prefer symbolic tools over `read_file`** — One `find_symbol` call replaces reading 50+ lines
5. **Combine overview + targeted reads** — `get_symbols_overview` then `find_symbol` for specific items
6. **Use `search_for_pattern` as last resort** — Symbolic tools are faster and more precise
