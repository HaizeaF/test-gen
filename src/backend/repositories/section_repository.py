"""Data access for sections."""

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.backend.models import Section
from src.backend.repositories.base_repository import BaseRepository


class SectionRepository(BaseRepository[Section]):
    """Reads and writes sections. Their topic is always loaded with them."""

    model = Section
    load_options = (joinedload(Section.topic),)

    def get_all(self) -> list[Section]:
        """Return every section ordered by id."""

        statement = select(Section).options(*self.load_options).order_by(Section.id.desc())
        return list(self.session.scalars(statement))

    def count_by_topic(self, topic_id: int) -> int:
        """Count the sections that belong to a topic."""
        return self._count(Section, Section.topic_id == topic_id)
