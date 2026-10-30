"""Service responsible for topic-related bussiness logic."""

from sqlalchemy import select
from sqlalchemy.orm import Session
from src.backend.schemas.topic import TopicCreate, TopicUpdate, TopicRead
from src.backend.models import Topic, Section
from src.backend.services.errors import ConflictError
from src.backend.services.common import apply_updates, commit, get, count_rows


class TopicService:
    def __init__(self, session: Session) -> None:
        """Initialize the service with a database session."""
        self.session = session

    def create(self, topic_create: TopicCreate) -> TopicRead:
        """Create a new topic."""
        topic = Topic(name=topic_create.name)

        self.session.add(topic)
        commit(self.session, f"A topic named '{topic_create.name}' already exists.")

        return self._to_read(topic)

    def get(self, topic_id: int) -> TopicRead:
        """Retrieve a topic by its identifier."""
        return self._to_read(get(self.session, Topic, topic_id))

    def get_all(self) -> list[TopicRead]:
        statement = select(Topic).order_by(Topic.id)
        topics = self.session.scalars(statement)
        return [self._to_read(topic) for topic in topics]

    def update(self, topic_id: int, topic_update: TopicUpdate) -> TopicRead:
        """Update an existing topic."""
        topic = self.get(topic_id)
        apply_updates(topic, topic_update)
        commit(self.session,  f"A topic named '{topic_update.name}' already exists.")

        return topic

    def delete(self, topic_id: int) -> None:
        """Delete a topic."""
        topic = self.get(topic_id)
        sections = count_rows(self.session, Section, Section.topic_id == topic_id)

        if sections:
            raise ConflictError(f"The topic '{topic.name}' still has {sections} section(s). Delete or move them first.")
        
        self.session.delete(topic)
        commit(self.session, f"The topic '{topic.name}' could not be deleted.")

    @staticmethod
    def _to_read(topic: Topic) -> TopicRead:
        return TopicRead.model_validate(topic)