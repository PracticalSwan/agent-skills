#!/usr/bin/env node

/**
 * Seed a MongoDB database with sample users, recipes, and comments.
 *
 * Usage:
 *   node seed-database.js                  # seed with defaults (20 per collection)
 *   node seed-database.js --count 50       # seed 50 documents per collection
 *   node seed-database.js --clear          # drop collections before seeding
 *   node seed-database.js --clear --count 100
 *
 * Requires MONGODB_URI env var (e.g. mongodb://localhost:27017/kitchen_odyssey).
 * No external dependencies beyond the mongodb driver (or mongoose).
 */

const { MongoClient, ObjectId } = require("mongodb");

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const MONGODB_URI = process.env.MONGODB_URI;
if (!MONGODB_URI) {
  console.error("Error: MONGODB_URI environment variable is not set.");
  process.exit(1);
}

const args = process.argv.slice(2);
const shouldClear = args.includes("--clear");
const countFlagIdx = args.indexOf("--count");
const COUNT =
  countFlagIdx !== -1 && args[countFlagIdx + 1]
    ? Math.max(1, parseInt(args[countFlagIdx + 1], 10) || 20)
    : 20;

// ---------------------------------------------------------------------------
// Simple random-data generators (no external deps)
// ---------------------------------------------------------------------------

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function pickN(arr, n) {
  const shuffled = [...arr].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(n, arr.length));
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomDate(startYear = 2023, endYear = 2026) {
  const start = new Date(startYear, 0, 1).getTime();
  const end = new Date(endYear, 0, 1).getTime();
  return new Date(start + Math.random() * (end - start));
}

// Data pools
const FIRST_NAMES = [
  "Alice", "Bob", "Carmen", "David", "Elena", "Frank", "Grace", "Henry",
  "Iris", "Jack", "Karen", "Leo", "Mia", "Nathan", "Olivia", "Paul",
  "Quinn", "Rita", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier"
];

const LAST_NAMES = [
  "Smith", "Johnson", "Lee", "Brown", "Garcia", "Kim", "Patel", "Chen",
  "Williams", "Lopez", "Nguyen", "Anderson", "Tanaka", "Muller", "Costa"
];

const CATEGORIES = [
  "Italian", "Mexican", "Thai", "Japanese", "Indian",
  "French", "Chinese", "American", "Mediterranean", "Korean"
];

const TAGS = [
  "vegetarian", "vegan", "gluten-free", "quick", "comfort-food",
  "healthy", "spicy", "dessert", "breakfast", "one-pot",
  "grilled", "baked", "soup", "salad", "seafood"
];

const RECIPE_ADJECTIVES = [
  "Classic", "Spicy", "Creamy", "Zesty", "Smoky",
  "Rustic", "Fresh", "Crispy", "Savory", "Tangy"
];

const RECIPE_NOUNS = [
  "Pasta", "Tacos", "Curry", "Stir-Fry", "Soup",
  "Salad", "Risotto", "Bowl", "Stew", "Sandwich",
  "Noodles", "Dumplings", "Pizza", "Burrito", "Casserole"
];

const INGREDIENTS = [
  "chicken breast", "olive oil", "garlic cloves", "onion", "tomatoes",
  "salt", "black pepper", "basil", "rice", "soy sauce",
  "ginger", "lemon juice", "bell pepper", "mushrooms", "spinach",
  "cheese", "butter", "flour", "eggs", "cream",
  "cilantro", "chili flakes", "coconut milk", "potatoes", "carrots"
];

const UNITS = ["g", "ml", "cups", "tbsp", "tsp", "pieces", "cloves", "slices"];

const COMMENT_TEXTS = [
  "Loved this recipe! Will make again.",
  "Turned out great, though I added extra garlic.",
  "Easy to follow instructions. Delicious result.",
  "My family really enjoyed this one.",
  "Good but could use a bit more seasoning.",
  "Perfect weeknight dinner recipe.",
  "The leftovers were even better the next day!",
  "I substituted tofu and it worked well.",
  "Restaurant quality. Highly recommend.",
  "Simple ingredients, amazing flavor.",
  "A new household favorite!",
  "Took longer than expected but worth the wait."
];

// ---------------------------------------------------------------------------
// Document generators
// ---------------------------------------------------------------------------

function generateUser(index) {
  const first = pick(FIRST_NAMES);
  const last = pick(LAST_NAMES);
  const suffix = index.toString().padStart(3, "0");
  return {
    _id: new ObjectId(),
    username: `${first.toLowerCase()}${last.toLowerCase()}${suffix}`,
    email: `${first.toLowerCase()}.${last.toLowerCase()}${suffix}@example.com`,
    displayName: `${first} ${last}`,
    role: index === 0 ? "admin" : pick(["user", "user", "user", "admin"]),
    avatar: `https://api.dicebear.com/7.x/initials/svg?seed=${first}${last}`,
    bio: `Hi, I'm ${first}. I love cooking ${pick(CATEGORIES)} food!`,
    createdAt: randomDate(2023, 2025),
    updatedAt: randomDate(2025, 2026)
  };
}

function generateRecipe(index, userIds) {
  const ingredientCount = randomInt(4, 10);
  const ingredients = pickN(INGREDIENTS, ingredientCount).map((name) => ({
    name,
    quantity: randomInt(1, 500),
    unit: pick(UNITS)
  }));

  const stepCount = randomInt(3, 8);
  const steps = Array.from({ length: stepCount }, (_, i) => ({
    order: i + 1,
    instruction: `Step ${i + 1}: ${pick(["Prepare", "Cook", "Mix", "Heat", "Combine", "Season", "Serve", "Let rest"])} the ${pick(INGREDIENTS)} ${pick(["until golden", "for 5 minutes", "thoroughly", "on medium heat", "until tender"])}.`
  }));

  return {
    _id: new ObjectId(),
    title: `${pick(RECIPE_ADJECTIVES)} ${pick(RECIPE_NOUNS)}`,
    slug: `recipe-${index.toString().padStart(4, "0")}`,
    description: `A delicious ${pick(CATEGORIES).toLowerCase()} dish that's perfect for ${pick(["weeknight dinners", "special occasions", "meal prep", "family gatherings"])}.`,
    category: pick(CATEGORIES),
    tags: pickN(TAGS, randomInt(1, 4)),
    ingredients,
    steps,
    prepTime: randomInt(5, 30),
    cookTime: randomInt(10, 90),
    servings: randomInt(1, 8),
    difficulty: pick(["Easy", "Medium", "Hard"]),
    rating: Math.round((randomInt(25, 50) / 10) * 10) / 10,
    views: randomInt(0, 5000),
    authorId: pick(userIds),
    status: pick(["published", "published", "published", "draft"]),
    createdAt: randomDate(2024, 2026),
    updatedAt: randomDate(2025, 2026)
  };
}

function generateComment(userIds, recipeIds) {
  return {
    _id: new ObjectId(),
    recipeId: pick(recipeIds),
    authorId: pick(userIds),
    text: pick(COMMENT_TEXTS),
    rating: randomInt(1, 5),
    createdAt: randomDate(2024, 2026)
  };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  let client;
  try {
    console.log(`Connecting to MongoDB...`);
    client = new MongoClient(MONGODB_URI);
    await client.connect();

    const db = client.db();
    console.log(`Database: ${db.databaseName}`);

    if (shouldClear) {
      console.log("Clearing existing data...");
      await Promise.all([
        db.collection("users").deleteMany({}),
        db.collection("recipes").deleteMany({}),
        db.collection("comments").deleteMany({})
      ]);
      console.log("Collections cleared.");
    }

    // Generate users
    console.log(`Generating ${COUNT} users...`);
    const users = Array.from({ length: COUNT }, (_, i) => generateUser(i));
    await db.collection("users").insertMany(users);
    const userIds = users.map((u) => u._id);

    // Generate recipes
    console.log(`Generating ${COUNT} recipes...`);
    const recipes = Array.from({ length: COUNT }, (_, i) =>
      generateRecipe(i, userIds)
    );
    await db.collection("recipes").insertMany(recipes);
    const recipeIds = recipes.map((r) => r._id);

    // Generate comments (2-3x recipe count)
    const commentCount = COUNT * randomInt(2, 3);
    console.log(`Generating ${commentCount} comments...`);
    const comments = Array.from({ length: commentCount }, () =>
      generateComment(userIds, recipeIds)
    );
    await db.collection("comments").insertMany(comments);

    console.log("\nSeed complete:");
    console.log(`  Users:    ${users.length}`);
    console.log(`  Recipes:  ${recipes.length}`);
    console.log(`  Comments: ${comments.length}`);
  } catch (err) {
    console.error("Seed failed:", err.message);
    process.exit(1);
  } finally {
    if (client) await client.close();
  }
}

main();
