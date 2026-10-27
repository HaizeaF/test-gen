"""Tests for the configuration."""

from src.backend.config.config import Config


def test_base_dir_is_the_project_root() -> None:
    """Test that BASE_DIR is computed from this file's location."""
    assert (Config.BASE_DIR / "pyproject.toml").is_file()
    assert (Config.BASE_DIR / "alembic.ini").is_file()
