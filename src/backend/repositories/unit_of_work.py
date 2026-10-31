"""The repositories of one request and the commit that saves their changes together."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.backend.models.errors import ConflictError
from src.backend.repositories.question_repository import QuestionRepository
from src.backend.repositories.section_repository import SectionRepository
from src.backend.repositories.topic_repository import TopicRepository


class UnitOfWork:
    """Gives the services every repository on one shared session and decides when the changes are saved."""

    def __init__(self, session: Session) -> None:
        """Initialize the repositories with the same database session."""
        self.session = session
        self.topics = TopicRepository(session)
        self.sections = SectionRepository(session)
        self.questions = QuestionRepository(session)

    def commit(self, conflict_message: str) -> None:
        """Commit. If the database refuses (unique or foreign key), roll back and raise ConflictError."""
        try:
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            raise ConflictError(conflict_message) from error
