"""Tests for the topic service."""

import pytest

from src.backend.models import Section, Topic
from src.backend.models.errors import ConflictError, NotFoundError
from src.backend.repositories.unit_of_work import UnitOfWork
from src.backend.schemas.topic import TopicCreate, TopicUpdate
from src.backend.services.topic_service import TopicService


@pytest.fixture
def service(uow: UnitOfWork) -> TopicService:
    """A topic service on the in-memory database."""
    return TopicService(uow)


def test_create_returns_the_stored_topic(service: TopicService) -> None:
    """Test that the topic returned by create has an id and is the same one that get finds."""
    created = service.create(TopicCreate(name="Maths"))

    assert created.id is not None
    assert created.name == "Maths"
    assert service.get(created.id) == created


def test_get_unknown_topic_raises_not_found(service: TopicService) -> None:
    """Test that asking for a topic that does not exist raises NotFoundError."""
    with pytest.raises(NotFoundError, match="Topic 999 not found"):
        service.get(999)


def test_update_renames_the_topic(service: TopicService, topic: Topic) -> None:
    """Test that update returns the new name and that the new name is what get finds afterwards."""
    updated = service.update(topic.id, TopicUpdate(name="Maps"))

    assert updated.name == "Maps"
    assert service.get(topic.id).name == "Maps"


def test_update_to_existing_name_raises_conflict_and_keeps_the_old_name(service: TopicService, topic: Topic) -> None:
    """Test that a name clash raises ConflictError and the rollback leaves the topic as it was."""
    other = service.create(TopicCreate(name="History"))

    with pytest.raises(ConflictError):
        service.update(other.id, TopicUpdate(name="Geography"))

    assert service.get(other.id).name == "History"


def test_delete_removes_the_topic(service: TopicService, topic: Topic) -> None:
    """Test that a deleted topic can no longer be found."""
    topic_id = topic.id

    service.delete(topic_id)

    with pytest.raises(NotFoundError):
        service.get(topic_id)


def test_delete_topic_with_sections_raises_conflict_and_keeps_it(service: TopicService, section: Section) -> None:
    """Test that a topic with sections is not deleted and the error says how many it has."""
    topic_id = section.topic_id

    with pytest.raises(ConflictError, match=r"1 section\(s\)"):
        service.delete(topic_id)

    assert service.get(topic_id).name == "Geography"
