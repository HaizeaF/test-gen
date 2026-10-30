"""Service responsible for section-related bussiness logic."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from src.backend.schemas.section import SectionCreate, SectionUpdate, SectionRead
from src.backend.models import Topic, Section, Question
from src.backend.services.errors import ConflictError
from src.backend.services.common import apply_updates, commit, get, count_rows


class SectionService:
    def __init__(self, session: Session) -> None:
        """Initialize the service with a database session."""
        self.session = session

    def create(self, section_create: SectionCreate) -> SectionRead:
        """Create a new section."""
        get(self.session, Topic, section_create.topic_id)
        section = Section(**section_create.model_dump())

        self.session.add(section)
        commit(self.session, f"That topic already has a section named '{section_create.name}'.")

        return self._to_read(section)

    def get(self, section_id: int) -> SectionRead:
        """Retrieve a section by its identifier."""
        return self._to_read(get(self.session, Section, section_id))

    def get_all(self) -> list[SectionRead]:
        statement = select(Section).options(joinedload(Section.topic)).order_by(Section.id)
        sections = self.session.scalars(statement)
        return [self._to_read(section) for section in sections]

    def update(self, section_id: int, section_update: SectionUpdate) -> SectionRead:
        """Update an existing section."""
        section = self.get(section_id)
        if section_update.topic_id is not None:
            get(self.session, Topic, section_update.topic_id)
        
        apply_updates(section, section_update)
        commit(self.session, f"That topic already has a section named '{section_update.name}'.")

        return section

    def delete(self, section_id: int) -> None:
        """Delete a section."""
        section = self.get(section_id)
        questions = count_rows(self.session, Question, Question.section_id == section_id)

        if questions:
            raise ConflictError(f"The section '{section.name}' still has {questions} question(s). Delete or move them first.")
        
        self.session.delete(section)
        commit(self.session, f"The section '{section.name}' could not be deleted.")

    @staticmethod
    def _to_read(section: Section) -> SectionRead:
        return SectionRead(id=section.id, name=section.name, topic_id=section.topic_id, topic_name=section.topic.name)