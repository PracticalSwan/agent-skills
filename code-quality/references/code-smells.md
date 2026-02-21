# Code Smells Reference

A catalog of code smells—indicators in source code that suggest deeper structural problems. Each entry describes the smell, how to detect it, its severity, and recommended refactoring.

---

## Bloaters

Smells where code has grown too large to work with effectively.

### Long Method

**Description:** A method that does too much, making it hard to understand, test, and modify. Rule of thumb: if you need a comment to explain a section, that section should be its own method.

**Detection Signals:**
- Function body exceeds 20-30 lines
- Multiple levels of abstraction within one function
- Inline comments explaining "what this block does"
- Difficult to name the function accurately

**Severity:** High — affects readability, testability, and maintainability

**Recommended Refactoring:**
- Extract Method for logical subsections
- Decompose Conditional for complex if/else chains
- Replace Temp with Query to reduce local variables
- Introduce Parameter Object if the method has many parameters

---

### Large Class

**Description:** A class that has taken on too many responsibilities. It typically has many fields, methods, and a name that can't describe everything it does.

**Detection Signals:**
- Class has 10+ methods or 7+ fields
- The class name includes "Manager", "Handler", "Processor", "Utils"
- Instance variables cluster into groups that are used independently
- Multiple developers frequently edit the same class (merge conflicts)

**Severity:** High — violates Single Responsibility Principle, makes changes risky

**Recommended Refactoring:**
- Extract Class for cohesive field/method groups
- Extract Subclass if behaviors vary by type
- Extract Interface to define role-specific contracts

---

### Long Parameter List

**Description:** A method takes more parameters than it can comfortably handle, making calls confusing and error-prone.

**Detection Signals:**
- More than 3-4 parameters
- Boolean parameters (`isAdmin`, `includeDeleted`) that toggle behavior
- Parameters that always travel together
- Callers frequently pass `null` or default values for unused params

**Severity:** Medium — impacts readability and ease of calling

**Recommended Refactoring:**
- Introduce Parameter Object
- Preserve Whole Object (pass the object instead of pulling fields)
- Replace Parameter with Method (let the callee query what it needs)

---

### Primitive Obsession

**Description:** Using primitive types (strings, numbers, booleans) to represent domain concepts instead of small objects or types.

**Detection Signals:**
- Phone numbers, emails, currencies stored as plain strings
- Status represented as string literals (`"active"`, `"pending"`)
- Validation logic scattered wherever the primitive is used
- Constants like `"USD"`, `"EUR"` used in multiple places

**Severity:** Medium — leads to duplication, invalid state, and scattered validation

**Recommended Refactoring:**
- Replace Data Value with Object (`Money`, `Email`, `PhoneNumber`)
- Replace Type Code with Subclasses or Strategy
- Introduce enum/union types for finite sets of values

```typescript
// Before: primitive obsession
function formatPrice(amount: number, currency: string): string { ... }

// After: value object
class Money {
  constructor(readonly amount: number, readonly currency: Currency) {}
  format(): string { ... }
}
```

---

## Object-Orientation Abusers

Smells that indicate misuse of OO principles.

### Switch Statements

**Description:** Complex switch/if-else chains that dispatch based on type codes or string comparisons, often duplicated across the codebase.

**Detection Signals:**
- Same switch on the same type code in multiple methods
- Adding a new type requires changes in many places
- Default/else branch throws or does nothing

**Severity:** Medium-High — violates Open/Closed Principle when types grow

**Recommended Refactoring:**
- Replace Conditional with Polymorphism
- Replace Type Code with Strategy pattern
- Use a lookup map for simple value dispatch

---

### Feature Envy

**Description:** A method that uses more data or methods from another class than its own. The method "envies" another class's features.

**Detection Signals:**
- The method accesses 3+ fields/methods of another object
- The method barely uses its own class's data
- Chained property access: `order.customer.address.city`

**Severity:** Medium — indicates misplaced logic, poor cohesion

**Recommended Refactoring:**
- Move Method to the class whose data it mostly uses
- Extract Method then Move Method for partial envy
- If the method orchestrates multiple objects, it may belong in a service

---

### Refused Bequest

**Description:** A subclass inherits methods or data it doesn't need or use, indicating a flawed hierarchy.

**Detection Signals:**
- Subclass overrides parent methods to throw errors or return nothing
- Subclass only uses a small fraction of inherited behavior
- The "is-a" relationship doesn't hold conceptually

**Severity:** Medium — creates confusing contracts and fragile hierarchies

**Recommended Refactoring:**
- Replace Inheritance with Delegation (composition over inheritance)
- Extract Superclass to share only the common behavior
- Push Down Method/Field to move unused members out of the parent

---

## Change Preventers

Smells that make changes difficult and far-reaching.

### Divergent Change

**Description:** A single class is modified for many different reasons. Each change touches the same class but for unrelated concerns.

**Detection Signals:**
- "Every time we add a new report type, we change this class"
- "Every time we change the database, we change this class"
- Multiple unrelated feature branches modify the same file

**Severity:** High — the class is doing too much

**Recommended Refactoring:**
- Extract Class to separate each axis of change
- Apply Single Responsibility Principle
- Create separate modules for separate concerns

---

### Shotgun Surgery

**Description:** A single change requires small modifications in many different classes. The opposite of Divergent Change.

**Detection Signals:**
- Adding a field requires editing 5+ files
- A "simple" change creates a large diff across many modules
- Related logic is scattered without a unifying abstraction

**Severity:** High — high risk of missing a spot, fragile codebase

**Recommended Refactoring:**
- Move Method / Move Field to consolidate scattered logic
- Inline Class if the split was too granular
- Introduce a Facade or Service to centralize the concern

---

### Parallel Inheritance Hierarchies

**Description:** Every time you create a subclass in one hierarchy, you must create a corresponding subclass in another.

**Detection Signals:**
- Class names mirror each other: `OrderProcessor`/`OrderValidator`, `ReportPDF`/`ReportCSV`
- Adding a type to one hierarchy always requires adding to another
- Hierarchies grow in lockstep

**Severity:** Medium — leads to class explosion and tight coupling

**Recommended Refactoring:**
- Move Method to collapse one hierarchy into the other
- Use composition to eliminate the parallel structure
- Apply Strategy or Visitor pattern

---

## Dispensables

Code elements that contribute nothing and should be removed.

### Dead Code

**Description:** Code that is never executed—unreachable branches, unused variables, commented-out blocks, unexported functions.

**Detection Signals:**
- IDE warnings for unused variables/imports
- `git blame` shows code unchanged for years
- Commented-out blocks with no explanation
- Functions with zero references/callers

**Severity:** Medium — clutters the codebase, confuses readers, makes coverage misleading

**Recommended Refactoring:**
- Delete it. Version control preserves history.
- Remove unused imports (IDE auto-fix or linter)
- Remove commented-out code blocks

---

### Lazy Class

**Description:** A class that doesn't do enough to justify its existence. It may have been created for anticipated complexity that never materialized.

**Detection Signals:**
- Class has 1-2 trivial methods
- Class is a thin wrapper that delegates everything
- No unique behavior beyond what its fields provide
- Class was created "just in case"

**Severity:** Low-Medium — adds unnecessary indirection

**Recommended Refactoring:**
- Inline Class—merge it into the class that uses it
- Collapse Hierarchy if it's a subclass with no unique behavior

---

### Speculative Generality

**Description:** Abstractions, parameters, or infrastructure added for hypothetical future needs that may never come.

**Detection Signals:**
- Abstract classes with only one concrete subclass
- Parameters/hooks that are never used (`options`, `config`, `flags`)
- "We might need this later" comments
- Generic frameworks wrapping simple operations

**Severity:** Medium — adds complexity without providing value (YAGNI violation)

**Recommended Refactoring:**
- Collapse Hierarchy for single-subclass abstractions
- Inline Class for unnecessary delegation
- Remove unused parameters and hooks
- Delete framework code that wraps trivial operations

---

### Duplicated Code

**Description:** The same (or very similar) code structure appears in multiple places. The most common and damaging smell.

**Detection Signals:**
- Copy-paste patterns across methods/classes/files
- Similar logic with minor variations (different variable names, slight condition changes)
- Bug fixes applied in one copy but not others
- Linter reports duplicate blocks

**Severity:** High — bugs must be fixed in multiple places, risk of inconsistency

**Recommended Refactoring:**
- Extract Method for duplicates within a class
- Extract Superclass / Pull Up Method for duplicates across sibling classes
- Extract a shared utility module for duplicates across unrelated classes
- Template Method pattern for algorithms with varying steps

---

## Couplers

Smells that create excessive coupling between classes.

### Message Chains

**Description:** A client asks object A for object B, then asks B for object C, then asks C for D—long chains of navigation.

**Detection Signals:**
- `a.getB().getC().getD().doSomething()`
- Changes in any intermediate class break the chain
- The client knows the internal structure of multiple objects

**Severity:** Medium — tight coupling to object graph structure (Law of Demeter violation)

**Recommended Refactoring:**
- Hide Delegate—add a method on the nearest object that encapsulates the chain
- Move the logic closer to the data it accesses
- Extract Method to name the intent of the chain

---

### Inappropriate Intimacy

**Description:** Two classes excessively access each other's internal details—private fields, internal methods, or implementation specifics.

**Detection Signals:**
- Classes access each other's private/protected members
- Bidirectional dependencies between classes
- Changing one class always requires changing the other
- Classes "reach into" each other frequently

**Severity:** Medium-High — tight coupling, difficult to change independently

**Recommended Refactoring:**
- Move Method / Move Field to resolve the dependency direction
- Extract Class to create a mediating abstraction
- Replace bidirectional association with unidirectional
- Hide Delegate to restore encapsulation

---

### Middle Man

**Description:** A class that delegates almost everything to another class, adding no value itself.

**Detection Signals:**
- Most methods are single-line delegations to another object
- The class has no logic of its own
- Removing the class would simplify the code
- The class exists only to "wrap" another class

**Severity:** Low-Medium — unnecessary indirection

**Recommended Refactoring:**
- Remove Middle Man—let clients talk directly to the delegate
- Inline Class if the wrapper adds zero value

---

## Severity Quick Reference

| Smell | Severity | Primary Impact |
|---|---|---|
| Long Method | High | Readability, testability |
| Large Class | High | Maintainability, SRP violation |
| Duplicated Code | High | Consistency, bug propagation |
| Divergent Change | High | Change impact |
| Shotgun Surgery | High | Change risk |
| Switch Statements | Medium-High | Extensibility |
| Feature Envy | Medium | Cohesion |
| Inappropriate Intimacy | Medium-High | Coupling |
| Primitive Obsession | Medium | Validation, type safety |
| Long Parameter List | Medium | Usability |
| Dead Code | Medium | Clutter, confusion |
| Speculative Generality | Medium | Unnecessary complexity |
| Message Chains | Medium | Coupling |
| Middle Man | Low-Medium | Unnecessary indirection |
| Lazy Class | Low-Medium | Unnecessary abstraction |
| Refused Bequest | Medium | Fragile hierarchy |
| Parallel Inheritance | Medium | Class explosion |
