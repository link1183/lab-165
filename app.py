from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Configuration
MONGO_URI = os.environ.get("MONGO_URI", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", "27017"))
MONGO_DB = os.environ.get("MONGO_DB", "my_data")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "open_data")

# Optional authentication
MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_AUTH_DB = os.environ.get("MONGO_AUTH_DB", "admin")

# Connect to MongoDB
try:
    if MONGO_USERNAME and MONGO_PASSWORD:
        # Connect with authentication
        client = MongoClient(
            MONGO_URI,
            MONGO_PORT,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            authSource=MONGO_AUTH_DB,
        )
        print(f"Connecting to MongoDB with authentication as {MONGO_USERNAME}")
    else:
        # Connect without authentication
        client = MongoClient(MONGO_URI, MONGO_PORT)
        print("Connecting to MongoDB without authentication")

    # Test connection
    client.admin.command("ping")
    print("Successfully connected to MongoDB!")

except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    exit(1)

# Select database and collection
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


@app.route("/")
def index():
    """Display a random document from the collection"""
    try:
        # Get total count of documents
        total_docs = collection.estimated_document_count()

        if total_docs == 0:
            return render_template(
                "index.html", data=None, error="No documents found in collection"
            )

        # Retrieve one random document using aggregation with $sample
        random_doc = collection.aggregate([{"$sample": {"size": 1}}])
        document = next(random_doc, None)

        if document:
            # Convert ObjectId to string for display
            if "_id" in document:
                document["_id"] = str(document["_id"])

            # Format experience for better readability
            if "experience" in document:
                document["experience_formatted"] = f"{int(document['experience']):,}"

            return render_template("index.html", data=document, doc_count=total_docs)
        else:
            return render_template(
                "index.html", data=None, error="Could not retrieve document"
            )

    except Exception as e:
        print(f"Error retrieving document: {e}")
        return render_template(
            "index.html", data=None, error=f"Database error: {str(e)}"
        )


@app.route("/health")
def health():
    """Health check endpoint"""
    try:
        # Test database connection
        client.admin.command("ping")
        doc_count = collection.estimated_document_count()

        # Get some basic stats
        necromancer_count = collection.count_documents({"class": "Necromancer"})
        level_100_count = collection.count_documents({"level": 100})

        return jsonify(
            {
                "status": "healthy",
                "database": MONGO_DB,
                "collection": MONGO_COLLECTION,
                "total_documents": doc_count,
                "necromancer_players": necromancer_count,
                "level_100_players": level_100_count,
                "authentication": "enabled" if MONGO_USERNAME else "disabled",
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/api/stats")
def api_stats():
    """API endpoint for collection statistics"""
    try:
        # Aggregate statistics
        pipeline = [
            {
                "$group": {
                    "_id": "$class",
                    "count": {"$sum": 1},
                    "avg_level": {"$avg": "$level"},
                    "max_experience": {"$max": "$experience"},
                }
            },
            {"$sort": {"count": -1}},
        ]

        class_stats = list(collection.aggregate(pipeline))

        # Count by ladder
        ladder_pipeline = [
            {"$group": {"_id": "$ladder", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]

        ladder_stats = list(collection.aggregate(ladder_pipeline))

        return jsonify(
            {
                "class_distribution": class_stats,
                "ladder_distribution": ladder_stats,
                "total_documents": collection.estimated_document_count(),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting application...")
    print(f"MongoDB URI: {MONGO_URI}:{MONGO_PORT}")
    print(f"Database: {MONGO_DB}")
    print(f"Collection: {MONGO_COLLECTION}")
    print(f"Authentication: {'Enabled' if MONGO_USERNAME else 'Disabled'}")

    app.run(debug=True, host="0.0.0.0", port=5000)
