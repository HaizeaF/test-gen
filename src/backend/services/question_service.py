"""Service responsible for question-related business logic."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.backend.models import Answer, Question, Section
from src.backend.schemas.enums import Option
from src.backend.schemas.question import QuestionCreate, QuestionUpdate, QuestionRead
from src.backend.services.errors import ConflictError
from src.backend.services.common import apply_updates, commit, count_rows, get


class QuestionService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, question_create: QuestionCreate) -> QuestionRead:
        """Create a new question."""
        get(self.session, Section, question_create.section_id)
        question = Question(**question_create.model_dump())

        self.session.add(question)
        commit(self.session, "The question could not be saved.")

        return self._to_read(question)

    def get(self, question_id: int) -> QuestionRead:
        """Retrieve a question by its identifier."""
        return self._to_read(get(self.session, Question, question_id))

    def get_all(self) -> list[QuestionRead]:
        statement = select(Question).options(joinedload(Question.section).joinedload(Section.topic)).order_by(Question.id)
        questions = self.session.scalars(statement)
        return [self._to_read(question) for question in questions]

    def update(self, question_id: int, question_update: QuestionUpdate) -> QuestionRead:
        """Update an existing question."""
        question = self.get(question_id)
        if question_update.section_id is not None:
            get(self.session, Section, question_update.section_id)
        
        apply_updates(question, question_update)
        commit(self.session, "The question could not be saved.")

        return question

    def delete(self, question_id: int) -> None:
        """Delete a question."""
        question = self.get(question_id)
        answers = count_rows(self.session, Answer, Answer.question_id == question_id)

        if answers:
            raise ConflictError(f"The question has {answers} answer(s).")
        
        self.session.delete(question)
        commit(self.session, "The question could not be deleted.")

    @staticmethod
    def _to_read(question: Question) -> QuestionRead:
        section = question.section
        return QuestionRead(
            id=question.id,
            section_id=question.section_id,
            section_name=section.name,
            topic_id=section.topic_id,
            topic_name=section.topic.name,
            text=question.text,
            option_a=question.option_a,
            option_b=question.option_b,
            option_c=question.option_c,
            option_d=question.option_d,
            correct_option=Option(question.correct_option),
            flagged=question.flagged
        )