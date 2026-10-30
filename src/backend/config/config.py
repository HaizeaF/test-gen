"""Centralized configuration for the backend."""

import os
from pathlib import Path

from dotenv import load_dotenv

_BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(_BASE_DIR / ".env")


class Config:
    # Paths
    BASE_DIR: Path = _BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"

    # Database
    DB_NAME: str = "test-gen.db"
    DB_URL: str = os.environ.get("DB_URL", f"sqlite:///{DATA_DIR / DB_NAME}")

    # Timestamps
    TIMEZONE: str = "Europe/Madrid"

    # CORS
    CORS_ORIGINS: list[str] = [origin.strip() for origin in os.environ.get("CORS_ORIGINS", "").split(",") if origin.strip()]
