/*
Task 2.2: MongoDB Implementation 

*/

const DB_NAME = "fleximart_nosql";
const COLLECTION = "products";

// Use a dedicated database for this task
const dbRef = db.getSiblingDB(DB_NAME);
const productsCol = dbRef.getCollection(COLLECTION);

// ------------------------------------------------------------
// Operation 1: Load Data (1 mark)
// Import the provided JSON file into collection 'products'
// ------------------------------------------------------------

print("\n==============================");
print("Operation 1: Load Data");
print("==============================");

try {
  productsCol.drop(); // Clear collection for repeatable runs
} catch (e) {
  // Ignore if collection doesn't exist
}

const fs = require("fs");
const path = require("path");


const jsonPath = path.join(process.cwd(), "data", "products_catalog.json");

if (!fs.existsSync(jsonPath)) {
  throw new Error("products_catalog.json not found in data folder at: " + jsonPath);
}

const rawText = fs.readFileSync(jsonPath, "utf-8");
const docs = JSON.parse(rawText);

if (!Array.isArray(docs)) {
  throw new Error("products_catalog.json must be a JSON array of products.");
}

productsCol.insertMany(docs);

// In mongosh, insertMany() return object fields can vary by version.
// So we report both attempted and actual count in collection.
print("Documents in JSON array: " + docs.length);
print("Documents now in collection: " + productsCol.countDocuments({}));

// ------------------------------------------------------------
// Operation 2: Basic Query (2 marks)
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock
// ------------------------------------------------------------

print("\n==============================");
print("Operation 2: Basic Query");
print("==============================");

const op2Cursor = productsCol.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { _id: 0, name: 1, price: 1, stock: 1 }
);

print("Electronics products with price < 50000 (name, price, stock):");
printjson(op2Cursor.toArray());

// ------------------------------------------------------------
// Operation 3: Review Analysis (2 marks)
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array
// ------------------------------------------------------------

print("\n==============================");
print("Operation 3: Review Analysis (avg rating >= 4.0)");
print("==============================");

const op3Pipeline = [
  // Keep only products that actually have reviews
  { $match: { reviews: { $exists: true, $type: "array", $ne: [] } } },

  // Flatten reviews array
  { $unwind: "$reviews" },

  // Group per product and compute average rating
  {
    $group: {
      _id: "$product_id",
      name: { $first: "$name" },
      category: { $first: "$category" },
      avg_rating: { $avg: "$reviews.rating" },
      review_count: { $sum: 1 }
    }
  },

  // Filter avg rating >= 4.0
  { $match: { avg_rating: { $gte: 4.0 } } },

  // Format output
  {
    $project: {
      _id: 0,
      product_id: "$_id",
      name: 1,
      category: 1,
      avg_rating: { $round: ["$avg_rating", 2] },
      review_count: 1
    }
  },

  { $sort: { avg_rating: -1, review_count: -1 } }
];

print("Products with avg_rating >= 4.0:");
printjson(productsCol.aggregate(op3Pipeline).toArray());

// ------------------------------------------------------------
// Operation 4: Update Operation (2 marks)
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
// (We keep review structure consistent with existing data: user_id + username)
// ------------------------------------------------------------

print("\n==============================");
print("Operation 4: Update Operation (push new review to ELEC001)");
print("==============================");

const newReview = {
  user_id: "U999",
  username: "ValueBuyer",
  rating: 4,
  comment: "Good value",
  date: new Date() // ISODate() equivalent
};

const op4Result = productsCol.updateOne(
  { product_id: "ELEC001" },
  { $push: { reviews: newReview } }
);

print("Matched count: " + op4Result.matchedCount);
print("Modified count: " + op4Result.modifiedCount);

print("Updated ELEC001 (showing reviews array):");
printjson(
  productsCol.findOne(
    { product_id: "ELEC001" },
    { _id: 0, product_id: 1, name: 1, reviews: 1 }
  )
);

// ------------------------------------------------------------
// Operation 5: Complex Aggregation (3 marks)
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending
// ------------------------------------------------------------

print("\n==============================");
print("Operation 5: Complex Aggregation (avg price by category)");
print("==============================");

const op5Pipeline = [
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: { $round: ["$avg_price", 2] },
      product_count: 1
    }
  },
  { $sort: { avg_price: -1 } }
];

print("Average price by category:");
printjson(productsCol.aggregate(op5Pipeline).toArray());

// Done
print("\nAll MongoDB operations completed.\n");
