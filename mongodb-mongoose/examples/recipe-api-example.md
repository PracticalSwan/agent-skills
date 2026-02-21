# Recipe CRUD API — Mongoose + Next.js API Routes

Complete example: schema with validation, repository with pagination/search, API route handlers, connection utility, and aggregation for statistics.

---

## 1. Connection Utility

`lib/mongodb.js`

```js
import mongoose from "mongoose";

const MONGODB_URI = process.env.MONGODB_URI;

if (!MONGODB_URI) {
  throw new Error("MONGODB_URI environment variable is not defined");
}

let cached = global.__mongooseCache;
if (!cached) {
  cached = global.__mongooseCache = { conn: null, promise: null };
}

export async function connectDB() {
  if (cached.conn) return cached.conn;

  if (!cached.promise) {
    cached.promise = mongoose
      .connect(MONGODB_URI, { bufferCommands: false })
      .then((m) => m);
  }

  cached.conn = await cached.promise;
  return cached.conn;
}
```

---

## 2. Recipe Schema

`models/Recipe.js`

```js
import mongoose from "mongoose";

const ingredientSchema = new mongoose.Schema(
  {
    name: { type: String, required: true, trim: true },
    quantity: { type: Number, required: true, min: 0 },
    unit: { type: String, required: true, trim: true }
  },
  { _id: false }
);

const stepSchema = new mongoose.Schema(
  {
    order: { type: Number, required: true },
    instruction: { type: String, required: true, trim: true }
  },
  { _id: false }
);

const recipeSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, "Title is required"],
      trim: true,
      maxlength: [200, "Title cannot exceed 200 characters"]
    },
    slug: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true
    },
    description: { type: String, trim: true, maxlength: 2000 },
    category: {
      type: String,
      required: true,
      enum: [
        "Italian", "Mexican", "Thai", "Japanese", "Indian",
        "French", "Chinese", "American", "Mediterranean", "Korean", "Other"
      ]
    },
    tags: [{ type: String, trim: true, lowercase: true }],
    ingredients: {
      type: [ingredientSchema],
      validate: [
        (val) => val.length >= 1,
        "At least one ingredient is required"
      ]
    },
    steps: {
      type: [stepSchema],
      validate: [(val) => val.length >= 1, "At least one step is required"]
    },
    prepTime: { type: Number, min: 0 },
    cookTime: { type: Number, min: 0 },
    servings: { type: Number, min: 1, default: 4 },
    difficulty: {
      type: String,
      enum: ["Easy", "Medium", "Hard"],
      default: "Medium"
    },
    rating: { type: Number, min: 0, max: 5, default: 0 },
    views: { type: Number, default: 0 },
    authorId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true
    },
    status: {
      type: String,
      enum: ["draft", "published", "archived"],
      default: "draft"
    }
  },
  { timestamps: true }
);

// ---------- Indexes (ESR order) ----------
recipeSchema.index({ status: 1, category: 1, rating: -1 });
recipeSchema.index({ authorId: 1, createdAt: -1 });
recipeSchema.index({ tags: 1 });
recipeSchema.index(
  { title: "text", description: "text", "ingredients.name": "text" },
  { weights: { title: 10, description: 5, "ingredients.name": 2 } }
);

// ---------- Middleware ----------
recipeSchema.pre("save", function (next) {
  if (this.isModified("title") && !this.isModified("slug")) {
    this.slug = this.title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");
  }
  next();
});

// Virtual: total time
recipeSchema.virtual("totalTime").get(function () {
  return (this.prepTime || 0) + (this.cookTime || 0);
});

recipeSchema.set("toJSON", { virtuals: true });

export default mongoose.models.Recipe ||
  mongoose.model("Recipe", recipeSchema);
```

---

## 3. Recipe Repository

`repositories/RecipeRepository.js`

```js
import Recipe from "@/models/Recipe";

export class RecipeRepository {
  async findById(id) {
    return Recipe.findById(id).populate("authorId", "displayName avatar").lean();
  }

  async findBySlug(slug) {
    return Recipe.findOne({ slug })
      .populate("authorId", "displayName avatar")
      .lean();
  }

  async search({ query, category, tags, difficulty, page = 1, limit = 12 }) {
    const filter = { status: "published" };

    if (query) {
      filter.$text = { $search: query };
    }
    if (category) {
      filter.category = category;
    }
    if (tags?.length) {
      filter.tags = { $in: tags };
    }
    if (difficulty) {
      filter.difficulty = difficulty;
    }

    const skip = (page - 1) * limit;

    const [recipes, total] = await Promise.all([
      Recipe.find(filter)
        .sort(query ? { score: { $meta: "textScore" } } : { createdAt: -1 })
        .skip(skip)
        .limit(limit)
        .populate("authorId", "displayName avatar")
        .lean(),
      Recipe.countDocuments(filter)
    ]);

    return {
      data: recipes,
      total,
      page,
      totalPages: Math.ceil(total / limit)
    };
  }

  async create(data) {
    const recipe = new Recipe(data);
    await recipe.save();
    return recipe.toJSON();
  }

  async update(id, data) {
    return Recipe.findByIdAndUpdate(id, data, {
      new: true,
      runValidators: true
    }).lean();
  }

  async delete(id) {
    return Recipe.findByIdAndDelete(id).lean();
  }

  async incrementViews(id) {
    return Recipe.findByIdAndUpdate(id, { $inc: { views: 1 } });
  }

  async findByAuthor(authorId, { page = 1, limit = 12 } = {}) {
    const skip = (page - 1) * limit;
    const filter = { authorId };

    const [recipes, total] = await Promise.all([
      Recipe.find(filter)
        .sort({ createdAt: -1 })
        .skip(skip)
        .limit(limit)
        .lean(),
      Recipe.countDocuments(filter)
    ]);

    return { data: recipes, total, page, totalPages: Math.ceil(total / limit) };
  }

  // ---------- Aggregations ----------

  async getStatistics() {
    const [result] = await Recipe.aggregate([
      {
        $facet: {
          overview: [
            {
              $group: {
                _id: null,
                totalRecipes: { $sum: 1 },
                published: {
                  $sum: { $cond: [{ $eq: ["$status", "published"] }, 1, 0] }
                },
                avgRating: { $avg: "$rating" },
                totalViews: { $sum: "$views" }
              }
            }
          ],
          byCategory: [
            {
              $group: {
                _id: "$category",
                count: { $sum: 1 },
                avgRating: { $avg: "$rating" }
              }
            },
            { $sort: { count: -1 } }
          ],
          byDifficulty: [
            { $group: { _id: "$difficulty", count: { $sum: 1 } } },
            { $sort: { count: -1 } }
          ],
          topRated: [
            { $match: { status: "published" } },
            { $sort: { rating: -1 } },
            { $limit: 5 },
            { $project: { title: 1, rating: 1, category: 1, slug: 1 } }
          ],
          monthlyTrend: [
            {
              $group: {
                _id: {
                  year: { $year: "$createdAt" },
                  month: { $month: "$createdAt" }
                },
                count: { $sum: 1 }
              }
            },
            { $sort: { "_id.year": 1, "_id.month": 1 } },
            { $limit: 12 }
          ]
        }
      }
    ]);

    return {
      overview: result.overview[0] ?? {},
      byCategory: result.byCategory,
      byDifficulty: result.byDifficulty,
      topRated: result.topRated,
      monthlyTrend: result.monthlyTrend
    };
  }
}

export const recipeRepository = new RecipeRepository();
```

---

## 4. API Route Handlers

### List / Create — `app/api/recipes/route.js`

```js
import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import { recipeRepository } from "@/repositories/RecipeRepository";

export async function GET(request) {
  try {
    await connectDB();

    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get("page") || "1", 10);
    const limit = Math.min(parseInt(searchParams.get("limit") || "12", 10), 50);
    const query = searchParams.get("q") || undefined;
    const category = searchParams.get("category") || undefined;
    const difficulty = searchParams.get("difficulty") || undefined;
    const tags = searchParams.get("tags")?.split(",").filter(Boolean);

    const result = await recipeRepository.search({
      query, category, tags, difficulty, page, limit
    });

    return NextResponse.json(result);
  } catch (err) {
    console.error("GET /api/recipes error:", err);
    return NextResponse.json(
      { error: "Failed to fetch recipes" },
      { status: 500 }
    );
  }
}

export async function POST(request) {
  try {
    await connectDB();

    const body = await request.json();
    const recipe = await recipeRepository.create(body);

    return NextResponse.json(recipe, { status: 201 });
  } catch (err) {
    if (err.name === "ValidationError") {
      const errors = Object.values(err.errors).map((e) => e.message);
      return NextResponse.json({ error: "Validation failed", errors }, { status: 400 });
    }
    if (err.code === 11000) {
      return NextResponse.json(
        { error: "A recipe with this slug already exists" },
        { status: 409 }
      );
    }
    console.error("POST /api/recipes error:", err);
    return NextResponse.json(
      { error: "Failed to create recipe" },
      { status: 500 }
    );
  }
}
```

### Get / Update / Delete — `app/api/recipes/[id]/route.js`

```js
import { NextResponse } from "next/server";
import mongoose from "mongoose";
import { connectDB } from "@/lib/mongodb";
import { recipeRepository } from "@/repositories/RecipeRepository";

function isValidObjectId(id) {
  return mongoose.Types.ObjectId.isValid(id);
}

export async function GET(request, { params }) {
  try {
    await connectDB();

    const { id } = await params;
    if (!isValidObjectId(id)) {
      return NextResponse.json({ error: "Invalid recipe ID" }, { status: 400 });
    }

    const recipe = await recipeRepository.findById(id);
    if (!recipe) {
      return NextResponse.json({ error: "Recipe not found" }, { status: 404 });
    }

    await recipeRepository.incrementViews(id);
    return NextResponse.json(recipe);
  } catch (err) {
    console.error("GET /api/recipes/[id] error:", err);
    return NextResponse.json(
      { error: "Failed to fetch recipe" },
      { status: 500 }
    );
  }
}

export async function PUT(request, { params }) {
  try {
    await connectDB();

    const { id } = await params;
    if (!isValidObjectId(id)) {
      return NextResponse.json({ error: "Invalid recipe ID" }, { status: 400 });
    }

    const body = await request.json();
    const recipe = await recipeRepository.update(id, body);
    if (!recipe) {
      return NextResponse.json({ error: "Recipe not found" }, { status: 404 });
    }

    return NextResponse.json(recipe);
  } catch (err) {
    if (err.name === "ValidationError") {
      const errors = Object.values(err.errors).map((e) => e.message);
      return NextResponse.json({ error: "Validation failed", errors }, { status: 400 });
    }
    console.error("PUT /api/recipes/[id] error:", err);
    return NextResponse.json(
      { error: "Failed to update recipe" },
      { status: 500 }
    );
  }
}

export async function DELETE(request, { params }) {
  try {
    await connectDB();

    const { id } = await params;
    if (!isValidObjectId(id)) {
      return NextResponse.json({ error: "Invalid recipe ID" }, { status: 400 });
    }

    const recipe = await recipeRepository.delete(id);
    if (!recipe) {
      return NextResponse.json({ error: "Recipe not found" }, { status: 404 });
    }

    return NextResponse.json({ message: "Recipe deleted" });
  } catch (err) {
    console.error("DELETE /api/recipes/[id] error:", err);
    return NextResponse.json(
      { error: "Failed to delete recipe" },
      { status: 500 }
    );
  }
}
```

### Statistics — `app/api/recipes/stats/route.js`

```js
import { NextResponse } from "next/server";
import { connectDB } from "@/lib/mongodb";
import { recipeRepository } from "@/repositories/RecipeRepository";

export async function GET() {
  try {
    await connectDB();
    const stats = await recipeRepository.getStatistics();
    return NextResponse.json(stats);
  } catch (err) {
    console.error("GET /api/recipes/stats error:", err);
    return NextResponse.json(
      { error: "Failed to fetch statistics" },
      { status: 500 }
    );
  }
}
```

---

## 5. Usage Examples

### Fetch recipes with search and pagination

```js
const res = await fetch("/api/recipes?q=pasta&category=Italian&page=1&limit=10");
const { data, total, page, totalPages } = await res.json();
```

### Create a recipe

```js
const res = await fetch("/api/recipes", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    title: "Spicy Thai Basil Stir-Fry",
    description: "A quick and flavorful Thai stir-fry.",
    category: "Thai",
    tags: ["spicy", "quick"],
    ingredients: [
      { name: "chicken breast", quantity: 300, unit: "g" },
      { name: "Thai basil", quantity: 1, unit: "cups" },
      { name: "chili flakes", quantity: 1, unit: "tsp" }
    ],
    steps: [
      { order: 1, instruction: "Slice the chicken into thin strips." },
      { order: 2, instruction: "Stir-fry on high heat with garlic and chili." },
      { order: 3, instruction: "Add basil leaves and serve over rice." }
    ],
    prepTime: 10,
    cookTime: 15,
    servings: 2,
    difficulty: "Easy",
    authorId: "665a1b2c3d4e5f6a7b8c9d0e",
    status: "published"
  })
});
```

### Get statistics dashboard

```js
const res = await fetch("/api/recipes/stats");
const { overview, byCategory, byDifficulty, topRated, monthlyTrend } =
  await res.json();

console.log(`Total recipes: ${overview.totalRecipes}`);
console.log(`Average rating: ${overview.avgRating.toFixed(1)}`);
console.log(`Top category: ${byCategory[0]._id} (${byCategory[0].count})`);
```
