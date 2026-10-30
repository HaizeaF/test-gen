"""Data access for topics."""

from sqlalchemy import select

from src.backend.models import Topic
from src.backend.repositories.base_repository import BaseRepository


class TopicRepository(BaseRepository[Topic]):
    """Reads and writes topics."""

    model = Topic

    def get_all(self) -> list[Topic]:
        """Return every topic ordered by id."""

        statement = select(Topic).order_by(Topic.id.desc())
        return list(self.session.scalars(statement))
