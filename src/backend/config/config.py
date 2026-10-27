"""Centralized configuration for the backend."""

import os
from pathlib import Path


class Config:
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parents[3]
    DATA_DIR: Path = BASE_DIR / "data"

    # Database
    DB_NAME: str = "test-gen.db"
    DB_URL: str = os.environ.get("DB_URL", f"sqlite:///{DATA_DIR / DB_NAME}")

    # Timestamps
    TIMEZONE: str = "Europe/Madrid"
