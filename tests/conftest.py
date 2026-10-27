"""Shared pytest fixures."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.backend.db.database import get_session
from src.backend.main import app
from src.backend.models.base import Base


@pytest.fixture
def engine() -> Iterator[Engine]:
    """A fresh in-memory database for every test, so tests cannot leak data into each other."""
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """Create a new database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """Test client whose database dependency uses the in-memory session."""
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
