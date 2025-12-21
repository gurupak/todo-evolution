"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str

    # Authentication
    better_auth_secret: str

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000


# Global settings instance
settings = Settings()
