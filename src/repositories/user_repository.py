"""
User repository module for database operations.

This module provides the UserRepository class for handling all user-related
database operations including creating, retrieving, and managing user documents
in MongoDB.
"""

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException


class UserRepository:
    """
    Repository class for user database operations.

    This class handles all CRUD operations for user documents in MongoDB,
    providing an abstraction layer between the application logic and the database.

    Attributes:
        collection: MongoDB users collection reference
    """

    def __init__(self, db):
        """
        Initialize the UserRepository with a database instance.

        Args:
            db: Database instance with access to MongoDB collections
        """
        self.collection = db.users

    async def create(self, user_data: dict) -> str:
        """
        Create a new user document in the database.

        Args:
            user_data: Dictionary containing user information

        Returns:
            str: The ObjectId of the newly created user as a string
        """
        result = await self.collection.insert_one(user_data)
        return str(result.inserted_id)

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
        try:
            obj_id = ObjectId(user_id)
        except InvalidId as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid user ID format: '{user_id}'. Must be a valid MongoDB ObjectId.",
            ) from exc

        user = await self.collection.find_one({"_id": obj_id})
        if user:
            user["_id"] = str(user["_id"])
        return user
