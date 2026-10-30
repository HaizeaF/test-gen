"""Service responsible for section-related business logic."""

from src.backend.models import Section
from src.backend.models.errors import ConflictError
from src.backend.repositories.unit_of_work import UnitOfWork
from src.backend.schemas.section import SectionCreate, SectionRead, SectionUpdate


class SectionService:
    """Applies the business rules of sections."""

    def __init__(self, uow: UnitOfWork) -> None:
        """Initialize the service with a unit of work."""
        self.uow = uow

    def create(self, section_create: SectionCreate) -> SectionRead:
        """Create a new section inside an existing topic."""
        self.uow.topics.get(section_create.topic_id)
        section = self.uow.sections.add(Section(**section_create.model_dump()))
        self.uow.commit(f"The topic '{section_create.topic_id}' already has a section named '{section_create.name}'.")

        return SectionRead.model_validate(section)

    def get(self, section_id: int) -> SectionRead:
        """Retrieve a section by its identifier."""
        return SectionRead.model_validate(self.uow.sections.get(section_id))

    def get_all(self) -> list[SectionRead]:
        """Retrieve every section."""
        return [SectionRead.model_validate(section) for section in self.uow.sections.get_all()]

    def update(self, section_id: int, section_update: SectionUpdate) -> SectionRead:
        """Update an existing section."""
        section = self.uow.sections.get(section_id)

        if section_update.topic_id is not None:
            self.uow.topics.get(section_update.topic_id)

        self.uow.sections.update(section, section_update.changes())
        self.uow.commit(f"The topic '{section_update.topic_id}' already has a section named '{section_update.name}'.")

        return SectionRead.model_validate(section)

    def delete(self, section_id: int) -> None:
        """Delete a section that has no questions."""
        section = self.uow.sections.get(section_id)
        questions = self.uow.questions.count_by_section(section_id)

        if questions:
            raise ConflictError(f"The section '{section.name}' still has {questions} question(s). Delete or move them first.")

        self.uow.sections.delete(section)
        self.uow.commit(f"The section '{section.name}' could not be deleted.")
