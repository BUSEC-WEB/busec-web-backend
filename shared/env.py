from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Every value comes from the root .env (see .env.example)
    so a missing key stops the app at startup with the key's name."""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    DATABASE_CONNECTION_STRING: str = Field(default=...)
    DEBUG: bool = Field(default=...)
    SECRET_KEY: str = Field(default=...)
    SECURE_MODE: bool = False
    ALLOWED_HOSTS: list[str] = []
    CORS_ALLOWED_ORIGINS: list[str] = []

    # S3-compatible object storage (MinIO in dev, any S3 provider in production).
    S3_ENDPOINT: str = Field(default=...)
    S3_SECURE: bool = True
    S3_ACCESS_KEY: str = Field(default=...)
    S3_SECRET_KEY: str = Field(default=...)
    S3_MAGAZINE_BUCKET: str = Field(default=...)
    S3_COVER_IMAGE_BUCKET: str = Field(default=...)


settings = Settings()
