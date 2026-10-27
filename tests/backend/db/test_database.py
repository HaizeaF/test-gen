"""Tests for the database configuration."""

import pytest
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.backend.models import Section


def test_sqlite_enforces_foreign_keys(engine: Engine) -> None:
    """Test that SQLite enforces foreign key constraints."""
    with engine.connect() as connection:
        assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar() == 1


def test_section_needs_an_existing_topic(session: Session) -> None:
    """Test that a section pointing to a topic that does not exist cannot be stored."""
    session.add(Section(topic_id=999, name="capitals"))

    with pytest.raises(IntegrityError):
        session.flush()
