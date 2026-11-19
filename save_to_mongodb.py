#!/usr/bin/env python
"""
Jeevadhaara - MongoDB Atlas Data Exporter & Synchronizer
Exports all donor and system records from SQLite database to MongoDB Atlas cluster.

Usage:
  python save_to_mongodb.py --password YOUR_ATLAS_PASSWORD
  python save_to_mongodb.py --uri "mongodb+srv://krishnaadithyan599_db_user:<password>@jeevadhaara.tzdqdn0.mongodb.net/"
  python save_to_mongodb.py  (will prompt interactively for password if not in .env)
"""

import os
import sys
import argparse
import getpass
import urllib.parse
from datetime import datetime
from pathlib import Path

# Load .env if present
try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

try:
    from pymongo import MongoClient, UpdateOne
    from pymongo.errors import ConnectionFailure, OperationFailure, ConfigurationError
except ImportError:
    print("ERROR: 'pymongo' is not installed.")
    print("Please install it with: pip install pymongo dnspython")
    sys.exit(1)

# Default cluster details provided by user
DEFAULT_BASE_URI = "mongodb+srv://krishnaadithyan599_db_user:<db_password>@jeevadhaara.tzdqdn0.mongodb.net/?retryWrites=true&w=majority&appName=jeevadhaara"
DEFAULT_DB_NAME = "jeevadhaara"


def get_sqlite_donors(db_path):
    """Reads all donors directly from the SQLite database."""
    import sqlite3
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"SQLite database not found at: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, full_name, email, phone, age, gender, blood_group, city, address, is_available, created_at
        FROM donors_donor
        ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    donors = []
    for r in rows:
        d = dict(r)
        d['is_available'] = bool(d['is_available'])
        donors.append(d)
    conn.close()
    return donors


def get_sqlite_users(db_path):
    """Reads non-sensitive user metadata from SQLite."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_staff, is_superuser, date_joined FROM auth_user")
    rows = cursor.fetchall()
    users = [dict(r) for r in rows]
    conn.close()
    return users


def build_mongo_uri(raw_uri, password=None):
    """Replaces <db_password> placeholder with properly URL-encoded password."""
    uri = raw_uri or os.environ.get("MONGODB_URI") or DEFAULT_BASE_URI

    if "<db_password>" in uri:
        if not password:
            password = os.environ.get("MONGODB_PASSWORD")
        if not password:
            print("\nMongoDB Atlas connection string requires your database user password.")
            print("User: krishnaadithyan599_db_user | Cluster: jeevadhaara.tzdqdn0.mongodb.net")
            password = getpass.getpass("Enter MongoDB Atlas Password: ").strip()

        if not password:
            raise ValueError("Password cannot be empty.")

        # URL-encode special characters like @, :, /, #, %
        encoded_password = urllib.parse.quote_plus(password)
        uri = uri.replace("<db_password>", encoded_password)

    return uri


def sync_to_mongodb(mongo_uri, db_name=DEFAULT_DB_NAME, sqlite_path="db.sqlite3"):
    """Connects to MongoDB Atlas and upserts all donors and summary metadata."""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Connecting to MongoDB Atlas cluster...")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=8000)
        # Verify connection
        client.admin.command('ping')
        print("[SUCCESS] Successfully authenticated and connected to MongoDB Atlas!")
    except ConfigurationError as ce:
        print(f"[CONFIG ERROR] Invalid connection string or DNS resolution issue: {ce}")
        return False
    except OperationFailure as of:
        print(f"[AUTH ERROR] Authentication failed. Please verify your MongoDB password: {of}")
        return False
    except ConnectionFailure as cf:
        print(f"[CONNECTION ERROR] Could not reach cluster. Check your internet or Atlas IP whitelist: {cf}")
        print("  Tip: Ensure your current IP is whitelisted in MongoDB Atlas (Network Access -> Add IP Address -> Allow from Anywhere).")
        return False
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False

    db = client[db_name]
    donors_collection = db["donors"]
    metadata_collection = db["system_metadata"]

    # 1. Read SQLite data
    print(f"\nReading data from local SQLite database: {sqlite_path}...")
    donors = get_sqlite_donors(sqlite_path)
    print(f"Found {len(donors)} donor records in SQLite.")

    # 2. Upsert donors into MongoDB
    if donors:
        print(f"Upserting {len(donors)} donors into MongoDB collection '{db_name}.donors'...")
        operations = []
        for d in donors:
            # Match by id or email
            filter_query = {"$or": [{"sqlite_id": d["id"]}, {"email": d["email"]}]}
            doc = {
                "sqlite_id": d["id"],
                "full_name": d["full_name"],
                "email": d["email"],
                "phone": d["phone"],
                "age": d["age"],
                "gender": d["gender"],
                "blood_group": d["blood_group"],
                "city": d["city"],
                "address": d["address"],
                "is_available": d["is_available"],
                "created_at": d["created_at"],
                "synced_at": datetime.utcnow().isoformat(),
            }
            operations.append(UpdateOne(filter_query, {"$set": doc}, upsert=True))

        result = donors_collection.bulk_write(operations)
        print(f"[SUCCESS] Donors Collection Updated:")
        print(f"  - Matched: {result.matched_count}")
        print(f"  - Modified: {result.modified_count}")
        print(f"  - Upserted: {len(result.upserted_ids)}")
        print(f"  - Total records in '{db_name}.donors': {donors_collection.count_documents({})}")

        # Create indexes in MongoDB for fast queries
        donors_collection.create_index([("blood_group", 1)])
        donors_collection.create_index([("city", 1)])
        donors_collection.create_index([("is_available", 1)])
        donors_collection.create_index([("email", 1)], unique=True, sparse=True)
        print("[SUCCESS] Created MongoDB indexes on (blood_group, city, is_available, email).")

    # 3. Save sync metadata
    try:
        users = get_sqlite_users(sqlite_path)
    except Exception:
        users = []

    sync_record = {
        "sync_timestamp": datetime.utcnow().isoformat(),
        "total_donors_synced": len(donors),
        "total_users_count": len(users),
        "blood_group_breakdown": {},
        "source": "Jeevadhaara SQLite Database",
    }
    for d in donors:
        bg = d["blood_group"]
        sync_record["blood_group_breakdown"][bg] = sync_record["blood_group_breakdown"].get(bg, 0) + 1

    metadata_collection.insert_one(sync_record)
    print(f"[SUCCESS] Logged sync audit entry in '{db_name}.system_metadata'.")

    # Print summary
    print("\n" + "=" * 60)
    print("JEEVADHAARA DATA EXPORT TO MONGODB ATLAS COMPLETE")
    print("=" * 60)
    print(f"Cluster:       jeevadhaara.tzdqdn0.mongodb.net")
    print(f"Database:      {db_name}")
    print(f"Collection:    donors ({donors_collection.count_documents({})} documents)")
    print(f"Available:     {donors_collection.count_documents({'is_available': True})} donors")
    print("=" * 60)

    client.close()
    return True


def main():
    parser = argparse.ArgumentParser(description="Save all Jeevadhaara data to MongoDB Atlas.")
    parser.add_argument("--password", "-p", help="MongoDB Atlas user password")
    parser.add_argument("--uri", "-u", help="Full MongoDB connection string URI")
    parser.add_argument("--db", "-d", default=DEFAULT_DB_NAME, help="Target MongoDB database name (default: jeevadhaara)")
    parser.add_argument("--sqlite", default="db.sqlite3", help="Path to SQLite database file")
    args = parser.parse_args()

    try:
        uri = build_mongo_uri(args.uri, args.password)
        success = sync_to_mongodb(uri, args.db, args.sqlite)
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL ERROR]: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
