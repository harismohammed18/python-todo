"""
User repository module for database operations.

This module provides the UserRepository class for handling all user-related
database operations including creating, retrieving, and managing user documents
in MongoDB.
"""

import logging

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

# pylint: disable=logging-fstring-interpolation
logger = logging.getLogger(__name__)


class UserRepository:
    """
    Repository class for user database operations.

    This class handles all CRUD operations for user documents in MongoDB,
    providing an abstraction layer between the application logic and the database.

    Attributes:
        collection: MongoDB users collection reference
    """

    def __init__(self, db) -> None:
        """
        Initialize the UserRepository with a database instance.

        Args:
            db: Database instance with access to MongoDB collections
        """
        self.collection = db.users
        logger.debug("UserRepository initialized with collection: users")

    async def create(self, user_data: dict) -> str:
        """
        Create a new user document in the database.

        Args:
            user_data: Dictionary containing user information

        Returns:
            str: The ObjectId of the newly created user as a string
        """
        logger.info("Creating new user in database")
        result = await self.collection.insert_one(user_data)
        user_id = str(result.inserted_id)
        logger.info("User created successfully with ID: %s", user_id)
        return user_id

    async def get_by_id(self, user_id: str) -> dict | None:
        """
        Retrieve a user document by its ID.

        Args:
            user_id: The MongoDB ObjectId of the user as a string

        Returns:
            dict: User document with _id as string, or None if not found

        Raises:
            HTTPException: If user_id is not a valid ObjectId format (400 status)
        """
        logger.debug("Retrieving user with ID: %s", user_id)
        try:
            obj_id = ObjectId(user_id)
        except InvalidId as exc:
            logger.warning("Invalid user ID format provided: %s", user_id)
            raise HTTPException(
                status_code=400,
                detail=f"Invalid user ID format: '{user_id}'. Must be a valid MongoDB ObjectId.",
            ) from exc

        user = await self.collection.find_one({"_id": obj_id})
        if user:
            user["_id"] = str(user["_id"])
            logger.info("User found with ID: %s", user_id)
        else:
            logger.warning("User not found with ID: %s", user_id)
        return user

    async def find_all(self) -> list[dict]:
        """
        Retrieve all user documents from the database.

        Returns:
            list[dict]: All user documents with _id as string
                       (empty list if collection is empty)
        """
        logger.info("Retrieving all users from database")
        users = await self.collection.find().to_list(length=None)
        for user in users:
            user["_id"] = str(user["_id"])
        logger.info(f"Retrieved {len(users)} users from database")
        return users
