"""Service responsible for topic-related business logic."""

from src.backend.models import Topic
from src.backend.models.errors import ConflictError
from src.backend.repositories.unit_of_work import UnitOfWork
from src.backend.schemas.topic import TopicCreate, TopicRead, TopicUpdate


class TopicService:
    """Applies the business rules of topics."""

    def __init__(self, uow: UnitOfWork) -> None:
        """Initialize the service with a unit of work."""
        self.uow = uow

    def create(self, topic_create: TopicCreate) -> TopicRead:
        """Create a new topic."""
        topic = self.uow.topics.add(Topic(name=topic_create.name))
        self.uow.commit(f"A topic named '{topic_create.name}' already exists.")

        return TopicRead.model_validate(topic)

    def get(self, topic_id: int) -> TopicRead:
        """Retrieve a topic by its identifier."""
        return TopicRead.model_validate(self.uow.topics.get(topic_id))

    def get_all(self) -> list[TopicRead]:
        """Retrieve every topic."""
        return [TopicRead.model_validate(topic) for topic in self.uow.topics.get_all()]

    def update(self, topic_id: int, topic_update: TopicUpdate) -> TopicRead:
        """Update an existing topic."""
        topic = self.uow.topics.get(topic_id)

        self.uow.topics.update(topic, topic_update.changes())
        self.uow.commit("A topic with that name already exists.")

        return TopicRead.model_validate(topic)

    def delete(self, topic_id: int) -> None:
        """Delete a topic that has no sections."""
        topic = self.uow.topics.get(topic_id)
        sections = self.uow.sections.count_by_topic(topic_id)

        if sections:
            raise ConflictError(f"The topic '{topic.name}' still has {sections} section(s). Delete or move them first.")

        self.uow.topics.delete(topic)
        self.uow.commit(f"The topic '{topic.name}' could not be deleted.")
