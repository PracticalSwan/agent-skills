# Complete Refactoring Workflow with Serena

## Scenario

Rename the class `RecipeService` to `RecipeRepository` and its method `getAll` to `findAll` across a TypeScript project. Update all references and document the decision.

---

## Step 1: Check Onboarding

Ensure Serena is initialized for the project.

```
Tool: check_onboarding_performed
Parameters: {}

Response:
  Onboarding has been performed. Project: Kitchen Odyssey
  Languages detected: TypeScript, JavaScript
  Files indexed: 47
```

## Step 2: Read Active Context

Understand current project state before making changes.

```
Tool: read_memory
Parameters:
  name: "active-context"

Response:
  ## Current Focus
  Refactoring service layer to follow repository pattern.

  ## Recent Changes
  - Migrated database calls from controllers to services
  - Added TypeScript strict mode
```

## Step 3: Get Symbols Overview

Map the file structure before diving into specifics.

```
Tool: get_symbols_overview
Parameters:
  relative_path: "src/services/RecipeService.ts"
  depth: 1

Response:
  Classes:
    RecipeService (lines 8-95)
      Methods:
        constructor (line 12)
        getAll (line 20)
        getById (line 35)
        create (line 48)
        update (line 62)
        delete (line 78)
  
  Interfaces:
    RecipeFilters (lines 1-6)
```

## Step 4: Find the Target Class

Read the class declaration (without full body) to understand its interface.

```
Tool: find_symbol
Parameters:
  name_path_pattern: "RecipeService"
  include_body: false
  depth: 1
  relative_path: "src/services/RecipeService.ts"

Response:
  Symbol: RecipeService (class)
  Path: src/services/RecipeService.ts:8-95
  
  Children:
    constructor(db: Database)
    getAll(filters?: RecipeFilters): Promise<Recipe[]>
    getById(id: string): Promise<Recipe | null>
    create(data: CreateRecipeDTO): Promise<Recipe>
    update(id: string, data: UpdateRecipeDTO): Promise<Recipe>
    delete(id: string): Promise<void>
```

## Step 5: Read the Method to Rename

Get the full implementation of `getAll` to prepare for renaming.

```
Tool: find_symbol
Parameters:
  name_path_pattern: "RecipeService/getAll"
  include_body: true

Response:
  async getAll(filters?: RecipeFilters): Promise<Recipe[]> {
    const query = this.db.collection('recipes').find();
    if (filters?.category) {
      query.where('category', filters.category);
    }
    if (filters?.search) {
      query.where('title', { $regex: filters.search, $options: 'i' });
    }
    return query.sort({ createdAt: -1 }).toArray();
  }
```

## Step 6: Find All References to the Class

Understand the impact radius before making changes.

```
Tool: find_referencing_symbols
Parameters:
  name_path_pattern: "RecipeService"
  relative_path: "src/services/RecipeService.ts"

Response:
  References found: 5

  1. src/controllers/RecipeController.ts:3
     import { RecipeService } from '../services/RecipeService';
     → Inside: top-level import

  2. src/controllers/RecipeController.ts:10
     constructor(private recipeService: RecipeService) {}
     → Inside: RecipeController/constructor

  3. src/routes/recipes.ts:5
     import { RecipeService } from '../services/RecipeService';
     → Inside: top-level import

  4. src/routes/recipes.ts:12
     const service = new RecipeService(db);
     → Inside: registerRecipeRoutes

  5. src/tests/recipe.test.ts:4
     import { RecipeService } from '../services/RecipeService';
     → Inside: top-level import
```

## Step 7: Find All References to the Method

```
Tool: find_referencing_symbols
Parameters:
  name_path_pattern: "RecipeService/getAll"
  relative_path: "src/services/RecipeService.ts"

Response:
  References found: 3

  1. src/controllers/RecipeController.ts:18
     const recipes = await this.recipeService.getAll(filters);
     → Inside: RecipeController/index

  2. src/routes/recipes.ts:16
     const recipes = await service.getAll(req.query);
     → Inside: registerRecipeRoutes (anonymous handler)

  3. src/tests/recipe.test.ts:22
     const result = await service.getAll();
     → Inside: describe "RecipeService" / it "returns all recipes"
```

## Step 8: Plan Changes

Based on reference analysis, the change set is:

| File | Change |
|------|--------|
| `src/services/RecipeService.ts` | Rename class to `RecipeRepository`, method `getAll` → `findAll` |
| `src/controllers/RecipeController.ts` | Update import, type annotation, and `getAll` call |
| `src/routes/recipes.ts` | Update import, constructor call, and `getAll` call |
| `src/tests/recipe.test.ts` | Update import, instantiation, and `getAll` call |

Also rename the file: `RecipeService.ts` → `RecipeRepository.ts`

## Step 9: Execute — Replace Class Body

```
Tool: replace_symbol_body
Parameters:
  name_path_pattern: "RecipeService"
  relative_path: "src/services/RecipeService.ts"
  new_body: |
    export class RecipeRepository {
      private db: Database;

      constructor(db: Database) {
        this.db = db;
      }

      async findAll(filters?: RecipeFilters): Promise<Recipe[]> {
        const query = this.db.collection('recipes').find();
        if (filters?.category) {
          query.where('category', filters.category);
        }
        if (filters?.search) {
          query.where('title', { $regex: filters.search, $options: 'i' });
        }
        return query.sort({ createdAt: -1 }).toArray();
      }

      async getById(id: string): Promise<Recipe | null> { ... }
      async create(data: CreateRecipeDTO): Promise<Recipe> { ... }
      async update(id: string, data: UpdateRecipeDTO): Promise<Recipe> { ... }
      async delete(id: string): Promise<void> { ... }
    }

Response:
  Symbol body replaced successfully.
```

## Step 10: Update References

Update each reference file (using standard file edit tools):

**src/controllers/RecipeController.ts:**
- `import { RecipeService }` → `import { RecipeRepository }`
- `private recipeService: RecipeService` → `private recipeRepo: RecipeRepository`
- `this.recipeService.getAll(` → `this.recipeRepo.findAll(`

**src/routes/recipes.ts:**
- `import { RecipeService }` → `import { RecipeRepository }`
- `new RecipeService(db)` → `new RecipeRepository(db)`
- `service.getAll(` → `service.findAll(`

**src/tests/recipe.test.ts:**
- `import { RecipeService }` → `import { RecipeRepository }`
- `new RecipeService(` → `new RecipeRepository(`
- `service.getAll()` → `service.findAll()`

## Step 11: Verify — Old Name Has No References

```
Tool: find_referencing_symbols
Parameters:
  name_path_pattern: "RecipeService"

Response:
  References found: 0
  ✓ No remaining references to old class name.
```

```
Tool: search_for_pattern
Parameters:
  substring_pattern: "getAll"
  relative_path: "src/"
  restrict_search_to_code_files: true

Response:
  No matches found.
  ✓ No remaining references to old method name.
```

## Step 12: Verify — New Name Has Expected References

```
Tool: find_referencing_symbols
Parameters:
  name_path_pattern: "RecipeRepository"

Response:
  References found: 5
  ✓ Matches expected count from Step 6.
```

## Step 13: Update Memories

Record the refactoring decision for future sessions.

```
Tool: edit_memory
Parameters:
  name: "system-patterns"
  content: |
    ## Data Access Pattern
    Using Repository pattern for all data access layers.
    - Services renamed to Repositories (e.g., RecipeService → RecipeRepository)
    - Method naming: findAll, findById, create, update, delete
    - Each repository takes a Database instance in constructor

    ## Naming Convention
    - Repositories: {Entity}Repository (e.g., RecipeRepository, UserRepository)
    - DTOs: Create{Entity}DTO, Update{Entity}DTO
    - Filters: {Entity}Filters
```

```
Tool: edit_memory
Parameters:
  name: "active-context"
  content: |
    ## Current Focus
    Completed RecipeService → RecipeRepository refactor.

    ## Recent Changes
    - Renamed RecipeService to RecipeRepository
    - Renamed getAll to findAll across codebase
    - Established repository naming convention

    ## Next Steps
    - Apply same pattern to UserService, CommentService
    - Update API documentation to reflect new names
```

---

## Summary

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `check_onboarding_performed` | Ensure Serena is ready |
| 2 | `read_memory` | Load current context |
| 3 | `get_symbols_overview` | Map file structure |
| 4-5 | `find_symbol` | Read class and method details |
| 6-7 | `find_referencing_symbols` | Identify all references |
| 8 | (planning) | Determine full change set |
| 9 | `replace_symbol_body` | Execute class rename |
| 10 | file edit tools | Update all references |
| 11-12 | `find_referencing_symbols` + `search_for_pattern` | Verify completeness |
| 13 | `edit_memory` | Document the decision |

**Key principle**: Use symbolic tools to understand impact before editing, then verify after editing. Always update memories so the next session knows what happened.
