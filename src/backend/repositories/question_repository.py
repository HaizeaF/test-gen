"""Data access for questions."""

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.backend.models import Answer, Question, Section
from src.backend.repositories.base_repository import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    """Reads and writes questions. Their section and topic is always loaded with them."""

    model = Question
    load_options = (joinedload(Question.section).joinedload(Section.topic),)

    def get_all(self) -> list[Question]:
        """Return every question, ordered by flagged and id."""

        statement = select(Question).options(*self.load_options).order_by(Question.flagged.desc(), Question.id.desc())
        return list(self.session.scalars(statement))

    def count_by_section(self, section_id: int) -> int:
        """Count the questions that belong to a section."""
        return self._count(Question, Question.section_id == section_id)

    def count_answers(self, question_id: int) -> int:
        """Count the answers given to a question."""
        return self._count(Answer, Answer.question_id == question_id)
