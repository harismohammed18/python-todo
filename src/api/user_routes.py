"""
User API routes module.

This module defines the FastAPI routes for user-related operations including
creating and retrieving users. It handles dependency injection for services
and repositories.
"""

from fastapi import APIRouter, Depends, Request

from src.models.user_model import User
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

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
    user_id = await service.create_user(user)
    return {"id": user_id}


@router.get("/users/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
) -> dict | None:
    """
    Retrieve a user by ID.

    Args:
        user_id: The MongoDB ObjectId of the user as a string
        service: UserService instance from dependency injection

    Returns:
        dict: User document with id, name, and email, or None if not found

    Raises:
        InvalidId: If user_id is not a valid ObjectId format
    """
    return await service.get_user(user_id)
