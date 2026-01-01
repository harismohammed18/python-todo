"""
User service module for business logic operations.

This module contains the UserService class which handles user-related business logic,
including user creation and retrieval. It acts as a bridge between the API routes
and the repository layer, providing abstraction and data transformation.
"""

import logging

from src.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    """
    Service class for user business logic operations.

    This class encapsulates the business logic for user management, handling
    data transformation between request/response models and database operations.

    Attributes:
        repo: UserRepository instance for database operations
    """

    def __init__(self, repo: UserRepository):
        """
        Initialize the UserService with a repository instance.

        Args:
            repo: UserRepository instance for accessing user data
        """
        self.repo = repo
        logger.debug("UserService initialized with repository")

    async def create_user(self, user) -> str:
        """
        Create a new user with the provided data.

        Converts the Pydantic user model to a dictionary with MongoDB field aliases
        and delegates to the repository for database insertion.

        Args:
            user: User model instance containing user information

        Returns:
            str: The ID of the newly created user
        """
        logger.info("Service: Creating new user")
        user_id = await self.repo.create(user.dict(by_alias=True))
        logger.info("Service: User created successfully with ID: %s", user_id)
        return user_id

    async def get_user(self, user_id: str) -> dict | None:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The MongoDB ObjectId of the user as a string

        Returns:
            dict: User document with all fields, or None if user not found
        """
        logger.info("Service: Fetching user with ID: %s", user_id)
        user = await self.repo.get_by_id(user_id)
        if user:
            logger.info("Service: User found with ID: %s", user_id)
        else:
            logger.warning("Service: User not found with ID: %s", user_id)
        return user

    async def get_all_users(self) -> list[dict]:
        """
        Retrieve all user documents.

        Returns:
            list[dict]: All User documents with all fields (empty list if no users found)
        """
        logger.info("Service: Fetching all users")
        users = await self.repo.find_all()
        logger.info("Service: Retrieved %d users", len(users))
        return users
