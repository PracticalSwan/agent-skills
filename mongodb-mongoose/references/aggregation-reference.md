# MongoDB Aggregation Pipeline Reference

Quick-reference for aggregation stages, accumulators, and expression operators used with Mongoose's `Model.aggregate()`.

---

## Pipeline Stages

### $match

Filter documents (like `find()`). Place early to leverage indexes.

```js
{ $match: { status: "published", rating: { $gte: 4 } } }
```

### $group

Group documents by key and apply accumulators.

```js
{
  $group: {
    _id: "$category",
    count: { $sum: 1 },
    avgRating: { $avg: "$rating" },
    recipes: { $push: "$title" }
  }
}
```

### $project

Reshape documents — include, exclude, or compute fields.

```js
{
  $project: {
    title: 1,
    authorName: "$author.name",
    ingredientCount: { $size: "$ingredients" },
    _id: 0
  }
}
```

### $lookup

Left outer join to another collection.

```js
{
  $lookup: {
    from: "users",
    localField: "authorId",
    foreignField: "_id",
    as: "author"
  }
}
```

**Pipeline variant** (correlated sub-query):

```js
{
  $lookup: {
    from: "comments",
    let: { recipeId: "$_id" },
    pipeline: [
      { $match: { $expr: { $eq: ["$recipeId", "$$recipeId"] } } },
      { $sort: { createdAt: -1 } },
      { $limit: 5 }
    ],
    as: "recentComments"
  }
}
```

### $unwind

Deconstruct an array field into one document per element.

```js
{ $unwind: { path: "$tags", preserveNullAndEmptyArrays: true } }
```

### $sort

Order documents. `1` ascending, `-1` descending.

```js
{ $sort: { rating: -1, createdAt: -1 } }
```

### $limit

```js
{ $limit: 10 }
```

### $skip

```js
{ $skip: 20 }
```

### $addFields

Add or overwrite fields without dropping existing ones.

```js
{
  $addFields: {
    fullName: { $concat: ["$firstName", " ", "$lastName"] },
    isPopular: { $gte: ["$views", 1000] }
  }
}
```

### $facet

Run multiple pipelines in parallel on the same input.

```js
{
  $facet: {
    metadata: [{ $count: "total" }],
    data: [{ $sort: { createdAt: -1 } }, { $skip: 0 }, { $limit: 10 }]
  }
}
```

### $bucket

Group documents into value-range buckets.

```js
{
  $bucket: {
    groupBy: "$prepTime",
    boundaries: [0, 15, 30, 60, 120, Infinity],
    default: "Other",
    output: { count: { $sum: 1 }, recipes: { $push: "$title" } }
  }
}
```

### $merge

Write pipeline output into an existing collection (upsert-capable).

```js
{
  $merge: {
    into: "monthlyStats",
    on: ["year", "month"],
    whenMatched: "merge",
    whenNotMatched: "insert"
  }
}
```

### $out

Replace an entire collection with pipeline output.

```js
{ $out: "cachedLeaderboard" }
```

---

## Accumulator Operators

Used inside `$group` (and `$setWindowFields`).

| Operator | Description | Example |
|-----------|-------------|---------|
| `$sum` | Sum numeric values or count | `{ $sum: "$price" }` / `{ $sum: 1 }` |
| `$avg` | Average | `{ $avg: "$rating" }` |
| `$first` | First value in group (order-dependent) | `{ $first: "$title" }` |
| `$last` | Last value in group | `{ $last: "$updatedAt" }` |
| `$push` | Collect all values into an array | `{ $push: "$tag" }` |
| `$addToSet` | Collect unique values into an array | `{ $addToSet: "$category" }` |
| `$min` | Minimum value | `{ $min: "$prepTime" }` |
| `$max` | Maximum value | `{ $max: "$rating" }` |

---

## Expression Operators

### $cond — if/then/else

```js
{
  $project: {
    difficulty: {
      $cond: {
        if: { $lte: ["$prepTime", 15] },
        then: "Easy",
        else: "Advanced"
      }
    }
  }
}
```

### $switch — multi-branch conditional

```js
{
  $project: {
    difficulty: {
      $switch: {
        branches: [
          { case: { $lte: ["$prepTime", 15] }, then: "Easy" },
          { case: { $lte: ["$prepTime", 45] }, then: "Medium" }
        ],
        default: "Hard"
      }
    }
  }
}
```

### $map — transform each array element

```js
{
  $project: {
    ingredientNames: {
      $map: {
        input: "$ingredients",
        as: "ing",
        in: "$$ing.name"
      }
    }
  }
}
```

### $filter — keep matching array elements

```js
{
  $project: {
    mainIngredients: {
      $filter: {
        input: "$ingredients",
        as: "ing",
        cond: { $eq: ["$$ing.isMain", true] }
      }
    }
  }
}
```

---

## Common Recipes

### Top N per Group

Get the top 3 recipes per category by rating:

```js
const topPerCategory = await Recipe.aggregate([
  { $sort: { rating: -1 } },
  {
    $group: {
      _id: "$category",
      recipes: { $push: { title: "$title", rating: "$rating" } }
    }
  },
  {
    $project: {
      category: "$_id",
      topRecipes: { $slice: ["$recipes", 3] }
    }
  }
]);
```

### Running Totals

Cumulative sign-ups per day:

```js
const runningTotals = await User.aggregate([
  {
    $group: {
      _id: { $dateToString: { format: "%Y-%m-%d", date: "$createdAt" } },
      dailyCount: { $sum: 1 }
    }
  },
  { $sort: { _id: 1 } },
  {
    $setWindowFields: {
      sortBy: { _id: 1 },
      output: {
        cumulativeUsers: {
          $sum: "$dailyCount",
          window: { documents: ["unbounded", "current"] }
        }
      }
    }
  }
]);
```

### Pivot (Rows to Columns)

Ratings distribution for a recipe:

```js
const pivot = await Comment.aggregate([
  { $match: { recipeId: targetId } },
  {
    $group: {
      _id: "$rating",
      count: { $sum: 1 }
    }
  },
  { $sort: { _id: 1 } },
  {
    $group: {
      _id: null,
      distribution: { $push: { k: { $toString: "$_id" }, v: "$count" } }
    }
  },
  { $replaceRoot: { newRoot: { $arrayToObject: "$distribution" } } }
]);
```

### Time-Series Bucketing

Recipe submissions grouped by month:

```js
const monthly = await Recipe.aggregate([
  {
    $group: {
      _id: {
        year: { $year: "$createdAt" },
        month: { $month: "$createdAt" }
      },
      count: { $sum: 1 },
      avgRating: { $avg: "$rating" }
    }
  },
  { $sort: { "_id.year": 1, "_id.month": 1 } },
  {
    $project: {
      _id: 0,
      period: {
        $concat: [
          { $toString: "$_id.year" }, "-",
          { $cond: [{ $lt: ["$_id.month", 10] }, { $concat: ["0", { $toString: "$_id.month" }] }, { $toString: "$_id.month" }] }
        ]
      },
      count: 1,
      avgRating: { $round: ["$avgRating", 1] }
    }
  }
]);
```

### Pagination with Total Count ($facet)

```js
async function paginateRecipes(filter, page = 1, limit = 12) {
  const skip = (page - 1) * limit;
  const [result] = await Recipe.aggregate([
    { $match: filter },
    {
      $facet: {
        metadata: [{ $count: "total" }],
        data: [
          { $sort: { createdAt: -1 } },
          { $skip: skip },
          { $limit: limit }
        ]
      }
    }
  ]);

  const total = result.metadata[0]?.total ?? 0;
  return {
    data: result.data,
    total,
    page,
    totalPages: Math.ceil(total / limit)
  };
}
```
