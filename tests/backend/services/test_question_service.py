"""Tests for the question service."""

import pytest

from src.backend.models import Answer, Question, Section
from src.backend.models.errors import ConflictError, NotFoundError
from src.backend.repositories.unit_of_work import UnitOfWork
from src.backend.schemas.enums import Option
from src.backend.schemas.question import QuestionCreate, QuestionUpdate
from src.backend.services.question_service import QuestionService


@pytest.fixture
def service(uow: UnitOfWork) -> QuestionService:
    """A question service on the in-memory database."""
    return QuestionService(uow)


def build_create(section_id: int) -> QuestionCreate:
    """Build a valid question to create inside the given section."""
    return QuestionCreate(
        section_id=section_id,
        text="What is the capital of France?",
        option_a="Paris",
        option_b="Rome",
        option_c="Madrid",
        option_d="Berlin",
        correct_option=Option.A,
    )


def test_create_returns_an_active_unflagged_question_with_its_names(service: QuestionService, section: Section) -> None:
    """Test that a new question starts active and not flagged, shows its section and topic, and is the one get finds."""
    created = service.create(build_create(section.id))

    assert created.section_name == "Capitals"
    assert created.topic_name == "Geography"
    assert created.correct_option == Option.A
    assert created.flagged is False
    assert created.active is True
    assert service.get(created.id) == created


def test_create_in_unknown_section_raises_not_found_and_stores_nothing(service: QuestionService) -> None:
    """Test that a missing section raises NotFoundError and no question is left behind."""
    with pytest.raises(NotFoundError, match="Section 999 not found"):
        service.create(build_create(999))

    assert service.get_all() == []


def test_get_unknown_question_raises_not_found(service: QuestionService) -> None:
    """Test that asking for a question that does not exist raises NotFoundError."""
    with pytest.raises(NotFoundError, match="Question 999 not found"):
        service.get(999)


def test_update_moves_and_deactivates_the_question(service: QuestionService, question: Question, other_section: Section) -> None:
    """Test that a move and a deactivation sent together are applied and show up when the question is read again."""
    updated = service.update(question.id, QuestionUpdate(section_id=other_section.id, active=False))

    assert updated.section_name == "Wars"
    assert updated.topic_name == "History"
    assert updated.active is False
    assert service.get(question.id) == updated


def test_update_with_unknown_section_raises_not_found_and_applies_nothing(service: QuestionService, question: Question) -> None:
    """Test that a missing target section stops the whole update, including the other fields sent with it."""
    with pytest.raises(NotFoundError, match="Section 999 not found"):
        service.update(question.id, QuestionUpdate(section_id=999, text="New text"))

    stored = service.get(question.id)
    assert stored.text == "What is the capital of Italy?"
    assert stored.section_name == "Capitals"


def test_delete_removes_the_question(service: QuestionService, question: Question) -> None:
    """Test that a deleted question can no longer be found."""
    question_id = question.id

    service.delete(question_id)

    with pytest.raises(NotFoundError):
        service.get(question_id)


def test_delete_question_with_answers_raises_conflict_and_keeps_it(
    service: QuestionService, question: Question, answer: Answer
) -> None:
    """Test that an answered question is not deleted and the error says how many answers it has."""
    question_id = question.id

    with pytest.raises(ConflictError, match=r"1 answer\(s\)"):
        service.delete(question_id)

    assert service.get(question_id).text == "What is the capital of Italy?"
