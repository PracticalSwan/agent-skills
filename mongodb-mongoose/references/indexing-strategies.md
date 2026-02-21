# MongoDB Indexing Strategies

Reference for choosing, creating, and maintaining indexes in MongoDB with Mongoose.

---

## Index Types

### Single Field

Index on one field. Supports queries, sorts, and range scans on that field.

```js
// Mongoose schema
recipeSchema.index({ slug: 1 });

// Shell
db.recipes.createIndex({ slug: 1 });
```

### Compound

Index on multiple fields. Supports queries that match a **prefix** of the index key pattern.

```js
recipeSchema.index({ category: 1, rating: -1, createdAt: -1 });
// Supports queries on:
//   { category }
//   { category, rating }
//   { category, rating, createdAt }
// Does NOT efficiently support:
//   { rating }  (not a prefix)
```

### Multikey

Automatically created when indexing a field that contains an array. Each array element gets an entry.

```js
recipeSchema.index({ tags: 1 });
// Efficiently finds: { tags: "vegetarian" }
```

> A compound index can include **at most one** array field.

### Text

Full-text search index. One per collection.

```js
recipeSchema.index(
  { title: "text", description: "text", "ingredients.name": "text" },
  { weights: { title: 10, description: 5, "ingredients.name": 2 } }
);
// Query: db.recipes.find({ $text: { $search: "pasta tomato" } })
```

### 2dsphere

Geospatial queries on GeoJSON data.

```js
storeSchema.index({ location: "2dsphere" });
// Query: $nearSphere, $geoWithin, $geoIntersects
```

### Hashed

Hash of field value. Supports **equality** only (no range). Used for hashed sharding.

```js
userSchema.index({ email: "hashed" });
```

### Wildcard

Index all fields (or a subtree) in documents with variable schemas.

```js
// Index everything under metadata.*
productSchema.index({ "metadata.$**": 1 });
```

---

## Index Properties

### Unique

Reject duplicate values.

```js
userSchema.index({ email: 1 }, { unique: true });
```

### Partial

Index only documents matching a filter expression. Smaller index, faster writes.

```js
recipeSchema.index(
  { rating: -1 },
  { partialFilterExpression: { status: "published" } }
);
```

> Queries must include the partial filter predicate to use this index.

### Sparse

Only index documents where the field **exists**. Legacy alternative to partial indexes.

```js
userSchema.index({ phone: 1 }, { sparse: true });
```

### TTL (Time-To-Live)

Auto-delete documents after a duration. Works on `Date` fields only.

```js
sessionSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });
// Document deleted when current time >= expiresAt

// Fixed TTL from creation:
logSchema.index({ createdAt: 1 }, { expireAfterSeconds: 86400 }); // 24h
```

---

## Compound Index Ordering — The ESR Rule

Order compound index fields for maximum efficiency:

1. **E**quality — fields tested with `=` (exact match)
2. **S**ort — fields used in `sort()`
3. **R**ange — fields tested with `$gt`, `$lt`, `$in`, `$regex`

**Example**: Find published recipes in a category, sorted by rating, with prep time under 30 min.

```js
// Query
db.recipes.find({
  status: "published",      // Equality
  category: "Italian",      // Equality
  prepTime: { $lte: 30 }   // Range
}).sort({ rating: -1 });    // Sort

// Optimal index: Equality -> Sort -> Range
recipeSchema.index({ status: 1, category: 1, rating: -1, prepTime: 1 });
```

---

## Using explain()

Analyze query plans to verify index usage.

```js
const explanation = await Recipe.find({ category: "Italian" })
  .sort({ rating: -1 })
  .explain("executionStats");

// Key fields to check:
// executionStats.nReturned          — docs returned
// executionStats.totalDocsExamined  — docs scanned (want ≈ nReturned)
// executionStats.totalKeysExamined  — index keys scanned
// winningPlan.stage                 — "IXSCAN" = good, "COLLSCAN" = bad
```

**Quick diagnostic rule**: If `totalDocsExamined >> nReturned`, the index isn't selective enough.

### Mongoose helper

```js
mongoose.set("debug", true); // Log all queries to console
```

---

## Covered Queries

A query is **covered** when the index contains all requested fields — MongoDB never reads the document.

```js
// Index
recipeSchema.index({ category: 1, title: 1, rating: 1 });

// Covered query (projected fields all in index, _id excluded)
db.recipes.find(
  { category: "Mexican" },
  { title: 1, rating: 1, _id: 0 }
);
```

Verify with `explain()`: look for `totalDocsExamined: 0`.

---

## Index Size Considerations

| Factor | Impact |
|--------|--------|
| Number of indexed fields | Each additional field increases index entry size |
| Array fields (multikey) | One entry **per array element** — can explode index size |
| String length | Long strings = larger index; consider hashed index for equality-only |
| Number of indexes | Each index adds write overhead (insert/update/delete) |
| Working set | Indexes should fit in RAM for best performance |

### Check index sizes

```js
db.recipes.stats().indexSizes
// { "_id_": 245760, "category_1_rating_-1": 163840, ... }

db.recipes.stats().totalIndexSize // bytes
```

### Mongoose: list indexes for a model

```js
const indexes = await Recipe.collection.getIndexes();
console.log(indexes);
```

---

## When NOT to Index

Indexes help reads but hurt writes. Avoid indexing when:

- **Low-cardinality fields** — A boolean `isActive` field with 50/50 distribution won't benefit much. Exception: partial indexes filtering on it.
- **Write-heavy, read-rare collections** — Logs or event streams where you rarely query mid-collection.
- **Small collections** — Under ~1000 documents, a collection scan is fast enough.
- **Fields only in aggregation** — If a field is only used deep inside a pipeline after `$group`, the index won't help.
- **Too many indexes per collection** — Each index slows writes. Aim for the fewest indexes that cover your access patterns. Audit with `$indexStats`.
- **Wide compound indexes on flexible queries** — If queries combine fields unpredictably, a few targeted indexes beat one wide one.

### Identifying unused indexes

```js
db.recipes.aggregate([{ $indexStats: {} }]);
// Check "accesses.ops" — if 0 for weeks, consider dropping
```

---

## Mongoose Schema Index Declaration Summary

```js
const recipeSchema = new Schema({ /* ... */ });

// Single field
recipeSchema.index({ slug: 1 }, { unique: true });

// Compound (ESR order)
recipeSchema.index({ status: 1, category: 1, rating: -1 });

// Text search
recipeSchema.index({ title: "text", description: "text" });

// TTL
recipeSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });

// Partial
recipeSchema.index(
  { authorId: 1, createdAt: -1 },
  { partialFilterExpression: { status: "published" } }
);

// Ensure indexes are created (development only)
await mongoose.connection.syncIndexes();
```
