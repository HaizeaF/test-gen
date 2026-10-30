"""Tests for the section service."""

import pytest

from src.backend.models import Question, Section, Topic
from src.backend.models.errors import ConflictError, NotFoundError
from src.backend.repositories.unit_of_work import UnitOfWork
from src.backend.schemas.section import SectionCreate, SectionUpdate
from src.backend.services.section_service import SectionService


@pytest.fixture
def service(uow: UnitOfWork) -> SectionService:
    """A section service on the in-memory database."""
    return SectionService(uow)


def test_create_returns_the_section_with_its_topic_name(service: SectionService, topic: Topic) -> None:
    """Test that the section returned by create carries the name of its topic and is the one that get finds."""
    created = service.create(SectionCreate(topic_id=topic.id, name="Rivers"))

    assert created.topic_id == topic.id
    assert created.topic_name == "Geography"
    assert service.get(created.id) == created


def test_create_in_unknown_topic_raises_not_found_and_stores_nothing(service: SectionService) -> None:
    """Test that a missing topic raises NotFoundError, not ConflictError, and no section is left behind."""
    with pytest.raises(NotFoundError, match="Topic 999 not found"):
        service.create(SectionCreate(topic_id=999, name="Rivers"))

    assert service.get_all() == []


def test_get_unknown_section_raises_not_found(service: SectionService) -> None:
    """Test that asking for a section that does not exist raises NotFoundError."""
    with pytest.raises(NotFoundError, match="Section 999 not found"):
        service.get(999)


def test_update_moves_the_section_to_another_topic(service: SectionService, section: Section, other_topic: Topic) -> None:
    """Test that after a move both the returned section and the stored one show the new topic."""
    updated = service.update(section.id, SectionUpdate(topic_id=other_topic.id))

    assert updated.topic_name == "History"
    assert service.get(section.id).topic_name == "History"


def test_update_with_unknown_topic_raises_not_found_and_applies_nothing(service: SectionService, section: Section) -> None:
    """Test that a missing target topic stops the whole update, including the other fields sent with it."""
    with pytest.raises(NotFoundError, match="Topic 999 not found"):
        service.update(section.id, SectionUpdate(name="Cities", topic_id=999))

    stored = service.get(section.id)
    assert stored.name == "Capitals"
    assert stored.topic_name == "Geography"


def test_update_to_a_topic_with_the_same_section_name_raises_conflict(
    service: SectionService, section: Section, other_topic: Topic
) -> None:
    """Test that a move that creates a duplicate name raises ConflictError and the section stays where it was."""
    service.create(SectionCreate(topic_id=other_topic.id, name="Capitals"))

    with pytest.raises(ConflictError):
        service.update(section.id, SectionUpdate(topic_id=other_topic.id))

    assert service.get(section.id).topic_name == "Geography"


def test_delete_removes_the_section(service: SectionService, section: Section) -> None:
    """Test that a deleted section can no longer be found."""
    section_id = section.id

    service.delete(section_id)

    with pytest.raises(NotFoundError):
        service.get(section_id)


def test_delete_section_with_questions_raises_conflict_and_keeps_it(
    service: SectionService, section: Section, question: Question
) -> None:
    """Test that a section with questions is not deleted and the error says how many it has."""
    section_id = section.id

    with pytest.raises(ConflictError, match=r"1 question\(s\)"):
        service.delete(section_id)

    assert service.get(section_id).name == "Capitals"
