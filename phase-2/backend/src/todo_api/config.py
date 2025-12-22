"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str

    # Authentication
    better_auth_secret: str

    # CORS - Updated for production
    frontend_url: str = "http://localhost:3000"

    # For Railway deployment, you might want to set this to the production frontend URL
    # but it's better to make it configurable
    production_frontend_url: str = "https://noble-perfection-production-7c4a.up.railway.app"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000


# Global settings instance
settings = Settings()
