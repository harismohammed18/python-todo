"""
Script to insert sample users into the database.

This script creates 10 sample users and inserts them into the MongoDB database.
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.db import Database as MongoDB  # pylint: disable=wrong-import-position
from src.repositories.user_repository import UserRepository  # pylint: disable=wrong-import-position

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

# Sample users data
SAMPLE_USERS = [
    {"name": "John Doe", "email": "john.doe@example.com"},
    {"name": "Jane Smith", "email": "jane.smith@example.com"},
    {"name": "Bob Johnson", "email": "bob.johnson@example.com"},
    {"name": "Alice Williams", "email": "alice.williams@example.com"},
    {"name": "Charlie Brown", "email": "charlie.brown@example.com"},
    {"name": "Diana Prince", "email": "diana.prince@example.com"},
    {"name": "Eve Davis", "email": "eve.davis@example.com"},
    {"name": "Frank Miller", "email": "frank.miller@example.com"},
    {"name": "Grace Lee", "email": "grace.lee@example.com"},
    {"name": "Henry Wilson", "email": "henry.wilson@example.com"},
]


async def insert_sample_users():
    """Insert 10 sample users into the database."""
    db = MongoDB(MONGO_URL, DB_NAME)
    repo = UserRepository(db.db)

    print(f"Inserting {len(SAMPLE_USERS)} sample users into database...")

    for user in SAMPLE_USERS:
        user_id = await repo.create(user)
        print(f"✓ Created user: {user['name']} ({user_id})")

    print(f"\n✓ Successfully inserted {len(SAMPLE_USERS)} users")
    await db.close_connection()


if __name__ == "__main__":
    asyncio.run(insert_sample_users())
