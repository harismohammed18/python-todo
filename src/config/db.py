"""
Database module for MongoDB integration with FastAPI.

This module provides database connection management and base models for MongoDB operations.
It includes AsyncIOMotorClient setup for asynchronous MongoDB operations and a base
Pydantic model with ObjectId support for MongoDB documents.
"""

from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    """Database connection and operations."""

    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def close_connection(self):
        """Close the database connection."""
        self.client.close()
