"""Service responsible for question-related business logic."""

from src.backend.models import Question
from src.backend.models.errors import ConflictError
from src.backend.repositories.unit_of_work import UnitOfWork
from src.backend.schemas.question import QuestionCreate, QuestionRead, QuestionUpdate


class QuestionService:
    """Applies the business rules of questions."""

    def __init__(self, uow: UnitOfWork) -> None:
        """Initialize the service with a unit of work."""
        self.uow = uow

    def create(self, question_create: QuestionCreate) -> QuestionRead:
        """Create a new question."""
        self.uow.sections.get(question_create.section_id)
        question = self.uow.questions.add(Question(**question_create.model_dump()))
        self.uow.commit("The question could not be saved.")

        return QuestionRead.model_validate(question)

    def get(self, question_id: int) -> QuestionRead:
        """Retrieve a question by its identifier."""
        return QuestionRead.model_validate(self.uow.questions.get(question_id))

    def get_all(self) -> list[QuestionRead]:
        """Retrieve every question."""
        return [QuestionRead.model_validate(question) for question in self.uow.questions.get_all()]

    def update(self, question_id: int, question_update: QuestionUpdate) -> QuestionRead:
        """Update an existing question."""
        question = self.uow.questions.get(question_id)

        if question_update.section_id is not None:
            self.uow.sections.get(question_update.section_id)

        self.uow.questions.update(question, question_update.changes())
        self.uow.commit("The question could not be saved.")

        return QuestionRead.model_validate(question)

    def delete(self, question_id: int) -> None:
        """Delete a question that has no answers."""
        question = self.uow.questions.get(question_id)
        answers = self.uow.questions.count_answers(question_id)

        if answers:
            raise ConflictError(f"The question has {answers} answer(s).")

        self.uow.questions.delete(question)
        self.uow.commit("The question could not be deleted.")
