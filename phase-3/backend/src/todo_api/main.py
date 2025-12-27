"""FastAPI main application."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import chat, tasks

# Set OpenAI API key for the agents SDK
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Web Application Backend",
    version="1.0.0",
)

# Configure CORS
cors_origins = [
    settings.frontend_url,
    "http://localhost:3000",  # Local development
    "http://localhost:3001",  # Alternative local port
    "https://noble-perfection-production-7c4a.up.railway.app",  # Production frontend
]

# Add the production frontend domain if not already included
if settings.frontend_url not in cors_origins:
    cors_origins.append(settings.frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register routers
app.include_router(tasks.router)
app.include_router(chat.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Todo API - Phase II", "version": "1.0.0"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
