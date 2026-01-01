"""
User API routes module.

This module defines the FastAPI routes for user-related operations including
creating and retrieving users. It handles dependency injection for services
and repositories.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from src.models.user_model import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["users"])


def get_user_service(request: Request) -> UserService:
    """
    Dependency injection function for UserService.

    Creates and returns a UserService instance with properly initialized
    repository and database connection.

    Args:
        request: FastAPI request object containing database in app state

    Returns:
        UserService: Configured service instance for user operations
    """
    logger.debug("Creating UserService instance via dependency injection")
    db = request.app.state.mongodb.db
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/users", response_model=dict, status_code=201)
async def create_user(
    user: User,
    service: UserService = Depends(get_user_service),
) -> dict:
    """
    Create a new user.

    Args:
        user: User model containing name and email
        service: UserService instance from dependency injection

    Returns:
        dict: Response containing the newly created user's ID

    Raises:
        ValidationError: If user data is invalid (missing/invalid fields)
    """
    logger.info("API: POST /api/users - Creating new user")
    user_id = await service.create_user(user)
    logger.info("API: User created successfully with ID: %s", user_id)
    return {"id": user_id}


@router.get("/users", response_model=list[dict])
async def get_all_users(
    service: UserService = Depends(get_user_service),
) -> list[dict]:
    """
    Retrieve all users.

    Args:
        service: UserService instance from dependency injection

    Returns:
        list[dict]: All user documents with id, name, and email
                   (empty list if no users found)
    """
    logger.info("API: GET /api/users - Retrieving all users")
    users = await service.get_all_users()
    logger.info("API: Retrieved %d users", len(users))
    return users


@router.get("/users/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> dict:
    """
    Retrieve a user by ID.

    Args:
        user_id: The MongoDB ObjectId of the user as a string
        service: UserService instance from dependency injection

    Returns:
        dict: User document with id, name, and email

    Raises:
        HTTPException: 404 if user not found
        HTTPException: 400 if user_id is not a valid ObjectId format
    """
    logger.info("API: GET /api/users/%s - Retrieving user", user_id)
    user = await service.get_user(user_id)
    if user:
        logger.info("API: User found with ID: %s", user_id)
        return user
    logger.warning("API: User not found with ID: %s", user_id)
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
