# Refactoring Catalog

Comprehensive catalog of refactoring techniques organized by category. Each entry includes when to apply, before/after examples, and common pitfalls.

---

## 1. Extract Method

**Category:** Composing Methods

**When to use:**
- A code fragment can be grouped together and given a descriptive name
- A method is too long and does multiple things
- Comments explain what a block of code does (the method name should replace the comment)

**Before:**

```javascript
function printInvoice(invoice) {
  console.log("===== Invoice =====");
  console.log(`Date: ${invoice.date}`);

  // calculate total
  let total = 0;
  for (const item of invoice.items) {
    total += item.price * item.quantity;
    if (item.taxable) {
      total += item.price * item.quantity * 0.07;
    }
  }

  // apply discount
  if (invoice.customerType === "premium") {
    total *= 0.9;
  } else if (invoice.customerType === "vip") {
    total *= 0.85;
  }

  console.log(`Total: $${total.toFixed(2)}`);
}
```

**After:**

```javascript
function printInvoice(invoice) {
  printHeader(invoice);
  const total = calculateTotal(invoice);
  console.log(`Total: $${total.toFixed(2)}`);
}

function calculateTotal(invoice) {
  const subtotal = calculateSubtotal(invoice.items);
  return applyDiscount(subtotal, invoice.customerType);
}

function calculateSubtotal(items) {
  return items.reduce((sum, item) => {
    const lineTotal = item.price * item.quantity;
    const tax = item.taxable ? lineTotal * 0.07 : 0;
    return sum + lineTotal + tax;
  }, 0);
}

function applyDiscount(amount, customerType) {
  const discounts = { premium: 0.9, vip: 0.85 };
  return amount * (discounts[customerType] ?? 1);
}

function printHeader(invoice) {
  console.log("===== Invoice =====");
  console.log(`Date: ${invoice.date}`);
}
```

**Pitfalls:**
- Extracting too aggressively, creating one-line methods with no reuse value
- Losing context by naming methods too generically (`doStuff`, `process`)
- Not passing enough context—relying on shared mutable state instead of parameters

---

## 2. Move Method

**Category:** Moving Features Between Objects

**When to use:**
- A method uses more features of another class than the one it's defined on
- Feature Envy smell detected
- A utility method belongs closer to the data it operates on

**Before:**

```javascript
class Order {
  constructor(customer, items) {
    this.customer = customer;
    this.items = items;
  }

  getDiscountedTotal() {
    const subtotal = this.items.reduce((s, i) => s + i.price, 0);
    if (this.customer.loyaltyPoints > 1000) return subtotal * 0.85;
    if (this.customer.loyaltyPoints > 500) return subtotal * 0.9;
    return subtotal;
  }
}
```

**After:**

```javascript
class Customer {
  constructor(name, loyaltyPoints) {
    this.name = name;
    this.loyaltyPoints = loyaltyPoints;
  }

  getDiscountMultiplier() {
    if (this.loyaltyPoints > 1000) return 0.85;
    if (this.loyaltyPoints > 500) return 0.9;
    return 1;
  }
}

class Order {
  constructor(customer, items) {
    this.customer = customer;
    this.items = items;
  }

  getDiscountedTotal() {
    const subtotal = this.items.reduce((s, i) => s + i.price, 0);
    return subtotal * this.customer.getDiscountMultiplier();
  }
}
```

**Pitfalls:**
- Moving a method that legitimately orchestrates multiple objects (it may belong in a service)
- Breaking the public API of a widely-used class without a migration path
- Moving to a class that already has too many responsibilities

---

## 3. Replace Conditional with Polymorphism

**Category:** Simplifying Conditional Expressions

**When to use:**
- A switch/if-else chain selects behavior based on a type or category
- The same conditional structure appears in multiple places
- New types are frequently added, requiring changes in many switch blocks

**Before:**

```typescript
type Shape = { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
    default:
      throw new Error(`Unknown shape: ${(shape as any).kind}`);
  }
}

function perimeter(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return 2 * Math.PI * shape.radius;
    case "rectangle":
      return 2 * (shape.width + shape.height);
    case "triangle":
      // simplified: assumes equilateral
      return 3 * shape.base;
    default:
      throw new Error(`Unknown shape`);
  }
}
```

**After:**

```typescript
interface Shape {
  area(): number;
  perimeter(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area() { return Math.PI * this.radius ** 2; }
  perimeter() { return 2 * Math.PI * this.radius; }
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area() { return this.width * this.height; }
  perimeter() { return 2 * (this.width + this.height); }
}

class Triangle implements Shape {
  constructor(private base: number, private height: number) {}
  area() { return 0.5 * this.base * this.height; }
  perimeter() { return 3 * this.base; }
}
```

**Pitfalls:**
- Over-engineering when the conditional is simple and unlikely to grow
- TypeScript discriminated unions with exhaustive checks may be preferable to class hierarchies
- Adding polymorphism when only one method varies—overkill for a single dispatch point

---

## 4. Introduce Parameter Object

**Category:** Simplifying Method Calls

**When to use:**
- Multiple parameters naturally group together and travel as a pack
- The same parameter group appears in several functions
- The parameter list is growing beyond 3-4 arguments

**Before:**

```typescript
function searchProducts(
  query: string,
  minPrice: number,
  maxPrice: number,
  category: string,
  sortBy: string,
  sortOrder: "asc" | "desc",
  page: number,
  pageSize: number
) {
  // ...
}

function countProducts(
  query: string,
  minPrice: number,
  maxPrice: number,
  category: string
) {
  // ...
}
```

**After:**

```typescript
interface ProductFilter {
  query: string;
  minPrice: number;
  maxPrice: number;
  category: string;
}

interface PaginationOptions {
  sortBy: string;
  sortOrder: "asc" | "desc";
  page: number;
  pageSize: number;
}

function searchProducts(filter: ProductFilter, pagination: PaginationOptions) {
  // ...
}

function countProducts(filter: ProductFilter) {
  // ...
}
```

**Pitfalls:**
- Creating a "god object" that bundles unrelated parameters
- Making optional parameters required because they're in the object
- Losing discoverability—callers now need to know the object shape

---

## 5. Replace Temp with Query

**Category:** Composing Methods

**When to use:**
- A temporary variable holds the result of an expression that could be a method
- The temp is used in multiple places within the method
- Extracting a query method would clarify intent

**Before:**

```javascript
function getPrice(order) {
  const basePrice = order.quantity * order.itemPrice;
  const discount = Math.max(0, order.quantity - 100) * order.itemPrice * 0.05;
  const shipping = Math.min(basePrice * 0.1, 50);
  return basePrice - discount + shipping;
}
```

**After:**

```javascript
function getPrice(order) {
  return basePrice(order) - discount(order) + shipping(order);
}

function basePrice(order) {
  return order.quantity * order.itemPrice;
}

function discount(order) {
  return Math.max(0, order.quantity - 100) * order.itemPrice * 0.05;
}

function shipping(order) {
  return Math.min(basePrice(order) * 0.1, 50);
}
```

**Pitfalls:**
- Performance cost if the query is expensive and called multiple times (cache or memoize)
- Do not apply when the temp captures a snapshot that must not change mid-method
- Over-extracting trivially simple expressions

---

## 6. Decompose Conditional

**Category:** Simplifying Conditional Expressions

**When to use:**
- Complex conditional logic makes the code hard to read
- The condition, then-branch, or else-branch contain substantial logic
- The reader needs to mentally parse what each branch means

**Before:**

```javascript
function calculateCharge(date, quantity, plan) {
  let charge;
  if (
    date.getMonth() >= 5 && date.getMonth() <= 8 &&
    plan.type !== "unlimited" &&
    quantity > plan.includedUnits
  ) {
    charge = quantity * plan.summerRate + plan.summerServiceCharge;
  } else {
    charge = quantity * plan.regularRate;
  }
  return charge;
}
```

**After:**

```javascript
function calculateCharge(date, quantity, plan) {
  if (isSummerSurcharge(date, quantity, plan)) {
    return summerCharge(quantity, plan);
  }
  return regularCharge(quantity, plan);
}

function isSummerSurcharge(date, quantity, plan) {
  const month = date.getMonth();
  return month >= 5 && month <= 8
    && plan.type !== "unlimited"
    && quantity > plan.includedUnits;
}

function summerCharge(quantity, plan) {
  return quantity * plan.summerRate + plan.summerServiceCharge;
}

function regularCharge(quantity, plan) {
  return quantity * plan.regularRate;
}
```

**Pitfalls:**
- Don't extract conditions that are already clear (e.g., `if (user.isAdmin)`)
- Naming the extracted predicate poorly can make things worse, not better
- Don't scatter related logic across too many tiny functions if it harms locality

---

## 7. Consolidate Duplicate Conditional Fragments

**Category:** Simplifying Conditional Expressions

**When to use:**
- The same code appears in every branch of a conditional
- Code before or after a conditional is duplicated across branches

**Before:**

```javascript
function calculateTotal(isSpecialDeal, price, quantity) {
  let total;
  if (isSpecialDeal) {
    total = price * quantity * 0.85;
    sendAnalyticsEvent("purchase", total);
    updateInventory(quantity);
  } else {
    total = price * quantity;
    sendAnalyticsEvent("purchase", total);
    updateInventory(quantity);
  }
  return total;
}
```

**After:**

```javascript
function calculateTotal(isSpecialDeal, price, quantity) {
  const total = isSpecialDeal
    ? price * quantity * 0.85
    : price * quantity;

  sendAnalyticsEvent("purchase", total);
  updateInventory(quantity);
  return total;
}
```

**Pitfalls:**
- Consolidating code that only *looks* the same but has semantic differences
- Moving code outside the conditional when order of execution matters

---

## 8. Replace Magic Number with Named Constant

**Category:** Organizing Data

**When to use:**
- A numeric literal appears in code with no clear meaning
- The same value is used in multiple places
- The value could change in the future (rates, limits, thresholds)

**Before:**

```javascript
function calculateShipping(weight, distance) {
  if (weight > 25) {
    return distance * 0.15 + 12.5;
  }
  if (distance > 500) {
    return weight * 0.08 + 7.99;
  }
  return 4.99;
}
```

**After:**

```javascript
const MAX_STANDARD_WEIGHT_KG = 25;
const LONG_DISTANCE_THRESHOLD_KM = 500;
const HEAVY_RATE_PER_KM = 0.15;
const HEAVY_SURCHARGE = 12.5;
const DISTANCE_RATE_PER_KG = 0.08;
const LONG_DISTANCE_BASE = 7.99;
const STANDARD_SHIPPING = 4.99;

function calculateShipping(weight, distance) {
  if (weight > MAX_STANDARD_WEIGHT_KG) {
    return distance * HEAVY_RATE_PER_KM + HEAVY_SURCHARGE;
  }
  if (distance > LONG_DISTANCE_THRESHOLD_KM) {
    return weight * DISTANCE_RATE_PER_KG + LONG_DISTANCE_BASE;
  }
  return STANDARD_SHIPPING;
}
```

**Pitfalls:**
- Naming constants too generically (`THRESHOLD`, `VALUE_1`)
- Extracting universally obvious values (`0`, `1`, `""`, `100` for percentages)
- Scattering constants far from their usage when they're only used once

---

## 9. Encapsulate Field

**Category:** Organizing Data

**When to use:**
- A public field is accessed directly from outside the class
- You need to add validation, transformation, or observation on field access
- You want to maintain the ability to change internal representation

**Before:**

```typescript
class Employee {
  name: string;
  salary: number;
  department: string;

  constructor(name: string, salary: number, department: string) {
    this.name = name;
    this.salary = salary;
    this.department = department;
  }
}

// usage
employee.salary = -5000; // no validation
```

**After:**

```typescript
class Employee {
  private _name: string;
  private _salary: number;
  private _department: string;

  constructor(name: string, salary: number, department: string) {
    this._name = name;
    this._salary = salary;
    this._department = department;
  }

  get name() { return this._name; }
  set name(value: string) {
    if (!value.trim()) throw new Error("Name cannot be empty");
    this._name = value.trim();
  }

  get salary() { return this._salary; }
  set salary(value: number) {
    if (value < 0) throw new Error("Salary cannot be negative");
    this._salary = value;
  }

  get department() { return this._department; }
  set department(value: string) { this._department = value; }
}
```

**Pitfalls:**
- Adding getters/setters for every field mechanically—only encapsulate when there's a reason
- In TypeScript, consider `readonly` for immutable fields instead of getters
- Setters that silently coerce values can hide bugs

---

## 10. Extract Class

**Category:** Moving Features Between Objects

**When to use:**
- A class has too many responsibilities (violates Single Responsibility Principle)
- A subset of fields and methods form a cohesive group
- The class has grown to the point where its name can't accurately describe everything it does

**Before:**

```typescript
class User {
  name: string;
  email: string;
  street: string;
  city: string;
  state: string;
  zip: string;
  phone: string;
  phoneType: "mobile" | "home" | "work";

  getFullAddress() {
    return `${this.street}\n${this.city}, ${this.state} ${this.zip}`;
  }

  getFormattedPhone() {
    return `(${this.phone.slice(0, 3)}) ${this.phone.slice(3, 6)}-${this.phone.slice(6)}`;
  }

  validateAddress() {
    return this.street && this.city && this.state && this.zip?.length === 5;
  }
}
```

**After:**

```typescript
class Address {
  constructor(
    public street: string,
    public city: string,
    public state: string,
    public zip: string
  ) {}

  format() {
    return `${this.street}\n${this.city}, ${this.state} ${this.zip}`;
  }

  isValid() {
    return !!(this.street && this.city && this.state && this.zip?.length === 5);
  }
}

class Phone {
  constructor(
    public number: string,
    public type: "mobile" | "home" | "work"
  ) {}

  format() {
    return `(${this.number.slice(0, 3)}) ${this.number.slice(3, 6)}-${this.number.slice(6)}`;
  }
}

class User {
  constructor(
    public name: string,
    public email: string,
    public address: Address,
    public phone: Phone
  ) {}
}
```

**Pitfalls:**
- Extracting too early before the class has actually grown
- Creating classes with only data and no behavior (anemic domain model)
- Breaking existing consumers that depend on the flat structure

---

## 11. Replace Error Code with Exception

**Category:** Making Method Calls Simpler

**When to use:**
- A method returns a special value (like `-1`, `null`, or `false`) to indicate an error
- Callers forget to check the return value, leading to silent failures
- Error handling logic pollutes the main flow

**Before:**

```javascript
function withdraw(account, amount) {
  if (amount <= 0) return -1;
  if (amount > account.balance) return -2;
  account.balance -= amount;
  return account.balance;
}

// caller must remember to check
const result = withdraw(account, 500);
if (result === -1) { /* invalid amount */ }
else if (result === -2) { /* insufficient funds */ }
```

**After:**

```javascript
class InvalidAmountError extends Error {
  constructor(amount) {
    super(`Invalid withdrawal amount: ${amount}`);
    this.name = "InvalidAmountError";
  }
}

class InsufficientFundsError extends Error {
  constructor(balance, amount) {
    super(`Cannot withdraw ${amount} from balance of ${balance}`);
    this.name = "InsufficientFundsError";
  }
}

function withdraw(account, amount) {
  if (amount <= 0) throw new InvalidAmountError(amount);
  if (amount > account.balance) throw new InsufficientFundsError(account.balance, amount);
  account.balance -= amount;
  return account.balance;
}
```

**Pitfalls:**
- Throwing exceptions for expected flow control (e.g., "user not found" in a search)
- Not creating specific error classes—generic `Error` loses context
- Missing error boundaries in async code (unhandled promise rejections)

---

## 12. Inline Method / Inline Temp

**Category:** Composing Methods

**When to use:**
- A method body is as clear as its name
- A temp variable is assigned once and used immediately
- An extracted method adds indirection without adding clarity

**Before:**

```javascript
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}
```

**After:**

```javascript
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

**Pitfalls:**
- Inlining a method that is used in multiple places—creates duplication
- Inlining when the extracted name genuinely improves readability
- Inlining complex expressions that become hard to read on one line

---

## Quick Reference Table

| Refactoring | Primary Smell | Risk | Effort |
|---|---|---|---|
| Extract Method | Long Method | Low | Low |
| Move Method | Feature Envy | Medium | Medium |
| Replace Conditional w/ Polymorphism | Switch Statements | Medium | High |
| Introduce Parameter Object | Long Parameter List | Low | Low |
| Replace Temp with Query | Long Method, Temps | Low | Low |
| Decompose Conditional | Complex Conditional | Low | Low |
| Consolidate Duplicate Fragments | Duplicated Code | Low | Low |
| Replace Magic Number | Mysterious Values | Low | Low |
| Encapsulate Field | Public Fields | Low | Medium |
| Extract Class | Large Class | Medium | High |
| Replace Error Code w/ Exception | Error-prone API | Medium | Medium |
| Inline Method / Inline Temp | Needless Indirection | Low | Low |
