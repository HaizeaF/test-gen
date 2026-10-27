"""Tests that keep Alembic migrations and ORM models in sync."""

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config as AlembicConfig
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, inspect

from src.backend.config.config import Config
from src.backend.models import Base


def _alembic_config(url: str) -> AlembicConfig:
    """Build an Alembic config pointing to a temporary database."""
    config = AlembicConfig(str(Config.BASE_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(Config.BASE_DIR / "src/backend/db/migrations"))
    config.set_main_option("sqlalchemy.url", url)

    return config


def test_upgrade_downgrade(tmp_path) -> None:
    """Test that Alembic migrations can be applied and reverted."""
    url = f"sqlite:///{tmp_path / 'test.db'}"
    command.upgrade(_alembic_config(url), "head")

    assert "answers" in inspect(create_engine(url)).get_table_names()

    command.downgrade(_alembic_config(url), "base")

    assert "answers" not in inspect(create_engine(url)).get_table_names()


def test_models_match_migrations(tmp_path) -> None:
    """Test that the ORM models match the Alembic migrations."""
    url = f"sqlite:///{tmp_path / 'test.db'}"
    command.upgrade(_alembic_config(url), "head")
    engine = create_engine(url)

    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        diff = compare_metadata(context, Base.metadata)

    assert not diff
