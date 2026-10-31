"""Shared pytest fixtures."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.backend.db.database import get_session
from src.backend.main import app
from src.backend.models import Answer, Base, Question, QuizSession, Section, Topic
from src.backend.repositories.unit_of_work import UnitOfWork


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
def uow(session: Session) -> UnitOfWork:
    """A unit of work on the in-memory session."""
    return UnitOfWork(session)


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """Test client whose database dependency uses the in-memory session."""
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def topic(session: Session) -> Topic:
    """A topic named Geography."""
    topic = Topic(name="Geography")
    session.add(topic)
    session.commit()

    return topic


@pytest.fixture
def other_topic(session: Session) -> Topic:
    """A second topic named History, to test moves and name clashes between topics."""
    other_topic = Topic(name="History")
    session.add(other_topic)
    session.commit()

    return other_topic


@pytest.fixture
def section(session: Session, topic: Topic) -> Section:
    """A section named Capitals inside the Geography topic."""
    section = Section(topic=topic, name="Capitals")
    session.add(section)
    session.commit()

    return section


@pytest.fixture
def other_section(session: Session, other_topic: Topic) -> Section:
    """A second section named Wars inside the History topic, to test moving questions."""
    other_section = Section(topic=other_topic, name="Wars")
    session.add(other_section)
    session.commit()

    return other_section


@pytest.fixture
def question(session: Session, section: Section) -> Question:
    """A question inside the Capitals section."""
    question = Question(
        section=section,
        text="What is the capital of Italy?",
        option_a="Paris",
        option_b="Moscow",
        option_c="Rome",
        option_d="Berlin",
        correct_option="c",
    )
    session.add(question)
    session.commit()

    return question


@pytest.fixture
def answer(session: Session, question: Question) -> Answer:
    """One correct answer to the question, taken inside a quiz session."""
    quiz_session = QuizSession(mode="random")
    answer = Answer(session=quiz_session, question=question, selected_option="c", is_correct=True, time_spent_seconds=3.5)
    session.add(answer)
    session.commit()

    return answer
