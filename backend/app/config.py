"""PlantMind platform configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven PlantMind platform settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "PlantMind"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "Development"
    DEPLOYMENT_MODE: str = "On-Premise"

    DATABASE_URL: str | None = None
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"


settings = Settings()