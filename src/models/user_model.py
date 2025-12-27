"""
User model module for user data validation and serialization.

This module defines Pydantic models for user-related operations in the FastAPI application.
It includes request/response models with MongoDB ObjectId support and field validation.
"""

from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    """
    User model for request and response validation.

    Attributes:
        id: MongoDB ObjectId as a string, aliased as _id for MongoDB compatibility
        name: User's full name (required, non-empty string)
        email: User's email address (required, valid email format)

    Configuration:
        - populate_by_name: Allows both field name and alias (_id) for population
        - json_encoders: Custom JSON encoding for ObjectId to string

    Raises:
        ValidationError: If name or email are missing or invalid
    """

    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(..., min_length=1, description="User's full name")
    email: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", description="User's email address")

    class Config:
        """Pydantic model configuration for MongoDB document handling."""

        populate_by_name = True
        json_encoders = {ObjectId: str}
