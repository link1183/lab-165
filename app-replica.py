from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Replica Set Configuration
REPLICA_SET_NAME = os.environ.get("REPLICA_SET_NAME", "rs0")
MONGO_DB = os.environ.get("MONGO_DB", "my_data")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "open_data")

# Replica set members (can be configured via environment)
REPLICA_MEMBERS = os.environ.get(
    "REPLICA_MEMBERS", "localhost:27017,localhost:27018,localhost:27019"
).split(",")

# Authentication
MONGO_USERNAME = os.environ.get("MONGO_USERNAME", "admin")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "AdminPassword123!")
MONGO_AUTH_DB = os.environ.get("MONGO_AUTH_DB", "admin")

# Connect to MongoDB Replica Set
try:
    # Use string format for read preference instead of enum
    client = MongoClient(
        REPLICA_MEMBERS,
        replicaSet=REPLICA_SET_NAME,
        username=MONGO_USERNAME,
        password=MONGO_PASSWORD,
        authSource=MONGO_AUTH_DB,
        readPreference="primary",  # Using primary for initial stability
        serverSelectionTimeoutMS=10000,  # 10 second timeout
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
    )

    # Test connection
    client.admin.command("ping")
    print("Successfully connected to MongoDB Replica Set!")

except Exception as e:
    print(f"Failed to connect to MongoDB Replica Set: {e}")
    print("Make sure the replica set is properly configured and running")
    exit(1)

# Select database and collection
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


@app.route("/")
def index():
    """Display a random document from the collection"""
    try:
        # Get replica set status for display
        rs_status = client.admin.command("replSetGetStatus")
        primary_host = None
        secondary_hosts = []

        for member in rs_status["members"]:
            if member["stateStr"] == "PRIMARY":
                primary_host = member["name"]
            elif member["stateStr"] == "SECONDARY":
                secondary_hosts.append(member["name"])

        # Get total count of documents
        total_docs = collection.estimated_document_count()

        if total_docs == 0:
            return render_template(
                "index.html",
                data=None,
                error="No documents found in collection",
                replica_info={
                    "primary": primary_host,
                    "secondaries": secondary_hosts,
                    "set_name": REPLICA_SET_NAME,
                },
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

            return render_template(
                "index.html",
                data=document,
                doc_count=total_docs,
                replica_info={
                    "primary": primary_host,
                    "secondaries": secondary_hosts,
                    "set_name": REPLICA_SET_NAME,
                },
            )
        else:
            return render_template(
                "index.html",
                data=None,
                error="Could not retrieve document",
                replica_info={
                    "primary": primary_host,
                    "secondaries": secondary_hosts,
                    "set_name": REPLICA_SET_NAME,
                },
            )

    except Exception as e:
        print(f"Error retrieving document: {e}")
        return render_template(
            "index.html",
            data=None,
            error=f"Database error: {str(e)}",
            replica_info=None,
        )


@app.route("/replica-status")
def replica_status():
    """Get detailed replica set status"""
    try:
        rs_status = client.admin.command("replSetGetStatus")
        return jsonify(
            {
                "status": "healthy",
                "replica_set": REPLICA_SET_NAME,
                "members": [
                    {
                        "name": member["name"],
                        "state": member["stateStr"],
                        "health": member["health"],
                        "uptime": member.get("uptime", 0),
                        "last_heartbeat": member.get("lastHeartbeat"),
                        "ping_ms": member.get("pingMs"),
                    }
                    for member in rs_status["members"]
                ],
                "set_version": rs_status.get("set", "unknown"),
                "date": rs_status.get("date"),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/health")
def health():
    """Health check endpoint for replica set"""
    try:
        # Test database connection
        client.admin.command("ping")
        doc_count = collection.estimated_document_count()

        # Get read preference info
        read_pref = str(client.read_preference)

        # Check replica set status
        rs_status = client.admin.command("replSetGetStatus")
        primary_count = sum(
            1 for member in rs_status["members"] if member["stateStr"] == "PRIMARY"
        )
        secondary_count = sum(
            1 for member in rs_status["members"] if member["stateStr"] == "SECONDARY"
        )

        return jsonify(
            {
                "status": "healthy",
                "database": MONGO_DB,
                "collection": MONGO_COLLECTION,
                "document_count": doc_count,
                "replica_set": REPLICA_SET_NAME,
                "read_preference": read_pref,
                "primary_count": primary_count,
                "secondary_count": secondary_count,
                "total_members": len(rs_status["members"]),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Replica Set Application...")
    print(f"Replica Set: {REPLICA_SET_NAME}")
    print(f"Members: {', '.join(REPLICA_MEMBERS)}")
    print(f"Database: {MONGO_DB}")
    print(f"Collection: {MONGO_COLLECTION}")
    print(f"Authentication: {MONGO_USERNAME}@{MONGO_AUTH_DB}")
    print("Read Preference: primary")

    app.run(debug=True, host="0.0.0.0", port=5000)
