"""
Database module for MongoDB integration with FastAPI.

This module provides database connection management and base models for MongoDB operations.
It includes AsyncIOMotorClient setup for asynchronous MongoDB operations and a base
Pydantic model with ObjectId support for MongoDB documents.
"""

import logging

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class Database:
    """Database connection and operations."""

    def __init__(self, uri: str, db_name: str):
        """
        Initialize database connection.

        Args:
            uri: MongoDB connection URI
            db_name: Database name
        """
        logger.debug("Initializing Database with URI and db_name: %s", db_name)
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.db_name = db_name
        logger.info("Database instance created for: %s", db_name)

    def get_database(self):
        """
        Get the database instance.

        Returns:
            Motor database instance
        """
        return self.db

    async def close_connection(self):
        """Close the database connection."""
        logger.info("Closing database connection")
        self.client.close()
        logger.info("Database connection closed")
