from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# shared/env.py -> repo root
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
    # JSON lists in .env, e.g. ALLOWED_HOSTS=["api.busec.online"]
    ALLOWED_HOSTS: list[str] = []
    CORS_ALLOWED_ORIGINS: list[str] = []


settings = Settings()
