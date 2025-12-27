"""
FastAPI Todo Application Entry Point

This module initializes the FastAPI application with MongoDB integration,
manages the application lifecycle (startup/shutdown), and includes all API routes.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from src.api.user_routes import router
from src.config.db import Database as MongoDB

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "fastapi_oop"


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events for the FastAPI application.

    Args:
        app_instance: FastAPI application instance

    Yields:
        None

    Startup phase:
        - Initializes MongoDB connection and stores it in app state

    Shutdown phase:
        - Closes MongoDB connection gracefully
    """
    # Startup
    app_instance.state.mongodb = MongoDB(MONGO_URL, DB_NAME)
    yield
    # Shutdown
    await app_instance.state.mongodb.close_connection()


app = FastAPI(
    title="Todo App",
    description="FastAPI application for managing todo items with MongoDB",
    version="1.0.0",
    lifespan=lifespan,
)


def get_db(request: Request):
    """
    Dependency function to retrieve the database instance.

    Args:
        request: FastAPI request object

    Returns:
        MongoDB database instance from application state
    """
    return request.app.state.mongodb.db


app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
